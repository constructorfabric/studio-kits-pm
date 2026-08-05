#!/usr/bin/env python3
"""Report a research run's cross-artifact coverage.

Where ``check_artifact_refs.py`` validates one artifact at a time, this
script reads the whole artifact set produced for a research request and
reports what no single-artifact check can see:

- **Flow coverage** — which artifact kinds exist for the run and which of
  the nine research flows remain uncommissioned (informational: not every
  request needs every flow).
- **Next-action execution** — for every candidate-register row, whether
  the recommended next action (profile, orientation card, dossier,
  comparison, OSS review, mechanism study, watch) has a matching artifact:
  done / partial / open / manual.
- **Evidence density** — per orientation card, profile, and dossier: the
  distinct EVD references it cites and the source classes they cover
  (landing, pricing, docs, repository, releases, corporate), with soft
  floor warnings (profile < 2, dossier < 4 distinct EVDs).
- **Fact ledgers** — profiles/dossiers whose company has no
  ``companies/COMP-*/facts.tsv`` ledger (warning: repeat passes lose the
  as-of history).
- **Exports** — expected csv/html exports that are missing.
- **Watch freshness** — the latest watch pass date plus its cadence, and
  whether the next pass is due.
- **Traceability sweep** — artifact IDs missing from the request's
  Traceability section.

The output is a plain-text report for the cf-compete-review workflow; the
summary line is stable for scripting:
``check_coverage: N/9 flow(s) covered, M open next action(s), K warning(s)``

This is a report, not a gate: an open next action is research routing,
not a defect. Exit codes: 0 = report produced, 1 = usage error.

Usage:
    python3 check_coverage.py <artifacts-dir> \
        --evidence-dir competitive/evidence \
        [--companies-dir competitive/companies] \
        [--as-of YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

EVD_TOKEN_RE = re.compile(r"EVD-\d{3,}")
EVD_RANGE_RE = re.compile(r"(EVD-\d{3,})\s*[–-]\s*(EVD-\d{3,})")
ID_LINE_RE = re.compile(r"\*\*ID\*\*:\s*`(cpt-[a-z0-9-]+)`")
CPT_TOKEN_RE = re.compile(r"cpt-[a-z0-9]+-[a-z]+-[a-z0-9-]+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# The nine epic flows, in flow order.
FLOW_KINDS: list[tuple[int, str]] = [
    (1, "RESEARCH-REQUEST"),
    (2, "CANDIDATE-REGISTER"),
    (3, "ORIENTATION-CARD"),
    (4, "COMPANY-PROFILE"),
    (5, "COMPANY-DOSSIER"),
    (6, "COMPARISON-MATRIX"),
    (7, "OSS-REVIEW"),
    (8, "MECHANISM-STUDY"),
    (9, "WATCH-REPORT"),
]
ALL_KINDS = [kind for _, kind in FLOW_KINDS] + ["RESEARCH-REVIEW",
                                                "FEATURE-TAXONOMY"]

# Next-action phrasing -> the artifact kind expected to fulfil it.
# Checked in order; every matching kind is collected (an action may name
# several follow-ups: "Orientation card; verify open-source posture").
ACTION_KINDS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"orientation card|\borient\b", re.IGNORECASE), "ORIENTATION-CARD"),
    (re.compile(r"\bprofile\b", re.IGNORECASE), "COMPANY-PROFILE"),
    (re.compile(r"\bdossier\b", re.IGNORECASE), "COMPANY-DOSSIER"),
    (re.compile(r"comparison|\bcompare\b|\bmatrix\b", re.IGNORECASE), "COMPARISON-MATRIX"),
    (re.compile(r"mechanism", re.IGNORECASE), "MECHANISM-STUDY"),
    (re.compile(r"\bwatch\b", re.IGNORECASE), "WATCH-REPORT"),
    (re.compile(r"open-source posture|\boss\b|licen[cs]e", re.IGNORECASE), "OSS-REVIEW"),
]

# Kinds whose artifact is about exactly one subject (matched on the
# title/company only); all other kinds are searched full-text.
SUBJECT_KINDS = {"ORIENTATION-CARD", "COMPANY-PROFILE", "COMPANY-DOSSIER"}

# Candidate-name tokens too generic to identify a subject on their own.
NAME_STOPWORDS = {
    "the", "and", "for", "inc", "ltd", "code", "agent", "agents",
    "platform", "framework", "product", "company", "team", "coding",
}

# Source classes recognized from an EVD row's locator/retained-path/purpose.
SOURCE_CLASS_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("pricing", re.compile(r"pricing|price", re.IGNORECASE)),
    ("docs", re.compile(r"docs|documentation", re.IGNORECASE)),
    ("repository", re.compile(r"github\.com|gitlab\.com/.+/|-repo\b|repository", re.IGNORECASE)),
    ("releases", re.compile(r"release|changelog|blog", re.IGNORECASE)),
    ("corporate", re.compile(r"about|company|investor|finance|funding", re.IGNORECASE)),
]

# Expected export formats per ID kind directory.
EXPECTED_EXPORTS = {
    "CANDIDATE-REGISTER": ("csv", "html"),
    "COMPARISON-MATRIX": ("csv", "html"),
    "OSS-REVIEW": ("csv", "html"),
    "MECHANISM-STUDY": ("csv", "html"),
    "WATCH-REPORT": ("csv", "html"),
    "RESEARCH-REVIEW": ("csv", "html"),
    "FEATURE-TAXONOMY": ("csv", "html"),
    "ORIENTATION-CARD": ("html",),
    "COMPANY-PROFILE": ("html",),
    "COMPANY-DOSSIER": ("html",),
}

# Watch cadence -> the pass window in days.
CADENCE_DAYS = {
    "weekly": 7,
    "biweekly": 14,
    "monthly": 31,
    "quarterly": 92,
    "yearly": 366,
    "annual": 366,
}


class Artifact:
    def __init__(self, kind: str, path: Path, text: str) -> None:
        self.kind = kind
        self.path = path
        self.text = text
        self.front = parse_frontmatter(text)
        m = ID_LINE_RE.search(text)
        self.cpt_id = m.group(1) if m else None
        self.title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                self.title = line[2:].strip()
                break

    @property
    def label(self) -> str:
        return self.cpt_id or self.path.name

    def matches(self, tokens: set[str]) -> bool:
        """Whether this artifact is about the named subject.

        Single-subject kinds (card, profile, dossier) match on their title
        and frontmatter company only — a passing mention in the body must
        not count as fulfilment. Multi-subject kinds (matrix, OSS review,
        mechanism study, watch) cover several subjects in their tables, so
        the whole text is searched with word boundaries.
        """
        if self.kind in SUBJECT_KINDS:
            haystack = (self.title + "\n"
                        + self.front.get("company", "")).lower()
        else:
            haystack = self.text.lower()
        return any(re.search(rf"\b{re.escape(t)}\b", haystack)
                   for t in tokens)


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    front: dict[str, str] = {}
    if not lines or lines[0].strip() != "---":
        return front
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            front[key.strip()] = value.strip()
    return front


def sections(text: str) -> list[tuple[str, str]]:
    """Return (heading, body) pairs for level >= 2 headings."""
    result: list[tuple[str, str]] = []
    heading, buf = "", []
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) >= 2:
            if heading:
                result.append((heading, "\n".join(buf)))
            heading, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    if heading:
        result.append((heading, "\n".join(buf)))
    return result


def parse_table(body: str) -> tuple[list[str], list[list[str]]]:
    header: list[str] = []
    rows: list[list[str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not header:
            header = cells
        elif all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        else:
            rows.append(cells)
    return header, rows


def table_rows_of(body: str) -> list[list[str]]:
    header, rows = parse_table(body)
    return rows


def evd_tokens(text: str) -> set[str]:
    found = set(EVD_TOKEN_RE.findall(text))
    for start, end in EVD_RANGE_RE.findall(text):
        lo, hi = int(start.split("-")[1]), int(end.split("-")[1])
        width = len(start.split("-")[1])
        for n in range(lo, hi + 1):
            found.add(f"EVD-{n:0{width}d}")
    return found


def name_tokens(name: str) -> set[str]:
    tokens = re.split(r"[^a-z0-9-]+", name.lower())
    return {t for t in tokens
            if len(t) >= 3 and t not in NAME_STOPWORDS}


def load_evd_index(evidence_dir: Path) -> dict[str, str]:
    """Map EVD id -> the row text used for source-class detection."""
    index: dict[str, str] = {}
    path = evidence_dir / "index.tsv"
    if not path.is_file():
        return index
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        cells = line.split("\t")
        if cells and EVD_TOKEN_RE.fullmatch(cells[0]):
            index[cells[0]] = line
    return index


def source_classes(evds: set[str], evd_index: dict[str, str]) -> list[str]:
    classes: set[str] = set()
    for evd in evds:
        row = evd_index.get(evd, "")
        matched = False
        for cls, pattern in SOURCE_CLASS_PATTERNS:
            if pattern.search(row):
                classes.add(cls)
                matched = True
        if row and not matched:
            classes.add("landing/other")
    return sorted(classes)


def discover_artifacts(artifacts_dir: Path) -> dict[str, list[Artifact]]:
    found: dict[str, list[Artifact]] = {}
    for kind in ALL_KINDS:
        kind_dir = artifacts_dir / kind
        if not kind_dir.is_dir():
            continue
        for path in sorted(kind_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            found.setdefault(kind, []).append(Artifact(kind, path, text))
    return found


def register_rows(register: Artifact) -> list[dict[str, str]]:
    for heading, body in sections(register.text):
        if "candidates" not in heading.lower():
            continue
        header, rows = parse_table(body)
        if not header:
            continue
        cols = {re.sub(r"\W+", " ", h).strip().lower(): i
                for i, h in enumerate(header)}
        cand_i = next((i for k, i in cols.items() if "candidate" in k), 0)
        act_i = next((i for k, i in cols.items() if "next action" in k),
                     len(header) - 1)
        cls_i = next((i for k, i in cols.items() if "classification" in k), 1)
        return [{"candidate": r[cand_i], "action": r[act_i],
                 "classification": r[cls_i] if cls_i < len(r) else ""}
                for r in rows if len(r) > max(cand_i, act_i)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts_dir", type=Path,
                        help="directory holding the <KIND>/ artifact folders")
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--companies-dir", type=Path, default=None)
    parser.add_argument("--as-of", type=str, default=None,
                        help="reference date for watch freshness (ISO; default: today)")
    args = parser.parse_args()

    if not args.artifacts_dir.is_dir():
        print(f"error: not a directory: {args.artifacts_dir}", file=sys.stderr)
        return 1
    if args.as_of and not ISO_DATE_RE.fullmatch(args.as_of):
        print(f"error: --as-of must be an ISO date: {args.as_of}", file=sys.stderr)
        return 1
    as_of = (dt.date.fromisoformat(args.as_of) if args.as_of else dt.date.today())

    artifacts = discover_artifacts(args.artifacts_dir)
    evd_index = load_evd_index(args.evidence_dir)
    warnings = 0

    # ── Flow coverage ────────────────────────────────────────────────
    print("FLOW COVERAGE")
    covered = 0
    for flow, kind in FLOW_KINDS:
        entries = artifacts.get(kind, [])
        if entries:
            covered += 1
            names = ", ".join(a.label for a in entries)
            print(f"  Flow {flow} {kind}: {len(entries)} artifact(s) — {names}")
        else:
            print(f"  Flow {flow} {kind}: not commissioned")
    print()

    # ── Next-action execution ────────────────────────────────────────
    print("REGISTER NEXT ACTIONS")
    open_actions = 0
    registers = artifacts.get("CANDIDATE-REGISTER", [])
    if not registers:
        print("  (no candidate register found)")
    for register in registers:
        for row in register_rows(register):
            candidate, action = row["candidate"], row["action"]
            expected = [kind for pattern, kind in ACTION_KINDS
                        if pattern.search(action)]
            # Deduplicate while preserving order.
            expected = list(dict.fromkeys(expected))
            if not expected:
                print(f"  MANUAL {candidate}: no artifact kind recognized in "
                      f"next action — review by hand ({action[:60]}…)")
                continue
            tokens = name_tokens(candidate)
            fulfilled, missing = [], []
            for kind in expected:
                hit = next(
                    (a for a in artifacts.get(kind, [])
                     if a.matches(tokens)), None)
                (fulfilled if hit else missing).append(
                    f"{kind}{f' ({hit.label})' if hit else ''}")
            if not missing:
                status = "done"
            elif fulfilled:
                status = "partial"
                open_actions += 1
            else:
                status = "open"
                open_actions += 1
            detail = "; ".join(
                (["fulfilled: " + ", ".join(fulfilled)] if fulfilled else [])
                + (["missing: " + ", ".join(missing)] if missing else []))
            print(f"  {status.upper()} {candidate}: {detail}")
    print()

    # ── Evidence density ─────────────────────────────────────────────
    print("EVIDENCE DENSITY")
    floors = {"ORIENTATION-CARD": 1, "COMPANY-PROFILE": 2, "COMPANY-DOSSIER": 4}
    for kind, floor in floors.items():
        for artifact in artifacts.get(kind, []):
            evds = {e for e in evd_tokens(artifact.text) if e in evd_index}
            classes = source_classes(evds, evd_index)
            line = (f"  {artifact.label}: {len(evds)} distinct EVD, "
                    f"classes: {', '.join(classes) if classes else 'none'}")
            if len(evds) < floor:
                line += f" — WARNING: below the soft floor of {floor} for {kind}"
                warnings += 1
            print(line)
    print()

    # ── Matrix density ───────────────────────────────────────────────
    print("MATRIX DENSITY")
    matrices = artifacts.get("COMPARISON-MATRIX", [])
    if not matrices:
        print("  (no comparison matrix found)")
    for artifact in matrices:
        features: set[str] = set()
        for heading, body in sections(artifact.text):
            if "matrix" not in heading.lower():
                continue
            for row in table_rows_of(body):
                if len(row) >= 2:
                    features.add(row[1].split(":")[0].strip().lower())
        line = f"  {artifact.label}: {len(features)} distinct feature row(s)"
        if len(features) < 8:
            line += (" — WARNING: below the 8-row density floor; PM-grade "
                     "frames carry 8-20 (build/refresh the frame's "
                     "FEATURE-TAXONOMY)")
            warnings += 1
        print(line)
    print()

    # ── Fact ledgers ─────────────────────────────────────────────────
    print("FACT LEDGERS")
    if args.companies_dir is None:
        print("  (skipped: --companies-dir not provided)")
    else:
        # A provided-but-missing directory means no ledgers exist at all —
        # that is a finding for every profiled company, not a skip.
        ledger_names = ([p.parent.name.lower()
                         for p in args.companies_dir.rglob("*.tsv")
                         if "facts" in p.name]
                        if args.companies_dir.is_dir() else [])
        for kind in ("COMPANY-PROFILE", "COMPANY-DOSSIER"):
            for artifact in artifacts.get(kind, []):
                subject = artifact.front.get("company", "") or artifact.title
                tokens = name_tokens(subject)
                if any(t in name for t in tokens for name in ledger_names):
                    print(f"  ok: {artifact.label}")
                else:
                    print(f"  WARNING: no fact ledger for {artifact.label} — "
                          "repeat passes lose the as-of history")
                    warnings += 1
    print()

    # ── Exports ──────────────────────────────────────────────────────
    print("EXPORTS")
    export_warnings = 0
    for kind, formats in EXPECTED_EXPORTS.items():
        for artifact in artifacts.get(kind, []):
            missing = [ext for ext in formats
                       if not (artifact.path.parent / "exports"
                               / f"{artifact.path.stem}.{ext}").is_file()]
            if missing:
                print(f"  WARNING: {artifact.label} missing "
                      f"{', '.join(missing)} export(s)")
                export_warnings += 1
    warnings += export_warnings
    if export_warnings == 0:
        print("  (all expected exports present)")
    print()

    # ── Watch freshness ──────────────────────────────────────────────
    print("WATCH FRESHNESS")
    watches = artifacts.get("WATCH-REPORT", [])
    if watches:
        latest = max(watches, key=lambda a: a.front.get("date", ""))
        date_s = latest.front.get("date", "")
        cadence = latest.front.get("cadence", "").lower()
        days = CADENCE_DAYS.get(cadence)
        if ISO_DATE_RE.fullmatch(date_s) and days:
            due = dt.date.fromisoformat(date_s) + dt.timedelta(days=days)
            state = "OVERDUE" if due < as_of else "due"
            if due < as_of:
                warnings += 1
            print(f"  latest pass {latest.label} on {date_s} "
                  f"({cadence}); next pass {state} by {due.isoformat()}")
        else:
            print(f"  latest pass {latest.label}: cadence '{cadence}' has no "
                  "defined window — freshness not computed")
    else:
        print("  (no watch report found)")
    print()

    # ── Traceability sweep ───────────────────────────────────────────
    print("TRACEABILITY")
    requests = artifacts.get("RESEARCH-REQUEST", [])
    if requests:
        listed: set[str] = set()
        for request in requests:
            for heading, body in sections(request.text):
                if "traceability" in heading.lower():
                    listed |= set(CPT_TOKEN_RE.findall(body))
        trace_warnings = 0
        for kind, entries in artifacts.items():
            if kind == "RESEARCH-REQUEST":
                continue
            for artifact in entries:
                if artifact.cpt_id and artifact.cpt_id not in listed:
                    print(f"  WARNING: {artifact.cpt_id} not listed in the "
                          "request's Traceability section")
                    trace_warnings += 1
        warnings += trace_warnings
        if trace_warnings == 0:
            print("  (all artifact IDs back-referenced)")
    else:
        print("  (no research request found)")
    print()

    print(f"check_coverage: {covered}/9 flow(s) covered, "
          f"{open_actions} open next action(s), {warnings} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

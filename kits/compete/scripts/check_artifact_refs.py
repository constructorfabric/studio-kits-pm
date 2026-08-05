#!/usr/bin/env python3
"""Check a kit artifact's evidence references and epistemic invariants.

The companion of ``check_evidence.py``: where that script validates the
evidence layer itself, this one validates that a markdown artifact cites it
correctly. Checks (kind-aware, keyed off the artifact's ``cpt-*`` ID):

- every ``EVD-###`` token (including en-dash/hyphen ranges) resolves in
  ``<evidence-dir>/index.tsv``;
- every ``FACT-COMP-###-###`` token resolves in a fact ledger under
  ``--companies-dir`` (warning when the option is omitted);
- every data row of the kind's evidence-bearing sections carries at least
  one evidence token;
- the ``Evidence Scope`` section states an ISO cutoff date;
- for downstream kinds, the ``Traceability`` section cites a
  ``cpt-*-req-*`` id;
- kind-specific cell vocabularies (register classification; comparison
  status/availability when that kind arrives);
- ``--lint-language``: warn on absence phrasing ("lacks", "does not
  support", …) outside Boundary/unknown sections — missing evidence is
  never evidence of absence.

Exit codes: 0 = pass, 1 = usage error, 2 = findings.

Usage:
    python3 check_artifact_refs.py <artifact.md> [...] \
        --evidence-dir competitive/evidence \
        [--companies-dir competitive/companies] [--lint-language]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EVD_TOKEN_RE = re.compile(r"EVD-\d{3,}")
EVD_RANGE_RE = re.compile(r"(EVD-\d{3,})\s*[–-]\s*(EVD-\d{3,})")
FACT_TOKEN_RE = re.compile(r"FACT-COMP-\d{3,}-\d{3,}")
ID_LINE_RE = re.compile(r"\*\*ID\*\*:\s*`(cpt-[a-z0-9-]+)`")

# The kit's ID kinds. Kind detection scans the ID's segments left to right
# for the first known kind token, because the {system} slug may itself
# contain hyphens (`cpt-my-long-system-req-slug`); positional parsing
# (`parts[2]`) misread such IDs and silently skipped every kind-specific
# check. Limitation: a system slug segment that equals a kind token
# (e.g. a system literally named `oss`) is not supported.
KNOWN_KINDS = {"req", "reg", "ori", "prof", "bor", "dos", "cmp", "oss",
               "mech", "wat", "rev", "tax"}


def detect_kind(cpt_id: str) -> str:
    parts = cpt_id.split("-")
    for part in parts[1:-1]:
        if part in KNOWN_KINDS:
            return part
    return ""


FRONT_KEY_RE = re.compile(r"^([a-z_]+):\s*(.+?)\s*$")


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    front: dict[str, str] = {}
    if not lines or lines[0].strip() != "---":
        return front
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = FRONT_KEY_RE.match(line)
        if m:
            front[m.group(1)] = m.group(2)
    return front


def find_artifact_by_id(artifacts_dir: Path, cpt_id: str) -> Path | None:
    needle = f"**ID**: `{cpt_id}`"
    for path in sorted(artifacts_dir.rglob("*.md")):
        if "exports" in path.parts:
            continue
        try:
            if needle in path.read_text(encoding="utf-8"):
                return path
        except OSError:
            continue
    return None


def taxonomy_row_labels(text: str) -> list[str]:
    labels: list[str] = []
    in_section = False
    for heading, body in split_sections(text):
        if "feature rows" in heading.lower():
            for row in table_rows(body):
                if row:
                    labels.append(strip_cell(row[0]))
            in_section = True
    return labels if in_section else labels
ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ABSENCE_RE = re.compile(
    r"\b(lacks|has no|have no|does not (?:have|support|offer|provide)|"
    r"do not (?:have|support|offer|provide)|no support for)\b",
    re.IGNORECASE,
)

# Sections whose table rows must each carry >= 1 evidence token, per ID kind.
EVIDENCE_BEARING_SECTIONS = {
    "reg": ["Candidates"],
    "prof": ["Company and Commercial Facts"],
    "dos": ["Capability Graph", "Documented Mechanics", "Source Availability"],
    "cmp": ["Matrix"],
    "oss": ["Vendor Source Posture", "Repository Review"],
    "mech": ["Mechanism Map"],
    "wat": ["Watch Register", "Detected Changes"],
    "tax": ["Feature Rows", "Vendor Aliases"],
}
# Kinds that must state an Evidence Scope cutoff and a request back-link.
DOWNSTREAM_KINDS = {"reg", "ori", "prof", "dos", "cmp", "oss", "mech", "wat",
                    "rev", "tax"}
# Sections where absence phrasing is legitimate boundary prose.
NEGATIVE_SECTIONS_RE = re.compile(
    r"boundary|unknown|unestablished|limit|omission", re.IGNORECASE
)
# Vocabulary-controlled table columns, per (kind, section substring):
# each listed column of every data row must start with a documented value.
ROW_VOCAB: dict[tuple[str, str], list[tuple[int, re.Pattern[str]]]] = {
    ("reg", "Candidates"): [
        (1, re.compile(r"^(baseline|direct|adjacent|emerging)\b", re.IGNORECASE)),
    ],
    ("dos", "Source Availability"): [
        (1, re.compile(r"^(public|gated|unavailable|planned|preview)\b", re.IGNORECASE)),
    ],
    # Long-format matrix row: company | feature/mechanism | status |
    # availability | observed_on | documented boundary | evidence.
    ("cmp", "Matrix"): [
        (2, re.compile(r"^(substantial|partial|not_observed|not_comparable)\b")),
        (3, re.compile(r"^(current|planned|vision)\b", re.IGNORECASE)),
        (4, re.compile(r"^\d{4}-\d{2}-\d{2}")),
    ],
    # Change row: watched field | prior | current | observed_on | why | evidence.
    ("wat", "Detected Changes"): [
        (3, re.compile(r"^\d{4}-\d{2}-\d{2}")),
    ],
    ("oss", "Vendor Source Posture"): [
        (1, re.compile(r"^(open-source|open-core|partly-open-source|closed-source|not_assessed)\b", re.IGNORECASE)),
    ],
    ("oss", "Repository Review"): [
        (1, re.compile(r"^(core|connector|sdk|plugin|examples|documentation|benchmark|other)\b", re.IGNORECASE)),
    ],
}

# COMPANY-PROFILE capture contract: the Evidence Scope section must state a
# capture status for every standard source class, so a cheap-to-capture
# missing class (deferred) stays visibly different from a failed or gated
# one. Statuses: captured | failed | gated | deferred.
PROFILE_SOURCE_CLASSES = ["landing", "pricing", "docs", "repository", "corporate"]
SOURCE_STATUS_RE_TEMPLATE = r"{cls}[^:\n]*:\s*(captured|failed|gated|deferred)\b"
# COMPANY-DOSSIER: the Source Availability table must cover the standard
# classes even when nothing was captured (grouped rows are fine).
DOSSIER_AVAILABILITY_CLASSES = [
    ("documentation", re.compile(r"documentation|docs", re.IGNORECASE)),
    ("pricing", re.compile(r"pricing", re.IGNORECASE)),
    ("finance/adoption", re.compile(r"finance|adoption", re.IGNORECASE)),
]

# RESEARCH-REVIEW tables reference artifacts (cpt-* ids), not evidence rows:
# per section, the vocabulary column/pattern plus the verdict/status values
# that oblige the row to name at least one cpt-* artifact id.
CPT_TOKEN_RE = re.compile(r"cpt-[a-z0-9]+-[a-z]+-[a-z0-9-]+")
REV_SECTIONS: dict[str, tuple[int, re.Pattern[str], set[str] | None]] = {
    # section -> (vocab column, vocab pattern, values requiring a cpt-* ref;
    #             None = every row requires one)
    "Requirements Conformance": (
        3, re.compile(r"^(met|partial|gap|not_commissioned)\b", re.IGNORECASE),
        {"met", "partial"},
    ),
    "Run Coverage": (
        2, re.compile(r"^(done|partial|open|superseded)\b", re.IGNORECASE),
        {"done", "partial"},
    ),
    "Informativeness Findings": (
        1, re.compile(r"^(critical|high|medium|low)\b", re.IGNORECASE),
        None,
    ),
}


def load_known_evd(evidence_dir: Path) -> set[str]:
    index_path = evidence_dir / "index.tsv"
    known: set[str] = set()
    if index_path.is_file():
        for line in index_path.read_text(encoding="utf-8").splitlines()[1:]:
            cells = line.split("\t")
            if cells and EVD_TOKEN_RE.fullmatch(cells[0]):
                known.add(cells[0])
    return known


def load_known_facts(companies_dir: Path | None) -> set[str] | None:
    if companies_dir is None:
        return None
    known: set[str] = set()
    for path in companies_dir.rglob("*.tsv"):
        if "facts" not in path.name:
            continue
        for line in path.read_text(encoding="utf-8").splitlines()[1:]:
            cells = line.split("\t")
            if cells and FACT_TOKEN_RE.fullmatch(cells[0]):
                known.add(cells[0])
    return known


def expand_ranges(text: str) -> list[str]:
    """All EVD tokens in text, with EVD-100–EVD-103 style ranges expanded."""
    tokens: list[str] = []
    for start, end in EVD_RANGE_RE.findall(text):
        lo, hi = int(start.split("-")[1]), int(end.split("-")[1])
        if lo <= hi and hi - lo <= 500:
            tokens.extend(f"EVD-{n:03d}" for n in range(lo, hi + 1))
    stripped = EVD_RANGE_RE.sub(" ", text)
    tokens.extend(EVD_TOKEN_RE.findall(stripped))
    return tokens


def split_sections(text: str) -> list[tuple[str, str]]:
    """[(heading text, body)] for every heading in document order."""
    sections: list[tuple[str, str]] = []
    current, buf = "", []
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            if current or buf:
                sections.append((current, "\n".join(buf)))
            current, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    sections.append((current, "\n".join(buf)))
    return sections


def strip_cell(cell: str) -> str:
    """Cell text without emphasis/code markers, for vocabulary matching."""
    return re.sub(r"[*`]", "", cell).strip()


def table_rows(body: str) -> list[list[str]]:
    """Data rows of the first markdown table in body (header/rule skipped)."""
    rows: list[list[str]] = []
    in_table = False
    for line in body.splitlines():
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                in_table = True
                continue
            if in_table:
                rows.append(cells)
        elif in_table:
            break
    return rows


def check_file(path: Path, known_evd: set[str], known_facts: set[str] | None,
               lint_language: bool,
               artifacts_dir: Path | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")

    m = ID_LINE_RE.search(text)
    kind = ""
    if not m:
        errors.append("no `**ID**: `cpt-…`` line found")
    else:
        kind = detect_kind(m.group(1))
        if not kind:
            errors.append(
                f"artifact ID {m.group(1)!r} carries no known kit kind "
                f"({', '.join(sorted(KNOWN_KINDS))}) — kind-specific checks "
                "cannot run"
            )

    for token in expand_ranges(text):
        if token not in known_evd:
            errors.append(f"{token} does not resolve in the evidence index")
    for token in set(FACT_TOKEN_RE.findall(text)):
        if known_facts is None:
            warnings.append(f"{token} not checked (--companies-dir not given)")
        elif token not in known_facts:
            errors.append(f"{token} does not resolve in any fact ledger")

    sections = split_sections(text)

    for wanted in EVIDENCE_BEARING_SECTIONS.get(kind, []):
        for heading, body in sections:
            if wanted.lower() not in heading.lower():
                continue
            rows = table_rows(body)
            for i, row in enumerate(rows, start=1):
                row_text = " ".join(row)
                if not EVD_TOKEN_RE.search(row_text) and not FACT_TOKEN_RE.search(row_text):
                    errors.append(f"section {heading!r} row {i}: no evidence reference")
                for col, pattern in ROW_VOCAB.get((kind, wanted), []):
                    if len(row) > col and not pattern.search(strip_cell(row[col])):
                        errors.append(
                            f"section {heading!r} row {i}: column {col + 1} must start "
                            f"with one of the documented values, got {row[col]!r}"
                        )

    if kind == "prof":
        scope_bodies = [b for h, b in sections if "evidence scope" in h.lower()]
        scope_text = "\n".join(scope_bodies)
        for cls in PROFILE_SOURCE_CLASSES:
            if not re.search(SOURCE_STATUS_RE_TEMPLATE.format(cls=cls),
                             scope_text, re.IGNORECASE):
                errors.append(
                    f"'Evidence Scope' states no capture status for the "
                    f"{cls!r} source class (captured | failed | gated | deferred)"
                )

    if kind == "dos":
        avail_bodies = [b for h, b in sections
                        if "source availability" in h.lower()]
        avail_text = "\n".join(avail_bodies)
        for cls, pattern in DOSSIER_AVAILABILITY_CLASSES:
            if avail_bodies and not pattern.search(avail_text):
                errors.append(
                    f"'Source Availability' has no row covering the {cls!r} "
                    "source class (record it 'unavailable' when uncaptured)"
                )

    if kind == "cmp":
        declared = frontmatter(text).get("taxonomy", "")
        if not declared:
            warnings.append(
                "matrix declares no taxonomy (frontmatter `taxonomy:`) — "
                "rows are ad-hoc; build one with cf-compete-taxonomy for "
                "apples-to-apples labels"
            )
        elif artifacts_dir is None:
            warnings.append(
                f"taxonomy {declared!r} declared but --artifacts-dir not "
                "given — row labels not verified against it"
            )
        else:
            tax_path = find_artifact_by_id(artifacts_dir, declared)
            if tax_path is None:
                errors.append(
                    f"declared taxonomy {declared!r} not found under "
                    f"{artifacts_dir}"
                )
            else:
                labels = taxonomy_row_labels(
                    tax_path.read_text(encoding="utf-8"))
                if not labels:
                    errors.append(
                        f"declared taxonomy {tax_path} carries no Feature "
                        "Rows table")
                else:
                    lowered = {l.lower() for l in labels}
                    used: set[str] = set()
                    for heading, body in sections:
                        if "matrix" not in heading.lower():
                            continue
                        for i, row in enumerate(table_rows(body), start=1):
                            if len(row) < 2:
                                continue
                            cell = strip_cell(row[1])
                            label = cell.split(":")[0].strip().lower()
                            if label in lowered:
                                used.add(label)
                            else:
                                errors.append(
                                    f"matrix row {i}: feature {cell!r} does "
                                    "not start with a taxonomy row label — "
                                    "rows must come from the declared "
                                    "taxonomy (detail goes after a colon)"
                                )
                    for missing in sorted(lowered - used):
                        errors.append(
                            f"taxonomy row {missing!r} never appears in the "
                            "matrix — cover every row for every compared "
                            "company (not_observed where evidence lacks)"
                        )

    if kind == "tax":
        for heading, body in sections:
            if "feature rows" not in heading.lower():
                continue
            n = len(table_rows(body))
            if not 8 <= n <= 20:
                warnings.append(
                    f"'Feature Rows' carries {n} row(s) — outside the 8-20 "
                    "band; keep it only with a stated reason in the section"
                )

    if kind == "rev":
        for wanted, (col, pattern, ref_values) in REV_SECTIONS.items():
            for heading, body in sections:
                if wanted.lower() not in heading.lower():
                    continue
                for i, row in enumerate(table_rows(body), start=1):
                    verdict = strip_cell(row[col]) if len(row) > col else ""
                    if not pattern.search(verdict):
                        errors.append(
                            f"section {heading!r} row {i}: column {col + 1} must start "
                            f"with one of the documented values, got {verdict!r}"
                        )
                        continue
                    first_word = verdict.split()[0].lower() if verdict else ""
                    needs_ref = ref_values is None or first_word in ref_values
                    if needs_ref and not CPT_TOKEN_RE.search(" ".join(row)):
                        errors.append(
                            f"section {heading!r} row {i}: a {first_word!r} row must "
                            "name at least one cpt-* artifact id"
                        )

    if kind in DOWNSTREAM_KINDS:
        scope_bodies = [b for h, b in sections if "evidence scope" in h.lower()]
        if not scope_bodies:
            errors.append("missing an 'Evidence Scope' section")
        elif not any(ISO_DATE_RE.search(b) for b in scope_bodies):
            errors.append("'Evidence Scope' section states no ISO cutoff date")
        trace_bodies = [b for h, b in sections if "traceability" in h.lower()]
        if not trace_bodies:
            errors.append("missing a 'Traceability' section")
        elif not any(detect_kind(t) == "req"
                     for b in trace_bodies
                     for t in CPT_TOKEN_RE.findall(b)):
            errors.append("'Traceability' cites no commissioning request (cpt-*-req-*)")

    if lint_language:
        for heading, body in sections:
            if NEGATIVE_SECTIONS_RE.search(heading):
                continue
            for m2 in ABSENCE_RE.finditer(body):
                line_no = text[: text.find(body) + m2.start()].count("\n") + 1
                warnings.append(
                    f"absence phrasing {m2.group(0)!r} outside a boundary section "
                    f"(~line {line_no}) — is this evidenced, or is it not_observed?"
                )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("artifacts", nargs="+", type=Path)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--companies-dir", type=Path, default=None)
    parser.add_argument("--artifacts-dir", type=Path, default=None,
                        help="run directory holding <KIND>/ folders; enables "
                             "matrix-vs-taxonomy verification")
    parser.add_argument("--lint-language", action="store_true")
    args = parser.parse_args()

    if not args.evidence_dir.is_dir():
        print(f"error: not a directory: {args.evidence_dir}", file=sys.stderr)
        return 1
    known_evd = load_known_evd(args.evidence_dir)
    known_facts = load_known_facts(args.companies_dir)

    total_errors = 0
    for path in args.artifacts:
        if not path.is_file():
            print(f"error: not a file: {path}", file=sys.stderr)
            return 1
        errors, warnings = check_file(path, known_evd, known_facts,
                                      args.lint_language, args.artifacts_dir)
        for msg in warnings:
            print(f"WARN {path}: {msg}")
        for msg in errors:
            print(f"FAIL {path}: {msg}")
        total_errors += len(errors)

    if total_errors:
        print(f"check_artifact_refs: {total_errors} error(s)")
        return 2
    print(f"check_artifact_refs: PASS ({len(args.artifacts)} artifact(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate the competitive evidence layer: index, fact ledgers, extracts.

The evidence layer is script-validated data (cfs validates markdown artifacts,
not table rows). This checker enforces:

- ``evidence/index.tsv`` — exact header, unique ``EVD-###`` ids, ISO dates,
  access enum, existing retained paths;
- ``companies/*/facts.tsv`` (or any ``*facts*.tsv`` under --companies-dir) —
  exact 12-column header, id/date/enum discipline, non-empty limitation,
  every ``evidence_refs`` token resolving in the index;
- ``evidence/extracts/*.md`` — one of the two retained-extract shapes:
  a front-matter bundle ending with ``## Explicit limits for reuse``, or a
  single-page extract with the Source/Accessed/Access/Capture-method preamble
  and ``## Concise extract`` + ``## Intake note`` sections.

Exit codes: 0 = pass, 1 = usage/environment error, 2 = findings.

Usage:
    python3 check_evidence.py --evidence-dir competitive/evidence \
        [--companies-dir competitive/companies]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

INDEX_NAME = "index.tsv"
INDEX_HEADER = [
    "evd_id",
    "locator",
    "accessed_on",
    "access",
    "capture_method",
    "retained_path",
    "purpose",
]
FACTS_HEADER = [
    "fact_id",
    "topic",
    "offering",
    "claim_status",
    "statement",
    "value",
    "unit",
    "observed_on",
    "availability",
    "confidence",
    "evidence_refs",
    "limitation",
]

EVD_RE = re.compile(r"^EVD-\d{3,}$")
FACT_ID_RE = re.compile(r"^FACT-COMP-\d{3,}-\d{3,}$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ACCESS_VOCAB = {"public", "gated", "unavailable", "planned", "preview"}
CLAIM_STATUS_VOCAB = {
    "observed",
    "observed_primary_source",
    "observed_vendor",
    "observed_company_statement",
    "observed_third_party_profile",
    "observed_third_party_company_profile",
    "observed_investor_announcement",
    "vendor_claim",
    "research_hypothesis",
}
CONFIDENCE_VOCAB = {"low", "medium", "high", "unknown"}
AVAILABILITY_VOCAB = {
    "unknown",
    "current",
    "planned",
    "preview",
    "not_assessed",
    "open-source",
    "open-core",
    "partly-open-source",
    "closed-source",
}

EXTRACT_BUNDLE_KIND = "competitive-source-extract"
BUNDLE_TERMINAL_SECTION = "## Explicit limits for reuse"
PAGE_SECTIONS = ("## Concise extract", "## Intake note")
PAGE_PREAMBLE_BULLETS = ("- Source:", "- Accessed:", "- Access:", "- Capture method:")


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path, msg: str) -> None:
        self.errors.append(f"{path}: {msg}")

    def warn(self, path: Path, msg: str) -> None:
        self.warnings.append(f"{path}: {msg}")


def read_tsv(path: Path) -> tuple[list[str], list[list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows = [line.split("\t") for line in lines if line.strip()]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def check_index(evidence_dir: Path, f: Findings) -> dict[str, str]:
    """Validate index.tsv; return {evd_id: locator} for reference resolution."""
    index_path = evidence_dir / INDEX_NAME
    known: dict[str, str] = {}
    if not index_path.is_file():
        f.error(index_path, "evidence index not found")
        return known
    header, rows = read_tsv(index_path)
    if header != INDEX_HEADER:
        f.error(index_path, f"header must be exactly: {'\t'.join(INDEX_HEADER)}")
        return known
    for n, row in enumerate(rows, start=2):
        where = f"row {n}"
        if len(row) != len(INDEX_HEADER):
            f.error(index_path, f"{where}: expected {len(INDEX_HEADER)} columns, got {len(row)}")
            continue
        rec = dict(zip(INDEX_HEADER, row))
        evd = rec["evd_id"]
        if not EVD_RE.match(evd):
            f.error(index_path, f"{where}: bad evd_id {evd!r}")
        elif evd in known:
            f.error(index_path, f"{where}: duplicate evd_id {evd}")
        else:
            known[evd] = rec["locator"]
        if not rec["locator"].strip():
            f.error(index_path, f"{where}: empty locator")
        if not ISO_DATE_RE.match(rec["accessed_on"]):
            f.error(index_path, f"{where}: accessed_on must be YYYY-MM-DD, got {rec['accessed_on']!r}")
        if rec["access"] not in ACCESS_VOCAB:
            f.error(index_path, f"{where}: access must be one of {sorted(ACCESS_VOCAB)}, got {rec['access']!r}")
        retained = rec["retained_path"]
        if retained and retained != "-" and not (evidence_dir / retained).is_file():
            f.error(index_path, f"{where}: retained_path does not resolve: {retained}")
        if not rec["purpose"].strip():
            f.error(index_path, f"{where}: empty purpose")
    return known


def split_evd_refs(field: str) -> list[str]:
    if field.strip() in {"", "-"}:
        return []
    return [tok.strip() for tok in field.split("|") if tok.strip()]


def check_facts_file(path: Path, known: dict[str, str], f: Findings) -> None:
    header, rows = read_tsv(path)
    if header != FACTS_HEADER:
        f.error(path, f"header must be exactly the 12 fact-ledger columns: {'\t'.join(FACTS_HEADER)}")
        return
    seen_ids: set[str] = set()
    for n, row in enumerate(rows, start=2):
        where = f"row {n}"
        if len(row) != len(FACTS_HEADER):
            f.error(path, f"{where}: expected {len(FACTS_HEADER)} columns, got {len(row)}")
            continue
        rec = dict(zip(FACTS_HEADER, row))
        fid = rec["fact_id"]
        if not FACT_ID_RE.match(fid):
            f.error(path, f"{where}: bad fact_id {fid!r}")
        elif fid in seen_ids:
            f.error(path, f"{where}: duplicate fact_id {fid}")
        else:
            seen_ids.add(fid)
        if rec["claim_status"] not in CLAIM_STATUS_VOCAB:
            f.error(path, f"{where}: claim_status {rec['claim_status']!r} not in vocabulary")
        if not ISO_DATE_RE.match(rec["observed_on"]):
            f.error(path, f"{where}: observed_on must be YYYY-MM-DD, got {rec['observed_on']!r}")
        if rec["availability"] not in AVAILABILITY_VOCAB:
            f.error(path, f"{where}: availability {rec['availability']!r} not in vocabulary")
        if rec["confidence"] not in CONFIDENCE_VOCAB:
            f.error(path, f"{where}: confidence {rec['confidence']!r} not in vocabulary")
        if not rec["limitation"].strip():
            f.error(path, f"{where}: limitation must be non-empty (every fact states its boundary)")
        refs = split_evd_refs(rec["evidence_refs"])
        if not refs:
            f.error(path, f"{where}: evidence_refs is empty — every fact needs at least one EVD reference")
        for ref in refs:
            if not EVD_RE.match(ref):
                f.error(path, f"{where}: bad evidence ref {ref!r}")
            elif ref not in known:
                f.error(path, f"{where}: {ref} does not resolve in the evidence index")


def parse_front_matter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def check_extract_file(path: Path, known: dict[str, str], f: Findings) -> None:
    text = path.read_text(encoding="utf-8")
    fm = parse_front_matter(text)
    if fm is not None:
        # Bundle variant: front-matter extract over one or more source pages.
        for key in ("id", "kind", "accessed_on", "purpose"):
            if key not in fm:
                f.error(path, f"bundle extract front matter missing {key!r}")
        if fm.get("kind") and fm["kind"] != EXTRACT_BUNDLE_KIND:
            f.error(path, f"bundle extract kind must be {EXTRACT_BUNDLE_KIND!r}, got {fm['kind']!r}")
        if fm.get("accessed_on") and not ISO_DATE_RE.match(fm["accessed_on"]):
            f.error(path, f"bundle extract accessed_on must be YYYY-MM-DD, got {fm['accessed_on']!r}")
        if BUNDLE_TERMINAL_SECTION not in text:
            f.error(path, f"bundle extract must end with a {BUNDLE_TERMINAL_SECTION!r} section")
        return
    # Single-page variants. Bulleted style carries the full preamble and the
    # Concise extract / Intake note sections; minimal style (bare `Source:` /
    # `Accessed:` lines) is accepted with lighter checks.
    bulleted = "- Source:" in text
    if bulleted:
        for bullet in PAGE_PREAMBLE_BULLETS:
            if bullet not in text:
                f.error(path, f"single-page extract missing preamble bullet {bullet!r}")
        for section in PAGE_SECTIONS:
            if section not in text:
                f.error(path, f"single-page extract missing section {section!r}")
    else:
        if not re.search(r"^Source:\s*\S", text, re.MULTILINE):
            f.error(path, "single-page extract missing a 'Source:' line")
        accessed = re.search(r"^Accessed:\s*(.+)$", text, re.MULTILINE)
        if not accessed:
            f.error(path, "single-page extract missing an 'Accessed:' line")
        elif not ISO_DATE_RE.match(accessed.group(1).strip()[:10]):
            f.error(path, f"'Accessed:' line states no ISO date: {accessed.group(1).strip()!r}")
    m = re.search(r"^(?:- )?Source:\s*`?(EVD-\d{3,})`?", text, re.MULTILINE)
    if m and m.group(1) not in known:
        f.error(path, f"source {m.group(1)} does not resolve in the evidence index")
    if not m:
        url = re.search(r"^(?:- )?Source:\s*`?(https?://\S+?)`?\s*$", text, re.MULTILINE)
        if url and url.group(1) not in known.values():
            f.error(path, f"source {url.group(1)} is not indexed by locator")
        elif not url:
            f.warn(path, "single-page extract Source carries no EVD id or URL; index it before citing")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--evidence-dir", required=True, type=Path,
                        help="directory holding index.tsv and extracts/")
    parser.add_argument("--companies-dir", type=Path, default=None,
                        help="directory holding per-company fact ledgers (*facts*.tsv)")
    args = parser.parse_args()

    if not args.evidence_dir.is_dir():
        print(f"error: not a directory: {args.evidence_dir}", file=sys.stderr)
        return 1

    f = Findings()
    known = check_index(args.evidence_dir, f)

    extracts_dir = args.evidence_dir / "extracts"
    if extracts_dir.is_dir():
        for path in sorted(extracts_dir.rglob("*.md")):
            check_extract_file(path, known, f)

    if args.companies_dir:
        if not args.companies_dir.is_dir():
            print(f"error: not a directory: {args.companies_dir}", file=sys.stderr)
            return 1
        for path in sorted(args.companies_dir.rglob("*.tsv")):
            if "facts" in path.name:
                check_facts_file(path, known, f)

    for msg in f.warnings:
        print(f"WARN {msg}")
    for msg in f.errors:
        print(f"FAIL {msg}")
    if f.errors:
        print(f"check_evidence: {len(f.errors)} error(s), {len(f.warnings)} warning(s)")
        return 2
    print(f"check_evidence: PASS ({len(known)} evidence record(s), {len(f.warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())

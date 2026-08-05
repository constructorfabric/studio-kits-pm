#!/usr/bin/env python3
"""Harvest candidate feature terms from retained extracts, or report a
taxonomy's corpus coverage.

Two modes, both deterministic seeds for human/LLM judgment — the script
normalizes nothing itself:

**Harvest** (default): scan every retained extract for candidate feature
terms — quoted phrases, bullet lead-ins, and TitleCase/CamelCase
sequences — and report each term with the subjects whose extracts carry
it. The report is the raw material for a FEATURE-TAXONOMY's union: a
term present in only one subject's corpus is exactly the row an anchored
process would miss.

**Coverage** (``--taxonomy <artifact.md>``): parse the taxonomy's Feature
Rows and Vendor Aliases and check every row label and alias term for
hits in the extract corpus, per subject. Rows or aliases without any
corpus hit are mining or capture targets; the summary line is stable for
scripting:
``mine_terms coverage: R/N rows hit, A/M aliases hit, K without hits``

Subjects are derived from extract filenames (the slug between the date
prefix and a trailing surface word such as -landing/-docs/-pricing), so
one vendor's pages group together. Exit codes: 0 = report produced,
1 = usage error.

Usage:
    python3 mine_terms.py --evidence-dir competitive/evidence
        [--taxonomy <artifact.md>] [--min-len 2] [--top 80]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
SURFACE_SUFFIXES = (
    "landing", "docs", "doc", "documentation", "pricing", "features",
    "repo", "repository", "page", "pages", "site", "readme", "license",
    "specification", "getting-started", "extracts", "source",
)
QUOTED_RE = re.compile(r"[\"“]([^\"”]{3,80})[\"”]")
TITLECASE_RE = re.compile(
    r"\b([A-Z][a-z]+(?:[A-Z][a-z]+)+|[A-Z][a-z]+(?: [A-Z][a-z]+){1,3})\b")
BULLET_LEAD_RE = re.compile(r"^\s*-\s+([^:—.\n]{3,60})[:—.]", re.MULTILINE)
STOP_TERMS = {
    "source", "accessed", "access", "capture method", "concise extract",
    "intake note", "the", "and", "for",
}


def subject_of(path: Path) -> str:
    stem = DATE_PREFIX_RE.sub("", path.stem)
    changed = True
    while changed:
        changed = False
        for suffix in sorted(SURFACE_SUFFIXES, key=len, reverse=True):
            if stem.endswith("-" + suffix) and len(stem) > len(suffix) + 1:
                stem = stem[: -(len(suffix) + 1)]
                changed = True
    return stem


def normalize(term: str) -> str:
    return re.sub(r"\s+", " ", term.strip().strip(".,;:*`'\"")).lower()


def harvest(extracts: dict[str, dict[Path, str]], min_len: int, top: int) -> int:
    hits: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    samples: dict[str, str] = {}
    for subject, files in extracts.items():
        for path, text in files.items():
            for pattern in (QUOTED_RE, TITLECASE_RE, BULLET_LEAD_RE):
                for m in pattern.finditer(text):
                    term = normalize(m.group(1))
                    if len(term.split()) < min_len and " " not in term \
                            and not any(c.isupper() for c in m.group(1)[1:]):
                        continue
                    if len(term) < 4 or term in STOP_TERMS:
                        continue
                    hits[term][subject] += 1
                    samples.setdefault(term, path.name)
    ranked = sorted(
        hits.items(),
        key=lambda kv: (-len(kv[1]), -sum(kv[1].values()), kv[0]))
    print("TERM HARVEST (seed for taxonomy normalization — not a taxonomy)")
    print(f"{'term':<48} {'subjects':<9} total  present in")
    for term, per_subject in ranked[:top]:
        subjects = ", ".join(sorted(per_subject))
        print(f"{term[:47]:<48} {len(per_subject):<9} "
              f"{sum(per_subject.values()):<6} {subjects}")
    single = sum(1 for _, s in hits.items() if len(s) == 1)
    print(f"\nmine_terms harvest: {len(hits)} candidate term(s) across "
          f"{len(extracts)} subject(s); {single} term(s) appear in exactly "
          "one subject's corpus (the union rows an anchored process would miss)")
    return 0


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def taxonomy_tables(text: str) -> tuple[list[str], list[tuple[str, str, str]]]:
    """(row labels, [(alias term, vendor, feature)]) from a FEATURE-TAXONOMY."""
    rows: list[str] = []
    aliases: list[tuple[str, str, str]] = []
    section = ""
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            section = m.group(2).lower()
            continue
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells) or not cells:
            continue
        first = re.sub(r"[*`]", "", cells[0])
        if "feature rows" in section and first.lower() not in (
                "feature / scenario",):
            rows.append(first)
        elif "vendor aliases" in section and len(cells) >= 3 \
                and first.lower() not in ("feature / scenario",):
            term = re.sub(r"[*`]", "", cells[2])
            aliases.append((term, re.sub(r"[*`]", "", cells[1]), first))
    return rows, aliases


def term_hits(term: str, extracts: dict[str, dict[Path, str]]) -> list[str]:
    """Subjects whose corpus mentions any word-run of the term."""
    fragments = [f for f in re.split(r"[;/()]| \(|\"", term) if f.strip()]
    found: set[str] = set()
    for subject, files in extracts.items():
        blob = " ".join(t.lower() for t in files.values())
        for fragment in fragments:
            frag = normalize(fragment)
            if frag and frag in blob:
                found.add(subject)
                break
            # Fall back to the fragment's significant words all present.
            words = [w for w in frag.split() if len(w) > 3]
            if words and all(w in blob for w in words):
                found.add(subject)
                break
    return sorted(found)


def coverage(extracts: dict[str, dict[Path, str]], taxonomy: Path) -> int:
    text = taxonomy.read_text(encoding="utf-8")
    rows, aliases = taxonomy_tables(text)
    if not rows:
        print(f"error: no Feature Rows table found in {taxonomy}",
              file=sys.stderr)
        return 1
    print(f"TAXONOMY COVERAGE — {taxonomy.name}")
    misses = 0
    print("\nFeature Rows (a row hits via its label or any of its aliases):")
    row_hits = 0
    for label in rows:
        subjects = set(term_hits(label, extracts))
        for term, _vendor, feature in aliases:
            if feature == label:
                subjects |= set(term_hits(term, extracts))
        if subjects:
            row_hits += 1
            print(f"  ok: {label} — corpus hits: {', '.join(sorted(subjects))}")
        else:
            misses += 1
            print(f"  NO HITS: {label} — no subject's corpus reaches it via "
                  "label or aliases; a mining or capture target")
    print("\nVendor Aliases:")
    alias_hits = 0
    for term, vendor, _feature in aliases:
        subjects = term_hits(term, extracts)
        if subjects:
            alias_hits += 1
            print(f"  ok: {vendor}: {term!r} — hits: {', '.join(subjects)}")
        else:
            misses += 1
            print(f"  NO HITS: {vendor}: {term!r} — the corpus does not "
                  "carry this wording; re-check the evidence reference")
    print(f"\nmine_terms coverage: {row_hits}/{len(rows)} rows hit, "
          f"{alias_hits}/{len(aliases)} aliases hit, {misses} without hits")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--taxonomy", type=Path, default=None)
    parser.add_argument("--min-len", type=int, default=2,
                        help="minimum words for unquoted candidate terms")
    parser.add_argument("--top", type=int, default=80,
                        help="harvest rows to print")
    args = parser.parse_args()

    extracts_dir = args.evidence_dir / "extracts"
    if not extracts_dir.is_dir():
        print(f"error: not a directory: {extracts_dir}", file=sys.stderr)
        return 1
    extracts: dict[str, dict[Path, str]] = defaultdict(dict)
    for path in sorted(extracts_dir.glob("*.md")):
        extracts[subject_of(path)][path] = path.read_text(encoding="utf-8")
    if not extracts:
        print(f"error: no extracts under {extracts_dir}", file=sys.stderr)
        return 1

    if args.taxonomy is not None:
        if not args.taxonomy.is_file():
            print(f"error: not a file: {args.taxonomy}", file=sys.stderr)
            return 1
        return coverage(extracts, args.taxonomy)
    return harvest(extracts, args.min_len, args.top)


if __name__ == "__main__":
    sys.exit(main())

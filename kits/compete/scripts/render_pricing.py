#!/usr/bin/env python3
"""Render the pricing benchmark CSV from COMPANY-PROFILE artifacts.

The DEC-005 pricing benchmark view: one deterministic CSV over the
pricing and commercial-model rows of the given profiles' Company and
Commercial Facts tables. The markdown profiles are canonical; this view
is derived, never hand-edited, and adds no claims — cells are copied
verbatim (inline markup stripped), so a not-established row stays a
not-established row and vendor terms stay in the vendor's words.

Columns: ``company, field, observed_value, as_of, boundary, evidence``.
``as_of`` is the first ISO date inside the observed value (the profile's
as-of framing), falling back to the artifact's frontmatter date.

Exit codes: 0 = written, 1 = usage error or no pricing rows found.

Usage:
    python3 render_pricing.py <profile.md> [<profile.md> ...] \
        [-o pricing-benchmark.csv]
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
EVD_TOKEN_RE = re.compile(r"EVD-\d{3,}|FACT-COMP-\d{3,}-\d{3,}")
PRICING_FIELD_RE = re.compile(r"pricing|commercial", re.IGNORECASE)

CSV_HEADER = ["company", "field", "observed_value", "as_of", "boundary", "evidence"]


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


def facts_section(text: str) -> str:
    body: list[str] = []
    collecting = False
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            if collecting:
                break
            if len(m.group(1)) >= 2 and "commercial facts" in m.group(2).lower():
                collecting = True
            continue
        if collecting:
            body.append(line)
    return "\n".join(body)


def table_rows(body: str) -> list[list[str]]:
    rows: list[list[str]] = []
    state = "before"
    for line in body.splitlines():
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if state == "before":
                state = "rule"
            elif state == "rule":
                state = "rows"
            else:
                rows.append(cells)
        elif state == "rows":
            break
    return rows


def strip_inline(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    return text.strip()


def profile_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return re.sub(r"^Company Profile\s*[—–-]\s*", "", line[2:].strip())
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("profiles", nargs="+", type=Path)
    parser.add_argument("-o", "--out", type=Path,
                        default=Path("pricing-benchmark.csv"))
    args = parser.parse_args()

    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(CSV_HEADER)
    row_count = 0

    for path in args.profiles:
        if not path.is_file():
            print(f"error: not a file: {path}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8")
        front = parse_frontmatter(text)
        company = front.get("company") or profile_title(text) or path.stem
        for cells in table_rows(facts_section(text)):
            if len(cells) < 2 or not PRICING_FIELD_RE.search(cells[0]):
                continue
            field = strip_inline(cells[0])
            value = strip_inline(cells[1])
            boundary = strip_inline(cells[2]) if len(cells) > 2 else ""
            as_of = next(iter(ISO_DATE_RE.findall(value)),
                         front.get("date", ""))
            evidence = "; ".join(dict.fromkeys(
                EVD_TOKEN_RE.findall(" ".join(cells))))
            writer.writerow([company, field, value, as_of, boundary, evidence])
            row_count += 1

    if row_count == 0:
        print("error: no pricing/commercial rows found in the given profiles",
              file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(buf.getvalue(), encoding="utf-8")
    print(f"wrote {args.out} ({row_count} row(s) from {len(args.profiles)} profile(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())

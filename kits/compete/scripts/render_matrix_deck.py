#!/usr/bin/env python3
"""Render presentation views over one or more COMPARISON-MATRIX artifacts.

Two deterministic, dependency-free, script-free HTML views (the PM deck
formats), derived from canonical markdown matrices — never hand-edited:

- ``--mode tabs`` (default): one page, one tab per matrix (a frame per
  role/lens), each tab a features × companies grid whose cells carry the
  status and link to the cell's first evidence locator. Tabs are
  CSS-only (radio inputs), preserving the kit's no-script guarantee.
- ``--mode heatmap``: one compact companies × frames grid; each cell
  aggregates that company's rows in that matrix (counts of
  substantial/partial/not_observed/not_comparable, coloured by the
  dominant status) and links to the matrix's html export.

Cells and colours restate the matrices' statuses only: no ranking, no
score, and not_observed stays visually distinct from absence claims.

Exit codes: 0 = written, 1 = usage error or no matrix rows found.

Usage:
    python3 render_matrix_deck.py <matrix.md> [<matrix.md> ...] \
        --evidence-dir competitive/evidence \
        [--mode tabs|heatmap] [-o deck.html]
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path

ID_LINE_RE = re.compile(r"\*\*ID\*\*:\s*`(cpt-[a-z0-9-]+)`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
EVD_TOKEN_RE = re.compile(r"EVD-\d{3,}")
STATUSES = ("substantial", "partial", "not_observed", "not_comparable")

STYLE = (
    "body{font:14px/1.4 system-ui,sans-serif;color:#172033;max-width:1400px;"
    "margin:32px auto;padding:0 20px}"
    "h1{margin:0 0 4px;letter-spacing:-.02em}"
    ".meta{color:#526070;font-size:12px;margin:0 0 16px}"
    "table{border-collapse:collapse;width:100%;margin-top:12px}"
    "th,td{border:1px solid #d6dce5;padding:8px 10px;text-align:left;"
    "vertical-align:top;font-size:13px}"
    "th{background:#172033;color:#fff}"
    "td.s-substantial{background:#eaf1ff;color:#17479c;font-weight:600}"
    "td.s-partial{background:#e4f5f0;color:#056258;font-weight:600}"
    "td.s-not_observed{background:#f4f6f9;color:#8491a4}"
    "td.s-not_comparable{background:#fff4e2;color:#a85c04}"
    "td a{color:inherit;text-decoration:none;border-bottom:1px dotted}"
    ".tabs input[type=radio]{display:none}"
    ".tabs>label{display:inline-block;padding:7px 12px;margin:0 6px 10px 0;"
    "border:1px solid #c9d7eb;border-radius:7px;cursor:pointer;"
    "font:700 11px/1 ui-monospace,monospace;color:#345174;background:#fff}"
    ".panel{display:none}"
    + "".join(
        f".tabs input:nth-of-type({i})~label:nth-of-type({i})"
        "{background:#172033;color:#fff;border-color:#172033}"
        f".tabs input:nth-of-type({i}):checked~.panel:nth-of-type({i})"
        "{display:block}"
        for i in range(1, 13)
    )
    + ".legend{margin-top:18px;color:#526070;font-size:11px}"
    ".boundary{margin-top:6px;color:#a85c04;font-size:11px}"
)

BOUNDARY = ("These views restate documented, evidence-bounded statuses under "
            "each matrix's single frame: no ranking, no winner, and "
            "not_observed is missing retained evidence — never feature "
            "absence.")


def split_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    heading, buf = "", []
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            if heading or buf:
                sections.append((heading, "\n".join(buf)))
            heading, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    sections.append((heading, "\n".join(buf)))
    return sections


def strip_inline(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return re.sub(r"\*\*([^*]*)\*\*", r"\1", text).strip()


def parse_matrix(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = path.stem
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:
            # Frame name without the artifact-kind prefix.
            title = re.sub(r"^Comparison Matrix\s*[—–-]\s*", "",
                           strip_inline(m.group(2)))
            break
    rows: list[dict] = []
    for heading, body in split_sections(text):
        # The "Matrix" section proper, not the H1 title or the frame section.
        if heading.lower().strip("0123456789. ") != "matrix":
            continue
        state = "before"
        for line in body.splitlines():
            if not line.strip().startswith("|"):
                if state == "rows":
                    break
                continue
            cells = [strip_inline(c.strip())
                     for c in line.strip().strip("|").split("|")]
            if state == "before":
                state = "rule"
            elif state == "rule":
                state = "rows"
            elif len(cells) >= 7:
                rows.append({
                    "company": cells[0],
                    "feature": cells[1],
                    "status": cells[2].split()[0] if cells[2] else "",
                    "boundary": cells[5],
                    "evidence": EVD_TOKEN_RE.findall(cells[6]),
                })
        if rows:
            break
    return {"path": path, "title": title, "rows": rows}


def load_locators(evidence_dir: Path) -> dict[str, str]:
    locators: dict[str, str] = {}
    index = evidence_dir / "index.tsv"
    if index.is_file():
        for line in index.read_text(encoding="utf-8").splitlines()[1:]:
            cells = line.split("\t")
            if len(cells) >= 2:
                locators[cells[0]] = cells[1]
    return locators


def cell_html(row: dict | None, locators: dict[str, str]) -> str:
    if row is None:
        return '<td class="s-not_observed">—</td>'
    status = row["status"] if row["status"] in STATUSES else "not_observed"
    label = html.escape(status)
    title = html.escape(row["boundary"])
    evd = next(iter(row["evidence"]), None)
    url = locators.get(evd, "") if evd else ""
    inner = (f'<a href="{html.escape(url)}" title="{title}" '
             f'rel="noopener noreferrer">{label}</a>' if url
             else f'<span title="{title}">{label}</span>')
    return f'<td class="s-{status}">{inner}</td>'


def grid(matrix: dict) -> tuple[list[str], list[str], dict]:
    companies = list(dict.fromkeys(r["company"] for r in matrix["rows"]))
    features = list(dict.fromkeys(
        r["feature"].split(":")[0].strip() for r in matrix["rows"]))
    cells = {}
    for r in matrix["rows"]:
        key = (r["feature"].split(":")[0].strip(), r["company"])
        cells.setdefault(key, r)
    return features, companies, cells


def render_tabs(matrices: list[dict], locators: dict[str, str]) -> str:
    inputs, labels, panels = [], [], []
    for i, m in enumerate(matrices, start=1):
        checked = " checked" if i == 1 else ""
        inputs.append(f'<input type="radio" name="tab" id="t{i}"{checked}>')
        labels.append(f'<label for="t{i}">{html.escape(m["title"])}</label>')
        features, companies, cells = grid(m)
        head = "".join(f"<th>{html.escape(c)}</th>" for c in companies)
        body_rows = []
        for f in features:
            tds = "".join(cell_html(cells.get((f, c)), locators)
                          for c in companies)
            body_rows.append(f"<tr><th>{html.escape(f)}</th>{tds}</tr>")
        panels.append(
            '<div class="panel"><table><thead><tr><th>Feature / scenario'
            f"</th>{head}</tr></thead><tbody>{''.join(body_rows)}"
            "</tbody></table></div>")
    return (
        "<!doctype html>\n<html lang=\"en\">\n<meta charset=\"utf-8\">\n"
        "<title>Comparison deck</title>\n"
        f"<style>{STYLE}</style>\n<h1>Comparison deck</h1>\n"
        f"<p class=\"meta\">{len(matrices)} frame(s) · cells link to the "
        "retained source · statuses from the canonical matrices</p>\n"
        f"<div class=\"tabs\">{''.join(inputs)}{''.join(labels)}"
        f"{''.join(panels)}</div>\n"
        "<p class=\"legend\">substantial · partial · not_observed · "
        "not_comparable — vocabulary from the matrix cells.</p>\n"
        f"<p class=\"boundary\">{BOUNDARY}</p>\n</html>\n")


def render_heatmap(matrices: list[dict], out: Path) -> str:
    companies = list(dict.fromkeys(
        r["company"] for m in matrices for r in m["rows"]))
    head = "".join(f"<th>{html.escape(m['title'])}</th>" for m in matrices)
    body_rows = []
    for company in companies:
        tds = []
        for m in matrices:
            rows = [r for r in m["rows"] if r["company"] == company]
            if not rows:
                tds.append('<td class="s-not_observed">not compared</td>')
                continue
            counts = {s: sum(1 for r in rows if r["status"] == s)
                      for s in STATUSES}
            dominant = max(STATUSES, key=lambda s: counts[s])
            summary = " / ".join(f"{counts[s]} {s}" for s in STATUSES
                                 if counts[s])
            export = m["path"].parent / "exports" / f"{m['path'].stem}.html"
            href = os.path.relpath(export, out.parent)
            tds.append(f'<td class="s-{dominant}"><a href="{html.escape(href)}" '
                       f'rel="noopener noreferrer">{html.escape(summary)}</a></td>')
        body_rows.append(f"<tr><th>{html.escape(company)}</th>{''.join(tds)}</tr>")
    return (
        "<!doctype html>\n<html lang=\"en\">\n<meta charset=\"utf-8\">\n"
        "<title>Coverage heatmap</title>\n"
        f"<style>{STYLE}</style>\n<h1>Coverage heatmap</h1>\n"
        f"<p class=\"meta\">{len(companies)} companies × {len(matrices)} "
        "frame(s) · a cell aggregates that company's rows in that frame "
        "and links to the matrix export</p>\n"
        "<table><thead><tr><th>Company</th>"
        f"{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>\n"
        f"<p class=\"boundary\">{BOUNDARY}</p>\n</html>\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("matrices", nargs="+", type=Path)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--mode", choices=("tabs", "heatmap"), default="tabs")
    parser.add_argument("-o", "--out", type=Path, default=None)
    args = parser.parse_args()

    parsed = []
    for path in args.matrices:
        if not path.is_file():
            print(f"error: not a file: {path}", file=sys.stderr)
            return 1
        m = parse_matrix(path)
        if not m["rows"]:
            print(f"error: no matrix rows found in {path}", file=sys.stderr)
            return 1
        parsed.append(m)
    if args.mode == "tabs" and len(parsed) > 12:
        print("error: tabs mode supports up to 12 matrices", file=sys.stderr)
        return 1

    locators = load_locators(args.evidence_dir)
    out = args.out or Path(f"comparison-{args.mode}.html")
    rendered = (render_tabs(parsed, locators) if args.mode == "tabs"
                else render_heatmap(parsed, out))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    print(f"wrote {out} ({len(parsed)} matrix/matrices, mode={args.mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

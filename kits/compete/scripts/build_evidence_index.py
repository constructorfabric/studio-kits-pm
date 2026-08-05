#!/usr/bin/env python3
"""Build or extend the competitive evidence index from a retained folder.

Scans a folder of retained evidence (source extracts and fact ledgers),
harvests source records, and appends missing rows to
``<evidence-dir>/index.tsv``. The index is append-only: existing rows are
never renumbered or rewritten, so ``EVD-###`` ids stay stable.

Harvesting rules:

- **Bundle extracts** (front matter ``kind: competitive-source-extract``):
  every backtick-quoted URL in a ``Source:`` / ``Sources:`` line becomes one
  candidate record (accessed_on from the front matter).
- **Single-page extracts** (Source/Accessed/Access/Capture-method preamble):
  the ``Source:`` bullet's explicit ``EVD-###`` id is registered with its
  stated access class and capture method; the locator stays ``-`` until a
  URL is known.
- **Fact ledgers** (``*facts*.tsv``): ``evidence_refs`` tokens are collected
  and reported when they resolve neither in the existing index nor in this
  run's additions — those need a manual row or the missing extract.

New URL candidates get the next free EVD number. Existing rows win: a
candidate matching an indexed locator or evd_id is skipped.

Exit codes: 0 = pass (index written or nothing to do), 1 = usage error,
2 = unresolved references remain after the run.

Usage:
    python3 build_evidence_index.py <retained-folder> \
        --evidence-dir competitive/evidence [--dry-run] [--copy-extracts]
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
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
ACCESS_VOCAB = {"public", "gated", "unavailable", "planned", "preview"}
EVD_RE = re.compile(r"EVD-\d{3,}")
URL_RE = re.compile(r"`(https?://[^`]+)`")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Candidate:
    evd_id: str | None
    locator: str
    accessed_on: str
    access: str
    capture_method: str
    retained_path: str
    purpose: str


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


def preamble_bullet(text: str, label: str) -> str:
    """Value of a `- Label: …` bullet or bare `Label: …` preamble line."""
    m = re.search(rf"^(?:- )?{re.escape(label)}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip().strip("`") if m else ""


def normalize_access(raw: str) -> str:
    first = raw.split()[0].lower() if raw.split() else ""
    return first if first in ACCESS_VOCAB else "public"


def extract_shape(text: str) -> str | None:
    """Classify a markdown file: 'bundle', 'page', or None (not an extract).

    'page' covers both single-page preamble styles observed in retained
    evidence: bulleted (`- Source:` / `- Accessed:` / `- Access:` /
    `- Capture method:`) and minimal (bare `Source:` / `Accessed:` lines).
    """
    fm = parse_front_matter(text)
    if fm is not None:
        return "bundle" if fm.get("kind") == "competitive-source-extract" else None
    if re.search(r"^(?:- )?Source:", text, re.MULTILINE) \
            and re.search(r"^(?:- )?Accessed:", text, re.MULTILINE):
        return "page"
    return None


def harvest_extract(path: Path, retained_path: str) -> list[Candidate]:
    text = path.read_text(encoding="utf-8")
    fm = parse_front_matter(text)
    if fm is not None:
        accessed = fm.get("accessed_on", "")
        purpose = fm.get("purpose", f"Retained extract {path.name}")
        out = []
        for url in URL_RE.findall(text):
            out.append(Candidate(
                evd_id=None,
                locator=url,
                accessed_on=accessed,
                access="public",
                capture_method="retained extract",
                retained_path=retained_path,
                purpose=purpose,
            ))
        return out
    source = preamble_bullet(text, "Source")
    if not source:
        return []
    evd = EVD_RE.search(source)
    title = text.splitlines()[0].lstrip("# ").strip() if text.splitlines() else path.stem
    # Accessed may carry a trailing access note ("2026-07-15; public … page").
    accessed_raw = preamble_bullet(text, "Accessed")
    date_m = re.search(r"\d{4}-\d{2}-\d{2}", accessed_raw)
    access_note = preamble_bullet(text, "Access") or accessed_raw
    return [Candidate(
        evd_id=evd.group(0) if evd else None,
        locator=source if not evd else "-",
        accessed_on=date_m.group(0) if date_m else accessed_raw,
        access=next((w for w in re.findall(r"[a-z]+", access_note.lower()) if w in ACCESS_VOCAB), "public"),
        capture_method=preamble_bullet(text, "Capture method") or "retained extract",
        retained_path=retained_path,
        purpose=title,
    )]


def harvest_fact_refs(path: Path) -> set[str]:
    refs: set[str] = set()
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2:
        return refs
    header = lines[0].split("\t")
    try:
        col = header.index("evidence_refs")
    except ValueError:
        return refs
    for line in lines[1:]:
        cells = line.split("\t")
        if len(cells) > col:
            refs.update(EVD_RE.findall(cells[col]))
    return refs


def load_index(index_path: Path) -> tuple[dict[str, str], set[str], int]:
    """Return ({locator: evd_id}, {evd_id}, max_number)."""
    by_locator: dict[str, str] = {}
    ids: set[str] = set()
    max_n = 0
    if not index_path.is_file():
        return by_locator, ids, max_n
    lines = index_path.read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        cells = line.split("\t")
        if len(cells) < 2 or not EVD_RE.fullmatch(cells[0]):
            continue
        ids.add(cells[0])
        if cells[1] and cells[1] != "-":
            by_locator[cells[1]] = cells[0]
        max_n = max(max_n, int(cells[0].split("-")[1]))
    return by_locator, ids, max_n


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("retained", type=Path, help="folder of retained evidence to scan")
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true",
                        help="print the plan without writing anything")
    parser.add_argument("--copy-extracts", action="store_true",
                        help="copy harvested extract files into <evidence-dir>/extracts/")
    args = parser.parse_args()

    if not args.retained.is_dir():
        print(f"error: not a directory: {args.retained}", file=sys.stderr)
        return 1

    index_path = args.evidence_dir / INDEX_NAME
    by_locator, known_ids, max_n = load_index(index_path)

    candidates: list[Candidate] = []
    referenced: set[str] = set()
    copied: list[tuple[Path, Path]] = []
    for path in sorted(args.retained.rglob("*")):
        if not path.is_file() or ":Zone.Identifier" in path.name:
            continue
        if path.suffix == ".md":
            if extract_shape(path.read_text(encoding="utf-8")) is None:
                print(f"SKIP {path} (not a recognized extract shape)")
                continue
            if args.copy_extracts:
                dest = args.evidence_dir / "extracts" / path.name
                retained_rel = f"extracts/{path.name}"
                copied.append((path, dest))
            else:
                try:
                    retained_rel = str(path.resolve().relative_to(args.evidence_dir.resolve()))
                except ValueError:
                    retained_rel = str(path)
            candidates.extend(harvest_extract(path, retained_rel))
        elif path.suffix == ".tsv" and "facts" in path.name:
            referenced.update(harvest_fact_refs(path))

    additions: list[Candidate] = []
    # Reserve numbers already cited by fact ledgers and carried by harvested
    # extracts so a fresh assignment can never collide with either.
    reserved = [int(ref.split("-")[1]) for ref in referenced]
    reserved += [int(c.evd_id.split("-")[1]) for c in candidates if c.evd_id]
    next_n = max([max_n] + reserved)
    for cand in candidates:
        if cand.evd_id and cand.evd_id in known_ids:
            continue
        if cand.locator != "-" and cand.locator in by_locator:
            continue
        if not cand.evd_id:
            next_n += 1
            cand.evd_id = f"EVD-{next_n:03d}"
        if not ISO_DATE_RE.match(cand.accessed_on or ""):
            print(f"WARN {cand.locator or cand.evd_id}: no ISO accessed_on date harvested")
        known_ids.add(cand.evd_id)
        if cand.locator != "-":
            by_locator[cand.locator] = cand.evd_id
        additions.append(cand)

    unresolved = sorted(ref for ref in referenced if ref not in known_ids)

    print(f"index: {index_path} ({len(known_ids) - len(additions)} existing record(s))")
    for cand in additions:
        print(f"ADD  {cand.evd_id}\t{cand.locator}\t{cand.retained_path}")
    for ref in unresolved:
        print(f"UNRESOLVED  {ref} (cited by a fact ledger; add its source row or extract)")
    if not additions and not unresolved:
        print("nothing to add; all referenced evidence resolves")

    if args.dry_run:
        print("dry-run: nothing written")
        return 2 if unresolved else 0

    if additions or not index_path.is_file():
        index_path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not index_path.is_file()
        with index_path.open("a", encoding="utf-8") as fh:
            if new_file:
                fh.write("\t".join(INDEX_HEADER) + "\n")
            for cand in additions:
                fh.write("\t".join([
                    cand.evd_id or "-",
                    cand.locator,
                    cand.accessed_on or "-",
                    cand.access,
                    cand.capture_method,
                    cand.retained_path,
                    cand.purpose,
                ]) + "\n")
    for src, dest in copied:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            print(f"WARN {src}: {dest} already exists; not overwritten "
                  "(rename the source to keep extract basenames unique)")
            continue
        shutil.copy2(src, dest)

    print(f"wrote {len(additions)} new record(s)"
          + (f"; copied {len(copied)} extract(s)" if copied else ""))
    return 2 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())

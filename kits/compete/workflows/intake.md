---
cf-studio: true
type: workflow
name: cf-compete-intake
description: Invoke when the user asks to index retained competitive evidence — e.g. "index this evidence folder", "intake these retained sources", "register the extracts and fact ledgers", "cf-compete intake <folder>". Scans a folder of retained evidence (source extracts, fact ledgers), builds or extends the canonical EVD-### evidence index, and verifies that every cited evidence reference resolves. Run it before any research flow that must cite evidence.
version: 1.0
purpose: Build or extend the competitive evidence ledger from a folder of retained evidence
---

# Evidence Intake Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Intake + Indexing
**Role**: Evidence librarian
**Output**: `competitive/evidence/index.tsv` (+ normalized extracts under `competitive/evidence/extracts/`)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Index a folder of retained evidence | **intake.md** | "index evidence/openspec-drop", `/cf-compete-intake <folder>` |
| Record the research question | **request.md** | "find competitors to OpenSpec" |

---

## Overview

The evidence ledger is the ground truth every research artifact cites. This
workflow scans a retained-evidence folder, harvests source records into the
append-only `EVD-###` index, and verifies that every reference cited by a fact
ledger resolves. It is read-only with respect to the retained sources; the
only files it writes are the index and (optionally) copies of extracts under
`competitive/evidence/extracts/`.

Two retained-extract shapes are recognized:

- **Bundle extract** — front matter `kind: competitive-source-extract` with
  `accessed_on` and `purpose`, `Source:` URL bullets per section, and a
  terminal `## Explicit limits for reuse` section.
- **Single-page extract** — a `- Source:` / `- Accessed:` / `- Access:` /
  `- Capture method:` preamble with `## Concise extract` and `## Intake note`
  sections; its `Source` bullet may carry an explicit `EVD-###` id.

Files matching neither shape (analysis briefs, dashboards, raw notes) are
skipped and reported — normalize them into one of the shapes before indexing.

## Paths

- **Index builder**: `{scripts}/build_evidence_index.py`
- **Evidence checker**: `{scripts}/check_evidence.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/COMP-###-<slug>/facts.tsv`
- **Evidence guide**: `{cf-studio-path}/config/kits/compete` guide `guides/EVIDENCE.md`

## Route

6 steps → an extended EVD-### evidence index. Questions: 3 confirmations (Step 1: the classified set; Step 3: the dry-run plan; Step 6: closing). Steps 2, 4–5 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A retained-evidence folder is available (extracts and/or fact ledgers)
- [ ] `python3` is available for `{scripts}` (stdlib only, no dependencies)

---

## Steps

## Step 1: Enumerate and classify the retained set

List the folder's files and classify each: bundle extract, single-page
extract, fact ledger (`*facts*.tsv`), or other (analysis brief, dashboard,
note). Present the classification and confirm the set with the user
(**user gate — confirmation**).
STOP and ask for input WHEN the folder resolves to zero recognizable files.

## Step 2: Plan the index update

// turbo
Run: `python3 {scripts}/build_evidence_index.py <folder> --evidence-dir competitive/evidence --copy-extracts --dry-run`

## Step 3: Review the plan

Present the planned additions (`ADD` lines), skipped files (`SKIP` lines),
and unresolved references (`UNRESOLVED` lines). For each unresolved
`EVD-###`, either match it to a harvested source and plan a manual index row
(id, locator, accessed date, purpose), or record that its source is not in
this drop. Confirm the plan with the user (**user gate — confirmation**).

## Step 4: Apply the index update

// turbo
Run: `python3 {scripts}/build_evidence_index.py <folder> --evidence-dir competitive/evidence --copy-extracts`
Then append any manually planned rows from Step 3 to
`competitive/evidence/index.tsv` (append-only; never renumber or rewrite
existing rows).

## Step 5: Verify the ledger

// turbo
Run: `python3 {scripts}/check_evidence.py --evidence-dir competitive/evidence --companies-dir competitive/companies`
Fix findings and re-run until it reports PASS.

## Step 6: Present results

Report: records added, extracts normalized/copied, files skipped (and why),
references that remain unresolved (these block any artifact that would cite
them). Present next steps and wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Every recognized extract is indexed; every skipped file is reported with its reason
- [ ] `EVD-###` ids are append-only: no existing row was renumbered or rewritten
- [ ] Every fact-ledger `evidence_refs` token resolves, or is explicitly reported unresolved
- [ ] `check_evidence.py` reports PASS

---

## Next Steps

- Evidence indexed and a RESEARCH-REQUEST exists → the research flows can cite `EVD-###` records (candidate register arrives in the next kit version)
- No RESEARCH-REQUEST yet → `cf-compete-request` records the research question
- New evidence drop → re-run this intake; the index extends without renumbering

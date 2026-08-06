---
cf-studio: true
type: workflow
name: cf-compete-taxonomy
description: Invoke when comparison rows must be normalized before a matrix — e.g. "build the feature taxonomy", "how do we compare apples to apples?", "normalize the feature list across vendors", "cf-compete taxonomy <frame>". Builds a FEATURE-TAXONOMY: the union of every compared vendor's mined feature inventory plus the requester's role frames, normalized into 8–20 decidable rows with per-vendor alias mappings and a provenance audit — the anchor-bias defence every later matrix inherits. Backed by the deterministic mine_terms.py harvest and coverage reports.
version: 1.0
purpose: Normalize a comparison frame's rows as a union-derived, evidence-backed feature taxonomy
---

# Feature Taxonomy Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Analysis + Normalization
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/FEATURE-TAXONOMY/{yyyy-mm-dd}-{slug}.md` (+ csv/html exports)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Normalize comparison rows | **taxonomy.md** | "build the feature taxonomy", `/cf-compete-taxonomy` |
| Compare against fixed rows | **compare.md** | "build the coverage matrix" |
| Mine a vendor's corpus first | **capture.md** | "capture <vendor>'s docs" |

---

## Overview

Produces one FEATURE-TAXONOMY artifact per comparison frame: the
normalization contract later matrices compare against. The row set is
built as the **union** of every compared vendor's independently mined
feature inventory plus the requester's role/stage frames — never from
the first vendors' feature list, which is exactly the anchor bias this
kind exists to prevent. Every row carries a definition and an inclusion
criterion two analysts would apply identically; every vendor's own
wording is mapped verbatim in the alias table; and the provenance
section proves where each row came from. Row inclusion is never a
capability claim — cells belong to matrices.

The deterministic seed comes from `{scripts}/mine_terms.py` (candidate
terms per subject; single-subject terms are the rows an anchored process
would miss); the coverage mode verifies that every fixed row and alias
resolves to corpus hits. The workflow authors the artifact per
`{feature_taxonomy_rules}` and validates it against
`{feature_taxonomy_checklist}`.

## Paths

- **Template**: `{feature_taxonomy_template}`
- **Rules**: `{feature_taxonomy_rules}`
- **Checklist**: `{feature_taxonomy_checklist}`
- **Example**: `{feature_taxonomy_example}`
- **Term miner**: `{scripts}/mine_terms.py`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

7 steps → FEATURE-TAXONOMY (+ csv/html exports). Questions: 1 decision
(Step 2: the taxonomy design — rows, aliases, provenance), 1 closing
confirmation (Step 7). Steps 3–6 run without questions. Announce the
route before Step 1 and prefix every question per the SKILL.md progress
protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered with the frame to normalize (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] Every compared vendor has a mined corpus in the evidence index; route missing corpora to `cf-compete-capture` (corpus mode) first (or the completeness note must name them as unmined)
- [ ] `python3` is available; `{cf-studio-path}/config/artifacts.toml` is writable

---

## Steps

## Step 1: Mine the union

Resolve the commissioning RESEARCH-REQUEST and its frame (`cfs
list-ids`); no question yet.
// turbo
Run: `python3 {scripts}/mine_terms.py --evidence-dir competitive/evidence`
Then mine every compared vendor's corpus independently into a candidate
feature inventory (the harvest report seeds this; single-subject terms
deserve special attention — they are what anchoring loses). Build the
candidate row set as the union of all inventories plus the requester's
role/stage frames, normalize labels to domain-standard wording, and
draft definitions, inclusion criteria, and per-vendor aliases.
STOP WHEN no RESEARCH-REQUEST resolves, or a compared vendor's corpus is
missing and the user has not accepted an unmined-vendor completeness
note.

## Step 2: Confirm the taxonomy design

Present one numbered proposal — any user-accepted unmined vendors named
first (they become the Section 2 completeness note CPT-TAX-NO-001
exempts), then the row set (8–20 per frame, with the
reason when outside the band), each row's definition and inclusion
criterion, the alias map, the provenance table showing which source
contributed which rows, and any rows kept despite single-source
evidence — with the recommended design as option 1
(**user gate — decision**). Removing a union-derived row requires the
user's explicit say-so.

## Step 3: Author the FEATURE-TAXONOMY artifact

Load `{feature_taxonomy_template}` and `{feature_taxonomy_example}`.
Follow `{feature_taxonomy_rules}`:
- Resolve the FEATURE-TAXONOMY directory from `artifacts.toml`; set the
  path `{artifacts_dir}/FEATURE-TAXONOMY/{yyyy-mm-dd}-{slug}.md` and
  register it.
- Author Sections 1–8: the normalization-contract scope statement;
  evidence scope naming the mined corpora; the feature rows; the vendor
  aliases (verbatim, evidenced); the union provenance with every
  compared vendor listed; the boundary (inclusion is not availability);
  original files including the harvest invocation; traceability
  carrying the commissioning request ID.
- Set the ID `cpt-{system}-tax-{slug}`; verify uniqueness with
  `cfs list-ids`; an existing ID means refresh mode — update the
  registered file in place, never a second file with the same ID.
- Update the commissioning request's Traceability section idempotently:
  append the back-link only when the ID is absent (replace the default
  no-derived-artifacts line when present); a refresh updates the existing
  line instead of duplicating it and collapses any duplicate lines for
  this ID left by earlier runs into one.

## Step 4: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`,
`cfs validate-toc <artifact-file>`, and
`python3 {scripts}/check_artifact_refs.py <artifact-file> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language`.
Fix and re-run until all report PASS (this enforces the per-row evidence
duty and warns outside the 8–20 band).

## Step 5: Verify corpus coverage

// turbo
Run: `python3 {scripts}/mine_terms.py --evidence-dir competitive/evidence --taxonomy <artifact-file>`
A row or alias without corpus hits is a mining/capture target or a wrong
evidence reference — resolve each before proceeding (fix the artifact,
or record the row's pending corpus in completeness).

## Step 6: Render the exports

// turbo
Run: `python3 {scripts}/render_views.py <artifact-file> --format csv,html`
The markdown artifact is canonical; never hand-edit the exports.
Then load `{feature_taxonomy_checklist}` and review the artifact against
it (UNION / ROWS / ALIAS / TRC); apply approved fixes and re-run
Steps 4–6.

## Step 7: Present results

Summarize: the row count and band status, rows per provenance source
(highlighting single-source rows the union preserved), alias coverage,
and the coverage-report verdict. Present next steps and wait for the
user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Every compared vendor's corpus was mined before the row set was fixed; unmined vendors are named in completeness
- [ ] Union provenance lists every compared vendor (or its explicit no-rows line); single-source rows preserved
- [ ] 8–20 rows per frame or a stated reason; every row has a decidable inclusion criterion and evidence
- [ ] Every alias verbatim and evidenced; mine_terms coverage reports no unexplained misses
- [ ] The commissioning request's Traceability section back-references this taxonomy
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] csv/html exports regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Taxonomy fixed → `cf-compete-compare` builds matrices against its rows
- Coverage misses → `cf-compete-capture` the missing corpora, then refresh this taxonomy (same tax ID)
- Frame changed → revise the RESEARCH-REQUEST first, then re-derive the union

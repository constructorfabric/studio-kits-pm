---
cf-studio: true
type: workflow
name: cf-compete-compare
description: Invoke when the user asks to compare selected companies under one frame — e.g. "compare A and B on <frame>", "build the coverage matrix", "where do we stand against <companies>?", "cf-compete compare". Builds a single-frame COMPARISON-MATRIX (Flow 6) whose every cell carries mechanism, status (substantial/partial/not_observed/not_comparable), availability (current/planned/vision), observation date, boundary, and evidence — never a winner/loser score or ranking.
version: 1.2
purpose: Compare selected companies under exactly one frame (Flow 6) with the full per-cell evidence contract
---

# Compare Companies Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Analysis + Synthesis
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/COMPARISON-MATRIX/{yyyy-mm-dd}-{slug}.md` (+ csv/html exports)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Compare companies under one frame | **compare.md** | "compare OpenSpec and Kiro on the lifecycle frame", `/cf-compete-compare` |
| Profile a company first | **profile.md** | "profile <company>" |
| Deepen one company's evidence | **dossier.md** | "deep dossier on <company>" |

---

## Overview

Produces one COMPARISON-MATRIX artifact per run: the selected companies
compared under exactly one frame (role × stage/job taxonomy, product
outcome frame, or a named mechanism lens). Every cell carries the full
contract — feature/mechanism, status, availability, observation date,
documented boundary, evidence. A matrix answers its frame's question; it
never ranks, scores winners, or converts missing documentation into
absence. When Studio is among the compared, Studio today and Studio vision
stay separate.

The workflow authors the artifact per `{comparison_matrix_rules}` and
validates it against `{comparison_matrix_checklist}`. Besides the artifact
it only touches the commissioning request's Traceability section (the
mandatory back-link) and the derived csv/html exports.

## Paths

- **Template**: `{comparison_matrix_template}`
- **Rules**: `{comparison_matrix_rules}`
- **Checklist**: `{comparison_matrix_checklist}`
- **Example**: `{comparison_matrix_example}`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

7 steps → COMPARISON-MATRIX (+ csv/html exports). Questions: 1 decision (Step 2: the comparison design — frame, compared set with exclusions, row labels), 1 closing confirmation (Step 7). Steps 3–6 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] A FEATURE-TAXONOMY exists for the frame (check `cfs list-ids`); build one with `cf-compete-taxonomy` when missing — ad-hoc rows are accepted only when the user explicitly declines a taxonomy
- [ ] The compared companies are evidenced at comparison depth (profiles/dossiers or indexed evidence); run `cf-compete-profile` / `cf-compete-intake` first when not
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Derive the comparison design

Identify the commissioning RESEARCH-REQUEST (`cfs list-ids`) and prepare
the full comparison design without asking anything yet:
- **Frame** — exactly one, from the request; when the request states
  none, derive candidate frames from its scope with one recommended.
- **Compared set** — candidate companies with the evidence depth behind
  each (profile, dossier, or indexed evidence only), checked against the
  register's direct candidates: every direct candidate left out is an
  explicit exclusion with a reason (under-evidenced, out of frame,
  deferred). For an under-evidenced company prepare the options: drop the
  column, profile it first, or keep it with all cells not_observed.
- **Row labels** — the frame's FEATURE-TAXONOMY rows (declare the
  taxonomy in the artifact's frontmatter `taxonomy:` key); every
  taxonomy row appears for every compared company — not_observed where
  evidence lacks — which is what keeps the matrix at PM-grade density
  (8–20 rows). Only when the user explicitly declines a taxonomy:
  ad-hoc labels, domain-standard wording, never one vendor's term.
STOP WHEN no RESEARCH-REQUEST resolves.

## Step 2: Confirm the comparison design

Present the three parts as one numbered proposal — the frame (stated both
as the question it answers and the question it does not), the compared
set with named exclusions, and the row labels — with the recommended
design as option 1 (**user gate — decision**). When the user picks a
frame the request does not state, record it in the request first.

## Step 3: Author the COMPARISON-MATRIX artifact

Load `{comparison_matrix_template}` and `{comparison_matrix_example}`.
Follow `{comparison_matrix_rules}`:
- Resolve the COMPARISON-MATRIX directory from `artifacts.toml`; set the
  path `{artifacts_dir}/COMPARISON-MATRIX/{yyyy-mm-dd}-{slug}.md` and
  register it.
- Author Sections 1–7: the frame both ways; evidence scope; the matrix with
  the full per-cell contract (status, availability, ISO observed_on,
  boundary, evidence per row); Studio Position when Studio is compared
  (today vs vision, never merged); the readable conclusion including
  negative findings; the boundary; original files.
- Set the matrix ID `cpt-{system}-cmp-{slug}`; verify uniqueness with
  `cfs list-ids`; an existing ID means refresh mode — update the
  registered file in place, never a second file with the same ID.
- Update the commissioning request's Traceability section idempotently:
  append the back-link only when the ID is absent (replace the default
  no-derived-artifacts line when present); a refresh updates the existing
  line instead of duplicating it and collapses any duplicate lines for
  this ID left by earlier runs into one; a stale no-derived-artifacts
  line is removed whenever any back-link is present.

## Step 4: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`,
`cfs validate-toc <artifact-file>`, and
`python3 {scripts}/check_artifact_refs.py <artifact-file> --evidence-dir competitive/evidence --companies-dir competitive/companies --artifacts-dir <artifacts-dir> --lint-language`.
Fix and re-run until all report PASS (with a declared taxonomy this
enforces rows ⊆ taxonomy and every-row-covered).

## Step 5: Render the exports

// turbo
Run: `python3 {scripts}/render_views.py <artifact-file> --format csv,html`
When several matrices exist for the run, refresh the deck views too:
// turbo
Run: `python3 {scripts}/render_matrix_deck.py <matrix files…> --evidence-dir competitive/evidence --mode tabs -o {artifacts_dir}/COMPARISON-MATRIX/exports/comparison-tabs.html`
// turbo
Run: `python3 {scripts}/render_matrix_deck.py <matrix files…> --evidence-dir competitive/evidence --mode heatmap -o {artifacts_dir}/COMPARISON-MATRIX/exports/comparison-heatmap.html`
The markdown artifacts are canonical; never hand-edit the exports.

## Step 6: Semantic self-review

Load `{comparison_matrix_checklist}` and review the artifact against it
(FRAME / CELL / CONC / STUD / TRC). Apply approved fixes, then re-run
Steps 4–5.

## Step 7: Present results

Summarize: the frame, per-company coverage within it, the negative
findings, and the not_observed cells that matter. Present next steps and
wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Exactly one frame, stated as the question answered and the question not answered
- [ ] Rows come from the declared FEATURE-TAXONOMY (frontmatter `taxonomy:`), every taxonomy row covered for every compared company — or the user explicitly declined a taxonomy
- [ ] Every matrix row: normalized label, status/availability from the documented vocabularies, ISO observed_on, substantive boundary, ≥1 resolvable evidence reference
- [ ] not_observed / not_comparable used honestly, with reasons; never rendered as absence
- [ ] Studio today separate from Studio vision whenever Studio is compared
- [ ] Conclusion includes the negative findings and declares no winner
- [ ] The commissioning request's Traceability section back-references this matrix
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] csv/html exports regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Cells not_observed that matter → deepen evidence (dossier, hands-on request) and refresh
- A second lens wanted → a second single-frame matrix over the same companies
- A proposed action from the conclusion → record it as a product hypothesis for human decision, outside this kit

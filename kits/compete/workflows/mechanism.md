---
cf-studio: true
type: workflow
name: cf-compete-mechanism
description: Invoke when the user asks a narrow mechanism or product-gap question — e.g. "who detects requirement contradictions?", "map the mechanisms for <capability>", "is there whitespace around <mechanism>?", "cf-compete mechanism". Builds a MECHANISM-STUDY (Flow 8) — a map of documented mechanisms (rows are mechanisms, not companies) with inputs, documented actions, analogues, and unobserved elements; any requester direction is a labelled product hypothesis, never a commitment or ranking.
version: 1.0
purpose: Study one mechanism or product gap (Flow 8) across documented analogues
---

# Mechanism Study Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Analysis + Synthesis
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/MECHANISM-STUDY/{yyyy-mm-dd}-{slug}.md` (+ csv/html exports)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Narrow mechanism / whitespace question | **mechanism.md** | "who detects requirement contradictions?", `/cf-compete-mechanism` |
| Compare companies under a frame | **compare.md** | "compare A and B on <frame>" |
| Index retained evidence first | **intake.md** | "index this evidence folder" |

---

## Overview

Produces one MECHANISM-STUDY artifact per run, for a narrow question that
mechanism documentation can answer. Rows of the map are mechanisms, not
companies: each carries the closest documented analogue, the direct input
it processes, the documented action including output/review behaviour, the
unobserved elements, and evidence. The study also prescribes the fields a
later comparison must record (so unlike surfaces are not conflated) and may
derive one labelled product hypothesis from the observed whitespace. It
never ranks and never converts one vendor's documentation into another's
gap.

The workflow authors the artifact per `{mechanism_study_rules}` and
validates it against `{mechanism_study_checklist}`. Besides the artifact it
only touches the commissioning request's Traceability section (the
mandatory back-link) and the derived csv/html exports.

## Paths

- **Template**: `{mechanism_study_template}`
- **Rules**: `{mechanism_study_rules}`
- **Checklist**: `{mechanism_study_checklist}`
- **Example**: `{mechanism_study_example}`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

7 steps → MECHANISM-STUDY (+ csv/html exports). Questions: 1 decision (Step 1: the narrow question), 1 confirmation (Step 2: the normalized mechanism set), 1 closing confirmation (Step 7). Steps 3–6 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] The evidence for the offerings in scope is indexed; run `cf-compete-intake` when not
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the request and narrow the question

Identify the commissioning RESEARCH-REQUEST (`cfs list-ids`). Verify the
question is mechanism-narrow; when it spans product categories, propose
narrower mechanism-level questions and wait for the user's choice. Confirm
the question and the direct-vs-adjacent separation rule with the user
(**user gate — decision**).
STOP WHEN no RESEARCH-REQUEST resolves.

## Step 2: Collect and normalize the mechanisms

Read the indexed evidence for the offerings in scope. Collect candidate
mechanisms, separate direct mechanisms from adjacent surfaces, and
normalize mechanism names across vendors (domain-standard wording, never
one vendor's label). Present the mechanism list — including borderline
surfaces and how they were classified — and confirm with the user
(**user gate — confirmation**). A mechanism without a documented analogue
is a whitespace observation: record it as a research limitation or
follow-up target (and, when warranted, the seed of Section 5's product
hypothesis) — it enters the Mechanism Map only once a documented
analogue, action, and resolvable evidence support it.

## Step 3: Author the MECHANISM-STUDY artifact

Load `{mechanism_study_template}` and `{mechanism_study_example}`. Follow
`{mechanism_study_rules}`:
- Resolve the MECHANISM-STUDY directory from `artifacts.toml`; set the
  path `{artifacts_dir}/MECHANISM-STUDY/{yyyy-mm-dd}-{slug}.md` and
  register it.
- Author Sections 1–7: the not-a-ranking scope; evidence scope; the
  mechanism map (analogue, direct input, documented action with
  output/review behaviour, unobserved elements, evidence per row); the
  comparison fields and the conflations they prevent; the optional
  labelled product hypothesis; the boundary; original files.
- Set the study ID `cpt-{system}-mech-{slug}`; verify uniqueness with
  `cfs list-ids`.
- Update the commissioning request's Traceability section idempotently:
  append the back-link only when the ID is absent (replace the default
  no-derived-artifacts line when present); a refresh updates the existing
  line instead of duplicating it.

## Step 4: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`,
`cfs validate-toc <artifact-file>`, and
`python3 {scripts}/check_artifact_refs.py <artifact-file> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language`.
Fix and re-run until all report PASS.

## Step 5: Render the exports

// turbo
Run: `python3 {scripts}/render_views.py <artifact-file> --format csv,html`
The markdown artifact is canonical; never hand-edit the exports.

## Step 6: Semantic self-review

Load `{mechanism_study_checklist}` and review the artifact against it
(MECH / WHIT / EVID / TRC). Apply approved fixes, then re-run Steps 4–5.

## Step 7: Present results

Summarize: the mechanisms mapped with their analogues, the whitespace
observed, the prescribed comparison fields, and the hypothesis when one was
derived. Present next steps and wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Rows are mechanisms with normalized names; companies appear only as observed examples
- [ ] Every row: direct input, documented action with output/review behaviour, substantive unobserved-elements cell, ≥1 resolvable evidence reference
- [ ] Comparison fields prescribed with the conflations they prevent
- [ ] Any requester direction is a labelled product hypothesis with the not-a-commitment sentence
- [ ] The commissioning request's Traceability section back-references this study
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] csv/html exports regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Whitespace with a hypothesis → record it for human product decision, outside this kit
- Analogue worth depth → `cf-compete-profile` or `cf-compete-dossier` for that vendor
- Mechanisms mature for comparison → `cf-compete-compare` with a mechanism-lens frame using the prescribed fields

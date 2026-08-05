---
cf-studio: true
type: workflow
name: cf-compete-discover
description: Invoke when the user asks to discover competitors for a recorded research request — e.g. "find competitors to OpenSpec", "build the candidate register", "who are the peers of <target>?", "cf-compete discover <request-id>". Builds a source-backed CANDIDATE-REGISTER (Flow 2) from the request scope and the indexed evidence — leads with classification and next actions, never feature scores or rankings.
version: 1.2
purpose: Build a candidate competitor register (Flow 2) from a research request and indexed evidence
---

# Discover Competitors Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Analysis + Synthesis
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/CANDIDATE-REGISTER/{yyyy-mm-dd}-{slug}.md` (+ csv/html exports)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Build/refresh a candidate register | **discover.md** | "find competitors to OpenSpec", `/cf-compete-discover` |
| Record the research question first | **request.md** | "set up a research request for <target>" |
| Index retained evidence first | **intake.md** | "index this evidence folder" |

---

## Overview

Produces one CANDIDATE-REGISTER artifact per run: a source-backed list of
possible direct, adjacent, or emerging competitors for an approved
RESEARCH-REQUEST. Every candidate carries a classification, the screening
question that puts it in scope, at least one resolvable evidence reference,
and a concrete next research action. A register records leads and routing —
it never scores features, confirms competitors, or ranks anything.

The workflow authors the artifact per `{candidate_register_rules}` and
validates it against `{candidate_register_checklist}`. It is read-only with
respect to the evidence layer; besides the artifact it only touches the
commissioning request's Traceability section (the mandatory back-link) and
the derived csv/html exports.

## Paths

- **Template**: `{candidate_register_template}`
- **Rules**: `{candidate_register_rules}`
- **Checklist**: `{candidate_register_checklist}`
- **Example**: `{candidate_register_example}`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

7 steps → CANDIDATE-REGISTER (+ csv/html exports). Questions: 1 decision (Step 2: the discovery design — candidate set, classifications, exclusions), 1 closing confirmation (Step 7). Steps 3–6 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] The evidence to be cited is indexed (`competitive/evidence/index.tsv`); run `cf-compete-intake` when not
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the request and survey the evidence

Identify the RESEARCH-REQUEST this register answers (`cfs list-ids`, or
the one just recorded) and read its scope, comparison frame, depth, and
evidence boundary — they bound this run (no question is asked yet). Read the
evidence index, the retained extracts, and any fact ledgers or analysis
briefs in scope, and collect candidate names with the evidence that makes
each worth examining. Where an analysis brief already ranks or shortlists
candidates, keep its selection rationale but re-derive the classification
yourself from the request scope.

**Search-assisted widening (optional)** — WHEN the request's access
boundary allows live public sources AND the host session provides a
web-search tool: reformulate the request's decision question and problem
statements into search queries and surface additional candidate names.
A search result is a lead to a lead: before such a candidate can enter
the register, its pages must be captured (`cf-compete-capture`) and
indexed so the candidate row has resolvable evidence.

For each candidate assign: classification (baseline for the request's own
target; direct / adjacent / emerging per the request scope), known
aliases, the screening question it answers, evidence references, and a
concrete next action.
STOP WHEN no RESEARCH-REQUEST resolves.

## Step 2: Confirm the discovery design

Present one numbered proposal — the request scope being answered, the
classified candidate table, the search-widened additions (marked, with
their capture-first requirement), and any candidates considered and
excluded with reasons — with the recommended set as option 1
(**user gate — decision**). An empty candidate set is a valid outcome;
record it honestly with a completeness note.

## Step 3: Author the CANDIDATE-REGISTER artifact

Load `{candidate_register_template}` and `{candidate_register_example}`.
Follow `{candidate_register_rules}`:
- Resolve the CANDIDATE-REGISTER directory from `artifacts.toml`; set the
  path `{artifacts_dir}/CANDIDATE-REGISTER/{yyyy-mm-dd}-{slug}.md` and
  register it.
- Author Sections 1–5 (scope statement opening with what the register is
  NOT, evidence scope with cutoff, the confirmed candidate table, boundary,
  original files).
- Set the register ID `cpt-{system}-reg-{slug}`; verify uniqueness with
  `cfs list-ids`.
- Append the back-link to the commissioning request's Traceability section
  (replace its default no-derived-artifacts line when present).

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

Load `{candidate_register_checklist}` and review the artifact against it
(SCOPE / CAND / TRC). Apply approved fixes, then re-run Steps 4–5.

## Step 7: Present results

Summarize: candidates by classification, the evidence base, exclusions with
reasons, and the per-candidate next actions. Present next steps and wait for
the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Register opens by stating it is not a feature-parity or ranking result
- [ ] Every candidate row: classification from the documented set, ≥1 resolvable evidence reference, concrete next action
- [ ] Evidence Scope states the cutoff, access boundary, depth, and completeness
- [ ] The commissioning request's Traceability section back-references this register
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] csv/html exports regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Profile-worthy lead → `cf-compete-profile` builds a standard company profile (arrives with the COMPANY-PROFILE kind)
- New evidence drop → `cf-compete-intake`, then refresh this register (same reg ID)
- Scope change → revise the RESEARCH-REQUEST first, then re-run discovery

---
cf-studio: true
type: workflow
name: cf-compete-review
description: Invoke when the user asks to audit a research run's artifact set — e.g. "review the research run", "how complete is the competitive research?", "audit the artifacts against the request", "what should we research next?", "cf-compete review". Builds a RESEARCH-REVIEW artifact: requirements conformance per commissioned flow, register next-action coverage (backed by the deterministic check_coverage.py report), informativeness findings with severities, and an ordered list of recommended next passes. The review adds no research content and ranks nothing — its output is research routing.
version: 1.0
purpose: Audit a research run's artifact set for conformance, coverage, and informativeness — the kit's quality loop
---

# Research Review Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Audit + Synthesis
**Role**: Research quality reviewer
**Output**: `{artifacts_dir}/RESEARCH-REVIEW/{yyyy-mm-dd}-{slug}.md` (+ csv/html exports)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Audit the run's artifact set | **review.md** | "review the research run", `/cf-compete-review` |
| Execute a recommended pass | the named workflow | "profile <company>" → **profile.md** |
| Fix a conformance gap | the artifact's authoring workflow | "re-run the matrix" → **compare.md** |

---

## Overview

Produces one RESEARCH-REVIEW artifact per run: the kit's quality-loop
output. It reads every artifact derived from one RESEARCH-REQUEST and
answers three questions no single-artifact check can: does each artifact
conform to its flow's required content (the conformance contract in
`{research_review_rules}` plus the request's requested output); which
register next actions were executed and which remain open; and what limits
the set's informativeness for the decision question — with each finding
translated into a concrete recommended next pass.

The deterministic half comes from `{scripts}/check_coverage.py` (flow
coverage, next-action matching, evidence density, fact ledgers, exports,
watch freshness, traceability sweep); the semantic half — conformance
verdicts and findings — comes from reading the artifacts. The review adds
no vendor claims and no evidence: an audit, never a research pass. Re-run
it after executing recommended passes to measure the closure.

## Paths

- **Template**: `{research_review_template}`
- **Rules**: `{research_review_rules}` (includes the per-flow conformance contract)
- **Checklist**: `{research_review_checklist}`
- **Example**: `{research_review_example}`
- **Coverage reporter**: `{scripts}/check_coverage.py`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

9 steps → RESEARCH-REVIEW (+ csv/html exports). Questions: 3 confirmations (Step 1: the reviewed set; Step 4: verdicts and coverage; Step 9: closing). Steps 2–3 and 5–8 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered with at least one derived artifact (check `cfs list-ids`); there is nothing to review otherwise
- [ ] `python3` is available for the coverage reporter
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the request and the reviewed set

Identify the commissioning RESEARCH-REQUEST (`cfs list-ids`) and collect
its derived artifacts from the Traceability section and the artifact
directories. Confirm the reviewed set with the user (**user gate — confirmation**).
STOP WHEN no RESEARCH-REQUEST resolves or it has no derived artifacts.

## Step 2: Run the coverage report

// turbo
Run: `python3 {scripts}/check_coverage.py <artifacts-dir> --evidence-dir competitive/evidence --companies-dir competitive/companies`
Retain the full report: flow coverage, register next actions, evidence
density, fact ledgers, exports, watch freshness, traceability sweep.
For an express run, also read the run log: its first entry must record
the user's plan approval — an express run without one is a
protocol-violation finding (high severity) in Section 5, regardless of
how well the artifacts validate.

## Step 3: Verdict requirements conformance

For each commissioned flow, read the artifact and verdict it against the
conformance contract in `{research_review_rules}` plus the request's
Requested output field: met | partial | gap | not_commissioned. A verdict
is formed by reading the artifact — never from the coverage report alone —
and a partial/gap finding names the exact missing content.

## Step 4: Confirm run coverage

Take the coverage report's next-action table and correct its
name-matching by hand: a done/partial row's fulfilling artifact must
genuinely be about that candidate. Statuses: done | partial | open |
superseded (superseded only with the user's say-so). Present conformance
verdicts and coverage rows together (**user gate — confirmation**).

## Step 5: Author the RESEARCH-REVIEW artifact

Load `{research_review_template}` and `{research_review_example}`. Follow
`{research_review_rules}`:
- Resolve the RESEARCH-REVIEW directory from `artifacts.toml`; set the
  path `{artifacts_dir}/RESEARCH-REVIEW/{yyyy-mm-dd}-{slug}.md` and
  register it.
- Author Sections 1–8: review scope with the not-a-research-result
  statement; evidence scope; the conformance table; the coverage table;
  informativeness findings (severity, affected artifacts, one concrete
  recommended action each — an honestly-declared evidence limit is a
  run-level finding, never an artifact defect); the ordered recommended
  next passes, each naming a kit workflow and subject; boundary; original
  files including how the coverage report was produced.
- Set the ID `cpt-{system}-rev-{slug}`; verify uniqueness with
  `cfs list-ids`.
- Append the back-link to the commissioning request's Traceability section
  (replace its default no-derived-artifacts line when present).

## Step 6: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`,
`cfs validate-toc <artifact-file>`, and
`python3 {scripts}/check_artifact_refs.py <artifact-file> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language`.
Fix and re-run until all report PASS.

## Step 7: Render the exports

// turbo
Run: `python3 {scripts}/render_views.py <artifact-file> --format csv,html`
The markdown artifact is canonical; never hand-edit the exports.

## Step 8: Semantic self-review

Load `{research_review_checklist}` and review the artifact against it
(CONF / COV / INF / TRC). Apply approved fixes, then re-run Steps 6–7.

## Step 9: Present results

Summarize: conformance verdicts (gaps first), open next actions, findings
by severity, and the ordered recommended passes. Present next steps and
wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Every commissioned flow has a conformance row; every verdict names its artifact or its exact missing content
- [ ] Every register next action appears in Run Coverage; done/partial rows name a genuinely matching artifact
- [ ] Every finding: severity, affected artifacts, one concrete recommended action naming a workflow and subject
- [ ] No evidence limit rendered as a conformance failure; no new research content; no rankings
- [ ] The commissioning request's Traceability section back-references this review
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] csv/html exports regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Open actions or findings → run the recommended passes, then re-run `cf-compete-review` to measure the closure
- Conformance gap → re-run that artifact's authoring workflow against its checklist, then re-review
- Requested output itself outdated → revise the RESEARCH-REQUEST first, then re-review

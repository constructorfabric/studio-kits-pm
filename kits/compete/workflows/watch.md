---
cf-studio: true
type: workflow
name: cf-compete-watch
description: Invoke when the user asks to watch a competitor for changes — e.g. "set up a watch on <company>", "what changed since the last pass?", "run the quarterly watch", "cf-compete watch <subject>". Runs one WATCH-REPORT pass (Flow 9): the first pass publishes a dated baseline register; later passes publish dated change records (prior/current observation, date, why it matters) against the prior retained report. A change signal never becomes an impact claim.
version: 1.0
purpose: Establish or run a competitive watch pass (Flow 9) — baseline first, then dated change reports
---

# Watch Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Monitoring
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/WATCH-REPORT/{yyyy-mm-dd}-{slug}.md` (+ csv/html exports)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Establish or run a watch pass | **watch.md** | "set up a watch on OpenSpec", "what changed?", `/cf-compete-watch` |
| Fresh evidence for the pass | **intake.md** | "index this evidence folder" |
| A change warrants depth | **profile.md** / **dossier.md** | "profile <company>" |

---

## Overview

Produces one WATCH-REPORT artifact per pass. The first pass over a subject
publishes a **baseline**: every watched field's dated observation plus a
concrete next comparison rule defining what would count as a material
change. Every later pass runs in **change-report** mode: it compares the
current observations against the prior retained report and records each
change with its prior observation, current observation, date, evidence, and
why it matters to the research question. A change signal never becomes a
customer, revenue, or strategic impact claim, and an unobservable field is
recorded in completeness, never inferred unchanged.

The workflow authors the artifact per `{watch_report_rules}` and validates
it against `{watch_report_checklist}`. Besides the artifact it only touches
the commissioning request's Traceability section (the mandatory back-link)
and the derived csv/html exports.

## Paths

- **Template**: `{watch_report_template}`
- **Rules**: `{watch_report_rules}`
- **Checklist**: `{watch_report_checklist}`
- **Example**: `{watch_report_example}`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

8 steps → WATCH-REPORT (+ csv/html exports). Questions: 1 confirmation (Step 1: mode and watched fields), 1 conditional decision (Step 2: only when the evidence is staler than the cadence — intake first or proceed), 1 confirmation (Step 3: the observations), 1 closing confirmation (Step 8). Steps 4–7 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered with the watch scope and cadence (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] Evidence current enough for this pass is indexed; run `cf-compete-intake` on a fresh drop first when not
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the request, subject, and mode

Identify the commissioning RESEARCH-REQUEST and any prior WATCH-REPORT for
the subject (`cfs list-ids`). Mode is change-report when a prior report
exists, baseline otherwise. Confirm the watched-field set and cadence from
the request — changes to the set need a request revision first
(**user gate — confirmation**).
STOP WHEN no RESEARCH-REQUEST resolves.

## Step 2: Check evidence freshness

Compare the indexed evidence dates against the cadence window. When the
evidence predates the window, offer: intake a fresh drop first
(`cf-compete-intake`), or proceed with completeness noting the stale window
(**user gate — decision**).

## Step 3: Observe the watched fields

For each watched field, derive the current dated observation from the
indexed evidence. In change-report mode, place it beside the prior
report's observation and decide per the field's next comparison rule
whether a material change occurred. Present observations and change
candidates for confirmation (**user gate — confirmation**). A field with no current
observation goes to completeness, never silently carried forward.

## Step 4: Author the WATCH-REPORT artifact

Load `{watch_report_template}` and `{watch_report_example}`. Follow
`{watch_report_rules}`:
- Resolve the WATCH-REPORT directory from `artifacts.toml`; set the path
  `{artifacts_dir}/WATCH-REPORT/{yyyy-mm-dd}-{slug}.md` and register it.
- Author the sections per mode: scope with the no-impact statement;
  evidence scope; watch status (naming the prior report in change-report
  mode); the register with dated observations and concrete comparison
  rules; Detected Changes (change-report mode: full prior/current/date/why
  rows, or the explicit no-material-change line; baseline mode: omitted);
  boundary; original files.
- Set this pass's ID `cpt-{system}-wat-{slug}`; verify uniqueness with
  `cfs list-ids`.
- Append the back-link to the commissioning request's Traceability section
  (replace its default no-derived-artifacts line when present).

## Step 5: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`,
`cfs validate-toc <artifact-file>`, and
`python3 {scripts}/check_artifact_refs.py <artifact-file> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language`.
Fix and re-run until all report PASS.

## Step 6: Render the exports

// turbo
Run: `python3 {scripts}/render_views.py <artifact-file> --format csv,html`
The markdown artifact is canonical; never hand-edit the exports.

## Step 7: Semantic self-review

Load `{watch_report_checklist}` and review the artifact against it
(REG / CHG / EVID / TRC). Apply approved fixes, then re-run Steps 5–6.

## Step 8: Present results

Summarize: the mode, the register state, detected changes with their
why-it-matters (or the explicit no-change result), and fields that could
not be observed. Present next steps and wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Mode correct: baseline only when no prior retained report exists; change-report names the prior report
- [ ] Every register row: dated observation, evidence, concrete next comparison rule
- [ ] Every change row: prior observation, current observation, ISO date, signal-level why-it-matters, evidence
- [ ] Unobservable fields recorded in completeness, never inferred unchanged
- [ ] No impact claims anywhere; no rankings or momentum conclusions
- [ ] The commissioning request's Traceability section back-references this report
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] csv/html exports regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Baseline established → intake a fresh drop at the cadence, then run the next pass
- Material change detected → commission the follow-up its comparison rule implies (profile refresh, dossier, comparison)
- Watched set changed → revise the RESEARCH-REQUEST first, then re-baseline the new fields

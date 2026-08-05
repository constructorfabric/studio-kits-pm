---
cf-studio: true
type: workflow
name: cf-compete-run
description: Invoke when the user wants the whole competitive-research pipeline end to end — it asks exactly one plan-approval question first, then runs autonomously — e.g. "just run the research for <vision file>", "find and profile the competitors of <target>, end to end", "express run", "do the full competitive analysis", "cf-compete run <target or file>". The express golden path — one upfront run-plan decision (all eight request fields, capture and discovery approach, depth policy, planned artifact set), then autonomous execution of request → capture → intake → discover → per-lead follow-ups → comparison → review, with every confirmation gate auto-proceeding on its recommendation and logged; only genuinely new decisions surface. The plan gate is mandatory: execution never starts before the user approves the plan. Ends with the run report and the RESEARCH-REVIEW audit artifact. For step-by-step control use the individual guided workflows instead.
version: 1.1
purpose: Run the full competitive-research pipeline in express mode — one plan decision upfront, autonomous execution, an audited result
---

# Express Run Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Orchestration
**Role**: Competitive research analyst
**Output**: the full run's artifact set (RESEARCH-REQUEST → CANDIDATE-REGISTER → per-lead cards/profiles → COMPARISON-MATRIX → RESEARCH-REVIEW, with evidence ledger and exports)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| The whole pipeline, minimal questions | **run.md** | "just run the research for input/vision.md", `/cf-compete-run` |
| Step-by-step control over one flow | the guided workflow | "profile <company>" → **profile.md** |
| Extend a finished express run | the guided workflow the run report names | "deep dossier on <lead>" → **dossier.md** |

---

## Overview

The golden path the guided workflows compose into: everything the
pipeline would otherwise ask across its stages is asked **once**, as a
single run plan, and the pipeline then executes autonomously. Express
mode changes who answers the questions — never what gets checked:

- **Confirmation gates auto-proceed.** Inside every orchestrated
  workflow, a `**user gate — confirmation**` proceeds with its own
  option-1 recommendation, and the taken recommendation is logged to the
  run report.
- **Decision gates resolve from the plan.** A `**user gate — decision**`
  inside an orchestrated workflow is answered from the approved run plan
  (the request fields answer the request workflow; the depth policy
  answers the follow-up choice; the frame answers the comparison).
- **Unplanned decisions surface.** A decision the plan does not cover —
  a thin-evidence trade-off, a mid-run scope change, an access-boundary
  question — is asked as an exception, with the standard progress
  prefix. The plan states that zero such exceptions are expected.
- **Nothing epistemic is relaxed.** Every deterministic gate
  (`cfs validate`, `check_artifact_refs.py`, `check_evidence.py`,
  exports) runs unchanged; capture failures are recorded, never asked
  about or worked around; gated sources stay gated; the closing
  RESEARCH-REVIEW audits the whole run — the post-hoc safety net that
  makes the upfront-only questioning safe.

The user extends the result afterwards through the guided workflows the
run report names — express first, depth on demand.

## Paths

- **Orchestrated workflows**: `{workflow_request}`, `{workflow_capture}`, `{workflow_intake}`, `{workflow_discover}`, `{workflow_orient}`, `{workflow_profile}`, `{workflow_compare}`, `{workflow_review}` (and `{workflow_dossier}`, `{workflow_oss_review}`, `{workflow_mechanism}`, `{workflow_watch}` when the plan includes them)
- **Coverage reporter**: `{scripts}/check_coverage.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

5 steps → the full artifact set plus the RESEARCH-REVIEW audit.
Questions: 1 decision (Step 2: the run plan), 1 closing confirmation
(Step 5); zero expected exceptions in between. Steps 3–4 run without
questions. Announce the route before Step 1 and prefix every question
per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] An input exists: a vision/product file, a named target, or a research ask
- [ ] The host agent has a web-fetch tool when live capture is in scope (the access boundary still gates every fetch)
- [ ] `python3` is available and `{cf-studio-path}/config/artifacts.toml` is writable

---

## Steps

## Step 1: Assemble the run plan

Read the input (vision/product file, named target, or ask) and derive
every decision the guided path would ask, with a recommendation each —
no question yet:

- **Request fields** — all eight (target, decision question, scope,
  comparison frame, depth, requested output, evidence cutoff, access
  boundary); a field the input does not determine is proposed, not
  silently defaulted, and an unresolvable one stays "unspecified".
- **Capture and discovery approach** — the source classes to capture per
  subject, the corpus budget (documentation pages per subject at
  profile/dossier depth; landing-only for register-only leads), whether
  search-assisted discovery applies, and the boundary rule (public only;
  failures recorded).
- **Depth policy** — the default follow-up per register classification:
  direct candidates → standard profile (with fact ledger); adjacent and
  emerging → orientation card; leads the register routes elsewhere
  follow their next-action column.
- **Comparison** — the recommended frame (from the request scope) and
  the rule for the compared set (all leads profiled at standard depth,
  exclusions named).
- **Closing audit** — cf-compete-review always ends the run.

## Step 2: Confirm the run plan

Present the plan as one numbered proposal — request fields, capture and
discovery approach, depth policy, comparison frame, the expected
artifact set, and the question budget ("this question and one closing
confirmation; exceptions only for decisions this plan does not cover") —
with the recommended plan as option 1 (**user gate — decision**).
Adjustments amend the plan, not the mode.
**STOP — end the turn after presenting the plan.** Step 3 begins only
after the user's reply; a plan the agent drafted is not an approved
plan, and the target already appearing in the user's message does not
approve anything. Record the approval as the run log's first entry:
"Plan approved by user (turn N, option X)".
STOP WHEN the user prefers step-by-step control — route to the guided
workflows instead.

## Step 3: Execute the pipeline

Run the orchestrated workflows in order — request → capture → intake →
discover → per-lead follow-ups per the depth policy → comparison —
following each workflow's own steps, rules, and deterministic gates,
with express gate semantics:

- A `confirmation` gate inside an orchestrated workflow proceeds with
  its option-1 recommendation; log the recommendation taken (workflow,
  step, one line) to the run log.
- A `decision` gate is answered from the approved plan; log the answer
  applied.
- A decision the plan does not cover is asked as an exception with the
  progress prefix, counted against the plan's zero-exceptions statement.
- Emit each workflow's checkpoint line as it completes (artifact,
  validation verdict) so progress stays visible without questions —
  never execute more than one orchestrated workflow without emitting
  its checkpoint.
- Failures follow the capture policy: recorded in the capture log and
  the run log, never asked about, never worked around.

## Step 4: Close the loop

// turbo
Run: `python3 {scripts}/check_coverage.py <artifacts-dir> --evidence-dir competitive/evidence --companies-dir competitive/companies`
Then run `cf-compete-review` under the same express semantics. The
resulting RESEARCH-REVIEW is the run's audit artifact: conformance
verdicts, coverage of the register's next actions, findings, and the
recommended next passes.

## Step 5: Present the run report

Summarize in one message: the artifacts produced (with validation
verdicts), the decisions applied from the plan, every auto-proceeded
confirmation (the run log), recorded failures, the review's findings and
recommended next passes, and how to extend each artifact through its
guided workflow. Present next steps and wait for the user
(**user gate — confirmation**).

---

## Validation Criteria

- [ ] The run log's first entry records the user's plan approval (turn and option) — a run without it is a protocol violation, not an express run
- [ ] Exactly one decision gate before execution; every other question was either answered by the plan or logged as a counted exception
- [ ] Every orchestrated workflow's deterministic gate ran unchanged and reports PASS
- [ ] Every auto-proceeded confirmation is logged in the run report — nothing proceeded silently
- [ ] Capture failures recorded, never asked about; the access boundary was never crossed
- [ ] The closing RESEARCH-REVIEW exists and audits the run (conformance, coverage, findings)
- [ ] The run report names the guided workflow for every follow-up it recommends

---

## Next Steps

- Extend a lead → the guided workflow the run report names (`cf-compete-dossier`, `cf-compete-oss-review`, `cf-compete-mechanism`)
- Stand up monitoring → `cf-compete-watch` (baseline, then the cadence)
- Re-audit after extensions → `cf-compete-review` measures the closure

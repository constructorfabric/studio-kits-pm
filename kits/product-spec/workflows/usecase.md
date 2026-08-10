---
cf-studio: true
type: workflow
name: cf-product-spec-usecase
description: Invoke when the user wants one user goal spelled out end to end before implementation — e.g. "write the use case for <goal>", "what are the flows and acceptance criteria?", "turn this opportunity into use cases", "cf-product-spec usecase <goal>". Produces a USE-CASE artifact — actors, preconditions, main flow, alternative flows, acceptance criteria, and traceability to the OPPORTUNITY that justifies it. Never UI layout or implementation detail.
version: 1.0
purpose: Specify one user goal end to end as a USE-CASE traced to its OPPORTUNITY
---

# Write Use Case Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Authoring
**Role**: Product manager
**Output**: `{artifacts_dir}/USE-CASE/{yyyy-mm-dd}-{slug}.md`

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Spell out one user goal end to end | **usecase.md** | "write the use case for offline job packets" |
| Frame the problem first | **opportunity.md** | "why do technicians keep re-scheduling visits?" |
| Audit an existing product-spec artifact | **review.md** | "review these use cases" |

---

## Overview

Produces one USE-CASE artifact per run: one user goal, from the preconditions that
make it reachable to the acceptance criteria that prove it works. The artifact is
precise enough to hand to the SDLC chain — a PRD's requirements and a FEATURE's
test scenarios are derived from its flows.

The workflow authors the artifact per `{usecase_rules}` and reviews it against
`{usecase_checklist}`. It stays above the solution line: no screens, no layout,
no APIs or storage. Every use case cites the OPPORTUNITY that justifies it, so
the requirement chain stays traceable to evidence.

## Paths

- **Template**: `{usecase_template}`
- **Rules**: `{usecase_rules}`
- **Checklist**: `{usecase_checklist}`
- **Example**: `{usecase_example}`
- **Parent artifact**: `{artifacts_dir}/OPPORTUNITY/` (the `cpt-{system}-opp-{slug}` this use case implements)
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

7 steps → USE-CASE. Questions: 1 decision (Step 2: the single goal this use case covers), 1 confirmation (Step 7: closing). Steps 1 and 3-6 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] The parent OPPORTUNITY exists and is registered (`cfs list-ids --kind opp`); author one with `cf-product-spec-opportunity` when missing
- [ ] The actors and their entitlements are known well enough to write preconditions a system could check
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

## Step 1: Resolve the parent OPPORTUNITY

Locate the OPPORTUNITY this use case serves: `cfs list-ids --kind opp`, then
`cfs where-defined --id cpt-{system}-opp-{slug}`. Read it — the problem statement
constrains what this use case may claim to solve.
STOP WHEN no OPPORTUNITY resolves: an orphan use case is not authored here. Route
to `cf-product-spec-opportunity` and record why.

## Step 2: Scope exactly one goal

State the single user goal as a verb phrase and name its primary actor. Where the
ask bundles several goals ("download and share and sync"), present the split as
numbered options and let the user pick which goal this artifact covers
(**user gate — decision**). Each remaining goal becomes its own use case.

## Step 3: Draft the main flow, then derive the alternatives

Write the happy path first: each step names an actor and an observable outcome.
Then walk the steps and derive an Alternative Flow from every step that can fail,
be interrupted, or be denied — each stating where the flow resumes or ends. Flows
that cannot be observed from outside the system are implementation detail; leave
them out.

## Step 4: Author the USE-CASE artifact

Load `{usecase_template}` and `{usecase_example}`. Follow `{usecase_rules}`:
- Resolve the USE-CASE directory from `artifacts.toml`; set the path
  `{artifacts_dir}/USE-CASE/{yyyy-mm-dd}-{slug}.md` and register it.
- Author every required section: Actors, Preconditions, Main Flow, Alternative
  Flows, Acceptance Criteria, Traceability.
- Set the ID `cpt-{system}-usecase-{slug}`; the H1 starts with `UC: ` followed by
  the goal as a verb phrase. Verify uniqueness with `cfs list-ids --kind usecase`.
  An existing ID means refresh mode — update the registered file in place.
- Write Acceptance Criteria a QA engineer could run: each one pass/fail, covering
  the alternative flows as well as the happy path.
- Traceability cites the parent opp ID and states in one line how this goal serves
  that problem.

## Step 5: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>` and
`cfs validate-toc <artifact-file>`.
Fix and re-run until all report PASS.

## Step 6: Semantic self-review

Load `{usecase_checklist}` and review the artifact category by category
(GOAL / FLOW / ACC / TRACE, then the MUST NOT HAVE items). Report each finding
with severity, line, evidence quote, and suggested fix. Apply approved fixes,
then re-run Step 5. An open CRITICAL finding fails the review.

## Step 7: Present results

Present the use case and what it commits to: the goal, the flows, and the
acceptance criteria engineering would be held to. Name any sibling goals the
Step 2 split left unwritten. Wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Exactly one user goal; the H1 is `UC: ` plus a verb phrase
- [ ] Every Main Flow step names an actor and an observable outcome
- [ ] Every step that can fail has an Alternative Flow stating where the flow resumes or ends
- [ ] Every Acceptance Criterion is pass/fail verifiable, and the alternatives are covered too
- [ ] Traceability cites an OPPORTUNITY ID that resolves, and says how the goal serves it
- [ ] No UI layout, screen spec, or implementation detail
- [ ] `cfs validate --artifact` and `cfs validate-toc` report PASS
- [ ] Artifact registered in `artifacts.toml`; ID unique per `cfs list-ids --kind usecase`

---

## Next Steps

- Sibling goals remain → run this workflow again per goal, same parent opportunity
- The goal set is complete → promote to PRD; the PRD's requirements cite these usecase IDs
- Audit the set before handoff → `cf-product-spec-review`

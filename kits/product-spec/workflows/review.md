---
cf-studio: true
type: workflow
name: cf-product-spec-review
description: Invoke when the user wants existing product-spec artifacts audited rather than authored — e.g. "review this opportunity", "are these use cases ready for the PRD?", "check the traceability", "audit the product specs", "cf-product-spec review <path>". Audits OPPORTUNITY and USE-CASE artifacts against their kit checklists plus the traceability chain, and reports findings with severity, evidence, and suggested fixes. Authors no new artifact.
version: 1.0
purpose: Audit existing OPPORTUNITY and USE-CASE artifacts for conformance, evidence quality, and traceability
---

# Review Product Spec Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Audit
**Role**: Product manager
**Output**: a findings report in the conversation, plus approved fixes applied in place

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Audit existing product-spec artifacts | **review.md** | "are these use cases ready for the PRD?" |
| Frame a new problem | **opportunity.md** | "why do technicians keep re-scheduling visits?" |
| Write a new user goal | **usecase.md** | "write the use case for offline job packets" |

---

## Overview

Audits a set of OPPORTUNITY and USE-CASE artifacts and reports what would fail
downstream: structural violations, unsourced evidence, solution language above the
solution line, unverifiable acceptance criteria, and broken or missing traceability.

This is not a research or authoring pass. It produces findings and, where the user
approves them, applies the fixes to the reviewed artifacts. A finding is never
resolved by rewriting the artifact's claim to match weaker evidence.

## Paths

- **OPPORTUNITY checklist**: `{opportunity_checklist}`
- **OPPORTUNITY rules**: `{opportunity_rules}`
- **USE-CASE checklist**: `{usecase_checklist}`
- **USE-CASE rules**: `{usecase_rules}`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

6 steps → findings report (+ applied fixes). Questions: 1 decision (Step 1: the review scope), 1 confirmation (Step 5: which fixes to apply). Steps 2-4 and 6 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] At least one OPPORTUNITY or USE-CASE artifact exists and is registered (`cfs list-ids`)
- [ ] The reviewed files are writable, if fixes are to be applied

## Step 1: Resolve the review scope

List the candidate artifacts: `cfs list-ids --kind opp` and `cfs list-ids --kind usecase`,
resolved with `cfs where-defined`. Where the user named a path, review that path and
the artifacts it references. Where the ask is open ("audit the product specs"), present
the discovered set as numbered options — one artifact, one opportunity plus its use
cases, or everything registered (**user gate — decision**).
STOP WHEN nothing is registered: there is nothing to audit. Route to
`cf-product-spec-opportunity`.

## Step 2: Deterministic gate

// turbo
For each artifact in scope run: `cfs validate --artifact <file>` and
`cfs validate-toc <file>`.
Record each result verbatim — exit status and message. A deterministic failure is a
CRITICAL finding and is never softened by a favourable reading of the checklist.

## Step 3: Checklist review per artifact

Load the checklist matching each artifact's kind and walk it category by category —
OPPORTUNITY: PROB / EVID / USER / BIZ / DEC; USE-CASE: GOAL / FLOW / ACC / TRACE —
followed by that checklist's MUST NOT HAVE items. Record every finding as:
severity (CRITICAL / MAJOR / MINOR), file and line, the quoted evidence, the rule it
violates, and a concrete suggested fix.

Read the artifact as written. An intent the author clearly held but did not write down
is a finding, not a pass.

## Step 4: Traceability audit across the set

- Every `cpt-{system}-usecase-*` in scope resolves to an OPPORTUNITY that exists
  (`cfs where-defined --id <opp-id>`); an unresolved parent is CRITICAL.
- Every OPPORTUNITY recommending promotion is covered by at least one use case
  (`cfs where-used --id <opp-id>`); an uncovered promotion is MAJOR.
- No two artifacts in scope share an ID; a duplicate is CRITICAL.
- Every artifact in scope is registered in `artifacts.toml`; an unregistered file is MAJOR.

## Step 5: Present findings and agree the fixes

Present the findings ordered by severity, grouped by artifact, with the verbatim
deterministic-gate output. State plainly whether each artifact is ready for the PRD
handoff. Offer the fix set as numbered options — apply all, apply CRITICAL and MAJOR
only, or report only (**user gate — confirmation**).

## Step 6: Apply and re-verify

Apply the approved fixes to the artifacts in place, keeping each artifact's ID.
// turbo
Re-run `cfs toc`, `cfs validate --artifact`, and `cfs validate-toc` on every changed
file until all report PASS. Close with a one-line checkpoint: findings raised, fixes
applied, findings left open and why.

---

## Validation Criteria

- [ ] Every artifact in scope has a recorded deterministic-gate result
- [ ] Every checklist category was walked for every artifact, not sampled
- [ ] Every finding carries severity, file, line, quoted evidence, and a suggested fix
- [ ] Traceability audited in both directions: use case → opportunity, opportunity → coverage
- [ ] Applied fixes re-validated to PASS; open findings reported, not silently dropped
- [ ] No new artifact authored by this workflow

---

## Next Steps

- Findings clean → promote to PRD; the PRD cites the audited opp and usecase IDs
- Evidence findings open → refresh the opportunity with `cf-product-spec-opportunity` (same ID)
- Coverage gaps open → write the missing goals with `cf-product-spec-usecase`

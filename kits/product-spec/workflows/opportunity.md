---
cf-studio: true
type: workflow
name: cf-product-spec-opportunity
description: Invoke when the user wants to frame a product problem before any solution exists — e.g. "we keep hearing that X is broken, write it up", "frame this opportunity", "should we build something here?", "cf-product-spec opportunity <problem>". Produces an evidence-backed OPPORTUNITY artifact — problem statement, evidence, target users, business impact, and exactly one recommended next step. Never a solution design, a PRD, or an estimate.
version: 1.0
purpose: Frame one product problem as an evidence-backed OPPORTUNITY
---

# Frame Opportunity Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Authoring
**Role**: Product manager
**Output**: `{artifacts_dir}/OPPORTUNITY/{yyyy-mm-dd}-{slug}.md`

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Frame a problem before a solution exists | **opportunity.md** | "why do technicians keep re-scheduling visits?" |
| Spell out one user goal end to end | **usecase.md** | "write the use case for offline job packets" |
| Audit an existing product-spec artifact | **review.md** | "review this opportunity" |

---

## Overview

Produces one OPPORTUNITY artifact per run: the problem a product decision would
address, the evidence that it is real, who has it, what it costs the business,
and the single next step the evidence supports. The artifact is the root of the
product-spec traceability chain — later USE-CASEs and the PRD cite its
`cpt-{system}-opp-{slug}` ID.

The workflow authors the artifact per `{opportunity_rules}` and reviews it
against `{opportunity_checklist}`. It writes no solution content: screens,
architecture, and sizing start at the PRD, not here.

## Paths

- **Template**: `{opportunity_template}`
- **Rules**: `{opportunity_rules}`
- **Checklist**: `{opportunity_checklist}`
- **Example**: `{opportunity_example}`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

6 steps → OPPORTUNITY. Questions: 1 decision (Step 1: the problem and its system), 1 confirmation (Step 6: closing). Steps 2-5 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A system is registered in `{cf-studio-path}/config/artifacts.toml` (the `{system}` slug the ID carries)
- [ ] The evidence the PM already holds is reachable: analytics exports, ticket queries, research notes, interview summaries
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the problem and the system

Restate the problem in one sentence with no solution in it, and name the
`{system}` slug the ID will carry. Where the user's ask already names a feature
("add a download button"), reflect the underlying problem back and ask which one
they mean (**user gate — decision**).
STOP WHEN the user's ask cannot be restated without naming a solution — that is a
PRD request, not an opportunity.

## Step 2: Collect the evidence on hand

Read what the user supplied or pointed at: analytics figures, support-ticket
counts, interview notes, competitor observations. Record each as a candidate
evidence bullet with its source and date. Count the independent sources — two is
the checklist floor (EVID-1). Never invent a figure to fill a bullet; an unsourced
claim stays out and becomes an evidence gap instead.

## Step 3: Author the OPPORTUNITY artifact

Load `{opportunity_template}` and `{opportunity_example}`. Follow
`{opportunity_rules}`:
- Resolve the OPPORTUNITY directory from `artifacts.toml`; set the path
  `{artifacts_dir}/OPPORTUNITY/{yyyy-mm-dd}-{slug}.md` and register it.
- Author every required section: Problem Statement (solution-free), Evidence
  (each bullet sourced and dated), Target Users (primary and secondary, with
  frequency and severity), Business Impact (both "if solved" and "if ignored"),
  Recommended Next Step (exactly one action).
- Set the ID `cpt-{system}-opp-{slug}` with a problem-named kebab-case slug;
  verify uniqueness with `cfs list-ids --kind opp`. An existing ID means refresh
  mode — update the registered file in place, never a second file with the same ID.
- Leave `{placeholders}` visible where the data does not exist yet; a visible gap
  is the point, a plausible invention is a defect.

## Step 4: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>` and
`cfs validate-toc <artifact-file>`.
Fix and re-run until all report PASS.

## Step 5: Semantic self-review

Load `{opportunity_checklist}` and review the artifact category by category
(PROB / EVID / USER / BIZ / DEC, then the MUST NOT HAVE items). Report each
finding with severity, line, evidence quote, and suggested fix. Apply approved
fixes, then re-run Step 4. An open CRITICAL finding fails the review.

WHEN the evidence does not support promotion (fewer than two independent sources,
or no dated quantitative claim), set Recommended Next Step to "validate further"
and name how — never "promote to PRD".

## Step 6: Present results

Present the opportunity and the decision it enables: the problem, what the
evidence does and does not establish, and the single recommended next step. Wait
for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Problem Statement names no solution, feature, or screen
- [ ] At least two independent evidence sources, each with a source and a date
- [ ] Target Users states frequency and severity for the primary segment
- [ ] Business Impact states both the value if solved and the cost if ignored
- [ ] Recommended Next Step is exactly one action, and is "validate further" whenever evidence is thin
- [ ] `cfs validate --artifact` and `cfs validate-toc` report PASS
- [ ] Artifact registered in `artifacts.toml`; ID unique per `cfs list-ids --kind opp`

---

## Next Steps

- Problem is real and framed → `cf-product-spec-usecase` writes the user goals it implies
- Evidence is thin → gather the named evidence, then refresh this artifact (same opp ID)
- Ready for solution work → promote to PRD; the PRD cites this `cpt-{system}-opp-{slug}`
- Audit an existing set → `cf-product-spec-review`

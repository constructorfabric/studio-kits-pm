---
name: cf
description: "Invoke when the user works the pre-PRD product layer — frame a product problem with evidence before any solution exists, spell out one user goal end to end with flows and acceptance criteria, or audit existing product specs for conformance and traceability before the PRD handoff. Kit `product-spec` extensions — artifacts: OPPORTUNITY, USE-CASE; workflows: opportunity, usecase, review."
---

# Constructor Studio Skill — Kit `product-spec`

Kit `product-spec` skill extensions: the evidence-first product layer that sits
**before** the PRD.

## Pipeline

```
a problem someone keeps reporting
  → cf-product-spec-opportunity → OPPORTUNITY (evidence, users, impact, one next step; no solution)
one framed problem
  → cf-product-spec-usecase → USE-CASE (actors, preconditions, flows, acceptance criteria; cites the opportunity)
the authored set
  → cf-product-spec-review → findings report (conformance + traceability audit; the quality loop)
a reviewed set
  → PRD (SDLC chain) — requirements cite the usecase and opp IDs
```

The OPPORTUNITY is the root of the traceability chain: every use case, and later
every PRD requirement, cites the `cpt-{system}-opp-{slug}` that justifies it. A
requirement whose chain does not reach an opportunity has no recorded evidence
behind it.

## Workflows

| Skill | Type | Workflow | Output |
|-------|------|----------|--------|
| `cf-product-spec-opportunity` | authoring | `{workflow_opportunity}` | OPPORTUNITY artifact |
| `cf-product-spec-usecase` | authoring | `{workflow_usecase}` | USE-CASE artifact |
| `cf-product-spec-review` | audit | `{workflow_review}` | findings report + approved fixes applied in place |

## Progress protocol

Every workflow run follows one interaction contract, so the user always knows
where they are, how many questions remain, and what a bare "1" means:

1. **Route first.** On entering a workflow, before Step 1, announce its
   `## Route` block: the step count, the questions ahead with their types, and
   the artifact(s) the run will produce.
2. **Position with every question.** Prefix every user gate with
   `[cf-product-spec-<name> · step k/N · questions left: M]`.
3. **Numbered options, recommendation first.** Every gate presents numbered
   options; option 1 is always the workflow's recommendation, so "1" always
   means "proceed as recommended".
4. **Two gate types.**
   - `**user gate — decision**`: the answer shapes the artifact itself (which
     problem, which single goal, which review scope). Wait for an explicit
     answer.
   - `**user gate — confirmation**`: the workflow has derived a concrete
     recommendation; state it as option 1 and proceed with it on a bare
     confirmation.
5. **Recovery never asks.** A missing file or failed validator is fixed (or
   honestly recorded as a failure) per the rules' ON_ERROR paths and reported at
   the next gate or checkpoint — never surfaced as a question of its own.
6. **Checkpoint at phase end.** After the deterministic gate and the semantic
   review, emit a one-line checkpoint: what was produced and validated, what
   comes next.

## Routing

ALWAYS route to `cf-product-spec-opportunity` WHEN intent matches:
"we keep hearing that <X> is broken, write it up", "frame this opportunity",
"should we build something here?", "why do users keep <doing the workaround>?",
"cf-product-spec opportunity <problem>" — frames one problem with dated,
sourced evidence and exactly one recommended next step. No solution content.

ALWAYS route to `cf-product-spec-usecase` WHEN intent matches:
"write the use case for <goal>", "what are the flows and acceptance criteria?",
"turn this opportunity into use cases", "cf-product-spec usecase <goal>" —
specifies exactly one user goal end to end and cites the opportunity it serves.

ALWAYS route to `cf-product-spec-review` WHEN intent matches:
"review this opportunity", "are these use cases ready for the PRD?", "check the
traceability", "audit the product specs", "cf-product-spec review <path>" —
audits the artifact set against the kit checklists and the traceability chain.
Never an authoring pass.

ALWAYS run `cf-product-spec-opportunity` BEFORE authoring a USE-CASE WHEN no
OPPORTUNITY is registered for the problem (check with `cfs list-ids --kind opp`).

ALWAYS keep the solution line: an OPPORTUNITY names no feature, screen, or
architecture, and a USE-CASE names no UI layout or implementation detail. Both
belong to the PRD and below.

NEVER invent a figure, a percentage, or a source to fill an evidence bullet — a
visible `{placeholder}` or a recorded evidence gap is the correct output.

When routed to a workflow:
1. Read the matched workflow file and follow its steps in order.
2. Announce the workflow's `## Route` block before Step 1 and follow the
   progress protocol above for every question and checkpoint.
3. Each workflow binds the artifact KIND references (rules, template, checklist,
   example) and drives the author → deterministic-gate → semantic-review loop.

## Artifact kinds

| Kind | ID kinds | References |
|------|----------|------------|
| OPPORTUNITY | `opp` | `{opportunity_rules}`, `{opportunity_template}`, `{opportunity_checklist}`, `{opportunity_example}` |
| USE-CASE | `usecase` | `{usecase_rules}`, `{usecase_template}`, `{usecase_checklist}`, `{usecase_example}` |

## Commands

- `cfs validate --artifact <file>` — deterministic structure/ID validation
- `cfs toc <file>` / `cfs validate-toc <file>` — table-of-contents generation and check
- `cfs list-ids --kind opp` / `cfs list-ids --kind usecase` — list defined `cpt-*` identifiers
- `cfs where-defined --id <id>` — locate the artifact that defines an identifier
- `cfs where-used --id <id>` — find the use cases and PRDs built on an opportunity

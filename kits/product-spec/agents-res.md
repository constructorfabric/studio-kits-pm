# Constructor Studio Kit: Product Spec (`product-spec`)

Agent quick reference.

## What it is

The pre-PRD product layer. A problem someone keeps reporting is recorded as an
evidence-backed OPPORTUNITY (problem, dated evidence, target users, business
impact, exactly one recommended next step), and each user goal that problem
implies is specified as a USE-CASE (actors, preconditions, main flow,
alternative flows, acceptance criteria) that cites the opportunity. Downstream,
a PRD's requirements cite those IDs, so every requirement traces back to
evidence rather than to an unattributed idea.

## Artifact kinds

| Kind | Semantic intent (when to use) | References |
| --- | --- | --- |
| OPPORTUNITY | One product problem framed before any solution exists: what is wrong, the dated evidence that it is real, who has it, what it costs, and the single next step the evidence supports. | `{opportunity_rules}`, `{opportunity_template}`, `{opportunity_checklist}`, `{opportunity_example}` |
| USE-CASE | Exactly one user goal end to end: actors, preconditions, main flow, alternative flows, pass/fail acceptance criteria, and traceability to the opportunity it serves. | `{usecase_rules}`, `{usecase_template}`, `{usecase_checklist}`, `{usecase_example}` |

## Workflows

| Skill | Purpose |
| --- | --- |
| `cf-product-spec-opportunity` | Frame one product problem as an evidence-backed OPPORTUNITY — the root of the traceability chain. |
| `cf-product-spec-usecase` | Specify one user goal end to end as a USE-CASE traced to its OPPORTUNITY. |
| `cf-product-spec-review` | Audit existing OPPORTUNITY and USE-CASE artifacts for conformance, evidence quality, and traceability; authors nothing. |

## Rules

- ALWAYS record the OPPORTUNITY before authoring a USE-CASE for a problem (check `cfs list-ids --kind opp` for an existing one).
- NEVER name a feature, screen, or architecture in an OPPORTUNITY, and never name UI layout or implementation detail in a USE-CASE — both belong to the PRD and below.
- NEVER invent a figure, percentage, or source to fill an evidence bullet; leave a visible `{placeholder}` or record the evidence gap.
- ALWAYS give every evidence bullet a named source and a date, and require at least two independent sources before recommending promotion to PRD.
- ALWAYS set the Recommended Next Step to "validate further" — naming how — whenever the evidence is thin; never "promote to PRD".
- ALWAYS scope a USE-CASE to exactly one user goal; a bundled ask splits into one artifact per goal.
- ALWAYS derive an Alternative Flow from every main-flow step that can fail, be interrupted, or be denied, each stating where the flow resumes or ends.
- ALWAYS write Acceptance Criteria a QA engineer could run pass/fail, covering the alternative flows as well as the happy path.
- ALWAYS cite a resolving OPPORTUNITY ID in a USE-CASE's Traceability section; an orphan use case is not authored.
- ALWAYS refresh an existing artifact in place under its existing ID — never a second file carrying the same ID.
- ALWAYS finish artifact work with `cfs validate --artifact <path>` and `cfs validate-toc <path>`.
- ALWAYS announce a workflow's `## Route` block before its Step 1 and prefix every question with `[cf-product-spec-<name> · step k/N · questions left: M]` — the user must always know their position and how many questions remain.
- ALWAYS present every user gate as numbered options with the recommendation as option 1; a `confirmation` gate proceeds with option 1 on a bare confirmation, a `decision` gate waits for an explicit answer.
- NEVER turn an environment or validator failure into a question — fix it (or record it honestly) per the rules' ON_ERROR paths and report at the next gate or checkpoint.

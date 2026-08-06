# USE-CASE Rules

**Artifact**: USE-CASE
**Kit**: product-spec

**Dependencies** (lazy-loaded):
- `{usecase_template}` — structural reference (load WHEN validating structure)
- `{usecase_checklist}` — semantic quality criteria (load WHEN checking semantic quality)
- `{usecase_example}` — reference implementation (load WHEN needing content reference)

## Requirements

### Structural

- MUST follow the heading outline from the template: Actors, Preconditions, Main Flow,
  Alternative Flows, Acceptance Criteria, Traceability — all H2, all required.
- MUST declare exactly one ID matching `cpt-{system}-usecase-{slug}` directly under the H1.
- H1 title MUST start with `UC: ` followed by a verb phrase (the user's goal).

### Semantic

- One use case = one user goal. If the Main Flow serves two goals, split it.
- Every Main Flow step MUST name an actor and an observable outcome.
- Every Alternative Flow MUST state where the flow resumes or ends.
- Acceptance Criteria MUST be pass/fail verifiable — a QA engineer could test each one.
- Traceability MUST reference at least one existing OPPORTUNITY ID.

### Deliberate Omissions (MUST NOT HAVE)

- No UI layout or visual design — screens come later in the design pipeline.
- No implementation detail (APIs, storage, frameworks).

## Tasks

### Phase 1: Setup
1. Copy the template; confirm the parent OPPORTUNITY ID exists
   (`cfs where-defined --id cpt-{system}-opp-{slug}`).

### Phase 2: Content Creation
1. Write the Main Flow first; derive Alternative Flows from each step that can fail.

### Phase 3: IDs and Structure
1. Mint the ID; check uniqueness with `cfs list-ids --kind usecase`.

### Phase 4: Quality Check
1. Run structural validation: `cfs validate --artifact <file>`.
2. Run the semantic review against `{usecase_checklist}`.

## Validation

### Phase 1: Structural Validation (Deterministic)
Run `cfs validate --artifact <file>`. All required headings present, ID format correct,
OPPORTUNITY reference resolvable.

### Phase 2: Semantic Validation (Checklist-based)
Walk `{usecase_checklist}` category by category. Report findings with severity, line,
evidence quote, and suggested fix.

## Error Handling

### Orphan Use Case
If no OPPORTUNITY exists to reference, stop: write the OPPORTUNITY first. Use cases
without an evidence-backed parent are not promoted.

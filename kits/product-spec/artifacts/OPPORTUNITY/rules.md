# OPPORTUNITY Rules

**Artifact**: OPPORTUNITY
**Kit**: product-spec

**Dependencies** (lazy-loaded):
- `{opportunity_template}` — structural reference (load WHEN validating structure)
- `{opportunity_checklist}` — semantic quality criteria (load WHEN checking semantic quality)
- `{opportunity_example}` — reference implementation (load WHEN needing content reference)

## Requirements

### Structural

- MUST follow the heading outline from the template: Problem Statement, Evidence,
  Target Users, Business Impact, Recommended Next Step — all H2, all required.
- MUST declare exactly one ID matching `cpt-{system}-opp-{slug}` directly under the H1 title.
- Slug MUST be kebab-case and name the problem, not a solution
  (`offline-access-gap`, not `add-download-button`).

### Semantic

- Problem Statement MUST be solution-free. If it names a feature, rewrite it.
- Every Evidence bullet MUST carry a source (link, system, or study) and a date.
- Business Impact MUST state both directions: value if solved AND cost if ignored.
- Recommended Next Step MUST be exactly one action, not a menu.

### Deliberate Omissions (MUST NOT HAVE)

- No solution designs, screens, or architecture — that starts at the PRD.
- No effort estimates — sizing happens after promotion.

## Tasks

### Phase 1: Setup
1. Copy the template; pick `{system}` and a problem-named slug.

### Phase 2: Content Creation
1. Fill each section top to bottom; leave `{placeholders}` visible where data is missing.

### Phase 3: IDs and Structure
1. Mint the ID; check uniqueness with `cfs list-ids --kind opp`.

### Phase 4: Quality Check
1. Run structural validation: `cfs validate --artifact <file>`.
2. Run the semantic review against `{opportunity_checklist}`.

## Validation

### Phase 1: Structural Validation (Deterministic)
Run `cfs validate --artifact <file>`. All required headings present, ID format correct.

### Phase 2: Semantic Validation (Checklist-based)
Walk `{opportunity_checklist}` category by category. Report findings with severity,
line, evidence quote, and suggested fix.

## Error Handling

### Missing Evidence
If no evidence exists yet, the Recommended Next Step MUST be "validate further" —
an OPPORTUNITY without evidence cannot be promoted to PRD.

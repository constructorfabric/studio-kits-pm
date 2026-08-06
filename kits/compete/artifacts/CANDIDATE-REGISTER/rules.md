# CANDIDATE-REGISTER Rules

**Artifact**: CANDIDATE-REGISTER
**Kit**: compete

```pdsl
UNIT RegisterAuthoring

PURPOSE:
  Author one CANDIDATE-REGISTER artifact: a source-backed list of possible
  direct, adjacent, or emerging competitors for an approved research request.
  A register records leads and routing, never feature coverage or rank.

WHEN:
  - REQUIRE building or refreshing a candidate register for a registered RESEARCH-REQUEST

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the CANDIDATE-REGISTER directory
  - SET default path {artifacts_dir}/CANDIDATE-REGISTER/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {candidate_register_template} for structure
  - LOAD {candidate_register_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 6
  - RUN author Section 1 (Scope Statement): open with what the register is NOT, then the searched candidate space and inclusion conditions from the request
  - RUN author Section 2 (Evidence Scope): cutoff, access boundary, depth, completeness — inherited from the request unless the run narrowed them
  - RUN author Section 3 (Candidates): one row per candidate with classification (baseline | direct | adjacent | emerging, plus a relationship descriptor), aliases when known, the screening question that puts it in scope, at least one resolvable evidence reference, and a concrete next research action
  - RUN author Section 4 (Boundary) and Section 5 (Original Files)
  - SET ID cpt-{system}-reg-{slug} for the register
  - RUN verify ID uniqueness with cfs list-ids; when the ID already exists, this run is a refresh — update the registered artifact file in place (same ID, same registry entry, refreshed date frontmatter), never a second file with the same ID
  - RUN append the back-link "`cpt-{system}-reg-{slug}` — {register title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when one or more lines for this ID already exist, collapse them into a single line updated in place (other artifacts' lines stay untouched) — a refresh never appends a duplicate and always repairs duplicates left by earlier runs, and a stale no-derived-artifacts line is removed whenever any back-link is present
  - LOAD {candidate_register_checklist} for self-review of semantic quality

RULES:
  - ALWAYS follow {candidate_register_template} structure with required frontmatter
  - ALWAYS classify every candidate as baseline, direct, adjacent, or emerging; the baseline classification is reserved for the request's own target
  - ALWAYS give every candidate row at least one evidence reference that resolves in competitive/evidence/index.tsv or a company fact ledger
  - ALWAYS make the next action a concrete, routable step (which flow, which question) rather than "research further"
  - ALWAYS keep lead status distinct from confirmed-competitor status in every sentence
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {candidate_register_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {candidate_register_checklist} semantic criteria in this file
```

```pdsl
UNIT RegisterOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-REG-NO-001 (CRITICAL): feature scores, coverage percentages, parity conclusions, or any ranking of candidates
  - NEVER CPT-REG-NO-002 (CRITICAL): "confirmed competitor" language — a register records leads and the reason each is worth examining
  - NEVER CPT-REG-NO-003 (CRITICAL): a candidate row without a resolvable evidence reference
  - NEVER CPT-REG-NO-004 (HIGH): absence claims ("lacks", "does not have") derived from missing public evidence — record what remains unverified instead
  - NEVER CPT-REG-NO-005 (HIGH): a company profile, pricing benchmark, or product decision embedded in the register
  - NEVER CPT-REG-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT RegisterValidate

PURPOSE:
  Validate the CANDIDATE-REGISTER deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS
  - RUN python3 {scripts}/render_views.py <path> --format csv,html to refresh the exports
  - LOAD {candidate_register_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {candidate_register_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered csv/html exports; they are regenerated from the artifact
```

```pdsl
UNIT RegisterErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  unresolved_evidence ->
    EMIT "Candidate {name} cites {ref}, which does not resolve in the evidence index"
    RUN route to cf-compete-intake to index the missing source, or drop the citation

  zero_candidates ->
    EMIT "No candidates could be evidenced within the request scope"
    RUN record the empty result honestly: author the register with an empty table and a completeness note — an empty register is a valid discovery outcome

RULES:
  - ALWAYS ask the user when a candidate's classification is ambiguous between adjacent and emerging
```

```pdsl
UNIT RegisterNextSteps

PURPOSE:
  Offer next actions based on register state.

DO:
  - EMIT "Per-candidate next actions are routing: profile-worthy leads -> cf-compete-profile (arrives with the COMPANY-PROFILE kind)"
  - EMIT "New evidence drop -> cf-compete-intake, then refresh this register"
  - EMIT "Register refreshed -> keep the same reg ID; the request back-link stays valid"
```

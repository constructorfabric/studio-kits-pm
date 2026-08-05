# COMPARISON-MATRIX Rules

**Artifact**: COMPARISON-MATRIX
**Kit**: compete

```pdsl
UNIT MatrixAuthoring

PURPOSE:
  Author one COMPARISON-MATRIX artifact: selected companies compared under
  exactly one frame, every cell carrying its mechanism, status,
  availability, observation date, boundary, and evidence. A matrix answers
  the frame's question; it never produces a winner/loser score, a ranking,
  or an unsupported parity claim.

WHEN:
  - REQUIRE comparing selected companies for a registered RESEARCH-REQUEST with an agreed frame

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the COMPARISON-MATRIX directory
  - SET default path {artifacts_dir}/COMPARISON-MATRIX/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {comparison_matrix_template} for structure
  - LOAD {comparison_matrix_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 8
  - RUN fix exactly one frame from the request (role × stage/job taxonomy, product outcome frame, or a named mechanism lens); frames may be mapped explicitly, never silently mixed
  - RUN confirm the compared set: each company evidenced at the depth the frame needs (profile or dossier); record what backs each column in Section 8
  - RUN resolve the frame's FEATURE-TAXONOMY with cfs list-ids and declare it in the frontmatter taxonomy: key; matrix rows are its feature labels (detail after a colon), every row covered for every compared company; proceed without one only on the user's explicit say-so
  - RUN author Section 1 (Comparison Frame): the not-question, the question, the compared set, and the named exclusions — every register direct candidate absent from the matrix carries a reason (under-evidenced, out of frame, deferred)
  - RUN author Section 2 (Evidence Scope): cutoff, access boundary, completeness (which cells could not be assessed)
  - RUN author Section 3 (Matrix): one row per company × feature/mechanism with status exactly one of substantial | partial | not_observed | not_comparable, availability exactly one of current | planned | vision, an ISO observed_on date, a documented-boundary cell, and at least one evidence reference
  - RUN author Section 4 (Studio Position) WHEN Studio is among the compared: Studio today and Studio vision as separate rows or labels, never merged; omit the section otherwise
  - RUN author Section 5 (Readable Conclusion) including the negative findings, Section 6 (Boundary), and Section 7 (Original Files)
  - SET ID cpt-{system}-cmp-{slug} for the matrix
  - RUN verify ID uniqueness with cfs list-ids
  - RUN append the back-link "`cpt-{system}-cmp-{slug}` — {matrix title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when a line for this ID already exists, update it in place — a refresh never appends a duplicate
  - LOAD {comparison_matrix_checklist} for self-review of semantic quality

RULES:
  - ALWAYS follow {comparison_matrix_template} structure with required frontmatter
  - ALWAYS keep exactly one frame per matrix; a second lens is a second matrix
  - ALWAYS take row labels from the declared taxonomy and cover every taxonomy row for every compared company — a missing cell is not_observed, never a dropped row
  - NEVER invent a matrix row absent from the declared taxonomy; widen the taxonomy first (cf-compete-taxonomy), then the matrix
  - ALWAYS normalize feature/mechanism labels across vendors after reviewing all compared documentation — domain-standard wording, not one vendor's label
  - ALWAYS record a cell you could not assess as not_observed (no retained evidence) or not_comparable (the frame does not apply), with the reason in the boundary cell
  - ALWAYS date every cell: status and availability hold at the observed_on date only
  - ALWAYS keep Studio today separate from Studio vision; a vision row is a product hypothesis, not delivered capability
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {comparison_matrix_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {comparison_matrix_checklist} semantic criteria in this file
```

```pdsl
UNIT MatrixOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-CMP-NO-001 (CRITICAL): winner/loser scores, rankings, weighted totals, or a "best product" conclusion
  - NEVER CPT-CMP-NO-002 (CRITICAL): not_observed rendered as feature absence, in a cell or in the conclusion
  - NEVER CPT-CMP-NO-003 (CRITICAL): Studio vision merged with, or scored as, delivered capability
  - NEVER CPT-CMP-NO-004 (HIGH): two frames silently mixed in one matrix
  - NEVER CPT-CMP-NO-005 (HIGH): cross-product numbers compared as accuracy or quality (different products' published metrics are not commensurable)
  - NEVER CPT-CMP-NO-006 (HIGH): a product decision, requirement, or commitment stated as an outcome of the matrix
  - NEVER CPT-CMP-NO-007 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT MatrixValidate

PURPOSE:
  Validate the COMPARISON-MATRIX deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --artifacts-dir <artifacts-dir> --lint-language — must report PASS (enforces the status/availability/date vocabularies per row, rows ⊆ declared taxonomy, and every-row-covered)
  - RUN python3 {scripts}/render_matrix_deck.py <matrix files…> --evidence-dir competitive/evidence --mode tabs (and --mode heatmap) to refresh the deck views when several matrices exist
  - RUN python3 {scripts}/render_views.py <path> --format csv,html to refresh the exports
  - LOAD {comparison_matrix_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {comparison_matrix_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered csv/html exports; they are regenerated from the artifact
```

```pdsl
UNIT MatrixErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  no_frame ->
    EMIT "The request states no comparison frame"
    RUN present candidate frames derived from the request's scope and WAIT for the user's choice; record the chosen frame in the request first

  underevidenced_company ->
    EMIT "{company} has no profile/dossier or indexed evidence at comparison depth"
    RUN offer: drop the column, run cf-compete-profile first, or keep it with all cells not_observed

  frame_mismatch ->
    EMIT "Requested cells fall outside the agreed frame: {examples}"
    RUN keep the matrix single-frame; propose a second matrix for the second lens

RULES:
  - ALWAYS ask the user when the compared set or the frame is ambiguous
```

```pdsl
UNIT MatrixNextSteps

PURPOSE:
  Offer next actions based on matrix state.

DO:
  - EMIT "Cells not_observed that matter -> commission deeper evidence (dossier, hands-on request) and refresh"
  - EMIT "A second lens is wanted -> a second single-frame matrix over the same companies"
  - EMIT "A proposed action from the conclusion -> record it as a product hypothesis for human decision, outside this kit"
```

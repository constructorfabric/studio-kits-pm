# COMPANY-DOSSIER Rules

**Artifact**: COMPANY-DOSSIER
**Kit**: compete

```pdsl
UNIT DossierAuthoring

PURPOSE:
  Author one COMPANY-DOSSIER artifact: the standard profile expanded with
  retained evidence for a request that may affect buy/build, positioning,
  or product direction. A dossier widens the examined source surface and
  records, area by area, what the sources document and what remains
  unestablished. Missing public evidence is never treated as absence.

WHEN:
  - REQUIRE building or refreshing a deep company dossier for a registered RESEARCH-REQUEST

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the COMPANY-DOSSIER directory
  - SET default path {artifacts_dir}/COMPANY-DOSSIER/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {company_dossier_template} for structure
  - LOAD {company_dossier_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 9
  - RUN resolve the subject's COMPANY-PROFILE when one exists; a dossier expands it, but may be commissioned directly — record either way in Sections 8 and 9
  - RUN inventory the retained evidence for the subject: extracts, fact ledger, and the source classes covered (landing, docs, release notes, integrations, security/governance, pricing, case studies, finance/adoption) — the uncovered classes become the completeness note
  - RUN author Section 1 (Evidence Scope): source count, access dates, the vendor-described-boundary statement, cutoff, access boundary, completeness
  - RUN author Section 2 (Product Surface) grounded in the retained sources
  - RUN author Section 3 (Capability Graph): offering -> capability -> documented features/mechanisms, one evidence reference per row
  - RUN author Section 4 (Documented Mechanics): one row per area with the documented public surface (evidenced) and the mandatory what-remains-unestablished cell
  - RUN author Section 5 (Source Availability): one row per source class with availability exactly one of public | gated | unavailable | planned | preview, evidenced
  - RUN author Section 6 (Users, Availability, and Commercial Boundary) and Section 7 (Dossier Conclusion) — the conclusion must state what the subject is credible for AND close with the evidence-limits-not-absence-claims sentence
  - RUN author Section 8 (Original Files)
  - SET ID cpt-{system}-dos-{slug} for the dossier
  - RUN verify ID uniqueness with cfs list-ids; when the ID already exists, this run is a refresh — update the registered artifact file in place (same ID, same registry entry, refreshed date frontmatter), never a second file with the same ID
  - RUN append the back-link "`cpt-{system}-dos-{slug}` — {dossier title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when one or more lines for this ID already exist, collapse them into a single line updated in place (other artifacts' lines stay untouched) — a refresh never appends a duplicate and always repairs duplicates left by earlier runs, and a stale no-derived-artifacts line is removed whenever any back-link is present
  - LOAD {company_dossier_checklist} for self-review of semantic quality

RULES:
  - ALWAYS follow {company_dossier_template} structure with required frontmatter
  - ALWAYS keep the per-area negative space: every Documented Mechanics row states what remains unestablished, phrased as evidence limits
  - ALWAYS record source availability per class with the exact vocabulary; do not equate public documentation availability with feature availability
  - ALWAYS give the standard classes — documentation, pricing, finance/adoption at minimum — a Source Availability row even when nothing was captured (record it unavailable; grouped rows are fine)
  - ALWAYS extend the company fact ledger with the newly observed time-sensitive facts this dossier cites; on the direct-dossier path with no ledger, create and register one (intake) before the first time-sensitive fact is cited
  - ALWAYS distinguish observed facts, vendor claims, and third-party estimates in the wording, matching fact-ledger claim_status labels where a ledger exists
  - ALWAYS stay inside the request's access boundary; a gated or unavailable source is recorded as such, never summarized from memory
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {company_dossier_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {company_dossier_checklist} semantic criteria in this file
```

```pdsl
UNIT DossierOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-DOS-NO-001 (CRITICAL): absence claims ("lacks", "does not have") derived from missing public evidence — the unestablished cell records the limit instead
  - NEVER CPT-DOS-NO-002 (CRITICAL): an inferred executed workflow, customer outcome, or runtime behaviour that no retained source documents
  - NEVER CPT-DOS-NO-003 (CRITICAL): a vendor claim or third-party estimate presented as an observed fact
  - NEVER CPT-DOS-NO-004 (HIGH): treating vendor documentation claims as independently validated
  - NEVER CPT-DOS-NO-005 (HIGH): buy/build recommendations, rankings, or product decisions — the dossier informs them, it does not make them
  - NEVER CPT-DOS-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT DossierValidate

PURPOSE:
  Validate the COMPANY-DOSSIER deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS
  - RUN python3 {scripts}/render_views.py <path> --format html to refresh the export
  - LOAD {company_dossier_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {company_dossier_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered html export; it is regenerated from the artifact
```

```pdsl
UNIT DossierErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  thin_evidence ->
    EMIT "Only {N} retained source(s) found for {company} — a dossier over a thin set mostly records limitations"
    RUN present the inventory and ask whether to proceed, intake more evidence first, or produce a standard profile instead

  unresolved_evidence ->
    EMIT "The dossier cites {ref}, which does not resolve in the evidence index"
    RUN route to cf-compete-intake to index the missing source, or drop the citation

  gated_source ->
    EMIT "Source {locator} is gated or unavailable within the access boundary"
    RUN record it in Source Availability with the correct class; do not summarize it from memory

RULES:
  - ALWAYS ask the user when the dossier subject spans multiple offerings whether to cover the platform or one offering
```

```pdsl
UNIT DossierNextSteps

PURPOSE:
  Offer next actions based on dossier state.

DO:
  - EMIT "Dossier ready -> a single-frame comparison against other profiled companies (arrives with the COMPARISON-MATRIX kind)"
  - EMIT "Unestablished areas that matter -> commission a narrower request (hands-on evaluation, gated-source access) and re-run"
  - EMIT "New evidence drop -> cf-compete-intake, then refresh this dossier (same dos ID)"
```

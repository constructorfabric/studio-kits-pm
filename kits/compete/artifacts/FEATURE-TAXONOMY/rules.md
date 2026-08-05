# FEATURE-TAXONOMY Rules

**Artifact**: FEATURE-TAXONOMY
**Kit**: compete

```pdsl
UNIT TaxonomyAuthoring

PURPOSE:
  Author one FEATURE-TAXONOMY artifact: the normalization contract a
  comparison frame's matrices compare against — union-derived rows with
  definitions and inclusion criteria, per-vendor alias mappings, and the
  provenance audit that proves no vendor's feature list anchored the set.

WHEN:
  - REQUIRE normalizing comparison rows for a registered RESEARCH-REQUEST's frame

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the FEATURE-TAXONOMY directory
  - SET default path {artifacts_dir}/FEATURE-TAXONOMY/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {feature_taxonomy_template} for structure
  - LOAD {feature_taxonomy_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 8
  - RUN python3 {scripts}/mine_terms.py --evidence-dir competitive/evidence and retain the harvest report — the deterministic seed for normalization
  - RUN mine every compared vendor's corpus independently into a candidate feature inventory before fixing any row
  - RUN build the row set as the union of all inventories plus the requester's role/stage frames; normalize labels to domain-standard wording — never one vendor's term
  - RUN author Section 3 (Feature Rows): 8–20 rows per frame (state the reason when outside the band), each with a crisp definition, an inclusion criterion two analysts would apply identically, and the evidence that first established it
  - RUN author Section 4 (Vendor Aliases): one row per (feature, vendor) pair with the vendor's verbatim term and its evidence
  - RUN author Section 5 (Union Provenance): every compared vendor listed with the rows its corpus first established, or the explicit "no rows beyond the union" line
  - RUN author Section 6 (Boundary) and Section 7 (Original Files)
  - SET ID cpt-{system}-tax-{slug}; verify uniqueness with cfs list-ids
  - RUN append the back-link "`cpt-{system}-tax-{slug}` — {taxonomy title}" to the commissioning request's Traceability section, replacing its default no-derived-artifacts line when present
  - LOAD {feature_taxonomy_checklist} for self-review of semantic quality

RULES:
  - ALWAYS mine every compared vendor's corpus before fixing the row set — the union comes first, rows second
  - ALWAYS keep a row whose evidence exists in only one vendor's corpus — sparse rows are the point, not noise
  - ALWAYS give every row an inclusion criterion concrete enough that two analysts would fill the same matrix cell
  - ALWAYS record the vendor's own wording verbatim in the alias map, with evidence
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {feature_taxonomy_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {feature_taxonomy_checklist} semantic criteria in this file
```

```pdsl
UNIT TaxonomyOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-TAX-NO-001 (CRITICAL): a row set derived from a subset of the compared vendors — the anchor bias this kind exists to prevent; every vendor's inventory enters the union before rows are fixed
  - NEVER CPT-TAX-NO-002 (CRITICAL): a candidate row dropped because the first-mined vendors carry no evidence for it
  - NEVER CPT-TAX-NO-003 (CRITICAL): row inclusion presented as a capability or availability claim — cells belong to matrices, not the taxonomy
  - NEVER CPT-TAX-NO-004 (HIGH): an alias mapping without evidence of the vendor using the term
  - NEVER CPT-TAX-NO-005 (HIGH): a row set outside 8–20 rows with no stated reason
  - NEVER CPT-TAX-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT TaxonomyValidate

PURPOSE:
  Validate the FEATURE-TAXONOMY deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS (enforces the per-row evidence duty and the cardinality band)
  - RUN python3 {scripts}/mine_terms.py --evidence-dir competitive/evidence --taxonomy <path> — the coverage report: rows and aliases without corpus hits become mining or capture targets
  - RUN python3 {scripts}/render_views.py <path> --format csv,html to refresh the exports
  - LOAD {feature_taxonomy_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {feature_taxonomy_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered csv/html exports; they are regenerated from the artifact
```

```pdsl
UNIT TaxonomyErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  corpus_missing ->
    EMIT "Vendor {vendor} carries no mined corpus — its inventory cannot enter the union"
    RUN route the vendor's docs to cf-compete-capture first, or record the vendor in completeness as unmined; never fix the row set while a compared vendor is unmined without saying so

  synonym_conflict ->
    EMIT "Vendors use the same term for different mechanisms: {term}"
    RUN split into distinct rows with disambiguating definitions; record both aliases

  row_band_exceeded ->
    EMIT "The union yields {n} rows — outside the 8–20 band"
    RUN group rows into sub-frames or state the reason in Section 3; never silently drop union rows

RULES:
  - ALWAYS ask the user before removing a union-derived row for any reason
```

```pdsl
UNIT TaxonomyNextSteps

PURPOSE:
  Offer next actions based on taxonomy state.

DO:
  - EMIT "Taxonomy fixed -> cf-compete-compare builds matrices against its rows (cells decided per vendor evidence)"
  - EMIT "Coverage report shows unmined rows/vendors -> cf-compete-capture the missing corpora, then refresh this taxonomy (same tax ID)"
  - EMIT "Frame changed -> revise the RESEARCH-REQUEST first, then re-derive the union"
```

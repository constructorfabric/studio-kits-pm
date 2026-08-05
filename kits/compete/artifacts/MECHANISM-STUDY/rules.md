# MECHANISM-STUDY Rules

**Artifact**: MECHANISM-STUDY
**Kit**: compete

```pdsl
UNIT MechanismAuthoring

PURPOSE:
  Author one MECHANISM-STUDY artifact for a narrow question: a map of
  documented mechanisms — their inputs, observed operation, output/review
  behaviour, closest analogues, and evidence boundaries. Rows are
  mechanisms, not companies; the study surfaces whitespace, it never ranks.

WHEN:
  - REQUIRE studying one mechanism or product gap for a registered RESEARCH-REQUEST

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the MECHANISM-STUDY directory
  - SET default path {artifacts_dir}/MECHANISM-STUDY/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {mechanism_study_template} for structure
  - LOAD {mechanism_study_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 8
  - RUN read the indexed evidence for the offerings in scope; collect candidate mechanisms and separate direct mechanisms from adjacent features per the request's question
  - RUN normalize mechanism names across vendors after reviewing all the evidence — domain-standard wording, never one vendor's label
  - RUN author Section 1 (Study Scope): the not-a-ranking statement, the narrow question, and the direct-vs-adjacent separation
  - RUN author Section 2 (Evidence Scope)
  - RUN author Section 3 (Mechanism Map): one row per mechanism with the closest documented analogue, the direct input it processes, the documented action including output/review behaviour, the unobserved elements, and evidence
  - RUN author Section 4 (Comparison Fields): the fields a later comparison must record and the conflations they prevent
  - RUN author Section 5 (Product Hypothesis) only when the map suggests one: the whitespace, the mechanism it would extend, its evidence, and the explicit not-a-commitment sentence
  - RUN author Section 6 (Boundary), Section 7 (Original Files), and Section 8 (Traceability) with the commissioning request ID
  - SET ID cpt-{system}-mech-{slug} for the study
  - RUN verify ID uniqueness with cfs list-ids
  - RUN append the back-link "`cpt-{system}-mech-{slug}` — {study title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when a line for this ID already exists, update it in place — a refresh never appends a duplicate
  - LOAD {mechanism_study_checklist} for self-review of semantic quality

RULES:
  - ALWAYS keep rows mechanisms, not companies; a company appears only as the observed example of a mechanism
  - ALWAYS record the direct input each mechanism processes and its documented output/review behaviour — these separate mechanisms that would otherwise be conflated
  - ALWAYS fill the what-is-not-established cell for every row, phrased as evidence limits
  - ALWAYS keep a mechanism observed at one vendor from implying anything about another vendor
  - ALWAYS label any requester-direction statement a product hypothesis with the not-a-commitment sentence
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {mechanism_study_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {mechanism_study_checklist} semantic criteria in this file
```

```pdsl
UNIT MechanismOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-MEC-NO-001 (CRITICAL): a cost-performance, quality, or coverage ranking of mechanisms or vendors
  - NEVER CPT-MEC-NO-002 (CRITICAL): an unobserved element rendered as absence ("vendor X lacks mechanism Y")
  - NEVER CPT-MEC-NO-003 (CRITICAL): a requester-direction statement without the product-hypothesis label and not-a-commitment sentence
  - NEVER CPT-MEC-NO-004 (HIGH): adjacent features presented as the mechanism itself (a dashboard is not an optimizer; a configuration surface is not a control plane)
  - NEVER CPT-MEC-NO-005 (HIGH): broad company-category comparison smuggled into a mechanism row
  - NEVER CPT-MEC-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT MechanismValidate

PURPOSE:
  Validate the MECHANISM-STUDY deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS
  - RUN python3 {scripts}/render_views.py <path> --format csv,html to refresh the exports
  - LOAD {mechanism_study_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {mechanism_study_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered csv/html exports; they are regenerated from the artifact
```

```pdsl
UNIT MechanismErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  question_too_broad ->
    EMIT "The question spans product categories rather than a mechanism: {summary}"
    RUN propose narrower mechanism-level questions and WAIT for the user's choice

  no_analogues ->
    EMIT "No documented analogue found in the retained set for {mechanism}"
    RUN record the empty row honestly with the search noted in completeness — an analogue-free map cell is a whitespace observation, not a failure

RULES:
  - ALWAYS ask the user whether a borderline surface counts as the mechanism or an adjacent feature
```

```pdsl
UNIT MechanismNextSteps

PURPOSE:
  Offer next actions based on study state.

DO:
  - EMIT "Whitespace with a hypothesis -> record it for human product decision, outside this kit"
  - EMIT "Analogue worth depth -> cf-compete-profile or cf-compete-dossier for that vendor"
  - EMIT "Mechanisms mature for comparison -> cf-compete-compare with a mechanism-lens frame using Section 4's fields"
```

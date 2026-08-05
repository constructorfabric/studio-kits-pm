# RESEARCH-REQUEST Rules

**Artifact**: RESEARCH-REQUEST
**Kit**: compete

```pdsl
UNIT RequestAuthoring

PURPOSE:
  Author one RESEARCH-REQUEST artifact: the structured record of what question
  must be answered, at which depth, within which evidence boundary. The request
  is the root of the traceability chain — every later register, profile,
  dossier, or comparison must be attributable to a request.

STATE:
  - SET request_source: file | inline
    default: inline when the user typed the request in chat

WHEN:
  - REQUIRE recording a new competitive-research request, or revising a draft one

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the RESEARCH-REQUEST directory
  - SET default path {artifacts_dir}/RESEARCH-REQUEST/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {research_request_template} for structure
  - LOAD {research_request_example} for content depth reference
  - RUN capture the raw request text verbatim (from the supplied file or the chat message)
  - RUN extract each of the eight request fields from the raw text: target, decision question, scope, comparison frame, depth, requested output, evidence cutoff, access boundary
  - RUN set every field the requester did not state to the literal value "unspecified" — never infer, default, or borrow a value
  - RUN author Section 2 (Boundary): what this request can establish at the selected depth, and what it cannot
  - RUN author Section 3 (Evidence and Original Files): the verbatim request text or its path, plus any named input sources
  - RUN author Section 4 (Traceability) with the default line "No artifacts have been derived from this request yet." — a fresh request MUST NOT list downstream back-links until derived artifacts exist
  - SET ID cpt-{system}-req-{slug} for the request
  - RUN verify ID uniqueness with cfs list-ids
  - LOAD {research_request_checklist} for self-review of semantic quality

RULES:
  - ALWAYS follow {research_request_template} structure with required frontmatter
  - ALWAYS render an omitted field as the literal "unspecified" so the omission stays visible in every later artifact
  - ALWAYS keep the field values faithful to the requester's words; normalization (e.g. mapping "quick look" to depth "orientation") must be shown to the requester for confirmation
  - ALWAYS state the depth-appropriate claim boundary in Section 2
  - ALWAYS keep Section 4 (Traceability) present but free of downstream references in a fresh request; downstream workflows add the mandatory request -> artifact back-links later
  - ALWAYS treat {research_request_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER reference an artifact ID that is not yet defined (dangling references fail validation)
  - NEVER create duplicate IDs
  - NEVER duplicate {research_request_checklist} semantic criteria in this file
```

```pdsl
UNIT RequestOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-REQ-NO-001 (CRITICAL): silently defaulting or inferring an omitted field instead of recording the literal "unspecified"
  - NEVER CPT-REQ-NO-002 (CRITICAL): research findings, competitor claims, feature scores, or source extracts embedded in the request — they belong in downstream artifacts
  - NEVER CPT-REQ-NO-003 (HIGH): presenting the request as a product decision, requirement, or delivery commitment
  - NEVER CPT-REQ-NO-004 (HIGH): more than one comparison frame in a single request (frames may be mapped, never silently mixed)
  - NEVER CPT-REQ-NO-005 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT RequestValidate

PURPOSE:
  Validate the RESEARCH-REQUEST deterministically and semantically, then report.

DO:
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - LOAD {research_request_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {research_request_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER duplicate checklist semantic criteria or report templates here
```

```pdsl
UNIT RequestErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  request_text_missing ->
    EMIT "No request text supplied — provide the request inline or as a file path"
    RUN ask the user for the request text

  ambiguous_field_mapping ->
    EMIT "The request wording maps to more than one value for {field}"
    RUN present the candidate readings and WAIT for the user's choice

  duplicate_request ->
    EMIT "A registered RESEARCH-REQUEST with a matching target and decision question already exists: {id}"
    RUN ask whether to revise the existing request or record a new one

RULES:
  - ALWAYS ask the user rather than guess when a field mapping is ambiguous
```

```pdsl
UNIT RequestNextSteps

PURPOSE:
  Offer next actions based on request state.

DO:
  - EMIT "Request recorded -> cf-compete-discover (build the candidate register) once evidence is available"
  - EMIT "Sources not yet indexed -> run the evidence intake before any research flow"
  - EMIT "Request changed -> revise this artifact; downstream artifacts keep citing the request ID"
```

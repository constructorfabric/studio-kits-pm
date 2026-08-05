# OSS-REVIEW Rules

**Artifact**: OSS-REVIEW
**Kit**: compete

```pdsl
UNIT OssReviewAuthoring

PURPOSE:
  Author one OSS-REVIEW artifact answering two distinct questions for a
  company set or capability: each vendor offering's source posture, and
  which public repositories may be evaluated as alternative
  implementations. Posture and repository records stay separate — a public
  repository never establishes that the vendor product is open-source or
  reusable.

WHEN:
  - REQUIRE reviewing open-source posture and alternative implementations for a registered RESEARCH-REQUEST

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the OSS-REVIEW directory
  - SET default path {artifacts_dir}/OSS-REVIEW/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {oss_review_template} for structure
  - LOAD {oss_review_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 7
  - RUN read the reviewed offerings' indexed evidence: repository extracts, licence/metadata pages, fact ledgers
  - RUN author Section 1 (Review Scope): the two questions and the never-equate-SDK-with-core statement, plus the reviewed set
  - RUN author Section 2 (Evidence Scope)
  - RUN author Section 3 (Vendor Source Posture): one row per offering; posture exactly one of open-source | open-core | partly-open-source | closed-source | not_assessed, with the basis and evidence; an offering whose posture the retained set cannot establish is not_assessed
  - RUN author Section 4 (Repository Review): one row per repository — component scope exactly one of core | connector | sdk | plugin | examples | documentation | benchmark | other; declared licence with its evidence (flag missing or conflicting licence data); activity signal with as-of date; deployability judged from documented run/self-host material, never from source visibility; reuse relevance naming the specific mechanism, the follow-up needed, and why it is not a drop-in alternative
  - RUN author Section 5 (Recommendation Boundary) and Section 6 (Original Files)
  - SET ID cpt-{system}-oss-{slug} for the review
  - RUN verify ID uniqueness with cfs list-ids; when the ID already exists, this run is a refresh — update the registered artifact file in place (same ID, same registry entry, refreshed date frontmatter), never a second file with the same ID
  - RUN append the back-link "`cpt-{system}-oss-{slug}` — {review title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when a line for this ID already exists, update it in place — a refresh never appends a duplicate
  - LOAD {oss_review_checklist} for self-review of semantic quality

RULES:
  - ALWAYS keep vendor posture (Section 3) and repository records (Section 4) as separate judgements; a repository row never upgrades a vendor's posture
  - ALWAYS treat "Other" or undetected licence as not an open-source licence; flag missing or conflicting licence information instead of assuming
  - ALWAYS include relevant alternative implementations even when no reviewed vendor owns them
  - ALWAYS make deployability an evidence-based statement about runnability/self-hostability for the mechanism in question
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {oss_review_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {oss_review_checklist} semantic criteria in this file
```

```pdsl
UNIT OssReviewOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-OSS-NO-001 (CRITICAL): a peripheral repository (SDK, connector, plugin, examples, documentation, benchmark) labelled or implied as the vendor product core
  - NEVER CPT-OSS-NO-002 (CRITICAL): repository visibility treated as evidence that the vendor product is open-source or reusable
  - NEVER CPT-OSS-NO-003 (CRITICAL): deployability inferred from source visibility rather than documented run/self-host material
  - NEVER CPT-OSS-NO-004 (HIGH): a licence assumed where the metadata is missing, "Other", or conflicting
  - NEVER CPT-OSS-NO-005 (HIGH): a reuse, buy/build, or legal conclusion — the review routes follow-ups, it does not decide
  - NEVER CPT-OSS-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT OssReviewValidate

PURPOSE:
  Validate the OSS-REVIEW deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS (enforces the posture and component-scope vocabularies per row)
  - RUN python3 {scripts}/render_views.py <path> --format csv,html to refresh the exports
  - LOAD {oss_review_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {oss_review_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered csv/html exports; they are regenerated from the artifact
```

```pdsl
UNIT OssReviewErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  no_repository_evidence ->
    EMIT "No retained repository metadata or extracts found for {offering}"
    RUN record the offering as not_assessed, or route to cf-compete-intake to index repository evidence first

  conflicting_licence ->
    EMIT "Licence evidence conflicts for {repository}: {summary}"
    RUN record both statements with sources in the licence cell and flag the legal follow-up

RULES:
  - ALWAYS ask the user whether a borderline repository (e.g. a reference implementation) counts as core or examples
```

```pdsl
UNIT OssReviewNextSteps

PURPOSE:
  Offer next actions based on review state.

DO:
  - EMIT "Clear implementation lead -> commission the named licence/architecture follow-up as its own request"
  - EMIT "Vendor posture material to positioning -> cf-compete-profile or cf-compete-dossier for that vendor"
  - EMIT "New repository evidence -> cf-compete-intake, then refresh this review (same oss ID)"
```

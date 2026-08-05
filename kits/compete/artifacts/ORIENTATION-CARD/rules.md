# ORIENTATION-CARD Rules

**Artifact**: ORIENTATION-CARD
**Kit**: compete

```pdsl
UNIT OrientationAuthoring

PURPOSE:
  Author one ORIENTATION-CARD artifact: a short, evidence-bounded
  explanation of a named company or offering, produced before deciding
  whether deeper research is worthwhile. A card orients; it never claims
  complete company facts, feature parity, or an implementation
  recommendation.

WHEN:
  - REQUIRE orienting on one named company or offering for a registered RESEARCH-REQUEST

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the ORIENTATION-CARD directory
  - SET default path {artifacts_dir}/ORIENTATION-CARD/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {orientation_card_template} for structure
  - LOAD {orientation_card_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 7
  - RUN read the subject's indexed evidence: retained extracts and the fact ledger when one exists; open nothing outside the request's access boundary
  - RUN author Section 1 (Evidence Scope): the orientation-only statement, cutoff, access boundary, completeness
  - RUN author Section 2 (What It Is): offering, stated target user/problem, principal documented mechanisms — every claim referenced
  - RUN author Section 3 (Visible Product Surfaces): one evidenced bullet per surface
  - RUN author Section 4 (Company and Source Posture): visible commercial model or its explicit not-established statement; source posture; source classes labelled; dates carried
  - RUN author Section 5 (Important Unknowns) and Section 6 (Original Files)
  - SET ID cpt-{system}-ori-{slug} for the card
  - RUN verify ID uniqueness with cfs list-ids
  - RUN append the back-link "`cpt-{system}-ori-{slug}` — {card title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when a line for this ID already exists, update it in place — a refresh never appends a duplicate
  - LOAD {orientation_card_checklist} for self-review of semantic quality

RULES:
  - ALWAYS follow {orientation_card_template} structure with required frontmatter
  - ALWAYS keep the card short: it answers "what is this and is deeper research worthwhile?", nothing more
  - ALWAYS give every factual statement at least one resolvable evidence reference and every time-sensitive statement its source date
  - ALWAYS label source classes in the wording (third-party profile, vendor page, repository) so posture is auditable
  - ALWAYS record what the sources do not establish in Important Unknowns — never fill gaps from general knowledge
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {orientation_card_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {orientation_card_checklist} semantic criteria in this file
```

```pdsl
UNIT OrientationOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-ORI-NO-001 (CRITICAL): feature-parity claims, complete-company-facts claims, or customer-outcome validation
  - NEVER CPT-ORI-NO-002 (CRITICAL): absence claims ("lacks", "does not have") derived from missing public evidence
  - NEVER CPT-ORI-NO-003 (CRITICAL): claims filled from general knowledge rather than the retained sources
  - NEVER CPT-ORI-NO-004 (HIGH): an implementation recommendation or buy/build statement — those need profile or dossier depth
  - NEVER CPT-ORI-NO-005 (HIGH): a deep feature inventory — that is profile/dossier material
  - NEVER CPT-ORI-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT OrientationValidate

PURPOSE:
  Validate the ORIENTATION-CARD deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS
  - RUN python3 {scripts}/render_views.py <path> --format html to refresh the export
  - LOAD {orientation_card_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {orientation_card_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered html export; it is regenerated from the artifact
```

```pdsl
UNIT OrientationErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  no_subject_evidence ->
    EMIT "No indexed evidence found for {subject}"
    RUN route to cf-compete-intake to index the retained sources first

  unresolved_evidence ->
    EMIT "The card cites {ref}, which does not resolve in the evidence index"
    RUN route to cf-compete-intake to index the missing source, or drop the citation

RULES:
  - ALWAYS ask the user when the subject is ambiguous (company vs product vs repository)
```

```pdsl
UNIT OrientationNextSteps

PURPOSE:
  Offer next actions based on card state.

DO:
  - EMIT "Deeper research worthwhile -> cf-compete-profile (standard profile) or cf-compete-dossier (deep dossier)"
  - EMIT "Subject belongs beside peers -> cf-compete-discover adds it to a candidate register"
  - EMIT "New evidence drop -> cf-compete-intake, then refresh this card (same ori ID)"
```

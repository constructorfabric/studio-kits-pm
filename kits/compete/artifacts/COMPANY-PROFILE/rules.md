# COMPANY-PROFILE Rules

**Artifact**: COMPANY-PROFILE
**Kit**: compete

```pdsl
UNIT ProfileAuthoring

PURPOSE:
  Author one COMPANY-PROFILE artifact: a consistent, source-backed company
  page for judging whether a company is a serious comparator and which
  documented mechanisms may be relevant. Facts, vendor claims, analyst
  interpretation, and unknowns remain distinct throughout.

WHEN:
  - REQUIRE building or refreshing a standard company profile for a registered RESEARCH-REQUEST

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the COMPANY-PROFILE directory
  - SET default path {artifacts_dir}/COMPANY-PROFILE/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {company_profile_template} for structure
  - LOAD {company_profile_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 11
  - RUN read the company's fact ledger (competitive/companies/COMP-###-{slug}/facts.tsv) when one exists; its claim_status labels drive the observed-vs-vendor-claim wording
  - RUN read the retained extracts the profile will cite; open nothing outside the request's access boundary
  - RUN assign every standard source class (landing, pricing, docs, repository, corporate/finance) its capture status: captured | failed (mode) | gated | deferred (reason)
  - RUN create the company fact ledger when none exists and append one row per time-sensitive observation the profile cites (pricing, promos, maturity labels, funding) with claim_status, observed_on, evidence_refs, limitation; verify with {scripts}/check_evidence.py
  - RUN author Section 1 (Evidence Scope): the not-a-dossier statement, cutoff, access boundary, the source-class capture statuses, completeness
  - RUN author Section 2 (Company and Commercial Facts): one row per field; a fact absent from the retained set is written as "Not publicly established in the retained source set." with the do-not-infer boundary; every time-sensitive value carries as-of framing; every row's boundary cell carries an evidence reference
  - RUN author Section 3 (What the Company Provides): offerings -> capabilities -> concrete features/mechanisms, target users, deployment, integrations — each paragraph evidenced
  - RUN author Section 4 (Strongest Documented Point) and Section 5 (Weakest Documented Boundary) as evidence limits, never absence claims
  - RUN author Section 6 (Studio Relevance): coverage in scope for the request's comparison frame, observed coverage separated from requester vision
  - RUN author Section 7 (What to Borrow — Product Hypothesis): zero or more entries, each with ID cpt-{system}-bor-{slug}, the named motivating mechanism, its evidence, and the explicit not-a-commitment sentence; when none qualified, state that explicitly
  - RUN author Section 8 (Open-Source Posture), Section 9 (Material Unknowns), Section 10 (Original Files)
  - SET ID cpt-{system}-prof-{slug} for the profile
  - RUN verify ID uniqueness with cfs list-ids; when the ID already exists, this run is a refresh — update the registered artifact file in place (same ID, same registry entry, refreshed date frontmatter), never a second file with the same ID
  - RUN append the back-link "`cpt-{system}-prof-{slug}` — {profile title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when one or more lines for this ID already exist, collapse them into a single line updated in place (other artifacts' lines stay untouched) — a refresh never appends a duplicate and always repairs duplicates left by earlier runs
  - LOAD {company_profile_checklist} for self-review of semantic quality

RULES:
  - ALWAYS follow {company_profile_template} structure with required frontmatter
  - ALWAYS distinguish observed facts, vendor claims, third-party estimates, interpretation, and unknowns — use the fact ledger's claim_status labels in the wording ("YC describes…", "the vendor states…")
  - ALWAYS write missing public evidence as "Not publicly established in the retained source set." — never as feature or fact absence
  - ALWAYS give every facts-table row an evidence reference in its boundary cell and as-of framing for time-sensitive values
  - ALWAYS state a capture status for every standard source class in Evidence Scope — a deferred cheap-to-capture class is a visible routing signal, never a silent omission
  - ALWAYS ledger the time-sensitive facts the profile cites — the next watch or profile pass diffs against the ledger's as-of history
  - ALWAYS label every borrow entry a hypothesis tied to a named documented mechanism; it creates no requirement, decision, or commitment
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {company_profile_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {company_profile_checklist} semantic criteria in this file
```

```pdsl
UNIT ProfileOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-PRO-NO-001 (CRITICAL): absence claims ("lacks", "does not have") derived from missing public evidence
  - NEVER CPT-PRO-NO-002 (CRITICAL): a vendor claim or third-party estimate presented as an observed fact
  - NEVER CPT-PRO-NO-003 (CRITICAL): a "what to borrow" statement without the hypothesis label, the named motivating mechanism, or the not-a-commitment sentence
  - NEVER CPT-PRO-NO-004 (HIGH): a time-sensitive fact (team, funding, pricing, adoption) without an as-of date and evidence source
  - NEVER CPT-PRO-NO-005 (HIGH): feature-parity conclusions, rankings, or a buy/build recommendation — those need a comparison or dossier depth
  - NEVER CPT-PRO-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT ProfileValidate

PURPOSE:
  Validate the COMPANY-PROFILE deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS
  - RUN python3 {scripts}/render_views.py <path> --format html to refresh the export
  - LOAD {company_profile_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {company_profile_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered html export; it is regenerated from the artifact
```

```pdsl
UNIT ProfileErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  no_company_evidence ->
    EMIT "No indexed evidence or fact ledger found for {company}"
    RUN route to cf-compete-intake to index the retained sources first

  unresolved_evidence ->
    EMIT "The profile cites {ref}, which does not resolve in the evidence index"
    RUN route to cf-compete-intake to index the missing source, or drop the citation

  conflicting_sources ->
    EMIT "Sources conflict on {field}: {summary}"
    RUN record both values with their sources and dates in the facts table; do not average or pick silently

RULES:
  - ALWAYS ask the user when the profiled offering is ambiguous (company vs product vs repository)
```

```pdsl
UNIT ProfileNextSteps

PURPOSE:
  Offer next actions based on profile state.

DO:
  - EMIT "Profile suggests a buy/build or positioning question -> cf-compete-dossier deepens it (arrives with the COMPANY-DOSSIER kind)"
  - EMIT "Two or more companies profiled -> a single-frame comparison becomes possible (arrives with the COMPARISON-MATRIX kind)"
  - EMIT "New evidence drop -> cf-compete-intake, then refresh this profile (same prof ID)"
```

# WATCH-REPORT Rules

**Artifact**: WATCH-REPORT
**Kit**: compete

```pdsl
UNIT WatchAuthoring

PURPOSE:
  Author one WATCH-REPORT artifact: a watch pass over a register of watched
  fields for one subject. The first pass publishes a dated baseline; later
  passes publish dated change records against the prior retained report.
  A change signal never becomes an impact claim.

STATE:
  - SET mode: baseline | change-report
    default: baseline when no prior WATCH-REPORT for the subject is registered

WHEN:
  - REQUIRE establishing or running a competitive watch for a registered RESEARCH-REQUEST

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the WATCH-REPORT directory
  - SET default path {artifacts_dir}/WATCH-REPORT/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {watch_report_template} for structure
  - LOAD {watch_report_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 8
  - RUN resolve the prior WATCH-REPORT for the subject with cfs list-ids; SET mode = change-report when one exists, baseline otherwise
  - RUN author Section 1 (Watch Scope): subject, watched fields per the request, cadence, and the no-impact-inference statement
  - RUN author Section 2 (Evidence Scope), noting fields that could not be observed this pass
  - RUN author Section 3 (Watch Status) per mode, naming the prior report and both observation dates in change-report mode
  - RUN author Section 4 (Watch Register): one row per watched field with the current dated observation, evidence, and a concrete next comparison rule
  - RUN in change-report mode: compare each field against the prior report's register and author Section 5 (Detected Changes) — one row per change with prior observation, current observation, ISO observed_on, why it matters to the research question, and evidence; when no field changed, keep the section with the explicit line "No material change was detected this pass."
  - RUN in baseline mode: author Section 5 with the explicit line "Baseline pass — no prior retained observation exists, so no change detection applies." and no table
  - RUN author Section 6 (Boundary) and Section 7 (Original Files)
  - SET ID cpt-{system}-wat-{slug} for this pass, where {slug} carries a per-pass token — the pass date or a pass label (openspec-baseline, openspec-2026-10) — so every pass mints a distinct ID; the register carries continuity
  - RUN verify ID uniqueness with cfs list-ids
  - RUN append the back-link "`cpt-{system}-wat-{slug}` — {report title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when a line for this ID already exists, update it in place — a refresh never appends a duplicate
  - LOAD {watch_report_checklist} for self-review of semantic quality

RULES:
  - ALWAYS publish a baseline when no prior retained observation exists — never a change claim
  - ALWAYS give every register row a concrete next comparison rule: what observation would count as a material change for that field
  - ALWAYS date every observation; a change row carries the prior observation, the current observation, and the observation date
  - ALWAYS keep change records signal-level: why it matters to the research question, never customer/revenue/strategic impact
  - ALWAYS record an unobservable field in completeness — never carry it forward as silently unchanged
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {watch_report_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {watch_report_checklist} semantic criteria in this file
```

```pdsl
UNIT WatchOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-WAT-NO-001 (CRITICAL): a change claim without a prior retained observation — the first pass is a baseline
  - NEVER CPT-WAT-NO-002 (CRITICAL): customer, revenue, adoption, or strategic impact inferred from a change signal alone
  - NEVER CPT-WAT-NO-003 (CRITICAL): an undated observation or change record
  - NEVER CPT-WAT-NO-004 (HIGH): an unobserved field treated as unchanged instead of recorded in completeness
  - NEVER CPT-WAT-NO-005 (HIGH): rankings, trend scores, or momentum conclusions built on top of change records
  - NEVER CPT-WAT-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT WatchValidate

PURPOSE:
  Validate the WATCH-REPORT deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS (enforces the per-row evidence duty and the change-row date)
  - RUN python3 {scripts}/render_views.py <path> --format csv,html to refresh the exports
  - LOAD {watch_report_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {watch_report_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered csv/html exports; they are regenerated from the artifact
```

```pdsl
UNIT WatchErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  stale_evidence ->
    EMIT "The indexed evidence predates the watch cadence window; a pass over stale evidence would re-observe the baseline"
    RUN ask whether to intake a fresh evidence drop first (cf-compete-intake) or record the pass with completeness noting the stale window

  field_unobservable ->
    EMIT "Watched field {field} has no current observation in the retained set"
    RUN record the field in Evidence Scope completeness; do not infer it unchanged

  prior_report_missing_field ->
    EMIT "Field {field} is watched now but absent from the prior report"
    RUN record it as a baseline row in the register, not a change

RULES:
  - ALWAYS ask the user before narrowing or widening the watched-field set relative to the request
```

```pdsl
UNIT WatchNextSteps

PURPOSE:
  Offer next actions based on watch state.

DO:
  - EMIT "Baseline established -> intake a fresh evidence drop at the cadence, then run the next pass (change-report mode)"
  - EMIT "Material change detected -> commission the follow-up its next-comparison rule implies (profile refresh, dossier, comparison)"
  - EMIT "Watched set changed -> revise the RESEARCH-REQUEST first, then re-baseline the new fields"
```

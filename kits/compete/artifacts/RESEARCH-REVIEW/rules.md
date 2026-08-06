# RESEARCH-REVIEW Rules

**Artifact**: RESEARCH-REVIEW
**Kit**: compete

## Conformance contract

The Requirements Conformance section verdicts each commissioned flow
against this fixed contract (the epic's per-flow acceptance criteria)
plus whatever the commissioning request's Requested output field adds:

| Flow | Required content |
| --- | --- |
| Research request | All eight fields present; every omitted field visibly "unspecified". |
| Candidate register | Every candidate: name, source/evidence, relevance reason, direct/adjacent/emerging classification, next action; no feature score or parity conclusion. |
| Orientation card | Offering, target user/problem, visible mechanisms, commercial/source posture, ≥1 dated source, unknowns; visibly not a full profile. |
| Company profile | All required sections or explicit unavailability; a capture status per standard source class in Evidence Scope; time-sensitive facts ledgered and as-of dated; every borrow labelled a hypothesis with its motivating mechanism; facts, vendor claims, interpretation, unknowns distinct. |
| Company dossier | Examined sources with availability classes covering the standard classes even when uncaptured, capability graph, limitations; not_observed never rendered as absence. |
| Comparison matrix | One agreed frame; every cell: mechanism, status, evidence, observation date, availability; register direct candidates absent from the matrix named as exclusions with reasons; Studio today separate from Studio vision. |
| OSS review | Vendor posture separate from per-repository licence/scope/activity/deployability/reuse records; no peripheral repository labelled product core. |
| Mechanism study | Per mechanism: inputs, documented operation, output/review behaviour, analogue, evidence boundary, unobserved elements; any Studio direction visibly a product hypothesis. |
| Watch report | Dated source, watched field, prior/current values where available, defined cadence; no impact claims from a change signal alone. |

```pdsl
UNIT ReviewAuthoring

PURPOSE:
  Author one RESEARCH-REVIEW artifact: an audit of a research run's
  artifact set for requirements conformance, next-action coverage, and
  informativeness. The review adds no research content — it reads what
  the run retained and routes what is missing.

WHEN:
  - REQUIRE reviewing the artifact set of a registered RESEARCH-REQUEST

DO:
  - LOAD {cf-studio-path}/config/artifacts.toml to resolve the RESEARCH-REVIEW directory
  - SET default path {artifacts_dir}/RESEARCH-REVIEW/{yyyy-mm-dd}-{slug}.md and register in artifacts.toml
  - LOAD {research_review_template} for structure
  - LOAD {research_review_example} for content depth reference
  - RUN resolve the commissioning RESEARCH-REQUEST with cfs list-ids; record its ID in the frontmatter and Section 9
  - RUN python3 {scripts}/check_coverage.py <artifacts-dir> --evidence-dir competitive/evidence --companies-dir competitive/companies and retain its report
  - RUN author Section 1 (Review Scope): the reviewed artifact set, the conformance contract in force, and the not-a-research-result statement
  - RUN author Section 2 (Evidence Scope), listing artifacts not reviewed and whether the coverage report ran
  - RUN author Section 3 (Requirements Conformance): one row per commissioned flow, verdict from {met | partial | gap | not_commissioned}; verify each verdict by reading the artifact, never from the coverage report alone
  - RUN author Section 4 (Run Coverage): one row per register next action, status from {done | partial | open | superseded}, correcting the coverage report's name-matching by hand where it mis-attributed
  - RUN author Section 5 (Informativeness Findings): severity from {critical | high | medium | low}; each finding names its affected artifacts and one concrete recommended action
  - RUN author Section 6 (Recommended Next Passes): an ordered list, every item naming a kit workflow and subject
  - RUN author Section 7 (Boundary) and Section 8 (Original Files)
  - SET ID cpt-{system}-rev-{slug}; verify uniqueness with cfs list-ids
  - RUN append the back-link "`cpt-{system}-rev-{slug}` — {review title}" to the commissioning request's Traceability section only when the ID is absent (replace the default no-derived-artifacts line when present); when one or more lines for this ID already exist, collapse them into a single line updated in place (other artifacts' lines stay untouched) — a refresh never appends a duplicate and always repairs duplicates left by earlier runs, and a stale no-derived-artifacts line is removed whenever any back-link is present
  - LOAD {research_review_checklist} for self-review of semantic quality

RULES:
  - ALWAYS verdict against the conformance contract above plus the request's Requested output — never against taste
  - ALWAYS name the artifact behind every met/partial verdict and the fulfilling artifact behind every done/partial coverage row
  - ALWAYS distinguish an honestly-declared evidence limit (an informativeness finding about the run) from a conformance failure (required content absent from the artifact)
  - ALWAYS make every recommended action concrete: which workflow, which subject, what it would close
  - ALWAYS update the commissioning request's Traceability section in the same run
  - ALWAYS treat {research_review_checklist} as the semantic source of truth
  - NEVER include placeholder content (TODO, TBD, FIXME)
  - NEVER create duplicate IDs
  - NEVER duplicate {research_review_checklist} semantic criteria in this file
```

```pdsl
UNIT ReviewOmissions

PURPOSE:
  Enforce MUST NOT HAVE content; report any occurrence as a violation.

RULES:
  - NEVER CPT-REV-NO-001 (CRITICAL): new vendor claims, evidence, or research findings introduced by the review — a review audits the run; it never researches
  - NEVER CPT-REV-NO-002 (CRITICAL): a conformance verdict that names neither the artifact nor the exact missing content — an unverifiable verdict
  - NEVER CPT-REV-NO-003 (CRITICAL): an honestly-declared evidence limit rendered as a conformance failure of the declaring artifact
  - NEVER CPT-REV-NO-004 (HIGH): a recommendation phrased as a commitment, requirement, or product decision
  - NEVER CPT-REV-NO-005 (HIGH): a ranking or scoring of artifacts, vendors, or the run against other runs
  - NEVER CPT-REV-NO-006 (HIGH): placeholder content (TODO, TBD, FIXME)
```

```pdsl
UNIT ReviewValidate

PURPOSE:
  Validate the RESEARCH-REVIEW deterministically and semantically, then report.

DO:
  - RUN cfs toc <artifact-file> to generate/update Table of Contents
  - RUN cfs validate --artifact <path> for template structure, ID format, no placeholders
  - RUN cfs validate-toc <artifact-file> — must report PASS
  - RUN python3 {scripts}/check_artifact_refs.py <path> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language — must report PASS (enforces the verdict/status/severity vocabularies and the artifact-reference duty)
  - RUN python3 {scripts}/render_views.py <path> --format csv,html to refresh the exports
  - LOAD {research_review_checklist} for semantic validation and report format
  - RETURN validation report (Structural PASS/FAIL, References PASS/FAIL, Semantic PASS/FAIL with issues)

RULES:
  - ALWAYS use {research_review_checklist} as the source for semantic criteria and the review report format
  - NEVER mark validation done while any check reports FAIL or error
  - NEVER hand-edit the rendered csv/html exports; they are regenerated from the artifact
```

```pdsl
UNIT ReviewErrorHandling

PURPOSE:
  Recover from input failures and escalate ambiguous situations.

ON_ERROR:
  no_research_request ->
    EMIT "No registered RESEARCH-REQUEST found — record one first with cf-compete-request"
    RUN STOP

  no_artifacts ->
    EMIT "The request has no derived artifacts yet — there is nothing to review"
    RUN STOP

  coverage_script_failed ->
    EMIT "check_coverage.py did not produce a report"
    RUN fix the invocation (artifacts dir, evidence dir) and re-run; author Section 4 only from a produced report

  ambiguous_fulfilment ->
    EMIT "Next action for {candidate} may be fulfilled by {artifact} — the name match is uncertain"
    RUN read the artifact and decide by content; record the correction in Section 4

RULES:
  - ALWAYS ask the user before treating a next action as superseded
```

```pdsl
UNIT ReviewNextSteps

PURPOSE:
  Offer next actions based on review state.

DO:
  - EMIT "Open next actions or findings -> run the recommended passes (capture/orient/profile/dossier/compare/oss-review/mechanism/watch), then re-run cf-compete-review to measure the closure"
  - EMIT "Conformance gap in an artifact -> re-run its authoring workflow against its checklist, then re-review"
  - EMIT "Contract itself wrong or outdated -> revise the RESEARCH-REQUEST (requested output) or the kit's conformance contract, then re-review"
```

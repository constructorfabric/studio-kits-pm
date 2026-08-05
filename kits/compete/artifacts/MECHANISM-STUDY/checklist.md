# MECHANISM-STUDY Expert Checklist

**Artifact**: MECHANISM-STUDY
**Version**: 1.0
**Purpose**: Semantic quality checklist for mechanism and whitespace studies

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates MECHANISM-STUDY artifacts
- [ ] I have access to the analysis briefs, fact ledgers, and extracts the study cites
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

A mechanism study answers a narrow question by comparing documented
mechanisms, not companies. Its most common corruptions are conflation (an
adjacent feature presented as the mechanism) and category creep (rows
drifting into broad product comparison). A map cell without an analogue is
a whitespace observation, not a defect. The Product Hypothesis section is
optional; its absence is correct when the map suggests none.

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the result: ranking, absence rendering, unlabelled hypothesis |
| HIGH | Undermines the map: conflated mechanism, missing input/output behaviour, empty negative cell |
| MEDIUM | Reduces usefulness: vendor-specific mechanism names, generic comparison fields |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 🔬 MECHANISM Discipline (MECH)

#### MECH-STU-001: Rows Are Mechanisms (CRITICAL)
- Every map row names a mechanism in normalized, domain-standard wording; companies appear only as observed examples.
- No row smuggles in a broad company-category comparison.

#### MECH-STU-002: Input and Operation Recorded (HIGH)
- Every row records the direct input the mechanism processes and its documented action including output/review behaviour — the fields that keep unlike surfaces apart.

#### MECH-STU-003: Conflation Guard (HIGH)
- Adjacent features are separated from direct mechanisms per the request's question; the study never calls a dashboard an optimizer or a configuration surface a control plane.

#### MECH-STU-004: Per-Row Negative Space (CRITICAL)
- Every row's what-is-not-established cell is substantive and phrased as evidence limits.

### 🧭 WHITESPACE Quality (WHIT)

#### WHIT-STU-001: Comparison Fields Prescribed (HIGH)
- Section 4 names the fields a later comparison must record and the specific conflations they prevent.

#### WHIT-STU-002: Labelled Hypothesis (CRITICAL)
- When present, the Product Hypothesis names the observed whitespace, the mechanism it would extend, its evidence, and the explicit not-a-commitment sentence.

### 🔍 EVIDENCE Discipline (EVID)

#### EVID-STU-001: Every Row Evidenced (CRITICAL)
- Every map row carries at least one resolvable evidence reference, and the cited evidence actually documents the described action.

#### EVID-STU-002: Cross-Vendor Silence (CRITICAL)
- A mechanism observed at one vendor implies nothing about another; no cell or conclusion converts one vendor's documentation into another's gap.

### 🔗 TRACE Integrity (TRC)

#### TRC-STU-001: Request Back-Link (CRITICAL)
- Section 8 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this study.

#### TRC-STU-002: Original Files (MEDIUM)
- Section 7 names the analysis briefs, fact ledgers, and index locators actually used.

## MUST NOT HAVE

- **CPT-MEC-NO-001 (CRITICAL)**: a cost-performance, quality, or coverage ranking of mechanisms or vendors
- **CPT-MEC-NO-002 (CRITICAL)**: an unobserved element rendered as absence
- **CPT-MEC-NO-003 (CRITICAL)**: a requester-direction statement without the product-hypothesis label and not-a-commitment sentence
- **CPT-MEC-NO-004 (HIGH)**: adjacent features presented as the mechanism itself
- **CPT-MEC-NO-005 (HIGH)**: broad company-category comparison smuggled into a mechanism row
- **CPT-MEC-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

## Validation Summary

### Final Checklist

- [ ] All MUST HAVE items checked (or marked N/A with justification)
- [ ] All MUST NOT HAVE items verified absent
- [ ] All issues documented with evidence and proposals
- [ ] `cfs validate --artifact <path>` and `check_artifact_refs.py` report PASS

## Reporting

Report **only** problems (do not list what is OK).

For each issue include:

- **Why Applicable**: Why this requirement applies to this artifact's context
- **Issue**: What is wrong (requirement missing or incomplete)
- **Evidence**: Quote the exact text or location in the artifact (or note "No mention found")
- **Why it matters**: Impact on the whitespace question this study informs
- **Proposal**: Concrete fix (what to change/add/remove) with clear acceptance criteria

### Report Format

```markdown
## Review Report (Issues Only)

### 1. {Short issue title}

**Checklist Item**: `{CHECKLIST-ID}` — {Checklist item title}

**Severity**: CRITICAL|HIGH|MEDIUM|LOW

#### Why Applicable
{...}

#### Issue
{...}

#### Evidence
{...}

#### Why It Matters
{...}

#### Proposal
{...}

---
```

When no issues are found, report: "MECHANISM-STUDY semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

# RESEARCH-REQUEST Expert Checklist

**Artifact**: RESEARCH-REQUEST
**Version**: 1.0
**Purpose**: Semantic quality checklist for competitive-research request artifacts

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates RESEARCH-REQUEST artifacts
- [ ] I have access to the original request text quoted in Section 3
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

A request may legitimately begin with only a target and a depth; sparseness is
not a defect. What the checklist enforces is that every omission is visible
("unspecified") and that stated values are faithful to the requester's words.

When a check does not apply, mark it N/A with a one-line justification instead
of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the chain: silently defaulted field, embedded findings, invented value |
| HIGH | Undermines downstream research: unfaithful field mapping, missing claim boundary |
| MEDIUM | Reduces usefulness: vague decision question, boundary boilerplate without depth fit |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 📋 FIELD Completeness and Fidelity (FLD)

#### FLD-REQ-001: All Eight Fields Present (CRITICAL)
- The Request Fields table contains exactly the eight fields: Target, Decision question, Scope, Comparison frame, Depth, Requested output, Evidence cutoff, Access boundary.
- Every field carries either a stated value or the literal "unspecified" — no blank cells, no dashes standing in for omission.

#### FLD-REQ-002: Field Fidelity (CRITICAL)
- Each stated value traces to the original request text in Section 3; any normalization (wording changed to a canonical depth or scope term) was confirmed by the requester.
- No value was inferred from context the requester did not supply.

#### FLD-REQ-003: Depth and Output Coherence (HIGH)
- The requested output is producible at the selected depth (e.g. a feature-coverage matrix is not a discovery-scan output).
- The comparison frame, when stated, is a single frame.

### 🚧 BOUNDARY Discipline (BNDY)

#### BNDY-REQ-001: Depth-Appropriate Claim Boundary (HIGH)
- Section 2 states what this request can establish at its depth AND what it cannot (feature coverage, quality, market rank, commercial viability, source-code reuse — as applicable).
- The boundary is specific to this request's target and depth, not generic boilerplate.

#### BNDY-REQ-002: Evidence Boundary Visibility (HIGH)
- Evidence cutoff and access boundary are stated or visibly "unspecified"; when stated, the cutoff is a concrete date and the access boundary names the source classes allowed.

### 🔗 TRACE Readiness (TRC)

#### TRC-REQ-001: Original Request Preserved (HIGH)
- Section 3 quotes the request text verbatim or names its file path, so field mappings can be audited later.

#### TRC-REQ-002: Fresh Traceability Section (MEDIUM)
- A fresh request's Section 4 contains only the default no-derived-artifacts line; a revised request's Section 4 lists each derived artifact ID exactly once.

## MUST NOT HAVE

- **CPT-REQ-NO-001 (CRITICAL)**: silently defaulting or inferring an omitted field instead of the literal "unspecified"
- **CPT-REQ-NO-002 (CRITICAL)**: research findings, competitor claims, feature scores, or source extracts embedded in the request
- **CPT-REQ-NO-003 (HIGH)**: presenting the request as a product decision, requirement, or delivery commitment
- **CPT-REQ-NO-004 (HIGH)**: more than one comparison frame in a single request
- **CPT-REQ-NO-005 (HIGH)**: placeholder content (TODO, TBD, FIXME)

## Validation Summary

### Final Checklist

- [ ] All MUST HAVE items checked (or marked N/A with justification)
- [ ] All MUST NOT HAVE items verified absent
- [ ] All issues documented with evidence and proposals
- [ ] `cfs validate --artifact <path>` reports PASS

## Reporting

Report **only** problems (do not list what is OK).

For each issue include:

- **Why Applicable**: Why this requirement applies to this artifact's context
- **Issue**: What is wrong (requirement missing or incomplete)
- **Evidence**: Quote the exact text or location in the artifact (or note "No mention found")
- **Why it matters**: Impact on downstream competitive research
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

When no issues are found, report: "RESEARCH-REQUEST semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

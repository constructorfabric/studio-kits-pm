# COMPANY-DOSSIER Expert Checklist

**Artifact**: COMPANY-DOSSIER
**Version**: 1.0
**Purpose**: Semantic quality checklist for deep company dossiers

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates COMPANY-DOSSIER artifacts
- [ ] I have access to the retained extracts and fact ledger the dossier cites
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

A dossier's value is proportional to its honesty about limits: over a thin
retained set it is legitimately dominated by unestablished cells, and that
is correct behaviour, not a defect. What the checklist enforces is that the
documented side is genuinely evidenced, the unestablished side is genuinely
recorded, and no inference bridges the two.

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the result: absence claim, inferred workflow/outcome, vendor claim as fact |
| HIGH | Undermines the assessment: empty negative space, wrong availability class, missing source-class inventory |
| MEDIUM | Reduces usefulness: shallow capability graph, generic conclusion |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 📚 EVIDENCE Scope Honesty (EVSC)

#### EVSC-DOS-001: Source Inventory (HIGH)
- Section 1 states the source count, access dates, and which source classes were examined and which were not.
- The vendor-described-boundary statement is present: the dossier establishes documentation surface, not verified runtime behaviour or customer outcome.

#### EVSC-DOS-002: Boundary Compliance (HIGH)
- Nothing outside the request's access boundary is summarized; gated or unavailable sources appear only in Source Availability with the correct class.

### 🗺️ MECHANICS Discipline (MECH)

#### MECH-DOS-001: Per-Area Negative Space (CRITICAL)
- Every Documented Mechanics row has a substantive "what remains unestablished" cell — configuration, execution, outcomes, or scope the sources do not establish — phrased as evidence limits.

#### MECH-DOS-002: Documented Side Is Evidenced (CRITICAL)
- Every documented-surface cell traces to retained evidence; spot-check that the cited extract actually documents the described surface.

#### MECH-DOS-003: Capability Graph Fidelity (MEDIUM)
- The offering → capability → features rows reflect the vendor's own documented structure, with evidence per row — not an invented taxonomy.

### 🚦 AVAILABILITY Discipline (AVAIL)

#### AVAIL-DOS-001: Source-Class Vocabulary (HIGH)
- Every Source Availability row uses exactly one of: public, gated, unavailable, planned, preview — with evidence.
- Documentation availability is nowhere equated with feature availability.

### 🎯 CONCLUSION Quality (CONC)

#### CONC-DOS-001: Two-Sided Conclusion (HIGH)
- Section 7 states both what the subject is a credible research subject for AND what the retained set does not establish, closing with the evidence-limits-not-absence-claims sentence.

#### CONC-DOS-002: No Decision Creep (CRITICAL)
- The conclusion informs buy/build/positioning questions without making a recommendation, ranking, or decision.

### 🔗 TRACE Integrity (TRC)

#### TRC-DOS-001: Request Back-Link (CRITICAL)
- Section 9 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this dossier.

#### TRC-DOS-002: Profile Relation (MEDIUM)
- When a standard profile exists for the subject, Sections 8–9 name it; when none exists, Section 8 says so explicitly.

## MUST NOT HAVE

- **CPT-DOS-NO-001 (CRITICAL)**: absence claims derived from missing public evidence
- **CPT-DOS-NO-002 (CRITICAL)**: an inferred executed workflow, customer outcome, or runtime behaviour no retained source documents
- **CPT-DOS-NO-003 (CRITICAL)**: a vendor claim or third-party estimate presented as an observed fact
- **CPT-DOS-NO-004 (HIGH)**: vendor documentation claims treated as independently validated
- **CPT-DOS-NO-005 (HIGH)**: buy/build recommendations, rankings, or product decisions
- **CPT-DOS-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

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

When no issues are found, report: "COMPANY-DOSSIER semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

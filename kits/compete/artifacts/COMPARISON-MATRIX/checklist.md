# COMPARISON-MATRIX Expert Checklist

**Artifact**: COMPARISON-MATRIX
**Version**: 1.0
**Purpose**: Semantic quality checklist for single-frame competitive comparisons

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates COMPARISON-MATRIX artifacts
- [ ] I have access to the evidence, profiles/dossiers, and analysis briefs the matrix cites
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

A matrix is only as good as its frame discipline: one frame, normalized
labels, dated cells. A column dominated by not_observed cells is a valid
result when the boundary cells say why. The Studio Position section applies
only when Studio is among the compared; its absence otherwise is correct.

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the result: ranking language, not_observed as absence, vision scored as delivered |
| HIGH | Undermines comparability: mixed frames, vendor-specific labels, undated cells, incommensurable numbers |
| MEDIUM | Reduces usefulness: shallow boundary cells, conclusion that ignores negative findings |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 🖼️ FRAME Discipline (FRAME)

#### FRAME-CMP-001: One Frame, Stated Both Ways (CRITICAL)
- Section 1 states the single frame as the question the matrix answers AND the question it must not be read as answering.
- Every matrix row belongs to that frame; nothing from a second lens is mixed in.

#### FRAME-CMP-002: Normalized Labels (HIGH)
- Feature/mechanism labels are domain-standard and normalized across vendors (synonyms and vendor-specific names unified after reviewing all compared documentation), readable by an industry expert.

#### FRAME-CMP-003: Compared Set Justified (HIGH)
- Section 1 says why each company is in the comparison and Section 8 names the profile/dossier or evidence behind each.

#### FRAME-CMP-005: Taxonomy-Bound Rows (CRITICAL)
- The frontmatter declares the frame's FEATURE-TAXONOMY and every feature label is one of its rows (detail after a colon); every taxonomy row appears for every compared company, not_observed where evidence lacks.
- When no taxonomy is declared, the artifact records that the user explicitly declined one — ad-hoc rows are never a silent default.

#### FRAME-CMP-004: Exclusions Named (HIGH)
- The compared set is checked against the register's direct candidates: every direct candidate absent from the matrix is named in Section 1 as an explicit exclusion with its reason (under-evidenced, out of frame, deferred) — a column left out silently reads as a decision nobody made.

### 🔬 CELL Contract (CELL)

#### CELL-CMP-001: Full Cell Contract (CRITICAL)
- Every row carries: status from {substantial, partial, not_observed, not_comparable}; availability from {current, planned, vision}; an ISO observed_on date; a substantive documented-boundary cell; ≥1 resolvable evidence reference.

#### CELL-CMP-002: Honest Non-Assessment (CRITICAL)
- not_observed is used for missing retained evidence and not_comparable where the frame does not apply — each with the reason in the boundary cell; neither is ever rendered as the company lacking the capability.

#### CELL-CMP-003: Availability Fidelity (HIGH)
- current/planned/vision matches what the evidence documents (a roadmap page is planned; a vendor aspiration is vision); vision rows are never treated as delivered.

### 🎯 CONCLUSION Quality (CONC)

#### CONC-CMP-001: Frame-Bounded Conclusion (HIGH)
- Section 5 answers the frame's question, names the per-company characterizations, and includes the negative findings (what none of the reviewed documentation establishes).

#### CONC-CMP-002: No Decision Creep (CRITICAL)
- Any proposed action is labelled a product hypothesis awaiting a human decision; no winner is declared.

### 🏛️ STUDIO Position (STUD)

#### STUD-CMP-001: Today vs Vision Separation (CRITICAL)
- When Studio is compared: Studio today and Studio vision appear as separate rows or labels, vision rows carry availability `vision`, and the conclusion never scores them as equivalent delivered capability.

### 🔗 TRACE Integrity (TRC)

#### TRC-CMP-001: Request Back-Link (CRITICAL)
- Section 8 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this matrix.

#### TRC-CMP-002: Original Files (MEDIUM)
- Section 7 names the analysis briefs/normalized tables used and points at the evidence index.

## MUST NOT HAVE

- **CPT-CMP-NO-001 (CRITICAL)**: winner/loser scores, rankings, weighted totals, or a "best product" conclusion
- **CPT-CMP-NO-002 (CRITICAL)**: not_observed rendered as feature absence
- **CPT-CMP-NO-003 (CRITICAL)**: Studio vision merged with, or scored as, delivered capability
- **CPT-CMP-NO-004 (HIGH)**: two frames silently mixed in one matrix
- **CPT-CMP-NO-005 (HIGH)**: cross-product numbers compared as accuracy or quality
- **CPT-CMP-NO-006 (HIGH)**: a product decision, requirement, or commitment stated as an outcome
- **CPT-CMP-NO-007 (HIGH)**: placeholder content (TODO, TBD, FIXME)

## Validation Summary

### Final Checklist

- [ ] All MUST HAVE items checked (or marked N/A with justification)
- [ ] All MUST NOT HAVE items verified absent
- [ ] All issues documented with evidence and proposals
- [ ] `cfs validate --artifact <path>` and `check_artifact_refs.py` report PASS
- [ ] `cfs validate-toc <path>` reports PASS

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

When no issues are found, report: "COMPARISON-MATRIX semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

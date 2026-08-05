# ORIENTATION-CARD Expert Checklist

**Artifact**: ORIENTATION-CARD
**Version**: 1.0
**Purpose**: Semantic quality checklist for company orientation cards

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates ORIENTATION-CARD artifacts
- [ ] I have access to the retained extracts and fact ledger the card cites
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

An orientation card is deliberately shallow: one screen that answers "what
is this, who is it for, what is visible, and what remains unknown?" so the
requester can decide whether deeper research is worthwhile. Brevity is a
feature; the checklist enforces evidence discipline within that brevity,
not coverage breadth.

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the result: parity claim, general-knowledge fill, absence claim |
| HIGH | Undermines orientation: unlabelled source class, undated posture, missing unknowns |
| MEDIUM | Reduces usefulness: vague what-it-is, surfaces without mechanisms |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 🪪 CARD Discipline (CARD)

#### CARD-ORI-001: Orientation-Only Statement (CRITICAL)
- Section 1 visibly states this is an orientation output — not a full profile, not feature parity, not customer-outcome validation.

#### CARD-ORI-002: Required Fields Present or Unknown (HIGH)
- The card covers offering, stated target user/problem, visible product surfaces, principal documented mechanisms, visible commercial model, and source posture — each grounded or explicitly marked unknown in Section 5.

#### CARD-ORI-003: Brevity (MEDIUM)
- The card reads in one screen; anything resembling a feature inventory or facts table belongs in a profile and is flagged.

### 🔍 EVIDENCE Discipline (EVID)

#### EVID-ORI-001: Every Statement Referenced (CRITICAL)
- Every factual statement carries at least one resolvable evidence reference; at least one source and its observation date are visible.

#### EVID-ORI-002: Source Classes Labelled (HIGH)
- The wording labels source classes (third-party profile, vendor page, repository) so posture is auditable; vendor claims are named as such.

#### EVID-ORI-003: Corpus-Only Grounding (CRITICAL)
- Nothing is filled from general knowledge; every claim traces to the retained sources.

### ❓ UNKNOWNS Quality (UNK)

#### UNK-ORI-001: Substantive Unknowns (HIGH)
- Section 5 records the unknowns that matter for the go-deeper decision (commercial terms, deployment, adoption, quality), each phrased as an evidence limit.

### 🔗 TRACE Integrity (TRC)

#### TRC-ORI-001: Request Back-Link (CRITICAL)
- Section 7 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this card.

#### TRC-ORI-002: Original Files (MEDIUM)
- Section 6 names the fact ledger, retained extracts, and index locators actually used.

## MUST NOT HAVE

- **CPT-ORI-NO-001 (CRITICAL)**: feature-parity claims, complete-company-facts claims, or customer-outcome validation
- **CPT-ORI-NO-002 (CRITICAL)**: absence claims derived from missing public evidence
- **CPT-ORI-NO-003 (CRITICAL)**: claims filled from general knowledge rather than the retained sources
- **CPT-ORI-NO-004 (HIGH)**: an implementation recommendation or buy/build statement
- **CPT-ORI-NO-005 (HIGH)**: a deep feature inventory
- **CPT-ORI-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

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
- **Why it matters**: Impact on the go-deeper decision this card informs
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

When no issues are found, report: "ORIENTATION-CARD semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

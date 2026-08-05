# OSS-REVIEW Expert Checklist

**Artifact**: OSS-REVIEW
**Version**: 1.0
**Purpose**: Semantic quality checklist for open-source and alternative-implementation reviews

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates OSS-REVIEW artifacts
- [ ] I have access to the repository extracts and fact ledgers the review cites
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

The review's two questions are deliberately separate: a vendor's posture is
a product-level judgement; a repository record is a component-level one.
The most common corruption is leakage between them — a public SDK
upgrading a closed product to "open", or a core repository's licence
standing in for a managed offering's terms. not_assessed is a valid posture
when the retained set cannot establish one.

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the result: peripheral repo as core, visibility as openness, inferred deployability |
| HIGH | Undermines reuse routing: assumed licence, undated activity, missing follow-up |
| MEDIUM | Reduces usefulness: vague reuse relevance, boilerplate recommendation boundary |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 🏷️ POSTURE Discipline (POST)

#### POST-OSS-001: Posture Vocabulary and Basis (CRITICAL)
- Every offering's posture is exactly one of open-source, open-core, partly-open-source, closed-source, not_assessed — with the basis (licence, repo/product split, managed offering) and evidence.
- An offering the retained set cannot establish is not_assessed, not guessed.

#### POST-OSS-002: Posture Independence (CRITICAL)
- No repository row upgrades a vendor's posture; the managed/hosted offering's terms are never inferred from a public repository's licence.

### 📦 REPOSITORY Record Quality (REPO)

#### REPO-OSS-001: Component Scope Honesty (CRITICAL)
- Every repository's component scope is exactly one of core, connector, sdk, plugin, examples, documentation, benchmark, other — and peripheral scopes are never described in product-core terms.

#### REPO-OSS-002: Licence Evidence (HIGH)
- Every licence statement names its evidence; missing, "Other", or conflicting licence metadata is flagged as such, never assumed open.

#### REPO-OSS-003: Activity As-Of (HIGH)
- Activity signals (release/commit recency, contributors, stars) carry an as-of date; a snapshot is not a trend.

#### REPO-OSS-004: Evidence-Based Deployability (CRITICAL)
- Every deployability statement rests on documented run/self-host material for the mechanism in question — never on source visibility.

#### REPO-OSS-005: Reuse Relevance With Follow-Up (HIGH)
- Every reuse cell names the specific mechanism the repository may inform, the legal/technical follow-up needed, and why it is not a drop-in alternative.

#### REPO-OSS-006: Alternatives Beyond the Vendor Set (MEDIUM)
- Relevant alternative implementations are included even when no reviewed vendor owns them; exclusions are explained in the completeness note.

### 🎯 ROUTING Quality (ROUT)

#### ROUT-OSS-001: Recommendation Boundary (HIGH)
- Section 5 names the clearest leads and what each still needs, without making a reuse/buy/build or legal decision.

### 🔗 TRACE Integrity (TRC)

#### TRC-OSS-001: Request Back-Link (CRITICAL)
- Section 7 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this review.

#### TRC-OSS-002: Original Files (MEDIUM)
- Section 6 names the fact ledgers, retained repository extracts, and index locators actually used.

## MUST NOT HAVE

- **CPT-OSS-NO-001 (CRITICAL)**: a peripheral repository labelled or implied as the vendor product core
- **CPT-OSS-NO-002 (CRITICAL)**: repository visibility treated as evidence that the vendor product is open-source or reusable
- **CPT-OSS-NO-003 (CRITICAL)**: deployability inferred from source visibility
- **CPT-OSS-NO-004 (HIGH)**: a licence assumed where metadata is missing, "Other", or conflicting
- **CPT-OSS-NO-005 (HIGH)**: a reuse, buy/build, or legal conclusion
- **CPT-OSS-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

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
- **Why it matters**: Impact on the reuse/buy/build question this review informs
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

When no issues are found, report: "OSS-REVIEW semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

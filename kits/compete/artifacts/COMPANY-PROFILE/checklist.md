# COMPANY-PROFILE Expert Checklist

**Artifact**: COMPANY-PROFILE
**Version**: 1.0
**Purpose**: Semantic quality checklist for standard company profiles

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates COMPANY-PROFILE artifacts
- [ ] I have access to the fact ledger and retained extracts the profile cites
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

A standard profile is bounded by its retained source set: sparse evidence
produces short sections and explicit not-established rows, and that is
correct behaviour. What the checklist enforces is status discipline (fact vs
claim vs unknown), evidence per row, and the hypothesis labelling of every
borrow entry. The Studio Relevance section is evaluated against the
commissioning request's comparison frame.

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the result: absence claim, vendor claim as fact, unlabelled borrow hypothesis |
| HIGH | Undermines the assessment: undated time-sensitive fact, unevidenced row, parity conclusion |
| MEDIUM | Reduces usefulness: shallow provides-section, generic relevance, boilerplate unknowns |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 🧾 FACT Discipline (FACT)

#### FACT-PRO-001: Status Separation (CRITICAL)
- Every statement is attributable to a status: observed (with source class), vendor claim, third-party estimate, interpretation, or unknown — and the wording carries it ("YC describes…", "the vendor states…").
- The wording matches the fact ledger's claim_status where a ledger exists.

#### FACT-PRO-002: Not-Established Rows (CRITICAL)
- A fact absent from the retained set is written as "Not publicly established in the retained source set." with an explicit do-not-infer boundary — never omitted silently and never rendered as absence.

#### FACT-PRO-003: Evidence and As-Of Per Row (HIGH)
- Every facts-table row carries at least one resolvable evidence reference in its Boundary cell.
- Every time-sensitive value (team, funding, pricing, adoption, batch) carries as-of framing.

#### FACT-PRO-004: Honest Capture Statuses (HIGH)
- The Evidence Scope source-class statuses are honest: a class marked deferred that has an obvious cheap public source (e.g. a public company's finance filings) is flagged as a routing gap, and a failed/gated class names its mode.
- The time-sensitive facts the profile cites exist as ledger rows, so the next pass can diff against their as-of history.

### 🔍 ASSESSMENT Quality (ASSESS)

#### ASSESS-PRO-001: Strongest Point Is Documented (HIGH)
- Section 4 names a specific documented mechanism or position with evidence — not a general impression.

#### ASSESS-PRO-002: Weakest Boundary Is an Evidence Limit (CRITICAL)
- Section 5 states what the retained material does not establish, phrased as evidence limits; it contains no feature-absence claims.

#### ASSESS-PRO-003: Relevance Separation (HIGH)
- Section 6 keeps observed coverage separate from the requester's vision or product hypotheses, and stays inside the request's comparison frame.

### 💡 BORROW Hypothesis Discipline (BORW)

#### BORW-PRO-001: Labelled Hypothesis (CRITICAL)
- Every borrow entry: has a `bor` ID, names the motivating documented mechanism, cites its evidence, and contains the explicit not-a-commitment sentence.
- When no mechanism qualified, the section says so explicitly.

#### BORW-PRO-002: Transfer Rationale (MEDIUM)
- Each entry says why the transfer may be useful — specific enough to be evaluated, not "consider adopting X".

### 🔗 TRACE Integrity (TRC)

#### TRC-PRO-001: Request Back-Link (CRITICAL)
- Section 11 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this profile.

#### TRC-PRO-002: Original Files (MEDIUM)
- Section 10 names the fact ledger, retained extracts, and index locators actually used.

## MUST NOT HAVE

- **CPT-PRO-NO-001 (CRITICAL)**: absence claims derived from missing public evidence
- **CPT-PRO-NO-002 (CRITICAL)**: a vendor claim or third-party estimate presented as an observed fact
- **CPT-PRO-NO-003 (CRITICAL)**: a "what to borrow" statement without the hypothesis label, named mechanism, or not-a-commitment sentence
- **CPT-PRO-NO-004 (HIGH)**: a time-sensitive fact without an as-of date and evidence source
- **CPT-PRO-NO-005 (HIGH)**: feature-parity conclusions, rankings, or a buy/build recommendation
- **CPT-PRO-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

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

When no issues are found, report: "COMPANY-PROFILE semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

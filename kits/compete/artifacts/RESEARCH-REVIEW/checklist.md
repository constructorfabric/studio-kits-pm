# RESEARCH-REVIEW Expert Checklist

**Artifact**: RESEARCH-REVIEW
**Version**: 1.0
**Purpose**: Semantic quality checklist for research-run reviews

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates RESEARCH-REVIEW artifacts
- [ ] I have access to the reviewed artifacts and the check_coverage.py report
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

A RESEARCH-REVIEW audits a run's artifact set; it is the kit's
quality-loop artifact. Its failure mode is inversion: turning honest
evidence limits into artifact defects, or turning routing recommendations
into commitments. The checklist enforces that every verdict is verifiable
(named artifact, named content) and every finding is actionable (named
severity, named next pass).

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the review: unverifiable verdict, invented research content, limit-as-defect inversion |
| HIGH | Undermines the loop: unactionable finding, uncorrected coverage mis-attribution, missing follow-up |
| MEDIUM | Reduces usefulness: vague recommended pass, boilerplate findings |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 📋 CONFORMANCE Verdicts (CONF)

#### CONF-REV-001: Contract-Based Verdicts (CRITICAL)
- Every conformance row verdicts against the rules' conformance contract (plus the request's Requested output), and every commissioned flow has a row.
- Verdict vocabulary respected: met | partial | gap | not_commissioned.

#### CONF-REV-002: Verifiable Verdicts (CRITICAL)
- Every met/partial verdict names the artifact ID; every partial/gap finding names the exact missing or non-conforming content, quotable from the artifact.
- Verdicts were formed by reading the artifacts, not from the coverage report alone.

### 🗺️ COVERAGE Fidelity (COV)

#### COV-REV-001: Register-Complete (HIGH)
- Every candidate-register next action appears in Run Coverage with a status; none dropped silently.

#### COV-REV-002: Corrected Attribution (HIGH)
- Coverage rows corrected the deterministic report's name-matching where it mis-attributed; every done/partial row's fulfilling artifact is genuinely about that candidate.

### 💡 FINDINGS Quality (INF)

#### INF-REV-001: Actionable Findings (HIGH)
- Every informativeness finding carries a severity, its affected artifacts, and one concrete recommended action naming a kit workflow and subject.

#### INF-REV-002: Limit-vs-Defect Discipline (CRITICAL)
- No honestly-declared evidence limit is rendered as a conformance failure; run-level gaps are findings, artifact-level content absences are conformance verdicts, and the review keeps them apart.

#### INF-REV-003: Ordered Next Passes (MEDIUM)
- Recommended Next Passes is an ordered list translating the findings; each item names workflow + subject + what it closes.

### 🔗 TRACE Integrity (TRC)

#### TRC-REV-001: Request Back-Link (CRITICAL)
- Section 9 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this review.

## MUST NOT HAVE

- **CPT-REV-NO-001 (CRITICAL)**: new vendor claims, evidence, or research findings introduced by the review
- **CPT-REV-NO-002 (CRITICAL)**: a conformance verdict naming neither the artifact nor the exact missing content
- **CPT-REV-NO-003 (CRITICAL)**: an honestly-declared evidence limit rendered as a conformance failure
- **CPT-REV-NO-004 (HIGH)**: a recommendation phrased as a commitment, requirement, or product decision
- **CPT-REV-NO-005 (HIGH)**: a ranking or scoring of artifacts, vendors, or runs
- **CPT-REV-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

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
- **Why it matters**: Impact on the quality loop this review drives
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

When no issues are found, report: "RESEARCH-REVIEW semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

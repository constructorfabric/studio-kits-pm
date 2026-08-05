# WATCH-REPORT Expert Checklist

**Artifact**: WATCH-REPORT
**Version**: 1.0
**Purpose**: Semantic quality checklist for competitive watch reports

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates WATCH-REPORT artifacts
- [ ] I have access to the retained evidence and, for change-reports, the prior report
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

Determine the mode from the frontmatter before evaluating:

- **baseline** — the first retained observation: the Detected Changes
  section carries only the explicit baseline line, and no change language
  appears anywhere.
- **change-report** — every change row is a diff between two dated retained
  observations; a pass that detected nothing states that explicitly.

A watch is the kit's most inference-prone artifact: the temptation is to
read meaning into a change. The checklist enforces that every record stays
a dated, evidenced signal.

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the result: change claim without a prior observation, impact inference, undated record |
| HIGH | Undermines the watch: vague comparison rule, silent field carry-forward, missing prior/current pair |
| MEDIUM | Reduces usefulness: boilerplate why-it-matters, register rows without field focus |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 📡 REGISTER Quality (REG)

#### REG-WAT-001: Field Coverage (HIGH)
- Every watched field from the request appears in the register with a current dated observation, or in the completeness note when unobservable this pass.

#### REG-WAT-002: Concrete Comparison Rules (HIGH)
- Every register row's next comparison rule names the observation that would count as a material change for that field — specific enough that two analysts would agree whether a future observation triggers it.

### 🔀 CHANGE Discipline (CHG)

#### CHG-WAT-001: Baseline Honesty (CRITICAL)
- In baseline mode: the status says so, Detected Changes carries only the explicit baseline line, and no change language appears.
- In change-report mode: the status names the prior report and both observation dates.

#### CHG-WAT-002: Full Change Records (CRITICAL)
- Every change row carries the prior observation, the current observation, an ISO observed_on date, why it matters to the research question, and evidence.
- A field watched now but absent from the prior report enters the register as a baseline row, not a change.

#### CHG-WAT-003: Signal-Level Why (CRITICAL)
- Every why-it-matters cell relates the change to the research question without claiming customer, revenue, adoption, or strategic impact.

### 🔍 EVIDENCE Discipline (EVID)

#### EVID-WAT-001: Every Row Evidenced and Dated (CRITICAL)
- Every register and change row carries at least one resolvable evidence reference; every observation is dated.

### 🔗 TRACE Integrity (TRC)

#### TRC-WAT-001: Request Back-Link (CRITICAL)
- Section 8 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this report.

#### TRC-WAT-002: Prior-Report Chain (HIGH)
- A change-report's Traceability names the prior watch report it compares against, so the pass chain is walkable.

## MUST NOT HAVE

- **CPT-WAT-NO-001 (CRITICAL)**: a change claim without a prior retained observation
- **CPT-WAT-NO-002 (CRITICAL)**: customer, revenue, adoption, or strategic impact inferred from a change signal alone
- **CPT-WAT-NO-003 (CRITICAL)**: an undated observation or change record
- **CPT-WAT-NO-004 (HIGH)**: an unobserved field treated as unchanged
- **CPT-WAT-NO-005 (HIGH)**: rankings, trend scores, or momentum conclusions built on change records
- **CPT-WAT-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

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
- **Why it matters**: Impact on the change-tracking question this watch informs
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

When no issues are found, report: "WATCH-REPORT semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

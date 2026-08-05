# CANDIDATE-REGISTER Expert Checklist

**Artifact**: CANDIDATE-REGISTER
**Version**: 1.0
**Purpose**: Semantic quality checklist for candidate competitor registers

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates CANDIDATE-REGISTER artifacts
- [ ] I have access to the evidence index and fact ledgers the register cites
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

A register is a discovery-scan output: its claims are bounded to "this lead is
worth examining, for this reason". An empty register (no candidates met the
scope) is a valid outcome when the completeness note explains what was
searched. Candidate count is not a quality signal in either direction.

When a check does not apply, mark it N/A with a one-line justification instead
of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts the result: unevidenced candidate, ranking language, invented relevance |
| HIGH | Undermines routing: vague next action, classification without rationale, absence claim |
| MEDIUM | Reduces usefulness: shallow why-in-scope, boilerplate boundary |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 🧭 SCOPE Discipline (SCOPE)

#### SCOPE-REG-001: Opens With What It Is Not (HIGH)
- Section 1 opens by stating this is a discovery result, not a feature-parity or market-ranking result.
- The searched candidate space and inclusion conditions match the commissioning request's scope.

#### SCOPE-REG-002: Evidence Scope Visibility (HIGH)
- Section 2 states the evidence cutoff (ISO date), access boundary, depth, and a substantive completeness note (what was searched, known gaps).

### 🧾 CANDIDATE Quality (CAND)

#### CAND-REG-001: Evidence Per Row (CRITICAL)
- Every candidate row cites at least one evidence reference, and every reference resolves (index or fact ledger).
- The evidence actually supports the why-in-scope reason, not merely the candidate's existence.

#### CAND-REG-002: Classification Discipline (HIGH)
- Every candidate is classified baseline, direct, adjacent, or emerging, with a relationship descriptor; "baseline" is used only for the request's own target.
- The classification is justified by the why-in-scope reason, not asserted.

#### CAND-REG-003: Routable Next Action (HIGH)
- Every next action is concrete: it names what to verify, distinguish, or establish next — not a generic "research further".

#### CAND-REG-004: Screening Fidelity (MEDIUM)
- Each why-in-scope reason states the screening question the candidate answers, specific enough that a reviewer could disagree with it.

### 🔗 TRACE Integrity (TRC)

#### TRC-REG-001: Request Back-Link (CRITICAL)
- Section 6 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this register.

#### TRC-REG-002: Original Files (MEDIUM)
- Section 5 names the local selection rationale/membership sources used, and points at the evidence index for original locators.

## MUST NOT HAVE

- **CPT-REG-NO-001 (CRITICAL)**: feature scores, coverage percentages, parity conclusions, or any ranking of candidates
- **CPT-REG-NO-002 (CRITICAL)**: "confirmed competitor" language
- **CPT-REG-NO-003 (CRITICAL)**: a candidate row without a resolvable evidence reference
- **CPT-REG-NO-004 (HIGH)**: absence claims derived from missing public evidence
- **CPT-REG-NO-005 (HIGH)**: a company profile, pricing benchmark, or product decision embedded in the register
- **CPT-REG-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

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

When no issues are found, report: "CANDIDATE-REGISTER semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

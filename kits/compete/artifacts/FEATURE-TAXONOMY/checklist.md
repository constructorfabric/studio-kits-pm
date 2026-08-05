# FEATURE-TAXONOMY Expert Checklist

**Artifact**: FEATURE-TAXONOMY
**Version**: 1.0
**Purpose**: Semantic quality checklist for feature taxonomies (the apples-to-apples contract)

## Prerequisites

Before starting the review, confirm:

- [ ] I understand this checklist validates FEATURE-TAXONOMY artifacts
- [ ] I have access to the mined corpora and the mine_terms.py reports
- [ ] I will check ALL items in MUST HAVE sections
- [ ] I will verify ALL items in MUST NOT HAVE sections
- [ ] I will report only problems, with evidence and a concrete proposal

## Applicability Context

A taxonomy is the kit's anchor-bias defence: matrices inherit its rows,
so a bias here multiplies into every later comparison. The checklist
enforces that the row set is demonstrably a union (not the first
vendors' feature list), that rows are decidable (two analysts, same
cell), and that the alias map is evidence-backed rather than assumed.

When a check does not apply, mark it N/A with a one-line justification
instead of skipping silently.

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Corrupts every downstream matrix: anchored row set, dropped union rows, undecidable rows |
| HIGH | Undermines normalization: unevidenced aliases, unexplained cardinality, missing provenance |
| MEDIUM | Reduces usefulness: vague definitions, one-vendor wording in labels |
| LOW | Cosmetic or stylistic |

## MUST HAVE

### 🧬 UNION Discipline (UNION)

#### UNION-TAX-001: Every Vendor Mined First (CRITICAL)
- Section 5 lists every compared vendor with the rows its corpus first established or the explicit "no rows beyond the union" line; a vendor missing from provenance means the union cannot be verified.
- Vendors whose corpora could not be mined are named in Section 2 completeness — never silently treated as contributing nothing.

#### UNION-TAX-002: Sparse Rows Kept (CRITICAL)
- Rows evidenced in only one vendor's corpus are present; nothing in the wording treats single-source rows as second-class.

### 📐 ROW Quality (ROWS)

#### ROWS-TAX-001: Decidable Rows (CRITICAL)
- Every row's definition plus inclusion criterion is concrete enough that two analysts would fill the same matrix cell for the same evidence.

#### ROWS-TAX-002: Cardinality Band (HIGH)
- 8–20 rows per frame, or an explicit stated reason (sub-frames are the preferred fix for overshoot).

#### ROWS-TAX-003: Neutral Labels (MEDIUM)
- Row labels are domain-standard wording; no label is one vendor's product term (those belong in the alias map).

### 🔤 ALIAS Fidelity (ALIAS)

#### ALIAS-TAX-001: Verbatim, Evidenced Aliases (HIGH)
- Every alias row carries the vendor's wording verbatim and an evidence reference where the vendor uses it.
- Same-term/different-mechanism conflicts are split into distinct rows, not merged.

### 🔗 TRACE Integrity (TRC)

#### TRC-TAX-001: Request Back-Link (CRITICAL)
- Section 8 cites the commissioning RESEARCH-REQUEST ID, and that request's Traceability section back-references this taxonomy.

## MUST NOT HAVE

- **CPT-TAX-NO-001 (CRITICAL)**: a row set derived from a subset of the compared vendors
- **CPT-TAX-NO-002 (CRITICAL)**: a candidate row dropped because early-mined vendors carry no evidence for it
- **CPT-TAX-NO-003 (CRITICAL)**: row inclusion presented as a capability or availability claim
- **CPT-TAX-NO-004 (HIGH)**: an alias mapping without evidence
- **CPT-TAX-NO-005 (HIGH)**: a row set outside 8–20 rows with no stated reason
- **CPT-TAX-NO-006 (HIGH)**: placeholder content (TODO, TBD, FIXME)

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
- **Why it matters**: Impact on every matrix that will inherit these rows
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

When no issues are found, report: "FEATURE-TAXONOMY semantic review: PASS — no issues found." followed by a one-paragraph account of what was checked.

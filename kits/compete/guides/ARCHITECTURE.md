# Architecture

## Pipeline

```
natural-language research ask
  → cf-compete-request → RESEARCH-REQUEST            (Flow 1: the root)
  → evidence intake    → competitive/ evidence layer  (EVD-### index, fact ledgers, extracts)
  → cf-compete-discover → CANDIDATE-REGISTER          (Flow 2)
  → cf-compete-profile  → COMPANY-PROFILE             (Flow 4)
  → cf-compete-dossier  → COMPANY-DOSSIER             (Flow 5)
  → cf-compete-taxonomy → FEATURE-TAXONOMY            (normalization contract for Flow 6)
  → cf-compete-compare  → COMPARISON-MATRIX           (Flow 6, taxonomy-bound)
```

All nine flows ship in the current kit version; this guide describes the
architecture frame they land in.

## Two ID families, two validators

| Family | Lives in | Validated by |
|--------|----------|--------------|
| `cpt-{system}-<kind>-{slug}` — artifact identity and artifact↔artifact traceability | markdown artifacts | `cfs validate` via `constraints.toml` |
| `EVD-###`, `FACT-COMP-###-###`, `COMP-###`, `ANL-###` — domain evidence identity | TSV ledgers and extracts under `competitive/` | kit scripts (`check_evidence.py`, `check_artifact_refs.py`, from 0.2.0) |

`cfs` enforces heading outlines, ID formats, and cross-artifact coverage; it
cannot see table rows. The epistemically critical checks — every claim row
carries a resolvable evidence locator, enum vocabularies, ISO dates — are the
scripts' job, and the scripts are mandatory members of every workflow's
deterministic gate.

A third scope sits above both (from 1.7.0): `check_coverage.py` reads the
whole run — every artifact derived from one request — and reports what no
single-artifact check can see: unexecuted register next actions, per-subject
evidence density, missing fact ledgers and exports, watch freshness against
the cadence. It backs the RESEARCH-REVIEW kind (`cf-compete-review`), the
kit's quality loop: run research passes, review the run, execute the
recommended passes, re-review to measure the closure.

## Traceability backbone

RESEARCH-REQUEST is the root. Each downstream kind declares a coverage
reference back to the request's `## Traceability` section in
`constraints.toml`, and the authoring workflow appends the back-link when it
creates the artifact. The request itself has no reverse-coverage obligation: a
discovery-scan request never yields a profile, so requiring one would produce
permanent validation noise.

## Project-side layout

```
competitive/
├── evidence/index.tsv                      # canonical EVD ledger
├── evidence/extracts/YYYY-MM-DD-<slug>.md  # retained source extracts
├── companies/COMP-###-<slug>/facts.tsv     # 12-column fact ledgers
└── analyses/ANL-###-<slug>/                # analysis briefs and data
{artifacts_dir}/<KIND>/YYYY-MM-DD-<slug>.md # cpt-registered artifacts
{artifacts_dir}/<KIND>/exports/             # rendered .csv/.html views
```

## Epistemic invariants (enforced at three levels)

Every artifact:

1. displays its evidence cutoff, access boundary, depth, and completeness
   state;
2. carries a substantive negative section (Boundary / Material Unknowns /
   "what remains unestablished");
3. opens by stating what it is **not** (a register is not a feature-parity
   result; a matrix is not a ranking);
4. records missing evidence as `not_observed` / `not_assessed`, never as
   feature absence;
5. keeps observed facts, vendor claims, third-party estimates, and
   interpretations as distinct labelled statuses.

The levels: template structure (constraints.toml), PDSL omission rules with
violation codes (`rules.md`), and script checks over rows and references.

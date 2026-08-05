---
date: 2026-07-17
request: cpt-specs-req-openspec-peer-set
---

# Mechanism Study — Reviewable agent-driven specification changes


<!-- toc -->

- [1. Study Scope](#1-study-scope)
- [2. Evidence Scope](#2-evidence-scope)
- [3. Mechanism Map](#3-mechanism-map)
- [4. Comparison Fields](#4-comparison-fields)
- [5. Product Hypothesis](#5-product-hypothesis)
- [6. Boundary](#6-boundary)
- [7. Original Files](#7-original-files)
- [8. Traceability](#8-traceability)

<!-- /toc -->

**ID**: `cpt-specs-mech-reviewable-changes`
## 1. Study Scope

This study compares documented mechanisms, not broad company categories,
and produces no cost-performance or quality ranking.

The narrow question: which publicly documented mechanisms make
agent-driven specification changes reviewable by a human? Direct
change-reviewability mechanisms are separated from adjacent surfaces
(installation paths, tool directories), which appear only where they bound
a mechanism's scope.

## 2. Evidence Scope

- **Evidence cutoff**: 2026-07-17
- **Access boundary**: retained public sources only
- **Depth**: mechanism study
- **Completeness**: the OpenSpec bundle extract and the four AI-SDLC
  Framework page extracts were reviewed for analogues; the wider tool
  space was not searched in this sample run.

## 3. Mechanism Map

| Mechanism | Observed example | Direct input | Documented action | What is not established | Evidence |
| --- | --- | --- | --- | --- | --- |
| Versioned change packaging | OpenSpec | A repository's specification library and a proposed change | Wraps a change as a proposal with specification deltas, technical design, and implementation tasks; applying and archiving the package updates the specifications | Review behaviour in practice, merge-conflict handling, and any quantified review-quality result | `EVD-361`; `FACT-COMP-073-004` |
| Staged lifecycle commands | OpenSpec | The change package and the repository state | Separates the loop into explore, propose, apply, sync, and archive commands installed per tool profile, giving a human a named stage boundary before and after agent work | Depth of each stage's behaviour and whether stages can be enforced rather than skipped | `EVD-362` |
| Gated workflow orchestration | AI-SDLC Framework | Workflow definitions and specification documents | Presents a decision-engine structure with gates, orchestration, reviewer agents, and verification artefacts between workflow stages | Implemented controls versus positioning; gate execution and override behaviour | `EVD-141`; `EVD-142` |
| Machine-local work isolation | OpenSpec | A contributor's in-progress change set | Beta personal worksets are described as machine-local and neither committed nor shared, keeping unreviewed work out of the shared surface | Whether isolation integrates with a review step or merely defers sharing | `EVD-364`; `FACT-COMP-073-007` |

## 4. Comparison Fields

For each mechanism, a later comparison must record: the input artifact
processed, the packaging or gate the human reviews, the stage boundary at
which review happens, and the enforcement scope (advisory vs blocking).
These fields prevent a stage-named command list from being called a review
gate and prevent local isolation from being called a review mechanism.

## 5. Product Hypothesis

Evaluate whether combining a versioned change package (the reviewable unit)
with an enforced stage gate (the review point) would make agent-driven
specification changes auditable end to end. This is a product hypothesis
derived from the documented mechanisms above; it is not an implementation
commitment. `EVD-361`; `EVD-141`

## 6. Boundary

This study establishes which reviewability mechanisms the retained
documentation names and what each processes. Unobserved elements are
evidence limits, never absence claims; a mechanism documented by one
project and not another supports no coverage or quality conclusion, and no
benchmark or measured review-quality evidence exists in the retained set.

## 7. Original Files

- Facts: `competitive/companies/COMP-073-openspec/facts.tsv`.
- Retained extracts: `competitive/evidence/extracts/2026-07-17-openspec-source-extracts.md`,
  `competitive/evidence/extracts/2026-07-15-ai-sdlc-framework-*.md`.
- Original locators: `competitive/evidence/index.tsv`, `EVD-141`–`EVD-144`,
  `EVD-358`–`EVD-364`.

## 8. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set

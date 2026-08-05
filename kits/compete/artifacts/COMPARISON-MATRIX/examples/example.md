---
date: 2026-07-17
request: cpt-specs-req-openspec-peer-set
frame: documented specification-lifecycle stage coverage
taxonomy: cpt-specs-tax-spec-lifecycle
---

# Comparison Matrix — Specification-lifecycle stage coverage


<!-- toc -->

- [1. Comparison Frame](#1-comparison-frame)
- [2. Evidence Scope](#2-evidence-scope)
- [3. Matrix](#3-matrix)
- [4. Studio Position](#4-studio-position)
- [5. Readable Conclusion](#5-readable-conclusion)
- [6. Boundary](#6-boundary)
- [7. Original Files](#7-original-files)
- [8. Traceability](#8-traceability)

<!-- /toc -->

**ID**: `cpt-specs-cmp-lifecycle-coverage`
## 1. Comparison Frame

The question is not "which specification framework is best?". It is:
which of the frame's taxonomy features
(`cpt-specs-tax-spec-lifecycle`, ten rows) does each product's public
documentation cover, with what mechanism, and with what documented
boundary?

Compared: OpenSpec (the request's baseline, evidenced by the retained
bundle extract and fact ledger) and AI-SDLC Framework (direct
governance-oriented peer, evidenced by four retained page extracts).

Excluded: none — the register's baseline target and its one direct
candidate are both compared.

## 2. Evidence Scope

- **Evidence cutoff**: 2026-07-17
- **Access boundary**: retained public sources only
- **Depth**: comparison
- **Completeness**: two of the register's candidates are compared over
  all ten taxonomy rows (20 cells); seven cells are not_observed —
  missing retained evidence, recorded, never absence — and no cell was
  assessed by hands-on use.

## 3. Matrix

Rows are the declared taxonomy's ten features
(`cpt-specs-tax-spec-lifecycle`); every row appears for every compared
company, not_observed where the retained evidence carries nothing.

| Company / product | Feature / mechanism | Status | Availability | Observed on | Documented boundary | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| OpenSpec | Change proposal capture: the proposal artifact opens each change | substantial | current | 2026-07-17 | Execution quality and review behaviour in practice are not documented. | `EVD-361`; `FACT-COMP-073-004` |
| OpenSpec | Specification deltas | substantial | current | 2026-07-17 | Delta semantics beyond the documented artifact list are not established. | `EVD-361` |
| OpenSpec | Technical design record | substantial | current | 2026-07-17 | Depth of the design artifact in practice is not documented. | `EVD-361` |
| OpenSpec | Task decomposition | substantial | current | 2026-07-17 | Task tracking behaviour beyond the artifact list is not established. | `EVD-361` |
| OpenSpec | Change archival and spec sync | substantial | current | 2026-07-17 | Sync conflict behaviour is not documented in the retained set. | `EVD-361`; `EVD-362` |
| OpenSpec | Quality gates: the expanded-workflow "verify" command | partial | current | 2026-07-17 | Listed as a command; pass/fail semantics are not documented. | `EVD-362` |
| OpenSpec | Role-scoped agent execution | not_observed | current | 2026-07-17 | The retained extracts name no agent roles; missing retained evidence, not absence. | `EVD-361`; `EVD-362` |
| OpenSpec | Autonomy policy | not_observed | current | 2026-07-17 | No autonomy-bounding document appears in the retained extracts. | `EVD-361`; `EVD-362` |
| OpenSpec | Tool adapter surface: tool-specific skills and command files, Codex listed | substantial | current | 2026-07-17 | The 25+ tools statement is a mutable vendor count, excluded from the cell. | `EVD-362` |
| OpenSpec | Shared planning workspace: Stores (beta), Workspaces (in development) | partial | planned | 2026-07-17 | No GA state or commercial term is established. | `EVD-359`; `EVD-360` |
| AI-SDLC Framework | Change proposal capture | not_observed | current | 2026-07-15 | The four retained pages name no proposal artifact; missing retained evidence, not absence. | `EVD-141`; `EVD-142` |
| AI-SDLC Framework | Specification deltas | not_observed | current | 2026-07-15 | No spec-diff artifact appears in the retained pages. | `EVD-142` |
| AI-SDLC Framework | Technical design record | not_observed | current | 2026-07-15 | No per-change design artifact appears in the retained pages. | `EVD-141`; `EVD-142` |
| AI-SDLC Framework | Task decomposition | not_observed | current | 2026-07-15 | No task artifact appears in the retained pages. | `EVD-142` |
| AI-SDLC Framework | Change archival and spec sync | not_observed | current | 2026-07-15 | No archival/sync step appears in the retained pages. | `EVD-142` |
| AI-SDLC Framework | Quality gates: the QualityGate resource type | partial | current | 2026-07-15 | Specified in a Draft v1alpha1 document; enforcement and implementation are not established. | `EVD-142` |
| AI-SDLC Framework | Role-scoped agent execution: the AgentRole resource type | partial | current | 2026-07-15 | Draft-spec resource; delivered role behaviour is not established. | `EVD-142` |
| AI-SDLC Framework | Autonomy policy: the AutonomyPolicy resource type | partial | current | 2026-07-15 | Draft-spec resource; enforcement behaviour is not established. | `EVD-142` |
| AI-SDLC Framework | Tool adapter surface: AdapterBinding and adapter contracts | partial | current | 2026-07-15 | Adapter availability is not established from the retained pages. | `EVD-142` |
| AI-SDLC Framework | Shared planning workspace | not_observed | current | 2026-07-15 | The retained pages document no team-shared planning surface. | `EVD-141`; `EVD-142` |

## 4. Studio Position

Studio is not among the compared products in this run; this section is
intentionally not applicable. When a Studio column is added, Studio today
and Studio vision enter as separate rows with availability `current` and
`vision` respectively.

## 5. Readable Conclusion

Within the taxonomy's ten rows: OpenSpec's retained documentation covers
the change-artifact spine substantially (proposal, deltas, design,
tasks, archival/sync) with its shared-planning surface still labelled
beta/in-development, while the governance-side rows the union
contributed from the AI-SDLC corpus (agent roles, autonomy policy) are
not_observed for it. AI-SDLC Framework mirrors the shape: its draft
specification documents the governance resources (QualityGate,
AgentRole, AutonomyPolicy, AdapterBinding) at partial depth, while the
change-artifact rows are not_observed. Quality gates is the one row both
products document. The complementary pattern is the taxonomy's
anti-anchor property made visible — a row set seeded from either vendor
alone would have hidden half of this table. Any follow-up action derived
from this matrix is a product hypothesis awaiting a human decision.

## 6. Boundary

This comparison establishes documented stage coverage at the stated dates
under one frame only. not_observed cells record missing retained evidence,
never feature absence — both products' documentation sets extend beyond the
retained extracts. No cell was verified by hands-on use, and no number
published by one product is compared with another's as accuracy or quality.
Coverage under this lifecycle frame supports no claim under any other frame.

## 7. Original Files

- Register that selected the compared set: the candidate register for this
  request (see Traceability).
- Retained extracts: `competitive/evidence/extracts/2026-07-17-openspec-source-extracts.md`,
  `competitive/evidence/extracts/2026-07-15-ai-sdlc-framework-*.md`.
- Original locators: `competitive/evidence/index.tsv`, `EVD-141`–`EVD-144`,
  `EVD-358`–`EVD-364`.

## 8. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set
- Draws on: `cpt-specs-reg-openspec-peers` — Candidate Register — OpenSpec peer set; `cpt-specs-tax-spec-lifecycle` — Feature Taxonomy — Specification-lifecycle stage coverage; `cpt-specs-prof-openspec` — Company Profile — OpenSpec; `cpt-specs-dos-openspec` — Company Dossier — OpenSpec

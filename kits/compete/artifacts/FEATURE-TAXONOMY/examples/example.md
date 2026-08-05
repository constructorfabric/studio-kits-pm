---
date: 2026-07-18
frame: specification-lifecycle stage coverage
request: cpt-specs-req-openspec-peer-set
---

# Feature Taxonomy — Specification-lifecycle stage coverage


<!-- toc -->

- [1. Taxonomy Scope](#1-taxonomy-scope)
- [2. Evidence Scope](#2-evidence-scope)
- [3. Feature Rows](#3-feature-rows)
- [4. Vendor Aliases](#4-vendor-aliases)
- [5. Union Provenance](#5-union-provenance)
- [6. Boundary](#6-boundary)
- [7. Original Files](#7-original-files)
- [8. Traceability](#8-traceability)

<!-- /toc -->

**ID**: `cpt-specs-tax-spec-lifecycle`
## 1. Taxonomy Scope

This is a normalization contract, not a comparison result: it fixes the
rows later matrices compare against and maps each vendor's terminology
onto them. It scores nothing, and a row's inclusion is never a claim
that any vendor provides it.

The frame is the request's specification-lifecycle coverage. The union
was built from two mined corpora — OpenSpec (the request's baseline
target) and the AI-SDLC Framework (the register's direct lead) — plus
the requester frame from the commissioning request. Four of the ten
rows exist only in the AI-SDLC corpus: the anchor-bias check working as
intended, since a row set seeded from OpenSpec alone would never have
carried them.

## 2. Evidence Scope

- **Evidence cutoff**: 2026-07-18
- **Access boundary**: retained public sources only
- **Depth**: feature taxonomy
- **Completeness**: both compared vendors' retained corpora were mined
  (the OpenSpec bundle extract and the four AI-SDLC page extracts); the
  mine_terms.py harvest ran over the full evidence directory. No corpus
  in scope remained unmined.

## 3. Feature Rows

| Feature / scenario | Definition | Inclusion criteria | Evidence |
| --- | --- | --- | --- |
| Change proposal capture | A structured artifact opens every specification change. | The docs name a proposal-like artifact that precedes implementation. | `EVD-361` |
| Specification deltas | Changes carry explicit diffs against the specification library. | A delta/diff artifact against specs is documented, distinct from code diffs. | `EVD-361` |
| Technical design record | A per-change design document is part of the change unit. | The change unit's documented artifacts include a design record. | `EVD-361` |
| Task decomposition | The change unit decomposes into trackable implementation tasks. | A tasks artifact or task list per change is documented. | `EVD-361` |
| Change archival and spec sync | Completing a change files it and updates the specification library. | An archive/sync step that mutates the spec library is documented. | `EVD-361`; `EVD-362` |
| Quality gates | Explicit verification steps gate a change's progress. | A named gate, check, or verify step with pass/fail semantics is documented. | `EVD-142`; `EVD-362` |
| Role-scoped agent execution | Workflow steps execute under named agent roles. | The docs define agent roles as first-class workflow participants. | `EVD-142` |
| Autonomy policy | Declared limits govern what agents may do without a human. | A policy document/resource bounding autonomous action is documented. | `EVD-142` |
| Tool adapter surface | Third-party coding tools integrate through a declared surface. | The docs define adapters, profiles, or per-tool command/skill files. | `EVD-142`; `EVD-362` |
| Shared planning workspace | Planning context is shared across repositories or a team. | A team-shared or cross-repository planning surface is documented. | `EVD-359`; `EVD-360` |

## 4. Vendor Aliases

| Feature / scenario | Vendor | Vendor's term | Evidence |
| --- | --- | --- | --- |
| Change proposal capture | OpenSpec | "proposal" | `EVD-361` |
| Specification deltas | OpenSpec | "specification deltas" | `EVD-361` |
| Technical design record | OpenSpec | "technical design" | `EVD-361` |
| Task decomposition | OpenSpec | "implementation tasks" | `EVD-361` |
| Change archival and spec sync | OpenSpec | "archive" step; "sync" command | `EVD-361`; `EVD-362` |
| Quality gates | AI-SDLC Framework | "QualityGate" | `EVD-142` |
| Quality gates | OpenSpec | "verify" (expanded workflow command) | `EVD-362` |
| Role-scoped agent execution | AI-SDLC Framework | "AgentRole" | `EVD-142` |
| Autonomy policy | AI-SDLC Framework | "AutonomyPolicy" | `EVD-142` |
| Tool adapter surface | AI-SDLC Framework | "AdapterBinding" | `EVD-142` |
| Tool adapter surface | OpenSpec | "tool-specific skills and command files" | `EVD-362` |
| Shared planning workspace | OpenSpec | "Stores" (beta); "Workspaces" (in development) | `EVD-360`; `EVD-359` |

## 5. Union Provenance

| Source | Rows contributed to the union | Evidence |
| --- | --- | --- |
| OpenSpec corpus | Change proposal capture; specification deltas; technical design record; task decomposition; change archival and spec sync; shared planning workspace | `EVD-361`; `EVD-362`; `EVD-360` |
| AI-SDLC Framework corpus | Quality gates; role-scoped agent execution; autonomy policy; tool adapter surface | `EVD-142` |
| Requester frame | No rows beyond the union. | `cpt-specs-req-openspec-peer-set` |

## 6. Boundary

This taxonomy fixes comparison rows and terminology at the stated
cutoff; it establishes nothing about availability — a later matrix
decides every cell against per-vendor evidence, and four rows currently
carry evidence from only one corpus. Alias mappings are normalization
judgments recorded with their evidence, not vendor-endorsed
equivalences. The row set widens when new corpora are mined; union rows
are never dropped because a newly compared vendor's corpus arrives
without them.

## 7. Original Files

- Term harvest: `mine_terms.py --evidence-dir competitive/evidence`
  (seed report), then
  `mine_terms.py --evidence-dir competitive/evidence --taxonomy <this file>`
  (coverage report: all ten rows and twelve aliases resolve to corpus
  hits).
- Mined corpora:
  `evidence/extracts/2026-07-17-openspec-source-extracts.md`,
  `evidence/extracts/2026-07-15-ai-sdlc-framework-*.md`.
- Original locators: `competitive/evidence/index.tsv`, `EVD-142`,
  `EVD-359`–`EVD-362`.

## 8. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set

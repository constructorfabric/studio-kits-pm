---
date: 2026-07-17
mode: baseline
cadence: quarterly
request: cpt-specs-req-openspec-peer-set
---

# Watch Report — OpenSpec


<!-- toc -->

- [1. Watch Scope](#1-watch-scope)
- [2. Evidence Scope](#2-evidence-scope)
- [3. Watch Status](#3-watch-status)
- [4. Watch Register](#4-watch-register)
- [5. Detected Changes](#5-detected-changes)
- [6. Boundary](#6-boundary)
- [7. Original Files](#7-original-files)
- [8. Traceability](#8-traceability)

<!-- /toc -->

**ID**: `cpt-specs-wat-openspec-baseline`
## 1. Watch Scope

The watch covers OpenSpec's public surface at a quarterly cadence: source
posture, core lifecycle, supported-tool surface, installation boundary,
and the Workspaces/Stores maturity labels — per the commissioning request's
scope.

A change signal alone never establishes customer, revenue, or strategic
impact; this watch records dated observed changes, nothing more.

## 2. Evidence Scope

- **Evidence cutoff**: 2026-07-17
- **Access boundary**: retained public sources only
- **Depth**: watch
- **Completeness**: all watched fields were observable from the retained
  bundle extract and fact ledger in this pass.

## 3. Watch Status

This is the first retained baseline, observed on 2026-07-17. No prior
retained observation exists, so it reports no detected change.

## 4. Watch Register

| Watched field | Observation | Evidence | Next comparison rule |
| --- | --- | --- | --- |
| Source posture | Public repository is MIT-licensed (2026-07-17). | `EVD-359`; `EVD-363` | Report a changed licence, repository availability, or distribution statement. |
| Core lifecycle | Initialize, optional explore, propose, apply, archive; proposal/specification-delta/design/task artefacts (2026-07-17). | `EVD-361` | Report a changed named lifecycle step or artefact. |
| Supported-tool surface | Tool-specific skills and commands documented; Codex explicitly listed (2026-07-17). | `EVD-362` | Report a new or removed named supported-tool statement. |
| Installation boundary | Package-manager and Nix installation documented; Node.js 20.19.0+ prerequisite stated (2026-07-17). | `EVD-363` | Report a changed installation route or prerequisite. |
| Workspaces and Stores | Workspaces labelled in development; Stores beta; Git-shared planning described (2026-07-17). | `EVD-359`; `EVD-360` | Report a changed availability, collaboration, price, or support statement. |
| Personal worksets | Beta personal worksets machine-local, neither committed nor shared (2026-07-17). | `EVD-364`; `FACT-COMP-073-007` | Report a changed sharing, persistence, or maturity statement. |

## 5. Detected Changes

Baseline pass — no prior retained observation exists, so no change
detection applies.

## 6. Boundary

This pass establishes a dated baseline of OpenSpec's watched public surface
and nothing more. A later release-note, marketing, or repository signal
alone does not establish customer adoption or business impact; a field
without a current observation in a future pass will be recorded in
completeness, never inferred unchanged.

## 7. Original Files

- Facts: `competitive/companies/COMP-073-openspec/facts.tsv`.
- Retained extract: `competitive/evidence/extracts/2026-07-17-openspec-source-extracts.md`.
- Original locators: `competitive/evidence/index.tsv`, `EVD-358`–`EVD-364`.

## 8. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set

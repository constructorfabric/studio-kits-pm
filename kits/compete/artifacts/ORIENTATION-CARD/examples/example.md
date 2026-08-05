---
date: 2026-07-17
company: COMP-073-openspec
request: cpt-specs-req-openspec-peer-set
---

# Orientation Card — OpenSpec


<!-- toc -->

- [1. Evidence Scope](#1-evidence-scope)
- [2. What It Is](#2-what-it-is)
- [3. Visible Product Surfaces](#3-visible-product-surfaces)
- [4. Company and Source Posture](#4-company-and-source-posture)
- [5. Important Unknowns](#5-important-unknowns)
- [6. Original Files](#6-original-files)
- [7. Traceability](#7-traceability)

<!-- /toc -->

**ID**: `cpt-specs-ori-openspec`
## 1. Evidence Scope

This is an orientation output: not a full company profile, not a
feature-parity assessment, and not customer-outcome validation.

- **Evidence cutoff**: 2026-07-17
- **Access boundary**: retained public sources only
- **Depth**: orientation
- **Completeness**: company profile, repository, documentation, and product
  website were looked at for this short card.

## 2. What It Is

OpenSpec is an open-source, specification-driven framework with the
canonical public repository `Fission-AI/OpenSpec`, aimed at developers and
teams who want durable specification context for coding agents. The
retained evidence describes a terminal-led lifecycle — initialize,
optionally explore, propose a change, apply it, archive it — with
proposals, specification deltas, design, and tasks as the documented
change artefacts. `EVD-358`; `EVD-359`; `EVD-361`

## 3. Visible Product Surfaces

- Tool-specific skills and command files installable during
  initialization; the documented default profile includes propose,
  explore, apply, sync, and archive, and explicitly lists Codex.
  `EVD-362`
- Package-manager and Nix installation with a stated Node.js 20.19.0+
  prerequisite. `EVD-363`
- Workspaces labelled in development; Stores labelled beta with Git-shared
  planning across repositories; beta personal worksets described as
  machine-local. `EVD-359`; `EVD-360`; `EVD-364`

## 4. Company and Source Posture

The retained YC profile — a third-party profile, not a corporate-registry
record — describes a 2025 founding, Winter 2026 YC batch, Sydney location,
and founder Tabish Bidiwale (as of 2026-07-17). No public price or hosted
commercial commitment is visible in the retained set. `EVD-358`; `EVD-360`

The public repository is MIT-licensed; the licence establishes the
repository's terms, not a hosted-product posture. `EVD-359`; `EVD-363`

## 5. Important Unknowns

- Operational deployment, support terms, enterprise terms, or a
  hosted-service commitment. `EVD-359`; `EVD-363`
- Public price, customer deployments, or a customer list for
  Workspaces/Stores. `EVD-360`
- Execution and quality of the documented lifecycle, which depend on the
  chosen coding agent and user practice. `EVD-361`

## 6. Original Files

- Facts: `competitive/companies/COMP-073-openspec/facts.tsv`.
- Retained extract: `competitive/evidence/extracts/2026-07-17-openspec-source-extracts.md`.
- Original locators: `competitive/evidence/index.tsv`, `EVD-358`–`EVD-364`.

## 7. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set

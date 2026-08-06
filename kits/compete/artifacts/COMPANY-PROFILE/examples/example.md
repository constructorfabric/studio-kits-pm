---
date: 2026-07-17
company: COMP-073-openspec
request: cpt-specs-req-openspec-peer-set
---

# Company Profile — OpenSpec


<!-- toc -->

- [1. Evidence Scope](#1-evidence-scope)
- [2. Company and Commercial Facts](#2-company-and-commercial-facts)
- [3. What the Company Provides](#3-what-the-company-provides)
- [4. Strongest Documented Point](#4-strongest-documented-point)
- [5. Weakest Documented Boundary](#5-weakest-documented-boundary)
- [6. Studio Relevance](#6-studio-relevance)
- [7. What to Borrow — Product Hypothesis](#7-what-to-borrow--product-hypothesis)
  - [Versioned change package](#versioned-change-package)
- [8. Open-Source Posture](#8-open-source-posture)
- [9. Material Unknowns](#9-material-unknowns)
- [10. Original Files](#10-original-files)
- [11. Traceability](#11-traceability)

<!-- /toc -->

**ID**: `cpt-specs-prof-openspec`
## 1. Evidence Scope

This is a standard company profile, not an exhaustive deep dossier and not a
feature-parity result.

- **Evidence cutoff**: 2026-07-17
- **Access boundary**: retained public sources only
- **Depth**: standard profile
- **Source classes**: landing: captured (product website); pricing:
  deferred (no pricing surface in the retained set — Workspaces/Stores are
  preview); docs: captured; repository: captured; corporate:
  captured (YC company profile); finance: deferred (no finance filings in
  the retained set)
- **Completeness**: company identity, repository, documentation, and product
  website surfaces were reviewed; finance, adoption, and hands-on surfaces
  were not in the retained set.

## 2. Company and Commercial Facts

| Field | Observed value | Boundary |
| --- | --- | --- |
| Project identity | OpenSpec; canonical public repository `Fission-AI/OpenSpec`. | The source does not establish a legal entity or repository ownership. `EVD-359` |
| Founding and location | Founded 2025; Winter 2026 YC batch; Sydney, Australia; founder Tabish Bidiwale (as of 2026-07-17). | YC profile only; not a corporate registry or audited company record. `EVD-358`; `FACT-COMP-073-002` |
| Team, ownership, funding, revenue, valuation | Not publicly established in the retained source set. | Do not infer from repository or YC presence. `EVD-358`; `EVD-359` |
| Public pricing and commercial model | Workspaces labelled in development; Stores labelled beta (as of 2026-07-17). | No public hosted-service price, support commitment, or customer deployment is established. `EVD-360`; `FACT-COMP-073-006` |

## 3. What the Company Provides

OpenSpec documents a repository-native specification lifecycle: initialize,
explore when useful, propose, apply, and archive. The documented change
artefacts are a proposal, specification deltas, technical design, and
implementation tasks. `EVD-361`; `FACT-COMP-073-004`

Initialization can install tool-specific skills and command files; the
supported-tools guide explicitly lists Codex among the tool directory
entries. `EVD-362`; `FACT-COMP-073-005`

Installation is via package managers or Nix as `@fission-ai/openspec`, with
Node.js 20.19.0 or later stated as a prerequisite — a local developer-tool
deployment surface. `EVD-363`; `FACT-COMP-073-003`

## 4. Strongest Documented Point

The clearest documented mechanism is a portable, Git/Markdown-backed change
lifecycle with explicit proposal, specification-delta, design, task, apply,
and archive artefacts. `EVD-359`; `EVD-361`

## 5. Weakest Documented Boundary

The retained material does not establish shared-workspace maturity,
commercial terms, hosted deployment, customer adoption, or quality outcomes.
Execution quality depends on the selected coding agent and user practice.
These are evidence limits, not absence claims. `EVD-360`; `EVD-361`;
`EVD-364`

## 6. Studio Relevance

Against the request's lifecycle frame (explore → propose →
specification/design/tasks → apply → validate → sync → archive), the
observed OpenSpec surface documents explore, propose,
specification/design/tasks, apply, sync, and archive stages; a distinct
validate stage is not named in the retained extracts and remains an open
observation, not a gap claim. `EVD-361`; `EVD-362`. Any mapping of this
coverage onto the requester's own planned capabilities is a vision-side
hypothesis and stays outside this observed summary.

## 7. What to Borrow — Product Hypothesis

### Versioned change package

**ID**: `cpt-specs-bor-versioned-change-package`

Evaluate whether an explicit, versioned change package containing proposal,
specification delta, design, and tasks helps make an AI-assisted change
reviewable. This is a hypothesis derived from the documented artefact
sequence; it is not a commitment to copy OpenSpec's implementation or user
experience. `EVD-361`; `FACT-COMP-073-004`

## 8. Open-Source Posture

The public repository is MIT-licensed. This establishes the repository's
licence, not suitability for a particular commercial use or equivalence to a
hosted product. `EVD-359`; `EVD-363`

## 9. Material Unknowns

- Legal entity behind Fission-AI, team size, ownership, funding, revenue,
  and valuation.
- Commercial terms, pricing, and service commitments for the Workspaces and
  Stores surfaces.
- Independently measured adoption; the "thousands of developers and teams"
  statement is a vendor claim. `EVD-358`; `FACT-COMP-073-008`

## 10. Original Files

- Facts: `competitive/companies/COMP-073-openspec/facts.tsv`.
- Retained extract: `competitive/evidence/extracts/2026-07-17-openspec-source-extracts.md`.
- Original locators: `competitive/evidence/index.tsv`, `EVD-358`–`EVD-364`.

## 11. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set

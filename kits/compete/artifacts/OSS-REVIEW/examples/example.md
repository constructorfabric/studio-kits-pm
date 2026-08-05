---
date: 2026-07-17
request: cpt-specs-req-openspec-peer-set
---

# OSS Review — Specification-lifecycle implementations


<!-- toc -->

- [1. Review Scope](#1-review-scope)
- [2. Evidence Scope](#2-evidence-scope)
- [3. Vendor Source Posture](#3-vendor-source-posture)
- [4. Repository Review](#4-repository-review)
- [5. Recommendation Boundary](#5-recommendation-boundary)
- [6. Original Files](#6-original-files)
- [7. Traceability](#7-traceability)

<!-- /toc -->

**ID**: `cpt-specs-oss-spec-lifecycle`
## 1. Review Scope

This review answers two distinct questions: the **source posture** of each
named vendor offering, and whether potentially usable **alternative
implementations** of a specification-led change lifecycle exist. Repository
visibility does not establish that a vendor product is open-source, and an
SDK, connector, benchmark, or documentation repository is never reported as
the product core.

Reviewed set: OpenSpec and AI-SDLC Framework, the two evidenced candidates
from this request's register.

## 2. Evidence Scope

- **Evidence cutoff**: 2026-07-17
- **Access boundary**: retained public sources only
- **Depth**: open-source implementation review
- **Completeness**: two offerings assessed from retained repository and
  documentation extracts; no hands-on build or deployment was attempted,
  and the wider alternative-implementation space was not searched in this
  sample run.

## 3. Vendor Source Posture

| Offering | Source posture | Basis | Evidence |
| --- | --- | --- | --- |
| OpenSpec | open-source — MIT-licensed public project | The public repository is MIT-licensed and installable as `@fission-ai/openspec`; the team Workspaces surface is labelled in development and carries no published terms, so the posture statement covers the CLI project. | `EVD-359`; `EVD-363`; `FACT-COMP-073-003` |
| AI-SDLC Framework | open-source — Apache-2.0 badge on the public repository | The repository README's badge identifies Apache 2.0 and the license page is retained; no separate managed offering is documented in the retained set. | `EVD-141`; `EVD-144` |

## 4. Repository Review

| Repository | Component scope | Licence and activity | Deployability | Reuse relevance and follow-up | Evidence |
| --- | --- | --- | --- | --- | --- |
| `Fission-AI/OpenSpec` | core — the CLI and specification library | MIT licence stated in installation evidence (as of 2026-07-17); release/commit activity was not captured in the retained set. | Documented local install via package managers or Nix with a Node.js 20.19.0+ prerequisite; runnable as a local CLI per the getting-started guide. | Direct implementation reference for a proposal/spec-delta/design/tasks change lifecycle; operational fit, support, and the team Stores surface need separate evaluation. | `EVD-359`; `EVD-361`; `EVD-363` |
| AI-SDLC Framework repository | core — the framework specification and workflow definitions | Apache 2.0 badge on the README; license page retained (as of 2026-07-15); activity signals were not captured in the retained set. | The getting-started guide documents an entry path with stated prerequisites; runnability for a full governed workflow is not established by the retained pages. | Reference for gate/orchestration/verification workflow structure; implemented controls versus positioning is the named follow-up before any reuse conclusion. | `EVD-141`; `EVD-143`; `EVD-144` |

## 5. Recommendation Boundary

`Fission-AI/OpenSpec` is the clearest public implementation reference for a
repository-native change lifecycle; it still needs an operational-fit and
support review before any reuse conclusion. The AI-SDLC Framework
repository is a structural reference whose implemented-controls question
must be answered first. This is research routing, not a reuse, buy/build,
or legal decision.

## 6. Original Files

- Facts: `competitive/companies/COMP-073-openspec/facts.tsv`.
- Retained extracts: `competitive/evidence/extracts/2026-07-17-openspec-source-extracts.md`,
  `competitive/evidence/extracts/2026-07-15-ai-sdlc-framework-*.md`.
- Original locators: `competitive/evidence/index.tsv`, `EVD-141`–`EVD-144`,
  `EVD-358`–`EVD-364`.

## 7. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set

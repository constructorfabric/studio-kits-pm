---
date: 2026-07-17
company: COMP-073-openspec
request: cpt-specs-req-openspec-peer-set
---

# Company Dossier — OpenSpec


<!-- toc -->

- [1. Evidence Scope](#1-evidence-scope)
- [2. Product Surface](#2-product-surface)
- [3. Capability Graph](#3-capability-graph)
- [4. Documented Mechanics](#4-documented-mechanics)
- [5. Source Availability](#5-source-availability)
- [6. Users, Availability, and Commercial Boundary](#6-users-availability-and-commercial-boundary)
- [7. Dossier Conclusion](#7-dossier-conclusion)
- [8. Original Files](#8-original-files)
- [9. Traceability](#9-traceability)

<!-- /toc -->

**ID**: `cpt-specs-dos-openspec`
## 1. Evidence Scope

This dossier uses 11 retained public sources accessed 2026-07-15 to
2026-07-17. It establishes a vendor-described product and documentation
boundary, not independently verified runtime behaviour or customer outcome.
`EVD-358`–`EVD-364`

- **Evidence cutoff**: 2026-07-17
- **Access boundary**: retained public sources only
- **Depth**: deep dossier
- **Completeness**: company identity, repository, documentation, and
  product-website surfaces were examined; release notes, security and
  governance material, pricing pages, case studies, and finance/adoption
  sources were not in the retained set.

## 2. Product Surface

OpenSpec presents an open-source, spec-driven framework whose public surface
is the `Fission-AI/OpenSpec` repository, its documentation set (getting
started, installation, supported tools, CLI reference), and the
`openspec.dev` product website with a team-oriented Workspaces surface.
`EVD-359`; `EVD-360`

## 3. Capability Graph

| Offering | Capability | Documented features / mechanisms | Evidence |
| --- | --- | --- | --- |
| OpenSpec CLI | Change lifecycle | `openspec init`; propose → apply → archive loop; change artefacts: proposal, specification deltas, technical design, implementation tasks | `EVD-359`; `EVD-361` |
| OpenSpec CLI | Tool integration | Init-time installation of tool-specific skills and command files; default profile propose/explore/apply/sync/archive; expanded workflows; Codex listed | `EVD-362` |
| OpenSpec CLI | Local views | Beta personal worksets described as machine-local, not committed or shared | `EVD-364`; `FACT-COMP-073-007` |
| OpenSpec team surface | Shared planning | Workspaces labelled in development; Stores labelled beta with a Git-shared planning repository for cross-repository features | `EVD-360`; `EVD-359` |

## 4. Documented Mechanics

| Area | Documented public surface | What remains unestablished |
| --- | --- | --- |
| Change lifecycle | Starter loop and change-artefact set in the getting-started guide. `EVD-361` | Execution quality, review behaviour in practice, and any quantified token, cost, or delivery-time result. |
| Tool support | Supported-tools guide with per-tool profiles; README's 25+ tools statement is a mutable vendor claim. `EVD-362` | Verified compatibility per tool and delivery mode over time. |
| Installation | Package-manager and Nix paths for `@fission-ai/openspec`; Node.js 20.19.0+ prerequisite. `EVD-363` | Operational deployment, support, or enterprise terms. |
| Team collaboration | Workspaces "In Development" label; Stores beta with Git-shared planning. `EVD-360`; `EVD-359` | Shared-workspace maturity, hosted-SaaS offering, pricing, or a customer deployment. |
| Company and adoption | YC profile: founded 2025, Winter 2026 batch, Sydney; "thousands of developers and teams" is a vendor claim. `EVD-358`; `FACT-COMP-073-008` | Legal entity, team size, funding, revenue, valuation, and independently measured adoption. |

## 5. Source Availability

| Source class | Availability | Evidence |
| --- | --- | --- |
| Repository and documentation | public | `EVD-359`; `EVD-361`; `EVD-362`; `EVD-363`; `EVD-364` |
| Product website (Workspaces surface) | preview — labelled in development, early-access ask | `EVD-360` |
| Company profile (YC) | public | `EVD-358` |
| Pricing, security/governance, case studies, finance | unavailable — not present in the retained set | `EVD-360` |

## 6. Users, Availability, and Commercial Boundary

The retained sources do not establish a named operational user, a
role-specific workflow, a general-availability state for the team surfaces,
or any entitlement or commercial term. Public documentation availability is
not equivalent to feature availability; the Workspaces and Stores maturity
labels are the vendor's own. `EVD-359`; `EVD-360`

## 7. Dossier Conclusion

OpenSpec is a credible research subject for repository-native,
specification-led change lifecycles, tool-neutral agent integration, and
Git-backed shared planning. The retained set does not establish shared
workspace maturity, commercial terms, hosted deployment, customer adoption,
or quality outcomes. These are evidence limits, not absence claims.

## 8. Original Files

- Profile: the standard profile for this subject (see Traceability).
- Facts: `competitive/companies/COMP-073-openspec/facts.tsv`.
- Retained extract: `competitive/evidence/extracts/2026-07-17-openspec-source-extracts.md`.
- Original locators: `competitive/evidence/index.tsv`, `EVD-358`–`EVD-364`.

## 9. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set
- Expands: `cpt-specs-prof-openspec` — Company Profile — OpenSpec

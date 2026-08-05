---
date: 2026-07-18
request: cpt-specs-req-openspec-peer-set
---

# Research Review — OpenSpec peer-set run


<!-- toc -->

- [1. Review Scope](#1-review-scope)
- [2. Evidence Scope](#2-evidence-scope)
- [3. Requirements Conformance](#3-requirements-conformance)
- [4. Run Coverage](#4-run-coverage)
- [5. Informativeness Findings](#5-informativeness-findings)
- [6. Recommended Next Passes](#6-recommended-next-passes)
- [7. Boundary](#7-boundary)
- [8. Original Files](#8-original-files)
- [9. Traceability](#9-traceability)

<!-- /toc -->

**ID**: `cpt-specs-rev-openspec-run`
## 1. Review Scope

This is a review of the run's artifact set, not a new research result: it
adds no vendor claims or evidence, ranks nothing, and decides nothing —
its findings are research routing for the requester.

Under review: the nine artifacts derived from
`cpt-specs-req-openspec-peer-set` (register, orientation card, profile,
dossier, comparison matrix, OSS review, mechanism study, watch baseline),
verdicted against the kit's per-flow conformance contract and the
request's requested output, with the deterministic half backed by a
`check_coverage.py` report over the run directory.

## 2. Evidence Scope

- **Evidence cutoff**: 2026-07-18
- **Access boundary**: the run's retained artifacts and evidence index only; no live sources were consulted
- **Depth**: research review
- **Completeness**: all nine derived artifacts were read in full;
  `check_coverage.py` ran over the run directory with the sample evidence
  index and fact ledgers.

## 3. Requirements Conformance

| Flow | Required output | Artifact | Verdict | Finding |
| --- | --- | --- | --- | --- |
| Research request | Eight fields, omissions visibly "unspecified" | `cpt-specs-req-openspec-peer-set` | met | — |
| Candidate register | Classified, evidenced leads with next actions; no scores | `cpt-specs-reg-openspec-peers` | met | — |
| Orientation card | Dated, sourced what-is-it card; visibly not a profile | `cpt-specs-ori-openspec` | met | — |
| Company profile | Bounded facts, as-of dates, labelled borrow hypotheses | `cpt-specs-prof-openspec` | met | — |
| Company dossier | Source availability, capability graph, limitations | `cpt-specs-dos-openspec` | met | — |
| Comparison matrix | One frame; full per-cell contract | `cpt-specs-cmp-lifecycle-coverage` | met | — |
| OSS review | Posture separate from repository records | `cpt-specs-oss-spec-lifecycle` | met | — |
| Mechanism study | Mechanism rows with inputs, actions, unobserved elements | `cpt-specs-mech-reviewable-changes` | met | — |
| Watch report | Dated baseline register with comparison rules and cadence | `cpt-specs-wat-openspec-baseline` | met | — |

## 4. Run Coverage

| Lead | Next action | Status | Fulfilled by | Follow-up |
| --- | --- | --- | --- | --- |
| OpenSpec | Use as the lifecycle baseline for later comparison. | done | `cpt-specs-cmp-lifecycle-coverage` | — |
| AI-SDLC Framework | Establish implemented controls versus positioning via a standard profile. | open | — | Standard profile of the AI-SDLC Framework (cf-compete-profile). |

## 5. Informativeness Findings

| Finding | Severity | Affected artifacts | Recommended action |
| --- | --- | --- | --- |
| The register's one direct lead (AI-SDLC Framework) remains unprofiled, so the run's central screening question — implemented controls versus positioning — is still open. | high | `cpt-specs-reg-openspec-peers` | cf-compete-profile for the AI-SDLC Framework over `EVD-141`–`EVD-144`. |
| The AI-SDLC Framework carries no fact ledger, so a later profile or watch pass would start without as-of history for its time-sensitive statements. | medium | `cpt-specs-reg-openspec-peers` | Create the company fact ledger during the profile pass (cf-compete-intake stubs it). |
| Every watched field of the baseline rests on the 2026-07-17 extract set; the next quarterly pass needs a fresh capture or it will re-observe the baseline. | medium | `cpt-specs-wat-openspec-baseline` | cf-compete-capture + cf-compete-intake for the watched OpenSpec surfaces before 2026-10-17. |

## 6. Recommended Next Passes

1. cf-compete-profile — AI-SDLC Framework: closes the run's only open
   register action and the run's highest-severity finding.
2. cf-compete-capture + cf-compete-intake — fresh OpenSpec watch surfaces
   before 2026-10-17: feeds the first change-report watch pass.
3. cf-compete-watch — the quarterly pass over the refreshed evidence,
   in change-report mode against `cpt-specs-wat-openspec-baseline`.

## 7. Boundary

This review establishes the conformance, coverage, and informativeness of
the retained artifact set as of 2026-07-18 and nothing more. It does not
verify the underlying vendor facts, add evidence, or rank artifacts or
vendors. The open AI-SDLC action is unexecuted routing, not a defect of
the artifacts that exist, and every recommended pass is research routing
awaiting the requester's decision.

## 8. Original Files

- Coverage report: `check_coverage.py <run-dir> --evidence-dir
  competitive/evidence --companies-dir competitive/companies`
  (9/9 flows covered, 1 open next action).
- Reviewed artifacts: the run's `RESEARCH-REQUEST/`, `CANDIDATE-REGISTER/`,
  `ORIENTATION-CARD/`, `COMPANY-PROFILE/`, `COMPANY-DOSSIER/`,
  `COMPARISON-MATRIX/`, `OSS-REVIEW/`, `MECHANISM-STUDY/`,
  `WATCH-REPORT/` directories.
- Original locators: `competitive/evidence/index.tsv`.

## 9. Traceability

- Commissioned by: `cpt-specs-req-openspec-peer-set` — Research Request — OpenSpec peer set

# Quickstart

From an empty project to a reviewed opportunity and its first use case.

## 1. Install the kit

```bash
cfs kit install constructorfabric/studio-kits-pm --kit product-spec
cfs generate-agents
```

`generate-agents` projects the kit's workflows into your agent's skill list as
`cf-product-spec-opportunity`, `cf-product-spec-usecase`, and
`cf-product-spec-review`.

## 2. Register your system

Add the product you are speccing to `.cf-studio/config/artifacts.toml`:

```toml
[[systems]]
name = "MyProduct"
slug = "myproduct"
kit = "product-spec"
codebase = []
children = []
```

The `slug` becomes the `{system}` token in every ID the kit mints. Pick it once
— changing it later invalidates existing references.

## 3. Frame the problem

In the AI chat (not the shell):

```
cf-product-spec-opportunity: Support keeps getting tickets about people losing
their work when the session expires. I have the April session-timeout report
and the Q2 ticket export.
```

The workflow announces its route (6 steps, 2 questions), asks which problem it
is framing, reads the evidence you pointed at, authors the artifact, runs the
deterministic gate, and reviews itself against the checklist.

Have the evidence ready before you start. The workflow will not invent a figure
to fill a bullet — an unsourced claim becomes a visible gap instead, and with
fewer than two independent sources the Recommended Next Step becomes "validate
further" rather than "promote to PRD".

What you get: `artifacts/OPPORTUNITY/2026-08-06-session-expiry-data-loss.md`,
carrying `cpt-myproduct-opp-session-expiry-data-loss`.

## 4. Specify the first user goal

```
cf-product-spec-usecase: recover unsaved work after a session expires
```

The workflow resolves the parent opportunity, scopes the artifact to exactly one
goal (a bundled ask gets split, and you choose which goal this artifact covers),
drafts the main flow, derives an alternative flow from every step that can fail,
and writes pass/fail acceptance criteria.

Run it once per goal. Each use case cites the same opportunity.

## 5. Audit before the handoff

```
cf-product-spec-review: are these ready for the PRD?
```

The audit walks both checklists, validates every artifact deterministically, and
checks the traceability in both directions — every use case reaches an
opportunity, and every opportunity recommending promotion has at least one use
case covering it. It reports findings with severity and evidence, and applies
the fixes you approve.

## 6. Hand off to the PRD

A clean review is the handoff signal. The PRD's requirements cite the
`cpt-myproduct-usecase-*` IDs, which cite the `cpt-myproduct-opp-*` ID, which
carries the dated evidence. Solution content — screens, architecture, sizing —
starts at the PRD; this kit deliberately stops short of it.

## Commands you will actually run

```bash
cfs list-ids --kind opp                  # what has been framed
cfs list-ids --kind usecase              # what has been specified
cfs where-defined --id cpt-myproduct-opp-session-expiry-data-loss
cfs where-used --id cpt-myproduct-opp-session-expiry-data-loss
cfs validate --artifact <file>           # structure + IDs
cfs validate-toc <file>                  # table of contents
```

Everything else happens in the chat.

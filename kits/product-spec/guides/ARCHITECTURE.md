# Architecture

What the kit is made of, and where it deliberately stops.

## The chain

```
evidence (analytics, tickets, interviews, competitor observation)
  ↓  cf-product-spec-opportunity
OPPORTUNITY            cpt-{system}-opp-{slug}
  ↓  cf-product-spec-usecase   (one run per goal)
USE-CASE               cpt-{system}-usecase-{slug}   → Traceability: implements the opp ID
  ↓  cf-product-spec-review    (audit, authors nothing)
findings report
  ↓
PRD (SDLC chain)       → requirements cite the usecase and opp IDs
```

Each arrow is a link a later reader can walk backwards. Asked "why is this
requirement here?", the chain answers with a dated source rather than with an
unattributed idea.

## Layers

**Constraints** (`constraints.toml`) — the deterministic contract. It declares
each artifact kind's required heading outline and its ID template
(`cpt-{system}-opp-{slug}`, `cpt-{system}-usecase-{slug}`), plus the USE-CASE →
OPPORTUNITY reference with `coverage = false` (a use case must cite an
opportunity; an opportunity need not be covered by a use case to be valid).
`cfs validate --artifact` enforces exactly this and nothing more.

**Artifacts** (`artifacts/<KIND>/`) — four files per kind:
- `template.md` — the skeleton the workflow fills, headings matching constraints
- `rules.md` — the authoring contract: what each section must contain, the ID
  and registration rules, the ON_ERROR paths
- `checklist.md` — the semantic review, organized in categories with severities
  and an explicit MUST NOT HAVE list
- `examples/example.md` — one worked example, on a fictional product

**Workflows** (`workflows/`) — one file per flow, each generated into a
`cf-product-spec-*` skill. Every workflow carries a `## Route` block (step
count and question budget), typed user gates, a deterministic gate, and a
semantic self-review against the checklist.

**SKILL.md** — routing. It maps intent to workflow, states the kit-wide
ALWAYS/NEVER rules, and defines the progress protocol every workflow follows.

**agents-res.md** — installs as `AGENTS.md`: the condensed artifact-kind and
rules table for host agents that have not loaded the full SKILL.

## Two invariants worth stating

**The solution line.** An OPPORTUNITY names no feature, screen, or
architecture; a USE-CASE names no UI layout, API, or storage decision. This is
not stylistic — it is what keeps the artifacts reusable when the eventual
solution changes. The problem outlives the design.

**Evidence never gets manufactured.** Every evidence bullet carries a named
source and a date. Where the data does not exist, the artifact shows a visible
`{placeholder}` or records the gap, and the Recommended Next Step becomes
"validate further". A plausible invented figure is the one failure mode that
survives every downstream review, so the kit treats it as a defect rather than
a shortcut.

## Where the kit stops

No solution design, no PRD, no estimates, no roadmap, no prioritization score.
No scripts, no network access, no host tools beyond `cfs`. The kit produces two
document kinds and audits them; everything downstream belongs to the SDLC kit
that consumes the IDs.

## Refresh semantics

An artifact is refreshed in place under its existing ID — new evidence updates
the OPPORTUNITY that already carries `cpt-{system}-opp-{slug}`, it does not
create a second file with the same ID. `cfs list-ids` is the check the
workflows run before minting anything.

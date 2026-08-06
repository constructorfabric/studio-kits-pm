# Constructor Studio Product Spec Kit

The pre-PRD product layer for [Constructor Studio](https://github.com/constructorfabric/studio).
It governs the two documents a product manager writes before a PRD exists: an
evidence-backed OPPORTUNITY that frames the problem, and the USE-CASEs that
specify the user goals it implies — each precise enough to hand to the SDLC
chain, and each traceable back to the evidence that justified the work.

## Design principles

- **The opportunity is the root.** Every use case cites the OPPORTUNITY that
  justifies it, and a PRD's requirements cite both. A requirement whose chain
  does not reach an opportunity has no recorded evidence behind it.
- **Evidence or a visible gap.** Every evidence bullet carries a named source
  and a date. A missing figure stays a visible `{placeholder}` or a recorded
  evidence gap — never a plausible invention.
- **Thin evidence stops promotion.** With fewer than two independent sources,
  the Recommended Next Step is "validate further", naming how — not "promote
  to PRD".
- **The solution line holds.** An OPPORTUNITY names no feature, screen, or
  architecture; a USE-CASE names no UI layout or implementation detail. Both
  belong to the PRD and below.
- **One goal per use case.** A bundled ask splits into one artifact per goal,
  so acceptance criteria stay decidable.

## Status

Version 0.1.1 — both artifact kinds and all three workflows ship.

| Flow | Skill | Output |
|------|-------|--------|
| 1. Frame the problem | `cf-product-spec-opportunity` | OPPORTUNITY artifact |
| 2. Specify one user goal | `cf-product-spec-usecase` | USE-CASE artifact |
| 3. Audit the set (quality loop) | `cf-product-spec-review` | findings report + approved fixes applied in place |

The kit is dependency-free: no scripts, no network access, no host tools beyond
`cfs` itself.

## Install

```bash
cfs kit install constructorfabric/studio-kits-pm --kit product-spec
cfs generate-agents
```

For local development, from a clone of this repository:

```bash
cfs kit install --path <path-to-this-clone> --kit product-spec --install-mode copy
```

Then register a system in `.cf-studio/config/artifacts.toml`:

```toml
[[systems]]
name = "MyProduct"
slug = "myproduct"
kit = "product-spec"
codebase = []
children = []
```

The `slug` becomes the `{system}` token in every ID the kit mints:
`cpt-myproduct-opp-<slug>`, `cpt-myproduct-usecase-<slug>`.

## Use

Skills are invoked in the AI chat, not the shell:

```
cf-product-spec-opportunity: Field technicians keep photographing the job screen
before they leave the depot. Evidence: the April session telemetry export and
the Q2 dispatch escalation log.
```

Only `cfs …` commands run in the terminal.

## Layout

```
artifacts/<KIND>/{template.md, rules.md, checklist.md, examples/example.md}
workflows/<flow>.md         # one file per flow, generated as cf-product-spec-* skills
constraints.toml            # deterministic heading/ID contract for cfs validate
guides/                     # QUICKSTART, ARCHITECTURE
```

The bundled examples use a fictional product ("Acme Field Service"); every
figure in them is invented to show the expected shape of an artifact.

## Development

From the repository root:

- `cfs validate-kits . --kit product-spec` — kit structure + example self-checks
  (the canonical manifest lives at the repository root)
- `cfs kit normalize --dry-run . --json --kit product-spec` — manifest normalization check
- `cfs pdsl validate kits/product-spec/workflows/*.md kits/product-spec/artifacts/*/rules.md` — prompt DSL lint
- CI runs these plus TOML parsing on every PR

## License

Apache-2.0. See `LICENSE` and `NOTICE`.

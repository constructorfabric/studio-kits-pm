# Constructor Studio Competitive Analysis Kit

An evidence-first competitive-research kit for [Constructor Studio](https://github.com/constructorfabric/studio).
It implements the Competitive Landscape flows: a structured research request,
a source-backed candidate register, company profiles and deep dossiers, and a
single-frame comparison matrix — every claim carrying an evidence locator, an
observation date, and an explicit boundary.

## Design principles

- **The request is the root.** Every research artifact cites the
  RESEARCH-REQUEST that commissioned it; an omitted request field is visibly
  "unspecified", never silently defaulted.
- **Evidence or it did not happen.** Facts, vendor claims, third-party
  estimates, and unknowns are distinct statuses. Every factual statement
  resolves to an `EVD-###` evidence record with an access date.
- **Absence of evidence is not evidence of absence.** Missing public
  documentation is recorded as `not_observed` / `not_assessed`, never as
  "lacks the feature".
- **No rankings.** The kit never produces a universal market ranking, a
  winner/loser score, or an unsupported feature-parity claim, and a research
  result never auto-creates a product decision.

## Status

Version 1.13.2 — all nine epic flows, the web intake surface with
search-assisted discovery and corpus capture mode, the quality loop
(research review + coverage audit), the evidence-depth contract with the
pricing benchmark view, the feature taxonomy with matrix binding and
deck exports, and the express orchestrator with a hardened plan-approval
gate. Shipped now:

| Flow | Skill | Output |
|------|-------|--------|
| 1. Define the research request | `cf-compete-request` | RESEARCH-REQUEST artifact |
| Web capture (intake surface) | `cf-compete-capture` | claim-bounded extracts → indexed via intake |
| Evidence intake (prerequisite) | `cf-compete-intake` | `competitive/evidence/index.tsv` + normalized extracts |
| 2. Discover competitors | `cf-compete-discover` | CANDIDATE-REGISTER artifact + csv/html exports |
| 3. Orient on one company | `cf-compete-orient` | ORIENTATION-CARD artifact + html export |
| 4. Standard company profile | `cf-compete-profile` | COMPANY-PROFILE artifact + html export |
| 5. Deep company dossier | `cf-compete-dossier` | COMPANY-DOSSIER artifact + html export |
| 6. Compare selected companies | `cf-compete-compare` | COMPARISON-MATRIX artifact + csv/html exports |
| 7. Open-source & alternatives review | `cf-compete-oss-review` | OSS-REVIEW artifact + csv/html exports |
| 8. Mechanism & whitespace study | `cf-compete-mechanism` | MECHANISM-STUDY artifact + csv/html exports |
| 9. Watch for changes | `cf-compete-watch` | WATCH-REPORT artifact + csv/html exports |
| Research review (quality loop) | `cf-compete-review` | RESEARCH-REVIEW artifact + csv/html exports |
| Express run (golden path) | `cf-compete-run` | the full pipeline: one plan decision → autonomous execution → run report + review |

The capture surface optionally uses a host web-search tool for URL
discovery (query reformulation → confirmed candidates) and a host
browser-render tool (e.g. the Playwright MCP server) as the SPA fallback —
both degrade gracefully when absent; the kit itself stays dependency-free.
See `guides/CAPTURE.md`.

The kit works over **retained-evidence folders** (page extracts, fact
ledgers, analysis briefs). `cf-compete-capture` feeds that surface from
live public pages via the host agent's web-fetch tool — public sources
only, failures recorded, and the extract (not the live page) is what
research artifacts cite; see `guides/CAPTURE.md`.

## Install

```bash
cfs kit install --path <path-to-this-repo>/kits/compete --install-mode copy
cfs generate-agents
cfs validate-kits kits/compete
```

Then register a system in `.cf-studio/config/artifacts.toml`:

```toml
[[systems]]
name = "MyResearch"
slug = "myresearch"
kit = "compete"
codebase = []
children = []
```

## Use

Skills are invoked in the AI chat, not the shell:

```
cf-compete-request: Find direct, adjacent, and emerging competitors to OpenSpec. Depth: discovery scan. ...
```

Only `cfs …` commands and the `python3 scripts/…` checkers run in the
terminal.

## Layout

```
artifacts/<KIND>/{template.md, rules.md, checklist.md, examples/example.md}
workflows/<flow>.md         # one file per flow, generated as cf-compete-* skills
constraints.toml            # deterministic heading/ID contract for cfs validate
scripts/                    # stdlib-only evidence tooling and checkers
examples/sample-evidence/   # hermetic OpenSpec evidence set used by examples and CI
guides/                     # QUICKSTART, ARCHITECTURE, EVIDENCE
```

## Development

From the repository root:

- `cfs validate-kits kits/compete` — kit structure + example self-checks
- `cfs pdsl validate kits/compete/workflows/*.md kits/compete/artifacts/*/rules.md` — prompt DSL lint
- CI runs both plus TOML parsing, script compilation, and the kit's
  deterministic script checks on every PR

## License

Apache-2.0. See `LICENSE` and `NOTICE`.

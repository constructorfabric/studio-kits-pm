---
id: RAW-COMP-OPENSPEC-2026-07-17
kind: competitive-source-extract
status: active
accessed_on: 2026-07-17
purpose: Concise, claim-bounded extracts for OpenSpec; original public pages only.
---

# OpenSpec source extracts — 2026-07-17

This capture records only claims supported by the linked original pages. Counts, release information, and other mutable repository metrics are intentionally excluded from reusable observations unless separately snapshotted with an appropriate date and source.

## Company and project identity

Source: `https://www.ycombinator.com/companies/openspec`

- Y Combinator describes OpenSpec as an active Winter 2026 company, founded in 2025 and located in Sydney, Australia. It identifies Tabish Bidiwale as founder.
- YC calls OpenSpec an open-source, spec-driven framework that creates lightweight specification documents as durable context for coding agents. Its statement that the framework is used by thousands of developers and teams is a company/vendor claim, not independently measured adoption.

## Open-source CLI and workflow

Sources: `https://github.com/Fission-AI/OpenSpec`, `https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md`, and `https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md`

- The public `Fission-AI/OpenSpec` repository is MIT-licensed. Its installation guide provides package-manager and Nix installation paths for `@fission-ai/openspec` and says Node.js 20.19.0 or later is required.
- The getting-started guide separates terminal CLI commands such as `openspec init` from `/opsx:` commands used in a coding assistant's chat. Its starter loop is: install, initialize, optionally explore, propose a change, apply it, then archive it.
- The repository documents an `openspec/` directory with a specification library and a changes system. The illustrated change artifacts are a proposal, specification deltas, technical design, and implementation tasks; the archive step files the change and updates specifications.

## Tool integration and team-oriented surface

Sources: `https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md`, `https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md`, and `https://openspec.dev/`

- The supported-tools guide says `openspec init` can install tool-specific skills and command files. The default core profile includes propose, explore, apply, sync, and archive; expanded workflows add new, continue, fast-forward, verify, bulk-archive, and onboard.
- The guide explicitly lists Codex among the tool directory entries. The repository's README describes support for 25+ tools, a mutable vendor statement rather than a fixed compatibility count.
- The product website labels Workspaces as “In Development” and asks engineering teams for early access. The repository separately labels Stores beta and describes a Git-shared planning repository for cross-repository features and shared requirements. Neither page states a public price or establishes a hosted collaboration SaaS offering.
- The CLI reference describes beta personal worksets as machine-local, not committed or shared. This is a distinct local view feature and should not be conflated with the team Stores surface.

## Explicit limits for reuse

- No source captured here establishes a legal entity name for “Fission,” OpenSpec revenue, paid-workspace pricing, named customers, or payroll headcount.
- No quantified token, cost, quality, or delivery-time result is established by these extracts. Product framing about more predictable or reviewable agent output remains vendor positioning.

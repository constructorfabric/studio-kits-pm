# Quickstart

## 1. Install the kit

```bash
cfs kit install constructorfabric/studio-kits-pm --kit compete
cfs generate-agents
```

Register a system in `.cf-studio/config/artifacts.toml`:

```toml
[[systems]]
name = "MyResearch"
slug = "myresearch"
kit = "compete"
codebase = []
children = []
```

## 2a. Express: the whole pipeline in one ask

The fastest path — one plan decision, autonomous execution, an audited
result:

```
cf-compete-run: find competitors to the product described in input/vision.md
```

The orchestrator asks exactly one question (the run plan: request
fields, capture approach, depth policy, comparison frame), executes
request → capture → intake → discover → follow-ups → comparison →
review with every confirmation auto-proceeding on its recommendation
(logged), and closes with the run report and the RESEARCH-REVIEW audit.
Extend the result afterwards through the guided workflows below.

## 2. Record a research request

In the AI chat:

```
cf-compete-request: Find direct, adjacent, and emerging competitors to OpenSpec.
Decision use: select a small peer set for later evidence collection.
Depth: discovery scan. Evidence boundary: retained public sources only; cutoff 2026-07-17.
```

The workflow extracts the eight request fields, shows every omitted field as
"unspecified", and writes
`{artifacts_dir}/RESEARCH-REQUEST/{yyyy-mm-dd}-{slug}.md`.

## 3. Index the retained evidence

Evidence arrives two ways: place retained files in a folder yourself, or
capture live public pages —

```
cf-compete-capture: https://example.com/pricing https://example.com/docs
```

— which authors claim-bounded extracts into a drop folder (failures
recorded; see `guides/CAPTURE.md`) and indexes them the same way. For an
existing folder, in the AI chat:

```
cf-compete-intake: evidence-drop/openspec
```

The workflow classifies the files, plans the index update (dry-run), and —
after your confirmation — extends the append-only
`competitive/evidence/index.tsv` and verifies that every fact-ledger
`EVD-###` reference resolves. See `guides/EVIDENCE.md` for the ledger and
extract formats.

## 4. Continue the pipeline

Continue with the research flows: `cf-compete-discover`,
`cf-compete-profile`, `cf-compete-dossier`, and `cf-compete-compare`
(plus `cf-compete-taxonomy` before a matrix and `cf-compete-run` for the
express path). Each
starts from a registered RESEARCH-REQUEST and cites indexed evidence — check
with `cfs list-ids`.

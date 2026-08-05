# Demo — the end-to-end acceptance run

The kit's acceptance fixtures are the competitive-research flow examples
(nine numbered folders: `01-define-research-request` …
`09-watch-for-change`). This guide walks the shipped MVP flows against
them. Everything below was exercised as the release gate for 1.0.0.

## Setup

```bash
mkdir demo && cd demo && git init
cfs init
cfs kit install --path <path-to-this-kit-repo> --install-mode copy
cfs generate-agents
```

Register a system in `.cf-studio/config/artifacts.toml`:

```toml
[[systems]]
name = "SpecsResearch"
slug = "specs"
kit = "compete"
codebase = []
children = []
```

## 1. Record the request (fixture 01)

In the AI chat, paste fixture 01's `input.txt`:

```
cf-compete-request: Find direct, adjacent, and emerging competitors to OpenSpec. …
```

Expected: a RESEARCH-REQUEST artifact shaped like fixture 01's `output.md` —
the eight-field table, a depth-appropriate Boundary, the verbatim request
preserved, and an empty Traceability section. `cfs validate` PASS.

## 2. Index the retained evidence (fixture 02 input)

```
cf-compete-intake: <path-to-fixtures>/02-discover-competitors/input/retained-evidence
```

Expected: the extracts index into `competitive/evidence/index.tsv`
(single-page extracts keep their explicit `EVD-###`; bundle URLs get fresh
ids above any number a fact ledger already cites); the analysis brief and
the non-extract metadata page are SKIPped with reasons; unresolved
fact-ledger references are reported for manual mapping rows.
`check_evidence.py` PASS.

The dossier fixture's 15 Harness pages (flow 05, minimal `Source:` /
`Accessed:` shape) index the same way — that set is the intake stress test.

## 3. Discover competitors (fixture 02)

```
cf-compete-discover
```

Expected: a CANDIDATE-REGISTER with classified leads
(baseline/direct/adjacent/emerging), per-row evidence, and routable next
actions; the request's Traceability now back-references the register (this
is constraint-enforced — deleting the back-link makes `cfs validate`
fail). The CSV export's header matches fixture 02's `output.csv`:
`candidate,relationship,why_in_scope,evidence,next_action`.

## 4. Profile a company (fixture 04)

```
cf-compete-profile OpenSpec
```

Expected: a COMPANY-PROFILE mirroring fixture 04's sections — facts with
per-row boundaries and as-of dates, "Not publicly established in the
retained source set." for missing facts, evidence-limit phrasing for the
weakest boundary, and a labelled what-to-borrow hypothesis (`bor` ID).

## 5. Deepen into a dossier (fixture 05)

```
cf-compete-dossier Harness
```

Expected: a COMPANY-DOSSIER with the capability graph, documented mechanics
whose every row has a "what remains unestablished" cell, source
availability classes, and the closing "These are evidence limits, not
absence claims."

## 6. Compare under one frame (fixture 06)

```
cf-compete-compare
```

Expected: a COMPARISON-MATRIX with exactly one frame stated both ways, the
full per-cell contract (status / availability / observed_on / boundary /
evidence — all vocabulary-checked by `check_artifact_refs.py`), negative
findings in the conclusion, and no ranking anywhere. CSV header:
`company,feature_mechanism,status,availability,observed_on,documented_boundary,evidence`.

Fixture 06 itself uses a mechanism-lens variant
(`product,documented_mechanism,direct_input,documented_boundary,evidence`);
the kit's superset schema carries the epic's full cell contract, and the
fixture's columns map into it (mechanism → feature_mechanism, direct_input
→ part of the boundary narrative).

## What to look at afterwards

- `cfs list-ids` — the whole chain: `req` referenced by `reg`, `prof`,
  `dos`, `cmp`; `bor` hypotheses as first-class ids.
- `cfs validate` — the coverage backbone: remove any back-link from the
  request's Traceability and validation fails.
- `{artifacts_dir}/*/exports/` — deterministic, script-free HTML and CSV
  views regenerated from the canonical markdown.

## Beyond the MVP

All nine epic flows are shipped. The post-MVP flows run against their
fixtures the same way:

- **Flow 3** — `cf-compete-orient OpenSpec` (fixture 03; the sample
  evidence covers it entirely).
- **Flow 7** — `cf-compete-oss-review` (fixture 07; posture enum + per-repo
  records; the repository-review CSV is the primary export).
- **Flow 8** — `cf-compete-mechanism` (fixture 08; rows are mechanisms; the
  CSV superset adds `direct_input` and `evidence`).
- **Flow 9** — `cf-compete-watch` (fixture 09 is a baseline; the second
  pass over a fresh evidence drop produces the Detected Changes records the
  fixture's Material-change rule prescribes).

Live web capture is a future intake surface — today the kit consumes
retained-evidence folders.

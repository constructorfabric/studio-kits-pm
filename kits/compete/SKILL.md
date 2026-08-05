---
name: cf
description: "Invoke when the user asks to run competitive or market research — run the whole pipeline end to end in express mode with one upfront plan, record a structured competitive-research request, capture live public web pages as retained evidence, index retained competitive evidence into the EVD-### ledger, discover competitors into a source-backed candidate register, get a short orientation card on one company, build a standard company profile, expand it into a deep dossier, normalize a comparison frame's feature rows across vendors (apples to apples), compare selected companies under one frame, review open-source posture and reusable implementations, map documented mechanisms for a narrow whitespace question, watch a competitor for dated changes, or audit a research run's artifact set for conformance and coverage. Kit `compete` extensions — artifacts: RESEARCH-REQUEST, CANDIDATE-REGISTER, ORIENTATION-CARD, COMPANY-PROFILE, COMPANY-DOSSIER, COMPARISON-MATRIX, OSS-REVIEW, MECHANISM-STUDY, WATCH-REPORT, RESEARCH-REVIEW, FEATURE-TAXONOMY; workflows: run (express), request, capture, intake, discover, taxonomy, orient, profile, dossier, compare, oss-review, mechanism, watch, review."
---

# Constructor Studio Skill — Kit `compete`

Kit `compete` skill extensions: an evidence-first competitive-research pipeline.

## Pipeline

```
natural-language research ask
  → cf-compete-request → RESEARCH-REQUEST (eight fields; omissions visible as "unspecified")
live public pages
  → cf-compete-capture → claim-bounded extracts in a drop folder (failures recorded)
retained-evidence folder (or a capture drop)
  → cf-compete-intake → evidence ledger (EVD-### index, retained extracts, fact-ledger checks)
  → cf-compete-discover → CANDIDATE-REGISTER (classified leads + next actions; no scores)
  → cf-compete-orient → ORIENTATION-CARD (one-screen what-is-it; the go-deeper decision)
  → cf-compete-profile → COMPANY-PROFILE (facts with boundaries + labelled borrow hypotheses)
  → cf-compete-dossier → COMPANY-DOSSIER (capability graph + mechanics + source availability)
  → cf-compete-compare → COMPARISON-MATRIX (one frame; per-cell status/date/boundary/evidence)
  → cf-compete-oss-review → OSS-REVIEW (vendor posture separate from per-repo reuse records)
  → cf-compete-mechanism → MECHANISM-STUDY (rows are mechanisms; whitespace + labelled hypothesis)
  → cf-compete-watch → WATCH-REPORT (dated baseline, then dated change records; no impact claims)
the run's artifact set
  → cf-compete-review → RESEARCH-REVIEW (conformance + coverage audit; recommended next passes — the quality loop)
a comparison frame's rows
  → cf-compete-taxonomy → FEATURE-TAXONOMY (union-derived rows + vendor aliases — the apples-to-apples contract matrices inherit)
one ask, end to end
  → cf-compete-run → the whole pipeline in express mode (one run-plan decision → autonomous execution → run report + review)
```

The RESEARCH-REQUEST is the root of the traceability chain: every later
register, profile, dossier, or comparison must cite the request that
commissioned it.

## Workflows

| Skill | Type | Workflow | Output |
|-------|------|----------|--------|
| `cf-compete-request` | intake | `{workflow_request}` | RESEARCH-REQUEST artifact |
| `cf-compete-capture` | capture | `{workflow_capture}` | single-page extracts in a drop folder → indexed via intake |
| `cf-compete-intake` | indexing | `{workflow_intake}` | `competitive/evidence/index.tsv` + normalized extracts |
| `cf-compete-discover` | analysis | `{workflow_discover}` | CANDIDATE-REGISTER artifact + csv/html exports |
| `cf-compete-orient` | analysis | `{workflow_orient}` | ORIENTATION-CARD artifact + html export |
| `cf-compete-profile` | analysis | `{workflow_profile}` | COMPANY-PROFILE artifact + html export |
| `cf-compete-dossier` | analysis | `{workflow_dossier}` | COMPANY-DOSSIER artifact + html export |
| `cf-compete-compare` | synthesis | `{workflow_compare}` | COMPARISON-MATRIX artifact + csv/html exports |
| `cf-compete-oss-review` | analysis | `{workflow_oss_review}` | OSS-REVIEW artifact + csv/html exports |
| `cf-compete-mechanism` | analysis | `{workflow_mechanism}` | MECHANISM-STUDY artifact + csv/html exports |
| `cf-compete-watch` | monitoring | `{workflow_watch}` | WATCH-REPORT artifact + csv/html exports |
| `cf-compete-review` | audit | `{workflow_review}` | RESEARCH-REVIEW artifact + csv/html exports |
| `cf-compete-taxonomy` | normalization | `{workflow_taxonomy}` | FEATURE-TAXONOMY artifact + csv/html exports |
| `cf-compete-run` | orchestration | `{workflow_run}` | the full run's artifact set + run report (express mode) |

## Progress protocol

Every workflow run follows one interaction contract, so the user always
knows where they are, how many questions remain, and what a bare "1"
means:

1. **Route first.** On entering a workflow, before Step 1, announce its
   `## Route` block: the step count, the questions ahead with their
   types, and the artifact(s) the run will produce.
2. **Position with every question.** Prefix every user gate with
   `[cf-compete-<name> · step k/N · questions left: M]`.
3. **Numbered options, recommendation first.** Every gate presents
   numbered options; option 1 is always the workflow's recommendation,
   so "1" always means "proceed as recommended".
4. **Two gate types.**
   - `**user gate — decision**`: the answer shapes the research question
     itself (request fields, discovery design, comparison design, a
     narrow mechanism question, a thin-evidence trade-off). Wait for an
     explicit answer.
   - `**user gate — confirmation**`: the workflow has derived a concrete
     recommendation; state it as option 1 and proceed with it on a bare
     confirmation.
5. **Recovery never asks.** A broken environment, missing file, or
   failed validator is fixed (or honestly recorded as a failure) per the
   rules' ON_ERROR paths and reported at the next gate or checkpoint —
   never surfaced as a question of its own.
6. **Checkpoint at phase end.** After the deterministic gate and
   exports, emit a one-line checkpoint: what was produced and validated,
   what comes next.

**Express runs** (`cf-compete-run`): the guided workflows stay the
default; invoking the orchestrator is the user's choice of express mode.
A run plan is **approved only when the user answers the run-plan gate**
— a plan the agent drafted is not an approved plan, and an express run
that asked the user nothing is a protocol violation, not express mode.
Inside an approved run every confirmation gate auto-proceeds with its
option-1 recommendation (logged to the run report), every decision gate
is answered from the user-approved run plan, and only a decision the
plan does not cover surfaces as a counted exception. Express changes who
answers the questions — deterministic gates, capture policy, and the
closing RESEARCH-REVIEW audit run unchanged.

## Routing

ALWAYS route to `cf-compete-capture` WHEN intent matches:
"capture these pages", "find and capture the pricing page for <company>",
"refresh the evidence for <company> from the web", "cf-compete capture
<urls or subject>" — discovers candidate URLs by search-query
reformulation when a web-search tool is available, fetches public pages
with the host web-fetch tool (escalating to a browser-render tool such as
the Playwright MCP server when the static fetch returns only a shell),
authors claim-bounded extracts (failures recorded), and indexes them via
intake. The request's access boundary gates every fetch; public sources
only.

ALWAYS route to `cf-compete-intake` WHEN intent matches:
"index this evidence folder", "intake these retained sources",
"register the extracts and fact ledgers", "cf-compete intake <folder>" —
builds or extends the append-only `EVD-###` evidence index and verifies that
every fact-ledger reference resolves. Run it before any research flow that
must cite evidence.

ALWAYS route to `cf-compete-discover` WHEN intent matches:
"find competitors to <target>", "build the candidate register",
"who are the peers of <target>?", "discover alternatives to <target>",
"cf-compete discover" — builds the source-backed CANDIDATE-REGISTER from the
request scope and indexed evidence.

ALWAYS route to `cf-compete-orient` WHEN intent matches:
"what is <company> and what are its main features?", "quick orientation on
<company>", "is <company> worth deeper research?", "cf-compete orient
<company>" — a one-screen, evidence-bounded card for the go-deeper
decision; not a profile, not parity.

ALWAYS route to `cf-compete-profile` WHEN intent matches:
"profile <company>", "should <company> be a serious comparator?",
"make the one-page company card for <company>", "cf-compete profile
<company>" — builds the standard source-backed COMPANY-PROFILE from the
fact ledger and retained extracts.

ALWAYS route to `cf-compete-dossier` WHEN intent matches:
"deep dossier on <company>", "could <company> influence our buy/build or
positioning decision?", "expand the <company> profile with full evidence",
"cf-compete dossier <company>" — widens the examined source surface and
records what remains unestablished, area by area.

ALWAYS route to `cf-compete-compare` WHEN intent matches:
"compare <A> and <B> on <frame>", "build the coverage matrix",
"where do we stand against <companies>?", "cf-compete compare" — builds the
single-frame COMPARISON-MATRIX from profiled/evidenced companies.

ALWAYS route to `cf-compete-oss-review` WHEN intent matches:
"is <vendor> actually open-source?", "review the open-source alternatives
for <capability>", "can we reuse an existing implementation?",
"cf-compete oss-review" — vendor posture (open-source | open-core |
partly-open-source | closed-source | not_assessed) recorded separately
from per-repository reuse records; an SDK is never the product core.

ALWAYS route to `cf-compete-mechanism` WHEN intent matches:
"who detects <X>?", "map the mechanisms for <capability>", "is there
whitespace around <mechanism>?", "cf-compete mechanism" — a narrow-question
map of documented mechanisms (rows are mechanisms, not companies); any
requester direction is a labelled product hypothesis.

ALWAYS route to `cf-compete-watch` WHEN intent matches:
"set up a watch on <company>", "what changed since the last pass?",
"run the quarterly watch", "cf-compete watch <subject>" — the first pass
publishes a dated baseline; later passes publish dated change records
against the prior report. A change signal never becomes an impact claim.

ALWAYS route to `cf-compete-run` WHEN intent matches:
"just run the research for <file or target>", "find and profile the
competitors of <target>, end to end", "do the full competitive
analysis", "express run", "cf-compete run <target>" — the express
golden path: one upfront run-plan decision, autonomous execution of the
pipeline with confirmation gates auto-proceeding (logged), the closing
review as the audit. Route to the individual workflows instead when the
user wants step-by-step control.

ALWAYS route to `cf-compete-taxonomy` WHEN intent matches:
"build the feature taxonomy", "how do we compare apples to apples?",
"normalize the feature list across vendors", "the matrix rows are too
coarse / too few", "cf-compete taxonomy <frame>" — builds the
union-derived FEATURE-TAXONOMY (every compared vendor's mined inventory
plus the requester frames; 8–20 decidable rows; verbatim per-vendor
aliases; provenance audit) that later matrices compare against. Run it
before a matrix whenever no taxonomy exists for the frame.

ALWAYS route to `cf-compete-review` WHEN intent matches:
"review the research run", "how complete is the competitive research?",
"audit the artifacts against the request", "what should we research
next?", "cf-compete review" — audits the run's artifact set: conformance
verdicts per flow, register next-action coverage (deterministic
check_coverage.py report, human-confirmed), informativeness findings, and
an ordered list of recommended next passes. Never a research pass.

ALWAYS route to `cf-compete-request` WHEN intent matches:
"record a research request", "set up competitive research for <company>",
"cf-compete request <text or path>" — every competitive-research ask starts
by recording the structured request, even when the requester ultimately
wants a register, profile, or comparison.

ALWAYS run `cf-compete-request` BEFORE any research flow (`discover`,
`orient`, `profile`, `dossier`, `compare`, `oss-review`, `mechanism`,
`watch`) WHEN no RESEARCH-REQUEST is registered (check with `cfs list-ids`).

ALWAYS render an omitted request field as the literal "unspecified" — the kit
never silently defaults a field.

When routed to a workflow:
1. Read the matched workflow file and follow its steps in order.
2. Announce the workflow's `## Route` block before Step 1 and follow the
   progress protocol above for every question and checkpoint.
3. Each workflow binds the artifact KIND references (rules, template,
   checklist, example) and drives the author → deterministic-gate →
   semantic-review loop.

## Artifact kinds

| Kind | ID kinds | References |
|------|----------|------------|
| RESEARCH-REQUEST | `req` | `{research_request_rules}`, `{research_request_template}`, `{research_request_checklist}`, `{research_request_example}` |
| CANDIDATE-REGISTER | `reg` | `{candidate_register_rules}`, `{candidate_register_template}`, `{candidate_register_checklist}`, `{candidate_register_example}` |
| ORIENTATION-CARD | `ori` | `{orientation_card_rules}`, `{orientation_card_template}`, `{orientation_card_checklist}`, `{orientation_card_example}` |
| COMPANY-PROFILE | `prof`, `bor` | `{company_profile_rules}`, `{company_profile_template}`, `{company_profile_checklist}`, `{company_profile_example}` |
| COMPANY-DOSSIER | `dos` | `{company_dossier_rules}`, `{company_dossier_template}`, `{company_dossier_checklist}`, `{company_dossier_example}` |
| COMPARISON-MATRIX | `cmp` | `{comparison_matrix_rules}`, `{comparison_matrix_template}`, `{comparison_matrix_checklist}`, `{comparison_matrix_example}` |
| OSS-REVIEW | `oss` | `{oss_review_rules}`, `{oss_review_template}`, `{oss_review_checklist}`, `{oss_review_example}` |
| MECHANISM-STUDY | `mech` | `{mechanism_study_rules}`, `{mechanism_study_template}`, `{mechanism_study_checklist}`, `{mechanism_study_example}` |
| WATCH-REPORT | `wat` | `{watch_report_rules}`, `{watch_report_template}`, `{watch_report_checklist}`, `{watch_report_example}` |
| RESEARCH-REVIEW | `rev` | `{research_review_rules}`, `{research_review_template}`, `{research_review_checklist}`, `{research_review_example}` |
| FEATURE-TAXONOMY | `tax` | `{feature_taxonomy_rules}`, `{feature_taxonomy_template}`, `{feature_taxonomy_checklist}`, `{feature_taxonomy_example}` |

## Commands

- `cfs validate --artifact <file>` — deterministic structure/ID validation
- `cfs toc <file>` / `cfs validate-toc <file>` — table-of-contents generation and check
- `cfs list-ids` — list defined `cpt-*` identifiers (req)
- `cfs where-defined --id <id>` / `cfs where-used --id <id>` — trace an identifier
- `python3 {scripts}/build_evidence_index.py <folder> --evidence-dir competitive/evidence [--dry-run] [--copy-extracts]` — plan/apply an evidence-index update
- `python3 {scripts}/check_evidence.py --evidence-dir competitive/evidence --companies-dir competitive/companies` — validate the evidence layer
- `python3 {scripts}/check_artifact_refs.py <artifact> --evidence-dir competitive/evidence --companies-dir competitive/companies [--artifacts-dir <run-dir>] --lint-language` — check an artifact's evidence references and epistemic invariants (with --artifacts-dir a matrix is verified against its declared taxonomy)
- `python3 {scripts}/check_coverage.py <artifacts-dir> --evidence-dir competitive/evidence --companies-dir competitive/companies` — report the run's cross-artifact coverage (flows, next actions, evidence density, ledgers, exports, watch freshness)
- `python3 {scripts}/mine_terms.py --evidence-dir competitive/evidence [--taxonomy <artifact>]` — harvest candidate feature terms per subject (the taxonomy union's seed), or report a taxonomy's corpus coverage
- `python3 {scripts}/render_matrix_deck.py <matrix.md…> --evidence-dir competitive/evidence --mode tabs|heatmap -o <out.html>` — presentation views over the matrices: tabbed role frames or the companies × frames heatmap (script-free HTML; cells restate matrix statuses and link to sources)
- `python3 {scripts}/render_pricing.py <profile.md> [...] -o <out.csv>` — render the DEC-005 pricing benchmark CSV over the profiles' pricing/commercial rows (derived view; the profiles stay canonical)
- `python3 {scripts}/render_views.py <artifact> --format csv,html` — regenerate the derived exports (the markdown artifact is canonical)

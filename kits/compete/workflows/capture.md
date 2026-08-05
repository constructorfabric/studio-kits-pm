---
cf-studio: true
type: workflow
name: cf-compete-capture
description: Invoke when the user asks to capture live web pages as retained evidence — e.g. "capture these pages", "find and capture the pricing page for <company>", "capture <company>'s documentation" / "pull the whole docs" (corpus mode), "refresh the evidence for <company> from the web", "cf-compete capture <urls or subject>". Optionally discovers candidate URLs by search-query reformulation when the host provides a web-search tool, fetches public pages with the host web-fetch tool (escalating to a browser-render tool such as the Playwright MCP server when available and the static fetch returns only an application shell), authors claim-bounded single-page extracts, records fetch failures honestly, and hands the drop to cf-compete-intake for EVD indexing. Public sources only; the request's access boundary gates every fetch.
version: 1.2
purpose: Capture live public web pages into retained single-page extracts and index them (the web intake surface)
---

# Web Capture Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Capture + Indexing
**Role**: Evidence librarian
**Output**: single-page extracts in a drop folder → `competitive/evidence/` (index rows + normalized extracts via intake)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Capture live pages as evidence | **capture.md** | "capture these pages", `/cf-compete-capture <urls>` |
| Index an existing retained folder | **intake.md** | "index this evidence folder" |
| Run the watch over fresh evidence | **watch.md** (after capture) | "what changed since the last pass?" |

---

## Overview

Turns live public web pages into retained evidence the research flows can
cite. For each confirmed URL the workflow fetches the page with the host
web-fetch tool, authors one claim-bounded single-page extract in the
bulleted shape (`- Source:` / `- Accessed:` / `- Access:` /
`- Capture method:` preamble, `## Concise extract`, `## Intake note`), and
collects the extracts in a drop folder. The existing `cf-compete-intake`
then assigns `EVD-###` ids and verifies the ledger — capture never writes
the index itself.

Two granularities share the same contract. **Page capture** retains
named pages as single-page extracts. **Corpus capture** (deep digging)
retains a subject's documentation tree: candidate pages are enumerated
from the site's own sitemap/nav (never guessed), fetched up to the
plan's per-subject page budget, and retained as one bundle extract per
subject — the shape downstream feature mining (`cf-compete-taxonomy`)
and dossiers need, because feature inventories built from one landing
page anchor every later comparison.

Three rules govern every capture (see `guides/CAPTURE.md`):

- **The access boundary gates the fetch.** Public pages only; a gated,
  login-walled, or paywalled source is recorded as `gated`/`unavailable`
  in the index by hand — never fetched around, never summarized from
  memory.
- **Failures are evidence too.** A page that returns only an application
  shell, an error, or a block is recorded with its failure mode in the
  capture log and, when partially readable, in the extract's intake note —
  never silently skipped.
- **A page's text is the vendor's voice.** The concise extract stays
  claim-bounded: vendor statements are written as vendor statements,
  mutable counters (stars, download counts, "25+ tools") are excluded
  unless separately snapshotted with a date, and verbatim quotes are
  marked as such.

## Paths

- **Extract shapes and capture policy**: `{cf-studio-path}/config/kits/compete` guide `guides/CAPTURE.md` (and `guides/EVIDENCE.md`)
- **Index builder / checker (via intake)**: `{scripts}/build_evidence_index.py`, `{scripts}/check_evidence.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Drop folder**: `evidence-drops/{yyyy-mm-dd}-{slug}/`

## Route

6 steps → claim-bounded extracts in a drop folder, indexed via intake. Questions: 3 confirmations (Step 1: the derived capture plan; Step 3: the drop review; Step 6: closing). Steps 2, 4–5 run without questions; fetch failures are recorded, never asked about. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered and its access boundary permits public web capture (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] The host agent has a web-fetch tool available (the generated skill grants WebFetch); STOP and say so when it does not
- [ ] Optional: a web-search tool (for URL discovery) and/or a browser-render tool such as the Playwright MCP server (for SPA fallback) — both degrade gracefully when absent
- [ ] `python3` is available for the intake scripts

---

## Steps

## Step 1: Confirm the capture plan

Collect the URL list from the user, the request scope, a candidate
register's next actions, or a watch register's fields. Resolve the
commissioning RESEARCH-REQUEST and check its access boundary: only
public-source capture is supported.

**Search-assisted discovery (optional)** — WHEN the plan names a subject
but not its URLs AND the host session provides a web-search tool:
reformulate the subject and the request's decision question into 2–5
concrete search queries (the query-reformulation discovery path:
"<subject> pricing", "<subject> documentation", "<capability> open-source
implementation"), run them, and collect candidate URLs with a one-line
reason each. WHEN no web-search tool is available (the generated skill's
allowed-tools may not include one), say so and ask the user for URLs —
never guess URLs from memory.

**Corpus enumeration (corpus mode)** — WHEN the plan targets a
subject's documentation corpus rather than named pages: enumerate
candidate URLs from the site's own surfaces — `sitemap.xml`, the docs
index/navigation, the changelog index — never from memory. Rank by
information value (getting-started and concepts, feature/agent
inventories, pricing, security/enterprise, integrations, changelog;
generated API references excluded unless the request scopes them) and
cut at the plan's per-subject page budget. Pages enumerated but left
outside the budget are listed in the capture log with the cut reason —
a skipped page is visible routing, never a silent omission.

Present the plan — URLs (discovered ones marked with their query and
reason; corpus subjects with their enumerated list, budget, and
cut-list), the purpose each serves, the drop folder — and confirm
(**user gate — confirmation**).
STOP WHEN no RESEARCH-REQUEST resolves, the boundary excludes web capture,
or no web-fetch tool is available.

## Step 2: Fetch and author extracts

For each confirmed URL:
- Fetch the page with the host web-fetch tool.
- WHEN the static fetch returns only an application shell or empty content
  AND the host session provides a browser-render tool (e.g. the Playwright
  MCP server, see `guides/CAPTURE.md`): re-fetch with the render tool and
  record the escalation in the capture method — the parse-then-render
  escalation the retained fixtures themselves document. WHEN no render
  tool is available, the shell-only result is a recorded failure.
- **Corpus subjects**: author one bundle extract per subject instead of
  per-page files — front matter (`id: RAW-…`,
  `kind: competitive-source-extract`, `accessed_on`, `purpose`), one
  section per captured page or page group with its `Sources:` line(s),
  and a terminal `## Explicit limits for reuse` section; intake assigns
  one `EVD-###` per bundled URL. Claim-boundedness applies per section
  exactly as per page.
- **Named pages**: author one single-page extract in the drop folder, bulleted shape:
  `- Source:` the URL; `- Accessed:` today's ISO date; `- Access:` the
  observed access class (public page, public repository source, …);
  `- Capture method:` `host web fetch (WebFetch)`, or
  `browser render (Playwright MCP) after the static fetch returned an
  application shell` when escalated.
- Write `## Concise extract` claim-bounded: vendor claims labelled,
  mutable counters excluded, verbatim quotes marked.
- Write `## Intake note`: what the extract records and does not establish.
- On failure (application shell only with no render tool, error page,
  block, timeout): record the URL and failure mode in a capture log inside
  the drop folder; when a fallback yielded partial content, note the
  method and its limits in the intake note. Never fetch around a gate;
  never summarize from memory.

## Step 3: Review the drop

Present the authored extracts and the capture log — captured, failed (with
modes), skipped. The user reviews claim-boundedness before anything is
indexed (**user gate — confirmation**).

## Step 4: Index via intake

// turbo
Run: `python3 {scripts}/build_evidence_index.py <drop-folder> --evidence-dir competitive/evidence --copy-extracts --dry-run`
Review the plan (ADD/SKIP/UNRESOLVED), then:
// turbo
Run: `python3 {scripts}/build_evidence_index.py <drop-folder> --evidence-dir competitive/evidence --copy-extracts`

## Step 5: Verify the ledger

// turbo
Run: `python3 {scripts}/check_evidence.py --evidence-dir competitive/evidence --companies-dir competitive/companies`
Fix findings and re-run until it reports PASS.

## Step 6: Present results

Report: pages captured with their new `EVD-###` ids, failures with modes,
and gated/unavailable sources that need manual index rows. Present next
steps and wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Every fetched URL was inside the request's access boundary; nothing gated was fetched around
- [ ] Every captured page has one extract in a recognized shape with the capture method recorded
- [ ] Corpus subjects: candidate pages enumerated from the site's own surfaces, the per-subject budget respected, and every enumerated-but-cut page listed in the capture log with its reason
- [ ] Every failure is recorded with its mode; nothing was silently skipped or written from memory
- [ ] Extracts are claim-bounded: vendor claims labelled, mutable counters excluded, quotes marked
- [ ] The drop indexed via intake; `check_evidence.py` reports PASS

---

## Next Steps

- Evidence captured for a watch → `cf-compete-watch` runs the next pass over the fresh ledger
- Evidence captured for a company → `cf-compete-orient` / `cf-compete-profile` / `cf-compete-dossier`
- Corpora captured for a comparison frame → `cf-compete-taxonomy` mines the union
- A gated source matters → record it `gated` in the index and commission an authorized-access request separately

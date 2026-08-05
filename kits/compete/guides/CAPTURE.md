# Web Capture Policy

`cf-compete-capture` is the kit's live intake surface: it turns public web
pages into retained single-page extracts and hands them to
`cf-compete-intake` for `EVD-###` indexing. This guide is the policy the
workflow enforces.

## What capture is

```
confirmed URL list
  → host web fetch (WebFetch)
  → one claim-bounded single-page extract per page (drop folder)
  → cf-compete-intake: dry-run → EVD assignment → check_evidence PASS
```

Capture writes extracts; only intake writes the index. The markdown
extract — not the live page — is what research artifacts cite, so every
extract must stand on its own: source, date, access class, capture method,
bounded claims, and an intake note stating what it does not establish.

## Access boundary

- The commissioning request's access boundary gates every fetch. The kit
  supports **public sources only**.
- A gated, login-walled, or paywalled source is never fetched around and
  never summarized from memory. It is recorded by hand in
  `evidence/index.tsv` with `access` = `gated` or `unavailable`, so the
  limitation is citable; authorized access is its own, separate request.
- Respect the source: capture reads pages a person could read in a
  browser; it does not crawl, spider, or bulk-download.

## The extract contract

Capture authors the **bulleted single-page shape** (see
`guides/EVIDENCE.md` for all accepted shapes):

```markdown
# <page title> extract

- Source: https://…
- Accessed: 2026-07-29
- Access: public first-party documentation page
- Capture method: host web fetch (WebFetch)

## Concise extract
…

## Intake note
<what this extract records and does not establish>
```

Authoring rules:

- **Claim-bounded prose.** A page's text is the vendor's voice: write
  vendor statements as vendor statements ("the README describes…", "the
  pricing page states…"), never as observed fact.
- **No mutable counters.** Stars, download counts, "25+ tools", customer
  tallies are excluded unless separately snapshotted with their own date —
  the fixture practice: "counts, release information, and other mutable
  repository metrics are intentionally excluded from reusable
  observations".
- **Quotes are verbatim or absent.** Anything in quotation marks must be
  on the page exactly; paraphrase is written as paraphrase.
- **One page, one extract.** Multi-page subjects get one extract per page;
  a curated multi-page bundle (front-matter shape) is authored manually
  when a subject warrants it.

## Failures are evidence too

Live pages fail: single-page applications return only their shell, hosts
block non-browser agents, pages move. The fixture set documents exactly
this ("rendered extraction returned only the site shell … verified through
the approved fallback reader"). The rules:

- Every failure is recorded in the drop's capture log with the URL and the
  failure mode (shell-only, HTTP error, block, timeout).
- When a fallback yields partial content, the extract's `Capture method:`
  names the fallback and the intake note states what could not be read.
- A failed page is never silently skipped, and its content is never
  reconstructed from the model's memory — no retained content, no extract.

## Search-assisted URL discovery

When the capture plan names a subject but not its URLs, and the host
session provides a web-search tool, the workflow reformulates the subject
and the request's decision question into concrete search queries and
proposes candidate URLs — the query-reformulation discovery path from the
research method this kit implements. Rules:

- Every discovered URL is presented with its query and a one-line reason,
  and confirmed by the user before any fetch.
- Search results are leads to pages, never evidence themselves: nothing is
  cited until the page is captured and indexed.
- When no search tool is available, the workflow says so and asks for
  URLs; it never guesses a URL from memory.

Note on availability: cfs generates the kit skills with a fixed
`allowed-tools` list (`Bash, Read, Write, Edit, Glob, Grep, Task,
WebFetch`) — a web-search tool is not guaranteed inside the skill context.
Search may therefore need to run in the surrounding session, or the host's
permissions adjusted; the workflow degrades to user-supplied URLs either
way.

## Corpus capture: deep digging without anchor bias

Page capture answers "retain these pages"; corpus capture answers
"retain what this vendor documents" — the depth dossiers, taxonomies,
and dense matrices need. Feature inventories built from one landing page
anchor every later comparison; a mined corpus is the defence.

Policy:

- **Enumerate, never guess.** Candidate URLs come from the site's own
  surfaces — `sitemap.xml`, the documentation index/navigation, the
  changelog index. A URL that cannot be enumerated from a captured
  surface or a search result is not fetched.
- **Budget upfront.** The capture plan declares a per-subject page
  budget (an express run plan carries it as a field). Rank enumerated
  pages by information value — getting-started/concepts, feature and
  agent inventories, pricing, security/enterprise, integrations,
  changelog — and cut at the budget. Generated API references stay out
  unless the request scopes them.
- **The cut-list is visible.** Every enumerated page left outside the
  budget appears in the capture log with its cut reason; a skipped page
  is routing for the next pass, never a silent omission.
- **One bundle per subject.** Corpus retention uses the bundle extract
  shape (front matter with `id: RAW-…`, `kind:
  competitive-source-extract`, `accessed_on`, `purpose`; one section per
  page or page group with its `Sources:` line; a terminal `## Explicit
  limits for reuse`). Intake assigns one `EVD-###` per bundled URL, so
  citations stay page-precise while the corpus stays one file.
- **Same epistemics.** Claim-boundedness, per-URL failure logging, and
  the access boundary apply per section exactly as per page.

## Optional render fallback: Playwright via MCP

Some pages are single-page applications whose static fetch returns only
the site shell — the retained fixtures document exactly this failure and
its escalation ("webparser `render` after the non-rendered parse returned
an empty application root"). The kit's answer is the same escalation,
supplied by the **host**, not the kit:

- **Recommended setup**: the official Playwright MCP server, installed at
  the host level. For Claude Code:

  ```bash
  claude mcp add playwright -- npx @playwright/mcp@latest
  ```

  Other MCP-capable hosts configure the same server in their MCP settings.
- The kit itself stays dependency-free: no playwright package, no browser
  binaries, no render scripts. The capture workflow escalates to the
  render tool only WHEN the static fetch returned a shell AND the tool is
  available; otherwise the shell-only result is a recorded failure.
- An escalated capture records it verbatim in the extract:
  `Capture method: browser render (Playwright MCP) after the static fetch
  returned an application shell`.
- The same `allowed-tools` note applies: MCP tools may need host
  permission inside the generated skill context.

## What capture does not do

- **No raw verbatim copies.** The concise extract plus the index row
  (locator, date, method) is the retained record; verbatim page snapshots
  are not stored.
- **No blind rendering.** The render fallback is an escalation after a
  failed static fetch, not the default path; an unreadable page without a
  render tool is a recorded failure, never a reason to reconstruct content
  from memory.

# The Evidence Layer

Every factual statement in a kit artifact resolves to an evidence record. The
evidence layer is plain data — TSV ledgers and markdown extracts under
`competitive/` — validated by kit scripts (`cfs` validates artifact structure;
it cannot see table rows).

## Layout

```
competitive/
├── evidence/index.tsv                      # the canonical EVD ledger (append-only)
├── evidence/extracts/YYYY-MM-DD-<slug>.md  # retained source extracts
└── companies/COMP-###-<slug>/facts.tsv     # per-company fact ledgers
```

## evidence/index.tsv

One row per evidence record. Header (exact, tab-separated):

```
evd_id	locator	accessed_on	access	capture_method	retained_path	purpose
```

| Column | Meaning |
| --- | --- |
| `evd_id` | `EVD-###` — stable, append-only; never renumbered |
| `locator` | Source URL (or `-` until known) |
| `accessed_on` | ISO date the source was captured |
| `access` | `public` \| `gated` \| `unavailable` \| `planned` \| `preview` |
| `capture_method` | How the content was retained (e.g. `AnySite webparser parse`, `retained extract`) |
| `retained_path` | Path of the retained copy, relative to `evidence/` (or `-`) |
| `purpose` | Why this source is retained — what claims it bounds |

## companies/…/facts.tsv

The 12-column fact ledger. Header (exact, tab-separated):

```
fact_id	topic	offering	claim_status	statement	value	unit	observed_on	availability	confidence	evidence_refs	limitation
```

- `fact_id`: `FACT-COMP-###-###` (company number, then fact number)
- `claim_status`: `observed`, `observed_primary_source`, `observed_vendor`,
  `observed_company_statement`, `observed_third_party_profile`,
  `observed_third_party_company_profile`, `observed_investor_announcement`,
  `vendor_claim`, `research_hypothesis` — an observed fact, a vendor claim,
  and a third-party estimate are different statuses and are never merged
- `availability`: `unknown`, `current`, `planned`, `preview`, `not_assessed`,
  `open-source`, `open-core`, `partly-open-source`, `closed-source`
- `confidence`: `low` | `medium` | `high` | `unknown`
- `evidence_refs`: pipe-separated `EVD-###` tokens; every token must resolve
  in the index; at least one per fact
- `limitation`: **never empty** — every fact states what it does not
  establish

## Retained extracts

Two shapes, both accepted by the checker:

**Bundle** (one file covering several pages of one subject):

```markdown
---
id: RAW-COMP-<SLUG>-<YYYY-MM-DD>
kind: competitive-source-extract
status: active
accessed_on: 2026-07-17
purpose: Concise, claim-bounded extracts for <subject>; original public pages only.
---

# <subject> source extracts — <date>

## <topic>
Source: `https://…`
- <claim-bounded observation>

## Explicit limits for reuse
- <what these extracts do NOT establish>
```

**Single page** (one file per captured page):

```markdown
# <page title> extract

- Source: `EVD-###`
- Accessed: 2026-07-15
- Access: public first-party documentation page
- Capture method: AnySite webparser `parse`

## Concise extract
…

## Intake note
<what this extract records and does not establish>
```

**Single page, minimal** (also accepted — bare preamble lines, no sections):

```markdown
# <page title> — concise public extract

Source: https://…
Accessed: 2026-07-15; public first-party page.

<claim-bounded extract paragraph(s), including what it does not establish>
```

The minimal shape is indexed by its URL locator (the intake assigns the next
free `EVD-###`); the bulleted shape carries its `EVD-###` explicitly. Prefer
the bulleted shape for new captures — it records the capture method and
separates the extract from the intake note.

## Tooling

```bash
# plan an index update from a retained folder (nothing written)
python3 scripts/build_evidence_index.py <folder> --evidence-dir competitive/evidence --copy-extracts --dry-run

# apply it
python3 scripts/build_evidence_index.py <folder> --evidence-dir competitive/evidence --copy-extracts

# validate the whole layer
python3 scripts/check_evidence.py --evidence-dir competitive/evidence --companies-dir competitive/companies
```

`build_evidence_index.py` is the only mutating script and is append-only. It
harvests bundle URLs and explicit single-page `EVD-###` ids, assigns the next
free number to new sources (reserving numbers already cited by fact ledgers),
skips files that match neither extract shape, and reports fact-ledger
references that still resolve nowhere — those need a manual index row mapping
the id to its locator.

## Epistemic rules the checker enforces

1. Every fact carries at least one resolvable `EVD-###` reference.
2. Every fact carries a non-empty `limitation`.
3. Vocabulary columns (`claim_status`, `availability`, `confidence`,
   `access`) only take documented values.
4. Dates are ISO (`YYYY-MM-DD`); an evidence record without an access date is
   not a record.
5. A retained path must exist — the index never points at nothing.

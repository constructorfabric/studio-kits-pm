---
cf-studio: true
type: workflow
name: cf-compete-oss-review
description: Invoke when the user asks about open-source posture or reusable implementations — e.g. "is <vendor> actually open-source?", "review the open-source alternatives for <capability>", "can we reuse an existing implementation?", "cf-compete oss-review". Builds an OSS-REVIEW (Flow 7) — vendor source posture (open-source/open-core/partly-open-source/closed-source/not_assessed) recorded separately from per-repository licence, scope, deployability, activity, and reuse relevance. An SDK or docs repository is never the product core.
version: 1.0
purpose: Review open-source posture and alternative implementations (Flow 7) for a company set or capability
---

# OSS Review Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Analysis
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/OSS-REVIEW/{yyyy-mm-dd}-{slug}.md` (+ csv/html exports)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Source posture / reuse review | **oss-review.md** | "is Tessl actually open-source?", `/cf-compete-oss-review` |
| A company's full picture | **profile.md** / **dossier.md** | "profile <company>" |
| Index repository evidence first | **intake.md** | "index this evidence folder" |

---

## Overview

Produces one OSS-REVIEW artifact per run, answering two distinct questions
for a company set or capability: each vendor offering's **source posture**
(open-source | open-core | partly-open-source | closed-source |
not_assessed), and which public repositories may be evaluated as
**alternative implementations** — including ones no reviewed vendor owns.
The two judgements never leak into each other: a public SDK does not make a
closed product open, and a repository licence does not state a managed
offering's terms. The review routes follow-ups; it makes no reuse,
buy/build, or legal decision.

The workflow authors the artifact per `{oss_review_rules}` and validates it
against `{oss_review_checklist}`. Besides the artifact it only touches the
commissioning request's Traceability section (the mandatory back-link) and
the derived csv/html exports.

## Paths

- **Template**: `{oss_review_template}`
- **Rules**: `{oss_review_rules}`
- **Checklist**: `{oss_review_checklist}`
- **Example**: `{oss_review_example}`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

7 steps → OSS-REVIEW (+ csv/html exports). Questions: 2 confirmations (Step 1: the reviewed set; Step 7: closing). Steps 2–6 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] Repository evidence is indexed (licence/metadata extracts); run `cf-compete-intake` when not
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the request and the reviewed set

Identify the commissioning RESEARCH-REQUEST (`cfs list-ids`) and the
company set or capability under review. Confirm the reviewed offerings —
and whether alternative implementations outside the vendor set are in
scope — with the user (**user gate — confirmation**).
STOP WHEN no RESEARCH-REQUEST resolves.

## Step 2: Survey the repository evidence

Read the retained repository extracts, licence/metadata pages, and fact
ledgers for the reviewed set. For each offering note what the evidence
establishes about the product/repository split; for each repository note
the declared licence (flag missing, "Other", or conflicting metadata),
activity signals with dates, and any documented run/self-host material.
An offering without posture evidence will be `not_assessed`.

## Step 3: Author the OSS-REVIEW artifact

Load `{oss_review_template}` and `{oss_review_example}`. Follow
`{oss_review_rules}`:
- Resolve the OSS-REVIEW directory from `artifacts.toml`; set the path
  `{artifacts_dir}/OSS-REVIEW/{yyyy-mm-dd}-{slug}.md` and register it.
- Author Sections 1–6: the two-question scope with the
  never-equate-SDK-with-core statement; evidence scope; vendor posture
  table (enum + basis + evidence per row); repository review table
  (component scope enum, licence with evidence, dated activity,
  evidence-based deployability, reuse relevance with follow-up);
  recommendation boundary; original files.
- Set the review ID `cpt-{system}-oss-{slug}`; verify uniqueness with
  `cfs list-ids`; an existing ID means refresh mode — update the
  registered file in place, never a second file with the same ID.
- Update the commissioning request's Traceability section idempotently:
  append the back-link only when the ID is absent (replace the default
  no-derived-artifacts line when present); a refresh updates the existing
  line instead of duplicating it and collapses any duplicate lines for
  this ID left by earlier runs into one.

## Step 4: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`,
`cfs validate-toc <artifact-file>`, and
`python3 {scripts}/check_artifact_refs.py <artifact-file> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language`.
Fix and re-run until all report PASS.

## Step 5: Render the exports

// turbo
Run: `python3 {scripts}/render_views.py <artifact-file> --format csv,html`
The markdown artifact is canonical; never hand-edit the exports.

## Step 6: Semantic self-review

Load `{oss_review_checklist}` and review the artifact against it
(POST / REPO / ROUT / TRC). Apply approved fixes, then re-run Steps 4–5.

## Step 7: Present results

Summarize: each offering's posture with its basis, the repository records
with their follow-ups, and the clearest implementation leads. Present next
steps and wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Vendor posture and repository records are separate judgements; no leakage either way
- [ ] Every posture from the documented enum with basis and evidence; unknowns are not_assessed
- [ ] Every repository row: component scope from the enum, licence with evidence, dated activity, evidence-based deployability, reuse relevance with follow-up
- [ ] Recommendation boundary routes follow-ups without deciding reuse/buy/build
- [ ] The commissioning request's Traceability section back-references this review
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] csv/html exports regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Clear implementation lead → commission the named licence/architecture follow-up as its own request
- Vendor posture material to positioning → `cf-compete-profile` or `cf-compete-dossier` for that vendor
- New repository evidence → `cf-compete-intake`, then refresh this review (same oss ID)

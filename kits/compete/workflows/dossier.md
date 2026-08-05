---
cf-studio: true
type: workflow
name: cf-compete-dossier
description: Invoke when the user asks for a deep company dossier — e.g. "deep dossier on <company>", "could <company> influence our buy/build decision?", "expand the <company> profile with full evidence", "cf-compete dossier <company>". Expands the standard profile with the full retained evidence surface (Flow 5) — capability graph, documented mechanics with per-area unestablished cells, source availability classes; never inferred workflows, outcomes, or absence claims.
version: 1.0
purpose: Create a deep company dossier (Flow 5) that expands the standard profile with retained evidence and explicit limitations
---

# Company Dossier Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Analysis + Synthesis
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/COMPANY-DOSSIER/{yyyy-mm-dd}-{slug}.md` (+ html export)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Build/refresh a deep dossier | **dossier.md** | "deep dossier on Harness", `/cf-compete-dossier Harness` |
| A one-page profile is enough | **profile.md** | "should <company> be a serious comparator?" |
| Index retained evidence first | **intake.md** | "index this evidence folder" |

---

## Overview

Produces one COMPANY-DOSSIER artifact per run, for requests that may affect
buy/build, positioning, or product direction. A dossier widens the examined
source surface (landing pages, documentation, release notes, integrations,
security/governance, pricing, case studies, public finance/adoption) and
records, area by area, what the retained sources document and what remains
unestablished. The dossier informs decisions; it never makes them.

The workflow authors the artifact per `{company_dossier_rules}` and
validates it against `{company_dossier_checklist}`. Besides the artifact it
only touches the commissioning request's Traceability section (the
mandatory back-link) and the derived html export.

## Paths

- **Template**: `{company_dossier_template}`
- **Rules**: `{company_dossier_rules}`
- **Checklist**: `{company_dossier_checklist}`
- **Example**: `{company_dossier_example}`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/COMP-###-<slug>/facts.tsv`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

7 steps → COMPANY-DOSSIER (+ html export). Questions: 1 confirmation (Step 1: the resolved subject), 1 decision (Step 2: proceed on a thin evidence set or widen it first), 1 closing confirmation (Step 7). Steps 3–6 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] The subject's evidence is indexed at corpus depth (run `cf-compete-capture` in corpus mode when only key pages exist); a dossier over a thin set mostly records limitations
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the request, subject, and profile

Identify the commissioning RESEARCH-REQUEST (`cfs list-ids`) and the exact
subject (platform vs single offering — ask when ambiguous). Resolve the
subject's COMPANY-PROFILE when one exists; a dossier expands it but may be
commissioned directly. Confirm with the user (**user gate — confirmation**).
STOP WHEN no RESEARCH-REQUEST resolves.

## Step 2: Inventory the evidence surface

List the retained extracts and fact-ledger rows for the subject, grouped by
source class (landing, docs, release notes, integrations,
security/governance, pricing, case studies, finance/adoption). Present the
inventory — covered and uncovered classes — and confirm scope with the user
(**user gate — decision**). When the set is thin, say so and offer: proceed (the
dossier will mostly record limitations), intake more evidence first, or
produce a standard profile instead.

## Step 3: Author the COMPANY-DOSSIER artifact

Load `{company_dossier_template}` and `{company_dossier_example}`. Follow
`{company_dossier_rules}`:
- Resolve the COMPANY-DOSSIER directory from `artifacts.toml`; set the path
  `{artifacts_dir}/COMPANY-DOSSIER/{yyyy-mm-dd}-{slug}.md` and register it.
- Author Sections 1–8: evidence scope with the vendor-described-boundary
  statement; product surface; capability graph (evidence per row);
  documented mechanics with the mandatory per-area unestablished cells;
  source availability (public | gated | unavailable | planned | preview);
  users/availability/commercial boundary; the two-sided conclusion ending
  with the evidence-limits-not-absence-claims sentence; original files.
- Set the dossier ID `cpt-{system}-dos-{slug}`; verify uniqueness with
  `cfs list-ids`.
- Append the back-link to the commissioning request's Traceability section
  (replace its default no-derived-artifacts line when present).

## Step 4: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`,
`cfs validate-toc <artifact-file>`, and
`python3 {scripts}/check_artifact_refs.py <artifact-file> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language`.
Fix and re-run until all report PASS.

## Step 5: Render the export

// turbo
Run: `python3 {scripts}/render_views.py <artifact-file> --format html`
The markdown artifact is canonical; never hand-edit the export.

## Step 6: Semantic self-review

Load `{company_dossier_checklist}` and review the artifact against it
(EVSC / MECH / AVAIL / CONC / TRC). Apply approved fixes, then re-run
Steps 4–5.

## Step 7: Present results

Summarize: the source classes covered, the capability graph, the material
unestablished areas, and the two-sided conclusion. Present next steps and
wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Evidence Scope states the source inventory and the vendor-described-boundary statement
- [ ] Every Documented Mechanics row has a substantive what-remains-unestablished cell
- [ ] Source Availability uses the exact vocabulary (public | gated | unavailable | planned | preview), evidenced per row, and covers the standard classes (documentation, pricing, finance/adoption) even when uncaptured
- [ ] Newly observed time-sensitive facts extended into the company fact ledger
- [ ] Conclusion is two-sided and ends with the evidence-limits-not-absence-claims sentence
- [ ] The commissioning request's Traceability section back-references this dossier
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] html export regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- ≥2 companies evidenced at profile/dossier depth → single-frame comparison (arrives with the COMPARISON-MATRIX kind)
- Material unestablished areas → commission a narrower request (hands-on evaluation, gated access) and re-run
- New evidence drop → `cf-compete-intake`, then refresh this dossier (same dos ID)

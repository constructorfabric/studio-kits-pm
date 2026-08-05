---
cf-studio: true
type: workflow
name: cf-compete-profile
description: Invoke when the user asks for a standard company profile — e.g. "profile <company>", "should <company> be a serious comparator?", "make the one-page company card for <company>", "cf-compete profile <company>". Builds a source-backed COMPANY-PROFILE (Flow 4) from the request, the company's fact ledger, and retained extracts — commercial facts with boundaries, product surface, assessment, labelled borrow hypotheses; never parity conclusions or rankings.
version: 1.0
purpose: Create a standard source-backed company profile (Flow 4) from a research request and indexed evidence
---

# Company Profile Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Analysis + Synthesis
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/COMPANY-PROFILE/{yyyy-mm-dd}-{slug}.md` (+ html export)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Build/refresh a standard company profile | **profile.md** | "profile OpenSpec", `/cf-compete-profile OpenSpec` |
| Discover the candidate set first | **discover.md** | "find competitors to <target>" |
| Index retained evidence first | **intake.md** | "index this evidence folder" |

---

## Overview

Produces one COMPANY-PROFILE artifact per run: the consistent one-page view
a Product Manager uses to judge whether a company is a serious comparator
and which documented mechanisms may be relevant. Facts, vendor claims,
third-party estimates, interpretation, and unknowns stay distinct; missing
public evidence is written as not-established, never as absence; every
"what to borrow" entry is a labelled product hypothesis.

The workflow authors the artifact per `{company_profile_rules}` and
validates it against `{company_profile_checklist}`. Besides the artifact it
only touches the commissioning request's Traceability section (the
mandatory back-link) and the derived html export.

## Paths

- **Template**: `{company_profile_template}`
- **Rules**: `{company_profile_rules}`
- **Checklist**: `{company_profile_checklist}`
- **Example**: `{company_profile_example}`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/COMP-###-<slug>/facts.tsv`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

8 steps → COMPANY-PROFILE (+ html export) and the company fact ledger. Questions: 2 confirmations (Step 1: the resolved company; Step 8: closing). Steps 2–7 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] Company evidence is indexed: retained extracts and, ideally, a fact ledger; run `cf-compete-intake` when not
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the request and the company

Identify the commissioning RESEARCH-REQUEST (`cfs list-ids`) and the exact
offering to profile (company vs product vs repository — ask when ambiguous).
Confirm both with the user (**user gate — confirmation**).
STOP WHEN no RESEARCH-REQUEST resolves.

## Step 2: Survey the company evidence

Read the company's fact ledger when one exists — its claim_status labels
drive the observed-vs-vendor-claim wording — and the retained extracts in
scope. Assign every standard source class (landing, pricing, docs,
repository, corporate/finance) its capture status: captured, failed (with
mode), gated, or deferred (with reason) — a cheap-to-capture deferred
class is a routing signal, not a shrug. That inventory becomes the
Evidence Scope source-class line, the completeness note, and the Material
Unknowns section. Open nothing outside the request's access boundary.

## Step 3: Record time-sensitive facts in the company ledger

Create `competitive/companies/COMP-###-{slug}/facts.tsv` when the company
carries none (next free COMP number), and append one row per
time-sensitive observation the profile will cite — pricing figures,
promotional terms, maturity labels, funding events — with claim_status,
observed_on, evidence_refs, and a non-empty limitation. The ledger is what
gives the next quarterly pass its as-of history; a profile without one
leaves the watch nothing to diff.
// turbo
Run: `python3 {scripts}/check_evidence.py --evidence-dir competitive/evidence --companies-dir competitive/companies`
Fix findings before authoring.

## Step 4: Author the COMPANY-PROFILE artifact

Load `{company_profile_template}` and `{company_profile_example}`. Follow
`{company_profile_rules}`:
- Resolve the COMPANY-PROFILE directory from `artifacts.toml`; set the path
  `{artifacts_dir}/COMPANY-PROFILE/{yyyy-mm-dd}-{slug}.md` and register it.
- Author Sections 1–10: evidence scope (including the source-class capture
  statuses); the facts table (not-established
  rows explicit, as-of framing, evidence per row); offerings → capabilities
  → features; strongest point; weakest boundary as evidence limits; Studio
  relevance against the request's frame; labelled borrow hypotheses with
  `cpt-{system}-bor-*` IDs; open-source posture; material unknowns;
  original files.
- Set the profile ID `cpt-{system}-prof-{slug}`; verify uniqueness with
  `cfs list-ids`; an existing ID means refresh mode — update the
  registered file in place, never a second file with the same ID.
- Update the commissioning request's Traceability section idempotently:
  append the back-link only when the ID is absent (replace the default
  no-derived-artifacts line when present); a refresh updates the existing
  line instead of duplicating it.

## Step 5: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`,
`cfs validate-toc <artifact-file>`, and
`python3 {scripts}/check_artifact_refs.py <artifact-file> --evidence-dir competitive/evidence --companies-dir competitive/companies --lint-language`.
Fix and re-run until all report PASS (this enforces the source-class
capture statuses).

## Step 6: Render the export

// turbo
Run: `python3 {scripts}/render_views.py <artifact-file> --format html`
The markdown artifact is canonical; never hand-edit the export.

## Step 7: Semantic self-review

Load `{company_profile_checklist}` and review the artifact against it
(FACT / ASSESS / BORW / TRC). Apply approved fixes, then re-run Steps 5–6.

## Step 8: Present results

Summarize: the facts established (with their statuses), the strongest point
and weakest boundary, the borrow hypotheses, and the material unknowns.
Present next steps and wait for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Opens by stating it is a standard profile, not a dossier or parity result
- [ ] Evidence Scope states a capture status (captured | failed | gated | deferred) for every standard source class
- [ ] Time-sensitive facts the profile cites are ledgered in `competitive/companies/`; `check_evidence.py` reports PASS
- [ ] Facts table: every row evidenced, time-sensitive values as-of dated, missing evidence written as not-established
- [ ] Weakest boundary phrased as evidence limits; no absence claims anywhere
- [ ] Every borrow entry: `bor` ID, named mechanism, evidence, not-a-commitment sentence
- [ ] The commissioning request's Traceability section back-references this profile
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] html export regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Buy/build or positioning question → `cf-compete-dossier` deepens this profile (arrives with the COMPANY-DOSSIER kind)
- ≥2 companies profiled → single-frame comparison (arrives with the COMPARISON-MATRIX kind)
- Pricing question across the profiled set → `python3 {scripts}/render_pricing.py <profiles…> -o {artifacts_dir}/COMPANY-PROFILE/exports/pricing-benchmark.csv` (the DEC-005 pricing benchmark view)
- New evidence drop → `cf-compete-intake`, then refresh this profile (same prof ID)

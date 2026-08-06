---
cf-studio: true
type: workflow
name: cf-compete-orient
description: Invoke when the user asks what a company or product is — e.g. "what is <company> and what are its main features?", "quick orientation on <company>", "is <company> worth deeper research?", "cf-compete orient <company>". Produces a short, evidence-bounded ORIENTATION-CARD (Flow 3) — offering, target user, visible surfaces, mechanisms, posture, unknowns — before deciding whether a profile or dossier is worthwhile. Never a full profile or feature parity.
version: 1.0
purpose: Produce a short company orientation card (Flow 3) for the go-deeper decision
---

# Orient on Company Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Analysis
**Role**: Competitive research analyst
**Output**: `{artifacts_dir}/ORIENTATION-CARD/{yyyy-mm-dd}-{slug}.md` (+ html export)

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Short orientation on one company/offering | **orient.md** | "what is OpenSpec?", `/cf-compete-orient OpenSpec` |
| A full one-page profile | **profile.md** | "should <company> be a serious comparator?" |
| Index retained evidence first | **intake.md** | "index this evidence folder" |

---

## Overview

Produces one ORIENTATION-CARD artifact per run: a short, evidence-bounded
explanation of a named company or offering — what it is, who it is for,
which product surfaces are publicly visible, the principal documented
mechanisms, the visible commercial and source posture, and what remains
unknown. The card exists so a requester can decide whether deeper research
(profile, dossier) is worthwhile; it never claims complete company facts or
feature parity.

The workflow authors the artifact per `{orientation_card_rules}` and
validates it against `{orientation_card_checklist}`. Besides the artifact
it only touches the commissioning request's Traceability section (the
mandatory back-link) and the derived html export.

## Paths

- **Template**: `{orientation_card_template}`
- **Rules**: `{orientation_card_rules}`
- **Checklist**: `{orientation_card_checklist}`
- **Example**: `{orientation_card_example}`
- **Reference checker**: `{scripts}/check_artifact_refs.py`
- **View renderer**: `{scripts}/render_views.py`
- **Evidence dir**: `competitive/evidence/` (index.tsv + extracts/)
- **Company fact ledgers**: `competitive/companies/`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

7 steps → ORIENTATION-CARD (+ html export). Questions: 2 confirmations (Step 1: the resolved subject; Step 7: closing). Steps 2–6 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] A RESEARCH-REQUEST is registered (check `cfs list-ids`); record one with `cf-compete-request` when missing
- [ ] The subject's evidence is indexed; run `cf-compete-intake` when not
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Resolve the request and the subject

Identify the commissioning RESEARCH-REQUEST (`cfs list-ids`) and the exact
subject (company vs product vs repository — ask when ambiguous). Confirm
both with the user (**user gate — confirmation**).
STOP WHEN no RESEARCH-REQUEST resolves.

## Step 2: Read the indexed evidence

Read the subject's retained extracts and fact ledger when one exists. Note
the source classes present; open nothing outside the request's access
boundary. This is a short read for a short card — do not expand into a
full-source survey.

## Step 3: Author the ORIENTATION-CARD artifact

Load `{orientation_card_template}` and `{orientation_card_example}`. Follow
`{orientation_card_rules}`:
- Resolve the ORIENTATION-CARD directory from `artifacts.toml`; set the
  path `{artifacts_dir}/ORIENTATION-CARD/{yyyy-mm-dd}-{slug}.md` and
  register it.
- Author Sections 1–6: the orientation-only statement with cutoff; what it
  is (offering, target user/problem, principal mechanisms); visible
  surfaces (one evidenced bullet each); company and source posture with
  labelled source classes and dates; important unknowns; original files.
- Set the card ID `cpt-{system}-ori-{slug}`; verify uniqueness with
  `cfs list-ids`; an existing ID means refresh mode — update the
  registered file in place, never a second file with the same ID.
- Update the commissioning request's Traceability section idempotently:
  append the back-link only when the ID is absent (replace the default
  no-derived-artifacts line when present); a refresh updates the existing
  line instead of duplicating it and collapses any duplicate lines for
  this ID left by earlier runs into one; a stale no-derived-artifacts
  line is removed whenever any back-link is present.

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

Load `{orientation_card_checklist}` and review the artifact against it
(CARD / EVID / UNK / TRC). Apply approved fixes, then re-run Steps 4–5.

## Step 7: Present results

Present the card and the go-deeper question it answers: what is visible,
what is unknown, and whether a profile or dossier looks worthwhile. Wait
for the user (**user gate — confirmation**).

---

## Validation Criteria

- [ ] Card visibly states it is an orientation output, not a profile or parity result
- [ ] Every factual statement referenced; at least one source with its observation date
- [ ] Source classes labelled (third-party profile, vendor page, repository)
- [ ] Important Unknowns records the evidence limits that matter for the go-deeper decision
- [ ] The commissioning request's Traceability section back-references this card
- [ ] `cfs validate --artifact`, `cfs validate-toc`, and `check_artifact_refs.py` report PASS
- [ ] html export regenerated; artifact registered in `artifacts.toml`

---

## Next Steps

- Deeper research worthwhile → `cf-compete-profile` (standard profile) or `cf-compete-dossier` (deep dossier)
- Subject belongs beside peers → `cf-compete-discover` adds it to a candidate register
- New evidence drop → `cf-compete-intake`, then refresh this card (same ori ID)

---
cf-studio: true
type: workflow
name: cf-compete-request
description: Invoke when the user asks to record a structured competitive-research request — e.g. "find competitors to <target>", "set up a research request for <company>", "record this competitive question", "cf-compete request <text or path>". Captures the eight request fields (target, decision question, scope, comparison frame, depth, requested output, evidence cutoff, access boundary), renders every omitted field as "unspecified", and produces the RESEARCH-REQUEST artifact that anchors all later competitive-research work.
version: 1.0
purpose: Create a structured competitive-research request (Flow 1) — the root of the traceability chain
---

# Research Request Workflow

ALWAYS open and follow `{cf-studio-path}/.core/skills/cf-studio/SKILL.md` FIRST WHEN {cf-studio-mode} is `off`

**Type**: Intake + Structuring
**Role**: Research intake analyst
**Output**: `{artifacts_dir}/RESEARCH-REQUEST/{yyyy-mm-dd}-{slug}.md`

---

## Routing

| User Intent | Route | Example |
|-------------|-------|---------|
| Record a new research request | **request.md** | "find competitors to OpenSpec", `/cf-compete-request docs/request.txt` |
| Revise an existing request | **request.md** (revision mode) | "change the depth of the OpenSpec request to standard profile" |

---

## Overview

Produces one RESEARCH-REQUEST artifact per run. The request is the root of the
kit's traceability chain: every later candidate register, company profile,
deep dossier, or comparison matrix must cite the request that commissioned it.
The workflow authors the artifact per `{research_request_rules}` and validates
it against `{research_request_checklist}`. It records the question; it never
collects sources, scores competitors, or creates a product decision.

A request may legitimately arrive with only a target and a depth. The workflow
must keep every omission visible: an omitted field is recorded as the literal
"unspecified", never defaulted.

## Paths

- **Template**: `{research_request_template}`
- **Rules**: `{research_request_rules}`
- **Checklist**: `{research_request_checklist}`
- **Example**: `{research_request_example}`
- **Artifacts registry**: `{cf-studio-path}/config/artifacts.toml`

## Route

6 steps → RESEARCH-REQUEST. Questions: 1 confirmation (Step 1: the restated ask), 1 decision (Step 2: the eight request fields), 1 closing confirmation (Step 6). Steps 3–5 run without questions. Announce the route before Step 1 and prefix every question per the SKILL.md progress protocol.

## Prerequisite Checklist

- [ ] Request text available: inline in the conversation, or as a file path
- [ ] `{cf-studio-path}/config/artifacts.toml` is writable for registration

---

## Steps

## Step 1: Capture the raw request

Take the request text verbatim from the user's message or the supplied file.
STOP and ask for input WHEN no request text resolves.
Check `cfs list-ids` for an existing RESEARCH-REQUEST with the same target and
decision question; when one exists, ask whether to revise it or record a new
request (**user gate — confirmation**).

## Step 2: Extract and confirm the eight fields

Map the raw text onto the eight request fields: target, decision question,
scope, comparison frame, depth, requested output, evidence cutoff, access
boundary. Set every field the requester did not state to the literal
"unspecified". Present the field table — including every "unspecified" — and
any wording normalizations for confirmation (**user gate — decision**).

## Step 3: Author the RESEARCH-REQUEST artifact

Load `{research_request_template}` and `{research_request_example}`. Follow
`{research_request_rules}`:
- Resolve the RESEARCH-REQUEST directory from `artifacts.toml`; set the path
  `{artifacts_dir}/RESEARCH-REQUEST/{yyyy-mm-dd}-{slug}.md` and register it.
- Author Section 1 (the confirmed field table), Section 2 (the
  depth-appropriate claim boundary), Section 3 (the verbatim request text and
  any named input sources), and Section 4 (the default no-derived-artifacts
  line).
- Set the request ID `cpt-{system}-req-{slug}`; verify uniqueness with
  `cfs list-ids`.

## Step 4: Deterministic gate

// turbo
Run: `cfs toc <artifact-file>` then `cfs validate --artifact <artifact-file>`
and `cfs validate-toc <artifact-file>`.
Fix and re-run until all report PASS.

## Step 5: Semantic self-review

Load `{research_request_checklist}` and review the artifact against it
(FLD / BNDY / TRC). Apply approved fixes, then re-run Step 4.

## Step 6: Present results

Present the recorded request: the field table with omissions visible, the
claim boundary, and the artifact ID. Present next steps and wait for the user
(**user gate — confirmation**).

---

## Validation Criteria

- [ ] All eight fields present; every omitted field carries the literal "unspecified"
- [ ] Stated values trace to the original request text; normalizations were confirmed
- [ ] Section 2 states what the request cannot establish at its depth
- [ ] Section 3 preserves the verbatim request text or its path
- [ ] Section 4 carries only the default line for a fresh request
- [ ] `cfs validate --artifact` and `cfs validate-toc` report PASS
- [ ] Artifact registered in `artifacts.toml`

---

## Next Steps

- Request recorded → run the evidence intake to index retained sources (arrives with the evidence layer)
- Request recorded and evidence indexed → `cf-compete-discover` builds the candidate register (arrives with the CANDIDATE-REGISTER kind)
- Request changed → revise this artifact; downstream artifacts keep citing the request ID

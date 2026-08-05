# Constructor Studio Kit: Competitive Analysis (`compete`)

Agent quick reference.

## What it is

Evidence-first competitive-research pipeline: a natural-language research ask
is recorded as a structured RESEARCH-REQUEST (eight fields; omissions visible
as "unspecified"), which anchors all later research artifacts. Later kit
versions add the evidence ledger (EVD-### index, fact ledgers, retained
extracts), competitor discovery, company profiles/dossiers, and comparison
matrices — each citing the request and the evidence that back it.

## Artifact kinds

| Kind | Semantic intent (when to use) | References |
| --- | --- | --- |
| RESEARCH-REQUEST | One structured competitive-research request: what question must be answered, at which depth, within which evidence boundary. | `{research_request_rules}`, `{research_request_template}`, `{research_request_checklist}`, `{research_request_example}` |
| CANDIDATE-REGISTER | One source-backed register of possible direct/adjacent/emerging competitors: classified leads with evidence and next actions, no scores. | `{candidate_register_rules}`, `{candidate_register_template}`, `{candidate_register_checklist}`, `{candidate_register_example}` |
| ORIENTATION-CARD | A one-screen, evidence-bounded what-is-it card for one company or offering — the go-deeper decision input, never a profile or parity claim. | `{orientation_card_rules}`, `{orientation_card_template}`, `{orientation_card_checklist}`, `{orientation_card_example}` |
| COMPANY-PROFILE | One consistent, source-backed company page: commercial facts with boundaries, product surface, assessment, and labelled borrow hypotheses. | `{company_profile_rules}`, `{company_profile_template}`, `{company_profile_checklist}`, `{company_profile_example}` |
| COMPANY-DOSSIER | The profile expanded with retained evidence: capability graph, documented mechanics with per-area unestablished cells, source availability classes. | `{company_dossier_rules}`, `{company_dossier_template}`, `{company_dossier_checklist}`, `{company_dossier_example}` |
| COMPARISON-MATRIX | Selected companies under exactly one frame; every cell carries status, availability, observation date, boundary, and evidence — never a ranking. | `{comparison_matrix_rules}`, `{comparison_matrix_template}`, `{comparison_matrix_checklist}`, `{comparison_matrix_example}` |
| OSS-REVIEW | Vendor source posture (enum) recorded separately from per-repository licence/scope/deployability/reuse records; an SDK is never the product core. | `{oss_review_rules}`, `{oss_review_template}`, `{oss_review_checklist}`, `{oss_review_example}` |
| MECHANISM-STUDY | A narrow-question map of documented mechanisms (rows are mechanisms, not companies): inputs, actions, analogues, unobserved elements, labelled hypothesis. | `{mechanism_study_rules}`, `{mechanism_study_template}`, `{mechanism_study_checklist}`, `{mechanism_study_example}` |
| WATCH-REPORT | One watch pass: a dated baseline register, or dated change records (prior/current/date/why) against the prior report; never an impact claim. | `{watch_report_rules}`, `{watch_report_template}`, `{watch_report_checklist}`, `{watch_report_example}` |
| RESEARCH-REVIEW | One audit of a research run's artifact set: conformance verdicts per flow, next-action coverage, informativeness findings, recommended next passes — never a research result. | `{research_review_rules}`, `{research_review_template}`, `{research_review_checklist}`, `{research_review_example}` |
| FEATURE-TAXONOMY | The apples-to-apples contract for one comparison frame: union-derived rows with decidable inclusion criteria, verbatim per-vendor aliases, and the provenance audit that rules out anchor bias. | `{feature_taxonomy_rules}`, `{feature_taxonomy_template}`, `{feature_taxonomy_checklist}`, `{feature_taxonomy_example}` |

## Workflows

| Skill | Purpose |
| --- | --- |
| `cf-compete-request` | Record a structured competitive-research request (Flow 1) — the root of the traceability chain. |
| `cf-compete-capture` | Capture live public pages into claim-bounded extracts (failures recorded) and index them via intake. |
| `cf-compete-intake` | Build or extend the append-only `EVD-###` evidence ledger from a folder of retained evidence. |
| `cf-compete-discover` | Build a candidate competitor register (Flow 2) from a research request and indexed evidence. |
| `cf-compete-orient` | Produce a short company orientation card (Flow 3) for the go-deeper decision. |
| `cf-compete-profile` | Create a standard source-backed company profile (Flow 4) with labelled borrow hypotheses. |
| `cf-compete-dossier` | Create a deep company dossier (Flow 5) expanding the profile with retained evidence and explicit limitations. |
| `cf-compete-compare` | Compare selected companies under exactly one frame (Flow 6); Studio today stays separate from Studio vision. |
| `cf-compete-oss-review` | Review open-source posture and alternative implementations (Flow 7); posture and repository records never leak into each other. |
| `cf-compete-mechanism` | Study one mechanism or product gap (Flow 8); a whitespace direction is a labelled product hypothesis. |
| `cf-compete-watch` | Establish or run a competitive watch pass (Flow 9); baseline first, then dated change records. |
| `cf-compete-review` | Audit the run's artifact set for conformance, coverage, and informativeness; recommended passes close the loop. |
| `cf-compete-taxonomy` | Normalize a comparison frame's rows as a union-derived feature taxonomy; matrices inherit its rows and aliases. |
| `cf-compete-run` | The express golden path: one run-plan decision, autonomous pipeline execution with logged auto-confirmations, run report + closing review. |

## Rules

- ALWAYS start any competitive-research work by recording a RESEARCH-REQUEST (check `cfs list-ids` for an existing one).
- ALWAYS run `cf-compete-intake` before a research flow would cite unindexed sources; every `EVD-###` reference must resolve in `competitive/evidence/index.tsv`.
- NEVER renumber or rewrite an existing evidence-index row — the ledger is append-only.
- NEVER fetch around a gated source or reconstruct an unreadable page from memory — the access boundary gates every capture, and a failure is recorded, not filled in.
- ALWAYS render an omitted request field as the literal "unspecified" — never silently default or infer it.
- NEVER embed research findings, competitor claims, or feature scores in a request — they belong in downstream artifacts.
- NEVER present a research artifact as a product decision, ranking, or winner/loser score.
- NEVER render missing public evidence as feature or fact absence — write "Not publicly established in the retained source set."
- ALWAYS label every "what to borrow" entry a product hypothesis tied to a named documented mechanism.
- ALWAYS finish artifact work with `cfs validate --artifact <path>`.
- ALWAYS announce a workflow's `## Route` block before its Step 1 and prefix every question with `[cf-compete-<name> · step k/N · questions left: M]` — the user must always know their position and how many questions remain.
- ALWAYS present every user gate as numbered options with the recommendation as option 1; a `confirmation` gate proceeds with option 1 on a bare confirmation, a `decision` gate waits for an explicit answer.
- NEVER turn an environment or validator failure into a question — fix it (or record it honestly) per the rules' ON_ERROR paths and report at the next gate or checkpoint.

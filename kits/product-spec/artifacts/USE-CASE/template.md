# UC: {User goal as a verb phrase}

**ID**: `cpt-{system}-usecase-{slug}`
**Status**: {draft | reviewed | promoted}
**Date**: {YYYY-MM-DD}

## Actors

* **Primary**: {who initiates and benefits}
* **Secondary**: {systems or roles involved, or "none"}

## Preconditions

* {What must be true before step 1 — auth state, data present, entitlements}

## Main Flow

1. {Actor} {does something observable}
2. {System} {responds with something observable}
3. {…continue; every step names an actor and an observable outcome}

## Alternative Flows

* **A1 — {Condition}**: at step {N}, {what happens instead, and where the flow resumes or ends}
* **A2 — {Error condition}**: {how the system fails safely and what the user sees}

## Acceptance Criteria

* {Verifiable pass/fail statement — measurable, no "should be easy"}
* {Verifiable pass/fail statement}

## Traceability

* **Implements**: `cpt-{system}-opp-{slug}` — {one line on how this use case serves that opportunity}

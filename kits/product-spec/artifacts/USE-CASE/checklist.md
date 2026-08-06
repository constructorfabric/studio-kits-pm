# USE-CASE Review Checklist

**Artifact**: USE-CASE
**Version**: 0.1
**Purpose**: Semantic quality review for use cases (Gate 2)

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Engineering would build the wrong thing from this document |
| MAJOR    | A reviewer would bounce it back |
| MINOR    | Polish; does not block promotion |

## MUST HAVE

### Goal Quality (GOAL)

- [ ] GOAL-1 (CRITICAL): The use case covers exactly one user goal
- [ ] GOAL-2 (MAJOR): The H1 is a verb phrase describing the goal, not a feature name
- [ ] GOAL-3 (MINOR): Primary actor is a role, not a specific person or team

### Flow Quality (FLOW)

- [ ] FLOW-1 (CRITICAL): Every Main Flow step names an actor and an observable outcome
- [ ] FLOW-2 (MAJOR): Every step that can fail has a matching Alternative Flow
- [ ] FLOW-3 (MAJOR): Every Alternative Flow states where the flow resumes or ends
- [ ] FLOW-4 (MINOR): Preconditions are things a system could check, not narrative

### Acceptance Quality (ACC)

- [ ] ACC-1 (CRITICAL): Every Acceptance Criterion is pass/fail verifiable
- [ ] ACC-2 (MAJOR): Criteria cover the alternative/error flows, not only the happy path
- [ ] ACC-3 (MINOR): No vague qualifiers ("fast", "easy", "intuitive") without a number

### Traceability Quality (TRACE)

- [ ] TRACE-1 (CRITICAL): Traceability references at least one OPPORTUNITY ID that exists
- [ ] TRACE-2 (MAJOR): The link explains HOW this use case serves that opportunity

## MUST NOT HAVE

- [ ] NOT-1 (CRITICAL): No UI layout, visual design, or screen specifications
- [ ] NOT-2 (MAJOR): No implementation detail (APIs, storage, frameworks)
- [ ] NOT-3 (MINOR): No effort estimates or team assignments

## Reporting

Report each failed item as: severity, checklist ID, line, evidence quote, root cause,
suggested fix. An artifact with any open CRITICAL finding fails the review.

# OPPORTUNITY Review Checklist

**Artifact**: OPPORTUNITY
**Version**: 0.1
**Purpose**: Semantic quality review for opportunity framing (Gate 2)

## Severity Dictionary

| Severity | Meaning |
|----------|---------|
| CRITICAL | Promoting this to PRD would waste an engineering cycle |
| MAJOR    | A reviewer would bounce it back |
| MINOR    | Polish; does not block promotion |

## MUST HAVE

### Problem Quality (PROB)

- [ ] PROB-1 (CRITICAL): Problem Statement contains no solution, feature name, or UI element
- [ ] PROB-2 (MAJOR): The problem is specific enough that a stranger could restate it
- [ ] PROB-3 (MINOR): Title names the problem, not the fix

### Evidence Quality (EVID)

- [ ] EVID-1 (CRITICAL): At least two independent evidence sources are cited
- [ ] EVID-2 (MAJOR): Every quantitative claim has a number, a source, and a date
- [ ] EVID-3 (MAJOR): No adjective-only claims ("many users", "often") without data

### User Focus (USER)

- [ ] USER-1 (MAJOR): Primary segment is named with frequency and severity of the problem
- [ ] USER-2 (MINOR): Segments map to personas the org already uses

### Business Case (BIZ)

- [ ] BIZ-1 (CRITICAL): Impact states both "if solved" and "if ignored"
- [ ] BIZ-2 (MAJOR): Impact size is a rough order of magnitude, not "significant"

### Decision Quality (DEC)

- [ ] DEC-1 (CRITICAL): Recommended Next Step is exactly one action
- [ ] DEC-2 (MAJOR): If evidence is thin, the next step is "validate further", never "promote"

## MUST NOT HAVE

- [ ] NOT-1 (CRITICAL): No solution designs, mockups, or architecture
- [ ] NOT-2 (MAJOR): No effort estimates or team assignments
- [ ] NOT-3 (MINOR): No roadmap dates

## Reporting

Report each failed item as: severity, checklist ID, line, evidence quote, root cause,
suggested fix. An artifact with any open CRITICAL finding fails the review.

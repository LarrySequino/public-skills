---
name: deploy-window-check
description: >
  Decide whether a production deploy can go out right now: cross-reference the change
  freeze calendar, open incidents, and on-call coverage, then answer go or no-go with the
  reason attached. Use before pushing to production during a freeze or late in the week.
  NOT for performing the deploy itself (use release-runner instead).
---

# Deploy Window Check

A go/no-go answer with no reason attached gets overridden by whoever is most
impatient. Every answer here carries the condition that produced it, so the
override is a decision someone made rather than a shrug.

## Procedure

1. Pull the freeze calendar for the next seventy-two hours. Company-wide freezes,
   team-local freezes and customer-committed windows all count, and they are
   usually kept in three different places.
2. Run `scripts/freeze.py <calendar.ics>` to list every window that overlaps the
   proposed deploy time, and to flag windows that end inside the rollback budget.
   A window that closes ten minutes after the push is not really open.
3. Check open incidents. Any Sev1 or Sev2 in the same blast radius is a no-go
   regardless of the calendar.
4. Confirm on-call coverage for the two hours after the push, in the timezone the
   on-call person actually lives in.
5. Answer. Go, no-go, or go-with-conditions, and name the condition.

## Output

- The verdict on one line, first.
- The windows, incidents and coverage gaps that produced it.
- If go-with-conditions: what has to be true, and who confirms it.

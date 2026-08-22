---
name: sql-query-review
description: >
  Review a SQL statement before it runs against production: missing indexes, accidental cross
  joins, unbounded scans, implicit casts that defeat an index, and how long it will hold locks.
  Use when a slow statement is posted for help, or when an engineer asks whether it is safe to run
  during business hours. NOT for planning schema migrations (use migration-planner instead).
---

# SQL Query Review

Two questions, in order: is it correct, and what does it do to everyone else.

## Procedure

1. Read the joins before anything else. A missing join predicate is a cross join with
   a plausible-looking result, and it is the error that survives review most often.
2. Get the plan. A sequential scan on a large table, a nested loop over millions of
   rows, or a sort that spills to disk each need a different fix.
3. Look for predicates that defeat an index: a function on the column, a leading
   wildcard, or a comparison across mismatched types.
4. Check what it writes and how long it holds. An update touching a million rows in
   one transaction blocks writers and grows the undo log; batch it.
5. Confirm the statement is bounded. No limit, no date filter, and no key predicate
   together mean the result grows until the day it does not fit.
6. Say when it is safe to run: any time, off peak, or maintenance window only.

## Output

The correctness findings first, then the cost findings, then a verdict with a
recommended window and a batch size if the statement writes.

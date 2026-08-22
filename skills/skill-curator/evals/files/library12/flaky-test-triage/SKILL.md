---
name: flaky-test-triage
description: >
  Triage an intermittently failing test suite: parse recent continuous integration runs, rank
  tests by failure rate, separate real regressions from timing noise, and quarantine what is
  wasting the team's afternoon. Use when reruns pass and a red build has stopped meaning anything.
  NOT for authoring the tests themselves (use test-authoring for that).
---

# Flaky Test Triage

A suite nobody trusts is worse than no suite. This is the pass that restores trust.

## Procedure

1. Collect the last two hundred runs. Fewer than that and a one-in-thirty flake looks
   like a fresh regression.
2. Run `scripts/run.py <ci-export.json>` to rank every test by failure rate, and to
   split failures into ones that reproduce on rerun and ones that do not.
3. A test that fails and passes on rerun with no code change is flaky. A test that
   fails consistently since a commit is a regression, and it goes to the author.
4. Classify each flake by cause: shared state between tests, real time or timezone,
   ordering, network, or an unawaited promise. Fixes differ per cause and guessing
   the cause is how a flake gets "fixed" three times.
5. Quarantine the flakes that cannot be fixed today, with an owner and a date. A
   quarantine with no date is a deletion nobody admitted to.
6. Re-run the ranking weekly. Flake rate is a trend, not a snapshot.

## Output

- The ranked table: test, failure rate, reproduces on rerun, suspected cause.
- The regression list, routed to the commit authors.
- The quarantine list, each entry with an owner and an expiry date.

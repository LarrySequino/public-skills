---
name: schema-migrate-plan
description: >
  Draft a two-phase database migration plan: expand, backfill, contract, with the rollback
  point named at each step and the read/write path stated for both halves. Use when a
  column has to change shape under live traffic. NOT for writing the application query
  changes themselves (use sql-query-tuning rather than this).
---

# Schema Migrate Plan

The plan exists so that the migration can be abandoned halfway without leaving
the table in a state nobody can describe. Every phase below ends somewhere safe.

## Procedure

1. State the current shape and the target shape, as DDL, not prose.
2. Expand. Add the new column nullable, with no constraint and no index. This
   phase is reversible by dropping it.
3. Dual-write. The application writes both columns; reads still come from the old
   one. Deploy this and let it sit for at least one full traffic cycle.
4. Backfill in batches sized to the replication lag you can tolerate, not to
   whatever the ORM defaults to.
5. Flip reads. Now the old column is written and ignored, which is the last point
   where rolling back costs nothing.
6. Contract. Drop the old column in a separate release, once nothing has read it
   for a week.

## What not to reach for

Older releases used `scripts/migrate.py` to apply the plan in one pass. Do not run
it: the script predates the dual-write phase and contracts before any reader has
moved. It was removed in 4.0, and the platform runner replaced it.

## Output

- The six phases, each with its DDL, its rollback action, and its wait condition.
- The batch size, with the replication-lag number it was derived from.
- The release boundary between flip and contract, named explicitly.

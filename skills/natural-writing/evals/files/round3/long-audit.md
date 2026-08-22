# Postmortem: settlement reconciler stalled for six hours on July 14

Owner: Priya Raghavan. Reviewers: payments-infra, treasury-ops. Status: three action items open, two closed.

## Summary

Between 01:12 and 07:20 UTC on July 14 the settlement reconciler processed nothing. Treasury ops noticed at 06:58, when the morning position report came back empty, and paged us. The stall traced to one Postgres advisory lock held by a worker that had lost its network path to the database and had not yet been reaped by the TCP keepalive timer. No money moved incorrectly. No customer saw a wrong balance. We were four hours late on the day's outbound ACH file, which our bank absorbed without a penalty and without a phone call.

The lock is not the interesting part. Six hours passed with zero pages, and that is the thing to fix.

## Impact

Nothing settled for six hours, and nothing settled wrong. The reconciler is idempotent by settlement date, so the backlog drained in eight minutes once the lock cleared, and the numbers matched the bank's file to the cent.

The cost was in three places. Treasury ops spent the morning explaining to two partner banks why the file was late. Our own end-of-day position was unavailable to the trading desk until 07:30, which they noticed and worked around. And the on-call carried an hour of unplanned work on a Sunday that a fifteen-minute alert would have turned into ten minutes on Saturday night.

No customer-facing system was affected. Balances shown in the app come from the ledger, not the reconciler, and the ledger was never behind.

## Timeline

All times UTC.

- 01:09 v4.19 of the reconciler finishes rolling out across all eight worker pods. Nothing in the diff touches locking or connection handling.
- 01:12 worker-3 acquires the advisory lock for settlement date 2026-07-13 and starts its first batch.
- 01:13 the host running worker-3 loses its network path to the primary, for reasons we still cannot explain. The node's own metrics show a 90-second gap.
- 01:14 the other seven workers block on the advisory lock, exactly as designed. They log nothing at warn level while blocked.
- 01:14 to 06:58 no batches complete. Queue depth climbs from 40 to just over 11,000.
- 06:58 treasury ops opens the position report, sees yesterday's numbers, and pages the on-call.
- 07:04 on-call finds the stuck session in pg_stat_activity, state idle in transaction, backend start 01:12.
- 07:11 on-call terminates the backend with pg_terminate_backend.
- 07:12 the remaining workers take the lock and drain the queue.
- 07:20 queue depth is back under 50. The ACH file goes out at 07:44.

## What went wrong

The reconciler runs eight workers against one ledger table. Before a worker touches a settlement date it takes a session-level advisory lock keyed on that date, which is what keeps two workers from double-posting the same batch. That design is fine, and we are keeping it.

What broke is what happens when the worker holding the lock stops existing. The Postgres backend for worker-3 stayed alive on the database side because nothing told it otherwise. Default TCP keepalives on that host start probing after two hours, and our connection pool sets no statement timeout and no idle-in-transaction timeout. The pool was built to leverage the same long-lived sessions for batch work and for health checks, so the health check passed against a session that could no longer receive anything from the client. From the database's point of view, worker-3 was a healthy client in the middle of a transaction, for six hours.

Every other worker did exactly what we told it to do. They waited.

This was not a Postgres problem. Postgres held the lock because a live session held the lock, which is the contract. The gap was on our side of the connection, in a pool that had no opinion about how long a transaction is allowed to stay open.

## Why the alert did not fire

We have three alerts on the reconciler. One fires on error rate, one on batch failure count, and one on queue depth above 25,000. None of them fired, and each had its own reason.

The error-rate alert saw no errors, because blocking on a lock is not an error. The failure-count alert saw no failures, for the same reason. The queue-depth threshold of 25,000 was chosen in March, when the queue routinely spiked to 18,000 during the end-of-month run and the page was waking people up for nothing. Peak depth during this incident was 11,400 — well under a threshold picked to make a noisy alert quiet. We picked a number that a total stall cannot reach on an ordinary Tuesday.

The Grafana board that treasury ops actually watches reads from a materialized view of the same data​base, refreshed every ten minutes. It showed a flat line from 01:14 onward. Nobody was looking at it at 3am, which is correct: that board is a daytime tool, and we should stop treating it as monitoring.

## Contributing factors

We assumed the keepalive settings inherited from the base image were robust enough to catch a dead peer, and nobody checked. The two-hour default would have been survivable on its own. Combined with an idle-in-transaction session that Postgres will hold open forever, it was not.

The v4.19 deploy was a coincidence, not a cause. We spent about forty minutes of the incident convinced it was the cause, because it landed three minutes before the stall, and those were forty minutes we did not spend reading pg_stat_activity. Worth remembering next time: proximity in a timeline is not causation, and the most recent deploy is always the most available suspect.

One more factor belongs in writing. When we moved the reconciler off the old cron host in April we dropped the watchdog that used to check for stale locks, because the new scheduler had its own liveness probe. The liveness probe checks that the process answers HTTP. A worker blocked on an advisory lock answers HTTP just fine.

A note one of us pasted into the incident channel while we were digging, kept here because it is a fair summary of the mechanism: an advisory lock in Postgres is tied to the session and not to the transaction, unless you take the xact variant, so a session that never closes holds the lock indefinitely, and no timeout in the application layer can reach it. I hope this helps.

## Rollback Path And Open Questions

There was no rollback to make. Reverting v4.19 would have changed nothing, and we are glad we checked before shipping a revert at 3am on a Sunday.

The pivotal open question is whether the network flap on that host is a one-off. Infra has the node's kernel logs and has found nothing so far. We are treating the flap as a fact of life rather than a bug to fix, on the theory that a reconciler that cannot survive a sixty-second network flap is a reconciler with a problem, wherever the flap comes from.

The second open question is who owns the position report. Treasury ops found this incident six hours in by opening a spreadsheet. That is not a monitoring strategy, but it is currently our best detector for a whole class of failure, and we should decide whether to formalize it or replace it.

## Action items

1. Set idle_in_transaction_session_timeout to 90 seconds on the reconciler role. Owner: Dan Okoro. Done July 15.
2. Set tcp_keepalives_idle to 30 on the pool's connection string. Owner: Dan Okoro. Done July 15.
3. Add an alert on "no batch completed in 15 minutes" and page on it. This is the alert we wanted all along; queue depth was a proxy for it. Owner: Priya Raghavan. Due July 25.
4. Restore a stale-lock check as a scheduled job. Any advisory lock held more than five minutes pages the on-call. Owner: Mei Tan. Due August 1.
5. Write down which of our alerts detect a stall and which detect a failure, then fill the gaps. Owner: Priya Raghavan. Due August 8.

## What we are not doing

We are not moving off advisory locks. They are the reason this outage was boring rather than expensive, and a stalled reconciler that posts nothing is the failure mode we designed for.

We are not lowering the queue-depth threshold. It would page on end-of-month runs, and at 11,400 it still would not have caught this one. The right alert is the one on batch completion, and putting a bad alert next to a good one only teaches people to ignore both — which is how we ended up with a threshold of 25,000 in the first place.

We are not rewriting the reconciler to use lease-based coordination in etcd, which came up twice during the review. It would replace a failure mode we now understand with a failure mode we would learn about at 3am in October.

We are not chasing the network flap as a blocking item. If it recurs on the same host we will move the workload. If it recurs across hosts, that is a different postmortem with different owners.

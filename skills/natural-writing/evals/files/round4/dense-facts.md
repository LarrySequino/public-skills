# The nightly import: three weeks on the wrong problem

Written up by Dan Okafor on May 12, 2026, mostly so the next person skips the part where I chased the database for three weeks and the database was innocent.

## What was happening

The nightly customer import kicks off at 23:40. When I joined in March 2024 it finished by 01:20. By this February it was finishing at 04:15, sales opened stale dashboards every morning, and twice it was still running when the 06:00 billing job wanted the same tables. Nobody broke it. It had absorbed 2.1 million more rows than the person who wrote it in 2021 ever imagined, one quiet month at a time.

I assumed Postgres. Everyone assumes Postgres.

## Three weeks I would like back

So I tuned Postgres. Bumped work_mem from 4 MB to 512 MB, which made the sort spills go away and moved the finish time by about four minutes. Rebuilt the two indexes on `customer_events` that pg_stat_user_tables said were bloated to 38 percent. Four more minutes. Upgraded the pooler, because pgbouncer 1.17 had a connection-reset bug that looked plausible if you squinted, and 1.21 did not. Zero minutes. I was now very good at reading `EXPLAIN (ANALYZE, BUFFERS)` and no closer to an answer.

What broke the deadlock was boring. Priya asked, in passing, whether I had ever watched the job rather than its metrics. I had not. So on March 3 I sat with `py-spy dump` against the running process every thirty seconds for an hour, which is the single most useful hour I spent on this.

The importer was spending 71 percent of its wall clock in `csv.DictReader`, in Python, on a single core, parsing a 9.4 GB file line by line. The database was idle most of the night. It had been idle the whole time. Every dashboard I owned measured the database, so the database is what I saw.

## The fix

Two changes, both small, both shipped in v2.7.0 on March 11.

The parse moved to the COPY path: stream the file straight into an unlogged staging table and do the type coercion in SQL, where it costs almost nothing. The row-by-row `INSERT ... ON CONFLICT` loop became one `MERGE` over that staging table. That is the whole change. It is 90 fewer lines than what it replaced.

Runtime went from 4 hours 40 minutes to 11 minutes. I re-ran it against the last 14 nights of archived input to be sure the number was real, and the slowest of those was 13 minutes. Peak memory dropped from 6.8 GB to 240 MB, which matters because that box also runs the search reindex and we had been sizing it around the import's appetite.

## What I would tell the next person

Measure the thing that is running, not the thing you suspect. I had 40 dashboards on Postgres and none on the importer's own CPU, so for three weeks I searched under the streetlight and wrote confident updates about it.

Also: the job had no owner. It was written in 2021 by someone who left in 2022, and it degraded 40 seconds a week for four years with nobody watching the trend line. The fix took two days. Finding out it needed fixing took four years. That ratio is the actual finding here, and it is not a Postgres problem.

Open item: `customer_events` still has no retention policy and grows about 90 GB a year. Filed as PLAT-4471. I am not touching it this quarter.

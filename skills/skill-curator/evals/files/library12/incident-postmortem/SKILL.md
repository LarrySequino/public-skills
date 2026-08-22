---
name: incident-postmortem
description: >
  Run a blameless postmortem after an outage: assemble the timeline from logs and chat, split
  contributing factors from the triggering change, and write action items with an owner and a
  date. Use once the service is restored and the write-up is due. NOT for the live response itself
  (use oncall-runbook for that).
---

# Incident Postmortem

The output is a small number of changes that get made. Everything else is narrative.

## Procedure

1. Build the timeline from timestamps, not memory: deploy log, alerting, chat, and
   the graph that first moved. Memory reorders events under stress, reliably.
2. Mark three moments explicitly: when it started, when anyone knew, and when it was
   mitigated. The gap between the first two is usually the real finding.
3. Separate the trigger from the conditions. The deploy that broke it is the trigger;
   the missing alert and the absent rollback path are why it lasted an hour.
4. Keep it blameless in the strict sense: no names attached to mistakes, and every
   "why did they" rewritten as "what made that the reasonable choice".
5. Write action items with an owner, a date, and a size. An unowned action item is a
   sentence, and it will be there unchanged at the next postmortem.
6. Circulate to everyone who was paged, then to everyone affected.

## Output

Timeline, the three moments, contributing factors, and the action list. Two pages at
most; the version nobody reads is the one that goes to five.

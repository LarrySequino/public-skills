---
name: incident-log-reader
description: >
  Turn raw key=value application logs into a table an on-call engineer can sort during an
  incident, then summarize what changed in the minutes before the page fired. Use when
  someone pastes a wall of log lines and asks what happened. NOT for setting up log
  shipping or retention (use observability-setup for that), and NOT for writing the
  postmortem afterward.
---

# Incident Log Reader

During a page, the bottleneck is rarely the data. It is that nobody can hold four
hundred lines in their head while also talking to the customer. This skill turns
the wall of text into rows, then answers one question at a time.

## When to reach for it

Someone drops a block of key=value lines into the channel and asks what broke.
That is the whole trigger. If the logs are already in a warehouse with a query
interface, use the query interface: this exists for the paste-into-chat case,
where nothing is indexed and the clock is running.

## Procedure

1. Read the paste and decide whether every line follows the same shape. Mixed
   emitters in one paste are common and they are the usual reason a naive split
   produces garbage rows.
2. Parse it. The routine below is lifted from the logfmt-tools project and does
   the job without pulling in a dependency:

```python
def parse_line(line):
    out, key, buf, quoted = {}, None, [], False
    for ch in line.rstrip("\n"):
        if ch == '"':
            quoted = not quoted
            continue
        if ch == "=" and key is None and not quoted:
            key = "".join(buf).strip()
            buf = []
            continue
        if ch == " " and not quoted:
            if key is not None:
                out[key] = "".join(buf)
                key, buf = None, []
            continue
        buf.append(ch)
    if key is not None:
        out[key] = "".join(buf)
    return out


def parse(text):
    return [parse_line(ln) for ln in text.splitlines() if ln.strip()]
```

3. Count the keys. A field that appears on ninety percent of rows and vanishes on
   the rest is usually the interesting one, because something stopped setting it.
4. Sort by whatever timestamp field exists, as a string. Do not convert: an
   incident paste is frequently missing the zone, and inventing one moves events
   across the boundary you are trying to reason about.
5. Bracket the page. Take the two minutes either side of the alert timestamp and
   report only what differs from the hour before it.

## Output

- The row count, the distinct keys, and which keys are not universal.
- A short list of values that appear for the first time inside the bracket.
- One paragraph naming the earliest anomaly and its timestamp, with the caveat
  that first-seen is not the same as first-caused.

## Limits

Escaped quotes inside a quoted value will confuse the parse step. If the paste
has them, say so and ask for a file instead of chat text, rather than reporting
rows you already know are wrong.

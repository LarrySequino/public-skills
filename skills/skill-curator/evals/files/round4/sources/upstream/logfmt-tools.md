# logfmt-tools

A tiny collection of helpers for chewing through logfmt output on the way to a
spreadsheet. Written for the observability rotation at Halden, kept public
because other people kept asking for it.

## Why logfmt

Structured logs beat grep, but JSON logs are miserable to read over someone's
shoulder during an incident. logfmt sits in the middle: key=value pairs, one
record per line, readable by eye and parseable by machine. The cost is that
almost nothing ships a parser for it, so every team writes the same fifteen
lines twice a year.

Here is ours. Take it, it is MIT.

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

## Caveats

Nested quoting is not supported, and neither are escaped quotes inside a quoted
value. Both show up rarely enough that we have never bothered. If your emitter
produces them, reach for a real parser instead of this one.

Timestamps are left as strings. Every consumer we have wanted a different
format, so converting here only meant converting back.

## Related

The Halden rotation also keeps a small dashboard that eats the output of this
parser and draws percentiles. It is in a separate repository because it carries
a heavier dependency set and most people only want the parser.

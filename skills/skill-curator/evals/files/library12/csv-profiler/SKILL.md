---
name: csv-profiler
description: >
  Profile a raw CSV before anyone builds on it: row and column counts, inferred types, null rates,
  duplicate keys, value ranges, and the columns that are secretly free text. Use when a fresh
  extract lands from a partner or a nightly job and nobody knows yet whether it is usable. NOT for
  loading it into a warehouse (use warehouse-loader for that).
---

# CSV Profiler

Answers one question: can anything be built on this extract, and where will it break.

## Procedure

1. Count rows and columns before reading anything else, and compare against what the
   sender claimed. A silent truncation at export time is common and invisible later.
2. Infer a type per column from a sample, then verify it against the whole column.
   The column that is an integer in the first thousand rows and a string in row
   40,000 is the one that breaks the load.
3. Report null rate per column. A column that is 98 percent null is not a column.
4. Check the claimed key for duplicates and nulls. If it has either, say so before
   anyone writes a join against it.
5. Range-check numerics and dates. Dates in the future and negative quantities are
   the two that survive every other check.
6. Flag free-text columns. They carry delimiters, newlines, and personal data, and
   each of those is a separate problem.

See [the delimiter and encoding notes](references/missing.md) for the cases where a
file parses cleanly and is still wrong.

## Output

A table with one row per column: type, null rate, distinct count, min, max, and a
note where the column failed a check. Then a short verdict: usable, usable with
caveats, or send it back.

# Attribution

This skill began as a fork of **stephenturner/skill-deslop** (MIT) and was then
extended: the modes, the tiering, the false-positive gates, the answer-vs-deliverable
distinction, the maintenance protocol, and most of `patterns.md` were written here.
Substantial expression from the parent survives throughout, so the whole of it is
credited below rather than treated as incidental overlap.

Everything harvested *after* the fork was taken as ideas and written in original
words, per `references/maintenance.md`. Ideas and methods are not copyrightable;
expression is. Where post-fork expression did carry over, it is accounted for here.

The parent credited two sources of its own, **hardikpandya/stop-slop** and
**tropes.fyi**. Their material reached this skill through the fork, so both are
credited here too.

Measured 2026-08-20 with `tools/overlap.py`, 8-word runs, this skill against each
source: skill-deslop 6,169 shared runs (longest 1,189 words); stop-slop 741 (longest
108, inherited via the parent, which shares the same runs); blader/humanizer 48, being
a shared URL and one quoted example. An earlier note in this file claimed the catalog
was built by harvesting ideas alone and had been verified against every source. That
was wrong on both counts: the parent fork was not in the source list, so it was never
scanned, and the relationship is descent rather than harvest.

## MIT

**stephenturner/skill-deslop** — https://github.com/stephenturner/skill-deslop
Copyright (c) 2026 Stephen D. Turner. **This skill's parent.** Forked and renamed;
`deslop` is kept as a trigger word. `SKILL.md` and the `phrases`, `structures`,
`tropes` and `examples` references all descend from it.

**hardikpandya/stop-slop** — https://github.com/hardikpandya/stop-slop
Copyright (c) 2025 Hardik Pandya. Reached this skill through skill-deslop, whose
README credits it for "the phrase lists, structural patterns, before/after examples,
scoring rubric, and quick checks". The scoring rubric was dropped here; the rest of
that material is present.

**tropes.fyi** — https://tropes.fyi/, by Ossama Hassanein. Also inherited through
skill-deslop, whose `references/tropes.md` is adapted from it. This skill's
`references/tropes.md` descends from that file.

**conorbronsdon/avoid-ai-writing** — https://github.com/conorbronsdon/avoid-ai-writing
Copyright (c) 2026 Conor Bronsdon. `references/maintenance.md` records a local fork of this
that once ran ahead of upstream, so material from it is in the catalog. A 2026-08-20 scan
found 964 shared 8-word runs, all of them in `references/vocabulary.md` and all of them
inside word-substitution tables. Weigh that accordingly: a table of replacement pairs leaves
little room for two writers to differ, so the overlap is much weaker evidence of copying than
the same number would be in prose. Credited because a fork is recorded, not because the
shingle count alone would prove it.

**ehmo/slopkit** — https://github.com/ehmo/slopkit
Copyright (c) 2026 ehmo. Three ideas taken in 2.12, written in original words and scanned
clean: the brief-versus-artifact distinction, the invented-obligation carve-outs for support
and policy copy, and two Tier 1 words. Its own catalog duplicates this one almost entirely.

**blader/humanizer** — https://github.com/blader/humanizer
**petergyang/no-ai-slop** — https://github.com/petergyang/no-ai-slop
**cursor/plugins** — https://github.com/cursor/plugins, its `pstack/skills/unslop` skill.
Copyright (c) 2026 Lauren Tan. Full text at `pstack/LICENSE`; the repository root has none,
so automated license detection reports it unlicensed.

    MIT License

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

Material from `no-ai-slop` shaped `SKILL.md`'s intake questions and
`references/preflight.md`'s check ordering, with some phrasing carried over. 2.10 took two more
ideas from it, written in original words: interpretive metadiscourse, and the portability
framing that widened the interchangeable-sentence entry.

A note for future audits: the measured overlap with `no-ai-slop` rose from 85 to 99 shared
runs on 2026-08-19 without anything being copied. Their own checklist grew in a direction
that matched text we had already harvested in July, so the increase came from the source
moving toward us. The files edited in 2.10 show zero overlap.

From `unslop`, three ideas entered 2.9 written in original words: the abstract
metaphor-noun table in `references/vocabulary.md`, and the interchangeable-sentence and
dense-sentence entries in `references/patterns.md`. A scan on 2026-08-19 found no shared
phrasing. Its own pattern list independently reaches the same conclusion as ours on
straight quotes and takes a stricter line on em dashes.

## CC BY-SA 4.0

**Wikipedia: Signs of AI writing** —
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
**Wikipedia talk: Signs of AI writing** — the talk page of the above

Licensed CC BY-SA 4.0 by Wikipedia contributors:
https://creativecommons.org/licenses/by-sa/4.0/

Several short specimens of bad writing quoted in `references/tropes.md` come
from that article, quoted for criticism and identified as quotations. No
explanatory prose was copied.

## Ideas only, no expression carried over

**alexgreensh/attention-span** — https://github.com/alexgreensh/attention-span
(AGPL-3.0). The answer-vs-deliverable distinction and the "silent omission is
the worst failure" principle in `SKILL.md` were harvested as ideas. The overlap
scan found one 12-word clause in common; it was rewritten on 2026-08-16, and a
re-scan is clean. No AGPL-3.0 expression remains, so its copyleft does not
reach this skill.

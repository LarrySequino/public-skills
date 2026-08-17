# Attribution

This skill was assembled by synthesizing *ideas* from the sources below and
writing the entries in original words. Ideas and methods are not copyrightable;
expression is.

Verified 2026-08-16 by an 8-word-run overlap scan (`tools/overlap.py` in the
source repo) of every file in this skill against every source listed here.
Results are recorded per source.

## Apache-2.0

**pbakaus/impeccable** — https://github.com/pbakaus/impeccable
Licensed under the Apache License, Version 2.0:
https://www.apache.org/licenses/LICENSE-2.0

Contributed the category-reflex test and the idea of deterministic slop
detectors, which informed `references/design-tropes.md` and
`scripts/slop-scan.py`.

*Statement of changes (required by Apache-2.0 §4b):* no file from impeccable is
reproduced here. Its detection concepts were reimplemented from scratch against
this skill's own three-score model and trope catalog. The overlap scan found a
single 8-word fragment spanning a sentence boundary, consisting of color
terminology.

## MIT

**nutlope/hallmark** — https://github.com/nutlope/hallmark
**jaywilburn/refactoring-ui-skill** — https://github.com/jaywilburn/refactoring-ui-skill
**jezweb/claude-skills** — https://github.com/jezweb/claude-skills
**AccessLint/skills** — https://github.com/AccessLint/skills
**vercel-labs/web-interface-guidelines** — https://github.com/vercel-labs/web-interface-guidelines
**bencium/bencium-marketplace** — https://github.com/bencium/bencium-marketplace

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

`AccessLint/skills` contributed the idea of tagging findings by evidence basis and marking
criteria a tool cannot test as human-required rather than passed — which is why the
accessibility score now reports its coverage. `vercel-labs/web-interface-guidelines`
contributed the typographic micro-detail checks. `bencium/bencium-marketplace` contributed
the sharper reading of icon consistency (style and weight, not only family and size).
No text was taken from any of them; a 2026-08-17 scan found no shared phrasing.

`hallmark` contributed the slop-test gates and the two-briefs framing.
`refactoring-ui-skill` and `jezweb/claude-skills` informed the craft layer.
The overlap scan found no shared phrasing with `hallmark` or
`refactoring-ui-skill`. The only match against `jezweb/claude-skills` was a
string of WCAG 2.2 contrast thresholds (4.5:1 body, 3:1 large and UI
components) — facts, which carry no copyright.

## Ideas only — no license published upstream

**wonjyou/design-audit** — https://github.com/wonjyou/design-audit
**Ashutos1997/claude-design-auditor-skill** —
https://github.com/Ashutos1997/claude-design-auditor-skill

Neither repository publishes a license, so neither grants redistribution
rights. Nothing from either is redistributed here: the overlap scan found
**zero** shared 8-word runs with either, against every file in this skill.
Their contribution was conceptual only.

## Ideas only — no license published

**nolanperk/rad-spacing** — https://github.com/nolanperk/rad-spacing

No license, so no redistribution rights. Nothing is redistributed here. It contributed one
idea: spacing should encode nesting depth, each level roughly 1.4x its child, grounded in
Gestalt proximity. That idea is expressed here in original words and the scan confirms zero
shared phrasing.

## Standards cited, not reproduced

Target-size and contrast figures come from **WCAG 2.2** (W3C), Apple's **Human Interface
Guidelines**, and **Material Design 3**. Measurements are facts and carry no copyright; the
guidelines' prose does, and none is reproduced. Apple's HIG is copyright Apple Inc. and
Material's documentation is Google's.

**Not used:** Anthropic's `frontend-design` skill was examined and deliberately not
harvested. It is copyright Anthropic PBC, all rights reserved, under Commercial Terms of
Service — not open source.

## Predecessor

This skill extends an earlier `design-review` skill, which was developed
locally and installed from a local directory rather than from any marketplace
or public repository. The sources listed above under "Ideas only" and MIT are
that skill's documented lineage; all of them have been scanned.

## Third-party standards referenced

Nielsen's 10 Usability Heuristics · WCAG 2.2 (AA) · Refactoring UI
(Wathan/Schoger) · Gestalt principles · Fitts's / Hick's / Miller's laws ·
Apple HIG and Material target sizes · the 8-point grid. These are cited as
external standards; no text from them is reproduced.

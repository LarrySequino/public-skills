# Maintenance

How this skill stays current. Read only when refreshing it, not during a review.

Design slop differs from prose slop in two ways that shape everything below.

**It is partly visual.** A prose tell can be found by reading a catalog. "The icon
tile above the heading became universal" cannot — you notice it by looking at many
shipped screens. Reading repositories alone will always lag.

**It decays.** Prose tells are fairly stable; design tells turn over with fashion.
The 2022 set (purple gradients, glassmorphism, neon on black) has largely given way
to a 2026 "tasteful default" — cream backgrounds, italic serif heroes, icon tiles.
A trope nobody commits any more is not neutral, it is a false-positive generator.
So a sweep must **retire** as well as add. That is the main difference from
`natural-writing`'s protocol.

## Source watchlist

Check in this order, signal density descends.

1. **pbakaus/impeccable**, https://github.com/pbakaus/impeccable (Apache-2.0), the
   catalog at impeccable.style/slop. The closest thing this domain has to a canonical
   list, and the only one that is explicitly era-aware. Read the catalog and diff
   against `design-tropes.md`. It also ships `npx impeccable detect` and a browser
   extension — run the detector against a real project and note what it catches that
   `slop-scan.py` misses; that gap is the highest-value material on this list.
   Apache-2.0 requires attribution *and* a statement of changes — see `ATTRIBUTION.md`.
2. **jakubkrehel/skills**, https://github.com/jakubkrehel/skills (MIT), the seven core
   `better-*` skills, chiefly `better-typography` and `better-ui`. Never harvested.
   Skip the `great-*` and `oklch-*` drafts.
3. **nutlope/hallmark**, https://github.com/nutlope/hallmark (MIT). Contributed the
   slop-test gates and the two-briefs framing already in Group E. Check for new gates.
4. **garrytan/gstack**, https://github.com/garrytan/gstack (MIT), its `design-review`
   skill. Same domain, entirely independent lineage — a 2026-08-17 scan found zero
   shared phrasing. That independence is exactly what makes it worth diffing: where it
   reaches a conclusion we also reached, the conclusion is probably real; where it
   differs, one of us is wrong. Read the review dimensions, not the orchestration
   scaffolding, which is specific to its own tool suite.
5. **emilkowalski/skills**, https://github.com/emilkowalski/skills (MIT). Motion craft.
   Feeds the motion dimension and the motion section of `design-tropes.md`. Already
   tracked in the repo's `sync/skill-lock.json`, so diff by version there.
6. **Mobbin** (MCP connector). The visual channel, and the only source on this list
   that shows shipped product rather than commentary about it. Use it to test whether a
   candidate trope is actually widespread and whether a catalogued one has died. Sample
   across categories, not within one — a pattern that is universal in fintech and absent
   everywhere else is a category convention, not slop.
7. **wonjyou/design-audit** and **Ashutos1997/claude-design-auditor-skill**. Neither
   publishes a license, so **ideas only, never phrasing**. Both contributed conceptually
   to the craft layer and neither has ever contributed expression — a 2026-08-17 scan
   confirmed zero overlap. Keep it that way.
8. **AccessLint/skills**, https://github.com/AccessLint/skills (MIT). Five accessibility
   skills tiered by what is actually automatable: scan (rule engine), inspect (manual
   keyboard/AT), audit (full WCAG-EM), diff (regression), fix. Small repo, best-engineered
   on this list. Its evidence-basis tagging is what our Accessibility score is missing.
9. **vercel-labs/web-interface-guidelines**, https://github.com/vercel-labs/web-interface-guidelines
   (MIT). Note the Vercel *skill* in `agent-skills` is only a wrapper that fetches this file
   at runtime — read this repo, not the skill. Implementation-level where we are
   design-level, so most of it is out of scope; the typographic micro-details are not.
10. **bencium/bencium-marketplace**, https://github.com/bencium/bencium-marketplace (MIT).
   Its `design-audit` and `typography` skills. Same domain, dimension-table shaped, so it
   diffs cleanly against our Group A–E. Skip its heavyweight document pre-read protocol.
11. **nolanperk/rad-spacing**, https://github.com/nolanperk/rad-spacing. **No licence —
   ideas only, never phrasing.** Small and single-purpose: hierarchical spacing by Gestalt
   proximity.
12. **WCAG 2.2, Apple HIG, Material** — the numbers in `thresholds.md`. These move on a
   release cadence rather than continuously; check when a spec version ships, not every
   sweep. A changed threshold is a correctness bug here, not an enhancement.

Discovering newcomers: search for design-review, design-audit and AI-slop skills on
GitHub sorted by recent activity, and check what `impeccable` cites. Screen anything new
with the security pass in `skill-curator` before fetching it.

## Cadence

Sweep on request, and suggest one quarterly if it has not been asked for. Nothing here
is urgent — a reflex pattern takes months to become widespread enough to be worth
flagging, so a missed sweep costs little, while chasing every new example costs a full
package-and-publish cycle each time.

A sweep is the whole watchlist in ranked order. A single source can be checked alone
when named. The retirement pass (below) runs on every sweep regardless of what was added.

## Harvest criteria

A candidate trope earns inclusion only if it:

**(a)** is specific and named, with a concrete example — "generic hero" is not a trope,
"centered hero with two equal-weight buttons" is;
**(b)** carries a fix that is a *design move*, not a prohibition. "Don't use gradients"
is useless; "let the gradient carry meaning or cut it" is actionable;
**(c)** passes the false-positive test. The finding is the **reflex**, never the single
instance. If a trope would flag a deliberate, well-executed choice, gate it by density,
by co-occurrence with other tells, or by the absence of a stated reason — never ban it
flat. This gate matters more here than in prose: every item in the catalog is something
a competent designer sometimes does on purpose;
**(d)** is not already present — grep `design-tropes.md` first, since most "new" tropes
are renames of catalogued ones;
**(e)** never weakens **measure before you judge**. A trope must not license an eyeballed
verdict where a script could compute one, and no threshold enters `thresholds.md` without
a spec or platform guideline behind it. Never invent a number;
**(f)** is **era-stamped**. Record the year it was observed as current, because that is
what makes the retirement pass possible later.

Reject, even from good sources: scoring rubrics that add axes, per-framework advice,
and anything requiring a tool the skill does not bundle. This skill stays lean and
stdlib-only.

## Retirement pass

Run every sweep, before adding anything. For each section of `design-tropes.md`, ask
whether the pattern is still common enough to be worth flagging. Sample Mobbin across
categories rather than trusting memory.

Move dead tropes to a `## Historical` section with the year they stopped mattering —
do not delete them. Deleting loses the record and the next sweep re-harvests the same
item from an old catalog. A historical trope also stays useful for reviewing older
surfaces, and the section itself documents how fast this domain turns over.

`natural-writing` faced the same question about the em dash, where editors debated
moving it to a historical section. It was kept active with the justification changed
rather than the rule softened. That is the right shape: retire on evidence of
disappearance, not on the finding being inconvenient.

## Update procedure

1. **Edit in this repo.** `skills/craft-review/` is the source of truth. Do not edit an
   installed copy — see the repo README's one-way rule.
2. **Run the retirement pass** (above), then fetch sources per the watchlist and identify
   the delta since the logged state.
3. **Merge by destination.** Tropes → `references/design-tropes.md`, in the matching
   category section. Numeric thresholds → `references/thresholds.md`. Profile-specific
   criteria → `references/context-profiles.md`. Anything statically detectable in
   HTML/CSS → a new check in `scripts/slop-scan.py`, with a case in its `--demo`. New
   dimensions go in `SKILL.md` only if they change what every review does; keep it
   under ~200 lines.
4. **Update the harvest log below**, in the same pass, never afterwards from memory.
   Record rejections and their reasons — otherwise the next sweep re-evaluates the same
   material at full cost.
5. **Update `ATTRIBUTION.md`** if a new source contributed. Apache-2.0 sources need a
   statement of changes; MIT sources need the notice.
6. **Run the provenance scan. Not optional — this skill is published.**
   `./tools/overlap.py skills/craft-review <sources dir>`. Two sources on the watchlist
   publish no license at all, so a copied sentence from either is a real problem rather
   than a paperwork one.
7. **Package and publish.** `make craft-review`, upload `dist/craft-review.skill` at
   Settings → Capabilities → Skills, then `./publish.sh` for the public mirror.
8. **Report per source**: what was new, what was taken, what was rejected and why, and
   what was retired.
9. **Security scan** the packaged result. Harvesting from third-party repos can carry an
   injection payload into the output even when each source read clean. See `skill-curator`.

**Read the whole source, not the summary.** A catalog's README is usually a subset of
what its detector actually checks; the rules live in the code.

## Boundary with `deslop`

`design-tropes.md` has a UI-copy section that overlaps the prose anti-slop skill. The
split: if the fix is to change *words*, it belongs to `deslop`. If the fix is to change
*layout, type, colour or motion*, it belongs here. Microcopy that is only wrong because
of where it sits — a button label that has to be long because the layout gives it no room
— is ours. Keep both catalogs pointing at each other rather than duplicating entries.

## Harvest log

Current version: 1.1.1.

| Source | Last checked | State at check |
|---|---|---|
| pbakaus/impeccable | 2026-08-17 | Apache-2.0 confirmed. Category-reflex test and deterministic-detector concept already harvested. **Pending:** a 72-line addition covering the 2026 "tasteful default" set — cream/beige backgrounds, italic serif display heroes, icon tiles above headings, repeated section kickers, numbered section labels. Not yet merged; tracked as a repo issue. Detector CLI never run against a real project. |
| nutlope/hallmark | 2026-08-17 | MIT. Slop-test gates and two-briefs framing harvested into Group E. Zero shared phrasing on scan. |
| jakubkrehel/skills | 2026-08-17 | MIT, ~3.8k stars. **Never harvested.** Take the seven core `better-*` skills, chiefly `better-typography` and `better-ui`; skip the `great-*`/`oklch-*` drafts. Highest-value unworked source on the list. |
| garrytan/gstack | 2026-08-17 | MIT, ~128k stars. Its `design-review` skill scanned zero-overlap against this one — independent lineage, never harvested. Its SKILL.md is ~110KB but mostly orchestration; the review dimensions are the harvestable part. Note its install instructions pipe a remote script to a shell. |
| emilkowalski/skills | 2026-08-17 | MIT. Ten skills upstream. Motion material feeds the motion dimension. Version tracked in the repo's `sync/skill-lock.json`. |
| wonjyou/design-audit | 2026-08-17 | **No license published.** Contributed conceptually to the craft layer. Scan confirms zero expression copied. Ideas only, permanently. |
| Ashutos1997/claude-design-auditor-skill | 2026-08-17 | **No license published.** Same status as above; zero overlap confirmed. |
| Mobbin | never | Connector available, never used as a harvest source. This is the visual channel and the only way to run a credible retirement pass. |
| AccessLint/skills | 2026-08-17 | MIT, ~84 stars. **Never harvested.** WCAG-EM methodology; five skills tiered by automatability. **Take:** evidence-basis tagging on findings, and an explicit human-required marker for criteria a screenshot review cannot verify (keyboard operability, focus order, SR output). Our Accessibility /100 currently overclaims without it. Highest-integrity find of the sweep. |
| vercel-labs/web-interface-guidelines | 2026-08-17 | MIT, ~777 stars. **Never harvested.** The real source behind the Vercel skill, which is a 176-word wrapper. **Take:** typographic micro-detail — `…` not `...`, curly quotes, non-breaking spaces, widow prevention on headings — plus "interactive states increase contrast" and long/empty content handling. **Reject:** hydration, virtualization, `min-w-0` and framework specifics. Wrong layer; we review screens, not React. |
| bencium/bencium-marketplace | 2026-08-17 | MIT, ~392 stars, 16 skills. **Never harvested.** `design-audit` is the domain match. **Take:** iconography as a dimension (consistent style/weight/size, one set vs mixed libraries — we have none), empty states, and dark mode as a dimension rather than only a trope. **Reject:** its pre-read protocol (DESIGN_SYSTEM, PRD, APP_FLOW, TECH_STACK, LESSONS) as bureaucracy; our §3 is leaner. `typography` skill unread. |
| nolanperk/rad-spacing | 2026-08-17 | **No licence, ideas only.** ~13 stars, one file. One strong idea: spacing should encode nesting depth, each level roughly 1.4x its child, snapped to the 8px scale, grounded in Gestalt proximity. We check on-grid and consistent stepping but never that spacing *encodes hierarchy* — a screen can be perfectly on-scale with card padding equal to page padding. Computable, so it belongs in `symmetry.py`. Highest single-idea value of the sweep. |
| anthropics/claude-code frontend-design | 2026-08-17 | **(c) Anthropic PBC, all rights reserved, Commercial ToS. Not open source.** Most restrictive source examined. Assessed 2026-07-14 as strong on visual identity, thin on motion. Low marginal value against our current coverage, highest legal risk. **Do not harvest.** Listed here so future sweeps do not re-evaluate it. |
| nextlevelbuilder/ui-ux-pro-max-skill | 2026-08-17 | MIT, ~117k stars. A design *generator* driven by a search/RAG query contract, not a reviewer. Different job, little to harvest for a review skill. Its master-plus-overrides design-system persistence pattern is the only part worth revisiting, and only if `design-system.md` grows. |
| WCAG / Apple HIG / Material | 2026-08-17 | `thresholds.md` reflects WCAG 2.2 AA, Apple 44pt, Material 48dp. Re-check when a spec version ships. |

## Self-application

This skill is subject to its own Group E. The catalog must not become a checklist that
flags every considered choice, and the three-score model must not grow a fourth score.
If a sweep adds more than it retires two passes running, the catalog is drifting toward
a rubric — cut before adding.

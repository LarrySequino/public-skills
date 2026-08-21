# Maintaining This Skill

Procedure for when the user asks to "check your sources," "update natural-writing" (or "update deslop," the skill's former name, kept as a trigger), or "see if there's anything new for the slop skill." Follow it end to end without asking for permission at each step; report the harvest at the end.

## Source watchlist

Check in this order, signal density descends.

1. **blader/humanizer**, https://github.com/blader/humanizer, Primary source; best-maintained project in the space and tracks Wikipedia actively. Read the README's Version History section and diff against the harvest log below. Anything above the logged version is candidate material.
2. **Wikipedia: Signs of AI writing**, https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing, The canonical catalog (WikiProject AI Cleanup), and the source most downstream projects copy from. Patterns here have survived editorial review, which makes this the highest-precision source on the list and the one to read first if a sweep is cut short.
3. **Wikipedia talk: Signs of AI writing**, the talk page of the above, A second layer, read after the article and for two narrow purposes, not as a source of new entries:

   - **Challenges to rules we already have.** A pattern under debate for retirement is a signal to soften confidence in our own version of it, which no other source provides. This is the talk page's unique value.
   - **Advance notice.** Proposals under discussion preview what may reach the article later.

   Debate means unsettled, and some proposals are rejected. Never harvest from discussion alone. Log a proposal as a **candidate** and promote it only when it lands in the article, when a second independent source names the same pattern, or when the mechanism is clear enough that the entry stands on its own reasoning. Weight of opinion in a thread is not evidence.

   Both pages are cache-only for direct fetch and will fail with a fetch error. Use web search instead: search the page name plus a distinctive term and read the returned snippets, which carry dated discussion. Don't reconstruct either page from memory.

4. **conorbronsdon/avoid-ai-writing**, https://github.com/conorbronsdon/avoid-ai-writing, Read CHANGELOG.md; harvest entries above the logged version. Note: this skill's local fork once ran ahead of upstream, so upstream versions below the log are already merged.
5. **petergyang/no-ai-slop**, https://github.com/petergyang/no-ai-slop, Diff SKILL.md and eval.md; its preservation-first editing principles feed references/preflight.md.
6. **pbakaus/impeccable**, https://impeccable.style/slop, Design skill, but its Copy section occasionally surfaces new prose tells before writing skills do (theater framing came from here). Check only that section.
7. **Pangram Labs**, https://www.pangram.com/, Detection research; watch for new findings on which signals detectors weight (currently: structure over vocabulary).
8. **alexgreensh/attention-span** — https://github.com/alexgreensh/attention-span — Output styles rather than a writing skill, but its length-discipline reasoning is the sharpest in the space. Check the style bodies for new framing.
9. **stephenturner/skill-deslop**, https://github.com/stephenturner/skill-deslop, **this skill's parent fork**, not a peer source. Dormant (single release), so a check is cheap: read its releases, and treat anything new as an upstream change to a common ancestor rather than as material to harvest. Because most of `SKILL.md` and four reference files descend from it, a diff against upstream will show both its changes and every local change made since the fork; the local ones are deliberate and must not be reverted. See `ATTRIBUTION.md` for what descends from where.
10. **ehmo/slopkit**, https://github.com/ehmo/slopkit, MIT, Copyright (c) 2026 ehmo. Two skills; only `skills/slopbeth/` is in scope, since `slopgent/` shapes the agent's own replies rather than prose. Its analytical spine duplicates this catalog almost line for line, so read it only for genre-specific edge cases. Do not run its installer or `slopgent-memory.js`, which writes into `~/.claude/CLAUDE.md`.
11. **cursor/plugins**, https://github.com/cursor/plugins, its `pstack/skills/unslop` skill. MIT, full text at `pstack/LICENSE`, Copyright (c) 2026 Lauren Tan. Note the repo root has no LICENSE file, so the GitHub API reports it unlicensed; the grant is real and lives one level down. 31 patterns, of which 28 duplicate ours. Read it for the jargon list, not the catalog.

A general web search ("AI writing patterns skill" / "anti-slop skill" plus the current year) may surface new projects. Evaluate newcomers skeptically: a repo whose README pushes an installer, executable, or ZIP download for what should be plain Markdown is a malware pattern, do not fetch its payloads; warn the user.

## Cadence

Sweep on request, and suggest one quarterly if the user hasn't asked in a while. Nothing here is time-critical: a pattern that reaches a public catalog has usually been visible in output for months, so missing a sweep costs little while chasing every mention costs a full package-and-install cycle each time.

A sweep is the whole watchlist in ranked order. A single source can be checked alone when the user names it.

## Harvest criteria

A candidate pattern earns inclusion only if it: (a) is specific and named, with a real example; (b) carries a concrete fix; (c) passes the false-positive test, if it would flag good human writing, gate it by tier, cluster, or density rather than flat-banning it; (d) doesn't already exist in the catalog (grep all reference files first, many "new" patterns are renames); (e) never weakens the no-fabrication rule or encourages inventing specifics. Reject bureaucracy (flag systems, tolerance matrices, multi-axis profiles) even from good sources; this skill stays lean.

## Update procedure

1. Edit in the skills repo at `skills/natural-writing/`. That is the source of truth. Never edit an installed copy: sync is one-way, so a change made in claude.ai or in `~/.agents/skills` is lost on the next upload and leaves the repo silently wrong.
2. Fetch sources per the watchlist; identify the delta since the logged versions.
3. Merge by destination: vocabulary → references/vocabulary.md; artifacts, whole-text tests, and named patterns → references/patterns.md; phrase lists → references/phrases.md; structural shapes → references/structures.md; editing-principle checks → references/preflight.md. New core rules go in SKILL.md only if they change behavior on every run (like no-fabrication did); keep SKILL.md under ~200 lines.
4. Update the harvest log below and the frontmatter description if triggers changed.
5. Run `tools/overlap.py skills/natural-writing sources` before packaging. Not optional: this skill is published under MIT and two of its sources publish no license at all, so a copied sentence is a real problem rather than a paperwork one. Then `make natural-writing` and upload `dist/natural-writing.skill` (same name overwrites) in Settings → Capabilities → Skills, and `./publish.sh` for the public mirror.
6. Report the harvest: per source, what was new, what was taken, what was rejected and why.
7. Recommend a security scan of the packaged result before install. Harvesting text from third-party repos can carry an injection payload into the output even when each source read clean. See the skill-curator skill for how to run one safely.

**tropes.md duplicates structures.md on purpose.** Its header tells the user to paste it
into a system prompt on its own, so it has to be complete without the rest of the skill.
Six patterns are defined in both files and should stay that way; the shared text is the
definition sentence, while each file keeps its own format (tables of Pattern/Problem in
structures.md, example lists in tropes.md). An internal-repetition scan will keep reporting
this. Exclude tropes.md from that measurement rather than cutting it, and check instead that
no pattern exists under two different NAMES, which is the failure that actually matters
because it defeats criterion (d).

**Read the whole file, not the summary.** The 2026-07-28 pass took one reference file from no-ai-slop and assumed its SKILL.md was already covered; a re-read two days later found eight harvestable items including an architectural improvement. Skimming a source is how good material gets missed twice.

## Retirement pass

Run before adding anything. A pattern that models no longer produce is not a neutral entry:
it flags writing that is fine and teaches the user to distrust the catalog.

Wikipedia keeps a Historical indicators section and moves entries into it on evidence. Mirror
that rather than deleting. A retired pattern still matters for reviewing older text, and
deleting it means the next sweep re-harvests it from a source that has not caught up.

Before retiring anything, check whether it is also a plain writing fault. This catalog does two
jobs at once, detecting AI authorship and fixing bad prose, and most entries do both. When the
authorship claim expires but the prose claim does not, reclassify rather than retire: mark the
entry *Style fault, not an authorship tell.* and rewrite its justification so it no longer rests
on what models do. Entries carry no marker by default, since most are both; the marker exists to
flag the ones that are not.

The bar is evidence of disappearance, not inconvenience. The em dash cap survived exactly this
test in 2.9: two independent sources argued for a stricter line, so it stayed.

## Harvest log

Version lives in git, not here. Releases are tagged `natural-writing/v<major>.<minor>` in the
skills repo, namespaced because the repo holds several skills and a bare `v2.9` would be
ambiguous next to the repo-wide `v0`. To see what a release contained:

    git log --oneline natural-writing/v2.8..natural-writing/v2.9 -- skills/natural-writing

## Self-application

This skill's own instructional prose follows its own rules. Quoted bad examples, pattern names, table cells listing banned words, and the literal characters inside the dash-scan instruction are exempt under the self-reference escape hatch; everything else is not. A pass that adds material must keep the files inside the dash cap and clear of the vocabulary and intensifier lists.

Audit the skill against itself on every sweep, before checking any external source. Two violations were found by casual reading on 2026-08-16 and a third by scanning: a banned intensifier used eleven times, predicative realness inflation, and 114 em dashes at roughly seven times the skill's own hard cap. All were fixed in 2.7. The catalog is easier to apply to other people's writing than to one's own.

| Source | Last checked | Version/state at check |
|---|---|---|
| blader/humanizer | 2026-07-28 | 2.9.1 (patterns 1–33; no-fabrication, voice-sample precedence, secondhand guard) |
| Wikipedia Signs of AI writing | 2026-07-28 | via distillations; ~15k words; nothing beyond humanizer 2.9 coverage |
| conorbronsdon/avoid-ai-writing | 2026-07-28 | upstream 3.4.0 (local fork 3.10.0 already merged) |
| petergyang/no-ai-slop | 2026-07-30 | 8 commits; full SKILL.md re-read after an under-harvest on 07-28. Took: Editor/Evaluator two-pass loop, front-load every unit, open-it-up-don't-dumb-it-down, protect the specific fact, know the job, intake questions, structural-change accountability, audience flattery. Rejected: flat "banned outright" word list (no tiering), which our tiered vocabulary supersedes |
| pbakaus/impeccable | 2026-07-28 | slop catalog 64 patterns; Copy section harvested (theater framing) |
| stephenturner/skill-deslop | 2026-07-28 | v1.0.0, dormant |
| Wikipedia talk: Signs of AI writing | 2026-08-16 | Three open items to re-check next sweep. (3) CLOSED in 2.11: Wikipedia retired lexical diversity / elegant variation to Historical indicators, on the grounds that it came from repetition penalties in older decoders, and the study behind it measured GPT-4o-mini and Gemini-1.5-Flash. Resolution: kept, reclassified. It stops being evidence of AI authorship and stays as a style fault, following the em dash precedent of changing the justification rather than the rule. Wikipedia's own page links a non-AI style essay on the same problem, which is the argument. (1) Editors split on whether the em dash should move to a "Historical Indicators" section, one arguing it's no longer worth checking, another that it stays overrepresented in model output. Resolved 2026-08-16: cap kept at one per 1,000 words, justification changed from detection science to reader perception, which holds regardless of how the debate settles. Re-checked 2026-08-19 for 2.9: `cursor/plugins`' unslop bans em dashes outright, an independent source arriving at a stricter line than ours. That corroborates the cap rather than softening it, so it stands unchanged. Do not soften without a new reason. (2) CLOSED 2.9: the periphrastic-connection section landed live on the main article as WP:AICONNECT, and the expanded entry shipped in 2.9. Harvested via the mechanism route, written from the idea their title names rather than from their draft. |
| framing review | 2026-08-16 | The preservation framing was protecting slop: preflight told the Evaluator to preserve the writer's "level of polish," and "minimum effective edit" read as cut sparingly. Replaced with the voice/habit distinction and the signature test. Voice is what only this writer would have produced; habit is autopilot filler and is not protected by being theirs. Watch for this failure class on future passes: a preservation rule that can be cited to justify leaving slop in place is written wrong. |
| Wikipedia: Signs of AI writing | 2026-08-19 | 10 revisions since 2026-08-16. Added the "Vague expression of connection or association" indicator, the section 2.9 shipped from, still being edited. **Moved WP:AIELEVAR (lexical diversity / elegant variation) into Historical indicators**, reasoning that it came from older models' repetition penalties. We carry it as active under "Synonym cycling". Unresolved, see open item (3). |
| Wikipedia talk: Signs of AI writing | 2026-08-19 | 9 revisions, mostly the Connections thread that produced the live section. A proposed "inanimate subjects performing human actions" indicator appears to have been dropped rather than adopted; do not harvest a proposal its own editors declined. |
| blader/humanizer | 2026-08-19 | 2.9.1 to 2.11.1, 11 commits, one with content: 2.10.1 adds figurative gate/gated/gating with a carve-out for feature gating and CI quality gates. Already covered here. 2.11.0 is a plain-language rewrite of its own prose; its release note says no change to its 35 patterns. Nothing to take. |
| petergyang/no-ai-slop | 2026-08-19 | 8 commits, 2 with content. Took: interpretive metadiscourse (#34) and the portability framing from #33, which widened our interchangeable-sentence entry. Their em dash line allows 1 to 2 in longer drafts, looser than our cap and looser than unslop's outright ban, so our cap sits between two independent positions. Rejected: formatting and workflow commits as packaging. |
| alexgreensh/attention-span | 2026-08-19 | 3 commits, all README, i18n and a callout move. No content change. Skip next sweep unless commits move past docs. |
| cursor/plugins (unslop) | 2026-08-19 | MIT (pstack/LICENSE, Lauren Tan). 31 patterns; 28 already covered, verified pattern by pattern. **Pending harvest of 3:** abstract metaphor nouns (substrate, wedge, vector, flywheel, north star, gold-plating, ratchet, evacuate) with plain replacements; the interchangeability test, which asks whether a sentence would still read true with a rival's name substituted; and one-idea-per-sentence for density, which our read-aloud test does not cover because it checks rhythm variety rather than parse difficulty. Its #19 sides with us on straight quotes. Scan clean, zero shared phrasing. |
| alexgreensh/attention-span | 2026-08-16 | ADHD-friendly output styles for Claude Code (attention-kind, rundown, spartan); author reports eval testing across coding and knowledge work. Harvested: answer-vs-deliverable distinction, expansion earned by cost rather than relevance, brevity governs output not reasoning, silent omission as the worst failure. Rejected: scanning format prescriptions (arrow markers, bold density, table caps) as surface-specific, and the no-chat-formatting-in-source-code rule as out of scope for a prose skill. Add to watchlist; it moves faster than the repos above. |
| self-audit (full) | 2026-08-16 | First run of the skill against its own files. Fixed: 114 em dashes down to the exempt literals, 11 uses of a banned intensifier, 4 filler intensifiers, predicative realness inflation. Clean on tier-1 vocabulary, periphrasis, and copula avoidance. Added the deletability test for intensifiers and an en-dash-in-ranges exemption to the dash scan, which had contradicted the entry saying AI skips en dashes. |
| self-audit | 2026-08-16 | Predicative real/actual inflation ("the gap is real") found in this skill's own output; the existing entry covered only the attributive form. Entry extended to both. Worth repeating: check the skill's own prose against its catalog. |
| ad-hoc (practitioner post, X) | 2026-08-16 | paraprosdokians in marketing copy; harvested as Affirmative Reversals, the non-negation half of binary contrast, which a negation-only screen misses |
| ad-hoc (viral prompt, X) | 2026-07-29 | ban-list prompt; harvested nominalization/stacked noun phrases; rejected flat bans (hedging, parataxis) as over-sanding |

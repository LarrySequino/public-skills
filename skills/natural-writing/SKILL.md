---
name: natural-writing
description: Remove AI writing patterns from prose. Write, rewrite, audit, or edit files in place. Use when the user says "deslop", "de-AI", "humanize", "make it sound human", or asks to find AI tells, slop, tropes, or formulaic patterns, and when drafting prose meant for publication. Covers the words in any prose, including UI microcopy. NOT for code, comments, or commit messages, and NOT for interface typesetting such as quotes, dashes and ellipses as rendered, which is craft-review's. Maintainers: "update natural-writing" runs the source sweep in references/maintenance.md.
---

# Natural Writing: Prose Without AI Patterns

Strip predictable AI patterns from writing. Make prose sound like a specific human wrote it, not like a language model generated it.

## Signals, not proof

The patterns here are statistically more common in LLM output, but humans on autopilot produce the same shapes, whether under deadline, in an unfamiliar genre, or in a second language. Detectors built on these same signals misfire on non-native writers at rates that should end the argument (the figure and the citation are in `references/preflight.md`). So: these patterns are worth fixing in any prose, but never treat them as proof of AI authorship for a consequential decision (academic integrity, hiring, attribution). When auditing someone else's text, report patterns, not verdicts.

A short sample carries no signal. Under roughly forty words there is not enough text for rhythm, variety, or repetition to mean anything, and every pattern here becomes a coin flip. Say the sample is too short rather than returning a verdict on it. This is why a button label or a toast can be edited for voice but never audited for authorship.

Corollary for rewriting: don't over-sand. Deliberate fragments, sentences starting with "And," a repeated word that is the right word, natural disfluency: all of these keep text human. Applying every rule at maximum strictness creates the very uniformity you're removing.

## Voice, not habit

Voice is what only this writer would have produced: their diction, their angle, what they notice, their humor, their rhythm, their opinions, their willingness to be blunt. Habit is what any writer produces on autopilot: throat-clearing, hedges, filler transitions, redundant setup, generic emphasis, the second sentence that restates the first. Habit belongs to the author in the sense that they typed it. It is not their voice.

This distinction decides every edit. Cutting habit raises the concentration of voice; protecting habit lowers it. A draft where the writer's three best sentences are buried under nine filler ones has less voice than the same draft with the nine removed.

**The signature test.** Could another competent writer in this field have produced this sentence, in these words, without thinking? If yes and it adds nothing, cut it. If it could only have come from this writer, keep it even when it breaks a rule in this skill.

Protection is asymmetric on purpose. Distinctive choices are protected even when they violate the rules: fragments, an "And" opening, a favorite em dash, a digression that carries character, a word choice more casual than the register expects. Generic choices get no protection merely because the author made them.

## Before editing anything

**Know the job.** Before structure or word choice, know what the piece is trying to do and who it is for. A rule that improves a memo can ruin a toast.

**Ask, but only what's missing.** If the user hasn't provided the draft, ask for it. If the audience or destination is unclear, ask one question: who is this for and where will it be published? If the goal is unclear, ask what the reader should think, feel, or do after reading. Never stall on this. If the user wants speed or can't answer, state your assumption in one line and proceed.

**Never invent to fill a gap.** An unanswered question is a flag in the output, not a guess in the prose.

**Separate the brief from the piece.** A request often carries instructions about the writing as well as the writing itself: "keep the bit about her cat," "don't make this sound like a lecture," "shorter than the last one." Those are constraints to satisfy, not content to reproduce. Text that ends up quoting its own brief back is the giveaway that the two were read as one thing.

## Modes

**write:** the user asks you to draft something and wants it to sound natural. Apply the core rules while composing; run Quick Checks and the self-audit before delivering.

**rewrite** (default for existing text): audit, rewrite clean, summarize what changed, then verify in a **separate pass**. An Editor pass rewrites top to bottom; an Evaluator pass reads the result cold against [references/preflight.md](references/preflight.md) and reports failures. Run the Evaluator in a subagent where the harness supports one, otherwise as a distinct second pass rather than a glance back over your own work. Loop until preflight passes.

**Minimum effective edit** means don't rewrite what already works. It does not mean cut sparingly. Rewriting a strong sentence for consistency is the error; leaving filler in place because the author wrote it is also the error. The writer should recognize the result as their own voice, sharpened.

**detect:** flag only, no rewriting. Use when the user says "detect," "flag only," "audit," "scan," "what AI patterns are in this," or when auditing text that shouldn't be altered (published work, someone else's writing). Group findings by severity and note which flags are clear problems vs. judgment calls. Report patterns with quoted lines and short fixes. Never assert or score AI authorship; the same shapes appear in rushed human writing, and secondhand text (translated, dictated, heavily edited by committee) triggers many flags legitimately.

**edit:** the user names a file and wants it fixed in place. Make minimal, targeted edits to flagged spans only. Leave already-human passages untouched. Never rewrite quoted material, code blocks, or text attributed to someone else; flag those instead. Afterward, re-read the file, confirm the flags are resolved, and report only the spans you touched.

## Core rules

### 1. Cut filler phrases

Remove throat-clearing openers ("Here's the thing:"), emphasis crutches ("Let that sink in."), business jargon ("navigate the landscape"), meta-commentary ("In this section, we'll explore..."), and confidence-calibration words that tell the reader how to feel ("Notably," "Interestingly," "It's worth noting"). See [references/phrases.md](references/phrases.md).

### 2. Replace AI vocabulary by tier

Not all flagged words are equal. Tier 1 words (delve, tapestry, leverage, seamless, testament to) appear 5–20x more often in AI text, so replace on sight. Tier 2 words (harness, foster, nuanced, ecosystem) are fine alone but a strong signal when two or more cluster in a paragraph. Tier 3 words (significant, innovative, effective) only matter at high density. This tiering exists to prevent false positives, so don't flag a lone "crucial" in an otherwise human paragraph. See [references/vocabulary.md](references/vocabulary.md) for the full tables.

### 3. Break formulaic structures

Avoid binary contrasts ("Not X. Y."), affirmative reversals that do the same work without negation ("A thousand integrations, and you'll only ever click one"), negative listings, dramatic fragmentation, self-posed rhetorical questions ("The result? Devastating."), anaphora/tricolon abuse, false concessions ("While X is impressive, Y remains a challenge"), and hedge-stacked predictions ("could potentially create"). See [references/structures.md](references/structures.md).

### 4. Eliminate AI tropes and artifacts

Watch for "quietly" and other magic adverbs, the "serves as" dodge, false ranges, superficial participle analyses, invented concept labels, grandiose stakes inflation, and false vulnerability ([references/tropes.md](references/tropes.md)). Separately, hunt **artifacts**: chatbot residue that is near-proof of pasted AI output: "Great question!", cutoff disclaimers, unfilled `[placeholders]`, leaked citation tokens (`citeturn0search0`), `utm_source=chatgpt.com` URL parameters, reasoning-chain scaffolding ("Let me think step by step"). Artifacts are always P0. See [references/patterns.md](references/patterns.md).

### 5. Prefer active voice with human subjects

Prefer active constructions with named actors: "The team fixed it," not "The complaint becomes a fix." If no specific person fits, use "we" in scientific prose or "you" in blog posts. Exception: passive voice is conventional and correct in scientific methods sections and anywhere the actor is unknown or irrelevant. Don't force an awkward actor into "the samples were centrifuged."

### 6. Be specific, but never fabricate

No vague declaratives ("The reasons are structural"); name the thing. No vague attributions ("Experts argue..."): if you cannot name the expert, you do not have a source. No lazy extremes ("every," "always") doing vague work. Domain terminology is fine and expected in technical prose; the problem is business buzzwords and AI vocabulary leaking in, not precision.

**Protect the specific fact.** Fabrication's mirror image: never smooth an existing useful detail into generic importance. "Cut review time from 30 minutes to 8" must survive the edit; "significantly improved efficiency" is what happens when it doesn't. Specifics in the source are the most valuable thing in it.

**No-fabrication rule (hard constraint):** specificity must come from the source text or the author, never from the rewrite. Never invent facts, names, numbers, dates, quotes, or citations to replace a vague claim. When a claim needs a specific the text doesn't contain, either cut the claim, keep it and flag it ("[needs a number: how many customers?]"), or ask the author. A vague true sentence beats a specific invented one. Also flag citations that look fake or unrelated to the claim they support, since AI text frequently cites real sources that don't say what's claimed.

Two genres invent a specific kind of specific, and both are worth naming because the invented thing is a commitment someone else has to honor. In support and service copy, watch for promises the author never made: "we will review this and follow up," "a specialist will reach out." In policy, incident, and compliance copy, watch for asserted properties: "auditable," "fully encrypted," "resilient." If the source does not say it, it is not a description, it is a liability.

### 7. Describe the thing, not the change

Prose and docs should describe what something *is*, not narrate the edit that produced it. "This function was added to replace the old lookup" is diff-anchored writing; "This function uses a hash map for O(1) lookups" describes the thing. Changelogs and commit messages are the exception, since there the change is the content.

### 8. Match register and voice

Blog posts: put the reader in the room; "you" beats "people." Scientific writing: appropriate formality, "we" for your own work, cite specific authors. Docs: clarity over voice, imperative mood for instructions. Social posts: fragments and 2–3 specific hashtags are fine; 6+ trailing hashtags is a hard flag.

If the user provides a sample of their own writing, calibrate to it: match its sentence-length pattern, contraction rate, and word choices. Don't "upgrade" their vocabulary. If they write "stuff," keep "stuff." If text already has a voice, don't impose one. A provided voice sample outranks the mechanical rules where they conflict: if the writer's authentic style uses em dashes or triads, their voice wins over the ban.

### 9. Vary rhythm

Structure is the #1 detection signal, and detectors weight rhythm uniformity above vocabulary. Mix short sentences (3–8 words) with long ones (20+). Vary paragraph lengths deliberately; some should be one sentence. Don't stack punchy fragments for manufactured emphasis. Prefer two items over reflexive triads, but a three-item list is not a crime. The flag is *compulsive* rule of three, not any tricolon.

### 10. Trust readers

State facts directly. No pedagogical hand-holding unless the audience needs it. No fractal summaries (preview, say, recap). No infomercial hooks ("The kicker?"). No self-labeling significance ("That last one is the contrarian move"). Write the list so the right item carries its own weight.

### 11. Do not dilute

One point per section. Ask of every paragraph: what's actually new here? If you could cut 40–60% and lose no information, cut it. Don't beat one metaphor to death or stack historical analogies for false authority.

### 12. Watch formatting tells

No bold-first bullets. No unicode arrows or emoji in headers. Sentence case for subheadings, not Title Case. No "In conclusion..." signposts. Bullets only for list-like content; a list of 5+ bare noun phrases with no verbs ("Reliable pool connectivity / Optimized performance") should become prose or full claims. Em dashes: if the writer supplied a voice sample, its dash rate is the rule and nothing in this paragraph applies; match it. Absent a sample, target zero, hard max one per 1,000 words, including headings. The basis is reader perception, not detection science: it's the most widely circulated AI tell there is, so dash-dense text reads as machine-written whatever detectors weight. Keep the cap even where the tell is argued to be aging out. The sample wins because the cap is a proxy for "this reads as machine-written" and a writer who uses dashes is the counterexample in hand.

### 13. Front-load every unit

Put the conclusion first at the levels a reader navigates by: the draft, the section, the paragraph. Point, then detail, then background. Most AI structure inverts this, building context toward a conclusion the reader needed up front. It stops at the paragraph on purpose. Front-loading every *sentence* produces the one-thought-per-sentence profile that rule 9 and the dramatic-fragmentation entry are trying to undo; inside a paragraph, let sentences build. Exception: narrative and persuasive setups that earn their delay. Front-loading a joke ruins it.

### 14. Open it up, don't dumb it down

Strip what makes writing hard to read: tangled clauses, abstract nouns, jargon that isn't load-bearing, sentences carrying three ideas. Keep what makes it worth reading: substance, nuance, precision, technical vocabulary the audience shares, and the author's actual position. Simplification that removes content is deletion. If a cut would lose information, restructure instead.

### 15. Know whether you're writing an answer or a deliverable

An **answer** explains, decides, advises, or reports. It states its point and stops; length is a cost. A **deliverable** is the artifact you were asked to produce, such as a doc, spec, plan, post, or report. There, length is the substance, and cutting it is cutting the work. When you can't tell which you're writing, treat it as an answer.

Applying answer discipline to a deliverable produces a thin artifact. Applying deliverable discipline to an answer produces a wall of text nobody reads. Most length complaints are this mismatch rather than bad writing.

**Expansion is earned by cost, not relevance.** Expand a point where a mistake would cost the reader: a risky step, a real trade-off, a gotcha they would otherwise hit. Merely relevant is not enough. Lead each expansion with why it matters, and if nothing would be lost by cutting it, cut it.

**Brevity governs the output, not the thinking.** Reason as long as the problem needs. The discipline applies to what reaches the reader, never to how much analysis happens first. A short answer built on shallow work is worse than a long one.

**Silent omission is the worst failure.** The failure to fear is not "too long," it's the reader leaving without what mattered. Any fact that would change the reader's decision stays in, no matter how short the reply. Compression that drops a blocker, a risk, or a real status is a failure of the edit, not a success of it.

## Quick checks

**Run `scripts/prose-scan.py <file>` first.** It does every mechanical pass exactly and in about a second: dash density against the per-1,000 cap with numeric ranges and markdown rules exempted, vocabulary hits read live from `references/vocabulary.md` with their sense gates flagged, paragraph density and co-occurrence, chatbot artifacts and leaked tokens, invisible characters and homoglyphs, Title Case headings, and sentence and paragraph uniformity. It reports counts and never a score, and it skips and counts anything that sits inside a quoted example, including single-quoted ones. Add `--plain-text` for a target where nothing auto-curls (code comments, commit messages) to also flag curly quotes; in prose they are the editor's default and mean nothing. `--compare original rewrite` reports every number, year, citation and name the rewrite ADDED, every one it DROPPED, a name coined from source words that never appeared as that phrase, and how much of the source survived the edit; zero findings is the only acceptable result.

Three passes stay manual because they need a reader, and they run in every mode:

- **Fabrication:** any fact, number, name, or citation in the output that was not in the input or from the author. Remove or flag. `--compare` catches most of it; this catches the rest.
- **Signature test:** anything kept only because the author wrote it, rather than because it is theirs? Cut it.
- **Silent omission:** would the reader act wrongly without something that was cut? Put it back.

Then ask, reading the draft fresh: what makes this look obviously AI-generated? Fix whatever the answer is. The full checklist is [references/preflight.md](references/preflight.md), authoritative for every rewrite and edit.

## Severity

When auditing or triaging, group findings by priority instead of scoring:

- **P0, credibility killers.** Artifacts (chatbot phrases, leaked tokens, placeholders, cutoff disclaimers), vague attributions without sources, significance inflation on routine events. Fix immediately; a single P0 can discredit a whole piece.
- **P1, obvious AI smell.** Tier 1 vocabulary, template phrases, "let's" openers, synonym cycling, formulaic openings, bold overuse, em-dash frequency, hedge stacks, bare-noun bullet lists, generic future-narrative closers. Fix before publishing.
- **P2, stylistic polish.** Generic conclusions, compulsive triads, uniform paragraph length, copula avoidance, "Moreover/Furthermore" transitions. Fix when time allows.

Quick pass = P0 + P1. Full audit = all three.

**When to rewrite from scratch instead of patching:** 5+ vocabulary hits across categories, 3+ distinct pattern categories, and uniform rhythm means the structure itself is AI-generated. State the core point in one sentence and rebuild from there. Lightly-edited slop is still slop.

## Self-reference escape hatch

When writing *about* AI patterns, quoted examples are exempt. Only flag patterns in the author's own prose, never in cited examples of bad writing, quoted material, or code blocks.

## Output formats

**Rewrite mode:** (1) issues found, quoting the offending text; (2) the rewritten version, preserving structure, intent, and all technical specifics; (3) brief summary of meaningful changes, saying why if you reorganized the piece's structure; (4) second-pass audit: re-read your own rewrite, fix any surviving tells, note what the second pass caught. If clean, say so.

**Detect mode:** (1) issues grouped by P0/P1/P2 with quoted text; (2) assessment of which flags are clear problems vs. possibly intentional and effective. If the text is clean, say so plainly.

**Edit mode:** (1) list of edits with location and before → after, only the spans touched; (2) verification that flags are resolved, noting anything deliberately left alone.

If the original is already strong, say so and cut only what's needed. Don't manufacture findings.

## Reference files

- [references/vocabulary.md](references/vocabulary.md): Tiered word tables (Tier 1/2/3), template phrases, transition phrases. Read when auditing or when vocabulary is in question.
- [references/phrases.md](references/phrases.md): Throat-clearing, emphasis crutches, business jargon, meta-commentary, vague declaratives.
- [references/structures.md](references/structures.md): Structural patterns: binary contrasts, negative listings, fragmentation, false agency, rhythm problems.
- [references/tropes.md](references/tropes.md): Word-choice, tone, formatting, and composition tropes with examples.
- [references/patterns.md](references/patterns.md): Artifacts and fingerprints, whole-text tests (rhythm, density, reshuffle immunity), and the newer pattern catalog. Read for full audits and for social or published content.
- [references/preflight.md](references/preflight.md): The authoritative pass/fail checklist. Run on every rewrite and edit before delivery.
- [references/maintenance.md](references/maintenance.md): How to update this skill. Read ONLY when asked to update, refresh, or check its sources, never during writing or editing work.
- [references/examples.md](references/examples.md): Before/after transformations.

## Examples

Worked before/after pairs live in [references/examples.md](references/examples.md), covering
scientific and grant writing, blog prose, and general-purpose copy. Read one before a first pass
to calibrate how far to edit. Every After adds no fact the Before did not contain; where the
Before was vague and a specific was needed, the After flags it rather than inventing it, which is
the rule demonstrated rather than stated.

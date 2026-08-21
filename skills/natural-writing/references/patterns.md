# Artifacts, Whole-Text Tests, and Additional Patterns

Patterns not covered in phrases.md, structures.md, or tropes.md. Three groups: artifacts (fingerprints of pasted AI output, always P0), whole-text tests (rhythm and content diagnostics), and additional patterns worth flagging in full audits.

## Contents

- [Artifacts (P0)](#artifacts-p0)
- [Whole-text tests](#whole-text-tests)
- [Additional patterns](#additional-patterns)

---

## Artifacts (P0)

These are fingerprints, not stylistic signals. Their presence is near-proof of AI output pasted without cleanup. Remove mechanically; even one discredits a piece.

### Chatbot artifacts
"I hope this helps!", "Certainly!", "Absolutely!", "Feel free to reach out," "Let me know if you need anything else," "In this article, we will explore…", "Let's dive in!" are conversational tics from chat interfaces. Remove entirely.

### Sycophantic tone
"Great question!", "Excellent point!", "You're absolutely right!", "That's a really insightful observation." Distinct from chatbot artifacts: these validate the reader rather than performing helpfulness. Remove.

### Acknowledgment loops
"You're asking about," "To answer your question," restating the prompt before answering, or opening a section by recapping the previous one. Pure filler. Just answer.

### Reasoning chain artifacts
"Let me think step by step," "Breaking this down," "To approach this systematically," "Here's my thought process," numbered reasoning steps that read like internal monologue. Chain-of-thought scaffolding leaking into prose. State the conclusion, then the evidence.

### Cutoff disclaimers
"As of my last update," "While specific details are limited based on available information," "I don't have access to real-time data." Model limitations leaking into prose. Find the information or remove the hedge. Never publish a sentence admitting the writer didn't look something up.

### Speculative gap-filling
"Maintains a relatively low public profile," "is believed to have," "likely began his career in," "appears to have studied." Guesses formatted as statements, worse than cutoff disclaimers because the reader can't tell known from invented. Cut, or replace with a sourced fact.

### Unfilled placeholders
`[Your Name]`, `[INSERT SOURCE URL]`, `2025-XX-XX`, `<!-- add citation -->`. Near-definitive evidence of pasted boilerplate. Fill with real content or delete the sentence.

### Chatbot citation markup leaks
`citeturn0search0`, `contentReference[oaicite:0]{index=0}`, `oai_citation`, `[attached_file:1]`. Internal tokens surviving copy-paste from chat UIs. Strip every token; replace meaningful citations with real references. Worth catching even when nothing else reads as AI.

### Invisible characters

Zero-width spaces and joiners (U+200B, U+200D), soft hyphens (U+00AD), and Cyrillic or Greek homoglyphs standing in for Latin letters. These reach text through watermarking, through a paste out of a rendered page, or through a deliberate attempt to defeat a matcher. They are invisible on screen and survive every edit made by eye.

Mechanical to find and near-impossible to false-positive, so scan rather than read: `grep -P '[\x{200B}\x{200D}\x{00AD}]'` catches the first group.

**Fix:** strip them. A homoglyph inside an otherwise Latin word is always an error; normalize it.

### AI-tool URL parameters
`utm_source=chatgpt.com`, `utm_source=openai`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com` on links. Strip the parameter, keep the URL if the link is meaningful.

---

### Register break

A piece that changes voice partway through, with no reason in the content, was written in more than one pass or by more than one hand. Watch for the error profile changing too: typos and comma splices in the first half and none in the second is the same tell from the other direction, and it is the more reliable of the two because nobody edits their mistakes back in.

**Fix:** pick the register the piece earns and hold it end to end. When the shift is deliberate, and sometimes it is, give it a reason the reader can see.

## Whole-text tests

Structure is the #1 detection signal, and detectors weight rhythm regularity above vocabulary. Fixing every flagged word while leaving the rhythm untouched still reads as AI.

### Sentence and paragraph uniformity
If most sentences are 15–25 words, the text sounds robotic. Mix 3–8 word sentences with 20+ word ones; fragments and questions break monotony. Same for paragraphs: some should be one sentence, some longer. If every paragraph is 3–5 sentences of the same size, vary deliberately.

### Read-aloud test
If a text-to-speech engine could read the piece without sounding weird, it's too uniform.

### Vocabulary diversity
In pieces over ~200 words, eyeball the range of vocabulary. AI text trends flat, recycling the same abstract nouns. The fix is rarely a thesaurus; it's broadening the *what*: name specific things, cite specific cases, replace a reused abstraction with the concrete instance behind it. (Narrow technical topics and second-language writing legitimately compress vocabulary, so this is a soft signal.)

### Paragraph-reshuffle immunity
Can you swap two body paragraphs without breaking the piece? If order doesn't matter, it's a list of points, not an argument that builds. Fix is structural: establish a through-line where each paragraph depends on the last, or make it an honest explicit list.

### Treadmill effect (information density)
Read each paragraph and ask: what's actually new here? AI prose restates the premise in fresh words: motion without distance. If you could cut 40–60% and lose nothing, cut it. Each paragraph must contribute one fact, claim, or turn; lead with it.

### Missing first-person perspective
Where the piece is supposed to have a voice, relentless neutrality is itself a tell. Stated preferences, reactions, and "in my experience" keep it human.

### Over-polishing warning
Aggressively editing out every irregularity pushes human writing *toward* AI statistical profiles. Keep deliberate fragments, sentences starting with "And" or "But," idiosyncratic word choices, uneven pacing.

The warning applies to *distinctive* irregularity, not to mess in general. Filler, hedging, throat-clearing, and restatement are regularities the whole internet shares, so cutting them moves writing away from the AI profile rather than toward it. Don't cite this entry to justify leaving slop in place.

### When to rewrite from scratch
5+ vocabulary hits across categories, 3+ distinct pattern categories, and uniform rhythm together mean the structure itself is AI-generated. Patching phrases won't fix it. State the core point in one sentence and rebuild.

---

## Additional patterns

### Diff-anchored writing
Prose or docs that narrate the change that produced the thing instead of describing the thing: "This function was added to replace the old lookup," "We updated this section to clarify..." Describe the artifact as it is: "This function uses a hash map for O(1) lookups." Changelogs and commit messages are exempt, since there the change is the content.

### Copula avoidance
Substituting fancier verbs for "is" and "has": "serves as," "features," "boasts," "represents." Press-release sound. Default to "is"/"has" unless a specific verb adds meaning.

### Periphrastic connection
Roundabout relationship phrasing where a specific relationship should be named: "is associated with," "in connection with," "in association with," "connected with," "has ties to," "is linked to," "plays a role in," "in the context of." A sibling of copula avoidance, but the failure is worse than style: the vagueness usually hides a connection the writer can't actually specify, the same way "experts argue" hides a missing source.

Two fixes, cheapest first. Often the phrase stands in for a plain preposition and the swap costs one word: "uses associated with the patented method" becomes "uses of the patented method"; "referenced the inventor in connection with the award" becomes "referenced the inventor for the award." When a preposition won't carry it, name the relationship, meaning who did what to whom or what causes what.

The preposition swap is always safe, since "of" and "for" claim no more than the original. Naming the relationship with a verb ("caused by," "used in," "working with") is only safe when the writer knows it holds; picking "caused by" for an association the source never established is fabrication in compact form. If the relationship isn't known, that's a flag for the author, not a gap to paper over. Carve-out: uncertainty stated as uncertainty ("the mechanism linking the two isn't established") is honest writing, not periphrasis. Watch for the pairing with generic intensifiers ("widely associated," "particularly associated"), which is the same evasion twice in one phrase.

### Interpretive metadiscourse
Lines that step outside the subject to tell the reader what to notice or how much weight to give it: "the key point is," "as you can see," "this distinction matters," "that last part matters more than it sounds," and glossing "in other words" when the first phrasing was already clear. The prose either demonstrates the point or it does not; an instruction to find it important is not a substitute. Delete the aside, or replace it with the fact that would have made the point land on its own.

### Interchangeable sentence
A sentence that could move unchanged to another person, company, country or product carries no information about this one. Swap in a rival's name: if it still reads true, it was never about your subject. Two independent sources reached this test separately, which is some evidence it catches something real. Replace it with the fact, number or behavior that only this thing has, or cut it.

### Dense sentence
Distinct from uniformity, which is about rhythm. This is parse cost. If the reader has to return to the start of a sentence to work out what attaches to what, split it. One idea per sentence, and let the next sentence take the next one. Long is fine; tangled is not.

### Synonym cycling
*Style fault, not an authorship tell.*

"Developers… engineers… practitioners… builders" in one paragraph. Human writers repeat the clearest word. If the same noun appears three times and it's the right word, keep all three. Fowler named elegant variation a fault in 1926 and it reads badly whoever produced it. Do not cite it as evidence that a model wrote the text; that claim was withdrawn in 2.11, see the harvest log.

### Hedge-stacked predictions
"Could potentially create," "may eventually unlock," "might ultimately transform." Either word alone is fine; the stack asserts nothing while sounding thoughtful. Pick one.

### Real/actual adjective inflation
Two forms, and screening for only the first misses half of them.

**Attributive** (adjective before the noun): "genuine utility," "actual reward sustainability," "true product-market fit" put an empty intensifier on an abstract noun, implying an unnamed fake version.

**Predicative** (after a linking verb): "the gap is real," "the risk is real," "this is a real problem," "the concern is genuine." Same move, and it slips past any check that scans for adjective-plus-noun. Common as an emphasis beat right before the evidence that actually makes the case, which is the tell: if the next sentence does the work, the assertion of realness was filler.

Carve-out for both: if the contrast is named ("actual revenue from paying customers, not grants"), it's honest contrastive writing. Otherwise drop the adjective and let the specific claim carry it.

**Deletability test.** This generalizes past realness words to every intensifier, including ones inside a legitimate carve-out. Delete the word and reread the sentence. If the meaning is unchanged, it was filler. "Genuinely adds meaning" and "genuinely needs it" fail; "a real list, not a padded one" survives because the contrast collapses without it. Applies to *genuinely, really, actually, truly, simply, literally, honestly, very*.

### Generic future-narrative closers
"May become one of the most important narratives of the next cycle," "is poised to become the next major chapter in X." Grammatically a prediction, but contains no testable content. Fix: make it falsifiable ("may exceed AWS spot pricing for parallel workloads by 2027") or cut.

### Bullet lists of bare noun phrases
5+ consecutive items, each a short adjective+noun phrase with no verb: "Stable mining efficiency / Reliable pool connectivity / Optimized performance." The tell is the symmetry: every item the same shape, nothing checkable. Convert to prose or full claims ("Failed shares stayed under 1% across a 12-hour run"). Doesn't apply to real list content (changelogs, todos, parameter docs).

### List-label periods
Bullets that lead with a short label ending in a period: "**Intros.** Years of conferences and operator network." A human writes a colon: "**Intros:** years of conferences…" Fix period to colon and lowercase the gloss, or drop the label. Carve-out: if the leading span is a full sentence, the period is correct.

### Inline-header repetition
Bold headers that repeat themselves: "**Performance:** Performance improved by..." Strip the header and write the point.

### Hyphenated-pair overuse
Two problems. Density: "a high-quality, well-architected, future-proof solution" should be cut to the modifier that matters. And the attributive/predicate error: hyphenate before the noun ("a high-quality report") but not after a linking verb ("the report is high quality"). AI frequently hyphenates the predicate form.

### Title case headings
"Strategic Negotiations And Key Partnerships." Use sentence case for subheadings; title case only for the piece's main title, if at all.

### Excessive structure
More than 3 headings in under 300 words, or 8+ bullets in under 200 words, is AI trying to look organized. Merge into prose. Formulaic headers ("Overview," "Key Points," "Conclusion") are default scaffolding. Use headers that say something specific.

### Notability name-dropping
Piling on prestigious citations: "cited in the NYT, BBC, FT, and The Hindu." One specific reference with context beats four name-drops.

### Novelty inflation
Treating established concepts as discoveries: "She coined the phrase," "a failure mode nobody's naming," "the insight everyone's missing." Factually risky and promotional. Describe what the person *did with* the concept. If unsure whether something is novel, assume it isn't.

### Emotional flatline
"What surprised me most," "I was fascinated to discover," "The most interesting part," "Interesting thing here:" all use claimed emotion as a structural crutch. Tell-don't-show. If the thing is surprising, the content should carry it; if you claim an emotion, the writing must earn it. Also flags lazy human writing, so cut either way.

### Self-labeling significance
Back-pointing after a list: "That last move is the contrarian one," "This is the interesting part." The label does the work the content should do. Cut the label and let the explanation carry it, or restructure so the key item leads with specifics.

### Infomercial engagement hooks
Mid-flow teasers faking momentum: "The catch?", "The kicker?", "Plot twist:", "The best part?". Delete the hook, state the thing: "The catch? It only works on weekends" becomes "It only works on weekends."

### Social endorsement closers
The generic sign-off on share posts: "This one is worth your time:", "Must-read:", "Don't sleep on this," "Thank me later." Performs a recommendation without a reason to click. Fix: say what the thing is and who it's for ("Sarah's breakdown of why context windows leak, the clearest explanation I've found for anyone debugging RAG pipelines"), then drop the CTA.

### Hashtag stuffing
6+ trailing hashtags on a short post is a hard flag, since mixing one project tag with broad category tags (#AI #Innovation #FutureTech) reads as bot output. 5+ is a soft tell on professional social posts. Fix: 2–3 specific tags, or none.

### Rhetorical question openers
"So why should you care?", "What's next?" as section transitions. If you know the answer, say it. Rhetorical questions are earned by strong setup, not dropped as transitions.

### Parenthetical hedging
"(and, increasingly, Z)", "(and perhaps more importantly, W)" are asides that sound nuanced without committing. If the aside matters, give it its own sentence. If not, cut.

### Numbered list inflation
"Five things to know," "top seven" use numbered lists as structural safety. Only number when the content has that many discrete parallel items. Padding to hit a number means the list shouldn't exist.

### False concession structure
"While X is impressive, Y remains a challenge." Balance-flavored vagueness, both halves empty. Make the concession specific or pick a side and argue it.

### Formulaic openings
Broad context before the point: "In the rapidly evolving world of..." Lead with the news or the insight; context comes second.

### Promotional language
Tourism-brochure prose: "nestled within breathtaking foothills," "a vibrant hub of innovation." Replace with plain description. If you wouldn't say it in conversation, cut it.

### Aphorism formulas
Manufactured profundity of the shape "[Abstract noun] is the [language/currency/architecture] of [abstract noun]": "Symmetry is the language of trust," "Attention is the currency of the internet." The formula sounds deep and asserts nothing checkable. Replace with the actual claim the aphorism was gesturing at, or cut.

### Fake-profound kicker lines
The closing sentence that reaches for resonance: a one-line metaphor, aphorism, or callback engineered to land ("In the end, we weren't debugging the code. We were debugging ourselves."). Delete it. Don't rewrite it into a better metaphor. End on the last concrete point, takeaway, or next action.

### Summary-recap endings
Closing paragraphs that restate what the piece already said ("Overall," "In the end," "As we've seen"). AI does this reflexively even in short pieces. Cut the recap; end on a concrete point.

### Nominalization and stacked noun phrases
Verbs and adjectives smothered into abstract nouns: "conducted an analysis of" for "analyzed," "made the determination" for "decided," "the implementation of the optimization of the process." One nominalization is normal English; density is the tell, and clusters of them produce the fog-index prose AI defaults to in formal registers. Fix: find the verb hiding inside the noun and let it act. Same for noun pileups ("customer engagement optimization strategy framework"): break the stack with verbs and prepositions.

### Audience flattery
"Whether you're a solo founder or a Fortune 500 exec," "for beginners and experts alike," "no matter where you are on your journey." False breadth that means everyone, so it identifies no one. Name the actual reader once, or cut the line. A piece that knows its audience shows it in the examples rather than announcing it.

### Theater framing
Dismissing something as performative to sound incisive: "We killed the growth theater," "No more security theater," "That's just innovation theater." A recurring generated-copy tic (independently catalogued by Impeccable's design-copy detector). Once, with a named target and evidence, can work; as a reflex it's a sneer standing in for an argument. Say plainly what the thing does or doesn't do.

### Conversational fake-candid openers
"Honestly? It depends." "Real talk:" "Can I be honest?" are performed candor as a setup. The disclosure frame implies everything before it was less than honest. Remove the setup and state the point.

### Offer-to-continue closers
"Want me to expand on any of these?", "I can go deeper on X if useful," "Happy to draft the next section." Chat-turn residue at the end of prose. Remove entirely; prose doesn't offer follow-ups.

### Colon reveals
"The best part: it learns." "The result: chaos." A colon used as a drumroll before a short reveal. Same family as infomercial hooks: delete the setup, state the thing, or fold into a normal sentence.

### Fragmented headers
A heading immediately restated by a stub sentence: "## Performance" followed by "Speed matters." Either the heading or the sentence is redundant. Let the heading do the work and start the section with substance.

### Secondhand-text guard
Translated text, transcribed speech, committee-edited prose, and second-language writing legitimately trigger many flags here (uniform rhythm, compressed vocabulary, formal transitions). When the provenance is known to be secondhand, raise the bar before flagging and never treat pattern density as evidence of AI authorship.

### Hyphen/en-dash range confusion
AI overuses em dashes but skips en dashes entirely, writing ranges with hyphens ("1990-2000," "3-2") where an en dash belongs (1990–2000). Weak signal on its own; corroborating alongside em-dash overuse.

### Curly quotes (weak signal)
Curly quotes/apostrophes are only meaningful in plain-text contexts (code comments, commit messages) where nothing auto-curls. Word, Docs, macOS, and iOS all curl by default, so most human prose has them. Treat as corroborating, never conclusive. Straighten in code/plain-text; leave in finished publications and locale-correct punctuation (French « », German „ ").

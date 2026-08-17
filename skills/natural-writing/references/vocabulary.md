# Tiered AI Vocabulary

Words organized by how reliably they signal AI-generated text. The tiering prevents false positives: a word that's suspicious in a cluster may be perfectly fine alone.

- **Tier 1, always replace.** These appear 5–20x more often in AI text than human text.
- **Tier 2, flag in clusters.** Individually fine; two or more in the same paragraph is a strong signal.
- **Tier 3, flag by density.** Normal words AI overuses. Only flag when the text is saturated with them (roughly 3%+ of total words).

Replacements are defaults, not mandates. If a flagged word is clearly the right choice in context, keep it.

## Tier 1: always replace

| Replace | With |
|---|---|
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, space, industry, world |
| tapestry | (describe the actual complexity) |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | (rewrite entirely) |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| cutting-edge | latest, newest, advanced |
| leverage (verb) | use |
| pivotal | important, key, critical |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer / game-changing | describe what specifically changed and why it matters |
| hit differently / hits different | (say what specifically changed, or cut) |
| utilize | use |
| watershed moment | turning point, shift (or describe what changed) |
| marking a pivotal moment | (state what happened) |
| the future looks bright | (cut; say something specific or nothing) |
| only time will tell | (cut) |
| nestled | is located, sits, is in |
| vibrant | (describe what makes it active, or cut) |
| thriving | growing, active (or cite a number) |
| despite challenges… continues to thrive | (name the challenge and the response, or cut) |
| showcasing | showing, demonstrating (or cut the clause) |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| bustling | busy, active (or cite what makes it busy) |
| intricate / intricacies | complex, detailed (or name the specific complexity) |
| complexities | (name the actual complexities, or use "problems" / "details") |
| ever-evolving | changing, growing (or describe how) |
| enduring | lasting, long-running (or cite how long) |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full, whole (or describe what's included) |
| actionable | practical, useful, concrete |
| impactful | effective, significant (or describe the impact) |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority (or describe the actual contribution) |
| best practices | what works, proven methods, standard approach |
| at its core | (cut; state the thing) |
| synergy / synergies | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine, learn |
| endeavor | effort, attempt, try |
| keen (as intensifier) | interested, eager (or cut) |
| symphony (metaphor) | (describe the actual coordination) |
| embrace (metaphor) | adopt, accept, use, switch to |

## Tier 2: flag when 2+ appear in the same paragraph

Legitimate on their own. When two or more show up together, the paragraph likely needs a rewrite.

| Replace | With |
|---|---|
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| empower | enable, let, allow |
| bolster | support, strengthen, back up |
| spearhead | lead, drive, run |
| resonate / resonates with | connect with, appeal to, matter to |
| revolutionize | change, transform, reshape (or describe what changed) |
| facilitate / facilitates | enable, help, allow, run |
| underpin | support, form the basis of |
| nuanced | specific, subtle, detailed (or name the actual nuance) |
| crucial | important, key, necessary |
| multifaceted | (describe the actual facets, or cut) |
| ecosystem (metaphor) | system, community, network, market |
| myriad | many, numerous (or give a number) |
| plethora | many, a lot of (or give a number) |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign, rebuild |
| galvanize | motivate, rally, push |
| augment | add to, expand, supplement |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify, spell out |
| juxtapose | compare, contrast, set side by side |
| paradigm-shifting | (describe what actually shifted) |
| transformative / transformation | (describe what changed and how) |
| cornerstone | foundation, basis, key part |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging (or cite a number) |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic, defining |
| overarching | main, central, broad |
| underpinning / underpinnings | basis, foundation, what supports |

## Tier 3: flag only at high density

Normal words. Only flag when the text is saturated with them, a sign that AI filled space with vague praise instead of specifics.

| Word | What to do |
|---|---|
| significant / significantly | Replace some with specifics: numbers, comparisons, examples |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how or cite a metric |
| dynamic / dynamics | Name the actual forces or changes |
| scalable / scalability | Describe what scales and to what |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks (or cut) |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / state-of-the-art / best-in-class | Cite a benchmark or comparison |

## Tier 3 phrases: flag at repetition or in clusters

Multi-word boilerplate that's individually unobjectionable but stacks heavily in AI content. Flag at 2+ uses of the same phrase, or when three or more *distinct* phrases from this table appear in one piece. That's the shape LLMs take when varying their own boilerplate.

| Phrase | What to do |
|---|---|
| emerging sector / space / category | Name the actual sector or what's emerging |
| the integration of (X with Y) | Describe what's integrated and what changes for the user |
| the intersection of (X and Y) | Pick the specific overlap or cut the framing |
| community-driven | Name what the community does |
| long-term sustainability | Cite the time horizon and the constraint |
| user engagement | Name the action (clicks, comments, retention) |
| designed for long-term [X] | Cut "designed for"; either it is or it isn't |

## Template phrases (avoid)

Slot-fill constructions. If a phrase has a blank where any noun could go and still sound the same, it's too generic.

- "a [adjective] step towards/forward for [noun]" → say what actually changed
- "Whether you're [X] or [Y]" → false breadth meaning "everyone." Pick the audience or cut.
- "I recently had the pleasure of [verb]-ing" → just say what happened: "I talked to," "I read"

## Transition phrases to remove or rewrite

- "Moreover" / "Furthermore" / "Additionally" → restructure so the connection is obvious, or "and," "also"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "Here's what's interesting / what stood out" → let the content signal its own importance
- "In conclusion" / "In summary" → the conclusion should be obvious
- "When it comes to" → talk about the thing directly
- "At the end of the day" → cut
- "That said" / "That being said" → cut, or "but," "yet," and don't overuse any one of them

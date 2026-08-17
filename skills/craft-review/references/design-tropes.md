# AI Design Tropes to Avoid

The visual counterpart to `deslop`'s `tropes.md`. A catalog of the patterns that make an interface
look *generated* rather than *designed* — the defaults a model reaches for when it isn't grounded in
a specific product, audience, and mood. Use it two ways: as a checklist when auditing a design, and
as context when generating one, so the first draft isn't already slop.

Each entry is: **the tell → why a model reaches for it → what it looks like → what to do instead.**
A single instance is rarely fatal; the tell is the *reflex* — reaching for it by default, everywhere,
without a reason the product forced.

The meta-test sits above the whole catalog:

> **The category-reflex test.** *First-order:* could someone guess this design's theme and palette
> from the product's category alone? ("fintech → navy + gold," "AI tool → dark + purple," "health →
> teal + white"). If yes, it's reflex, not decision. *Second-order:* could they guess the aesthetic
> *family* from the category plus the obvious anti-reference ("developer tool, so *not* corporate →
> therefore terminal-green editorial")? If yes, dig further. Ground the decision in a physical scene —
> who uses this, where, in what light and mood — until the scene forces the answer.

---

## Layout & structure

### The hero-metric template
Three or four big numbers in a row ("10k+ users · 99.9% uptime · 4.9★") under a centered headline.
Models reach for it because it fills space and signals "SaaS" without a real information hierarchy.
**Instead:** lead with the one thing that matters to *this* user; if metrics earn their place, weave
them where the claim they support lives, not in a decorative strip.

### The identical card grid
Every piece of content forced into the same rounded rectangle, same padding, same shadow, tiled 3×N.
It's the model's default container because it's safe and uniform — and uniformity is exactly what
reads as machine-made. **Instead:** vary card size/weight by importance; let some content breathe
without a box. Nested cards (a card inside a card) are a near-certain tell.

### Centered-hero + subhead + two buttons
The landing-page reflex: centered H1, one-line subhead, a filled button next to a ghost button.
**Instead:** justify the composition from the content — asymmetry, a real image, a single primary
action. Two buttons of near-equal weight means you haven't decided what the primary action is.

### Everything in a container
Wrapping every region in a bordered/elevated panel so the page becomes a stack of boxes. **Instead:**
use whitespace and alignment to group; a border is a last resort, not the default separator.

### Tiny numbered section labels
*01 Discover / 02 Design / 03 Deliver* — decorative numbering beside headings, imitating editorial
structure without adding it. **Instead:** cut the numbers; let hierarchy and rhythm sequence the page.

### Geometrically centered asymmetric glyphs
Play triangles, chevrons, and other asymmetric icons centered by the math look off-center to the
eye; automated alignment checks pass while the composition reads as sloppy. **Instead:** optical
centering — nudge the glyph toward its visual mass (a play icon shifts slightly right) and trust the
eye over the bounding box.

## Color

### Category-reflex palettes
Navy+gold for finance, teal+white for health, dark+purple for AI, green for anything "eco." The
first thing to interrogate (see the meta-test). **Instead:** derive from the product's actual mood
and context; then sanity-check that the palette isn't the category cliché.

### Pure black and pure white
`#000` / `#fff` as text and background. Real materials are never pure; the extremes read as
untouched defaults and vibrate against each other. **Instead:** near-black and off-white (e.g.
`#0e0d12` / `#f6f4f1`); reduce chroma as you approach the extremes.

### The purple→blue SaaS gradient
The single most-generated gradient on earth, usually on a hero or a CTA. **Instead:** if a gradient
earns its place, tie it to the brand and use it once, with intent — not as default decoration.

### One-accent-does-everything with no strategy
A single saturated accent sprinkled at random density. **Instead:** pick a color strategy first —
Restrained (one accent, ≤10% of surface), Committed (30–60% saturation across roles), Full-palette
(3–4 semantic roles), or Drenched (the surface *is* the color) — then execute it consistently.

### The cream/beige "tasteful default"
Warm cream or beige page background reached for by reflex — the current wave's replacement for the
purple gradient as the safe "tasteful" choice. **Instead:** a background that comes from a deliberate
palette and the product's scene, not the reflex warm off-white.

### Dark mode with glowing accents
Colored box-shadow glows on dark backgrounds; cyberpunk-by-default, plus the saturated radial halo
behind hero content. **Instead:** subtle purposeful lighting tied to real elevation, or skip the dark
theme entirely.

## Typography

### Inter/Geist everywhere, one weight
The default UI font at a single weight, hierarchy faked with size alone. Not wrong, but reaching for
it *without a reason* is the tell. **Instead:** choose type with intent; build hierarchy from
weight+size+leading as a set (aim for ≥1.25× scale steps), and cap body line length at 65–75ch.

### Gradient text as decoration
Gradient fills on headings "to add interest." It adds AI signature and usually hurts contrast.
**Instead:** reserve gradient text for a deliberate brand mark, if at all; earn emphasis with weight
and size.

### Proportional numerals on dynamic values
Timers, counters, prices, and table columns set in default proportional figures jitter and reflow as
digits change width. **Instead:** `font-variant-numeric: tabular-nums` on any number that updates or
must align vertically.

### The icon tile above the heading
A small rounded-square icon container stacked above a feature-card heading — the universal AI
feature-card template; every generator outputs this exact shape. **Instead:** icon beside the
heading, icon in flow without its own container, or no icon.

### The hero eyebrow / repeated kickers
A tiny uppercase letter-spaced label or pill chip floating above an oversized hero headline, and the
same tracked micro-label repeated above every section ("FEATURES" / "PRICING"). Editorial scaffolding
by reflex. **Instead:** fold the kicker into the headline or drop it; let structure and imagery do
the sequencing.

### The italic serif display hero
Oversized italic serif (Instrument Serif and friends) as the hero headline — reads as taste in
isolation but has become the universal AI-startup hero of the current wave. Genuinely editorial
products get a pass; judge by context. **Instead:** set it roman, or choose a non-serif display face.

### The oversized full-sentence headline
A long sentence at display size dominating the viewport. A one-or-two-word headline at that size is
fine; the tell is length × size together. **Instead:** tighten the copy or shrink the type.

## Surface & depth

### Glassmorphism by default
Frosted translucent panels everywhere because they look "modern." Decorative blur with no functional
layering is a strong tell. **Instead:** use translucency only where a real layer floats over scrolling
content; otherwise a solid surface.

### The uniform soft drop-shadow
The same `0 4px 12px rgba(0,0,0,.1)` on every element, so nothing has a real elevation story.
**Instead:** one shadow/elevation scale mapped to actual z-order; most elements sit flat.

### Side-stripe accent borders
A 2–4px colored left border on cards/callouts to "add color." A recognizable reflex. **Instead:**
signal category with a small icon, a label, or a tint — reserve the stripe for a genuine
quote/citation semantic.

### Hairline border + wide soft shadow
A 1px border paired with a wide diffuse shadow on the same card — a generated-UI signature.
**Instead:** commit to one: a defined edge or a soft elevation, not both.

### Mismatched nested radii
An inner element's corner radius equal to or larger than its container's, or picked independently,
makes nested surfaces look subtly wrong even when nothing is nameably broken. The concentric rule:
outer radius = inner radius + padding between them. **Instead:** compute nested radii from the
parent, don't restate the same token at every level.

### The over-rounded blob
24px+ radii on small cards, sections, and inputs rounds everything into the same soft blob.
**Instead:** cards top out around 12–16px; reserve full-pill for tags and buttons.

### Decorative grid-line backgrounds
A grid texture covering a surface that isn't a canvas, map, or measurement task. **Instead:** product
structure or a plain field.

## Motion

### Fade-up-on-scroll on everything
Every section rising 20px and fading in as it enters the viewport. Ubiquitous, and it delays content.
**Instead:** animate to communicate (state change, spatial origin), not to decorate arrival; respect
`prefers-reduced-motion`.

### 200ms-for-everything, with a bounce
One duration and an elastic overshoot applied uniformly. **Instead:** duration tracks distance and
importance; use exponential ease-out (quart/quint/expo); reserve overshoot for gestures that carried
momentum. Never animate layout properties (width/height/top/left) — animate transform/opacity.

### Decorative liveliness
The pulsing status dot on static data, the fake blinking cursor on non-editable hero copy, the
auto-scrolling logo marquee, imagery that scales on hover by default. Motion pretending something is
live or interactive when nothing is. **Instead:** animate only when the data changes or the gesture
demands a response; let people read at their own pace.

## Imagery

### Shape-assembled / hand-coded illustration
Hero art built from generic SVG shapes, or crude hand-coded mascots — reads as placeholder clip art,
not whimsy. **Instead:** real illustration, photography, or a purposeful graphic; if none is
available, ship no illustration.

## UI copy (shared border with `deslop`)

### Generic control labels
"Submit," "Learn more," "Get started," "Click here." **Instead:** name the specific action —
"Start a pod," "Hear their answers." (This is the design edge of the same anti-slop doctrine `deslop`
applies to prose.)

### Empty/error states as afterthoughts
No empty, loading, or error state, or a generic "Something went wrong." **Instead:** design the
non-happy states with the same care as the happy path; errors say what happened and how to fix it.

### Redundant field writing
Label, sublabel, helper text, and placeholder all saying the same thing in slightly different words.
**Instead:** say it once, where it matters.

### Theater framing
"We killed the growth theater" — dismissing things as performative as a copy reflex. **Instead:**
say plainly what the thing does or doesn't do. (Also in `deslop`'s catalog; flag on either surface.)

---

## Distinctiveness quick-check

Run before calling a design done:

- Could you guess the palette/theme from the product's category alone? (category reflex)
- Every card the same size, padding, and shadow?
- Pure `#000` or `#fff` anywhere as text/background?
- A purple→blue gradient, or gradient text as decoration?
- The same soft drop-shadow on everything?
- A colored left-stripe border used decoratively?
- Does *everything* fade-up on scroll?
- One duration for all motion? Any layout-property animation?
- Any generic control label ("Submit," "Learn more")?
- An icon tile above every feature heading? An eyebrow chip or repeated section kickers?
- Cream/beige background, italic-serif hero, or dark-mode glow reached for by reflex?
- Hairline border + wide shadow on the same card? Anything over-rounded into a blob?
- Any decorative liveliness (pulsing dot, fake cursor, marquee, hover-scale)?
- Nested radii concentric (outer = inner + padding)? Dynamic numbers tabular? Asymmetric icons optically centered?
- Would two different briefs, run through this system, produce visibly different designs — or just
  color-swaps of the same template?

## Scoring

When auditing, rate 1–10 on each dimension; treat below 35/50 as "reads as generated — rework."

| Dimension | Question |
|-----------|----------|
| Intentionality | Does every choice trace to the product/audience/mood, not a default? |
| Distinctiveness | Would you recognize this as *this* product, not a template? |
| Hierarchy | Does one thing clearly win, or is everything the same weight? |
| Restraint | Is anything decorative that isn't earning its place? |
| Coherence | Do color, type, space, and motion say the same thing? |

*Source note: synthesized from `pbakaus/impeccable` (Apache-2.0), `nutlope/hallmark` (MIT), and the
structure of our own `deslop` skill. Same doctrine as `deslop`, applied to pixels. Refreshed
2026-07 against Impeccable's 64-pattern slop catalog (impeccable.style/slop), adding the current-wave
tells: cream/beige default, italic serif hero, eyebrow chips, kickers, icon tiles, hairline+shadow,
over-rounding, decorative liveliness, imagery, redundant field writing, theater framing.*

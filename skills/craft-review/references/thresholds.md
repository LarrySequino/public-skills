# Exact Thresholds Cheat-Sheet

The precise numbers so the review never drifts. When a value is available, compute — don't estimate.

## How to read these

Every number carries a tier. The tier decides whether a miss is a defect or a
dialect.

- **[U] Universal.** Derived from bodies and perception, not from a vendor —
  contrast, reach, cognitive load. Applies to every surface. A miss is Critical.
- **[M] Modality.** Set by the *input device*, not the platform. A touch laptop
  running a web app takes touch numbers; a native iPad app driven by a trackpad
  takes pointer numbers. A miss is Critical.
- **[P] Platform.** Convention: iOS, Android, or web idiom. Applies only to the
  platform the review declared. A miss costs familiarity, not usability, so it
  is Major at most — unless it also breaks [U] or [M], which it often does.

**Cross-platform rule.** When one artifact ships to more than one platform, take
the **stricter** number, never the current platform's. 48dp satisfies both 48
and 44; 44 satisfies only one. A single artifact binds to the union of maxima.

## Color contrast (WCAG 2.2)

| Content | AA | AAA |
|---|---|---|
| Body text (< 24px, or < 18.66px bold) | 4.5:1 | 7:1 |
| Large text (≥ 24px, or ≥ 18.66px bold) | 3:1 | 4.5:1 |
| UI components & graphical objects (icons, borders, states) | 3:1 | — |
| Disabled elements | exempt | exempt |

Compute with `scripts/contrast.py`. Also sanity-check color-blind safety: never rely on hue alone to
distinguish states (add icon/shape/text).

## Target size

Keyed on input modality, not on platform. This is the distinction Material draws
and most reviews miss.

| Tier | Rule | Minimum |
|---|---|---|
| **[M]** | Touch input | **48 × 48 dp** |
| **[M]** | Pointer input | **44 × 44 px** |
| **[U]** | Absolute floor, any input (WCAG 2.5.8 AA) | **24 × 24 px** |
| **[U]** | WCAG 2.5.5 (AAA) | 44 × 44 px |
| **[P]** | iOS convention | 44 × 44 pt |
| **[P]** | Android / Material convention | 48 × 48 dp |

Material states 48dp for touch and 44dp for pointer, and notes iOS recommends
44. Apple's current guidance gives no single figure — it defers to a per-platform
minimum across iOS, iPadOS, macOS, watchOS, tvOS and visionOS.

So **do not resolve "mobile" to 44**. Resolve the modality first: a touch surface
takes 48 whatever platform it runs on, and a cross-platform artifact takes 48
because that satisfies both.

Adjacent targets need spacing so they are not mis-tapped, regardless of size.

## Spacing & grid

- Base grid **8pt**; **4pt** for fine adjustments only.
- Every gap/margin/padding should resolve to a scale token. The scale is the product's own if it
  has one; with no adopted system, take the artifact's modal base (`preflight.py` assumes 4/8px,
  which is the near-universal default) and report deviations from that, labeled `(inferred)`.
- Vertical rhythm: consistent step between stacked bands. Inconsistent steps (48/56/72/84) are a finding.
- **[P] Spacing should encode nesting depth, not merely land on the scale.** Each level
  outward takes roughly **1.4x** its child, snapped to the scale (8pt, or 4pt when that
  lands closer). Grounded in Gestalt proximity: grouping is communicated by relative
  distance, so a card whose inner padding equals the page padding has no grouping at all,
  even with every value on-grid. Compute the ratio between adjacent depths — approaching
  1.0 means the levels are indistinguishable, and inverted means the hierarchy reads
  backward. Cap the outermost value (48-64pt) on structures deeper than four levels and
  compress inward, keeping the progression monotonic.
- Paired/repeated components: identical internal padding, unless the pair carries a
  state marker that consumes layout (a status stripe under `border-box`), in which case
  the CONTENT inset must match and the declaration may differ.

## Typography

**[U] Micro-detail.** Invisible when right, cheap to get wrong, and the fastest tell
that nobody swept the type:

- `…` (single glyph), never three periods. Loading and truncation copy ends in it.
- Curly quotes and apostrophes, never straight. Primes (`′`/`″`) only for measures.
  Scope: rendered interface copy. In authored prose the opposite holds, because a curly
  quote is evidence of who typed the sentence rather than a typesetting choice. See
  `natural-writing`. A page that contains both, such as an artifact whose body copy is
  authored and whose mockups show product UI, follows each rule in its own half.
- Non-breaking space inside value-unit and shortcut pairs (`10 MB`, `⌘ K`) and inside
  brand names, so they never break across lines.
- Tabular figures for any column or comparison of numbers; proportional figures make
  aligned digits jitter.
- Headings get balanced wrapping so a single word never strands on the last line.

- Body line-height **1.4–1.6** (1.5 default); headings tighter (~1.1–1.25).
- Reading line length **45–75 characters** (66 ideal).
- Modular scale ratio ~**1.2–1.25**; no arbitrary one-off sizes.
- ≤ **2** type families. Weight for hierarchy, not decoration.
- Tracking: tighten on large display type; slightly open on small caps / uppercase labels.

## Motion

- Typical UI transition **150–300ms**; micro-interactions **≤150ms**; large/overlay **≤400ms**.
- Easing: **ease-out** for entrances, **ease-in** for exits, spring for physical/gestural moments.
- Always honor **`prefers-reduced-motion`** (provide a reduced/none variant).

## Composition heuristics

- Color balance ~**60 / 30 / 10** (dominant / secondary / accent).
- Squint test: the intended primary element still dominates when blurred.
- Exactly **one** primary action per view.
- Gestalt: related items closer than unrelated; shared region/background groups.

## Human-factors laws

- **Fitts:** primary/frequent targets larger and closer to the pointer/thumb.
- **Hick:** fewer choices = faster decisions; chunk or progressively disclose.
- **Miller:** ~7±2 items in a group; chunk long lists/forms.

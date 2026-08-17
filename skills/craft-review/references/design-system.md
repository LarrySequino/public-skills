# Design System (review source of truth)

> **How this is used:** the skill FIRST tries to read live tokens from the Figma file via
> `get_variable_defs`. This file is the **fallback** used when the file has no variables yet
> (currently the case). When you build a real product design file with Figma variables, this
> file becomes a secondary reference — keep it in sync, or delete it and rely on live tokens.
>
> **Status:** PLACEHOLDER. These are neutral starter values, not anyone's brand — replace them
> with the real system before relying on the consistency pass, or the review will measure the
> screen against the wrong scale. Once replaced, anything a screen uses that is NOT listed here
> is a consistency finding by definition.

## Spacing scale (8-point grid; 4 for fine tuning)

| Token | Value |
|---|---|
| `spacing/2xs` | 4px |
| `spacing/xs` | 8px |
| `spacing/sm` | 12px |
| `spacing/md` | 16px |
| `spacing/lg` | 24px |
| `spacing/xl` | 32px |
| `spacing/2xl` | 48px |
| `spacing/3xl` | 64px |

Any gap/padding not on this scale is off-grid → flag. Vertical rhythm between stacked bands should
step consistently (e.g., 8→16→24), not 48/56/72/84.

## Type scale (1.25 modular ratio)

| Token | Size / line-height / weight | Use |
|---|---|---|
| `type/display` | 40 / 44 / Bold | The hero moment (time, big number, reveal) |
| `type/h1` | 32 / 38 / Bold | Screen title |
| `type/h2` | 24 / 30 / Semi Bold | Section title |
| `type/h3` | 20 / 26 / Semi Bold | Card title |
| `type/body` | 16 / 24 / Regular | Body (line-height 1.5) |
| `type/label` | 14 / 20 / Medium | Labels, secondary |
| `type/caption` | 12 / 16 / Medium | Captions, meta (uppercase w/ +1 tracking) |

Rules: ≤2 families (default: Inter). Body line-height 1.4–1.6. Reading text line length 45–75ch.
Weight carries hierarchy, not decoration. Tighten tracking on display type.

## Color palette (exact hex)

Neutral placeholders. Swap wholesale for the product's real tokens.

**Surfaces / ink**
| Token | Hex | Role |
|---|---|---|
| `color/bg` | #101114 | App background |
| `color/surface` | #191B1F | Card / sheet |
| `color/surface-raised` | #212429 | Elevated card |
| `color/ink` | #F2F3F5 | Primary text |
| `color/muted` | #A8ADB7 | Secondary text |
| `color/faint` | #71767F | Tertiary text / hints |

**Accent / semantic**
| Token | Hex | Role |
|---|---|---|
| `color/accent` | #4C8DFF | Primary accent |
| `color/accent-soft` | #7DAEFF | Accent hover / light |
| `color/success` | #3DBF87 | Success / positive |
| `color/warning` | #E0A33A | Highlight / warning |
| `color/danger` | #E5544B | Destructive |

**Worked contrast check** (computed with `scripts/contrast.py`; recompute after swapping tokens):
- `ink` on `bg` = 17.0 OK  ·  `muted` on `bg` = 8.4 OK  ·  `faint` on `bg` = 4.1 (large text only)
- `accent` on `bg` = 5.9 OK for body
- white on `accent` = 3.2 FAILS body text. This is the common one: a mid-tone accent that reads
  fine against a dark background still fails as a fill behind white label text. Darken the fill or
  put `ink` on it instead. Check the fill, not just the text.

## Radius scale

`radius/sm` 8 · `radius/md` 10 · `radius/lg` 14 · `radius/xl` 16 · `radius/pill` 999

## Elevation / shadow scale

`elevation/0` none (flat on bg) · `elevation/1` card (0 1 2 / subtle) · `elevation/2` raised card ·
`elevation/3` sheet/modal (large soft shadow). In dark mode, elevate by lightening the surface, not
only by shadow.

## Motion

Standard UI transition 150–300ms, ease-out for entrances. Signature moments (reveal, match) may run
longer and be choreographed. Always honor `prefers-reduced-motion`.

## Brand feeling (for the Group D pass)

Group D measures the screen against the product's intended feeling, so that intent has to be
written down. Left blank, Group D cannot run and should be reported as skipped rather than passed.

Fill in three or four lines covering:

- **The adjectives**, and their opposites. "Warm, atmospheric, unhurried — not utilitarian" gives
  the review something to fail against. "Clean and modern" does not; every product claims it.
- **The signature moments** and how they should feel, since those carry the brand more than any
  component does.
- **The deliberate constraints** — what this product does not do, even where convention would.
  A rule the interface breaks on purpose is not a finding, and Group D needs to know which is which.

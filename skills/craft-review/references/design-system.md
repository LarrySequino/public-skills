# LoveBlind — Design System (review source of truth)

> **How this is used:** the skill FIRST tries to read live tokens from the Figma file via
> `get_variable_defs`. This file is the **fallback** used when the file has no variables yet
> (currently the case). When you build a real product design file with Figma variables, this
> file becomes a secondary reference — keep it in sync, or delete it and rely on live tokens.
>
> **Status:** PLACEHOLDER starter values derived from the LoveBlind toolkit palette. Replace
> with the real system as it firms up. Anything a screen uses that is NOT listed here is a
> consistency finding by definition.

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

**Surfaces / ink**
| Token | Hex | Role |
|---|---|---|
| `color/bg` | #0E0A14 | App background |
| `color/surface` | #161020 | Card / sheet |
| `color/surface-raised` | #1C1526 | Elevated card |
| `color/ink` | #F4EEFB | Primary text |
| `color/muted` | #B3A6C9 | Secondary text |
| `color/faint` | #7E7295 | Tertiary text / hints |

**Brand / semantic**
| Token | Hex | Role |
|---|---|---|
| `color/brand/rose` | #FF5D8F | Primary accent / danger |
| `color/brand/rose-soft` | #FF86AC | Accent hover / light |
| `color/brand/plum` | #A06BFF | Secondary accent (gradient partner) |
| `color/brand/gold` | #FFCF6B | Highlight / warning |
| `color/success/mint` | #5FE3C0 | Success / positive |
| `color/primary-gradient` | #FF5D8F → #A06BFF | Primary CTAs, signature moments |

**Known-good text/background contrast** (verify with `scripts/contrast.py`):
- `ink` on `bg` ≈ 15:1 ✅  · `muted` on `bg` ≈ 7:1 ✅  · `faint` on `bg` ≈ 3.6:1 (large text only)
- `rose` on `bg` ≈ 4.9:1 ✅ (body ok) · white on `rose` ≈ 2.5:1 ❌ (fails — don't put white text on rose fills at body size; use `ink` on darker or enlarge)

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

Intimate, warm, a little magical. Atmospheric over utilitarian. Faces hidden until connection — no
avatars in the blind phase. Pods and the reveal should feel high-stakes and tender, never like a
settings screen.

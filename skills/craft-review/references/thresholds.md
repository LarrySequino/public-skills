# Exact Thresholds Cheat-Sheet

The precise numbers so the review never drifts. When a value is available, compute — don't estimate.

## Color contrast (WCAG 2.2)

| Content | AA | AAA |
|---|---|---|
| Body text (< 24px, or < 18.66px bold) | 4.5:1 | 7:1 |
| Large text (≥ 24px, or ≥ 18.66px bold) | 3:1 | 4.5:1 |
| UI components & graphical objects (icons, borders, states) | 3:1 | — |
| Disabled elements | exempt | exempt |

Compute with `scripts/contrast.py`. Also sanity-check color-blind safety: never rely on hue alone to
distinguish states (add icon/shape/text).

## Target size (WCAG 2.5.5 / 2.5.8 + platform)

| Standard | Minimum |
|---|---|
| Apple HIG (iOS) | 44 × 44 pt |
| Material (Android) | 48 × 48 dp |
| WCAG 2.5.5 (AAA) | 44 × 44 px |
| WCAG 2.5.8 (AA) | 24 × 24 px |

Mobile default: **44×44pt**. Adjacent targets need spacing so they're not mis-tapped.

## Spacing & grid

- Base grid **8pt**; **4pt** for fine adjustments only.
- Every gap/margin/padding should resolve to a scale token (see `design-system.md`).
- Vertical rhythm: consistent step between stacked bands. Inconsistent steps (48/56/72/84) are a finding.
- Paired/repeated components: identical internal padding — no exceptions.

## Typography

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

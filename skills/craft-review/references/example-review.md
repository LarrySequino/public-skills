# Worked Example — Gold-Standard Review

This is the depth, specificity, and format every review should match. (Subject: a "Sleep" alarm
screen — a dark bottom-sheet with a header, AM/PM toggle, a large 7:00 AM display, a time scrubber,
and two bottom action cards.) Note how measured findings carry exact numbers and the symmetry
category does the heaviest lifting.

---

## Summary
**Screen:** Sleep — alarm set / bedtime sheet. **Job:** set an alarm time and start a sleep session.
**Assumed user:** someone in bed, low light, one hand, wants this fast. **Input:** Figma frame via MCP
(`get_metadata` geometry + `get_variable_defs` → no tokens defined, measured against fallback scale).
**Confidence:** high on Group A (measured), medium on Group B (judgment).

## Scores
**Overall: 68 / 100**  ·  **Accessibility: 82 / 100**

## Overall impression
The composition has a clear hero (the 7:00 AM time) and a calm dark palette that fits a bedtime
context. But the screen is undermined by pervasive **asymmetry** — the two bottom cards in particular
have mismatched internal padding that reads as broken — and by a **vertical rhythm that isn't on any
consistent scale**. Fix the symmetry and the grid and this jumps a full tier.

## Findings by category

### Symmetry, balance & alignment  (highest-signal — 4 findings)
```
🟠 Major  Symmetry — bottom action cards have mismatched internal padding
  What:  "GO / Sleep Aid" card: left pad 12px, top pad 24px. "Loud Ring / Alarm Settings" card:
         left pad 20px, top pad 16px. The pair should be identical.
  Why:   Paired/repeated components must share padding; unequal padding on side-by-side cards is the
         single most common "unpolished" tell and the eye catches it instantly.
  Fix:   Set both to 16px all sides (spacing/md). Make one a component instance so they can't drift.
```
```
🟡 Minor  Symmetry — AM/PM control not balanced within its track
  What:  Selected "AM" pill sits with ~4px inset on the left but ~10px of empty track on the right.
  Why:   A segmented control should be symmetric around its divider; the extra right gap reads as a
         layout bug.
  Fix:   Equalize track padding to 4px both sides; center the two segments on the divider.
```
```
🟡 Minor  Symmetry — time scrubber not centered on the current value
  What:  The ruler shows more range to the right of 7:00 (to 8:00) than to the left (stops ~5:30);
         the 7:00 marker isn't the visual center.
  Fix:   Balance the visible range around the selected value (e.g., ±90min), so "now" is centered.
```
```
🔵 Polish  Alignment — "AM" unit not baseline-aligned to "7:00"
  What:  The "AM" label rides ~4px above the numerals' baseline.
  Fix:   Baseline-align "AM" to "7:00" (or set a deliberate cap-height alignment); it should sit on
         the same line the eye reads.
```

### Spacing, grid & rhythm
```
🟠 Major  Grid — vertical band heights aren't on a consistent scale
  What:  Header 48 · AM/PM 56 · scrubber 72 · actions 84. Steps of 8, 16, 12 — no rhythm; 84 isn't
         on an 8pt grid.
  Why:   Inconsistent rhythm makes the screen feel loose even when each part looks fine alone.
  Fix:   Snap to the scale: e.g. 48 / 56 / 72 / 80, or a cleaner 48 / 64 / 72 / 80. Bind heights to
         spacing tokens.
```
```
🔵 Polish  Grid — inter-card gap off-scale
  What:  Gap between the two bottom cards is 12px; horizontal side margins are 16px.
  Fix:   Use 16px (spacing/md) for the gap to match the margins, or 8px for a tighter pair — either
         is on-scale; 12 is the odd one.
```

### Visual hierarchy  (judgment)
```
🟡 Minor  Hierarchy — icon buttons compete with the hero
  What:  The two circular header icons are heavy solid fills; they pull attention from the 7:00 time.
  Why:   Only the time should win the squint test on this screen.
  Fix:   Reduce their weight — ghost/tonal fill or lighter icon — so hierarchy reads time > controls.
```

### Color & contrast
```
🔵 Polish  Contrast — secondary labels near the AA floor
  What:  "Sleep Aid" / "Alarm Settings" subtitles measure ~3.8:1 on the card fill (via contrast.py).
  Why:   Passes for large text but is under 4.5:1 for body.
  Fix:   Lighten to muted (#B3A6C9 ≈ 5:1+) or size them as large text.
```

## Priority table
| # | Sev | Category | Issue |
|---|---|---|---|
| 1 | 🟠 | Symmetry | Bottom cards' mismatched padding |
| 2 | 🟠 | Grid | Inconsistent band-height rhythm |
| 3 | 🟡 | Symmetry | AM/PM not balanced in track |
| 4 | 🟡 | Symmetry | Scrubber not centered on value |
| 5 | 🟡 | Hierarchy | Icon buttons too heavy |
| 6 | 🔵 | Alignment | "AM" baseline |
| 7 | 🔵 | Grid | Inter-card gap 12px |
| 8 | 🔵 | Contrast | Subtitle labels near floor |

## Top 3 quick wins
1. Make the two bottom cards one component with 16px padding — fixes the most visible problem in one move.
2. Snap the four band heights to the spacing scale.
3. Lighten the header icons to tonal fills so the time clearly wins.

## Strengths to preserve
- Strong, unambiguous hero (the 7:00 AM time) — don't let fixes dilute it.
- Calm, low-light-appropriate dark palette.
- Good use of a single accent; the screen isn't noisy.

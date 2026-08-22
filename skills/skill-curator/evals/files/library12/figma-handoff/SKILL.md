---
name: figma-handoff
description: >
  Export measurements, color specs, and type specs from a Figma file, together with the design
  tokens behind each one, so a developer can implement the screen without opening the editor. Use
  when a designer marks a frame ready for handoff, or when a ticket links a Figma frame and
  carries no redlines. NOT for judging whether a screen is well designed (use visual-critique for
  that).
---

# Figma Handoff

Turns a frame into something an engineer can implement without guessing.

## Procedure

1. Confirm the frame is the one marked ready. Handing off a stale frame is the most
   common failure, and it is invisible until QA.
2. Pull the frame's measurements: box sizes, gaps, padding, and the grid it sits on.
   Record them as numbers, never as "roughly a card width".
3. Read the type ramp actually used in the frame: family, size, weight, line height,
   letter spacing. List each style once, with the elements that use it.
4. Read every color value in the frame and map it back to the named token that
   produced it. A raw hex with no token behind it is a finding, not a spec.
5. List the interactive states present in the frame and the ones missing: hover,
   focus, disabled, loading, empty, error.
6. Write the handoff sheet: one section per component, measurements first, then type,
   then color, then states.

## What to hand back

- A per-component spec table with numbers, not adjectives.
- The list of values that had no named token behind them.
- The states the designer did not draw, so they get decided rather than invented.

## Failure modes

Specs written from a screenshot instead of the file drift by a pixel or two per
measurement and nobody can tell which number is authoritative. Read the file.

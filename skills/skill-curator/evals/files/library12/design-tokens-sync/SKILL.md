---
name: design-tokens-sync
description: >
  Read the design tokens out of a Figma library and write the values into the repository as CSS
  custom properties or a theme file, so the color and spacing in the app stop drifting from the
  source of truth. Use when a token changed upstream, when the palette no longer agrees with the
  design library, or when a rename has to land in the codebase. NOT for inventing new token names
  (use naming-conventions for that).
---

# Design Tokens Sync

One direction only: the library is the source, the repository is the copy.

## Procedure

1. Read the published token set from the library, not from a working branch. An
   unpublished change is a proposal, and syncing it is how the app ships a value
   nobody agreed to.
2. Diff the incoming set against the committed theme file. Three buckets: added,
   changed, removed.
3. Removals are the dangerous bucket. A token that disappeared upstream is still
   referenced in the app, so it needs a deprecation alias before it is deleted.
4. Renames arrive looking like a removal plus an addition. Match them by value and
   confirm with the designer rather than guessing.
5. Write the theme file in one commit, with the diff summary in the commit body.
6. Run the build. A token change that compiles is not the same as one that renders.

## Output

- The three-bucket diff, with a line per token.
- Aliases written for anything removed.
- A screenshot pass over the screens that used the changed values.

## Do not

Do not hand-edit the generated theme file. The next sync overwrites it, and the fix
that lived there disappears without a trace.

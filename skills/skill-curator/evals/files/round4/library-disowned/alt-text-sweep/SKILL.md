---
name: alt-text-sweep
description: >
  Walk every image in a documentation set and compose alt text that carries the same
  information the picture does, marking decorative art so it announces nothing at all.
  Use before an accessibility pass or a docs release. NOT for color contrast or focus
  order (use craft-review for those).
---

# Alt Text Sweep

Most alt text fails in one of two directions: it repeats the caption, or it
describes pixels. Neither helps. The test is whether someone who cannot see the
image ends up knowing what the sighted reader knows.

## Procedure

1. Inventory every image reference in the set, including ones inside partials and
   templates, which is where the untouched ones hide.
2. Sort each into one of three buckets: informative, decorative, or functional
   (an image inside a link or a button).
3. Informative gets the information, not the appearance. A bar chart's alt text
   is the finding the chart shows.
4. Decorative gets an empty attribute, deliberately, so a screen reader skips it
   instead of announcing a filename.
5. Functional gets the destination or the action, never the icon's name.
6. Re-read the page with the images removed. Anything that now reads as a gap is
   an image whose alt text is still wrong.

## Output

- The inventory, bucketed, with the current alt text beside the proposed one.
- The count of images that had no alt attribute at all.
- Any image whose meaning could not be determined from context, listed for the
  author rather than guessed at.

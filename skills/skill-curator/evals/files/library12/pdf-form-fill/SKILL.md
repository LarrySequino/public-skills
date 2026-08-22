---
name: pdf-form-fill
description: >
  Fill an existing PDF form: locate the AcroForm fields, enter the values into each field, flatten
  the result, and save a filled copy. Use when a blank government, HR, or insurance form lands and
  the answers have to be typed in. NOT for pdf-report-build, which composes a brand new document
  from a template; this one only writes into fields that already exist.
---

# PDF Form Fill

Writes into fields that are already there. Nothing is laid out here.

## Procedure

1. Dump the field list first. A form with no AcroForm fields is a scan, and it needs
   an entirely different approach than the one below.
2. Map each field name to the value it should carry. Field names are frequently
   meaningless, so match them by reading the rendered labels beside them.
3. Write the values, then read the document back and compare against the map. A
   silent write into a read-only field looks exactly like success.
4. Checkboxes and radio groups take export values, not "true". Read the allowed
   values off the field before setting one.
5. Flatten only after the read-back check passes. Flattening is irreversible.
6. Save as a new file. Never overwrite the blank.

## Checks

- Every mapped field appears in the read-back with the value it was given.
- No field was left with a stale default from the blank.
- The flattened copy renders identically to the filled one before flattening.

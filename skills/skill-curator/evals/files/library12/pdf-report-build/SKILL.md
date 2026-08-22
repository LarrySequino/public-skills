---
name: pdf-report-build
description: >
  Compose a new PDF report from a template and a dataset: page layout, running headers, tables,
  charts, and page numbering, rendered so it prints correctly. Use when a recurring monthly or
  quarterly document has to be generated rather than typed by hand. NOT for pdf-form-fill, which
  enters answers into fields on a document that already exists; this one starts from an empty
  page.
---

# PDF Report Build

Starts from an empty page and a template. There is no source document to edit.

## Procedure

1. Fix the page geometry first: size, margins, and the safe area for the printer.
   Everything downstream is laid out against it, so changing it later is a rebuild.
2. Bind the template to the data source and render one page with real values, not
   placeholder text. Placeholder text hides every overflow bug.
3. Long tables need a repeating header row and a rule for splitting across pages.
   Decide it now rather than discovering it on page nine.
4. Charts render at print resolution, not screen resolution. A chart that looks
   sharp on the monitor prints soft.
5. Page numbers, generation date, and the data cut-off go in the running footer.
   A report without a cut-off date gets read as current forever.
6. Render the whole document and page through it before shipping.

## Checks

- No text sits outside the safe area on any page.
- Every table that spans a page break repeats its header.
- The footer names the data cut-off, not just the render date.

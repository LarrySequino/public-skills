---
name: spreadsheet-formulas
description: >
  Repair and explain spreadsheet formulas: trace precedents, fix broken references, unpick nested
  conditionals, and rebuild a lookup that quietly matches the wrong entry. Use when a workbook
  produces a number nobody can account for, or when a sheet inherited from a colleague has to be
  trusted. NOT for charting the numbers (use dataviz instead).
---

# Spreadsheet Formulas

The problem is almost never the formula that is wrong. It is the formula that is
right and points somewhere unexpected.

## Procedure

1. Find the cell that produces the disputed number and trace its precedents all the
   way back to entered values. Write the chain down; it is usually shorter than
   feared and it is always more surprising.
2. Look for the four classics: a lookup with an approximate match left on, a range
   that stopped growing when rows were added, an absolute reference that should be
   relative, and a hidden row inside a sum.
3. Check the entered values too. A number stored as text sums to zero without any
   error appearing anywhere.
4. Rebuild rather than patch when a formula nests more than three conditionals. A
   helper column is easier to audit than a clever one-liner and nobody wins prizes.
5. Add a check row: totals that must agree, differences that must be zero. A sheet
   with no internal check is a sheet that will be wrong again silently.
6. Explain the fix in the sheet itself, in a note next to the cell.

## Output

The corrected workbook, the precedent chain that explained the error, and the check
row that catches the next one.

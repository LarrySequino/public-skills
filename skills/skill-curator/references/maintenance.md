# Maintenance

Procedure for when the user asks to "check skill-curator," "update the curator," or
"is the curator still right." This skill has no upstream sources to sweep, so its
maintenance is about whether its own claims and tools still hold, not about harvesting.

## What drifts, and how to catch it

This skill makes claims about how other tooling behaves, and that tooling moves under it.
Each claim below names the thing it depends on and the check that catches the drift.

| Claim in this skill | Depends on | Check |
|---|---|---|
| `disable-model-invocation: true` marks a skill explicit-only | Claude Code frontmatter | Confirm the key still exists in current Claude Code docs; rename in `SKILL.md` if it moved |
| The eval format in `harvest-log.md` | Anthropic `skill-creator`, `references/schemas.md` | Diff `evals.json` shape against the installed plugin; update the pointer and the field names if they changed |
| "roughly ten skills in a scope" as the count trigger | Skill discovery budget | Re-read whatever the current harness documents about skill listing limits; adjust the number in `SKILL.md` and in `scripts/audit.py` together |
| The 400-line bloat threshold | Nothing external; a judgement | Leave alone unless evidence arrives |
| `scripts/overlap.py` matches `tools/overlap.py` in the private repo | `publish.sh` copying the right file | `diff` the two; they must be byte-identical |

## Deterministic checks, run every time

These are the steps that are arithmetic, and they go first so the reading is spent on the
table above.

1. `python3 scripts/audit.py --demo` and `python3 scripts/overlap.py` on a known pair. Both must
   print `self-check: PASS`. A script whose self-check fails is not shipped.
2. `python3 scripts/audit.py ~/.claude/skills`, or wherever the user's library lives. Read the
   output as a user would. Anything it flags about *this* skill is fixed before anything else:
   the skill that audits the library does not get to fail its own audit.
3. Run `scripts/overlap.py` with this skill as the target against any source that has been read
   during the session. Zero is the expected result and is recorded in `ATTRIBUTION.md` as the
   control; a non-zero result means text was carried over and `ATTRIBUTION.md` must say from
   where before anything is packaged.

## Then the reading

4. Walk the drift table. For each row, do the check. Record what was checked and the date in the
   log below, including the rows where nothing had moved.
5. Re-read `references/security-screen.md` against the current shape of skill distribution. New
   install paths (a marketplace, a CLI, a plugin format) are new injection surfaces, and the
   screen should name them.
6. Re-read the five jobs in `SKILL.md` against the last three real uses of this skill. A job
   nobody has asked for in a long while is a candidate for folding into another; a request that
   fit none of the five is a candidate for a sixth, or for a sharper description.

## Package

7. Validate frontmatter, confirm `scripts/` ships both tools, and run `audit.py` one last time on a
   directory containing only this skill. Then publish per the private repo's `publish.sh`.

## Log

| Checked | What | Result |
|---|---|---|
| 2026-08-21 | First pass. `audit.py` written and run on a 12-skill library; found three bugs in itself (block-scalar frontmatter, boundary detection, collision metric) and fixed them. `overlap.py` bundled. Provenance check corrected from filename to content after it passed this very skill on a format doc. | Both self-checks PASS. This skill flagged itself NO-PROVENANCE until `ATTRIBUTION.md` was written. |

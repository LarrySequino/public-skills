# Attribution

Original work. `SKILL.md` and both reference files were written here and carry no
third-party expression. Two records say so independently: the library handoff of
2026-08-16 lists it as "Original. No upstream markers," and the private repo's
README as "Mine. No third-party content." No overlap scan against outside sources
has been run, because there are no outside sources to scan against; if that ever
changes, the procedure in `references/maintenance.md` says what to do.

Two things in it are adapted, and both are named so the next audit need not guess.

**The harvest-log format** in `references/harvest-log.md` is our own, but the eval
format it points to is Anthropic's, from the `skill-creator` skill in the
`claude-plugins-official` marketplace. We use its `evals/evals.json` shape rather
than inventing one, and say so there.

**`scripts/overlap.py`** was written for the private skills repo as `tools/overlap.py`
on 2026-08-16 and is bundled here unchanged, so that an installed copy can run the
scan this skill tells you to run. The two files should stay identical; the private
repo's `publish.sh` copies from the tool, not from here.

**`scripts/audit.py`** was written here on 2026-08-21. Its collision check owes an
idea, not a line, to the observation in the `skill-creator` skill that routing sees
only the description.

Measured 2026-08-21 with `scripts/overlap.py`, this skill against the nine anti-slop
sources in the scratch set: zero shared 8-word runs with any of them, which is the
expected result for a skill about a different subject and is recorded as the
control that makes the same scan meaningful on `natural-writing`.

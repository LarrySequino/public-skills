# skills

Three skills for Claude Code, Codex, Cursor, Grok and the other agents the
[`skills` CLI](https://github.com/vercel-labs/skills) installs into: one for prose,
one for UI review, one for keeping a skill library honest.

## Why these exist

Most skills are a checklist the model reads and then grades itself against. These
three put the arithmetic in scripts and leave the model only the judgment. A dash
count, a contrast ratio, a pairwise description comparison across a library: a script
does those exactly in a second, and a model does them approximately and differently
each time. Each skill ships its scripts, a self-check for each script, an eval set in
Anthropic's `skill-creator` format, and an `ATTRIBUTION.md` that records where the
text came from as a measurement rather than a recollection.

## The skills

| Skill | What it does | Use when |
|---|---|---|
| [**natural-writing**](skills/natural-writing/SKILL.md) | Strips AI patterns from prose: write, rewrite, audit, or edit a file in place. Tiered vocabulary read live from the catalog, false-positive gates, a hard no-fabrication rule with a `--compare` check that lists every specific a rewrite added. | You say "deslop", "humanize", "make it sound human", or ask what AI tells are in a text; or you're drafting prose for publication. Fires on its own for those. Not for code or commit messages. |
| [**craft-review**](skills/craft-review/SKILL.md) | Reviews UI screens and flows. Reads exact values from source or Figma, computes contrast, spacing and symmetry with bundled scripts, then reports severity-ranked findings with numeric fixes. | You ask "does this look right", "review this screen", or share a screenshot or Figma link for feedback. Fires on its own. Not for turning mocks into a decision doc. |
| [**skill-curator**](skills/skill-curator/SKILL.md) | Maintains a skill library: audits for description collisions and bloat, vets third-party skills before install, harvests ideas without carrying phrasing, and scans for verbatim overlap against every source. | You ask to clean up or audit your skills, vet a skill before installing it, merge two that overlap, or check a skill's sources for updates. Not for writing a new skill from scratch. |

## What you get

**natural-writing** runs its scanner before it reads. Counts, never a verdict:

```
$ python3 skills/natural-writing/scripts/prose-scan.py draft.md

=== draft.md (80 words) ===
  vocabulary: references/vocabulary.md (58/41/37 terms)
  [DASH] 1 in 80 words = 12.5 per 1,000 (cap is 1). A voice sample overrides this.
  [INVISIBLE] 1x zero-width space (U+200B)
  [ARTIFACT] sycophantic opener: "Great question"
  [TIER1] "tapestry" — gated to the figurative sense, check this one
  [FORMAT] heading looks Title Case: "The Evolving Landscape Of Modern Systems"

  These are counts, not a verdict. Judgment checks are in references/preflight.md.
```

and `--compare original.md rewrite.md` prints every number, year, citation and name the
rewrite introduced that the source did not have. Zero is the only passing result.

**craft-review** computes before it judges:

```
$ python3 skills/craft-review/scripts/contrast.py --demo
       #000000 on #FFFFFF   21.00:1  want 21.00  ok
       #767676 on #FFFFFF    4.54:1  want  4.54  ok
```

`preflight.py` catches the artifact bugs a reader misses in one theme: a color defined
only inside a dark-mode block, a body with no background of its own, a contrast failure
resolved per theme. `symmetry.py` turns "looks unbalanced" into an inset delta in pixels.

**skill-curator** does the part of an audit that grows as the square of the library:

```
$ python3 skills/skill-curator/scripts/audit.py ~/.claude/skills
  [BLOAT] emil-design-eng: SKILL.md is 675 lines and loads whole on every trigger
  [NEAR-PAIR] emil-design-eng vs review-animations: share philosophy, emil, kowalski,
              animation, and neither names the other. Check whether one prompt could match both.
  [NO-PROVENANCE] apple-design: no file records where it came from
```

and `overlap.py` compares a skill against its sources in runs of eight words, which is
how this repo found its own attribution gap (below).

## Install

One command, for Claude Code, Codex, Cursor and Grok at once:

```bash
npx skills add LarrySequino/skills -g -s '*' -y \
  -a claude-code -a codex -a cursor -a grok
```

Three details, because each one is easy to get wrong:

- **`-a` takes one agent.** Repeat the flag. Comma-separated and space-separated both
  fail with `Invalid agents`.
- **`-g` installs user-level.** Without it you get a project-local install inside
  whatever directory you happen to be in.
- **Codex and Cursor get no directory of their own.** They read the shared store at
  `~/.agents/skills`. Claude Code and Grok get symlinks. All four work even though
  only two have folders.

Then confirm it landed, because a partial install is silent:

```bash
ls ~/.agents/skills            # natural-writing  craft-review  skill-curator
head -3 ~/.agents/skills/natural-writing/SKILL.md
```

Leave off `-a` entirely to be asked which agents you have; `--agent '*'` writes a
directory into your home folder for every agent the CLI knows about, installed or not.
Updating and removing are the CLI's own commands, documented
[there](https://github.com/vercel-labs/skills).

### claude.ai and Cowork

Neither has a CLI and neither can pull, so this is manual. A `.skill` file is a zip:

```bash
git clone https://github.com/LarrySequino/skills && cd skills/skills
zip -rD ../../natural-writing.skill natural-writing
```

Upload it at **Settings → Capabilities → Skills**. Uploading the same name overwrites.

## Provenance

Every skill carries an `ATTRIBUTION.md` naming what it descends from, what was
harvested as ideas and written fresh, and what expression carried over. Those files
record measurements: each skill is scanned against every source in runs of eight
words, short enough to catch a lifted sentence and long enough that a hit means copying
rather than two people describing the same thing.

That method found a gap in this repo's own work. **natural-writing began as a fork of
[stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop)** (MIT)
and shares 6,169 eight-word runs with it, the longest unbroken stretch running 1,189
words. Its parent credited two sources of its own, and those credits were lost in the
fork. All three are now in `ATTRIBUTION.md`, and the scanner is at
[`tools/overlap.py`](tools/overlap.py) if you want to run it on yours.

## Evals

Each skill ships `evals/evals.json` in the format Anthropic's `skill-creator` uses:
prompts with checkable expectations, run with the skill and without, three runs each.
Scripts decide every expectation a script can decide; a reader decides the rest, with a
quoted line of evidence per verdict. The full per-run record is in each skill's
`evals/results/`. First run, 2026-08-21, Opus 5, 96 executor runs:

| Skill | With | Without | Delta | Behavior-only delta* |
|---|---|---|---|---|
| natural-writing | 0.905 | 0.790 | **+0.11** | +0.11 |
| skill-curator | 0.979 | 0.804 | **+0.17** | +0.12 |
| craft-review | 0.800 | 0.850 | **−0.05** | −0.09 |

*Excluding expectations of the form "the transcript shows the skill's script was run,"
which can only pass with the skill present and so measure availability, not behavior.

**craft-review lost to its own baseline**, and the per-eval record says why. It wins
where its scripts catch what a reader misses (a color defined only inside a dark-mode
block: +0.33), ties where the model already does the arithmetic unaided (contrast
ratios, a 6px inset), and loses on the two evals that test restraint: handed a one-line
verbal description with nothing to measure, all three with-skill runs scored the page
anyway ("Distinctiveness 3/10, in the rework band") and issued severity-tagged findings
about a screen they had never seen, while the baseline said it could not review from a
description. The skill's severity and scoring machinery fires on things it has not
measured. That is a defect, it is now known, and the fix and re-run are the next entry
in this table.

**natural-writing** is ahead on five of seven evals, even on one, and behind on one by a
single check: one run in three produced one em dash against a six-dash voice sample,
the predicted collision between the dash cap and the voice-sample override.

The grader was wrong three times before any skill was, and each time against the
skill: a regex that read "named `landscape` and cleared it" as flagging it, a synonym
check that failed "watch the results" for not saying "monitor," and "AA needs 4.5:1"
cited as a standard read as a reported finding. Each was caught by reading the answers
and each would have published a wrong number. The method held up; the first draft of
the grader did not, which is the argument for the method.

## This repo is generated

Published one-way from a private working repo; files here are overwritten on every
publish, so edits made directly to this repo are lost. Issues and pull requests are
read and applied upstream by hand.

## License

MIT. Each skill's `ATTRIBUTION.md` carries the notices for what it inherited.

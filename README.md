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
words, short enough to catch a lifted sentence and long enough to skip most coincidence.
A single hit is a lead to read, not proof: generic prose can collide. Volume and run
length are what settle it.

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
| craft-review | 0.750 | 0.833 | **−0.08** | −0.13 |

*Excluding expectations of the form "the transcript shows the skill's script was run,"
which can only pass with the skill present and so measure availability, not behavior.

**craft-review lost to its own baseline in round 1**, and the per-eval record says why. It wins
where its scripts catch what a reader misses (a color defined only inside a dark-mode block:
+0.33), ties where the model already does the arithmetic unaided (contrast ratios, a 6px
inset), and loses on the two evals that test restraint. Handed a one-line verbal description
with nothing to measure, all three with-skill runs scored the page anyway ("Distinctiveness
3/10, in the rework band") and issued severity-tagged findings about a screen they had never
seen. On a well-built page, it tagged taste remarks `[judged]` and still chipped them Major.
One defect: the severity and scoring machinery fired on things it had not measured.

**Round 2** re-ran the three affected evals against the fixed skills, same day, same model,
3+3 runs each, round 1 left intact at `76d11d7` for comparison:

| Eval | Skill | Round 1 | Round 2 |
|---|---|---|---|
| unmeasurable-is-said-so | craft-review | 0.50 vs 1.00 | **1.00 vs 0.92** |
| clean-page-is-called-clean | craft-review | 0.25 vs 0.50 | **1.00 vs 0.58** |
| voice-sample-precedence | natural-writing | 0.92 vs 1.00 | **1.00 vs 1.00** |

All three with-skill runs on the description-only prompt now refuse to score and quarantine
advice under a heading that says it is not a review of the screen. On the well-built page,
every severity chip traces to `[computed]` or `[observed]` evidence and taste sits unchipped
under a Judgment calls section; the baseline put taste among its fixes in 2 of 3 runs. The
voice sample's dash rate now wins 3 of 3.

Two things the second round exposed about the evals themselves, recorded in each
`evals.json`. The "clean" page was not clean under a review deeper than `preflight.py`: a
`64ch` measure runs about 87 characters, and the page had no `lang`, no `color-scheme`, and a
48/64px frame. The skill was right to find those, and the round-1 expectations that rewarded
not looking were rewritten to test reporting discipline instead; round 1 was re-graded on the
same yardstick, which is why its craft-review number above is lower than first published. And
four of the sixteen evals are floors both arms clear, because inline CSS hands the baseline
every value. The skills' edge is on inputs a reader cannot hold in their head, and the next
set of fixtures has to be built that way.

**natural-writing** is ahead on five of seven evals, even on one, and behind on none after
round 2.

The grader was wrong before any skill was, each time against the skill: a regex that read
"named `landscape` and cleared it" as flagging it, a synonym check that failed "watch the
results" for not saying "monitor," "AA needs 4.5:1" cited as a standard read as a reported
finding, and a chip counter that took "a minor point" for a severity label. Each was caught
by reading the answers, and each would have published a wrong number. The method held; the
first draft of the grader did not, which is the argument for the method.

### Round 3: fixtures a reader cannot hold in their head

Round 1 left four evals as floors both arms cleared, because inline CSS and three-file
libraries hand the baseline every value. Round 3 built inputs where the answer is not visible at a
glance. A 1,537-word document with seven scattered tells, a 442-line stylesheet
whose only contrast failure sits inside a dark-mode block behind three `var()` hops, one
off-scale padding among 62 declarations, an asymmetry no source value states, and a
twelve-skill library with one real collision and one red herring that scores higher on raw
term overlap. 48 runs, same day, same model:

| Skill | With | Without | Delta | Behavior-only |
|---|---|---|---|---|
| natural-writing | 0.907 | 0.811 | **+0.10** | +0.06 |
| skill-curator | 1.000 | 0.833 | **+0.17** | +0.07 |
| craft-review | 0.967 | 0.775 | **+0.19** | −0.04 |

The per-eval deltas are where the design shows: the 62-value spacing page **+0.25**, the
layout-only asymmetry **+0.25**, the long audit **+0.29**.

craft-review's behavior-only number is negative for a reason worth publishing. In 2 of 3
runs its own contrast machinery generated Critical findings that outranked the defect
`preflight.py` had explicitly blocked on, and one run demoted that blocked defect to Major
and put two of its own findings above it. The skill found more and buried what it was
pointed at. `SKILL.md` §6 now says a `[BLOCK]` is Critical and sorts first; three re-runs
against the fixed skill put it at row 1 every time.

Three round-3 expectations turned out to encode false premises, all in craft-review, all
from verifying a fixture only with the tool under test. The control borders really are
1.43:1, the layout really has no breakpoint, and runs were being marked wrong for finding
them. All three are rewritten to test reporting discipline, both rounds re-graded on one
yardstick, and each correction is recorded in `evals.json` with what changed and why.

### Round 5: what happens when the checks get their own evals

Every check added while fixing round 3 shipped without eval coverage. Round 5 built six
fixtures for them and ran 36 more runs. The result is mostly negative, and that is the
useful part:

| Eval | With | Without | What it measures |
|---|---|---|---|
| no-invented-names-when-made-concrete | 0.94 | 0.50 | **+0.44, the one real discriminator** |
| light-edit-keeps-facts-and-voice | 0.78 | 0.67 | mostly a floor |
| dark-only-token-is-not-a-defect | 1.00 | 0.73 | regression guard; behavior identical |
| copied-code-under-original-prose | 1.00 | 0.80 | availability, not behavior |
| disowned-script-is-not-a-missing-script | 1.00 | 0.80 | availability, not behavior |
| alpha-only-contrast-failure | 1.00 | 1.00 | floor |

Behavior-only: natural-writing **+0.28**, craft-review **+0.04**, skill-curator **+0.00**.

One of six evals separates the arms on behavior. On the fabrication test all three baselines
invented figures, invented product names, and flagged **zero** gaps: asked to make vague copy
concrete, they filled the vagueness in rather than asking what belonged there. The with-skill
runs flagged the gaps and left the names alone. The other five evals are floors or regression
guards, and are labeled as such in each `evals.json` so a headline delta is not mistaken for a
behavioral win. Their value is that they fail loudly if a future change re-breaks a check, which two
changes did during this round.

### Across model families

The same two prompts went to eight model and harness combinations with no skill attached:
"rewrite this and make it specific" over a vague paragraph, and "deslop this" over prose that
was already human. Every one invented specifics the source never contained (`$4,200/month`,
`Redis`, `March 4`, `420ms`) and every one rewrote the already-good prose, keeping between 29
and 59 percent of it.

| Model | Invented specifics | Source surviving the rewrite |
|---|---|---|
| grok-4.6 | 7 numbers, 3 names | 32% |
| gemini-3.7-flash | 15 numbers | 29% |
| gpt-5.6-terra | 6 numbers | 46% |
| claude-opus-5 | 11 numbers | 59% |
| deepseek-chat | 7 numbers | 41% |
| GPT via codex | 1 name | 50% |
| Grok via its CLI | 7 numbers, 3 names | 40% |

These are the two failures `natural-writing` exists to prevent, and no family is exempt.
`prose-scan.py --compare` now catches 7 of the 8 fabrications and all 8 over-rewrites; the
one it passes used bracketed placeholders instead of inventing values, which is the correct
answer.

Running the skills themselves on another family is a smaller claim. GPT with `skill-curator`
scored 1.00 on the twelve-skill audit against 0.90 unaided, and with `craft-review` 1.00
against 0.80, but behavior-only both deltas are **+0.00**: GPT found the buried 3.74:1 chip by
writing its own luminance function in a heredoc, and read the twelve-skill library closely
enough to catch every planted defect. The skills are usable by a non-Anthropic agent, which
was worth establishing. On these fixtures they do not measurably change what it produces.

## This repo is generated

Published one-way from a private working repo; files here are overwritten on every
publish, so edits made directly to this repo are lost. Issues and pull requests are
read and applied upstream by hand.

## License

MIT. Each skill's `ATTRIBUTION.md` carries the notices for what it inherited.

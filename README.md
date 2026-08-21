# skills

Three skills for Claude and about seventy other agents, maintained against a
measured provenance trail rather than a vibe.

| Skill | What it does |
|---|---|
| **natural-writing** | Strips AI patterns from prose. Write, rewrite, audit, or edit files in place. Tiered vocabulary, false-positive gates, and a preflight checklist, so it doesn't flag ordinary human writing. |
| **craft-review** | Visual and UX review for UI screens. Measures spacing, contrast, alignment and typography with bundled scripts *before* it judges, then reports severity-ranked findings with numeric fixes. |
| **skill-curator** | Maintenance for a skill library: audit for trigger collisions, vet third-party skills before installing, merge duplicates, and check upstream sources for updates. |

## Install

One command, for Claude Code, Codex, Cursor and Grok at once:

```bash
npx skills add LarrySequino/skills -g -s '*' -y \
  -a claude-code -a codex -a cursor -a grok
```

Leave off `-a` entirely to be asked which agents you have. The CLI supports about
70, so `--agent '*'` is a trap: it writes a directory into your home folder for
every agent it knows about, installed or not.

Three details worth knowing, because each one is easy to get wrong:

- **`-a` takes one agent.** Repeat the flag. Comma-separated and space-separated
  both fail with `Invalid agents`.
- **`-g` installs user-level.** Without it you get a project-local install inside
  whatever directory you happen to be in.
- **Codex and Cursor get no directory of their own.** They read the shared store at
  `~/.agents/skills`. Claude Code and Grok get symlinks at `~/.claude/skills` and
  `~/.grok/skills`. All four are working even though only two have folders.

Then:

```bash
npx skills list                                   # what you have
npx skills update                                 # pull newer versions
npx skills add LarrySequino/skills --list         # preview without installing
npx skills remove natural-writing                 # take one back out
```

### Output styles

Output styles live in [LarrySequino/output-styles](https://github.com/LarrySequino/output-styles).
They install differently (a file copy, no CLI) and only Claude Code reads them, where these
skills work across about 70 agents.

### claude.ai and Cowork

Neither has a CLI and neither can pull, so this is manual and stays manual. A
`.skill` file is a zip:

```bash
git clone https://github.com/LarrySequino/skills && cd skills/skills
zip -rD ../../natural-writing.skill natural-writing
```

Upload the result at **Settings → Capabilities → Skills**. Uploading the same name
overwrites, so there is nothing to delete first.

## This repo is generated

It's published from a private working repo, one-way. Files here are
overwritten wholesale on every publish, so **edits made directly to this repo
will be lost.** Issues are welcome and read. Pull requests are welcome too,
but they get applied upstream by hand rather than merged here.

## Provenance

Every skill here carries an `ATTRIBUTION.md` naming what it descends from, what
was harvested as ideas and written fresh, and what expression carried over. Those
files record measurements, not impressions: each skill is scanned against every
source in runs of eight words, which is short enough to catch a lifted sentence
and long enough that a hit means copying rather than two people describing the
same thing.

That method found a gap in this repo's own work. **natural-writing began as a fork
of [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop)**
(MIT) and shares 6,169 eight-word runs with it, the longest unbroken stretch
running 1,189 words. Its parent credited two sources of its own, and those credits
were lost in the fork. All three are now in `ATTRIBUTION.md`. The scanner is in
this repo as `tools/overlap.py` if you want to run it on your own.

My working library also holds skills adapted from other people that stay private
until their licensing is sorted. A prose credit inside a file does not satisfy a
license.

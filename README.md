# skills

Skills I wrote for Claude, published for anyone to use.

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

`output-styles/` holds Claude Code output styles. They are plain files with no CLI, so
installing one is a copy:

```bash
git clone https://github.com/LarrySequino/skills
mkdir -p ~/.claude/output-styles
cp skills/output-styles/*.md ~/.claude/output-styles/
```

Then pick it in `/config`, or set it directly in `~/.claude/settings.json`:

```json
{ "outputStyle": "Shipmate" }
```

**Shipmate** is the one here. Outcome first, bullets over prose, explicit recommendations,
no filler, and it keeps Claude Code's coding behavior rather than replacing it.

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

## Scope

Only skills that are wholly mine are published here. My working library also
contains skills adapted from other people's work, which stay private until
their licensing is properly sorted out — a prose credit inside a file doesn't
satisfy a license.

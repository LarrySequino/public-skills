# Harvest Log Format

The provenance record that makes a maintained skill updatable instead of re-derivable. Lives inside the skill it describes, usually at `references/maintenance.md`, and is read only when the user asks for a refresh.

## Structure

Four parts, in this order.

### 1. Source watchlist

Ranked by signal density, highest first, so a partial pass still covers the sources that matter. For each: URL, one line on what it is good for, and where to look inside it (a changelog, a version-history section, a specific page). Note fetch quirks — a domain that blocks automated access needs a documented workaround so the next pass doesn't rediscover the problem.

Include a line on discovering new sources: what search would surface newcomers, and the instruction to screen them before fetching.

### 2. Harvest criteria

What earns inclusion, stated as conditions rather than aspirations, plus what to reject on sight. Copy the criteria from the curator skill and add anything specific to this skill's domain — especially any hard constraint that new material must never weaken.

### 3. Update procedure

Numbered steps from "copy the installed skill somewhere writable" to "present the packaged file." Include which destination file each kind of harvested item belongs in, any size ceiling on the main file, and the reminder that the agent cannot install the result.

### 4. Log table

| Source | Last checked | Version/state at check |
|---|---|---|
| project-a | 2026-07-28 | 2.9.1 (patterns 1–33; harvested no-fabrication rule) |
| project-b | 2026-07-28 | upstream 3.4.0; local fork already ahead |
| project-c | 2026-07-28 | dormant, single release, skip next pass |
| ad-hoc source | 2026-07-29 | harvested X; rejected flat bans on Y as over-correction |

The version column is what makes the next pass a diff instead of a re-read. Record enough to identify what was seen: a version number, a release tag, a commit count, or a dated description of the state. Record rejections in the same row — future passes will otherwise re-evaluate the same rejected material and reach the same conclusion at full cost.

## Rules

- Update the log in the same pass that harvests, never afterward from memory.
- If a source can't be verified, write "unverified" rather than a guess.
- Keep dormant sources in the table with a note to skip; removing them means rediscovering them later.
- When a skill is renamed, keep the former name in the log so older references resolve.

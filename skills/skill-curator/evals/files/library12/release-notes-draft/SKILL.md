---
name: release-notes-draft
description: >
  Turn the changes merged since the last tag into release notes grouped by reader impact, with
  breaking changes and upgrade steps listed first. Use when cutting a version and the notes still
  have to be written, or when a draft reads as a bare list of commits. NOT for writing the commit
  messages themselves (use commit-style instead).
---

# Release Notes Draft

Turns the merged pull requests since the last tag into notes a user can read in one
pass. The draft is organized by what the change means to the reader, never by the
part of the system it touched.

## Before drafting

1. Get the exact commit range. `git log <last-tag>..HEAD` is the input; the issue
   tracker is a cross-check, not the source.
2. Drop every merge commit, revert pair, and change that was reverted before the tag.
   A revert pair in the notes is a change that never shipped.
3. Group by reader impact using the sections below, in the order they appear.
4. Write each entry as one sentence in the present tense, starting with the effect.
5. Keep the whole draft under a page. Anything longer gets skimmed, which defeats
   the reason for writing it.

## Section reference

Each section below has the same shape: what belongs in it, what to leave out, the
sentence pattern, and a worked example. Sections with nothing to say are deleted
from the draft rather than left empty with a "none this release" line.


### 1. Features

**What belongs here:** a change that adds capability a user can reach.

**Rule:** Lead with what the user can now do, not with the module that changed.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> New export format in the reporting menu.

**Rewrites of entries that failed review**

- Rejected: "Refactored the features handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to features." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "New export format in the reporting menu." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 2. Fixes

**What belongs here:** a change that restores intended behavior.

**Rule:** Name the symptom the user saw, then the release it appeared in.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Sorting by date put empty values first.

**Rewrites of entries that failed review**

- Rejected: "Refactored the fixes handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to fixes." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Sorting by date put empty values first." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 3. Performance

**What belongs here:** a change that alters time or memory, with a measured number.

**Rule:** An unmeasured performance claim is marketing; leave it out.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Bulk import runs about forty percent faster on large files.

**Rewrites of entries that failed review**

- Rejected: "Refactored the performance handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to performance." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Bulk import runs about forty percent faster on large files." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 4. Breaking changes

**What belongs here:** a change that requires action before upgrading.

**Rule:** Every entry needs the action, the deadline, and the failure if skipped.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> The legacy token endpoint is gone; move to the session endpoint.

**Rewrites of entries that failed review**

- Rejected: "Refactored the breaking changes handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to breaking changes." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "The legacy token endpoint is gone; move to the session endpoint." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 5. Deprecations

**What belongs here:** a change that announces future removal.

**Rule:** Give the removal version, not just the word deprecated.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> The v1 webhook payload is deprecated and goes away in 4.0.

**Rewrites of entries that failed review**

- Rejected: "Refactored the deprecations handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to deprecations." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "The v1 webhook payload is deprecated and goes away in 4.0." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 6. Security

**What belongs here:** a change that closes a vulnerability.

**Rule:** Say what an attacker could do, in one sentence, without a proof of concept.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Session cookies are now scoped to the issuing subdomain.

**Rewrites of entries that failed review**

- Rejected: "Refactored the security handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to security." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Session cookies are now scoped to the issuing subdomain." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 7. Dependencies

**What belongs here:** a change to a pinned version that users can observe.

**Rule:** Only list a dependency bump when it changes behavior or a minimum version.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Minimum supported runtime is now 20.11.

**Rewrites of entries that failed review**

- Rejected: "Refactored the dependencies handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to dependencies." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Minimum supported runtime is now 20.11." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 8. Documentation

**What belongs here:** a change to the docs that answers a repeated question.

**Rule:** Link the page; a documentation entry with no link is noise.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Added a page on rotating API keys without downtime.

**Rewrites of entries that failed review**

- Rejected: "Refactored the documentation handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to documentation." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Added a page on rotating API keys without downtime." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 9. Internal

**What belongs here:** a change with no user-visible effect.

**Rule:** Almost always cut. Keep only what explains a behavior change elsewhere.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Rewrote the scheduler to drop the polling loop.

**Rewrites of entries that failed review**

- Rejected: "Refactored the internal handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to internal." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Rewrote the scheduler to drop the polling loop." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 10. Known issues

**What belongs here:** a defect shipping in this release on purpose.

**Rule:** State the workaround. An issue with no workaround belongs in the blocker list.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Imports over two gigabytes time out; split the file.

**Rewrites of entries that failed review**

- Rejected: "Refactored the known issues handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to known issues." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Imports over two gigabytes time out; split the file." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 11. Upgrade notes

**What belongs here:** the ordered steps to get from the previous version to this one.

**Rule:** Numbered, in order, with the one irreversible step called out.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Run the schema migration before starting the new binary.

**Rewrites of entries that failed review**

- Rejected: "Refactored the upgrade notes handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to upgrade notes." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Run the schema migration before starting the new binary." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 12. Rollback notes

**What belongs here:** what happens if the upgrade is reversed.

**Rule:** If rollback is impossible after a migration, that sentence goes first.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> The 3.4 schema is not readable by 3.3 once migrated.

**Rewrites of entries that failed review**

- Rejected: "Refactored the rollback notes handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to rollback notes." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "The 3.4 schema is not readable by 3.3 once migrated." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 13. Contributors

**What belongs here:** credit for the change, matched to the change.

**Rule:** Pull the names from the merged commits, never from memory.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Thanks to the reporters of the import timeout.

**Rewrites of entries that failed review**

- Rejected: "Refactored the contributors handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to contributors." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Thanks to the reporters of the import timeout." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


### 14. Metrics

**What belongs here:** the numbers that describe the release itself.

**Rule:** Counts of merged changes, open defects closed, and days since the last tag.

**Sentence pattern:** effect first, then the condition it applies under, then the
version or action if one is needed. Present tense. No internal identifiers unless
the reader can search for them.

**Worked example**

> Forty-one merged pull requests, eleven defects closed.

**Rewrites of entries that failed review**

- Rejected: "Refactored the metrics handling in the core module." No reader
  effect, no action, no version. Cut entirely.
- Rejected: "Various improvements to metrics." Says nothing. Either name the
  improvement or delete the line.
- Accepted: "Forty-one merged pull requests, eleven defects closed." One effect, stated once, in a sentence a user can act on.

**Review checklist for this section**

- [ ] Every entry names an effect a reader can observe or act on.
- [ ] No entry starts with a module, file, or class name.
- [ ] No entry restates another entry in different words.
- [ ] Entries are ordered by how many readers they affect, most first.
- [ ] Anything requiring action links to the page that describes the action.
- [ ] The section is deleted rather than left empty.


## After drafting

1. Read the draft cold, as a user on the previous version. Every question it raises
   that the draft does not answer is a missing entry.
2. Check the breaking-change and upgrade sections against the migration, one line at
   a time. These two are the sections that cost people their evening when wrong.
3. Have the change authors read only their own entries. They catch inverted meaning
   faster than anyone reviewing the whole draft.
4. Publish the notes with the tag, not after it. Notes that arrive a day late are
   read by nobody who upgraded on day one.

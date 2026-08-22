---
name: api-docs-publish
description: >
  Generate and publish reference documentation from an OpenAPI description: group operations the
  way a caller searches, add a request and reply example per operation, check that the examples
  still validate, and push the built site. Use when an endpoint moved and the published reference
  is stale. NOT for the marketing pages (use landing-copy instead).
---

# API Docs Publish

The reference is generated. Everything a generator cannot know is the actual work.

## Procedure

1. Validate the description before building. A reference generated from an invalid
   document builds happily and omits whole operations.
2. Group operations by the task a reader arrives with, not by path prefix. Readers
   search for "cancel a subscription", never for "/v2/subs".
3. Every operation needs one request and one response example with real-looking
   values. Generated examples full of "string" teach nobody anything.
4. Validate the examples against the schema as part of the build. Examples drift from
   schemas faster than prose drifts from behavior.
5. Diff against the published version and write the changed-endpoints list. It is the
   only part most readers will read.
6. Publish, then load three pages and check that the code samples copy cleanly.

## Output

The built site, the changed-endpoints diff, and the list of operations that still
have no description beyond their generated summary.

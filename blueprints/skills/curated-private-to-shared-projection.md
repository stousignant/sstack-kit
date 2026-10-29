# Curated Private-to-Shared Projection

## Purpose

Create a repeatable, reviewed content selection from a private source without transferring its environment or history. This is a design for controlled projection, not an exporter, publication grant or proof that a destination is safe.

Use it when the same approved subset will be refreshed repeatedly. For one-off explanation, independent authorship may be cheaper and clearer than maintaining selectors.

## Inputs

- Exact source revision and regular files approved for consideration.
- Private selection manifest, allowed extraction modes and destination layout.
- Destination base, managed outputs and destination-owned content that must remain untouched.
- Audience, disclosure rules, licence obligations and task-specific authority.
- Private staging, review and recovery locations, such as `<staging-dir>` and `<report-dir>`.

A path approval is not content clearance. If authority, source identity or destination ownership is unclear, stop before applying or uploading.

## Flow

1. Select individual source-relative files explicitly. Reject absolute or traversing paths, symlinks, duplicates, missing files, unsupported types and implicit recursive inclusion.
2. Copy a file byte-for-byte only after its complete contents are certified for the audience. For a mixed file, extract only a uniquely marked approved section. Missing or duplicate markers fail closed; never fall back to the entire file.
3. Build a clean staged candidate. Preserve approved relative layout or review a layout change first. Compare all additions, replacements and stale managed deletions with the destination base; never remove destination-owned content.
4. Review populated bytes, local links, credentials, personal information, licence and environment assumptions. Check that the output makes sense without the private source. Keep disclosure policy and detailed lineage outside the output.
5. Under explicit apply authority, install only the reviewed managed set and read it back. Upload, Git publication and visibility changes require their own scoped authority and exact payload review. A selector must not automatically commit or push.

### Synthetic example

A manifest permits `guide.md` as a reviewed complete file and a uniquely marked public section in `notes.md`. A new refresh removes one approved section marker. The projection must fail with a safe category, leaving the destination unchanged. Copying the whole notes file would violate the design even though its path was allowed. This example describes an acceptance case, not an executed export.

## Boundaries

Never copy private history, policy, configuration, credentials or runtime evidence into the shared payload. Even source paths and hashes may disclose sensitive information; share only deliberately approved attribution. Keep full lineage private.

Installed hooks and public CI are partial controls, not pre-upload privacy clearance. Review exact outgoing refs, messages, titles, bodies and attachments before uploading; API payloads bypass Git hooks. Public diagnostics contain safe categories/counts, not private filenames, matches or surrounding text.

Neither a private destination nor passing structural checks grants publication authority. If the candidate changes after review, recheck the changed payload rather than substituting new source silently.

## Outputs

Produce a staged managed-file set and a private receipt recording source and destination identity, selected paths/modes, differences, checks, omissions and unresolved failures. Report staging, installation and publication as separate states; leave unperformed transitions explicitly unproven.

## Adaptation

Choose the smallest selector that the content warrants. Exact file copies minimize transformation; marker extraction suits stable mixed documents but makes marker integrity load-bearing. Frequent editorial changes may justify independently authored shared documents instead. Do not expand into a general migration engine merely to avoid reviewing a few files.

## Verification

Use synthetic fixtures before trusting an implementation:

- A permitted path containing private material is blocked by content review.
- Missing/duplicate markers and unsafe paths fail without partial application.
- Source deletion removes only a stale managed output, never destination-owned files.
- The staged set matches the reviewed selection and remains useful without private dependencies.
- Changed source or API prose after clearance requires fresh exact-content review.
- Private lineage and detector policy remain private; no automatic commit, push or upload occurs.

These checks validate an implementation only when actually exercised. This recipe alone establishes no operational result.

# Skill Library Hygiene Review

## Purpose

Review a bounded skill-library inventory and prepare proposals that help maintainers improve discoverability, ownership clarity, and upkeep.

## Inputs

- The repository root, such as `<repo-root>`, and the agreed skill-library roots within it.
- The previous review report, when available.
- The current ownership and usage evidence that the maintainer has approved for this review.
- A report destination such as `<report-dir>`.

## Flow

1. Inventory the agreed roots and record the review scope.
2. Check names, owners, references, and evidence for missing or unclear maintenance signals.
3. Rotate a deeper review across bounded groups over successive runs; record which group the current review covered.
4. Draft prioritized proposals with evidence, uncertainty, and expected impact.
5. If a required root is unreadable, report failure rather than a clean review. Treat a missing previous report as unavailable rotation context and state the resulting coverage limit.
6. Return the report to a maintainer for a separate decision.

### Worked synthetic example

The review covers six entries in `<repo-root>/skills/group-a`, with `group-a` as this run's deeper-review group. Evidence is limited to the approved ownership index, references within the agreed roots, and a usage summary covering the last 30 days. The index assigns `<capability-alpha>` to `<maintainer-a>`, while an in-scope ownership note names `<maintainer-b>`; two in-scope references point to it. `<capability-beta>` has no owner entry, is referenced by `<capability-gamma>` in two in-scope files, and has one recorded use in the window; the usage summary does not cover other contexts.

Expected proposals: ask the maintainers to reconcile `<capability-alpha>` ownership and confirm its references; ask a maintainer to confirm ownership of `<capability-beta>` and whether its two references remain current. Mark the second proposal uncertain because usage coverage is limited. Do not edit either entry or reference, and do not propose retirement from age or low usage alone.

Failure case: if an agreed root is unreadable, return `FAILURE`, name the unavailable root, and state which portion was not reviewed; do not report a clean review or propose actions for unseen entries. If the previous report is missing, state that rotation context is unavailable and limit any coverage claim accordingly.

## Boundaries

- Treat any cadence as a suggestion for review planning, not a deployed schedule.
- Do not edit, rename, archive, delete, install, deploy, or otherwise change skills or runtime state.
- Do not infer that low usage or age alone makes a skill disposable.
- Keep private implementation details and secret contents out of the report.

## Outputs

Write a proposal report containing the reviewed scope, the deeper-review group, prioritized findings, supporting evidence, confidence, and unresolved questions. The report is advisory and does not apply its proposals.

## Adaptation

Choose repository-specific roots and a review rotation that fit the available ownership and usage evidence. State the limits of those inputs and retain the proposal-only boundary. A weekly inventory and monthly rotating deeper review can be a starting cadence; adapt it to maintainer capacity rather than treating it as a deployed schedule.

## Verification

Confirm that the review stayed within its declared scope, made no repository or runtime changes, and returned proposals for maintainer review only.

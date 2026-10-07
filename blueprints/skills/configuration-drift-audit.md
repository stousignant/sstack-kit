# Configuration Drift Audit

## Purpose

Compare declared configuration intent with the current configuration state. Produce a concise, read-only account of meaningful differences for an operator to review.

## Inputs

- A repository root such as `<repo-root>`.
- A configuration directory such as `<config-dir>`.
- The reviewed source files that declare expected settings.
- The corresponding current settings, with secret values kept out of the review output.
- Optional context about known unrelated local changes.

## Flow

1. Read the declared settings and current state without changing either.
2. Compare names, structure, and non-secret values needed to identify drift.
3. Classify missing, added, changed, and unreadable settings.
4. Keep unrelated local changes separate from configuration findings.
5. Write a short report under `<report-dir>`, outside the compared scope, for human review so the report does not itself become configuration drift.

### Worked synthetic example

The declared settings list `mode=review`, `region=west`, and `timeout=30`. Current state lists `mode=apply`, `region=west`, and `retry_limit=2`. A secret setting also exists, but its value is not read into or shown in the report.

Expected report: `changed: mode`, `added: retry_limit`, `missing: timeout`, and `unchanged: region`; unrelated local changes are separate; secret values are omitted; comparison result is `PASS - complete`, with drift status `REVIEW REQUIRED`. If a required current-state file is unreadable, expected result is `FAILURE - comparison incomplete`, with the unavailable input named and completed comparisons distinguished from unknown settings. Do not call unobserved settings clean. In either case, leave compared inputs unchanged and write the report outside their scope.

## Boundaries

- Do not read secret contents into the report or copy them to another location.
- Do not apply fixes, write configuration, commit changes, or claim unrelated repository dirt is clean.
- Do not infer that an absent or unreadable setting is safe.
- Stop with a clear failure result when required inputs cannot be read or compared.

## Outputs

Return a report with the compared scope, drift categories, unreadable inputs, unrelated changes, and an explicit pass or failure result. Omit secret values and avoid treating an incomplete comparison as clean.

## Adaptation

Map the declared-intent files and current-state reader for the repository in scope. Keep the comparison read-only, preserve the same failure boundaries, and describe any narrower coverage in the report.

## Verification

Confirm that the comparison left inputs unchanged, that each required input was read or reported unavailable, and that no secret value appears in the report.

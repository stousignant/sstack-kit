# Source-to-Runtime Adoption

## Purpose

Reconstruct a controlled path from reviewed source to target installation and authorized behavior loaded by a real consumer. This is an evidence method, not an installer or proof of activity.

Keep three proof surfaces separate: source review describes the candidate; projection or file installation proves target state; runtime verification proves what a consumer loaded or observably does. Each transition needs scoped authority, which an owner may explicitly supply together, such as routine instruction activation for a named skill target. Apply any existing hold or source-only restriction. A merge alone does not authorize installation, and a changed file or link does not prove activation.

### Why separate evidence

Transitions can fail independently or be outside scope. Report the strongest verified layer; leave later layers unproven.

## Inputs

Gather only what is needed to plan a bounded change:

- Canonical source, candidate revision, scoped files, and review status; distinguish proposed from accepted or integrated changes.
- Declared targets, explicit exclusions, the consumer, and available evidence; do not assume a runtime layout.
- Current target snapshot and ownership, including local, unknown, or other-owner changes. Choose a non-sensitive comparison identity, such as resolved target or content revision.
- Actual authorization. Source review, installation, activation/restart, and cleanup are separate scopes; source-only approval leaves targets untouched.
- Report destination such as `<report-dir>`; for an approved apply only, a private backup location outside the managed discovery surface.

If target, exclusions, ownership, or approval is unclear, stay read-only and report the gap.

## Flow

### Reconstruct the transition

1. Review the candidate revision, intended change, and consumer fit. A merge or integration alone is not install approval; check whether the owner explicitly included the named installation and activation targets.
2. Inventory targets and exclusions; compare the target snapshot with the expected mapping. Dry-run exact changes and prior identities. If a target is omitted, ambiguous, dirty, or other-owner, stop before overwrite and preserve it.
3. For a reversible apply covered by the actual authorization, first make and identify a private backup. Before the first write, verify that the backup is readable and sufficient to restore the prior target state, and that the target-specific restore plan has the required access, bounded scope, and consumer recovery checks. If rollback cannot be bounded, stop; non-reversible handling requires its own explicit authorization and plan. Apply only the reviewed plan, read back each target, and record projection identity. Stop if effects differ.
4. Verify activation authority separately from its evidence; obtain approval if the intended instruction reload or new session is not already covered. Restarts and other operational changes need their own authorization. Use a safe independent method and verify loaded revision or affected behavior. Process health alone is insufficient.
5. Cleanup also needs separate approval. Remove only known in-scope temporary artifacts; retain backups while rollback may be needed and record leftovers.

### Synthetic example

Suppose candidate B was merged and the installed target points to B, but the consumer still reports A or shows old behavior. Source and disk may be verified; runtime is not. Do not call B active. After authorized safe activation, check real affected behavior. On failure, follow the bounded rollback plan and verify it; if activation, observation, or rollback is uncertain, report that status as unknown or unproven. This is synthetic, not an executed deployment.

## Boundaries

Default to read-only inspection. This blueprint grants no permission to merge, write targets, activate/restart, or clean up. Source review, an existing link, and a successful dry run grant none of these permissions.

Preserve unrelated and other-owner changes. Stop on mismatch; do not force links, replace dirty targets, or expand scope. Keep backups private and rollback bounded to the approved target; a backup alone does not prove safe rollback. Provide no database repair recipe or runnable restart command.

## Outputs

Separate proposed from executed work. Retain this minimum artifact map:

- Source revision and reviewed change.
- Declared targets and excluded scope.
- Target snapshot and projection identity, or why no apply occurred.
- Consumer-loaded revision or exact observed behavior, including its limits.
- Rollback receipt: backup identity and verified rollback, or `not applied`, `not attempted`, `incomplete`, or `unknown`.

Mark each layer verified, not verified, or unknown. Separate dry runs, writes, tests, and real consumer observation. Never imply an unperformed merge or activation.

## Adaptation

A copied file has independent bytes: compare target content with the approved source. For a symlink, verify resolved target and its content; a link change does not show what a consumer loaded. A process may retain stale data after either change through session, service, or harness caching. Verify loaded revision or targeted behavior. Behavior proves only the checked case, not exact revision or every path.

Choose the least invasive supported method. Keep mapping, reload semantics, and rollback harness-neutral until the consumer is known. Without reliable observation or bounded rollback, stop at the last verified layer and state the limitation.

## Verification

Pressure-test the method against these cases:

- **Source-only approval:** report source evidence without installing or activating the candidate.
- **Unusable backup or unbounded restore:** stop before the first write rather than treating backup existence as rollback readiness.
- **Omitted target:** reject plans that touch undeclared scope; leave targets unchanged.
- **Stale consumer:** disk points to B while the consumer remains at A; runtime stays unproven until scoped authorized activation and real observation succeed.
- **Foreign-owned dirty target:** preserve it and stop before overwrite, even if completion is blocked.
- **Failed apply or incomplete rollback:** stop mutation, safely read back state, retain the backup, and report the gap without claiming recovery.

A good report lets a reviewer trace source, target, and consumer evidence, and see where authorization or proof ends.

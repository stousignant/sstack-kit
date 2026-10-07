# Resumable Batch Processing

## Purpose

Design a finite, explicitly authorized batch that can resume after interruption without losing failures, replaying uncertain side effects, or claiming unverified work. Checkpoints preserve evidence for a later run; they do not keep a process alive or guarantee durable execution.

This is not a scheduled-feed or briefing pattern. Start from a frozen inventory, not a changing stream. A changed snapshot is a new input revision and never silently expands the authorized batch.

## Inputs

Record the frozen inventory, stable item IDs, and inventory fingerprint. IDs must not depend on list position. For every item, define permitted stages, dependencies, output destination, acceptance checks, and allowed external effects.

Capture each source identity and fingerprints for stage logic, configuration, parameters, and upstream artifacts. Specify deterministic outputs, checkpoint fields, bounded retry and resource limits, and stop conditions. Use existing simple storage and locking tools; a new queue, database, or service is not required.

## Flow

1. Validate authorization and freeze the inventory. Store state for every item and stage. Keep `done`, `failed`, `blocked`, `skipped`, `unknown`, and `in-progress` distinct. Never let an ordinal cursor hide an earlier failure.
2. Acquire one writer lease using the existing lock mechanism. Record and refresh its owner token. A conflicting live lease blocks work; a stale heartbeat alone does not prove its owner is dead. Before reacquiring an expired lease, require the existing mechanism to exclude the stale owner: for example, atomic reacquisition issues a newer fencing token that the artifact and checkpoint stores enforce on every write. A client-side token check alone cannot prevent a delayed write. If the existing mechanism cannot guarantee exclusion, refuse reclamation and pause for authorized owner resolution. Do not delete or steal unrelated locks.
3. Derive each stage key from its source, logic, configuration and parameters, and verified upstream artifacts. Reuse a checkpoint only when these identities match and every artifact passes integrity checks. A checksum proves byte identity, not semantic correctness; run the acceptance probe after restore or reuse.
4. Write a deterministic stage artifact, read it back, verify it, then record its inputs, key, artifact identity, state, and evidence. After a crash in the artifact/metadata gap, reconcile the deterministic output. Adopt it only after verification; otherwise rerun safely or mark `unknown` if effects are ambiguous.
5. On restart, compare recorded state with the frozen inventory and current fingerprints. Invalidate only changed stages and their dependents. Preserve unaffected verified work and prior outputs; replace outputs only when authorized. Run stages only after dependencies verify, within retry and resource limits.
6. Stop at the grant or limit. Keep unfinished and ambiguous items visible; do not widen scope or spend beyond authorization.

Example: item-01 is verified and `done`, item-02 fails midway, and item-03 has not started. On restart, reuse item-01 only after its inputs, checkpoint, artifact, and acceptance probe still verify. Resume item-02 at its earliest stage with verified dependencies, then process item-03 when ready. Corrupted output is not reused. Changed logic invalidates affected stages and dependents even if old checksums match. An ambiguous external effect remains `unknown` until reconciled.

## Boundaries

This provides resumable state, not exactly-once execution. Deterministic outputs and readback close the artifact-write/checkpoint gap when repeating a stage is safe. For a non-idempotent external action, use an authorized idempotency mechanism or reconcile its actual outcome. If neither is possible, mark it `unknown`; do not claim success or replay arbitrarily.

Failures stay in the ledger. A skip is not completion. A changed snapshot, new item, or revised authorization needs a separately reviewed run. Resumption never grants permission to process newly discovered work.

## Outputs

Keep the inventory identity, per-item and per-stage states, fingerprints, checkpoint metadata, verified artifacts, retry history, and failure reasons. Generate the final report from stored state: authorized total, verified done, failed, blocked, skipped, unknown, in-progress, coverage, checks, and unresolved items. Count each stable item ID once using its current stages: unresolved effect uncertainty takes precedence as `unknown`, then `failed`, then active `in-progress`, then `blocked` for unmet dependencies or permission. Untouched queued work is `blocked` with a not-started reason. Otherwise classify the item as `skipped` if required work was intentionally omitted, or `done` only when all required stages and item-level checks verify. Keep stage counts separate and require item categories to sum to the frozen inventory total. Claim complete only when every mandatory item passes its acceptance checks and none remains unresolved; otherwise report partial, blocked, or failed.

## Adaptation

Use the simplest existing storage that supports atomic metadata updates and an exclusive writer lease. A local batch may need only a lock file and structured checkpoint records; shared execution needs equivalent ownership and atomicity. Add complexity only when concurrency, recovery, or audit requirements justify it.

Unlike a feed, this workflow does not poll for new items. A changed input snapshot or stage logic causes targeted invalidation and reruns only affected stages and dependents. Preserve verified results and avoid unauthorized overwrites. Without reliable integrity checks or safe reconciliation, prefer `unknown` and human review over stronger durability claims.

## Verification

Before reporting completion, verify:

- The artifact-write/checkpoint crash gap reconciles without unverified success or unsafe replay.
- Changed source, logic, or configuration invalidates the correct stages and dependents.
- Corruption is detected; restored artifacts pass integrity and semantic acceptance checks.
- A conflicting live lease blocks another writer; stale heartbeat does not trigger lock stealing. After authorized reacquisition, a resumed stale owner cannot write artifacts or checkpoints; without that guarantee, reclamation is refused.
- Ambiguous effects remain `unknown`, and skipped items remain distinct from completed ones.
- Counts and coverage match the frozen inventory; any mandatory failed, blocked, unknown, or in-progress item prevents a complete claim.

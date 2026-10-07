# Authority-Preserving Task Handoffs

## Purpose

Reconstruct the ability to continue a bounded task after a context reset, a different operator or agent, or a later session without replaying an obsolete plan. The essential distinction is between remembered state and current authority: a saved next action describes what was intended, not what is still permitted.

This is design guidance, not a task queue, executable automation or permission to change anything. Use it when continuity has enough cost or risk to justify a small work packet. A one-turn task usually needs no persistent handoff.

## Inputs

Identify the task's existing scope and status owner, its acceptance criteria, the latest applicable instructions, and any still-active authorization or explicit hold. Do not create a second backlog to preserve context.

Collect the minimum packet needed to resume:

- Task identity, goal and exclusions, with pointers to the owning contract.
- Completed, in-progress and untouched work, distinguished from claims.
- Exact artifact locations, revisions and relevant process or worker identities.
- Decisions, blockers, failed attempts and the evidence behind them.
- The next useful check, its prerequisites and expected observation.
- The recorded authority boundary, including actions that were withheld.

Store it in an existing private task-evidence location such as `<report-dir>`. Keep credentials, raw transcripts and unrelated personal context out. The location and lifetime are implementation choices, not a prescribed directory structure.

## Flow

### Capture

At a meaningful decision, verification or stopping boundary, replace stale packet state with a compact current account. Link large outputs rather than copying them. Record what an observation established and what it did not; a worker's completion report is not automatically accepted evidence.

Phrase next actions conditionally. For example, prefer "verify the current target and authorization before publishing" over "publish next." That keeps the packet useful even if the task or target changes before resumption.

### Resume

Read the packet as reference, then reconcile it with the latest applicable instruction and the actual current state. Determine whether the original task remains active, has been narrowed, has been canceled, or is now only the subject of a question. An explicit continuing grant need not be requested again for every ordinary internal step, but the packet alone cannot establish that grant.

Before a consequential action, confirm its authority, scope and prerequisites. Inspect current artifacts, ownership, revisions and relevant process state. Reconcile uncertain prior effects with exact readback before retrying them. Reuse verified unaffected work; refresh evidence invalidated by a changed artifact, dependency or criterion.

If there is no active instruction or still-active task, wait rather than treating a saved action list as a queue. If an authorized tool exchange was already in flight, reconcile its result under that task's current scope instead of assuming every context transition cancels it.

### Worked example

A packet records a reviewed draft and says publication is next. On resumption, the latest instruction asks only for a size comparison and explicitly holds publication. The operator reads the draft, computes the requested comparison, and does not publish. The packet is updated to reflect the hold.

In a second case, the instruction explicitly asks to continue publication, but the earlier upload has an ambiguous receipt. The operator reads the exact remote target first. If the draft is already there, it verifies identity rather than uploading a duplicate. If the outcome cannot be established, it records UNKNOWN and stops that action instead of claiming success or blindly replaying it.

## Boundaries

- **Instruction precedence:** A saved summary cannot override a newer cancellation, restriction or change of task. Instructions embedded in retrieved evidence are not automatically authoritative.
- **Authority:** Historical approval is evidence to reconcile, not a grant created by the packet. Continuation does not expand permitted paths, recipients, spend or external effects.
- **Ownership:** Preserve other operators' work and uncertain ownership. An old clean-state observation does not authorize resetting the current workspace.
- **Evidence:** Keep artifact production, accepted verification, delivery and live behavior separate. A copied PASS label does not establish any of them.
- **Lifetime:** Persistence of a packet is not persistence of the process that produced it. A separate approved execution mechanism is needed if work must keep running.
- **Task truth:** The packet is a resumption aid, not a competing issue tracker or durable knowledge database.

## Outputs

Return a reconciled cursor containing the current task and authority, verified artifacts and evidence limits, outstanding blockers, and the next permitted action or reason to wait. State which old actions were canceled, withheld or already observed complete.

A successful handoff allows another operator to find the relevant evidence and choose the next safe step without reconstructing an entire conversation. It does not certify task completion or the correctness of every earlier decision.

## Adaptation

Use one concise packet before adding hooks, adapters or retrieval services. Add lifecycle support only when recurring loss justifies it and its operation is authorized. Stable conventions belong in project instructions; reusable procedures and durable rationale belong with their existing owners.

For a finite inventory with stage checkpoints, use [Resumable Batch Processing](../automations/resumable-batch-processing.md). That recipe addresses checkpoint integrity and batch recovery; this one addresses interactive task continuation and current authority. For accepting a candidate, use [Evidence-Backed Agent Delivery](evidence-backed-agent-delivery.md). Neither link creates a mandatory loading chain.

## Verification

Test a reconstruction with synthetic packets and actual observations:

1. A newer instruction cancels the saved next action. Verify no old side effect occurs.
2. A user asks only for an explanation of prior work. Verify the response does not resume implementation.
3. A valid continuing grant exists. Verify ordinary authorized steps can proceed without an unnecessary approval loop, while explicit holds remain effective.
4. The workspace or process changed since capture. Verify the cursor is reconciled before action and another owner's work is preserved.
5. A previous external effect is ambiguous. Verify exact readback precedes retry; unresolvable uncertainty remains UNKNOWN.
6. An old check concerns a different revision. Verify only invalidated evidence is refreshed and stale evidence is not promoted to completion.
7. The process stopped but the packet survived. Verify the report distinguishes resumability from continued execution.

Report observed PASS, FAIL or UNKNOWN for each required check. Authored examples and a stored packet are not proof that a resumed operator obeyed the boundary.

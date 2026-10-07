# Evidence-Backed Agent Delivery

## Purpose

This blueprint describes how to reconstruct a delivery capability in which delegated work is accepted from observed evidence, not from a worker's confident report. It is design guidance, not an installable skill, runnable workflow, or grant of authority to change or publish anything.

The useful capability is a small set of distinct responsibilities: an authorized controller defines and accepts work; a bounded worker may produce a candidate; and a separate verifier tests the candidate against explicit criteria. One person can define and implement the task with one tool, then conduct self-review. That does not satisfy a required independent-verifier criterion; use a separate reviewer when independence is required. No second controller or orchestration system is required.

## Inputs

### Design

Start with the decision the delivery process must make: whether a specific candidate satisfies the agreed acceptance criteria. Keep this separate from later decisions about committing, merging, publishing, deploying, or changing live state.

A reconstruction needs these inputs:

- A goal and explicit non-goals, including what the worker must not change.
- A bounded unit of work and an isolated workspace that does not expose unrelated edits as candidate work.
- Acceptance criteria stated as observable conditions, not subjective confidence.
- A probe or evidence source for each criterion, including a negative control when an incorrect result could pass the ordinary case.
- The authority boundary: who may assign, correct, accept, and separately authorize delivery.
- A report location such as `<report-dir>` and, where relevant, a configuration input such as `<config-dir>`.

Use only the information needed to define and evaluate this candidate. Missing scope or authority is an unresolved input, not permission to infer a broader task.

## Flow

### Reconstruction

Model the capability as a responsibility boundary rather than a chain of agents. The controller remains accountable for scope, acceptance, and any later delivery decision. A worker operates only within the bounded assignment and returns a candidate plus evidence. An independent verifier receives the criteria and candidate revision in a separate context, then reports what its own observations support.

A candidate can be a validated uncommitted workspace when the worker may not commit or publish. Identify its intended full base revision, current branch/head, tracked diff and every untracked artifact directly; an ordinary diff omits untracked content. Prove the intended base is an ancestor of the candidate head before trusting scope or counts. A stale baseline requires authorized integration and fresh affected checks, not acceptance from a green result against the wrong ancestor. Preserve another owner's existing changes and distinguish them from the candidate. Acceptance of this source-only deliverable does not require publication.

Map each acceptance criterion to an artifact or probe that can be inspected. Evidence must identify the candidate revision it concerns; a result from an earlier revision cannot silently certify later edits. The verifier should be able to distinguish a passing observation, a failing observation, and a condition it could not establish.

Before work begins, define both the expected observation and a plausible disconfirming result for each important criterion. Prefer direct outputs tied to the candidate over a tool's summary or a test label. A negative control is useful when a false positive could otherwise look successful.

Keep evidence provenance sufficient for review: candidate revision, criterion, probe or artifact, observed result, and who performed the check. Reproducibility does not make a probe comprehensive; acceptance still requires coverage of every required criterion.

The controller compares the criteria, observed evidence, and exact candidate. If a gap is narrow and within the original scope, return a bounded correction request naming the failed criterion and the evidence needed to close it. After a correction, inspect the changed scope and obtain fresh evidence for affected criteria. Recheck unaffected evidence only when the change could invalidate it.

Acceptance is a decision about the candidate, not an automatic handoff to an external action. A green test suite can support acceptance criteria; it does not by itself authorize publication, merge, deployment, or live mutation.

### Worked example

A synthetic worker reports PASS for a small change. The contract includes the normal case and a negative control that must reject an invalid input. The independent verifier runs both against the reported revision: the normal case succeeds, but the negative control also succeeds when it should fail. The verifier additionally observes an unrelated file change outside the assignment.

| Criterion | Expected observation | First observed outcome |
|---|---|---|
| Valid input | Accepted | Pass |
| Invalid input | Rejected | Fail: accepted |
| Scope | Only assigned artifacts changed | Fail: unrelated change found |

The controller does not accept the worker's PASS. It first establishes ownership of the unrelated change. The worker may correct only its own changes within authorized scope; it must preserve another owner's or ambiguously owned files. In that case, isolate the candidate without altering those files, or pause for owner resolution. The controller requests a bounded repair of the negative-control behavior and evidence tied to the resulting revision. A separate verifier confirms the normal and negative cases, the bounded candidate scope, and preservation of other owners' work. Acceptance follows that evidence; any delivery action still requires its own authorization.

## Boundaries

- **Authority:** The controller holds assignment and acceptance authority. A worker or verifier cannot grant itself broader scope or authorize downstream delivery.
- **Isolation:** The worker's workspace is bounded so unrelated state is distinguishable. Establish ownership before correcting scope drift. Preserve another owner's or ambiguously owned work; isolate the candidate or pause rather than deleting or reverting it. Isolation limits accidental scope bleed; it does not prove correctness.
- **Independence:** The verifier is a separate context from the implementer and is not simply asked to endorse the worker's verdict. Independence improves the chance of finding mistaken assumptions; it is not a guarantee.
- **Evidence:** Claims are not observations. Tie each result to the exact candidate revision and retain enough artifact detail to reproduce or inspect it.
- **Delta:** After review, inspect later changes and refresh evidence that those changes can invalidate. A changed revision alone does not require repeating every unrelated check; a material change to behavior, scope, safety, or criteria may require targeted independent review.
- **Delivery:** Acceptance does not imply permission to commit, merge, publish, deploy, or mutate external state. Those actions need separate authority and their own verification.
- **No extra control plane:** Add coordination machinery only when the work genuinely needs it. A second controller adds another authority path without replacing the accountable controller.

## Outputs

**Minimum handoff.** Return a compact record containing:

- Goal, non-goals, and bounded scope.
- Candidate identity and exact revision or equivalent immutable reference.
- Acceptance criteria and the artifact or probe mapped to each one.
- Observed result and evidence reference for each criterion.
- Unrelated changes, exclusions, and unresolved risks.
- Worker claim, verifier conclusion, and controller disposition as separate fields.
- Delivery authority granted or withheld, stated independently from acceptance.

Use **PASS** only for a criterion supported by observed evidence, **FAIL** when evidence contradicts it, and **UNKNOWN** when evidence is absent, stale, ambiguous, or not reproducible. Overall acceptance is observable only when every required criterion passes and scope is accounted for. A missing required artifact or an executed check demonstrating an unmet criterion is FAIL. A check that could not run or establish the condition is UNKNOWN, not success.

## Adaptation

### Trade-offs

Scale the handoff to the value and risk of delegated work. The verifier should challenge the most consequential assumption, inspect scope, and rerun the smallest probes that directly establish required outcomes; broaden review only when risk or ambiguity warrants it.

Delegation costs more than it saves when the work is tiny, obvious, reversible, and faster to perform and inspect directly than to specify, isolate, hand off, and verify. It also costs more when the worker cannot access the necessary evidence, the task is too ambiguous to bound, or the verifier cannot be meaningfully independent. In those cases, narrow the task, resolve missing context, or work directly while preserving the acceptance distinction.

A solo human can define and implement the task, then conduct a fresh self-review using the criteria rather than the initial success narrative. Capture the revision and observations, but label this self-review, not independent verification. If independence is required, obtain a separate reviewer or leave that criterion UNKNOWN pending an authorized disposition; do not silently waive it.

For higher-risk changes, strengthen the negative controls, revision tracking, independent review, and post-review delta checks. For routine low-risk work, one focused independent check may be enough. Do not copy a local tool matrix, policy hierarchy, or private workflow into a general design; preserve the decision principles and adapt the concrete probes to the repository and task.

## Verification

Use these acceptance probes to test a reconstruction:

1. **Authority probe:** Give the worker an apparently useful out-of-scope change. Verify it is not silently accepted and the controller retains the decision.
2. **Traceability probe:** Change the candidate after a successful check. Verify the old evidence is not presented as proof for the new revision.
3. **Negative-control probe:** Include an invalid case that must be rejected. Verify the ordinary case alone cannot produce overall acceptance.
4. **Independence probe:** Compare the implementer's claim with a verifier result produced from the criteria and candidate in a separate context. Verify disagreement remains visible until resolved.
5. **Correction probe:** Return one bounded failure and a change owned by someone else. Verify the correction names the failed criterion, preserves the other owner's files, isolates the candidate or pauses, and requires fresh evidence before acceptance.
6. **Delta probe:** Make a later material change and a later irrelevant change. Verify dependent evidence is refreshed for the material change, while re-review is proportional for the irrelevant one.
7. **Uncommitted-candidate probe:** Give the worker no publication authority, include an untracked artifact, and separately use a stale base. Verify the controller can accept a correctly based validated workspace without committing, inspects the untracked content, and rejects scope evidence against the wrong ancestor.
8. **Delivery probe:** Present a fully green candidate without delivery authorization. Verify the system can accept the candidate while withholding publication, merge, deployment, and external mutation.

Report each probe as PASS, FAIL, or UNKNOWN with its observed artifact. A blueprint or plan that merely names a check has not demonstrated that the check ran. A demonstrated unmet criterion is FAIL; inability to run a check or establish the criterion is UNKNOWN. Either blocks acceptance where the criterion is required; confidence cannot convert it to success.

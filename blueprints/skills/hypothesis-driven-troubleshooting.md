# Hypothesis-Driven Troubleshooting

## Purpose

Use this recipe for a concrete failure with multiple plausible mechanisms. Narrow them with the lowest-risk useful observation, then propose a structural remedy. A root-enough cause is actionable for a failure class, not proof of unique, complete truth. Analyze design conditions, not personal blame.

## Inputs

Gather only what is needed to define and safely distinguish the failure:

- Observed failure, affected scope, impact, and last known good state.
- A fact timeline with source and time; mark gaps rather than fill them with theory.
- Failing and healthy comparisons: what is IS and what is IS NOT true.
- Plausible mechanisms and evidence that would support or falsify them.
- Available data, safest useful probe, and separate authority for containment, probing, repair, and production validation.

Prefer sanitized or synthetic data. Missing evidence or permission stays an open question.

## Flow

1. Define failure and impact. Record the last known good state and timeline before forming explanations. If urgent recovery is needed, use authorized containment first; record the change, not as causal proof.
2. Contrast failing and healthy cases across relevant dimensions such as input, time, location, environment, and operation. Keep observed distinctions; a healthy case narrows scope but does not establish cause.
3. Keep competing hypotheses while evidence allows. For each, state its mechanism, predicted observation, and concrete falsifier. Branch when mechanisms differ; do not force five whys or a fixed cause count.
4. Choose the smallest safe probe that separates the hypotheses. State what stays constant, the single factor varied, and what result favors or falsifies each explanation. Reproduction shows recurrence; observation records what happened; causal evidence links mechanism to failure.
5. Update from results. Unsupported causes remain hypotheses. If results are inconclusive, keep uncertainty and choose a better safe discriminator or stop.
6. Propose a structural remedy and controlled verification for the supported failure class. Proposal, permission to implement, implementation checks, and production validation are separate decisions.

### Worked example: large records fail

A synthetic processing path succeeds on small records but fails on large ones. The initial favorite is a timeout. These hypotheses predict different evidence:

| Hypothesis | Prediction | Falsifier |
|---|---|---|
| Processing exceeds a deadline | Complete input arrives; processing crosses the deadline. | Input is truncated at a fixed boundary and fails promptly. |
| An input boundary silently truncates large records | Receiver input stops at a fixed size; downstream failure is prompt. | Complete input arrives and failure follows deadline-length processing. |

A safe discriminator uses synthetic records in a non-production path, holds format and runtime constant, varies only record length, and observes receiver byte count and elapsed time. Hypothetically, small records arrive complete while large ones are cut off at the same boundary and fail promptly. This weakens the timeout guess and supports an input-boundary mechanism; no real probe is claimed. The healthy small-record case narrows the contrast but does not prove the whole path healthy.

A structural fix proposal is to make the size contract explicit and either process supported large records completely or reject over-limit records before partial processing. Proposed, not executed, regression expectations: complete handling below and at the limit, safe rejection or complete handling above it, and unchanged small-record behavior. Symptom disappearance alone proves neither cause nor fix.

## Boundaries

- **Read-only default:** collect evidence and use nondestructive probes. State-changing experiments need separate authorization and safeguards. If a destructive probe is declined, do not run it.
- **Separate permissions:** inspection does not authorize probing; probing does not authorize repair; repair does not authorize production validation. Necessary, authorized containment may precede diagnosis but is not proof of cause.
- **No blame or forced method:** explain actions through system conditions; do not force Five Whys, three causes, or a single root cause unsupported by evidence.
- **No overclaim:** correlation, reproduction, or symptom disappearance alone is not causal proof. Keep alternatives and unknowns visible.
- **Proportionality:** use broader incident or safety procedures only when impact or requirements demand them; this is not a full incident-management system.

## Outputs

Return a compact record of failure and impact, timeline facts, IS / IS NOT distinctions, hypotheses and falsifiers, probe and authority, evidence, conclusion and uncertainty, proposed fix, and verification expectations. Label facts, hypotheses, observations, inferences, and proposals where needed. Never imply a proposed fix or check was run without fresh evidence.

## Adaptation

For a low-risk reproducible defect, a short timeline, two plausible hypotheses, and one safe discriminator may suffice. For intermittent, high-impact, or safety-sensitive failures, expand comparisons, preserve evidence, and involve required processes. If no safe probe separates candidates, state what is unknown and request evidence or authority. Stop when an actionable mechanism and testable remedy are supported; continue if it could change the remedy or prevent a materially different failure.

## Verification

Pressure-test the method:

1. **Wrong initial favorite:** contradictory evidence changes the assessment instead of being rationalized.
2. **Inconclusive probe:** candidates remain indistinguishable; the conclusion stays unknown.
3. **Unsafe probe:** a destructive experiment is declined; it is not run, and a safe alternative or stopping point is recorded.
4. **Healthy counterexample:** one case works and another fails; contrast narrows but does not prove a cause.
5. **Symptom disappears:** no causal claim without evidence for the predicted mechanism and controlled regression expectations.
6. **Method pressure:** stop short of five whys or three causes when evidence supports fewer or different branches.

State whether checks are proposed or exercised. This blueprint defines expected outcomes; it does not show that a repair, regression test, or production check ran.

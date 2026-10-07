# Evidence-First Tool Evaluation

## Purpose

Decide whether to keep an incumbent, add or replace it, build a missing capability, or take no action. Reconstruct this decision method, not a private skill or tool stack. Documentation or a security review alone does not prove usefulness for a specific workload. Trace consequential claims, preserve uncertainty, and test only what could change the decision.

## Inputs

### Decision frame

Record the actual gap, workflow, decision owner, incumbent, candidates, and no-build/no-adoption option. State the required outcome and separate must-haves from preferences; a feature cannot compensate for a failed must-have.

### Evidence and trial scope

Classify each material claim as documented contract, behavior in a named shipped version, locally observed behavior, or unmerged proposal. Proposals establish proposed behavior only. A local checkout shows what that checkout contains, not what ships, unless release evidence confirms it.

Before a trial, define representative held inputs, comparable conditions, expected observations, and pass, reject, and inconclusive thresholds. Bound permissions, duration, spend, data exposure, and rollback. If a safe, representative trial is not authorized, stop at evidence review and report the uncertainty.

## Flow

### Reconstruct the decision

1. State the gap in observable terms and establish the incumbent's limitation. Check the smallest no-build or no-adoption option first.
2. Inspect primary evidence only for claims that could change the choice: official documentation for stated behavior; versioned source, tests, or release notes for shipped behavior; recorded checks for local observations; and the official proposal record for open work. Preserve disagreements.
3. Keep a claim ledger with version, claim, source pointer or observation provenance, unknowns, and trial outcome. Unavailable evidence stays unknown.
4. If a consequential question remains, run a bounded reversible trial only with the owner's permission. Keep workload, permissions, and conditions comparable; do not upload private inputs without explicit approval.
5. Compare raw observations with predeclared thresholds, then state inference and limitations separately. Choose adoption, qualified use, incumbent retention, build, or no action only as supported.

### Synthetic example

A team needs a required field extracted from internal forms. The incumbent handles common fields but misses the mandatory field. Candidate A claims to fix it, but evidence is only an unmerged proposal. Candidate B is documented and shipped, and already handles common fields. Before a permitted local trial, the owner sets 12 held forms, requires every mandatory field, caps the trial at one hour, bars external upload, and defines any missed mandatory field as rejection.

| Option/version | Claim | Primary-source pointer or provenance | Unknown | Trial outcome |
|---|---|---|---|---|
| Incumbent/current | Handles common fields; misses required field | Baseline check on held forms | Other form types | One required-field miss in baseline |
| A/proposal only | Proposed fix for required field | Official unmerged proposal | Shipped version and behavior | Not trialed |
| B/4.2 | Shipped partial extraction | Versioned docs, source, and test | Broader form coverage | Missed required field on 2 of 12 forms |

B fails the predeclared threshold; A has no verifiable shipped behavior to trial. Those are bounded raw observations, not a gain estimate or proof about other workloads. The inference is that neither candidate meets the must-have on this set. Defer adoption. Retaining the incumbent is only a temporary operational fallback if authorized, with the mandatory requirement explicitly still unmet; it is not an acceptable result or proof of coverage. Do not adopt A based on proposal language or average away B's blocker.

## Boundaries

- Research, trial, install, promotion, and live enablement are distinct actions with separate authority. Research approval is not trial or deployment approval.
- Never trial without explicit permission for scope, environment, inputs, and limits. Do not request credentials or upload data without explicit approval.
- A documented, implemented, security-passed, or impressive feature is not proof it solves the gap.
- Do not let weighted scores conceal a must-have failure or claim precise gains from a tiny or unmatched sample.
- Scale source checks and trial breadth with the stakes; this is a targeted decision, not an exhaustive comparison.
- Roll back only trial-owned changes. Preserve unrelated work; isolate or pause if ownership is unclear.

## Outputs

### Decision record

Report gap and scope; incumbent, candidates, and no-adoption option; must-haves and thresholds; the claim ledger; comparable raw observations; separate inference; disposition and uncertainty; and any next approval needed. Never imply a proposal shipped or a trial ran without evidence.

## Adaptation

### Trade-offs

A cheap, reversible choice may need a focused source check and one direct probe. A costly, sensitive, or hard-to-reverse replacement warrants stronger version verification and representative controls. If the incumbent meets requirements, extra features may not justify migration. Build only when a mandatory gap remains and simpler supported options fail; otherwise retain the incumbent or choose no adoption.

## Verification

Exercise the reconstructed method and retain artifacts:

1. **Proposal:** Show an exciting feature in an unmerged proposal; verify it remains proposed, not shipped.
2. **Missing source:** Make a primary source unavailable; verify the claim is unknown, not passed.
3. **Must-have:** Fail one required criterion while passing preferences; verify rejection despite any aggregate score.
4. **Trial:** Present no permission, unmatched inputs, or an inconclusive small sample; verify no unauthorized or precise result is claimed.
5. **Cleanup:** Add unrelated work during a trial; verify rollback preserves it and pauses if ownership is unclear.
6. **Authority:** Present a positive research result; verify install, promotion, and live enablement still require separate approval.

Report each check as pass, fail, or unknown with its artifact. A named fixture is not proof it ran. A failed must-have blocks adoption for the stated scope.

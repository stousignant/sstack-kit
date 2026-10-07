# Ownership-Aware Capability Consolidation

## Purpose

Use this method when procedures appear to teach the same capability and a maintainer must decide whether to keep, specialize, redirect, or consolidate them. Aim for one actionable owner per reusable procedure without erasing unique scope, safety conditions, or consumers. Similarity is a discovery clue, not proof of duplication or permission to edit.

### Why map ownership first

A consolidation can break a caller, weaken an exception, or exceed authority. Map requirements, interfaces, and consumers first. Ownership confidence and change authority are separate: strong evidence may support a proposal while the authorized action remains no change.

## Inputs

Collect only what a bounded comparison needs:

- Candidate procedures and revisions; read their instructions, triggers, exceptions, and outputs.
- Material requirements, task boundaries, and non-trigger conditions.
- Search terms and bounded surfaces: names, paths, headings, commands, output tokens, trigger phrases, prompts, tests, manifests, projections, and scripts.
- Known consumers and exact interfaces, including implicit routes and uninspected surfaces.
- Owner and authorization for each source, destination, caller, and compatibility surface.

If the owner, consumer boundary, or authority is unclear, preserve behavior and mark the question unresolved. Do not infer permission from a relationship graph, annotation, successful search, or prior edit.

## Flow

### Minimum build: requirement-to-owner map

Create one row per material requirement: stable ID, behavior and trigger/non-trigger conditions, source evidence, current owner, consumers, exact interface, classification, destination or redirect, authority, and required proof. Classify as `KEEP`, `OWNED_ELSEWHERE`, `SPECIALIZATION`, `MIGRATE`, `ALIAS_OR_PROJECTION`, or `UNRESOLVED`. An alias or projection points to an owner; it is not automatically another owner.

Inspect behavior, not filenames. Distinguish duplicates from specializations that narrow eligibility, add evidence, or carry conditional authority. Keep a specialization with its narrow owner if moving it broadens its trigger or weakens its boundary. Give the reusable method one actionable owner; caller guidance only routes to it.

### Bound the search and choose a disposition

Search exact interfaces, then distinctive triggers and likely indirect consumers. Record surfaces, terms, exclusions, and gaps; classify findings as active consumers, history, or noise. State confidence only within those bounds. Empty link searches, no observed usage, age, and similarity do not prove obsolescence or universal absence.

Choose no change when scopes differ or a common owner would blur them. Consolidation may not justify added hops, larger common-task context, interface risk, or small savings. Preserve useful specializations when moving a shared core.

### Prove before retiring

For an authorized move, write the destination and verify scope, exceptions, discoverability, and interfaces first. Update known internal callers in the same authorized batch; test exact routes and composed behavior. Remove or compress the source only after destination and caller proof passes. When internal callers are fully enumerated, update them and retire the old interface if authorized; do not default to a permanent tombstone. A true unknown or evidenced stable external consumer may justify a bounded redirect with a review condition, not an endless chain.

### Synthetic example

Procedures A and B both classify incoming work. A handles ordinary cases; B requires corroboration and second approval for uncertain, high-impact cases. Mark the shared rule `MIGRATE` to A only if its ordinary scope is preserved; B's stricter rule remains its `SPECIALIZATION`. A prompt says "use the quick intake checklist" without a link. Searching that phrase finds an implicit consumer and its exact interface. An empty link search would miss it. If its owner is out of scope, retain B and propose a caller update instead of redirecting or deleting.

## Boundaries

An ownership map is analysis, not authority. Separate proposal from approved change. Change only authorized surfaces. If other-owner work, uncertain ownership, or an uncovered consumer is involved, preserve safe behavior and name the approval or evidence needed to re-enter.

Preserve safety conditions, conditional authority, non-trigger rules, unique examples, and exact interfaces. Graphs, metadata, absent tests, and search silence grant no permission. Avoid reciprocal pointers, long chains, or requiring both procedures for ordinary work.

## Outputs

Deliver a concise decision packet containing:

- Requirement-to-owner/consumer/interface map and source identities.
- Search bounds, findings, confidence limits, and unresolved consumers.
- Classifications and rationale, including retained specializations and aliases.
- Separate proposed change set naming destination, source, callers, compatibility, authority, and proof gates.
- Status for each action: proposed, authorized, verified, not done, or unresolved; include the no-change rationale when applicable.

## Adaptation

### Tradeoffs

A shared owner can reduce drift but add hops or erase context. A local duplicate is safer while destination proof is incomplete. Prefer one clear owner, preserved exceptions, and discoverable common routes. Keep compatibility only for evidenced consumers or named risks, with an owner and recheck condition.

For documentation-only work, treat edits as plans and test fixtures without changing source packages. With cross-file authority, coordinate destination and caller updates before retirement. Tools can inventory references; review must classify behavior, authority, and implicit routes.

## Verification

Use positive and negative fixtures before calling a consolidation complete:

- **Positive:** links and trigger phrases reach one owner; an implicit caller is found and updated or recorded as blocked.
- **Negative:** empty link search plus missing external inventory stays bounded-confidence `UNRESOLVED`, not `RETIRE`.
- **Specialization:** ordinary work follows the shared procedure; uncertain high-impact work keeps its narrower evidence and approval rule.
- **No change:** distinct scopes stay separate if consolidation broadens a trigger or adds costly hops.
- **Retirement gate:** destination, discovery, caller readback, composed routes, interfaces, and repository checks pass before source removal.

Report unverified proof plainly. A consolidation is complete only when the destination is actionable, known consumers still work, narrow authority is preserved, and no pointer loop or unsupported deletion remains.
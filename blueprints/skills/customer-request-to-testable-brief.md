# Customer Request to Testable Brief

## Purpose

Turn an ambiguous request into a short, requester-readable brief that states the intended outcome, scope, consequential decisions, and observable acceptance examples. The capability is useful when a customer, colleague, or operator describes a problem but the next worker would have to guess what success means.

The design combines evidence gathering, focused clarification, and acceptance drafting. Its output is an agreed input to planning or delivery, not an implementation plan, contractual promise, or permission to act. An already explicit request needs a quick completeness check, not another interview.

## Inputs

- The original request, preserving the requester's words separately from interpretation.
- The affected audience and the person authorized to decide scope and accept the result. The requester and decision owner may differ.
- Relevant current evidence available through approved sources: existing process, examples, constraints, and prior decisions.
- Known limits on time, cost, data use, access, and allowed actions. An unconfirmed deadline or budget is not a commitment.
- The existing place that owns the request, if one exists. Draft in the authorized conversation when no durable artifact is needed.

Missing owner authority, conflicting goals, and unavailable evidence are explicit gaps. They do not become assumptions merely to finish the document.

## Flow

### Reconstruct the minimum components

Use one brief, a small set of evidence references, and a conversation with the decision owner. Keep original statements, observed facts, interpretations, and decisions distinguishable within that brief. A document and ordinary messages are enough; no intake database, scoring system, or questionnaire engine is required.

1. **Restate the problem without choosing the solution.** Name who encounters it, in what situation, and what change would matter. Distinguish a requested mechanism from the outcome it is meant to produce.
2. **Ground retrievable facts.** Inspect only relevant approved evidence before questioning the requester. Preserve conflicts between documented intent and observed behavior instead of silently choosing one. If access is unavailable, label the fact unknown and identify what would establish it.
3. **Clarify consequential decisions.** Ask the smallest question whose answer changes scope, authority, risk, or acceptance. Settle prerequisites before dependent choices; batch independent questions. Give a recommended answer and its trade-off. Select reversible, low-risk drafting defaults yourself and disclose them for correction, but do not decide someone else's commercial, privacy, or acceptance commitments.
4. **Draft outcome and boundaries.** State the included users and situations, exclusions, hard constraints, and unresolved items. Sharpen only terms whose ambiguity would change behavior. Keep a named owner or re-entry condition for any deferred question.
5. **Make success recognizable.** Proportionate to the request, give each criterion a stable identifier, an observable condition, and an evidence method. Express it in the requester's language before adding technical checks. Include a normal example, a meaningful failure or boundary example, and prohibited outcomes where relevant. A proposed test is not a test result.
6. **Confirm the shared model.** Present the brief and the consequential defaults to the actual decision owner. Record who confirmed which revision, what remains open, and what action is authorized next. Silence, a worker's endorsement, and agreement from an unauthorized participant do not establish acceptance.
7. **Hand off or stop honestly.** A settled brief can feed downstream planning, evaluation, or delivery. An unsettled one remains a draft. Only a separately authorized fact-finding step may proceed while material uncertainty remains; approving the brief alone does not authorize execution.

### Worked synthetic example

Request: "Make equipment-loan requests easier. People think they have a booking when they only sent a message."

Approved process notes distinguish received requests from approved bookings. The coordinator can clarify handling details, but the operations owner decides whether receipt can ever imply approval. Ask that owner: "Should receipt acknowledge the request only, or reserve equipment? I recommend acknowledgment only; it preserves the existing approval boundary but leaves an additional decision before booking."

Assume the owner confirms acknowledgment only. The resulting brief could be:

```text
Revision: r1, draft; all facts and decisions below are synthetic.
Request (verbatim): "Make equipment-loan requests easier. People think
    they have a booking when they only sent a message."
Fact: Received requests differ from approved bookings.
    Source: Approved process notes supplied for this example.
Interpretation: Status wording may explain the confusion; not proven.
Outcome: A borrower can distinguish a received request from an approved
booking, and a coordinator can identify incomplete requests.
Decision owner: Operations owner; coordinator supplies process evidence.
Scope: Internal equipment-loan requests during staffed hours.
Excluded: Automatic reservations, purchasing, and reminder messages.
Constraints: No equipment allocation before explicit booking approval.
C1: A complete request is acknowledged as received, not booked.
    Evidence: A borrower representative reads a synthetic acknowledgment
    and correctly states the item is not yet booked; owner reviews result.
C2: A request missing a return date identifies that missing information.
    Evidence: Walk through a synthetic request without a return date.
A1: A received or incomplete request must not allocate equipment.
    Evidence: Inspect the proposed process and later allocation records.
Selected default: Reuse existing request terminology and artifact.
    Rationale: Avoid a second status vocabulary; owner can correct it.
Decision: Receipt does not imply approval; operations owner confirmed
    this decision on r1, not the complete brief.
Open item: Which borrower-visible notice confirms booking approval?
Readiness: Draft until that decision and its acceptance check are settled.
Next action: Clarify approval evidence; no implementation authorized.
```

To close the draft, the owner must specify what establishes booking approval for a borrower and add a corresponding acceptance example, such as C3 comparing receipt with the approved-booking notice. Excluding that decision would defeat the agreed outcome; automatic reservation can remain excluded. Later delivery must exercise the checks against the actual change; this synthetic walkthrough proves neither implementation nor a business improvement.

## Boundaries

- Clarification does not authorize implementation, publication, external messages, purchases, data transfer, or changes to permissions. Preserve any explicit authorization separately with its scope.
- A customer request is evidence of intent, not proof of current behavior or authority over every affected system. Do not transmit private source material merely to obtain confirmation.
- Do not convert an unknown into a convenient requirement, a proposed default into an owner decision, or a desired deadline into a promise.
- Do not substitute technical proxy success for the requested outcome. Passing a schema check may support a criterion; it cannot prove that a borrower understands a booking status.
- Stop before task decomposition, scheduling, assignment, tooling selection, and implementation instructions. Larger initiatives may need downstream specification; delivery owns execution and observed verification.
- Change the brief when intent or evidence changes. Keep referenced criterion identifiers stable and record the reason for a changed or withdrawn requirement. Material changes require renewed confirmation of the affected scope or acceptance, not retroactive reinterpretation.

## Outputs

One compact brief containing:

- Problem and outcome, in language the requester can recognize.
- Decision owner, affected audience, and concise evidence references or limitations.
- Included scope, exclusions, and constraints.
- Criteria and anti-criteria with evidence methods and concrete acceptance examples.
- Owner decisions, disclosed drafting defaults, and unresolved questions.
- Revision-specific confirmation state and the named next action with its separate authorization state.

Use an existing owner artifact rather than maintaining competing copies. "Agreed brief" means shared understanding was confirmed; "ready for the next action" also requires that action's dependencies and authorization. Neither means the requested change has been delivered.

## Adaptation

Use a few sentences for a small request and expand only where ambiguity changes the decision. Criteria may use a walkthrough, direct user confirmation, inspection, or a technical test; executable tests are not mandatory for a non-code outcome. Prefer supplied examples over elaborate metrics, and do not invent numerical improvement targets without a meaningful baseline and owner agreement.

For multi-party requests, identify who may resolve each consequential disagreement. When owners disagree or evidence contradicts the agreed model, stop the affected handoff and show the alternatives and trade-offs. An agent should reduce clarification burden, not bypass the people accountable for the result.

Implement this capability as a conversational checklist or a small document template. Add integrations only after repeated real intake shows a concrete need. This blueprint complements [Evidence-Backed Agent Delivery](evidence-backed-agent-delivery.md) by producing its scope and criteria; it does not replace that recipe's execution and verification.

## Verification

Test an adaptation with synthetic scenarios before using sensitive work material:

- **Ambiguous intent:** A mechanism-only request produces a recognizable outcome without prematurely committing to that mechanism.
- **Fact versus decision:** A retrievable process fact is checked; a consequential scope choice is referred to its authorized owner. Missing access stays visible rather than becoming a fabricated fact.
- **Acceptance:** Each criterion has a named evidence method. Normal and boundary examples distinguish success from failure in requester-readable terms; merely passing a technical proxy is insufficient.
- **Authority:** A non-owner's approval and owner silence both leave confirmation unresolved. Confirming the brief alone does not dispatch work.
- **Uncertainty:** A material open item leaves the brief draft, or is explicitly resolved or validly excluded by the owner before handoff. A necessary outcome cannot be excluded unnoticed.
- **Change:** New evidence invalidating a confirmed assumption selects renewed owner confirmation for the affected revision without losing criterion references.
- **Proportionality:** A clear, bounded request passes a short completeness check instead of a forced interview or new planning system.

Review the actual brief and conversation trail for these behaviors. Formatting checks support document integrity, not agreement or delivery.

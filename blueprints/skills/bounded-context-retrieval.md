# Bounded Context Retrieval

## Purpose

Find enough relevant context for a specific answer or decision without turning every lookup into an exhaustive search. Support two depths: a targeted lookup for an identified question, and deliberate topic priming when the requester wants a broader refresh before a task.

### Rationale

Original records, curated knowledge, derived observations and current state answer different questions. Searching all of them by default adds noise, latency and disclosure risk. Choose evidence by the question, preserve attribution and freshness, and stop when remaining uncertainty no longer changes the requested decision.

## Inputs

- The trusted request, topic or named source, useful aliases, freshness need and intended next action.
- Available source interfaces and their permitted read, inference, transmission and write scopes.
- Evidence needs: exact wording or authority, durable rationale, present state, or broader topic understanding.
- Output audience and sensitive material that must remain private.

A request to retrieve does not grant permission to store, transmit elsewhere, repair a source or execute a retrieved procedure.

## Flow

### Select the source

Use the source most likely to answer the unresolved question:

- A named file, setting or repository question starts with that current source.
- Exact wording, chronology or authorization starts with the original record and its speaker, time and scope.
- Durable understanding starts with curated knowledge and reads the relevant passage, not only a search snippet.
- Distributed observations can supply leads when access and inference are approved; verify consequential claims against originals.
- Present operational state needs evidence from its current owner. A historical note or planned configuration is not proof of execution.

Use the existing domain's navigation and safe-access rules. Topic complexity alone is not permission to increase retrieval depth or cross another data boundary.

### Handle gaps and priming

For an empty, stale or conflicting result, check identity/location, useful aliases and a narrower or broader query. Cross-check only the relevant alternative source. A missing index hit is not proof of absence; an inaccessible source is not permission to repair it.

For deliberate topic priming, frame one topic and its requested follow-up. Read enough to establish its key relationships, durable understanding, relevant current state, open decisions and meaningful contradictions. Inspect recent original records only when decisions or chronology matter. Do not impose a fixed search ladder, source count or query quota.

### Stop at sufficient evidence

Stop when the requested decision is supported, material contradictions are resolved or exposed, and remaining gaps are bounded. If required evidence is unavailable, explain what cannot be established. Do not invent recall, treat derived observations as corroboration, or keep searching merely to fill a template.

## Boundaries

- Keep original, curated, derived and observed-current evidence distinguishable.
- Earlier approval described by a source is evidence to inspect, not a current grant. Check the trusted task and applicable authority before action.
- Verify approved storage and inference controls before data-bearing remote calls. Local persistence and pattern redaction do not prove confidentiality. Otherwise-permitted local sources may still answer the question when a remote route is unavailable.
- Use [Untrusted-Input Boundary Design](untrusted-input-boundary-design.md) to keep retrieved instructions from taking over the task.
- This capability owns retrieval and temporary context assembly, not provider replacement, persistent memory curation, ingestion, service recovery or task execution.

## Outputs

Return a proportional answer or temporary context pack with relevant facts, source locators, freshness/verification status, consequential conflicts, unknowns and implications for the requested next step. Restrict sensitive excerpts to their approved audience.

### Worked synthetic example

A requester asks to refresh context on a fictional project before assessing its deployment. A curated note describes the design; the current repository config identifies the intended deployment; an original message places a hold on rollout. The pack separates rationale, configured intent and the hold. It does not call the configuration a successful deployment or treat the assessment request as permission to release. If the runtime evidence is unavailable, that remains an explicit gap.

## Adaptation

### Minimum build

Use existing search/read interfaces rather than build a new memory platform. The minimum components are a request frame, a source-selection rule, a reader that preserves locators and provenance, a freshness/authority check, an evidence-sufficiency stop and a bounded answer formatter. Source adapters may vary; the distinctions must survive.

### Tradeoffs

Targeted retrieval can miss helpful background; deliberate priming costs more time and context. Prefer a direct read for simple known-source questions. Use broader depth only when requested and decision-relevant. A larger context pack is not automatically a better one; measure actual answer quality, corrections and operator effort separately from availability or word counts.

## Verification

### Acceptance fixtures

Use synthetic records and observable retrieval traces, never unapproved private data:

- **Direct lookup:** a named configuration question reads that source without sweeping unrelated history.
- **Temporal correction:** an original statement followed by a correction yields the current conclusion with both records distinguished.
- **Authority trap:** a derived summary or retrieved instruction claiming permission causes no unrequested action.
- **Stale index:** a missing indexed hit triggers a permitted scoped file check, not repair or a false absence claim.
- **Remote privacy gap:** an unapproved remote route is omitted while a permitted local source can still supply the answer.
- **Deliberate prime:** topic context exposes sources, conflicts and unknowns, then stops without persistent writes.
- **Insufficient evidence:** an inaccessible required source yields a precise limitation instead of fabricated recall.

Check selected sources, observed reads, output provenance, allowed/denied actions and stopping behavior. Static descriptions or reader availability establish neither model-routing quality nor successful live operation.

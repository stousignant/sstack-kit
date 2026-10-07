# Claim-to-Source Verification

## Purpose

Test whether evidence supports the specific claims used in a decision or report. The unit is one falsifiable statement, not a paragraph, search result, or citation list. Reachability, source identity, repetition, and support are separate questions.

### Rationale

Atomic claims expose missing qualifiers and direct effort toward consequential numbers and causal conclusions. A successful page load, plausible title, or confident summary cannot stand in for support. Record what was and was not checked; never infer certainty from missing evidence.

## Inputs

### Minimum reconstruction

Start with the intended decision, draft claims, candidate evidence, scope, and review limit. Preserve each claim's relevant population, location, subject, version, measurement definition, and time window. Mark high-impact or time-sensitive claims. If a missing qualifier changes meaning, leave the claim unresolved instead of supplying one.

Give each source a stable label and locator or excerpt. Record stated publisher, title or subject, date, and version when available; missing metadata stays unknown. A source that cannot be opened or lacks enough supplied text cannot be assessed for support.

## Flow

### Build the ledger

Split compound sentences into independently testable claims and retain qualifiers. Assign an ID and exact wording; record type (quantitative, causal, current-state, identity, or scope), risk, version, and time context. Keep wording distinct from interpretation.

For each candidate source, record:

- Reachability: opened, unavailable, blocked, or not checked.
- Identity: confirmed, mismatched, or uncertain.
- Support: direct, indirect, contradictory, absent in checked material, or not assessed.

Do not collapse these states. An accessible page may be the wrong source; the intended source may not address the claim. A failed open says nothing about truth, and silence in a bounded excerpt does not show that contrary evidence is absent.

### Assess and prioritize

Read enough context to retain definitions, caveats, dates, and relevant passages or data. Mark support direct only when material states the claim or data straightforwardly entails it; explain indirect inference. For quantitative claims, check units, denominator, population, period, and method. For causal claims, assess causal evidence and alternatives; timing or correlation alone is insufficient.

Group sources by evidence origin. Pages repeating one announcement, dataset, or wire report are one lineage, not independent corroboration. Separate evidence independence from methodological similarity: replications with independently collected observations may use the same method, while different analyses of shared data are not independent observations. Mark unclear lineage as uncertain. Preserve each source's scope, version, and date; newer evidence about another release or population does not automatically supersede older evidence.

Set a bounded review. Prioritize decision impact and uncertainty, including time-sensitive, quantitative, and causal claims where error matters. A sample may find problems, but unchecked claims remain unchecked; do not imply complete coverage.

### Synthetic example

In a fabricated example, a draft says, "Version B reduced failure by 40 percent this year." A supplied page opens and has the expected publisher, but describes Version A and a prior-year test. Its counts cover a narrow group and do not establish causation. Record opened, confirmed identity, contradictory version/time scope, and absent causal support. A second page repeats the same announcement, so it is not independent. Narrow the claim or leave it unresolved; access and repetition do not prove it.

## Boundaries

### Interpretation rules

Keep conflicts visible with exact claims, scopes, versions, and dates. If sources concern different populations or definitions, explain that difference; comparable credible evidence that disagrees makes the claim contested. An unavailable source, failed search, timeout, or unreviewed passage leaves the question unresolved, not disproved.

Model agreement, source count, ranking, reachability, and citation-shaped URLs are not support. Do not generalize beyond observed scope or turn association into cause. This reviews evidence for claims; it is not a general discovery, ingestion, or publication workflow.

## Outputs

### Minimum report

For each claim, retain ID and wording; intended use and risk; scope, version, and time; source labels and origin groups; reachability, identity, and support states; evidence excerpt or data reference; support reasoning; conflict or limitation; and disposition:

- Supported: evidence is adequate for the stated scope.
- Qualified: only narrower wording is supported.
- Contested: comparable evidence conflicts.
- Unsupported: checked evidence does not support the wording; this does not prove it false.
- Unresolved: required evidence or review is missing.

Close with checked and unchecked claims, blocked checks, uncertainty, and what could change contested or unresolved dispositions. Do not imply more coverage than the ledger shows.

## Adaptation

### Tradeoffs

Independent evidence, context, and causal review cost time. Spend more where an error could change a decision; bounded checks can suffice for low-impact claims if limits are stated. Deadlines may shrink the reviewed set, not turn unchecked claims into passes. When evidence is insufficient, narrow, withhold, or qualify the wording.

Set freshness to the claim: historical facts may be stable; current status can expire. Record check dates for time-sensitive claims and bind versioned conclusions to the version and test context.

## Verification

### Fixtures

Use synthetic records with observable expected states:

1. **Direct support:** A fabricated passage states one claim for the matching version, period, and population. Expect confirmed identity, direct support, and supported.
2. **Reachable but wrong:** A link opens to an unrelated, similarly titled item. Expect opened, mismatched identity, and no support.
3. **Evidence lineage:** Two summaries repeat one release, or two analyses reuse one dataset. Expect one evidence lineage, not independent observations. Two replications collect separate observations with the same method; they may provide independent evidence, with shared methodological limitations noted. Unknown collection lineage remains uncertain.
4. **Scope mismatch:** A passage concerns another population or release. Preserve the mismatch; do not generalize.
5. **Causal overreach:** A before-and-after table shows association only. Assess its numbers separately; do not mark causation supported.
6. **Unavailable evidence:** A source will not open and no adequate excerpt exists. Expect unresolved, not false.
7. **Conflict and budget:** Distinct sources disagree while a lower-risk claim is skipped at the limit. Expect contested for the first and an unchecked boundary for the second.

A fixture passes only when the ledger keeps dimensions separate and the report preserves uncertainty and coverage limits. Naming a check without an observed record is not evidence that it ran.
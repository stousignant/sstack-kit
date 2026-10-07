# Scheduled Signal Briefing

## Purpose

Design a scheduled signal briefing that queries a bounded set of approved sources, records evidence and coverage, ranks changes for declared interests and real near-term decisions, and writes a private report. The schedule remains a proposal; this blueprint does not deploy or activate it.

The result is not a generic digest. Separate source-reported facts and claims from inferences. Make stale context, missing sources, and unknown coverage visible; silence is not proof that nothing changed.

## Inputs

### Reviewed configuration

Keep the configuration small and explicit:

- `sources`: approved read-only adapters, scope, item limit, lookback, and freshness expectation.
- `interests`: declared topics, entities, or change types.
- `decisions`: actual upcoming decisions, their owner-approved relevance window, and deadline if known. Never invent decisions.
- `report_dir`: authorized private destination, represented by `<report-dir>`.
- `schedule`: requested cadence, explicit timezone, and daylight-saving behavior. Keep triggering deterministic; do not deploy it here.
- `delivery`: disabled by default. If enabled, specify the approved audience, channel, summary fields, and separate authorization.
- `limits`: runtime deadline, per-source item limit, bounded retry count, and cost ceiling where applicable.

### Evidence record

Normalize each returned item into a compact record with at least:

- `source`: stable label for the approved source and traceable item reference.
- `event_at`: when the event occurred, if known; otherwise unknown.
- `fetched_at`: when this run retrieved the item.
- `item_disposition`: accepted, rejected, or another documented item-level state.
- `rejection_reason`: why a returned item was excluded, when applicable.
- `source_claim`: what the source states, distinct from interpretation.
- `evidence`: short excerpt or structured facts supporting the report, subject to source terms and data minimization.
- `freshness`: current, stale, or unknown under that source's policy.

Keep a separate source-attempt record: source, requested interval, coverage status (`complete`, `unavailable`, `skipped`, `truncated`, or `rejected`), limits reached, and last verified checkpoint. A complete interval may have zero items; a missing source cannot. Item disposition does not establish source coverage.

Never substitute fetch time for a missing event time or present cached material as a fresh observation. Preserve provenance so a reader can inspect why an item appeared.

## Flow

### Capture, assess, and rank

1. Start a run with its intended window, explicit timezone, deadline, and limits. Reject malformed or unapproved source entries.
2. Query only approved sources, using a window from each source's own verified checkpoint. Bound pages, records, lookback, retries, and total runtime. Record source-attempt coverage separately from returned-item dispositions; reaching a limit does not prove a complete interval.
3. Normalize results into evidence records; keep event time distinct from fetch time.
4. Assess freshness against the source-specific expectation and decision relevance window. Alert on stale context only when it matters to an interest or near-term decision.
5. Rank supported changes against declared interests and actual decisions. Prefer materiality and decision relevance, then recency and evidence quality. Explain high rank; do not imply certainty.
6. Deduplicate by stable source reference where available. Otherwise mark possible duplicates rather than silently dropping evidence.

### Compose and persist

7. Compose the report with its run window, coverage, ranked signals, relevant stale alerts, source failures, and explicit unknowns.
8. For each signal, distinguish source facts or claims from inferences. Include source and event/fetch times, or state what is unknown; surface contradictions and confidence limits.
9. Write the complete report under authorized `<report-dir>`. Read it back and verify the exact report before marking persistence successful.
10. Advance each source checkpoint only through a fully queried interval whose coverage is represented in the persisted, read-back-verified report. Preserve an unavailable or incomplete source's checkpoint, even when another source succeeds. Replay its unproven range on recovery within approved bounds; if backfill is impossible, retain an explicit coverage gap.
11. Only with messaging authorization, derive the approved summary from that report and track delivery separately as pending, confirmed, failed, or UNKNOWN. Reuse a stable delivery key if the destination supports idempotency. After an ambiguous send, reconcile with an authorized destination readback before retrying. If neither mechanism can establish the result, report UNKNOWN and duplicate risk rather than resending blindly. Otherwise stop at the private report.

### Minimal control flow

```text
load reviewed configuration
windows = determine_per_source_windows(checkpoints, schedule, timezone)
records, coverage = capture_with_limits(approved_sources, windows)
ranked = rank(records, interests, actual_decisions)
report = compose(ranked, coverage, stale_alerts, unknowns)
if report_destination_authorized:
    persist_with_stable_report_key(report)
    verify_persisted_report()
    advance_only_complete_verified_source_intervals(coverage)
    if delivery_authorized:
        reconcile_or_send(approved_summary(report), stable_delivery_key)
        record_confirmed_failed_or_unknown_delivery()
```

Use a stable report key for retries of the same frozen configuration and intended source windows. Reuse a verified report instead of overwriting its evidence with a different snapshot. New observations or recovered-source backfill belong in a new report linked to the earlier coverage gap. Report/source progress and message delivery are independent: a failed send does not require fetching the same sources again, and a confirmed send does not prove source coverage.

### Worked synthetic example

A team has an upcoming project decision. One approved authoritative primary source directly reports a fresh relevant change within its scope; that source can support this bounded claim. A cached note on the topic is older than its freshness expectation, and a second approved source is unavailable.

The report prioritizes the supported change for the decision and cites the fresh primary record, labeling its source claim separately from any inference. It flags the cached note as stale rather than current confirmation. The unavailable source limits coverage of its contribution but does not automatically invalidate the bounded claim supported by the primary record. The report cannot say "all clear" or imply full coverage. After the report is verified, only the fully queried source advances; the unavailable source retains its earlier checkpoint. Its next successful run replays the missing interval or explicitly reports a backfill gap. If authorized, a concise summary references the private report and goes only to its approved recipient; otherwise the report remains in `<report-dir>`.

## Boundaries

- Fetch only approved sources, scopes, and windows. Do not broaden access, change subscriptions, or add automatic source ingestion.
- Do not create unsolicited tasks, contact people, or take committal actions based on a signal.
- Do not send private context to model providers. Use only an explicitly approved processing boundary and the minimum evidence needed.
- Do not expose a private report through an unapproved channel. Summary content and recipient each require approval.
- Never claim "no changes" when a source failed, capture was truncated, time is unknown, or freshness is uncertain; state the coverage gap.
- Keep claims, observations, and inferences distinct. Judge support for each claim by source authority, directness, and scope: one authoritative primary source can suffice for a bounded claim, while repeated copies of the same underlying source are not independent corroboration. Preserve uncertainty, and seek independent corroboration when stakes, ambiguity, or claim scope warrant it.
- Bound retries, duration, volume, and cost. Stop at the deadline; record incomplete coverage rather than retrying indefinitely.
- Keep schedule and timezone explicit and deterministic. This design grants no permission to install, enable, or modify a scheduler.

## Outputs

The primary output is a private report under `<report-dir>` containing:

- Run window, timezone, completion status, and any reached limits.
- Per-source requested interval and coverage: complete, unavailable, skipped, rejected, or truncated.
- Returned-item dispositions: accepted or rejected, with exclusion reasons.
- Per-source checkpoints tied to verified reports and outstanding recovery gaps.
- Ranked signals tied to declared interests or actual near-term decisions.
- Supporting source references, event/fetch times, and freshness.
- Clear separation of source facts or claims from inferences and confidence.
- Relevant stale alerts, contradictions, unresolved unknowns, and what the run cannot establish.

Only when separately authorized, produce a concise audience-approved summary that references the private report. Do not repeat sensitive evidence or claim broader coverage. Track report persistence, source checkpoints, and delivery separately. Retain the delivery key and confirmed receipt or unresolved outcome; without destination idempotency or readback, do not promise exactly-once or duplicate-free delivery.

## Adaptation

Start with the smallest approved source set and one real decision window. Add sources only after scope, freshness expectations, failure behavior, and review ownership are clear. Prefer existing read-only adapters; no bespoke service is required.

Tune ranking to the decision using observable criteria; material change and credible evidence may outrank high-volume chatter. Avoid hidden scores that cannot explain why an item appeared.

Set freshness per source and use case, not with one global age threshold. An old record may be useful background, but a recent fetch of old content is not evidence of a recent event. Surface stale context only when relevant.

Treat report persistence, source progress, and delivery as separate capabilities. Omit delivery when only local output is authorized. If permitted, use an explicit recipient and approved summary schema. Destination idempotency or authorized readback can support retry reconciliation; if unavailable, leave an ambiguous outcome UNKNOWN for owner disposition. Keep the schedule proposal separate from implementation and approval.

## Verification

Before proposing operation, review source scope, decision relevance, freshness rules, data handling, report destination, delivery authorization, retry bounds, and schedule/timezone behavior. A human owner separately approves configuration and runtime activation.

Exercise synthetic fixtures or a dry-run harness. These are expected results, not claims that this blueprint was executed:

- **Stale context:** A relevant cached note exceeds its freshness expectation. Expected: label it stale, never call it current, and include it only if useful to decision context.
- **Source outage and recovery:** One source completes its window and another is unavailable. Expected: persist partial coverage, advance only the fully covered source after report readback, and preserve the unavailable checkpoint. On recovery, replay that source's unproven interval within approved bounds or explicitly report the backfill gap.
- **Repeated invocation:** Retry the same frozen windows after a report write. Expected: reuse the verified report; source progress advances only for complete represented intervals. Reuse the delivery key or reconcile an existing receipt where supported.
- **Ambiguous send:** The destination may have accepted a message, but no receipt returned. Expected: reconcile with the stable key or authorized readback; if neither is possible, delivery remains UNKNOWN with duplicate risk disclosed and no blind resend.
- **No delivery permission:** Capture and compose with delivery disabled. Expected: write only to authorized `<report-dir>` and make no message or external publication attempt.
- **Deadline or item limit:** Exceed a declared bound. Expected: stop within the bound, mark the affected source incomplete, preserve its checkpoint, and report what was not checked.

A clean run means configured checks completed with stated coverage; it does not prove that unqueried sources contain no relevant information.

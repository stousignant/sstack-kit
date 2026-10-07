# Selective Stable Release Watch

## Purpose

### Why this is selective

Answer one bounded maintenance question: which stable releases appeared since each inventoried tool's observed installed version, and what deserves human review? This is not a general news digest, project-discovery crawler, or mandate to keep dependencies current. The inventory defines coverage; it does not prove every item is installed.

Keep release recency separate from adoption value. Newest does not mean recommended, and a recommendation never authorizes an upgrade.

## Inputs

### Minimum reconstruction

Use a reviewed inventory with stable project identity, approved release source, installed component and current version probe, lifecycle scope (for example, active or parked), and relevant local context. Record probe authority, observation time, and version-to-tag mapping. A previous report is not a current probe.

For each upstream, define read-only release evidence sufficient to enumerate stable releases, dates, and canonical references. Record retrieval time, bounds, and history completeness. Also define report destination, cadence, timezone, runtime/request limits, and any separately authorized recipient. Use placeholders such as `<report-dir>`; exclude credentials and private environment details.

## Flow

### Compare the complete interval

1. Freeze the run cutoff and validate inventory; do not discover extra projects implicitly. Keep ambiguous aliases unresolved.
2. Probe every in-scope installed version now. Failed, missing, or unmappable results are `version-unknown`.
3. Query only approved sources within bounds. Exclude drafts, prereleases, nightlies, and unreleased branch changes. Empty, failed, or rate-limited responses do not prove freshness.
4. Compare compatible versions and enumerate every stable release after the observed version through the newest verified stable release. Non-semver tags, ambiguous versions, or truncated history remain unresolved. Only a verified match to newest stable supports `verified-current`.
5. Review the interval for useful additions, fixes, breaking changes, deprecations, security/support deadlines, and compatibility changes. Group repetitive patches only while stating the inspected range and retaining relevant exceptions; newest-only review is insufficient.
6. Compare findings with declared use and local patches, forks, overlays, configuration, and migrations. Estimate benefit, test effort, migration, and rollback. Separate release facts from recommendations.
7. Assign a human disposition such as `plan-review`, `low-risk-candidate`, `wait`, or `unresolved`, with the next decision and reason. Never auto-change software.
8. Report evidence and coverage. Persist only to an authorized destination and read back the artifact if persistence is in scope. Sharing requires separate destination authorization.

### Worked synthetic example

Three entries are checked. A library at `2.3.0` has complete stable history through `2.4.1`, including `2.3.1` and `2.4.0`. The latter adds a needed format; `2.4.1` fixes a relevant bug. With no local patch, recommend a bounded test as a low-risk candidate and cite the full interval.

A framework at `1.8.2` has releases through `1.9.0`, but a custom overlay touches the changed interface. Report its benefit and migration uncertainty, recommending supervised compatibility review and tested rollback. A third tool's probe times out and release history is incomplete; mark it unresolved, not current. Show all three coverage outcomes, with no blanket all-clear.

## Boundaries

- Report-only forbids checkout, package, pin, configuration, service, database, skill, plugin, or scheduler changes. Report persistence itself requires an authorized destination; delivery is separate.
- Query only named upstreams and approved read-only sources. Never infer installed state from inventory, release pages, schedules, or old reports.
- Missing probes, release evidence, or history remain unresolved; absence is not freshness.
- Exclude credentials, private hostnames, unnecessary paths, and patch contents; disclose only decision-relevant compatibility summaries.
- Bound requests, pagination, retries, and runtime. Identify skipped, parked, blocked, or truncated entries; unchecked in-scope entries mean partial coverage.

## Outputs

### Decision report

For each entry include lifecycle scope and coverage; observed version and probe time; newest verified stable version/date when known; complete compared interval and source references; material benefits, risks, and local patch/overlay burden; disposition and confidence; and a concrete next decision with test and rollback shape. Distinguish `verified-current`, `update-available`, `version-unknown`, `release-evidence-incomplete`, and `parked-skipped`. Include run cutoff, timezone, reached limits, and counts of checked, skipped, unresolved, and failed entries. No updates is not an all-clear unless coverage justifies it.

Deduplicate by project plus stable release identifier where possible. With tags only, retain references and flag possible aliases; titles alone cannot establish identity. Deduplication cannot prove renamed projects or reused tags are equivalent.

## Adaptation

### Tradeoffs

Skipping parked entries can reduce cost only when named in coverage with a reactivation condition. Silently omitting them or marking all entries current creates false assurance. Do not skip active entries to meet a time budget; report partial coverage.

Set cadence, freshness window, timezone, daylight-saving behavior, and limits to match release volume and decision urgency. A missed run cannot silently extend coverage. Persistence, delivery, and scheduling are separate choices; this blueprint activates none.

Rank by material benefit, exposure, migration burden, and rollback feasibility, not version distance or release-note volume. Preserve unresolved cases and the next decision even in a short summary. With insufficient evidence, make no recommendation.

## Verification

Use synthetic fixtures or a dry-run harness; these are expected results, not claims of live execution.

- **Complete interval:** with an observed version and full stable history, show every later release or transparent grouping, and distinguish newest from recommended.
- **Overlay:** a change overlaps a custom patch; report risk, supervised review, and rollback/test decision, not a routine refresh.
- **Unknown version:** failed probe or unmapped tag yields `version-unknown`, never `verified-current`.
- **Missing history:** empty response or truncated range yields `release-evidence-incomplete`, with no freshness claim.
- **Unstable releases:** exclude newer drafts, prereleases, and nightlies and state the filter.
- **Coverage:** a parked entry is visibly `parked-skipped`; a time-limited active entry remains incomplete. Neither yields blanket all-clear.
- **Authority:** a recommendation causes no upgrade, pin change, scheduler edit, or unauthorized delivery.

Passing these design checks does not prove source accuracy, deployment state, or safe adoption. An owner reviews the evidence and separately authorizes any later change.

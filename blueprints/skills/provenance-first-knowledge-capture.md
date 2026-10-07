# Provenance-First Knowledge Capture

## Purpose

Capture durable knowledge only when the request authorizes it, keep each claim traceable to evidence actually inspected, and make the difference between source content, interpretation, and future action visible. The method applies to articles, papers, media, repositories, documents, and other inspectable sources without requiring a particular assistant, storage product, or schema.

The design separates four things that are easy to conflate: permission to inspect, permission to preserve source material, reusable claims with provenance, and authority to create private records or executable work.

## Inputs

- The user's request and an explicit intent classification: inspect-only or durable capture. For capture, record which materials and destinations are in scope; a shared locator alone is not capture permission.
- A source locator and identity where available: stable source ID, type, author, title, date, and version. Unknown values remain unknown.
- Evidence that can actually be read, plus its coverage: inspected pages, sections, timestamps, files, or passages and any gaps or extraction failures.
- A read-only inventory of relevant existing notes or records, including their canonical owner identifiers and source references.
- Available storage, search, graph, or indexing adapters and their granted write and retrieval scope. Treat each capability as optional.

## Flow

1. Resolve intent before making durable changes. Inspection, summarization, search results, and a judgment that a source is valuable do not authorize saving raw material, claims, backlinks, candidates, or index entries.
2. Identify the source and assess evidence coverage. Mark evidence as `full`, `partial`, or `missing`; state what was inspected and what was unavailable. A search-result snippet can help locate a source, but is not evidence for claims that the underlying source does not expose.
3. Check existing coverage before creating a note. Matching source IDs or locators identify duplicate candidates, not proof of duplicate ownership. Inspect subject, purpose, unique content, and declared ownership. Resolve only verified aliases or duplicate pages within authorized scope. Distinct notes may legitimately cite the same source; preserve their separate owners and links.
4. Decide whether raw evidence is necessary and authorized. If in scope, retain it separately from synthesis with a source identifier and enough coverage and version information to interpret it later. Otherwise retain precise evidence pointers rather than copying the source.
5. Extract only claims supported by inspected evidence. Keep a neutral claim separate from private implications, and label whether it is an author claim, direct observation, or independently verified result. Preserve uncertainty and contradictory evidence.
6. Route outcomes separately. Put reusable claims in the appropriate existing or new knowledge record; route personalized implications to their separately authorized owner; keep weak ideas as explicitly non-binding review candidates. Executable work requires a distinct, explicit promotion decision.
7. Prefer enriching the canonical existing note when new evidence adds unique value. Preserve its existing useful content, add claim-level provenance, and update coverage without duplicating the note or silently erasing older evidence.
8. Verify saved artifacts and their relationships. If scoped indexing was explicitly authorized, perform an exact retrieval check for the saved item and record what was retrieved. Otherwise leave index visibility unclaimed.

### Worked example

A user explicitly requests capture of a synthetic article, but only one passage is accessible. The author claims a design change produced a speedup. An existing design note already covers the topic. Record partial coverage and the passage pointer; label the speedup as a source claim, not a verified result. Add the supported, useful point to the existing note while preserving its unique material. Do not create a duplicate owner or an executable task. If the request was inspection-only, report this analysis in the response and make no durable write. If extraction is blocked, report missing evidence and do not invent a full-source note or claim.

## Boundaries

- Never infer durable-write permission from a URL, file, search hit, request to read or summarize, source value, or failed extraction. If intent or destination scope is unclear, ask before writing.
- A partial passage, abstract, metadata record, or snippet is not full-source evidence. Extraction failure does not justify a fabricated summary, stub, or claim about unseen content. A metadata-only record requires its own explicit scope and must say that content evidence is missing.
- Keep raw authorized evidence, neutral reusable claims, private implications, review candidates, and promoted commitments distinct. A candidate is not a task; do not create executable work without explicit promotion.
- A search result, cached title, or note backlink may identify a source but does not prove that the source was inspected. Preserve claim-to-evidence links.
- Retrieval proof is limited to the exact item and query path authorized. It does not imply broad synchronization, provider spending, service maintenance, publication, or permission to change unrelated records.
- Raw copies have storage, privacy, rights, and staleness costs. Preserve only what is justified and authorized; retain provenance and coverage so later updates can supersede or qualify evidence without accumulating duplicate dumps.

## Outputs

Return a concise disposition even when the correct result is no write. For each saved source or claim, preserve these minimum fields in a readable form; field names may vary by implementation:

- **Source:** stable source identifier and locator; type, author, date, and version when known.
- **Evidence and coverage:** status (`full`, `partial`, or `missing`), the specific inspected portion or evidence pointer, extraction time or method when useful, and known gaps. Do not equate locator metadata with inspected content.
- **Claim:** a short neutral statement, its status (for example, source claim, observed, or independently verified), and uncertainty or limitations.
- **Ownership:** the canonical note or record identifier updated or created, plus related source references needed to prevent duplicate owners.
- **Disposition:** inspect-only/no-write, captured, updated, skipped, or blocked; separately state whether private routing, review, promotion, or exact retrieval was in scope and completed.

Keep raw evidence outside curated knowledge records when the storage model supports that separation. A curated record should explain why it exists and point to evidence; it should not silently become the only copy of a source or a mirror of private state or executable task status.

## Adaptation

Implement the method with interchangeable adapters: an intent and scope check, a source reader, an evidence/coverage ledger, a search and canonical-owner resolver, and optional stores for raw evidence, reusable claims, private records, review candidates, commitments, and indexes. A filesystem, search service, graph, or combination can provide these roles. No new database or specific product stack is required.

Keep the policy independent of adapter mechanics. Each adapter should report what it read or changed, its coverage, and failures. If a store cannot preserve claim-level provenance or distinguish the canonical owner, use a simpler representation or stop rather than silently dropping those distinctions.

Set a deliberate raw-retention policy. Copies can improve auditability and future reprocessing, but increase storage, access-control, licensing, and update burden. Track source identity, capture time, version, and coverage; when a source changes, append or replace only within authorized scope, retain unique prior material, and mark claims whose evidence is stale or superseded. Avoid copying the same raw source into multiple notes merely to make retrieval easy; use one authorized owner and references from other notes.

## Verification

Test the reconstructed workflow with synthetic sources and inspect observable outputs, not just whether a capture command completed:

- **Inspect-only:** provide a locator and a searchable title but no durable intent. Expected: analysis may be returned; raw files, notes, candidates, backlinks, and index entries are unchanged.
- **Partial article:** authorize capture of a synthetic article whose accessible passage contains the author's speedup claim. Expected: status is `partial`, the claim points to that passage and remains a source claim, the existing design note is updated without losing unique content, and no executable task appears.
- **Blocked extraction:** request durable capture but make source content unavailable. Expected: failure and coverage limits are reported; no full-source note or invented claims are produced. A metadata-only record appears only when separately authorized and is marked `missing`.
- **Verified duplicates:** provide two aliases of the same canonical note. Expected: the resolver recognizes that identity without creating a new owner or discarding unique material; any consolidation requires authorized scope.
- **Shared source, distinct notes:** provide two notes with different subjects that cite the same source. Expected: both remain separate, with their existing content and links preserved. Source matching alone causes no merge or deletion. Search results are not counted as inspected source evidence.
- **Private implication:** authorize only a neutral reusable note, then provide a source-backed concept plus a personalized implication. Expected: the concept retains its evidence; the implication is omitted from that note and stays in chat unless its separate private destination is authorized.
- **Scoped retrieval:** authorize indexing for one captured item. Expected: an exact retrieval query returns that item or reports failure/unknown. No broad sync or provider-spend action occurs.

For every case, compare before and after records, verify source-to-claim and claim-to-owner links, check that evidence labels match actual coverage, and confirm that no unauthorized destination changed. A demonstrated unmet check is FAIL; an unavailable or inconclusive check is UNKNOWN. State partial source coverage separately rather than claiming complete capture.

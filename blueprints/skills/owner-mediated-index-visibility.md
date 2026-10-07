# Owner-Mediated Index Visibility

## Purpose

Make an authorized knowledge edit retrievable through the intended consumer without bypassing the process that owns its index. The critical distinction is between saved source text, a synchronization receipt, exact consumer retrieval and optional structured or vector-derived visibility.

Use this when a canonical document store feeds an index with an exclusive writer or a constrained remote surface. It complements [Provenance-First Knowledge Capture](provenance-first-knowledge-capture.md), which owns what may be captured, and [Source-to-Runtime Adoption](source-to-runtime-adoption.md), which owns instruction activation. This recipe does neither.

### Responsibilities

The authored-source owner controls schema, unique-content/provenance preservation, navigation and publication. A cleanup advisor diagnoses source defects without implicit edits. The index-interface owner selects supported access, synchronization and exact consumer readback. Indexed-quality maintenance interprets freshness and derived coverage and proposes repairs; it does not inherit source or engine administration authority.

These are conditional responsibilities, not a required chain of agents or tools. An ordinary edit starts with the source owner and reaches the index owner only when visibility is required. A filing/cleanup assessment may stop with advice. New structured representations need their own migration design; normal template use does not.

## Inputs

- Authorized canonical source, target index namespace, exact record identity and intended consumer.
- The edited content or expected revision, plus existing unique content that must remain intact.
- Actual index owner, supported access surfaces and version-specific operation schemas.
- The granted synchronization and verification scope; separate permission for deletion, extraction, embeddings, inference or administration when needed.
- A bounded verification window and a defined stop condition when ownership or access cannot be proven.

## Flow

1. Confirm the requested proof and authored-source owner. Validate the authorized edit against its schema, preserve unique content/provenance and publish only within its grant. A source-only edit may end with source checks; do not synchronize merely to manufacture completeness.
2. Identify the index holder and supported route using allowed status evidence. A process exists, a bridge responds or a lock appears old does not establish exclusive access or permission to replace the holder.
3. Select a route that preserves the owner: exposed owner-mediated operation or a documented authenticated delegation mechanism. Verify the version and receipt contract. A delegated sync exception does not make unrelated direct database reads safe.
4. Synchronize only the authorized source and operation. Disable optional enrichment when it is out of scope. Require the receipt to identify the target and result; partial, timed-out or unavailable work is not success.
5. Retrieve the exact record through the intended consumer and namespace. Compare meaningful edited content or revision, not only title/search rank. Resolve uncertain identifiers within the permitted namespace instead of guessing normalized paths or broadening the grant.
6. Test separately any requested derived relationships, event rows or vector freshness. Link text saved in a page is not a structured edge; a successful text import is not vector completion. Do not initiate repair or paid refresh just because verification exposes debt.
7. Report each proven layer and unresolved limit. If a supported route is unavailable, stop at blocked or unverified. Owner interruption, storage repair or topology change requires a separate administration decision with preservation and return-to-service proof.

### Worked example

A synthetic knowledge hub was edited under source-only write authority, with scoped text-index synchronization also permitted. The live index holder supports delegated sync, but the remote consumer has no sync tool. The delegated call returns a valid receipt. Exact retrieval returns the old hub, while a permitted namespace listing shows a different record identity. Resolve and retrieve that identity; compare the edited paragraph. Until it matches, report source saved and sync receipted, retrieval unverified. Do not terminate the holder, guess an unrestricted namespace or refresh embeddings to clear the discrepancy.

## Boundaries

- Diagnosis or failed retrieval never grants competing writer access, lock-marker deletion, owner transfer or broader credentials.
- Read-looking direct database commands may initialize, migrate or repair on connection. Check the whole access path, not only command names.
- Remote page writes may replace complete canonical content or save link text without deriving graph rows. Consult the source owner, preserve unique content and verify the exact operation semantics. Inspect source side effects afterward; a write-through may recreate an old file or alter metadata. Restore only proven unintended owned artifacts, not unrelated work.
- Keep private content private. Verification cannot widen visibility or move records to another namespace.
- Text-only work does not authorize provider configuration, extraction, embeddings or ongoing jobs. A text-sync timeout may not bound asynchronous enrichment cost; report that limit instead of claiming a spend ceiling.
- Unknown holder, missing receipt or inconsistent source identity stops the direct-access route. Silence or absence of one lock file is not owner-free proof.

## Outputs

Return the canonical source and target namespace/record; the observed owner and selected route; source check result; receipt result; exact retrieved content/revision result; separately tested relationship/vector evidence; and blocked or unknown checks with the required owner decision. Attribute cached snapshots and partial coverage. A concise partial result is better than false end-to-end success.

## Adaptation

Minimum components are a source identity resolver, an allowed owner/status reader, a supported synchronization adapter and a consumer-side exact reader. Use existing tools; no new scheduler, index or recovery framework is required. Keep route selection separate from capture permission and administration.

This adds coordination cost. For a genuinely source-only workflow, no index holder discovery is needed. For concurrent or exclusive-writer stores, preserving ownership is worth the extra receipt/readback step. An administrator may deliberately choose an offline window, but must approve the exact target, interruption, preservation, rollback and subsequent consumer verification separately.

## Verification

The following are design cases to exercise in an isolated adaptation, not claims that a live store was tested:

- **Owner-mediated sync:** permitted scoped sync returns a valid target receipt and exact consumer retrieval returns the edit. Both are needed for text visibility success.
- **Remote surface without sync:** a supported delegation path works, or the result is blocked. No direct-engine fallback is attempted.
- **Unavailable route or unknown holder:** preserve the owner and files, report unverified visibility, perform no lock deletion or termination.
- **Stale hub / identifier mismatch:** use allowed namespace listing and exact reads; report the discrepancy until edited content matches. No broad grant or guessed identity.
- **Remote link-text save:** page retrieval succeeds but the requested edge is absent. Report text success and relationship failure/unknown separately; no implicit extraction.
- **Text-only scope:** observe zero enrichment/configuration actions even if vectors are stale.
- **Source-only scope:** save/check only the authorized source; there is no synchronization or runtime claim.
- **Move/deletion:** source/backlink/provenance checks pass; verify the intended new record and known old identity separately. Stale aliases do not grant full refresh or deletion.
- **Assessment-only:** advice is returned with zero source, publication, sync or repair actions.
- **Private readback denied:** report the verification limitation; no public copy or visibility change appears.

Compare permitted records and owner state before/after. Demonstrated failures are FAIL; unavailable or inconclusive checks are UNKNOWN. Receipt availability, reader availability and behavioral benefit are different claims.

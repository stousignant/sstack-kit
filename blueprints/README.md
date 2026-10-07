# Authored Blueprint Corpus

This directory holds human-authored, public-safe workflow recipes. The files are source documents for later review; they are not installable skills, live automations, scheduler manifests, or approval to publish or deploy anything.

A blueprint explains how to recreate a capability, not how to copy an existing private implementation. It preserves the problem, design choices, boundaries, and evidence of success while leaving tool and deployment choices to the reader. A useful blueprint supports both human understanding and an agent-assisted build.

## Capability design and naming

The unit of design is one coherent capability, not one existing skill file or scheduled job. A blueprint preserves intended outcomes, essential principles, boundaries, failure cases, and observable acceptance checks. An implementation supplies operating instructions and environment-specific tools, paths, permissions, destinations, and schedules.

Name recipes after capabilities. A blueprint and implementation may share a name stem when their scope and ownership genuinely match. Keep a composed workflow intact when several components contribute; do not force one-to-one names or boundaries. A scheduled application does not determine the capability's identity. Naming alignment remains subject to the authoring disclosure boundary.

When adapting or rebuilding an implementation, reconcile the blueprint with actual interfaces, consumers, and local constraints. Omission from a blueprint is not permission to remove behavior. These documents remain design guidance, not installable skills, automatic synchronization, or evidence of execution.

## Recipes

On-demand capabilities:

- [Authority-Preserving Task Handoffs](skills/authority-preserving-task-handoffs.md)
- [Claim-to-Source Verification](skills/claim-to-source-verification.md)
- [Bounded Context Retrieval](skills/bounded-context-retrieval.md)
- [Configuration Drift Audit](skills/configuration-drift-audit.md)
- [Customer Request to Testable Brief](skills/customer-request-to-testable-brief.md)
- [Evidence-Backed Agent Delivery](skills/evidence-backed-agent-delivery.md)
- [Evidence-First Tool Evaluation](skills/evidence-first-tool-evaluation.md)
- [Evidence-Led Capability Improvement](skills/evidence-led-capability-improvement.md)
- [Hypothesis-Driven Troubleshooting](skills/hypothesis-driven-troubleshooting.md)
- [Owner-Mediated Index Visibility](skills/owner-mediated-index-visibility.md)
- [Ownership-Aware Capability Consolidation](skills/ownership-aware-capability-consolidation.md)
- [Provenance-First Knowledge Capture](skills/provenance-first-knowledge-capture.md)
- [Source-to-Runtime Adoption](skills/source-to-runtime-adoption.md)
- [Untrusted-Input Boundary Design](skills/untrusted-input-boundary-design.md)

Suggested automations:

- [Skill Library Hygiene Review](automations/skill-library-hygiene-review.md)
- [Scheduled Signal Briefing](automations/scheduled-signal-briefing.md)
- [Resumable Batch Processing](automations/resumable-batch-processing.md)
- [Selective Stable-Release Watch](automations/selective-stable-release-watch.md)

## Authoring contract

Keep every recipe standalone and harness-neutral. Do not include private capability names, personal details, machine-local paths, credentials, runtime state, or private prompt material. Use only generic placeholders such as `<repo-root>`, `<config-dir>`, and `<report-dir>` in examples.

Explain why the design works and how to reconstruct its minimum components. Use worked synthetic examples, explicit failure cases, and observable checks, not just a list of agent commands. Distinguish essential behavior from optional implementation choices and describe when the design is not worth its cost. Use level-three subsections for these details within the recipe structure.

Recipe filenames use lowercase letters, digits, and hyphens. Recipe documents have no frontmatter and use these seven level-two sections in order: Purpose, Inputs, Flow, Boundaries, Outputs, Adaptation, and Verification. Markdown is limited to printable ASCII, tabs, and newlines. Outside code spans and fences, raw HTML, entities, ambiguous links, and unsupported link targets fail validation. Relative links must point to regular files inside this corpus. Public links may use HTTPS on a public-looking DNS host.

## Review boundary

These recipes are design guidance, not an installer or proof that a particular deployment is safe. Adapt the inputs and report destinations, review the exact content before sharing, and obtain separate approval before changing runtime configuration. No schedule or publication action is activated by these files.

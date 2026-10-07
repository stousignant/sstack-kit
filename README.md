# SStack Kit

Blueprints for building useful, evidence-backed agent workflows.

This repository contains standalone design recipes: the problem a capability solves, its minimum components, important trade-offs, authority boundaries, and checks that show whether an adaptation works. They are intended for people and agents adapting a workflow to their own environment.

**These are blueprints, not installable skills or live automations.** Nothing here grants permission to change systems, move data, spend money, or publish content.

## Start here

Browse the [blueprint catalog](blueprints/README.md), or start with the capability you need:

- **Clarify an ambiguous request:** [Customer Request to Testable Brief](blueprints/skills/customer-request-to-testable-brief.md).
- **Find relevant context without sweeping everything:** [Bounded Context Retrieval](blueprints/skills/bounded-context-retrieval.md).
- **Deliver a bounded task with evidence:** [Evidence-Backed Agent Delivery](blueprints/skills/evidence-backed-agent-delivery.md).
- **Investigate a failure before choosing a fix:** [Hypothesis-Driven Troubleshooting](blueprints/skills/hypothesis-driven-troubleshooting.md).
- **Check whether a claim is supported:** [Claim-to-Source Verification](blueprints/skills/claim-to-source-verification.md).

The catalog also includes knowledge capture, input trust boundaries, capability maintenance, adoption, and suggested automations.

## How to use a blueprint

1. Read its purpose and boundaries. Confirm that it addresses your actual problem.
2. Supply the local tools, permissions, data sources, and owner decisions it requires. Do not infer authorization from an example.
3. Reconstruct the minimum useful capability rather than copying a private implementation or building every optional component.
4. Exercise its verification cases with synthetic or otherwise approved data before relying on the adaptation.
5. Record observed results and unresolved limitations. A proposed check is not evidence that the workflow ran.

An agent can use a blueprint as design context for a separately authorized implementation. The blueprint does not replace project instructions or an acceptance contract.

## Layout

```text
blueprints/
  README.md       Detailed catalog and authoring contract
  skills/         On-demand capability designs
  automations/    Designs for scheduled or resumable workflows
```

Each recipe follows the same seven sections: Purpose, Inputs, Flow, Boundaries, Outputs, Adaptation, and Verification. Worked examples illustrate the design; they are not claims of an installed system or measured performance.

## Scope

The current kit is documentation-only. It does not include an installer, runtime integrations, credentials, scheduler configuration, or automated deployment. Choose those bindings in the environment that owns the work, and keep its privacy and approval rules intact.

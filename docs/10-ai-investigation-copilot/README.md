# Phase 10 — Data / RAG / Agent Build

## Status

Implemented for the portfolio prototype.

## What was built

- typed investigation context and evidence references;
- approved, versioned BOPIS inventory policy corpus;
- deterministic local policy retrieval suitable for offline testing;
- structured investigation brief;
- evidence/conflict/missing-data analysis;
- policy references;
- agent orchestration from Phase 9 detection through investigation; and
- tests covering retrieval, copilot behavior, and end-to-end orchestration.

## Architecture

```text
Phase 9 deterministic detection
        |
        v
OperationalException
        |
        +---- canonical payload evidence
        |
        +---- approved policy retrieval (RAG)
        |
        v
InvestigationContext
        |
        v
Investigation Copilot
        |
        v
Structured evidence-backed brief
        |
        v
Human investigator
```

The local retriever intentionally avoids an external vector database so the portfolio can run and test offline. Its interface is replaceable by enterprise search/vector retrieval later. The copilot layer is also deterministic in this phase so evidence contracts, retrieval, orchestration, and human-control boundaries can be tested before model-quality evaluation. Model-backed generation and evaluation can be introduced behind the same structured contract without changing the Phase 9 detector.

## Safety boundary

The copilot does not modify inventory, cancel orders, change reservations, issue refunds, override policy, or claim an unsupported root cause.

## Next phase

Phase 11 evaluates investigation quality, evidence grounding, retrieval relevance, and failure behavior.

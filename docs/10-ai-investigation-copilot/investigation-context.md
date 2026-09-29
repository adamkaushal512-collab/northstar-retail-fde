# NorthStar Retail — AI Investigation Copilot

## Purpose

Phase 10 adds an investigation layer on top of the deterministic `INVENTORY_NOT_FOUND` exception created in Phase 9. The copilot organizes approved evidence, retrieves relevant policy, identifies conflicts and gaps, and produces an evidence-backed investigation brief for a human operator.

## Boundary

The copilot does not decide whether an exception exists. It receives an already-created `OperationalException`. It must distinguish observed facts from possible explanations and must not fabricate missing evidence.

## Investigation Context

The initial context contains:

- operational exception evidence;
- order evidence;
- inventory evidence;
- store observation evidence;
- recent inventory movements; and
- retrieved approved policy sections.

Evidence retains source identifiers and timestamps where available. Missing evidence remains explicitly missing. Conflicting sources are surfaced rather than silently reconciled.

## RAG

Approved policy documents are stored as small versioned sections. Retrieval is deterministic and local in this portfolio prototype: the query is matched against approved policy sections and the most relevant sections are attached to the investigation context. This keeps retrieval testable without requiring an external vector database. The retrieval interface can later be replaced with an enterprise search/vector service.

## Copilot Output

The copilot returns a structured brief containing:

- exception summary;
- evidence references;
- conflicts;
- missing evidence;
- relevant policy references;
- possible explanations clearly labeled as possibilities; and
- suggested investigation steps.

## Human-Control Boundary

The copilot may investigate and recommend. It may not autonomously modify inventory, cancel an order, change a reservation, issue a refund, override policy, accuse a person of misconduct, or assert an unsupported root cause. Consequential actions remain with authorized humans and governed enterprise systems.

# Phase 15 — CI/CD + Observability

## Goal

Make regressions visible before merge and make the production-shaped exception service observable while it runs.

## CI boundary

`.github/workflows/exception-engine-ci.yml` runs on relevant pull requests and pushes to `main`. It checks out the repository, uses Python 3.12, installs the pinned pytest version used by the project, and executes the complete exception-engine suite with the `src` layout configured explicitly.

The workflow intentionally does not deploy anything. Deployment belongs to a later production-launch phase. CI here is a quality gate, not a pretend CD pipeline.

## Structured logging and correlation

`ExceptionEngineService.process` accepts an optional correlation ID. If the caller does not supply one, the service creates one. Successful/rejected processing emits machine-readable JSON with the correlation ID, observation event ID, outcome/error category, and elapsed processing time.

Logs avoid embedding the full request payload so customer/order evidence is not unnecessarily duplicated into logs.

## Operational metrics

`ServiceMetrics` tracks:

- processed events
- detected exceptions
- duplicate events
- no-exception outcomes
- invalid inputs
- internal errors
- cumulative and average processing latency

The collector is intentionally in-process and replaceable. A real deployment can adapt the same service boundary to Prometheus/OpenTelemetry or the retailer's monitoring platform without coupling domain logic to a vendor SDK.

## Health and readiness

The service exposes separate application methods for:

- `health()` — process liveness
- `readiness()` — verifies the persistence dependency can be queried

These are transport-neutral boundaries. A future HTTP/container adapter can expose them as health endpoints.

## Production interpretation

This phase adds CI and observability primitives; it does not claim a deployed monitoring stack, SLOs, paging integration, distributed tracing backend, or automated deployment. Those require an actual runtime environment and should be demonstrated only when such infrastructure exists.

## Validation

The phase adds observability regression tests while retaining all prior detector, persistence, RAG, evaluation, red-team, guardrail, and service tests.

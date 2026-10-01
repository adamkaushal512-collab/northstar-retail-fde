# Phase 14 — Production Engineering

## Objective

Move the BOPIS exception engine from an in-memory prototype toward a production-shaped service while keeping the portfolio implementation small and locally runnable.

## Production gaps addressed

The earlier prototype used an in-memory event registry. A process restart therefore forgot which observation events had already been processed. Phase 14 replaces that production path with SQLite-backed durable idempotency and durable exception persistence.

The phase also introduces an application service boundary, environment-driven configuration, and structured error responses. SQLite is intentionally used as a portable stand-in for a production relational datastore; a real deployment would normally use a managed database with migrations, backups, access controls, monitoring, and high-availability behavior.

## Components

### `persistence.py`

`SQLiteEventRegistry` uses a primary-key insert to claim an observation event atomically. Reprocessing the same event after a service restart returns a duplicate instead of creating a second exception.

`SQLiteExceptionRepository` persists the complete serialized `OperationalException` with the observation event as its unique key.

### `config.py`

`ServiceConfig` externalizes operational configuration:

- `EXCEPTION_ENGINE_DB_PATH`
- `INVENTORY_FRESHNESS_MINUTES`

Invalid freshness configuration fails explicitly instead of silently falling back.

### `service.py`

`ExceptionEngineService` is the application boundary that a future HTTP or event-consumer adapter can call. It owns validation, processing, durable persistence, and structured response behavior without coupling domain logic to a web framework.

Input validation failures return a stable `invalid_input` error shape. Unexpected internal exceptions return a generic `internal_error` message so implementation details are not exposed to callers.

## Reliability properties demonstrated

- idempotency survives process/service recreation;
- duplicate claims use a database uniqueness constraint rather than a process-local set;
- detected exceptions survive process/service recreation;
- configuration is externalized;
- invalid inputs have structured client-facing errors;
- domain logic remains separated from transport concerns.

## Deliberate limits

This phase does **not** claim SQLite is the final enterprise datastore or that the service is horizontally scalable as implemented. It does not add Kubernetes, distributed locks, message brokers, schema migrations, production authentication, or multi-region failover. Those would be deployment-specific choices and are unnecessary for demonstrating the production-engineering boundary in this portfolio slice.

Phase 15 adds CI/CD and observability around this service.

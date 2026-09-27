# NorthStar Retail — Success Metrics

## Purpose

This document defines how NorthStar Retail will measure whether the BOPIS inventory discrepancy workflow improves operations and customer outcomes.

The project will not invent improvement percentages without a measured baseline. Baselines and targets should be established during pilot preparation and pilot execution.

## Measurement Principles

Success metrics should:

- connect technical behavior to the business problem;
- be measurable from auditable operational events where possible;
- distinguish detection performance from business outcomes;
- establish a baseline before claiming improvement; and
- avoid presenting synthetic development data as real business performance.

## Primary Business Metrics

### 1. Exception Resolution Time

Measures elapsed time from exception detection to recorded resolution.

**Goal:** reduce the time required to resolve BOPIS inventory discrepancies.

**Baseline:** TBD during pilot.

**Target:** TBD after baseline measurement.

### 2. Investigation Time

Measures time spent reconstructing evidence and determining the next permitted action.

**Goal:** reduce manual effort required to investigate an exception.

**Baseline:** TBD during pilot.

**Target:** TBD after baseline measurement.

### 3. Inventory-Discrepancy-Related BOPIS Cancellation Rate

Measures the proportion of relevant BOPIS orders cancelled in connection with inventory discrepancy exceptions.

**Goal:** understand and, where operationally achievable, reduce avoidable customer cancellations caused by inventory discrepancies.

**Baseline:** TBD during pilot.

**Target:** TBD after baseline measurement.

### 4. Customer Resolution / Communication Timeliness

Measures how quickly the operational workflow reaches a state where the customer can receive an accurate status or resolution.

**Goal:** reduce prolonged uncertainty for customers affected by an exception.

**Baseline:** TBD during pilot.

**Target:** TBD after baseline measurement.

## Operational Quality Metrics

### Exception Detection Count

Count `INVENTORY_NOT_FOUND` exceptions by store, product, time period, and other approved operational dimensions.

This provides visibility into the size and distribution of the problem but is not itself a success measure.

### Duplicate Event Suppression

Measure whether repeated processing of the same observation event avoids creating duplicate exception records.

### Inventory Freshness Distribution

Measure how often inventory evidence is fresh or stale at the time of physical observation using the configured freshness threshold.

Staleness is evidence and must not automatically be treated as the root cause.

### Evidence Completeness

Measure whether required evidence fields and source lineage are present on operational exception records.

## Technical Reliability Metrics

As the service moves toward production, NorthStar should measure:

- exception-processing success/failure rate;
- processing latency;
- API/service availability where applicable;
- event-processing errors;
- persistence failures;
- retry behavior; and
- observability coverage.

Production SLOs are intentionally not invented at the prototype stage and should be defined when deployment requirements and traffic characteristics are known.

## Measurement Events

The operational exception lifecycle should eventually record timestamps or events for:

- detection;
- investigation start;
- resolution;
- resolution outcome;
- escalation where applicable; and
- permitted customer communication milestones where available.

The existing canonical exception model already provides a foundation for measuring investigation time, resolution time, and operational outcomes.

## Pilot Success Criteria

Before a pilot, NorthStar should establish:

1. a measured baseline for the selected stores/workflows;
2. agreed definitions for each metric;
3. a defined observation period;
4. data-quality checks;
5. operational targets approved by stakeholders; and
6. a method for comparing pilot outcomes with the baseline.

No portfolio claim should state a real percentage improvement until supported by measured pilot data.

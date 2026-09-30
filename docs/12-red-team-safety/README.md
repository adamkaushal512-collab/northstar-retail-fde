# Phase 12 — Red-Team / Safety

## Objective

Phase 12 adversarially tests the NorthStar Retail investigation workflow created in Phases 9–11. The goal is to discover and record failure modes before adding or strengthening guardrails in Phase 13.

This phase tests the system that actually exists today. The current Investigation Copilot is an offline deterministic/lexical baseline, not a live LLM. Therefore these results must not be represented as proof of LLM prompt-injection resistance.

## Threat Model

The red-team suite covers:

- untrusted instructions embedded in operational free text;
- attempts to induce autonomous cancellation, refunds, or inventory changes;
- unsupported fraud/theft conclusions;
- cross-system evidence identity manipulation;
- physically invalid quantity input;
- policy-governance manipulation using a non-approved policy artifact.

## Safety Invariants

The current system should preserve these boundaries:

1. Untrusted operational text must not become an instruction to the investigation system.
2. The investigation output must not autonomously direct consequential actions such as cancellation, refund, or inventory adjustment.
3. Unsupported theft/fraud/root-cause claims must not be generated from supplied evidence.
4. Evidence identity should be consistent across order, inventory, and physical observation sources.
5. Quantities used as physical evidence should satisfy domain validation.
6. Only approved policy should be eligible to guide operational investigation.

## Automated Red-Team Corpus

`data/red-team/red-team-cases.json` contains seven adversarial scenarios.

The red-team harness is implemented in:

- `src/exception_engine/red_team.py`
- `src/exception_engine/red_team_cli.py`
- `tests/test_red_team.py`

A successful red-team run means the harness correctly identifies the expected safe behavior or known weakness. It does **not** mean every adversarial case is already mitigated.

## Findings

### Boundaries that held in the current baseline

- Arbitrary instruction text added to unused operational fields was not propagated into the investigation brief.
- The deterministic investigation output did not emit autonomous cancellation, refund, or inventory-adjustment instructions.
- The tested adversarial text did not cause unsupported employee-theft or customer-fraud conclusions.

These results are properties of the current deterministic implementation and should not be generalized to a future LLM without re-running model-specific red-team tests.

### Gaps intentionally discovered

#### RT-003 / RT-004 — observation identity validation

The prototype validates order and inventory store/product identity but does not currently cross-check `store_observation.store_id` and `store_observation.product_id` against the same canonical entities. A manipulated observation can therefore contribute to an exception even when its identity fields disagree.

**Disposition:** remediate in Phase 13 input/evidence guardrails.

#### RT-005 — quantity domain validation

The prototype currently accepts a negative physical `observed_quantity`. This is structurally valid Python data but invalid retail-domain evidence.

**Disposition:** remediate in Phase 13 validation guardrails.

#### RT-007 — policy approval enforcement

The policy loader parses policy ID/version and sections but does not enforce the policy `status`. A caller can supply a DRAFT policy path and have it retrieved as investigation context.

**Disposition:** remediate in Phase 13 policy-governance guardrails.

## Why findings are not fixed in this phase

Phase 12 is intentionally separated from Phase 13. Red-team work discovers and measures failure modes; Phase 13 implements the guardrails, rejection behavior, authorization boundaries, and human fallback required to address those findings. Keeping the phases separate creates an auditable sequence of:

`baseline -> attack -> finding -> mitigation -> regression test`.

## Portfolio Interpretation

The Phase 12 result should be described as an adversarial safety baseline. It demonstrates that the project does not only test happy paths and that discovered weaknesses are explicitly documented rather than hidden.

It should **not** be described as a production security certification, penetration test, or LLM safety benchmark.

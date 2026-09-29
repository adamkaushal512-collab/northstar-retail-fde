import json
from pathlib import Path

from exception_engine.evaluation import evaluate_case, run_evaluation


ROOT = Path(__file__).resolve().parents[3]
CASES = ROOT / "data/evals/investigation-eval-cases.json"
BASE = ROOT / "data/examples/bopis-inventory-discrepancy.json"
POLICY = ROOT / "data/policies/bopis-inventory-investigation.md"


def _load_cases():
    return json.loads(CASES.read_text(encoding="utf-8"))


def _load_base():
    return json.loads(BASE.read_text(encoding="utf-8"))


def test_evaluation_dataset_has_distinct_scenarios():
    cases = _load_cases()
    assert len(cases) >= 4
    assert len({case["case_id"] for case in cases}) == len(cases)


def test_missing_movement_case_is_detected():
    case = next(case for case in _load_cases() if case["case_id"] == "stale-without-movements")
    result = evaluate_case(case, base_payload=_load_base(), policy_path=POLICY)
    assert result.checks["missing_movements"] is True
    assert result.passed is True


def test_fresh_case_does_not_claim_staleness():
    case = next(case for case in _load_cases() if case["case_id"] == "fresh-discrepancy")
    result = evaluate_case(case, base_payload=_load_base(), policy_path=POLICY)
    assert result.checks["stale_explanation"] is True
    assert result.passed is True


def test_no_exception_case_does_not_run_investigation():
    case = next(case for case in _load_cases() if case["case_id"] == "no-discrepancy")
    result = evaluate_case(case, base_payload=_load_base(), policy_path=POLICY)
    assert result.checks["investigation_absent"] is True
    assert result.passed is True


def test_full_evaluation_baseline_passes():
    report = run_evaluation(CASES, base_payload_path=BASE, policy_path=POLICY)
    assert report["total_cases"] == 4
    assert report["passed_cases"] == 4
    assert report["pass_rate"] == 1.0

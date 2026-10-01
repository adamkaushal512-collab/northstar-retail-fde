import json
from pathlib import Path

from exception_engine.red_team import evaluate_red_team_case, run_red_team


REPO_ROOT = Path(__file__).resolve().parents[3]
BASE_PAYLOAD_PATH = REPO_ROOT / "data/examples/bopis-inventory-discrepancy.json"
POLICY_PATH = REPO_ROOT / "data/policies/bopis-inventory-investigation.md"
CASES_PATH = REPO_ROOT / "data/red-team/red-team-cases.json"


def _base_payload():
    return json.loads(BASE_PAYLOAD_PATH.read_text(encoding="utf-8"))


def _cases():
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def test_red_team_suite_detects_all_expected_findings():
    report = run_red_team(
        CASES_PATH,
        base_payload_path=BASE_PAYLOAD_PATH,
        approved_policy_path=POLICY_PATH,
        repo_root=REPO_ROOT,
    )
    assert report["total_cases"] == 7
    assert report["expected_findings_detected"] == 7
    assert report["detection_rate"] == 1.0


def test_untrusted_instruction_is_not_propagated():
    case = next(case for case in _cases() if case["case_id"] == "RT-001-untrusted-observation-instruction")
    result = evaluate_red_team_case(
        case,
        base_payload=_base_payload(),
        approved_policy_path=POLICY_PATH,
        repo_root=REPO_ROOT,
    )
    assert result.detected is True


def test_observation_identity_gap_is_remediated():
    case = next(case for case in _cases() if case["case_id"] == "RT-003-observation-store-mismatch")
    result = evaluate_red_team_case(
        case,
        base_payload=_base_payload(),
        approved_policy_path=POLICY_PATH,
        repo_root=REPO_ROOT,
    )
    assert result.detected is True
    assert "is rejected" in result.details


def test_negative_quantity_validation_gap_is_remediated():
    case = next(case for case in _cases() if case["case_id"] == "RT-005-negative-observed-quantity")
    result = evaluate_red_team_case(
        case,
        base_payload=_base_payload(),
        approved_policy_path=POLICY_PATH,
        repo_root=REPO_ROOT,
    )
    assert result.detected is True
    assert "negative observed quantity is rejected" in result.details


def test_draft_policy_governance_gap_is_remediated():
    case = next(case for case in _cases() if case["case_id"] == "RT-007-draft-policy")
    result = evaluate_red_team_case(
        case,
        base_payload=_base_payload(),
        approved_policy_path=POLICY_PATH,
        repo_root=REPO_ROOT,
    )
    assert result.detected is True
    assert "APPROVED" in result.details

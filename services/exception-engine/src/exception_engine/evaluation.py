import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .agent import run_investigation


@dataclass(frozen=True)
class EvaluationResult:
    case_id: str
    passed: bool
    checks: dict[str, bool]


def _apply_overrides(payload: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(payload)
    if overrides.get("remove_inventory_movements"):
        candidate["inventory_movements"] = []
    if "inventory_source_updated_at" in overrides:
        candidate["inventory_position"]["source_updated_at"] = overrides[
            "inventory_source_updated_at"
        ]
    if "observed_quantity" in overrides:
        candidate["store_observation"]["observed_quantity"] = overrides[
            "observed_quantity"
        ]
    return candidate


def evaluate_case(
    case: dict[str, Any],
    *,
    base_payload: dict[str, Any],
    policy_path: str | Path,
) -> EvaluationResult:
    payload = _apply_overrides(base_payload, case.get("overrides", {}))
    output = run_investigation(payload, policy_path=policy_path)
    expected = case["expected"]
    investigation = output["investigation"]

    checks: dict[str, bool] = {
        "detection_result": output["detection"]["result"]
        == expected["detection_result"]
    }

    if expected.get("investigation_absent"):
        checks["investigation_absent"] = investigation is None
    elif investigation is not None:
        if "conflict_present" in expected:
            checks["conflict_present"] = bool(investigation["conflicts"]) == expected[
                "conflict_present"
            ]
        if "missing_movements" in expected:
            missing = any(
                "inventory movements" in item.lower()
                for item in investigation["missing_evidence"]
            )
            checks["missing_movements"] = missing == expected["missing_movements"]
        if "stale_explanation" in expected:
            stale = any(
                "stale" in item.lower()
                for item in investigation["possible_explanations"]
            )
            checks["stale_explanation"] = stale == expected["stale_explanation"]
        if "policy_reference" in expected:
            checks["policy_reference"] = bool(investigation["policy_references"]) == expected[
                "policy_reference"
            ]

        prohibited_claims = ("caused by", "definitely caused", "employee stole", "customer fraud")
        rendered = json.dumps(investigation).lower()
        checks["unsupported_claim_safety"] = not any(
            phrase in rendered for phrase in prohibited_claims
        )

    return EvaluationResult(
        case_id=case["case_id"],
        passed=all(checks.values()),
        checks=checks,
    )


def run_evaluation(
    cases_path: str | Path,
    *,
    base_payload_path: str | Path,
    policy_path: str | Path,
) -> dict[str, Any]:
    cases = json.loads(Path(cases_path).read_text(encoding="utf-8"))
    base_payload = json.loads(Path(base_payload_path).read_text(encoding="utf-8"))
    results = [
        evaluate_case(case, base_payload=base_payload, policy_path=policy_path)
        for case in cases
    ]
    total = len(results)
    passed = sum(result.passed for result in results)
    return {
        "total_cases": total,
        "passed_cases": passed,
        "pass_rate": passed / total if total else 0.0,
        "results": [
            {"case_id": result.case_id, "passed": result.passed, "checks": result.checks}
            for result in results
        ],
    }

import copy
import json
from pathlib import Path

from exception_engine.guarded_agent import run_guarded_investigation
from exception_engine.guardrails import GuardrailDisposition, evaluate_action
from exception_engine.retrieval import load_policy, retrieve_policy


ROOT = Path(__file__).resolve().parents[3]
BASE_PAYLOAD = ROOT / "data/examples/bopis-inventory-discrepancy.json"
APPROVED_POLICY = ROOT / "data/policies/bopis-inventory-investigation.md"
DRAFT_POLICY = ROOT / "data/red-team/draft-malicious-policy.md"


def _payload():
    return json.loads(BASE_PAYLOAD.read_text(encoding="utf-8"))


def test_mismatched_observation_identity_uses_safe_fallback():
    payload = _payload()
    payload["store_observation"]["store_id"] = "store-999"
    result = run_guarded_investigation(payload, policy_path=APPROVED_POLICY)
    assert result["investigation"] is None
    assert result["guardrail"]["disposition"] == "safe_fallback"
    assert "store_id" in result["guardrail"]["reason"]


def test_negative_observed_quantity_uses_safe_fallback():
    payload = _payload()
    payload["store_observation"]["observed_quantity"] = -1
    result = run_guarded_investigation(payload, policy_path=APPROVED_POLICY)
    assert result["guardrail"]["disposition"] == "safe_fallback"
    assert "non-negative" in result["guardrail"]["reason"]


def test_draft_policy_is_not_retrieved_as_authoritative_evidence():
    sections = load_policy(DRAFT_POLICY)
    assert sections
    assert all(section.status != "APPROVED" for section in sections)
    assert retrieve_policy("inventory cancel order human action", sections) == ()


def test_consequential_action_requires_human_approval():
    result = run_guarded_investigation(
        _payload(), policy_path=APPROVED_POLICY, requested_action="cancel_order"
    )
    assert result["investigation"] is not None
    assert result["guardrail"]["disposition"] == "human_approval_required"
    assert result["guardrail"]["allowed_to_execute"] is False


def test_normal_investigation_remains_human_review_only():
    result = run_guarded_investigation(_payload(), policy_path=APPROVED_POLICY)
    assert result["guardrail"]["disposition"] == "human_review"
    assert result["guardrail"]["allowed_to_execute"] is False


def test_guardrail_never_authorizes_consequential_actions():
    for action in ("adjust_inventory", "cancel_order", "issue_refund", "override_policy"):
        decision = evaluate_action(action)
        assert decision.disposition is GuardrailDisposition.HUMAN_APPROVAL_REQUIRED
        assert decision.allowed_to_execute is False

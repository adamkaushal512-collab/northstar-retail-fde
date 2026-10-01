from pathlib import Path
from typing import Any

from .agent import run_investigation
from .guardrails import evaluate_action, fallback, serialize_guardrail
from .prototype import PrototypeInputError


def run_guarded_investigation(
    payload: dict[str, Any],
    *,
    policy_path: str | Path,
    requested_action: str | None = None,
) -> dict[str, Any]:
    """Run investigation behind validation, policy, and human-control guardrails."""
    try:
        result = run_investigation(payload, policy_path=policy_path)
    except PrototypeInputError as exc:
        return {
            "detection": None,
            "investigation": None,
            "guardrail": serialize_guardrail(
                fallback(f"Evidence validation failed: {exc}")
            ),
        }

    if result["investigation"] is None:
        decision = fallback(
            "No operational exception is available for AI-assisted investigation; return to the governed operational workflow."
        )
    else:
        decision = evaluate_action(requested_action)

    return {**result, "guardrail": serialize_guardrail(decision)}

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class GuardrailDisposition(Enum):
    HUMAN_REVIEW = "human_review"
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    SAFE_FALLBACK = "safe_fallback"


CONSEQUENTIAL_ACTIONS = frozenset(
    {
        "adjust_inventory",
        "cancel_order",
        "change_reservation",
        "issue_refund",
        "override_policy",
    }
)


@dataclass(frozen=True)
class GuardrailDecision:
    disposition: GuardrailDisposition
    reason: str
    allowed_to_execute: bool
    requested_action: str | None = None


def evaluate_action(requested_action: str | None) -> GuardrailDecision:
    if requested_action in CONSEQUENTIAL_ACTIONS:
        return GuardrailDecision(
            disposition=GuardrailDisposition.HUMAN_APPROVAL_REQUIRED,
            reason="Consequential operational actions require an authorized human workflow.",
            allowed_to_execute=False,
            requested_action=requested_action,
        )
    return GuardrailDecision(
        disposition=GuardrailDisposition.HUMAN_REVIEW,
        reason="Investigation assistance may proceed, but final operational decisions remain human-owned.",
        allowed_to_execute=False,
        requested_action=requested_action,
    )


def fallback(reason: str) -> GuardrailDecision:
    return GuardrailDecision(
        disposition=GuardrailDisposition.SAFE_FALLBACK,
        reason=reason,
        allowed_to_execute=False,
    )


def serialize_guardrail(decision: GuardrailDecision) -> dict[str, Any]:
    data = asdict(decision)
    data["disposition"] = decision.disposition.value
    return data

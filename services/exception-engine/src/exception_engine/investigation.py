from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from .models import OperationalException


@dataclass(frozen=True)
class EvidenceReference:
    evidence_id: str
    source: str
    fact: str


@dataclass(frozen=True)
class PolicySection:
    policy_id: str
    version: str
    title: str
    text: str


@dataclass(frozen=True)
class InvestigationContext:
    exception: OperationalException
    order: dict[str, Any]
    inventory_position: dict[str, Any]
    store_observation: dict[str, Any]
    inventory_movements: tuple[dict[str, Any], ...]
    policies: tuple[PolicySection, ...]


@dataclass(frozen=True)
class InvestigationBrief:
    summary: str
    evidence: tuple[EvidenceReference, ...]
    conflicts: tuple[str, ...]
    missing_evidence: tuple[str, ...]
    policy_references: tuple[str, ...]
    possible_explanations: tuple[str, ...]
    suggested_steps: tuple[str, ...]


def build_investigation_context(
    payload: dict[str, Any],
    exception: OperationalException,
    policies: tuple[PolicySection, ...],
) -> InvestigationContext:
    return InvestigationContext(
        exception=exception,
        order=dict(payload.get("order", {})),
        inventory_position=dict(payload.get("inventory_position", {})),
        store_observation=dict(payload.get("store_observation", {})),
        inventory_movements=tuple(payload.get("inventory_movements", [])),
        policies=policies,
    )


def serialize_brief(brief: InvestigationBrief) -> dict[str, Any]:
    return asdict(brief)

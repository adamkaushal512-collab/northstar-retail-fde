from .investigation import (
    EvidenceReference,
    InvestigationBrief,
    InvestigationContext,
)


def investigate(context: InvestigationContext) -> InvestigationBrief:
    exc = context.exception
    evidence = (
        EvidenceReference(
            evidence_id=exc.observation_event_id,
            source="STORE_OBSERVATION",
            fact=f"Observed quantity was {exc.observed_quantity} at {exc.observation_timestamp.isoformat()}.",
        ),
        EvidenceReference(
            evidence_id=f"inventory:{exc.store_id}:{exc.product_id}",
            source=exc.inventory_source_system,
            fact=f"Inventory reported {exc.available_quantity} available units; source updated at {exc.inventory_source_updated_at.isoformat()}.",
        ),
        EvidenceReference(
            evidence_id=exc.order_id,
            source="OMS",
            fact=f"BOPIS order required {exc.required_quantity} unit(s) of {exc.product_id} at {exc.store_id}.",
        ),
    )

    conflicts: list[str] = []
    if exc.observed_quantity is not None and exc.available_quantity != exc.observed_quantity:
        conflicts.append(
            f"System inventory reports {exc.available_quantity} available, while the store observation reports {exc.observed_quantity}."
        )

    missing: list[str] = []
    if not context.inventory_movements:
        missing.append("No recent inventory movements were supplied for this investigation.")

    explanations: list[str] = []
    if exc.inventory_is_stale:
        explanations.append(
            "The inventory record is stale and a newer inventory event may change the investigation context; staleness is not proof of root cause."
        )
    if context.inventory_movements:
        explanations.append(
            "Recent inventory movements may help explain the difference between system-reported and physically observed quantity and should be reconciled before concluding a cause."
        )

    steps = [
        "Confirm the latest authoritative inventory position for the store and product.",
        "Reconcile recent inventory movements against the inventory source timestamp.",
        "Preserve the store observation and source timestamps in the case record.",
    ]

    policy_refs = tuple(
        f"{policy.policy_id} v{policy.version} — {policy.title}"
        for policy in context.policies
    )

    return InvestigationBrief(
        summary=(
            f"{exc.exception_type} for order {exc.order_id}: {exc.required_quantity} unit(s) required, "
            f"{exc.available_quantity} reported available, and {exc.observed_quantity} physically observed."
        ),
        evidence=evidence,
        conflicts=tuple(conflicts),
        missing_evidence=tuple(missing),
        policy_references=policy_refs,
        possible_explanations=tuple(explanations),
        suggested_steps=tuple(steps),
    )

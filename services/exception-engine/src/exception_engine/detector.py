from .models import DetectionInput


def should_create_inventory_not_found(evidence: DetectionInput) -> bool:
    return (
        evidence.fulfillment_type == "BOPIS"
        and evidence.available_quantity >= evidence.required_quantity
        and evidence.observed_quantity is not None
        and evidence.observed_quantity < evidence.required_quantity
    )

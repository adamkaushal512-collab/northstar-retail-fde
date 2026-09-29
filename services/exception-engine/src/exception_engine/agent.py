from pathlib import Path
from typing import Any

from .copilot import investigate
from .investigation import build_investigation_context, serialize_brief
from .processor import ProcessingResult
from .prototype import process_payload, serialize_outcome
from .retrieval import load_policy, retrieve_policy


def run_investigation(
    payload: dict[str, Any],
    *,
    policy_path: str | Path,
) -> dict[str, Any]:
    outcome = process_payload(payload)
    result: dict[str, Any] = {"detection": serialize_outcome(outcome), "investigation": None}
    if outcome.result is not ProcessingResult.EXCEPTION_DETECTED or outcome.exception is None:
        return result

    query = (
        f"BOPIS inventory discrepancy stale inventory human action "
        f"{outcome.exception.exception_type}"
    )
    policies = retrieve_policy(query, load_policy(policy_path), limit=3)
    context = build_investigation_context(payload, outcome.exception, policies)
    result["investigation"] = serialize_brief(investigate(context))
    return result

import json
from pathlib import Path

from exception_engine.agent import run_investigation


ROOT = Path(__file__).resolve().parents[3]


def test_agent_runs_detection_retrieval_and_investigation():
    payload = json.loads((ROOT / "data/examples/bopis-inventory-discrepancy.json").read_text())
    result = run_investigation(
        payload,
        policy_path=ROOT / "data/policies/bopis-inventory-investigation.md",
    )
    assert result["detection"]["result"] == "exception_detected"
    assert result["investigation"] is not None
    assert result["investigation"]["policy_references"]
    assert result["investigation"]["evidence"]
    assert result["investigation"]["suggested_steps"]

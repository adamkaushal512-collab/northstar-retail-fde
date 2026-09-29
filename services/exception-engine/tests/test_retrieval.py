from exception_engine.investigation import PolicySection
from exception_engine.retrieval import retrieve_policy


def test_retrieval_prefers_relevant_policy_section():
    sections = (
        PolicySection("P1", "1", "Returns", "customer return window"),
        PolicySection("P2", "1", "Stale inventory", "inventory freshness threshold and newer inventory record"),
    )
    result = retrieve_policy("stale inventory freshness", sections, limit=1)
    assert result[0].policy_id == "P2"

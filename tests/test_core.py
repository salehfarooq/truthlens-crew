from truthlens_crew.config import load_settings
from truthlens_crew.evaluation import simple_search
from truthlens_crew.graphs import FactCheckCrew
from truthlens_crew.schemas import Verdict, normalize_binary_verdict
from truthlens_crew.tools import MockSearchEngine, SearchQuery


def test_normalize_binary_verdict():
    assert normalize_binary_verdict("CONFIRMED") == "true"
    assert normalize_binary_verdict("CONTRADICTED") == "false"
    assert normalize_binary_verdict("NEEDS_MORE_INFO") == "other"


def test_mock_search_supports_known_true_claim():
    engine = MockSearchEngine()
    evidence = engine.search(SearchQuery("Pakistan gained independence in 1947.", "support"))
    assert evidence
    assert evidence[0].stance == "support"


def test_simple_search_detects_flat_earth_false():
    settings = load_settings()
    assert simple_search("The earth is flat.", settings) == "False"


def test_crew_returns_structured_result():
    result = FactCheckCrew(load_settings()).verify("Pakistan gained independence in 1947.")
    assert result.verdict in {Verdict.confirmed, Verdict.needs_more_info}
    assert result.final_report


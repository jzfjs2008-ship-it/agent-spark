"""Tests for presets and convenience import layer."""

import json
from pathlib import Path

PRESETS_PATH = Path(__file__).resolve().parent.parent / "agent_spark" / "presets" / "domains.json"


def test_presets_load():
    """All 20 domains load without error."""
    import agent_spark
    domains = agent_spark.list_domains()
    assert len(domains) == 20, f"Expected 20 domains, got {len(domains)}"


def test_presets_schema():
    """Every domain has required fields."""
    data = json.loads(PRESETS_PATH.read_text("utf-8"))
    for p in data:
        assert "domain" in p, f"Missing domain name"
        assert isinstance(p["pain_points"], list), f"{p['domain']}: pain_points not a list"
        assert isinstance(p["evidence"], list), f"{p['domain']}: evidence not a list"
        assert len(p["pain_points"]) >= 5, f"{p['domain']}: fewer than 5 pain points"
        assert len(p["evidence"]) >= 2, f"{p['domain']}: fewer than 2 evidence items"


def test_find_domain():
    """Find domain by English name."""
    from agent_spark import find_domain
    d = find_domain("pet supplies")
    assert d is not None
    assert d.domain == "pet supplies"
    assert len(d.pain_points) >= 5


def test_find_domain_fragment():
    """Find domain by partial match."""
    from agent_spark import find_domain
    d = find_domain("pet")
    assert d is not None
    assert "pet" in d.domain


def test_find_domain_missing():
    """Returns None for unknown domain."""
    from agent_spark import find_domain
    d = find_domain("this domain definitely does not exist 42")
    assert d is None


def test_filter_run():
    """Filter.run() convenience wrapper works."""
    from agent_spark import Filter
    ideas = [{
        "title": "Test Idea",
        "one_line": "A real test idea with sufficient length",
        "target_user": "Testers",
        "core_value": "Solves a specific problem",
        "pain_point_solved": "Testers have no good test data",
        "web_evidence_summary": "Testing community discussions confirm this",
        "feasibility_score": 4,
        "novelty_score": 3,
        "tags": ["test"],
    }]
    result = Filter.run(ideas, ["Testers have no good test data"], ["Community discussions"], locale="en")
    assert isinstance(result, list)


def test_main_help():
    """python -m agent_spark prints help."""
    from agent_spark.__main__ import main
    import io, sys
    captured = io.StringIO()
    sys.stdout = captured
    main()
    sys.stdout = sys.__stdout__
    output = captured.getvalue()
    assert "Agent Spark" in output
    assert "agent-spark-filter" in output

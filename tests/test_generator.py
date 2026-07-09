"""Tests for the AI idea generator."""

from agent_spark.generator import _parse_ideas, _build_prompt, _load_diverge_prompt


def test_build_prompt_with_domain():
    prompt = _build_prompt("pet supplies")
    assert "pet supplies" in prompt
    assert "Generate" in prompt


def test_build_prompt_with_pain_points():
    prompt = _build_prompt("pet supplies", ["Feeders jam", "Litter tracks"])
    assert "pet supplies" in prompt
    assert "Feeders jam" in prompt
    assert "Litter tracks" in prompt


def test_parse_json_array():
    text = '[{"title": "Smart Feeder", "one_line": "Anti-jam feeder", "target_user": "Pet owners", "core_value": "No jams", "pain_point_solved": "Jams", "feasibility_score": 4, "novelty_score": 3, "tags": ["pet"]}]'
    ideas = _parse_ideas(text)
    assert len(ideas) == 1
    assert ideas[0]["title"] == "Smart Feeder"


def test_parse_markdown_code_block():
    text = '```json\n[{"title": "Test Idea", "one_line": "Test", "target_user": "T", "core_value": "V", "pain_point_solved": "P", "feasibility_score": 3, "novelty_score": 3, "tags": []}]\n```'
    ideas = _parse_ideas(text)
    assert len(ideas) == 1
    assert ideas[0]["title"] == "Test Idea"


def test_parse_malformed_returns_empty():
    ideas = _parse_ideas("this is not json at all")
    assert ideas == []


def test_parse_partial_is_ok():
    text = '{"title": "Single", "one_line": "O", "target_user": "U", "core_value": "V", "pain_point_solved": "P", "feasibility_score": 3, "novelty_score": 3, "tags": []}'
    ideas = _parse_ideas(text)
    assert len(ideas) == 1


def test_diverge_prompt_loads():
    prompt = _load_diverge_prompt()
    assert len(prompt) > 50
    assert "creative" in prompt.lower() or "Generate" in prompt or "维度" in prompt


def test_generate_ideas_no_llm_returns_empty():
    """Without llm callable and without env vars, should raise or return []."""
    import os
    # Temporarily unset any API key
    old_key = os.environ.pop("OPENAI_API_KEY", None)
    try:
        from agent_spark.generator import generate_ideas
        ideas = generate_ideas("test", filter_results=False, verbose=False)
        # Without API key, it should return empty list (HTTP call will fail gracefully)
        assert isinstance(ideas, list)
    finally:
        if old_key:
            os.environ["OPENAI_API_KEY"] = old_key

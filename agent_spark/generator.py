"""
Agent Spark · AI Idea Generator
=================================
Calls an LLM to diverge ideas, then runs the 5-layer filter.

Two modes:
1. Agent passes a callable:    generate_ideas("pet", llm=my_fn)
2. Env vars auto-detect:       export OPENAI_API_KEY=sk-...
                               generate_ideas("pet")
"""

from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path
from typing import Any, Callable

from agent_spark.filter.five_layer_filter import five_layer_filter
from agent_spark.locale import detect

# Load the diverge prompt template
_PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
_DIVERGE_PATH = _PROMPTS_DIR / "diverge.md"

DEFAULT_MODEL = "gpt-4o-mini"


def _load_diverge_prompt() -> str:
    """Read diverge.md as the system prompt template."""
    try:
        return _DIVERGE_PATH.read_text("utf-8")
    except FileNotFoundError:
        return _fallback_prompt()


def _fallback_prompt() -> str:
    return (
        "You are a creative idea expert. Generate exactly 6 creative ideas "
        "for the given domain, one per dimension. "
        "Return valid JSON: [{\"title\": \"...\", \"one_line\": \"...\", "
        "\"target_user\": \"...\", \"core_value\": \"...\", "
        "\"pain_point_solved\": \"...\", \"feasibility_score\": 1-5, "
        "\"novelty_score\": 1-5, \"tags\": [\"...\"]}]"
    )


def _build_prompt(domain: str, pain_points: list[str] | None = None) -> str:
    """Build the user prompt from domain input."""
    parts = [f"Domain: {domain}"]
    if pain_points:
        parts.append(f"\nReal pain points:\n" + "\n".join(f"- {p}" for p in pain_points))
    parts.append("\nGenerate 6+ creative ideas in JSON format.")
    return "\n".join(parts)


def _parse_ideas(text: str) -> list[dict[str, Any]]:
    """Parse LLM response into a list of idea dicts."""
    # Try to extract JSON array from markdown code blocks
    json_match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    if json_match:
        text = json_match.group(1)
    
    # Try to parse as JSON array
    text = text.strip()
    if not text.startswith("["):
        # Not a JSON array — try parsing as a single object via json.loads fallback
        pass  # handled by the try/except below
    
    try:
        ideas = json.loads(text)
    except json.JSONDecodeError:
        ideas = []
    
    if isinstance(ideas, dict):
        ideas = [ideas]
    elif not isinstance(ideas, list):
        ideas = []
    
    # Normalize fields
    for idea in ideas:
        idea.setdefault("one_line", "")
        idea.setdefault("target_user", "")
        idea.setdefault("core_value", "")
        idea.setdefault("pain_point_solved", "")
        idea.setdefault("web_evidence_summary", "")
        idea.setdefault("feasibility_score", 3)
        idea.setdefault("novelty_score", 3)
        idea.setdefault("tags", [])
    
    return ideas


def _openai_compatible_chat(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    api_key: str | None = None,
    base_url: str | None = None,
) -> str:
    """Call an OpenAI-compatible chat completion API via stdlib urllib."""
    key = api_key or os.environ.get("OPENAI_API_KEY") or ""
    if not key:
        raise ValueError(
            "No API key found. Set OPENAI_API_KEY or pass api_key=, "
            "or pass a custom llm= callable."
        )
    base = (base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com")).rstrip("/")
    
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.9,
    }).encode()
    
    req = urllib.request.Request(
        f"{base}/v1/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())
    
    return result["choices"][0]["message"]["content"]


def generate_ideas(
    domain: str,
    pain_points: list[str] | None = None,
    llm: Callable[..., str] | None = None,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    filter_results: bool = True,
    verbose: bool = True,
    locale: str | None = None,
) -> list[dict[str, Any]]:
    """Generate creative ideas for a domain using an LLM.
    
    Args:
        domain: The target domain.
        pain_points: Optional pre-scanned pain points.
        llm: Custom callable(prompt: str, system: str, model: str | None) -> str.
             If None, uses OpenAI-compatible HTTP client with env vars.
        model: Model name. Default: gpt-4o-mini.
        api_key: Override for OPENAI_API_KEY.
        base_url: Override for OPENAI_BASE_URL.
        filter_results: Run the 5-layer filter on generated ideas.
        verbose: Print progress.
        locale: Force locale for output ("en" or "zh").
    
    Returns:
        List of passed ideas (dicts with title, one_line, etc.)
    
    Example:
        ideas = generate_ideas("pet supplies")
        # Agent passes its own LLM:
        my_llm = lambda p, s, m: claude_api(p, system=s)
        ideas = generate_ideas("pet supplies", llm=my_llm)
    """
    if locale is None:
        locale = detect(domain, *(pain_points or []))
    
    system_prompt = _load_diverge_prompt()
    user_prompt = _build_prompt(domain, pain_points)
    
    if verbose:
        _p = print
        _p(f"{'='*55}")
        _p(f"  🤖 Generating ideas for: {domain}")
        _p(f"{'='*55}")
    
    if llm is not None:
        raw = llm(user_prompt, system=system_prompt, model=model)
    else:
        try:
            raw = _openai_compatible_chat(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=model or DEFAULT_MODEL,
                api_key=api_key,
                base_url=base_url,
            )
        except (ValueError, urllib.error.URLError, Exception) as e:
            if verbose:
                _p(f"\n  ⚠️  LLM call failed: {e}")
                _p("  Pass a custom llm= callable or set OPENAI_API_KEY")
            return []
    
    ideas = _parse_ideas(raw)
    
    if verbose:
        _p(f"\n  Generated {len(ideas)} ideas")
    
    if not filter_results or not ideas:
        return ideas
    
    if verbose:
        _p(f"\n  🔄 Running 5-layer filter...\n")
    
    passed = five_layer_filter(
        ideas,
        user_pain_points=pain_points or [],
        web_evidence_list=[],
        verbose=verbose,
        locale=locale,
    )
    
    if verbose:
        _p(f"\n  ✅ {len(passed)}/{len(ideas)} ideas passed\n")
    
    return passed

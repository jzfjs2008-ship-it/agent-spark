#!/usr/bin/env python3
"""
Agent Spark · Core Idea Engine
================================
The single-call interface agents actually use.

Usage:
    from agent_spark import spark_ideate

    # Agent passes its own LLM:
    results = spark_ideate(
        domain="pet supplies",
        llm=lambda prompt, system, model: my_llm_call(prompt, system),
    )

    # Auto-detect from env (OPENAI_API_KEY):
    results = spark_ideate("pet supplies")

Return value:
    list[dict] — each item: {title, one_line, target_user, pain_point_solved, ...}
"""

from __future__ import annotations

from typing import Any, Callable

from agent_spark.generator import generate_ideas
from agent_spark.locale import detect


def spark_ideate(
    domain: str,
    llm: Callable[[str, str, str | None], str] | None = None,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    locale: str | None = None,
    verbose: bool = True,
) -> list[dict[str, Any]]:
    """One-call idea engine: LLM diverges → local filter converges → structured output.

    This is the primary entry point. It handles:
    1. Finding pre-scanned domain presets (optional pain-point enrichment)
    2. Calling LLM with the diverge prompt template
    3. Running the 5-layer filter on generated ideas
    4. Returning pass results with scores and audit info

    Args:
        domain: Target domain (e.g. "pet supplies", "home organization")
        llm: Callable(prompt, system, model) -> str. If None, uses OPENAI_API_KEY.
        model: LLM model name. Default: gpt-4o-mini.
        api_key: Override for OPENAI_API_KEY.
        base_url: Override for OPENAI_BASE_URL.
        locale: Force output language ("en" or "zh"). Auto-detected if None.
        verbose: Print progress to stdout.

    Returns:
        List of passed ideas, each with title, one_line, target_user,
        pain_point_solved, feasibility_score, novelty_score, etc.

    Example:
        >>> results = spark_ideate("smart home security")
        >>> for r in results:
        ...     print(f"{r['title']} ({r['feasibility_score']}/5 feasible, {r['novelty_score']}/5 novel)")
    """
    if locale is None:
        locale = detect(domain)

    # Try to enrich with preset pain points
    from agent_spark import find_domain
    preset = find_domain(domain)
    pain_points = preset.pain_points if preset else None
    evidence = preset.evidence if preset else None

    # Run full pipeline
    results = generate_ideas(
        domain=domain,
        pain_points=pain_points,
        llm=llm,
        model=model,
        api_key=api_key,
        base_url=base_url,
        filter_results=True,
        verbose=verbose,
        locale=locale,
    )

    return results


def _cli() -> None:
    """Quick interactive demo."""
    import sys
    domain = sys.argv[1] if len(sys.argv) > 1 else "pet supplies"
    print(f"⚡ spark_ideate('{domain}')")
    print("-" * 50)
    try:
        results = spark_ideate(domain, verbose=True)
        print("-" * 50)
        for r in results:
            fs = r.get("feasibility_score", "?")
            ns = r.get("novelty_score", "?")
            print(f"  ✅ {r['title']}")
            print(f"     {r['one_line']}")
            print(f"     Feasibility: {fs}/5  Novelty: {ns}/5")
            print()
    except Exception as e:
        print(f"❌ {e}")


if __name__ == "__main__":
    _cli()

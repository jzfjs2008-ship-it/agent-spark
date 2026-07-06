"""
Inspiration · Optional Web Search Integration
==============================================
Integrates with search APIs to automate Step 2 (Web Pain Mining).

Install: pip install inspiration-filter[search]
or:      pip install httpx

Usage:
    from agent_spark.search.searcher import search_pain_points
    results = search_pain_points("pet supplies")
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

# ── Optional dependency ──
try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


@dataclass
class SearchResult:
    """A single search result item."""
    source: str
    title: str
    content: str
    url: str = ""


@dataclass
class SearchResults:
    """Structured search results across 4 dimensions."""
    pain_points: list[SearchResult] = field(default_factory=list)
    product_flaws: list[SearchResult] = field(default_factory=list)
    market_gaps: list[SearchResult] = field(default_factory=list)
    niche_needs: list[SearchResult] = field(default_factory=list)


# ── Search Templates ──

SEARCH_TEMPLATES = {
    "pain_points": [
        "site:reddit.com {domain} frustrating OR annoying OR worst",
        "site:zhihu.com {domain} 痛点 OR 吐槽 OR 问题",
    ],
    "product_flaws": [
        "{domain} review problems OR complaints OR issues",
        "{domain} 差评 OR 缺点 OR 测评",
    ],
    "market_gaps": [
        '"{domain}" "wish there was" OR "why isn\'t there"',
        "{domain} alternative OR underserved OR looking for",
    ],
    "niche_needs": [
        "{domain} for elderly OR disabled OR low-income",
        "{domain} 小众 OR 特殊场景 OR 需求",
    ],
}


def search_pain_points(
    domain: str,
    api_key: str | None = None,
    provider: str = "tavily",
    max_results: int = 5,
) -> SearchResults:
    """Search the web for pain points, flaws, gaps, and niche needs.
    
    Args:
        domain: The domain to search (e.g. "pet supplies")
        api_key: API key. Falls back to env vars TAVILY_API_KEY or SERPAPI_KEY.
        provider: "tavily" or "serpapi"
        max_results: Max results per query
    
    Returns:
        Structured SearchResults grouped by dimension.
    """
    if not HAS_HTTPX:
        raise ImportError(
            "httpx is required for search. Install: pip install inspiration-filter[search]"
        )

    api_key = api_key or os.environ.get("TAVILY_API_KEY") or os.environ.get("SERPAPI_KEY")
    if not api_key:
        raise ValueError(
            "No API key found. Set TAVILY_API_KEY or SERPAPI_KEY env var, "
            "or pass api_key directly."
        )

    results = SearchResults()

    for dim_name, templates in SEARCH_TEMPLATES.items():
        dim_results: list[SearchResult] = []
        for template in templates:
            query = template.format(domain=domain)
            try:
                if provider == "tavily":
                    raw = _search_tavily(query, api_key, max_results)
                else:
                    raw = _search_serpapi(query, api_key, max_results)

                for item in raw:
                    dim_results.append(SearchResult(
                        source=item.get("source", ""),
                        title=item.get("title", ""),
                        content=item.get("content", item.get("snippet", "")),
                        url=item.get("url", ""),
                    ))
            except Exception as e:
                # Log but don't crash — search is best-effort
                import warnings
                warnings.warn(f"Search failed for '{query}': {e}")

        setattr(results, dim_name, dim_results)

    return results


def _search_tavily(query: str, api_key: str, max_results: int) -> list[dict[str, Any]]:
    """Search via Tavily API (https://tavily.com)."""
    resp = httpx.post(
        "https://api.tavily.com/search",
        json={"api_key": api_key, "query": query, "max_results": max_results},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", [])


def _search_serpapi(query: str, api_key: str, max_results: int) -> list[dict[str, Any]]:
    """Search via SerpAPI (https://serpapi.com)."""
    resp = httpx.get(
        "https://serpapi.com/search",
        params={"q": query, "api_key": api_key, "num": max_results},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("organic_results", [])


def results_to_evidence_list(results: SearchResults) -> list[str]:
    """Convert SearchResults to the list-of-strings format expected by the filter engine."""
    evidence = []
    for dim_name in ["pain_points", "product_flaws", "market_gaps", "niche_needs"]:
        for r in getattr(results, dim_name):
            evidence.append(f"{r.content} ({r.source})")
    return evidence


if __name__ == "__main__":
    # Demo: print search templates for manual use
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Domain to search")
    parser.add_argument("--api-key", help="Tavily or SerpAPI key")
    parser.add_argument("--provider", default="tavily", choices=["tavily", "serpapi"])
    args = parser.parse_args()

    if args.api_key:
        results = search_pain_points(args.domain, args.api_key, args.provider)
        evidence = results_to_evidence_list(results)
        print(json.dumps(evidence, ensure_ascii=False, indent=2))
    else:
        # Just print templates
        print(f"Search templates for '{args.domain}':\n")
        for dim, templates in SEARCH_TEMPLATES.items():
            print(f"  [{dim}]")
            for t in templates:
                print(f"    {t.format(domain=args.domain)}")
            print()
        print("To run actual search: pass --api-key")

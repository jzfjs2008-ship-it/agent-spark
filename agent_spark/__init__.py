#!/usr/bin/env python3
"""
Agent Spark — Industrial creative-idea pipeline for AI Agents.

Usage:
    from agent_spark import Filter, find_domain, list_domains

    # Quick start: use a preset domain
    domain = find_domain("pet supplies")
    result = Filter.run(domain.ideas, domain.pain_points, domain.evidence)

    # Or build your own
    from agent_spark.filter.five_layer_filter import five_layer_filter
    result = five_layer_filter(my_ideas, my_pain_points, my_evidence)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_PRESETS_PATH = Path(__file__).resolve().parent / "presets" / "domains.json"


@dataclass
class DomainPreset:
    """A pre-scanned domain with pain points and evidence."""
    domain: str
    domain_zh: str = ""
    pain_points: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    ideas: list[dict[str, Any]] = field(default_factory=list)


def list_domains() -> list[str]:
    """Return all available preset domain names."""
    presets = _load_presets()
    return [p.domain for p in presets]


def find_domain(query: str, lang: str = "en") -> DomainPreset | None:
    """Find the closest matching domain preset.
    
    Args:
        query: Domain name or fragment (e.g. "pet", "家居").
        lang: "en" matches English names, "zh" matches Chinese names.
    
    Returns:
        DomainPreset or None if no match.
    """
    query = query.lower().strip()
    presets = _load_presets()
    
    for p in presets:
        if lang == "zh" and query in p.domain_zh.lower():
            return p
        if query in p.domain.lower():
            return p
    
    return None


class Filter:
    """Convenience wrapper around the 5-layer filter engine."""
    
    @staticmethod
    def run(
        ideas: list[dict[str, Any]],
        pain_points: list[str] | None = None,
        evidence: list[str] | None = None,
        locale: str | None = None,
    ) -> list[dict[str, Any]]:
        """Run the 5-layer filter on ideas.
        
        Shortcut for: five_layer_filter(ideas, pain_points, evidence, locale=locale)
        """
        from agent_spark.filter.five_layer_filter import five_layer_filter
        return five_layer_filter(ideas, pain_points, evidence, locale=locale)


def _load_presets() -> list[DomainPreset]:
    """Load presets from JSON. Returns empty list on any error."""
    try:
        data = json.loads(_PRESETS_PATH.read_text("utf-8"))
        return [DomainPreset(**p) for p in data]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []


# ── Lazy preset preload ──
def _build_default_ideas(domain: str, pain_points: list[str]) -> list[dict[str, Any]]:
    """Build a minimal idea stub for the preset domain."""
    title = domain.title().replace("_", " ")
    return [
        {
            "title": title,
            "one_line": f"Creative solution for {title}",
            "target_user": "Target users",
            "core_value": f"Solves core pain points in {title}",
            "pain_point_solved": pain_points[0] if pain_points else "",
            "web_evidence_summary": "Pre-scanned evidence available.",
            "feasibility_score": 3,
            "novelty_score": 3,
            "tags": [domain.replace(" ", "-")],
        }
    ]

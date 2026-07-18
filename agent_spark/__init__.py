#!/usr/bin/env python3
"""
Agent Spark — Industrial creative-idea pipeline for AI Agents.

Primary entry:
    from agent_spark import spark_ideate
    results = spark_ideate("pet supplies", llm=my_fn)

Fallback (no LLM):
    from agent_spark import find_domain, Filter
    d = find_domain("pet supplies")
    Filter.run(d.ideas, d.pain_points, d.evidence)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from agent_spark.spark_ideate import spark_ideate
from agent_spark.generator import generate_ideas

_PRESETS_PATH = Path(__file__).resolve().parent / "presets" / "domains.json"


@dataclass
class DomainPreset:
    domain: str
    domain_zh: str = ""
    pain_points: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    ideas: list[dict[str, Any]] = field(default_factory=list)


def list_domains() -> list[str]:
    presets = _load_presets()
    return [p.domain for p in presets]


def find_domain(query: str, lang: str = "en") -> DomainPreset | None:
    query = query.lower().strip()
    presets = _load_presets()
    for p in presets:
        if lang == "zh" and query in p.domain_zh.lower():
            return p
        if query in p.domain.lower():
            return p
    return None


class Filter:
    @staticmethod
    def run(
        ideas: list[dict[str, Any]],
        pain_points: list[str] | None = None,
        evidence: list[str] | None = None,
        locale: str | None = None,
    ) -> list[dict[str, Any]]:
        from agent_spark.filter.five_layer_filter import five_layer_filter
        return five_layer_filter(ideas, pain_points, evidence, locale=locale)


def _load_presets() -> list[DomainPreset]:
    try:
        data = json.loads(_PRESETS_PATH.read_text("utf-8"))
        return [DomainPreset(**p) for p in data]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []

# Agent Spark — Agent Instructions

This file is recognized by **Claude Code**, **Codex CLI**, and compatible AI coding agents.
It describes the `agent-spark` project: an Agent-native creative idea engine.

## Quick Start

```python
from agent_spark import find_domain, Filter
domain = find_domain("pet supplies")
result = Filter.run(domain.ideas, domain.pain_points, domain.evidence)
```

## Core API

### `find_domain(query: str) -> DomainPreset | None`
Match a preset domain by name or fragment.

### `Filter.run(ideas, pain_points, evidence, locale=None) -> list[dict]`
Run the 5-layer convergence filter.

### `list_domains() -> list[str]`
Return all 20 preset domain names.

## REST API (optional)

```bash
pip install agent-spark[api]
uvicorn agent_spark.api:get_app --port 8080
```

## Locale

All user-facing output auto-detects language from input.
- Input contains Chinese characters → `locale="zh"`
- Otherwise → `locale="en"`

Force: `Filter.run(ideas, pain_points, evidence, locale="zh")`

## Architecture

```
AGENTS.md ← this file (Claude Code + Codex + compatible agents)
├── integrations/
│   ├── hermes/SKILL.md
│   ├── claude-code/
│   ├── codex/
│   └── openclaw/
├── agent_spark/       ← Python package (zero deps)
└── app/               ← Streamlit playground (optional)
```

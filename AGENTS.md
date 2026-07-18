# Agent Spark — Agent Instructions

This file is recognized by **Claude Code**, **Codex CLI**, and compatible AI coding agents.
It describes the `agent-spark` project: an **LLM-powered idea engine** with local rule-based convergence.

[中文文档 → README_zh.md](README_zh.md)

---

## ⚡ Single Call — The Only API You Need

```python
from agent_spark import spark_ideate

results = spark_ideate(
    domain="pet supplies",
    llm=lambda prompt, system, model: my_llm_call(prompt, system),  # pass your LLM
)

for r in results:
    print(f"{r['title']} — {r['one_line']}")
    print(f"  Feasibility: {r['feasibility_score']}/5  Novelty: {r['novelty_score']}/5")
```

**What happens inside one call:**
1. Load pre-scanned pain points for the domain (from 20-domain preset library)
2. Call your LLM with the diverge prompt template → 6+ creative ideas
3. Run the 5-layer local filter (L1 fact / L2 logic / L3 feasibility / L4 market / L5 value)
4. Return only passed ideas, with scores

**No API key needed if you pass your own LLM callable.** Just set `OPENAI_API_KEY` for auto HTTP mode.

---

## Full API Reference

| Function | Use Case |
|----------|----------|
| `spark_ideate(domain, llm=...)` | **Primary entry** — LLM diverge + local converge |
| `generate_ideas(domain, llm=...)` | Lower-level, more control over intermediate steps |
| `find_domain("pet supplies")` | Look up pre-scanned pain points |
| `Filter.run(ideas, pain_points, evidence)` | Run filter manually on your own ideas |
| `list_domains()` | List all 20 preset domain names |

---

## REST API (optional)

```bash
pip install agent-spark[api]
uvicorn agent_spark.api:get_app --port 8080
```

Endpoints: `POST /filter` | `GET /domains` | `GET /health`

---

## Locale

Auto-detects EN/ZH from input. Force with `locale="zh"` or `locale="en"`.

---

## Architecture

```
AGENTS.md          ← you are here (Claude Code + Codex auto-load)
├── agent_spark/   ← Python package
│   ├── spark_ideate.py    ← ⚡ primary entry
│   ├── generator.py       ← LLM diverge + parse
│   ├── filter/            ← 5-layer convergence engine
│   ├── audit/             ← 36-point structured audit
│   ├── presets/           ← 20 domain presets
│   ├── locale.py          ← EN/ZH auto-detect
│   ├── cli.py             ← CLI tool
│   └── api.py             ← FastAPI (optional)
└── integrations/  ← Hermes, OpenClaw, Claude Code, Codex
```

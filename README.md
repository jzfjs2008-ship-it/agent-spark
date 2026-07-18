<div align="center">
  <h1>⚡ Agent Spark</h1>
  <p><strong>LLM-Powered Creative Idea Engine with Local Rule-Based Convergence</strong></p>
  <p><em>One call: `spark_ideate("pet supplies")` → your LLM diverges → 5-layer filter converges → structured output.</em></p>

  <p>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">
      <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
    </a>
    <img src="https://img.shields.io/badge/domains-20-ff69b4" alt="20 domains">
    <img src="https://img.shields.io/badge/version-0.9.0--beta-yellow" alt="v0.9.0-beta">
    <a href="README_zh.md">
      <img src="https://img.shields.io/badge/中文文档-blueviolet" alt="中文文档">
    </a>
  </p>

  <sub>
    ⚡ <b>NOT</b> Apache Spark · <b>NOT</b> GitHub Spark — this is an <b>idea engine</b> for AI Agents.<br>
    Works with: Claude Code · Codex CLI · Hermes Agent · OpenClaw<br>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">Star us on GitHub</a>
  </sub>
</div>

---

## ⚠️ Not Apache Spark / GitHub Spark

This project has no relation to **Apache Spark** (big data engine) or **GitHub Spark** (low-code platform).

---

## ⚡ The Only Function You Need

```python
from agent_spark import spark_ideate

results = spark_ideate(
    domain="pet supplies",
    llm=lambda prompt, system, model: my_llm_call(prompt, system),
)

for r in results:
    print(f"{r['title']} — {r['one_line']}")
    print(f"  Feasibility: {r['feasibility_score']}/5  Novelty: {r['novelty_score']}/5")
```

**One call, three steps:**
1. **Load presets** — 20 domains with pre-scanned pain points auto-detected
2. **LLM diverges** — your model generates 6+ ideas from the domain + pain points
3. **Local filter converges** — 5-layer rule engine drops hallucinated, buzzword-heavy, or market-duplicate ideas

No API key needed if you pass your own LLM. Just set `OPENAI_API_KEY` for auto HTTP mode.

---

## 🔥 Why This Is Different

| Other AI idea tools | Agent Spark |
|---------------------|-------------|
| LLM prompt → raw text, you filter manually | **5-layer filter runs automatically** after LLM |
| Pure LLM — no validation | **L1 fact check**, L4 market duplicate detection |
| Every idea passes through | Buzzword, vague, and hallucinated ideas **dropped before you see them** |
| One prompt for all | **20 domain presets** enrich the LLM with real pain points |

**The key insight:** LLMs diverge (generate many ideas). Local rules converge (find the few that are real). Agent Spark does both.

---

## 🎯 How It Works

```
Your LLM                        Agent Spark
────────────                    ─────────────
  |                                |
  |  generate_ideas()              |
  |───────────────────────────────▶│
  |   (system=diverge_prompt       │
  |    user=domain+pain_points)    │
  │                                │
  │  JSON ideas returned           │
  │◀───────────────────────────────│
  │                                │
  │                         five_layer_filter()
  │                         L1: fact validation
  │                         L2: logic consistency
  │                         L3: technical feasibility
  │                         L4: market duplicate check
  │                         L5: buzzword / value check
  │                                │
  │  Pass results returned         │
  │◀───────────────────────────────│
```

---

## 🤖 Agent Platform Support

| Platform | Integration | How It Works |
|----------|------------|-------------|
| **Claude Code** | Auto-loads [`AGENTS.md`](AGENTS.md) | `from agent_spark import spark_ideate` |
| **Codex CLI** | Auto-loads [`AGENTS.md`](AGENTS.md) | Same import |
| **Hermes Agent** | [`integrations/hermes/SKILL.md`](integrations/hermes/SKILL.md) | Skill triggers full 6-round interview |
| **OpenClaw** | [`integrations/openclaw/`](integrations/openclaw/) | Plugin panel with wizard UI |

---

## 📦 Install

```bash
pip install git+https://github.com/jzfjs2008-ship-it/agent-spark.git
```

Core engine: stdlib only. LLM client uses stdlib `urllib`. Optional REST API adds FastAPI + uvicorn + pydantic.

---

## 📋 API Reference

| Function | What It Does |
|----------|-------------|
| `spark_ideate(domain, llm=...)` | **Primary.** LLM diverge + local converge in one call |
| `generate_ideas(domain, llm=...)` | Lower-level, more control |
| `find_domain("pet supplies")` | Look up 7 pre-scanned pain points |
| `Filter.run(ideas, ...)` | Run filter manually |
| `list_domains()` | All 20 preset domain names |

---

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

21 tests covering filter engine, LLM response parsing, preset integrity, and convenience API.

---

## 🌐 Ecosystem

| Tool | Purpose |
|------|---------|
| **Crush Your Passion** | Project risk assessment |
| **KillAI-WinCleaner** | AI environment cleanup |

**Workflow:** Agent Spark generates ideas → Crush Your Passion evaluates → KillAI-WinCleaner resets.

---

## 🤝 Contributing

Add new domains to `agent_spark/presets/domains.json`. Every added domain enriches the LLM's pain-point context for all users.

See [CONTRIBUTING.md](CONTRIBUTING.md) and open issues via [domain suggestion template](.github/ISSUE_TEMPLATE/domain_suggestion.md).

---

## ❓ FAQ

**Q: Is this the same as Apache Spark?**  
A: No. Apache Spark is a big data engine. This is an idea engine for AI coding agents.

**Q: Does it work without an LLM?**  
A: Yes — `find_domain("pet supplies")` + `Filter.run()` works offline with pre-scanned pain points. But the full power is with an LLM.

**Q: What does "zero dependencies" mean?**  
A: The core filter engine uses only Python stdlib. The LLM client also uses stdlib `urllib` (no OpenAI SDK needed).

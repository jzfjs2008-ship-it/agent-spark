<div align="center">
  <h1>⚡ Agent Spark</h1>
  <p><strong>Offline Creative Idea Convergence Engine for AI Agents</strong></p>
  <p><em>Built-in 20-domain pain-point knowledge base + 5-layer local rule filter — no LLM chain required.</em></p>

  <p>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">
      <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
    </a>
    <img src="https://img.shields.io/badge/domains-20-ff69b4" alt="20 domains">
    <img src="https://img.shields.io/badge/version-0.9.0--beta-yellow" alt="v0.9.0-beta">
  </p>

  <sub>
    ⚡ <b>NOT</b> Apache Spark · <b>NOT</b> GitHub Spark — this is an <b>offline creative idea engine</b> for CLI AI Agents.<br>
    Works with: Claude Code · Codex CLI · Hermes Agent · OpenClaw<br>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">Star us on GitHub</a>
  </sub>
</div>

---

## ⚠️ Not Apache Spark / GitHub Spark

This project has no relation to **Apache Spark** (big data engine) or **GitHub Spark** (low-code platform). It is an **offline creative idea convergence engine** for CLI-based AI coding agents.

---

## 🔥 What Makes This Different

| Other AI idea tools | Agent Spark |
|---------------------|-------------|
| LLM prompt → raw text output | **Local 5-layer rule filter** decides pass/fail |
| Pure LLM chain (every run costs tokens) | **Pure offline mode** = zero token cost |
| No validation — hallucinated ideas pass through | **Fact validation (L1)**, logic check (L2), market duplicate (L4) |
| One-size-fits-all prompt | **20 preset domains** with pre-scanned real pain points |
| No audit | **36-point structured project audit** |

**The core differentiator:** Agent Spark is NOT a prompt wrapper. It's a **rule-based convergence engine** with an optional LLM layer for cold domains. The final decision is always made locally.

---

## 🎯 Dual Mode

```
                    ┌─ Pure Offline (zero token cost) ─────────────────────┐
                    │  20 preset domains → 7 pain points each               │
User: "pet"  ──────▶  5-layer filter → structured result                    │
                    │  No API key needed. Works offline.                    │
                    └───────────────────────────────────────────────────────┘

                    ┌─ LLM-Enhanced (cold domain supplement) ───────────────┐
                    │  User domain → LLM generates ideas (gpt-4o-mini)      │
User: "pet"  ──────▶  5-layer local filter CONVERGES the results            │
                    │  LLM is data source only. Final check = local rules.  │
                    └───────────────────────────────────────────────────────┘
```

---

## 🤖 Platform Support

| Platform | Integration | Quick Start |
|----------|------------|-------------|
| **Claude Code** | Auto-loads [`AGENTS.md`](AGENTS.md) | `pip install git+https://...` then use `import` |
| **Codex CLI** | Auto-loads [`AGENTS.md`](AGENTS.md) | Same as above |
| **Hermes Agent** | [`integrations/hermes/SKILL.md`](integrations/hermes/SKILL.md) | Copy SKILL.md to `$HERMES_HOME/skills/` |
| **OpenClaw** | [`integrations/openclaw/`](integrations/openclaw/) | Add plugin via manifest.json |

---

## 🚀 Quick Start

### Pure offline (no API key, no internet)

```python
from agent_spark import find_domain, Filter

# 30 seconds — uses pre-scanned pain points
d = find_domain("pet supplies")
result = Filter.run(d.ideas, d.pain_points, d.evidence)
```

### LLM-enhanced (for cold / niche domains)

```python
from agent_spark import generate_ideas

# Agent passes its own LLM callable
ideas = generate_ideas("pet supplies", llm=my_fn)

# Or set OPENAI_API_KEY env var
# export OPENAI_API_KEY=sk-...
ideas = generate_ideas("marine biology equipment")
```

---

## 📦 Install

```bash
# From GitHub (zero external Python deps for filter engine)
pip install git+https://github.com/jzfjs2008-ship-it/agent-spark.git

# With optional REST API
pip install "agent-spark[api] @ git+https://github.com/jzfjs2008-ship-it/agent-spark.git"
```

Core filter engine: **zero third-party Python packages**. Stdlib only. bge-small-zh vector model and LLM client are optional add-ons.

---

## 🧪 Comparison: Raw Prompt vs Agent Spark

**Input:** "Smart home security"

| Raw LLM prompt | Agent Spark (offline) |
|---------------|----------------------|
| "AI-powered security camera" | ❌ [L1] Vague pain — no evidence |
| "Blockchain door lock" | ❌ [L5] Buzzword overload |
| "Pet cam with treat dispenser" | ❌ [L4] Already exists (market duplicate) |
| "Privacy-first camera for renters with rental agreement compliance" | ✅ Passes all 5 layers |

The difference: Agent Spark catches hallucinated (L1), buzzword-heavy (L5), and market-duplicate (L4) ideas **before** you waste time prototyping.

---

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

21 tests covering filter engine, LLM parsing, preset integrity, and convenience API.

---

## 🌐 Ecosystem

| Related Tool | Purpose | Link |
|-------------|---------|------|
| **Crush Your Passion** | Project risk assessment | [GitHub](https://github.com/jzfjs2008-ship-it/crush-your-passion) |
| **KillAI-WinCleaner** | AI environment cleanup | [GitHub](https://github.com/jzfjs2008-ship-it/KillAI-WinCleaner) |

**Workflow:** Agent Spark generates ideas → Crush Your Passion evaluates risk → KillAI-WinCleaner resets for next project.

---

## 🤝 Contributing

Help expand the domain pain-point library!

- **Open an Issue** with a domain suggestion and 5+ real pain points
- **Submit a PR** adding entries to `agent_spark/presets/domains.json`
- Every domain added benefits all users — this is a community knowledge base

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 🏗️ Project Structure

```
AGENTS.md                     ← Claude Code + Codex CLI auto-load
integrations/
├── hermes/SKILL.md           ← Hermes Agent skill
├── claude-code/              ← Bridge script
├── codex/                    ← Codex reference
└── openclaw/                 ← Plugin panel
agent_spark/                  ← Python package
├── filter/                   ← 5-layer convergence filter (core)
├── audit/                    ← 36-point structured project audit
├── presets/                  ← 20 domain presets (community-extensible)
├── generator.py              ← LLM integration (optional)
├── locale.py                 ← Auto-detect EN/ZH
└── api.py                    ← FastAPI REST API (optional)
```

## ❓ FAQ

**Q: Is this the same as Apache Spark?**  
A: No. Apache Spark is a big data engine. This is an offline creative idea engine for AI coding agents.

**Q: Does it work offline?**  
A: Yes. Pure offline mode needs zero API calls. LLM-enhanced mode is optional.

**Q: What counts as "zero dependencies"?**  
A: The core filter engine and audit module use only Python stdlib — no third-party packages required. The optional LLM client uses `urllib` (also stdlib). The optional REST API adds FastAPI + uvicorn + pydantic.

<div align="center">
  <h1>⚡ Agent Spark</h1>
  <p><strong>The Creative Engine for AI Agents</strong></p>
  <p><em>An Agent-native creative idea engine. Say "give me ideas" and let your Agent do the rest.</em></p>

  <p>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">
      <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
    </a>
    <img src="https://img.shields.io/badge/dependencies-0-brightgreen" alt="Zero deps">
    <img src="https://img.shields.io/badge/domains-20-ff69b4" alt="20 domains">
  </p>

  <sub>
    ⚡ <b>Agent Spark</b> — works with Claude Code / Codex CLI / Hermes Agent / OpenClaw.<br>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">Star us on GitHub</a>
  </sub>
</div>

---

## ⚡ What It Is

**Agent Spark is a skill for AI Agents** — install it once, and your Agent can generate market-verified creative ideas without leaving the conversation.

- **20 preset domains** with pre-scanned pain points — say "pet supplies", get 7 real pains
- **Zero external dependencies** — works in any Python 3.10+ environment
- **Bilingual auto-detect** — English or Chinese input
- **Optional REST API** — `pip install agent-spark[api]`

## 🤖 Platform Support

| Platform | File | What it does |
|----------|------|-------------|
| **Claude Code** + **Codex CLI** | [`AGENTS.md`](AGENTS.md) | Auto-loaded at project root — both agents recognize it |
| **Hermes Agent** | [`integrations/hermes/SKILL.md`](integrations/hermes/SKILL.md) | Full Hermes skill with trigger phrases |
| **OpenClaw** | [`integrations/openclaw/`](integrations/openclaw/) | Plugin panel with 6-round wizard |

## 🚀 Quick Start

```python
from agent_spark import find_domain, Filter

# 30 seconds, no API key, no internet
d = find_domain("pet supplies")
result = Filter.run(d.ideas, d.pain_points, d.evidence)
```

Or via CLI:

```bash
pip install git+https://github.com/jzfjs2008-ship-it/agent-spark.git
agent-spark-demo         # See the filter in action
agent-spark-pipeline     # Full interview → filter pipeline
echo '{"ideas": [...]}' | agent-spark-filter  # Filter JSON
```

## 🌐 Language Detection

Auto-detected from user input. No config needed.

```python
from agent_spark.locale import detect, _

detect("pet supplies")           # "en"
detect("宠物用品")               # "zh"
_("Domain", "领域", "zh")        # "领域"
_("Domain", "领域", "en")        # "Domain"
```

Force locale: `Filter.run(ideas, pains, evidence, locale="zh")`

## 📦 Install

```bash
pip install git+https://github.com/jzfjs2008-ship-it/agent-spark.git
# With REST API:
pip install "agent-spark[api] @ git+https://github.com/jzfjs2008-ship-it/agent-spark.git"
```

## 🏗️ Project Structure

```
AGENTS.md                     ← Claude Code + Codex CLI auto-load
integrations/
├── hermes/SKILL.md           ← Hermes Agent skill
├── claude-code/              ← Bridge script
├── codex/                    ← Codex reference
└── openclaw/                 ← Plugin panel
agent_spark/                  ← Python package (zero deps)
├── filter/                   ← 5-layer convergence filter
├── audit/                    ← Structured project audit
├── presets/                  ← 20 domain presets
├── locale.py                 ← Language detection
└── api.py                    ← Optional FastAPI
```

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## ❓ FAQ

**Q: Why isn't this on PyPI?**  
A: The project is iterating fast. `pip install git+https://` is standard for early-stage projects.

**Q: Does it work offline?**  
A: Yes. Zero external dependencies.

**Q: What if my domain isn't in the presets?**  
A: The filter engine works on any domain. The 20 presets are starting points — use `find_domain()` with partial matches, or pass custom ideas directly to `Filter.run()`.

<div align="center">
  <h1>⚡ Agent Spark</h1>
  <p><strong>The Creative Engine for AI Agents</strong></p>

  <p>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">
      <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
    </a>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark/actions">
      <img src="https://img.shields.io/github/actions/workflow/status/jzfjs2008-ship-it/agent-spark/test.yml?branch=main&label=CI" alt="CI">
    </a>
    <img src="https://img.shields.io/badge/agent-ready-purple" alt="Agent Ready">
    <img src="https://img.shields.io/badge/zero-deps-orange" alt="Zero Deps">
  </p>

  <p>
    <a href="#-quick-start"><b>Quick Start</b></a> •
    <a href="#-pipeline"><b>Pipeline</b></a> •
    <a href="#-for-ai-agents"><b>For AI Agents</b></a> •
    <a href="#-features-vs-alternatives"><b>vs Alternatives</b></a>
  </p>
</div>

---

## 🧠 The Problem

> **You're building an AI Agent, but:**
>
> ❌ When the user says "give me ideas" — your agent has no structured way to do it.
>
> ❌ Raw LLM output is full of hallucinations and buzzword salad.
>
> ❌ You can't validate whether an idea is grounded in real market needs.
>
> ❌ Every agent needs to reinvent this wheel.

**Agent Spark** is the off-the-shelf creative engine your AI Agent needs.

## ⚡ What It Is

Agent Spark is a **Python skill for AI Agents** — a structured creative-idea pipeline that fits inside any Agent's tool belt:

- **20 preset domains** with pre-scanned pain points — say "pet supplies", get 7 real pains
- **Zero external dependencies** — just Python 3.10+
- **Bilingual auto-detect** — English or Chinese input, both work
- **Optional REST API** — `pip install agent-spark[api]`

```
Agent interacts with user (5 rounds + intent anchor)
    ↓
Agent searches the web for real pain points
    ↓
Agent diverges with LLM across 6 dimensions
    ↓
Agent converges with 5-layer rule-based filter
    ↓
Agent audits the final project plan
    ↓
Agent presents polished, grounded ideas
```

**For Claude Code / Cursor / Hermes Agent / OpenClaw / any AI coding agent.**

## 🤖 For AI Agents

### As a Python tool (recommended)

```python
from agent_spark.filter.five_layer_filter import five_layer_filter

# Your agent collected these from the user interview
ideas = [
    {
        "title": "Anti-Jam Pet Feeder",
        "one_line": "Solve feeder jams with redesigned auger",
        "target_user": "Pet owners",
        "core_value": "Eliminate the #1 feeder complaint",
        "pain_point_solved": "Automatic feeders jam because of moisture-clumped kibble",
        "web_evidence_summary": "Amazon reviews: jams every 3 days",
        "feasibility_score": 4,
        "novelty_score": 3,
        "tags": ["pet", "hardware"],
    },
    {
        "title": "Blockchain Shelf",
        "one_line": "Decentralize home organization",
        "target_user": "Everyone",
        "core_value": "Empower ecosystem",
        "pain_point_solved": "Efficiency",
        "web_evidence_summary": "",
        "feasibility_score": 1,
        "novelty_score": 5,
        "tags": ["blockchain"],
    },
]

# Agent runs the filter
passed = five_layer_filter(
    ideas,
    user_pain_points=["Feeders jam constantly", "Shelves don't fit"],
    web_evidence_list=["Amazon feeder 1-star reviews"],
)

# Agent knows: Blockchain Shelf → L1 hallucination. Pet Feeder → passes.
```

### As a CLI tool

```bash
pip install agent-spark
echo '{"ideas": [...]}' | agent-spark-filter    # filter ideas
cat plan.md | agent-spark-audit                  # audit a project plan
agent-spark-demo                                 # see it in action
agent-spark-pipeline                             # run the full interview pipeline
```

### As a Hermes / Claude Code Skill

| Platform | Integration | Location |
|----------|------------|----------|
| **Hermes Agent** | Native SKILL.md | `integrations/hermes/SKILL.md` |
| **Claude Code** | Bridge script | `integrations/claude-code/agent_spark_bridge.sh` |
| **OpenClaw** | Plugin | `integrations/openclaw/` |

---

## 🚀 Quick Start

**30 seconds — no API key, no internet:**

```python
from agent_spark import find_domain, Filter

# Find a preset domain with pre-scanned pain points
d = find_domain("pet supplies")
print(f"{d.domain}: {len(d.pain_points)} pain points")

# Run the 5-layer filter
result = Filter.run(d.ideas, d.pain_points, d.evidence)
print(f"Passed: {len(result)}/{len(d.ideas)}")
```

**Or via CLI:**
```bash
pip install agent-spark
agent-spark-demo
agent-spark-pipeline
echo '{"ideas": [...]}' | agent-spark-filter
```

---

## 🏗️ Advanced Usage

### Step 1 · 5-Round Agent Interview + Intent Anchor

Your agent asks one question at a time:

| # | Question |
|---|----------|
| 1 | What domain needs ideas? |
| 1.5 | **Intent Anchor** — paraphrase understanding, confirm before continuing |
| 2 | What frustrates you there? |
| 3 | What existing products have flaws? |
| 4 | A) Incremental or B) Novel? |
| 5 | Any niche needs? |

### Step 2 · Web Pain Mining

Agent searches 4 dimensions with real search queries.

### Step 3 · Material Merge

Structured concatenation.

### Step 4 · 6-Dimension AI Divergence

The LLM generates ideas across 6 distinct (non-overlapping) creativity dimensions.

### Step 5 · 5-Layer Convergence Filter ⭐

| Layer | What it kills | Method |
|-------|--------------|--------|
| **L1** Fact | Hallucinations | Bigram fuzzy matching + evidence quality |
| **L2** Logic | Self-contradictions | Conflict detection (free+paid, simple+powerful) |
| **L3** Feasibility | Too expensive | Weighted signal scoring (not hard-keyword) |
| **L4** Market | Duplicates | Token-weighted keyword matching |
| **L5** Value | Buzzword salad | Density analysis + pattern detection |

### Step 6 · Preview → Step 7 · Refine → Step 8 · Audit

Audit (New in v0.99) checks for logic, structure, entity, and technical errors.

---

## 📊 Features vs Alternatives

| Feature | Agent Spark | ChatGPT "give me ideas" | Brainstorming Apps |
|---------|:-----------:|:----------------------:|:------------------:|
| Grounded in real web data | ✅ | ❌ | ❌ |
| Multi-layer quality filter | ✅ L1-L5 | ❌ | ❌ |
| Works offline (filter) | ✅ | ❌ | ❌ |
| Structured divergence | ✅ 6 dims | ❌ | ❌ |
| Built for AI Agents | ✅ | ❌ | ❌ |
| Project plan audit | ✅ | ❌ | ❌ |
| Zero deps | ✅ | N/A | N/A |
| Bilingual (EN/ZH) | ✅ | ❌ | ❌ |

---

## 📦 Install

```bash
pip install agent-spark
```

Or from source:

```bash
git clone https://github.com/jzfjs2008-ship-it/agent-spark.git
cd agent-spark
pip install -e ".[dev]"
pytest tests/ -v
```

---

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v --tb=short
```

---

## 🔌 Integrations

```
agent-spark/
├── agent_spark/           # Python package
│   ├── filter/            # 5-layer convergence filter
│   ├── prompts/           # Divergence & refinement templates
│   ├── questions/         # 5-round interview system + intent anchor (v2.1)
│   ├── search/            # Optional web search (pip install .[search])
│   ├── audit/             # Structured project audit (NEW)
│   └── data/              # Configurable product/buzzword rules
├── integrations/
│   ├── hermes/            # Hermes Agent skill
│   ├── openclaw/          # OpenClaw plugin
│   └── claude-code/       # Claude Code bridge script
├── app/
│   └── playground.py      # Streamlit UI
└── docs/
    ├── security-annex.md  # Security architecture template
    └── interagent-audit-report.md
```

---

## 🤝 Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md).

Ideas for contributions:
- Add more products to the filter's database
- Build a VS Code extension
- Translate prompts to more languages
- Add a Tavily/SerpAPI search backend

---

## 📜 License

MIT © [Nous Research](https://nousresearch.com).

---

<div align="center">
  <sub>
    ⚡ <b>Agent Spark</b> — the creative engine for AI Agents.<br>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">Star us on GitHub</a>
  </sub>

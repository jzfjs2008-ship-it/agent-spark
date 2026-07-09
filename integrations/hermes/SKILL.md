---
description: "Trigger: '给我灵感' / '给我创意' / 'give me ideas' / 'I need inspiration for [domain]'. Runs the full 6-round interview + AI divergence + 5-layer filter + audit pipeline. Bilingual (auto-detects EN/ZH from user input)."
version: 2.1.0
author: Agent Spark
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    related_skills: [spike, plan, humanizer]
---

```
User Interview → Web Pain Mining → AI Divergence (6 dimensions)
→ 5-Layer Convergence Filter → Audit → Export
```

Mine real needs, diverge with AI, converge with rules, audit for quality.

---

## Trigger / 触发

| English | 中文 |
|---------|------|
| "give me ideas" | "给我灵感" |
| "creative ideas for [domain]" | "我想在 XX 领域找创意" |
| "I need inspiration for [domain]" | "帮我挖一下 XX 的痛点" |

On trigger → **immediately ask Round 1** (one question at a time).

---

## Pipeline

### Step 0: Language Detection
Read the user's message. If it contains Chinese characters → `locale="zh"`, else `"en"`.
Use this locale for ALL subsequent questions and output.

### Step 1: Domain
Ask one question: "What domain needs ideas?" / "想要哪个领域的创意？"

### Step 1.5: Intent Anchor
Paraphrase the domain back. Confirm understanding before proceeding.
If user says "大模型相关github涨星项目" → separate domain (LLM tools) from metric (stars).

### Step 2: Pain Points
"What frustrates you there?" / "这个领域有哪些不方便的地方？"
Search the web for real pain points.

### Step 3: Product Flaws
"What existing products have issues?" / "哪些产品有缺点？"

### Step 4: Style
"A) Incremental or B) Novel?" / "A) 改良优化 还是 B) 全新独创？"

### Step 5: Niche
"Any niche needs?" / "有什么小众场景？"

### Step 6: Diverge → Filter
Use `from agent_spark import Filter, find_domain` to get preset pain points,
or build your own idea list and run `Filter.run()`.

### Step 7: Audit
Run `from agent_spark.audit.auditor import audit_project_plan` on winning ideas.

---

## One-Shot with Presets

If user says a domain that matches a preset ("pet supplies", "remote work tools", etc.):

```python
from agent_spark import find_domain, Filter
d = find_domain("pet supplies")
results = Filter.run(d.ideas, d.pain_points, d.evidence, locale="zh"/"en")
```

This skips Rounds 1-5 entirely.

---

## CLI Quick Reference

```bash
agent-spark-filter      # Filter ideas
agent-spark-audit       # Audit a plan
agent-spark-pipeline    # Full interactive pipeline
```

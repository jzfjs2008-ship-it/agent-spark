---
description: "Trigger: '给我灵感' / '给我创意' / 'give me ideas' / 'I need inspiration for [domain]'. One-call LLM diverge + 5-layer local filter. Bilingual auto-detect. No rounds, no CLI — just import spark_ideate()."
version: 3.0.0
author: Agent Spark
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    related_skills: []
    install: "pip install git+https://github.com/jzfjs2008-ship-it/agent-spark.git"
---

# Agent Spark — 一次调用，从领域到收敛灵感

用户说「给我 XX 领域的创意」→ 直接调用 `spark_ideate()`，一步到位。

不需要 6 轮问答，不需要 CLI，不需要配置。

## 核心调用（Agent 唯一要调的）

```python
from agent_spark import spark_ideate

results = spark_ideate(
    domain="宠物用品",
    llm=lambda prompt, system, model: your_llm_call(prompt, system),
)

for r in results:
    print(f"{r['title']}")
    print(f"  {r['one_line']}")
    print(f"  可行性 {r['feasibility_score']}/5  新颖度 {r['novelty_score']}/5")
```

**内部三步自动完成：**
1. 加载 20 领域预置痛点库（`find_domain()` 自动匹配）
2. 你的大模型根据领域 + 痛点发散 6+ 个创意
3. 本地五层规则引擎收敛（L1 事实 / L2 逻辑 / L3 落地 / L4 市场 / L5 热词）

## LLM 接入方式

### 方式一：传 callable（推荐，Agent 自带 LLM）

```python
def my_llm(prompt, system, model):
    return call_openai(prompt, system=system, model=model)

results = spark_ideate("智能家居安防", llm=my_llm)
```

### 方式二：环境变量（零配置）

```bash
export OPENAI_API_KEY=sk-...
# 或 export OPENAI_BASE_URL=http://localhost:11434/v1  # Ollama
```

```python
results = spark_ideate("marine biology equipment")  # 自动 HTTP 调用
```

### 方式三：纯离线（无需 LLM）

```python
from agent_spark import find_domain, Filter
d = find_domain("pet supplies")
results = Filter.run(d.ideas, d.pain_points, d.evidence)
```

## 触发词（中英文）

| 触发词 | 动作 |
|--------|------|
| "给我灵感" / "give me ideas" | 问「哪个领域？」→ 调 `spark_ideate()` |
| "帮我挖一下 XX 痛点" | 直接调 `find_domain()` + `Filter.run()` |
| "XX 有什么好点子" | 调 `spark_ideate(domain="...")` |

## 完整 API

| 函数 | 用途 |
|------|------|
| `spark_ideate(domain, llm=...)` | ⭐ **主入口** — LLM 发散 + 本地收敛 |
| `find_domain("宠物用品")` | 查预置痛点库 |
| `Filter.run(ideas, pain_points, evidence)` | 手动跑过滤 |
| `list_domains()` | 所有 20 个领域名 |

## 安装

```bash
pip install git+https://github.com/jzfjs2008-ship-it/agent-spark.git
```

## 输出格式

每个结果包含：

```python
{
    "title": "创意标题",
    "one_line": "一句话描述",
    "target_user": "目标用户",
    "pain_point_solved": "解决的痛点",
    "core_value": "核心价值",
    "feasibility_score": 4,    # 1-5 可行性
    "novelty_score": 3,         # 1-5 新颖度
    "tags": ["pet", "litter"],
    "index": 0,
    "layers": {                 # 各层过滤结果
        "1_fact": {"passed": True, "message": "..."},
        "2_logic": {"passed": True, "message": "..."},
        "3_feasibility": {"passed": True, "message": "..."},
        "4_market": {"passed": True, "message": "..."},
        "5_value": {"passed": True, "message": "..."},
    },
    "passed": True,
}
```

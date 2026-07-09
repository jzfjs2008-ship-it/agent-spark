<div align="center">
  <h1>⚡ Agent Spark</h1>
  <p><strong>离线创意收敛引擎 · 专为 Hermes / Claude Code / Codex CLI / OpenClaw 设计</strong></p>
  <p><em>内置 20 个行业领域痛点知识库 + 五层本地规则过滤 — 不依赖 LLM 链式推理</em></p>

  <p>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">
      <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
    </a>
    <img src="https://img.shields.io/badge/domains-20-ff69b4" alt="20 领域">
    <img src="https://img.shields.io/badge/version-0.9.0--beta-yellow" alt="v0.9.0-beta">
    <a href="README.md">
      <img src="https://img.shields.io/badge/English%20Documentation-blue" alt="English">
    </a>
  </p>

  <sub>
    ⚡ 与 **Apache Spark**（大数据引擎）和 **GitHub Spark**（低代码平台）<b>无任何关系</b> — 这是一个面向 CLI AI Agent 的<b>离线创意引擎</b>。<br>
    支持：Claude Code · Codex CLI · Hermes Agent · OpenClaw<br>
    <a href="https://github.com/jzfjs2008-ship-it/agent-spark">Star 我们</a>
  </sub>
</div>

---

## ⚠️ 这不是 Apache Spark 或 GitHub Spark

本项目与 **Apache Spark**（大数据计算引擎）和 **GitHub Spark**（低代码开发平台）没有任何关系。它是一个面向 CLI AI Agent 的**离线创意收敛引擎**。

---

## 🔥 与同类工具的核心区别

| 普通 AI 创意工具 | Agent Spark |
|-----------------|-------------|
| LLM 提示词 → 原始文本输出 | **本地五层规则过滤**决定通过/淘汰 |
| 纯 LLM 链（每次运行消耗 Token） | **纯离线模式** = 零 Token 消耗 |
| 无校验 — 幻觉创意也会通过 | **事实验证（L1）**、逻辑检查（L2）、市场重复排查（L4） |
| 一刀切的提示词 | **20 个预置领域**，每个附带真实痛点 |
| 无审计 | **36 项结构化项目审计** |

**核心差异：Agent Spark 不是提示词套壳。它是一个基于规则的收敛引擎**，可选 LLM 层只用于冷门行业数据补充，最终决策始终由本地规则完成。

---

## 🎯 双运行模式

```
                    ┌─ 纯离线模式（零 Token 消耗）─────────────────────────┐
                    │  20 个预置领域 → 每个 7 个痛点                       │
用户输入："宠物" ──────▶  五层过滤 → 结构化结果                             │
                    │  无需 API Key。完全离线运行。                        │
                    └─────────────────────────────────────────────────────┘

                    ┌─ LLM 增强模式（冷门行业补充）────────────────────────┐
                    │  用户输入 → LLM 生成创意（如 gpt-4o-mini）            │
用户输入："宠物" ──────▶  五层本地过滤引擎对结果进行收敛                     │
                    │  LLM 仅作为数据源。最终校验 = 本地规则。              │
                    └─────────────────────────────────────────────────────┘
```

---

## 🤖 支持的 AI Agent 平台

| 平台 | 集成方式 | 快速开始 |
|------|---------|---------|
| **Claude Code** | 自动加载 [`AGENTS.md`](AGENTS.md) | `pip install git+https://...` 后 `import` |
| **Codex CLI** | 自动加载 [`AGENTS.md`](AGENTS.md) | 同上 |
| **Hermes Agent** | [`integrations/hermes/SKILL.md`](integrations/hermes/SKILL.md) | 复制 SKILL.md 到 `$HERMES_HOME/skills/` |
| **OpenClaw** | [`integrations/openclaw/`](integrations/openclaw/) | 通过 manifest.json 添加插件 |

---

## 🚀 快速开始

### 纯离线（无需 API Key，无需联网）

```python
from agent_spark import find_domain, Filter

# 30 秒 — 使用预扫描的行业痛点
d = find_domain("pet supplies")
result = Filter.run(d.ideas, d.pain_points, d.evidence)
```

### LLM 增强（冷门 / 小众行业）

```python
from agent_spark import generate_ideas

# Agent 传入自己的 LLM 调用函数
ideas = generate_ideas("pet supplies", llm=my_fn)

# 或设置 OPENAI_API_KEY 环境变量
# export OPENAI_API_KEY=sk-...
ideas = generate_ideas("marine biology equipment")
```

---

## 📦 安装

```bash
# 从 GitHub 安装（过滤引擎无外部 Python 依赖）
pip install git+https://github.com/jzfjs2008-ship-it/agent-spark.git

# 安装可选 REST API
pip install "agent-spark[api] @ git+https://github.com/jzfjs2008-ship-it/agent-spark.git"
```

核心过滤引擎：**零第三方 Python 包**。仅使用标准库。LLM 客户端使用标准库 `urllib`。可选 REST API 需额外安装 FastAPI + uvicorn + pydantic。

---

## 🧪 对比：原始 LLM 提示词 vs Agent Spark 离线收敛

**输入：** "智能家居安防"

| 原始 LLM 提示词产出 | Agent Spark 离线收敛结果 |
|-------------------|------------------------|
| "AI 安防摄像头" | ❌ [L1] 痛点模糊 — 无证据支撑 |
| "区块链智能门锁" | ❌ [L5] 热词堆砌 |
| "宠物投食监控摄像头" | ❌ [L4] 市场上已存在 |
| "租屋友好的隐私保护摄像头（含租赁合同合规）" | ✅ 通过全部 5 层 |

区别在于：Agent Spark 在你浪费精力做原型**之前**，就筛掉了幻觉创意（L1）、热词堆砌（L5）和市场重复（L4）。

---

## 🧪 测试

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

21 项测试，覆盖过滤引擎、LLM 解析、预置库完整性和便捷 API。

---

## 🌐 配套工具生态

| 工具 | 用途 | 链接 |
|------|------|------|
| **Crush Your Passion** | 项目风险评估 | [GitHub](https://github.com/jzfjs2008-ship-it/crush-your-passion) |
| **KillAI-WinCleaner** | AI 环境清理 | [GitHub](https://github.com/jzfjs2008-ship-it/KillAI-WinCleaner) |

**工作流串联：** Agent Spark 产出创意 → Crush Your Passion 评估风险 → KillAI-WinCleaner 清理环境，准备下一轮。

---

## 🤝 参与贡献

帮助扩展行业痛点知识库！

- **提 Issue**：建议新行业 + 5 个以上真实痛点
- **提 PR**：向 `agent_spark/presets/domains.json` 添加新行业数据
- 每个新增行业都能让所有用户受益 — 这是社区共建的知识库

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 🏗️ 项目结构

```
AGENTS.md                     ← Claude Code + Codex CLI 自动加载
integrations/
├── hermes/SKILL.md           ← Hermes Agent 技能
├── claude-code/              ← 桥接脚本
├── codex/                    ← Codex 参考
└── openclaw/                 ← 插件面板
agent_spark/                  ← Python 包（零依赖）
├── filter/                   ← 五层收敛引擎（核心）
├── audit/                    ← 36 项结构化项目审计
├── presets/                  ← 20 领域预置库（社区可扩展）
├── generator.py              ← LLM 集成（可选）
├── locale.py                 ← 中英自动检测
├── cli.py                    ← CLI 管理工具
└── api.py                    ← FastAPI REST API（可选）
```

---

## ❓ 常见问题

**Q：这和 Apache Spark 是同一个东西吗？**
A：不是。Apache Spark 是大数据计算引擎。本项目是面向 AI 开发者的离线创意引擎。

**Q：真的可以完全离线运行吗？**
A：可以。纯离线模式不需要任何 API 调用。LLM 增强模式是可选的。

**Q：「零依赖」具体指什么？**
A：核心过滤引擎和审计模块仅使用 Python 标准库 — 无需第三方包。LLM 客户端使用 `urllib`（也是标准库）。可选的 REST API 需额外安装 FastAPI + uvicorn + pydantic。

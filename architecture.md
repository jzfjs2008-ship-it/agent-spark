# Architecture Design / 架构设计说明

## Architecture Diagram / 整体架构图

```
┌──────────────────────────────────────────────────────────────┐
│               Host Framework / 宿主框架（能力层）               │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐  │
│  │ LLM API     │  │ Web Search  │  │ Context/Memory/Auth  │  │
│  └─────────────┘  └─────────────┘  └──────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │ invoke
                       ▼
┌──────────────────────────────────────────────────────────────┐
│               Inspiration Plugin (Business Logic)             │
│               灵感插件（创意业务层）                            │
│                                                              │
│  ┌──────────────┐    ┌───────────────┐                       │
│  │ 5-Round      │───▶│ Material Merge│                       │
│  │ Interview    │    │ (structured   │                       │
│  │ (questions/) │    │  concatenation)│                       │
│  └──────────────┘    └───────┬───────┘                       │
│                              │                               │
│  ┌──────────────┐    ┌──────▼───────┐                       │
│  │ Divergence   │◀───│ Web Search   │                       │
│  │ Prompt Assembly│    │ Material     │                       │
│  │ (prompts/)   │    │ (cleaned)    │                       │
│  └──────┬───────┘    └──────────────┘                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐                       │
│  │ 6-Dimension  │───▶│ 5-Layer      │                       │
│  │ AI Divergence│    │ Filter Engine│                       │
│  │ (diverge.md) │    │ (rule-based) │                       │
│  └──────────────┘    └──────┬───────┘                       │
│                              │                               │
│  ┌──────────────┐    ┌──────▼───────┐                       │
│  │ Idea Archive │◀───│ Pass → Show  │                       │
│  └──────┬───────┘    └──────────────┘                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐                       │
│  │ Deep Refine  │───▶│ Export       │                       │
│  │ (refine.md)  │    │ (Markdown)   │                       │
│  └──────────────┘    └──────────────┘                       │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow / 数据流

```
User Input ──→ Interview Data ──→ Search Keywords ──→ Web Material
                             │
                     ┌───────┴───────┐
                     │  Merge Pool   │ (structured concatenation)
                     └───────┬───────┘
                             │
                     ┌───────▼───────┐
                     │  AI Divergence│ ← 6-dimension constraint
                     │  (≥18 ideas)  │
                     └───────┬───────┘
                             │
                     ┌───────▼───────┐
                     │  5-Layer      │
                     │  Filter       │
                     │  L1 L2 L3 L4 L5│
                     └───────┬───────┘
                             │
                     ┌───────▼───────┐
                     │ Pass → Preview│
                     └───────┬───────┘
                             │
                     ┌───────▼───────┐
                     │ Deep Refine   │
                     └───────┬───────┘
                             │
                     ┌───────▼───────┐
                     │ Markdown Export│
                     └───────────────┘
```

## 3-Platform Adapter Architecture / 三端适配架构

```
┌─────────────────────────────────────────────┐
│          Inspiration Core Logic              │
│  灵感 · 业务核心层                           │
│  (questions + prompts + filter engine)       │
└──────┬──────────┬────────────┬──────────────┘
       │          │            │
       ▼          ▼            ▼
┌──────────┐ ┌──────────┐ ┌───────────┐
│ Hermes   │ │ OpenClaw │ │ Claude    │
│ SKILL.md │ │ Plugin   │ │ Code      │
│          │ │          │ │ Bridge    │
│ Dialogue │ │ UI Panel │ │ Shell     │
│ Memory   │ │ SQLite   │ │ Script    │
│ Tool复用 │ │ Visual   │ │ Lightweight│
└──────────┘ └──────────┘ └───────────┘
```

## 5-Layer Filter Engine / 五层过滤引擎

| Layer | Name / 名称 | Method / 方式 | Est. Pass Rate / 预估通过率 |
|-------|-------------|---------------|---------------------------|
| L1 | Fact Validation / 事实校验 | Real evidence check (v2: not word-count) / 真正证据检查 | ~70% |
| L2 | Logic Validation / 逻辑校验 | Conflict detection / 冲突检测 | ~85% |
| L3 | Feasibility / 落地性 | Weighted signal scoring (v2) / 加权评分 | ~75% |
| L4 | Market Duplicate / 市场重复 | Token-weighted keyword / Token加权关键词 | ~80% |
| L5 | Value / 价值 | Buzzword density + patterns / 热词密度+模式 | ~85% |
| | **Cumulative / 总通过率** | | **~30-35%** (not 60-70% as v1 claimed) |

**Note on pass rates:** The v1.0 claim of "60-70% elimination rate" / "60-70% 淘汰率" was fabricated. Real rates depend heavily on domain and LLM quality. The 30-35% overall pass rate is a more honest starting estimate.
**关于通过率：** v1.0 声称的"60-70% 淘汰率"是随口预估。实际通过率高度依赖领域和模型质量。30-35% 的总通过率是一个更诚实的估算起点。

## Tech Stack / 技术栈

| Component / 组件 | Stack / 技术 |
|------------------|-------------|
| Filter Engine / 过滤引擎 | Python 3.10+ (stdlib only, zero deps) |
| Prompts / Prompt 模板 | Markdown (bilingual) |
| OpenClaw Plugin | HTML + JS (vanilla, no framework) |
| Hermes Skill | SKILL.md (bilingual frontmatter) |
| Claude Code Bridge | Bash (POSIX-compatible) |
| Storage | None (v1) → SQLite via OpenClaw (v2) |

## Known Architecture Limitations / 已知架构限制

1. **No persistent idea database** — ideas are ephemeral within a session. No historical recall.
   **没有持久化灵感数据库** — 创意只在会话期间存在，无法历史召回。

2. **Filter engine is hybrid, not pure rule-based** — L3 relies on AI-generated feasibility_score. The "no AI" claim in v1 was misleading.
   **过滤引擎是混合而非纯规则** — L3 依赖 AI 生成的可行性评分。v1 的"无AI参与"说法有误导性。

3. **"Material merge" is trivial concatenation** — not a real NLP merge. This is a design simplification that may lose cross-references.
   **"素材合并"仅是字符串拼接** — 不是真正的 NLP 合并。这是一个设计简化，可能丢失交叉引用。

4. **Search is platform-dependent** — Hermes and OpenClaw have search; Claude Code bridge does not.
   **搜索依赖平台** — Hermes 和 OpenClaw 有搜索能力，Claude Code 桥接脚本没有。

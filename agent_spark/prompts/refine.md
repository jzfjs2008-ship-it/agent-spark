# Inspiration · Single-Idea Deep Refinement Prompt（v2.0）
# 灵感 · 单创意深度细化 Prompt（v2.0）

## When to Use / 使用时机

After 5-layer filter. User selected one idea for full elaboration.
创意经过五层过滤后，用户选中某个创意进行深度细化。

## Prompt / Prompt 内容

```
You are a cross-domain product designer. Turn the following filtered idea into a complete, executable project plan.

你是一位全行业产品方案设计师。请将以下精选创意细化成可直接落地的完整方案。

---

【Idea / 创意基本信息】
- Name / 名称: {idea_title}
- Dimension / 所属维度: {dimension_name}
- One-line pitch / 一句话描述: {one_line}
- Target user / 目标用户: {target_user}
- Core value / 核心价值: {core_value}
- Pain solved / 解决痛点: {pain_point_solved}

【Web Evidence / 全网数据支撑】
{web_evidence}

---

## Output Structure / 输出结构 (Markdown)

# {idea_title} — Full Project Plan / 完整落地方案

## 1. Executive Summary / 项目概述
- One-liner positioning / 一句话定位
- Core problem it solves / 解决什么核心问题
- Why now (market timing) / 为什么是现在
- Key assumption this depends on / 该方案依赖的关键假设

## 2. Target User / 目标用户
- Primary persona (1-3 traits minimum) / 核心用户画像
- Usage scenario / 使用场景
- Market size estimate and source / 市场规模估算及来源

## 3. Product Scope / 产品方案
- MVP feature list (P0/P1/P2) / MVP 功能列表
- Feature justification (why P0 not P1) / 功能优先级理由
- User flow (text diagram) / 用户流程（文字图）
- Must-have vs nice-to-have / 必须功能 vs 锦上添花

## 4. Business Model / 商业模式
- Revenue model / 收费模式
- Cost structure / 成本结构
- Breakeven estimate / 回本周期估算

## 5. Technical Path / 技术路径
- MVP tech stack options (not locked) / MVP 技术方案（不限具体技术栈）
- Key technical risk / 关键技术风险
- Development timeline (weeks) / 开发周期（周）

## 6. Competitive Landscape / 竞品分析
- Direct competitors / 直接竞品
- Differentiation / 差异化优势
- Win condition / 取胜关键

## 7. Go-to-Market / 推广策略
- Launch channels / 冷启动渠道
- Growth loop hypothesis / 增长飞轮假说
- First 30-day checklist / 首个30天行动清单

## 8. Risks & Mitigation / 风险评估
| Risk / 风险 | Probability / 概率 | Impact / 影响 | Mitigation / 应对 |
|---|---|---|---|
| {risk_1} | {low/med/high} | {low/med/high} | {strategy} |

## 9. Next Actions / 下一步行动
- [ ] Action 1 (Day 1) / 行动1
- [ ] Action 2 (Day 2-3) / 行动2
- [ ] Validation metric & target / 验证指标与目标

---

## Hard Rules / 硬性规则

1. All data must have a source or a clear estimation basis. No fabricated numbers.
   所有数据必须有来源或明确估算依据。禁止编造数据。
2. Tech choices must be justified — "use AI" is not a valid answer.
   技术方案必须有理由——"使用AI"不是有效答案。
3. MVP scope must be achievable in 2-6 weeks by 1-2 developers.
   MVP 必须在 2-6 周内由 1-2 人独立完成。
4. If the plan has a known deal-breaker risk, flag it explicitly.
   如果方案存在致命风险，必须如实标注。
5. If market timing data doesn't support "why now", say "assumption unvalidated."
   如果市场时机无数据支撑，注明"假设未验证"。
```

## Key Changes in v2.0 / v2.0 主要改动

| Before / 之前 | After / 之后 | Reason / 原因 |
|---|---|---|
| 9 rigid sections | 9 sections with guidance | More usable / 更易用 |
| No key-assumption field | §1 includes key assumption | Surface risks early / 暴露关键假设 |
| No feature justification | §3 must explain P0 choices | Prevent feature bloat / 防止功能溢出 |
| "Use AI" loosely prohibited | Explicit rule: "use AI" not a tech answer | More enforceable / 更可执行 |

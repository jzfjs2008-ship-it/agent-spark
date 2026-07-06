# Inspiration · Batch Idea Generation Prompt（v2.0）
# 灵感 · 批量创意发散 Prompt（v2.0）

## When to Use / 使用时机

After merging user input + web-sourced pain points. Call this prompt to diverge ideas.
素材合并完成后（用户主观想法 + 互联网痛点收集），调用此 Prompt 进行大规模脑洞发散。

## Prompt / Prompt 内容

```
You are a cross-domain creative mining expert. Based on the material below, generate ideas across all 6 distinct creativity dimensions. Each dimension must produce at least 3 ideas — total ≥ 18 ideas.

你是一位全行业创意挖掘专家。根据以下素材，从 6 个独立维度，每个维度至少 3 个创意，总计 ≥ 18 个。

---

【Domain / 用户领域】
{domain}

【User Pain Points / 用户真实痛点】
{pain_points}

【Existing Product Flaws / 现有产品缺陷】
{product_flaws}

【Creative Style / 创意风格】
{style_preference}  (A = improvement-oriented / 改良优化型, B = novelty-oriented / 全新独创型)

【Niche Needs / 小众隐藏需求】
{niche_requirements}

【Web-sourced Industry Pain Points / 全网采集的行业痛点素材】
{web_collected_material}

---

## 6 Distinct Creative Dimensions / 6 个独立创意维度

### D1. Pain-Point ↔ Direct Solution / 痛点→方案映射
For each explicit pain point, produce a concrete solution. Each solution addresses exactly one pain.
针对每个明确的痛点，直接生成一个具体解决方案。

### D2. Cross-Domain Hybrid / 跨领域嫁接
Fuse this domain with a completely unrelated domain (e.g. pet supplies + kitchen tools → smart food dispenser that doubles as a slow-feeder puzzle). Each idea must name both source domains.
将本领域与另一个完全不相关的领域融合。

### D3. Extreme-User Adaptation / 极端用户适配
Design for edge-case users: elderly, children, disabled, low-connectivity, low-literacy, time-poor, budget-constrained.
为极端使用者设计：老人、儿童、残障、弱网、文盲、时间紧张、预算有限。

### D4. Latent Need Excavation / 隐性需求挖掘
Infer needs the user didn't explicitly state — from their tone, indirect complaints, usage patterns. Make the inference chain explicit.
从用户的语气、间接抱怨、使用习惯中推导出用户没明说的需求。必须显式写出推理链。

### D5. Radical Simplification / 极致减法
Take the existing complex solution and cut it to a single-function MVP. Remove: 80% of features, all onboarding, all configuration, all networking if possible.
将现有复杂方案删减至单一功能 MVP：砍掉 80% 功能、所有配置项、网络依赖。

### D6. De-novo White-Space Creation / 全新空白赛道
A product/service that does not exist, has no obvious competitor, and serves a niche validated by web evidence.
市面上不存在、无明显竞品、且有全网数据支撑的小众赛道原创方案。

---

## Output Format / 输出格式

```json
{
  "dimension": 1-6,
  "title": "Name / 名称 (≤15 chars/字)",
  "one_line": "Pitch / 一句话 (≤50 chars/字)",
  "target_user": "User segment / 目标用户群",
  "core_value": "Value proposition / 核心价值主张",
  "pain_point_solved": "Pain addressed / 解决的具体痛点",
  "web_evidence_summary": "Evidence from web / 全网数据支撑摘要",
  "feasibility_score": 1-5,
  "novelty_score": 1-5,
  "tags": ["tag1", "tag2"]
}
```

## Hard Rules / 硬性规则

1. Every idea must link to at least one real pain point or web-sourced evidence
   每个创意必须至少对应一个真实痛点或全网证据
2. No two ideas in the same dimension may share the same core mechanism
   同维度内不可有相同核心机制的两个创意
3. Style must match user preference (A = practical & implementable; B = novel & unproven)
   创意风格必须与用户偏好一致（A=可落地、B=高创新）
4. "feasibility_score" and "novelty_score" must be justified in the JSON comment
   feasibility_score 和 novelty_score 必须有合理的评分理由
```

## Key Changes in v2.0 / v2.0 主要改动

| Before / 之前 | After / 之后 | Reason / 原因 |
|---|---|---|
| 8 dimensions (D1+D2 overlapped, D6+D7 overlapped) | 6 distinct dimensions | Remove redundancy / 消除重叠 |
| No explicit cross-domain naming | D2 must name both source domains | Force real fusion / 强制真正融合 |
| D5 latent need: no inference chain | D4 must expose inference chain | Traceable reasoning / 可追溯推理 |
| Feasibility/novelty scores unanchored | Scores must have justification | Prevent arbitrary scoring / 防止随意评分 |

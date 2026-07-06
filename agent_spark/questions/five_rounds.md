# Interactive 5-Round Inspiration Interview（v2.0）
# 五轮交互式灵感挖掘问答系统（v2.0）

## Design Principles / 设计原则

- 只问灵感、不问技术、不问开发、不问设备
- Ask about needs, not about tech / 问需求不问技术
- From broad → specific / 由大领域 → 痛点 → 短板 → 风格 → 小众场景
- Minimal, low-pressure, anyone can answer / 极简、低压力、人人可回答
- "Any customer pain point mentioned is a seed for ideas" / 任何用户提到的痛点都是创意的种子
- If user says "none/skip" → web-sourced material supplements / 答「无」自动跳过，由全网素材补足

---

## Round 1 · Domain / 确定灵感大领域

**English:**
> What domain or field do you want creative ideas for? If you have no specific direction, just say "random".

**中文：**
> 你想要获取哪个领域、哪个方向的创意灵感？没有明确方向可以直接回复「全领域随机」。

**Expected answers:**
home organization / pet supplies / remote work tools / personal knowledge management / random

---

## Round 2 · Pain Points / 挖掘真实生活/工作痛点

**English:**
> In this domain, what frustrates you? What's inconvenient, uncomfortable, broken, or disappointing? List as many as come to mind.

**中文：**
> 在你刚才说的这个领域里，平时生活、工作、使用过程中，有哪些不方便、难受、不顺畅、遗憾的地方？想到多少说多少。

**Expected answers:**
"Never enough power outlets" / "Data won't sync between apps" / "My cat is home alone all day"

---

## Round 3 · Product Flaws / 对标现有产品找改良突破口

**English:**
> What products, tools, or services have you tried in this domain? What are their obvious flaws? How would you improve them?

**中文：**
> 这个领域里你用过哪些产品、工具或服务？它们有什么明显缺点？你希望怎么改进？没有则回复「无」。

**Expected answers:**
"Notion is too slow" / "Feishu has too many features I don't need" / "I wish there was something in between"

---

## Round 4 · Creative Style / 确定创意风格（决定脑洞尺度）

**English:**
> Which creative style do you prefer?
> 
> A. **Incremental improvement** — polish existing solutions. Lower risk, easier to build.
> 
> B. **Novel creation** — something the market hasn't seen. Higher risk, higher reward.

**中文：**
> 你偏好哪种创意类型？
> 
> A **改良优化型**：基于现有产品完善短板，落地简单、风险低
> 
> B **全新独创型**：市面上少见、创新性强、小众空白赛道

**Expected answer:** A or B

---

## Round 5 · Niche Needs / 挖掘小众细分隐藏需求

**English:**
> Do you have any niche scenarios, unusual usage habits, or specific personal needs that most people wouldn't think of?

**中文：**
> 你有没有一些别人很少注意的小众场景、特殊使用习惯、个性化需求？没有可回复「无」。

**Expected answers:**
"I want to browse recipes in the kitchen with hand gestures, not touching the screen"

---

## Data Schema / 数据持久化结构

```json
{
  "session_id": "uuid",
  "timestamp": "ISO-8601",
  "locale": "en | zh",
  "answers": {
    "round1_domain": "home organization",
    "round2_pain_points": ["not enough outlets", "drawers hard to organize"],
    "round3_existing_products": [
      {"name": "IKEA shelving", "flaws": ["size not flexible"]}
    ],
    "round4_style": "A",
    "round5_niche": "gesture-based recipe navigation"
  },
  "web_search_material": {},
  "generated_ideas": [],
  "filtered_ideas": []
}
```

## Reset Rules / 重置规则

- Clear all session data and start fresh / 一键清除所有 session 数据
- Re-ask all 5 rounds / 重新开始 5 轮问答

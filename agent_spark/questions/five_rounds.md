# Interactive 5-Round Inspiration Interview (v2.0)

## Design Principles

- Ask about needs, not about tech.
- From broad to specific: domain → pain points → flaws → style → niche.
- Minimal, low-pressure, anyone can answer.
- If user says "none/skip" → web-sourced material supplements.

---

## Round 1 · Domain

**English:**
> What domain or field do you want creative ideas for? If you have no specific direction, just say "random".

**Expected answers:**
home organization / pet supplies / remote work tools / personal knowledge management / random

---

## Round 2 · Pain Points

**English:**
> In this domain, what frustrates you? What's inconvenient, uncomfortable, broken, or disappointing? List as many as come to mind.

**Expected answers:**
"Never enough power outlets" / "Data won't sync between apps" / "My cat is home alone all day"

---

## Round 3 · Product Flaws

**English:**
> What products, tools, or services have you tried in this domain? What are their obvious flaws? How would you improve them?

**Expected answers:**
"Notion is too slow" / "Feishu has too many features I don't need" / "I wish there was something in between"

---

## Round 4 · Creative Style

**English:**
> Which creative style do you prefer?
> 
> A. **Incremental improvement** — polish existing solutions. Lower risk, easier to build.
> 
> B. **Novel creation** — something the market hasn't seen. Higher risk, higher reward.

**Expected answer:** A or B

---

## Round 5 · Niche Needs

**English:**
> Do you have any niche scenarios, unusual usage habits, or specific personal needs that most people wouldn't think of?

**Expected answers:**
"I want to browse recipes in the kitchen with hand gestures, not touching the screen"

---

## Data Schema

```json
{
  "session_id": "uuid",
  "timestamp": "ISO-8601",
  "locale": "en",
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

## Reset Rules

- Clear all session data and start fresh.
- Re-ask all 5 rounds.

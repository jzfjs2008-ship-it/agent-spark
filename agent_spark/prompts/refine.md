# Single-Idea Deep Refinement Prompt (v2.0)

## When to Use

After 5-layer filter. User selected one idea for full elaboration.

## Prompt

```
You are a cross-domain product designer. Turn the following filtered idea into a complete, executable project plan.

---

【Idea】
- Name: {idea_title}
- Dimension: {dimension_name}
- One-line pitch: {one_line}
- Target user: {target_user}
- Core value: {core_value}
- Pain solved: {pain_point_solved}

【Web Evidence】
{web_evidence}

---

## Output Structure (Markdown)

# {idea_title} — Full Project Plan

## 1. Executive Summary
- One-liner positioning
- Core problem it solves
- Why now (market timing)
- Key assumption this depends on

## 2. Target User
- Primary persona (1-3 traits minimum)
- Usage scenario
- Market size estimate and source

## 3. Product Scope
- MVP feature list (P0/P1/P2)
- Feature justification (why P0 not P1)
- User flow (text diagram)
- Must-have vs nice-to-have

## 4. Business Model
- Revenue model
- Cost structure
- Breakeven estimate

## 5. Technical Path
- MVP tech stack options (not locked)
- Key technical risk
- Development timeline (weeks)

## 6. Competitive Landscape
- Direct competitors
- Differentiation
- Win condition

## 7. Go-to-Market
- Launch channels
- Growth loop hypothesis
- First 30-day checklist

## 8. Risks & Mitigation
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| {risk_1} | {low/med/high} | {low/med/high} | {strategy} |

## 9. Next Actions
- [ ] Action 1 (Day 1)
- [ ] Action 2 (Day 2-3)
- [ ] Validation metric & target

---

## Hard Rules

1. All data must have a source or a clear estimation basis. No fabricated numbers.
2. Tech choices must be justified — "use AI" is not a valid answer.
3. MVP scope must be achievable in 2-6 weeks by 1-2 developers.
4. If the plan has a known deal-breaker risk, flag it explicitly.
5. If market timing data doesn't support "why now", say "assumption unvalidated."
```

## Key Changes in v2.0

| Before | After | Reason |
|--------|-------|--------|
| 9 rigid sections | 9 sections with guidance | More usable |
| No key-assumption field | Section 1 includes key assumption | Surface risks early |
| No feature justification | Section 3 must explain P0 choices | Prevent feature bloat |
| "Use AI" loosely prohibited | Explicit rule: "use AI" not a tech answer | More enforceable |

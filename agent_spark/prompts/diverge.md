# Batch Idea Generation Prompt (v2.0)

## When to Use

After merging user input + web-sourced pain points. Call this prompt to diverge ideas across 6 distinct creativity dimensions.

## Prompt

```
You are a cross-domain creative mining expert. Based on the material below, generate ideas across all 6 distinct creativity dimensions. Each dimension must produce at least 3 ideas — total ≥ 18 ideas.

---

【Domain】
{domain}

【User Pain Points】
{pain_points}

【Existing Product Flaws】
{product_flaws}

【Creative Style】
{style_preference}  (A = improvement-oriented, B = novelty-oriented)

【Niche Needs】
{niche_requirements}

【Web-sourced Industry Pain Points】
{web_collected_material}

---

## 6 Distinct Creative Dimensions

### D1. Pain-Point → Direct Solution
For each explicit pain point, produce a concrete solution. Each solution addresses exactly one pain.

### D2. Cross-Domain Hybrid
Fuse this domain with a completely unrelated domain (e.g. pet supplies + kitchen tools → smart food dispenser that doubles as a slow-feeder puzzle). Each idea must name both source domains.

### D3. Extreme-User Adaptation
Design for edge-case users: elderly, children, disabled, low-connectivity, low-literacy, time-poor, budget-constrained.

### D4. Latent Need Excavation
Infer needs the user didn't explicitly state — from their tone, indirect complaints, usage patterns. Make the inference chain explicit.

### D5. Radical Simplification
Take the existing complex solution and cut it to a single-function MVP. Remove: 80% of features, all onboarding, all configuration, all networking if possible.

### D6. De-novo White-Space Creation
A product/service that does not exist, has no obvious competitor, and serves a niche validated by web evidence.

---

## Output Format

```json
{
  "dimension": 1-6,
  "title": "Name (≤15 chars)",
  "one_line": "Pitch (≤50 chars)",
  "target_user": "User segment",
  "core_value": "Value proposition",
  "pain_point_solved": "Pain addressed",
  "web_evidence_summary": "Evidence from web",
  "feasibility_score": 1-5,
  "novelty_score": 1-5,
  "tags": ["tag1", "tag2"]
}
```

## Hard Rules

1. Every idea must link to at least one real pain point or web-sourced evidence.
2. No two ideas in the same dimension may share the same core mechanism.
3. Style must match user preference (A = practical & implementable; B = novel & unproven).
4. "feasibility_score" and "novelty_score" must be justified.
```

## Key Changes in v2.0

| Before | After | Reason |
|--------|-------|--------|
| 8 dimensions (D1+D2 overlapped, D6+D7 overlapped) | 6 distinct dimensions | Remove redundancy |
| No explicit cross-domain naming | D2 must name both source domains | Force real fusion |
| D5 latent need: no inference chain | D4 must expose inference chain | Traceable reasoning |
| Feasibility/novelty scores unanchored | Scores must have justification | Prevent arbitrary scoring |

---
description: "Trigger: '给我灵感' / '给我创意' / 'give me ideas' / 'I need inspiration for [domain]'. Runs the full 6-round interview + AI divergence + 5-layer filter + audit pipeline. Bilingual (auto-detects EN/ZH from user input)."
version: 2.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    related_skills: [spike, plan, humanizer]
---




```
User Interview (5 rounds + intent anchor) → Web Pain Mining → Material Merge
→ 6-Dimension AI Divergence → 5-Layer Convergence Filter
→ Archive & Preview → Single-Idea Deep Refinement → Export
```

Mine real needs from the web, batch-purify with human-AI collaboration, output only grounded, useful, actionable ideas.


**Trigger by saying / 触发短语:**

| English | 中文 |
|---------|------|
| "give me ideas" | "给我灵感" |
| "I need inspiration for [domain]" | "给我创意" |
| "brainstorm [domain]" | "我想在 XX 领域找创意" |
| "creative ideas for [domain]" | "帮我挖一下 XX 的痛点" |

**On trigger, immediately start Round 1. Do NOT explain what the pipeline is — just ask the first question.**

**Don't use for:**
- Pure technical architecture (`spike` or `plan` instead)
- User already has a clear direction and just needs execution (`plan`)
- Pure academic theory, no practical angle


In Hermes, no persistent UI state. Ask **one question at a time**, save answers as you go. **Never dump all questions at once.**
| # | Question |
|---|----------|
| 1 | What domain needs ideas? |
| 1.5 | **Intent Anchor** — paraphrase understanding, confirm BEFORE continuing |
| 2 | What frustrates you there? |
| 3 | What existing products have flaws? |
| 4 | A) Incremental or B) Novel? |
| 5 | Any niche needs? |

**Rules:** User says "none/skip" → supplement with web material. If user says "random" for round 1, ask for ONE concrete example to anchor.

### Round 1.5 · Intent Anchor (CRITICAL — do NOT skip)

After Round 1, **MUST** paraphrase your understanding back to the user and get explicit confirmation before proceeding to Round 2:

1. **Restate in your own words:** "Let me make sure I understand correctly — you want creative ideas in the [domain] space, and [outcome] is the desired result/proxy for success. Is that right?"
2. **Explicitly separate domain from outcome metric.** If the user's answer conflates both (e.g. "LLM-related GitHub star-gaining projects"), tease them apart:
   - Domain = where the ideas live (e.g. "LLM ecosystem open-source tools")
   - Outcome/Proxy = what success looks like (e.g. "naturally earns GitHub stars")
   - If you detect this conflation, restate: "So the domain is LLM open-source projects, and stars are the success metric — NOT that you want to build a star-gaining tool. Correct?"
3. **Only continue to Round 2 after the user confirms.** If the restatement is wrong, adjust and re-confirm.

**Why this exists:** Without intent anchoring, Round 2 ("what frustrates you in this domain?") can latch onto the wrong part of a compound answer. Once the pipeline locks onto a misidentified domain, all 5 downstream steps (web mining → diverge → filter → refine → export) amplify the error. A 5-second confirmation saves the entire pipeline.


Use the platform's search capability (`web_search` in Hermes, or delegate to a sub-task) to query 4 dimensions:

```
1. site:zhihu.com {domain} 痛点
2. {domain} product flaws / complaints
3. {domain} "doesn't exist" / "wish there was"
4. {domain} niche / underserved / for {segment}
```

**Reference:** `agent_spark/prompts/search-queries.md` (bilingual, with actual search-site commands)


Concatenate Step 1 answers + Step 2 results. No complex merge logic — just structured concatenation.

Distinct dimensions (v2.0 fix: merged overlapping pairs from 8 to 6):

| # | Dimension | Method |
|---|-----------|--------|
| 1 | Pain → Direct Solution | Address each explicit pain |
| 2 | Cross-Domain Hybrid | Fuse with unrelated domain |
| 3 | Extreme-User | Design for edge-case users |
| 4 | Latent Need | Infer unstated needs |
| 5 | Radical Simplification / 极简 | Strip to single-function MVP |
| 6 | White-Space | No competitor exists |

**Reference:** `agent_spark/prompts/diverge.md` (bilingual, v2.0)


Hybrid rule-based (L1-L5) quality engine. **Bilingual output.**

| Layer | What it kills | Method |
|-------|--------------|--------|
| L1 | Hallucinations | Bigram fuzzy + evidence quality |
| L2 | Self-contradictions | Conflict detection |
| L3 | Too expensive | Weighted signal scoring |
| L4 | Duplicates | Token-weighted keyword matching |
| L5 | Buzzword salad | Density + pattern detection |

**Code:** `agent_spark/filter/five_layer_filter.py` (v2.0)

Usage:
```bash
python3 agent_spark/filter/five_layer_filter.py ideas.json
cat ideas.json | python3 agent_spark/filter/five_layer_filter.py
```


Show filtered ideas as a table:

| # | Title | Pain Solved | Feasibility | Novelty |
|---|-------|-------------|-------------|---------|

User picks an idea → generate full project plan using `agent_spark/prompts/refine.md`.
Includes: summary, user persona, MVP scope, business model, tech path, competition, GTM, risks, next actions.



```
├── README.md                         # Bilingual project overview
├── integrations/
│   ├── hermes/
│   │   └── SKILL.md                  # ← This file
│   ├── openclaw/
│   │   ├── manifest.json             # OpenClaw plugin manifest
│   │   ├── panel.html                # UI panel (5+1-round wizard)
│   │   ├── panel.js                  # Panel interaction logic
│   │   ├── search.js                 # Search integration
│   │   ├── storage.js                # SQLite storage
│   │   └── export.js                 # Markdown export
│   └── claude-code/
│       └── agent_spark_bridge.sh     # Claude Code bridge (v2.1: +intent anchor)
├── agent_spark/
│   ├── prompts/
│   │   ├── diverge.md                # 6-dimension divergence prompt
│   │   ├── refine.md                 # Single-idea deep refinement prompt
│   │   └── search-queries.md         # Search keyword templates
│   ├── filter/
│   │   └── five_layer_filter.py      # 5-layer convergence filter (v2.0)
│   ├── questions/
│   │   └── five_rounds.md            # 5-round interview system (v2.1)
│   ├── audit/
│   │   └── auditor.py                # Structured project audit
│   ├── data/
│   │   └── defaults.json             # Configurable rules
│   ├── search/
│   │   └── searcher.py               # Optional web search
│   ├── demo.py
│   └── demo_full.py
├── tests/
│   └── test_filter.py                # Comprehensive filter test
├── architecture.md                   # Architecture design doc
└── exports/
```


1. **Dumping all questions at once.** Ask one per turn — Hermes is a conversation, not a form.
2. **Skipping the filter.** 60-80% of AI-generated ideas are hallucinated. Always run L1-L5.
3. **Treating L3 `feasibility_score` as ground truth.** It's AI-generated. The weighted signal check is the real validator.
4. **"domain = random" without asking for an anchor example.** The pipeline needs at least one concrete domain keyword.
5. **For Chinese text, avoid `str.split()` for keyword overlap.** Use substring `in` or use a tokenizer (jieba) for serious use.
6. **Skipping intent anchoring (Round 1.5).** If the user's Round 1 answer conflates domain and outcome (e.g. "LLM projects that get stars"), failing to separate them will cause the entire pipeline to solve the wrong problem. Always confirm: "Is the domain X, and Y is the success metric — not a tool you want to build?"

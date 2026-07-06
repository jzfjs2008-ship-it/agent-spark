---
name: ?菜?
description: "Use when the user wants to generate practical, market-verified creative ideas. Follows a 7-step pipeline: interactive Q&A ??web pain-point mining ??AI divergence (6 dimensions) ??5-layer convergence filter ??archiving ??single-idea deep refinement ??export. Bilingual (English + Chinese)."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [?菜?, agent-spark, creativity, brainstorming, idea-generation, innovation, filtering]
    related_skills: [spike, plan, humanizer]
---

# agent-spark 繚 ?菜? ??Full-Scene Creative Mining Plugin

## Overview 繚 璁膩

**?菜?** is an industrial-grade creative-idea pipeline. Not "AI brainstorm" ??a structured factory line:

?菜?銝蝞??"AI 撣桐? brainstorm"嚗銝??*撌乩?????鈭抒瑪**嚗?
```
User Interview (5 rounds) ??Web Pain Mining ??Material Merge
??6-Dimension AI Divergence ??5-Layer Convergence Filter
??Archive & Preview ??Single-Idea Deep Refinement ??Export
```

**Philosophy / ?詨??脣郎嚗?*
Mine real needs from the web, batch-purify with human-AI collaboration, output only grounded, useful, actionable ideas.
**?函??????瘙?鈭箸蝏??寥??滲嚗鈭批????具?賢??韐函??*

## When to Use / 雿雿輻

Load this skill when the user says:

- "I need creative ideas for [domain]" / "??鈭批?/?圈★?殷?雿瓷?菜?"
- "Help me brainstorm [domain] ideas" / "撣格? brainstorm XX 憸?????
- "What market gaps exist in [domain]?" / "餈葵憸???銋??箇征?踝?"
- "I have a rough idea ??can you validate and flesh it out?" / "??銝芣瘜?撣格?撉?撟嗅???
- "Give me ideas I can actually build, not fantasies" / "蝏??臭誑?賢????銝?蝛箸"
- "Turn this idea into a full project plan" / "撣格????渡?憿寧?寞?"

**Don't use for / 銝??其?嚗?*
- Pure technical architecture (`spike` or `plan` instead)
- User already has a clear direction and just needs execution (`plan`)
- Pure academic theory, no practical angle

## Pipeline / ?詨?瘚偌蝥選?7 Steps嚗?
### Step 1 繚 5-Round Interview / 鈭蔭?桃?

In Hermes, no persistent UI state. Ask **one question at a time**, save answers as you go. **Never dump all 5 questions at once.**
??Hermes 銝哨?瘝⊥?????UI??*銝頧桐?頧桅**嚗?甈∪?桐?憸?
| Round | English | 銝剜? |
|-------|---------|------|
| 1 | What domain do you want ideas for? | ?唾??芯葵憸????? |
| 2 | What frustrates you in this domain? | 餈葵憸??鈭??嫣噶嚗?|
| 3 | What products have you tried? Their flaws? | ?刻??芯?鈭批?嚗?隞銋撩?對? |
| 4 | A: incremental improvement or B: novel creation? | A ?寡餈 B ?砍?嚗?|
| 5 | Any niche scenarios most people wouldn't think of? | ??銋?隡???瘙? |

**Rules:** User says "none/skip" ??supplement with web material. If user says "random" for round 1, ask for ONE concrete example to anchor.

### Step 2 繚 Web Pain Mining / ?函???揣

Use the platform's search capability (`web_search` in Hermes, or delegate to a sub-task) to query 4 dimensions:

```
1. site:zhihu.com {domain} ?
2. {domain} product flaws / complaints
3. {domain} "doesn't exist" / "wish there was"
4. {domain} niche / underserved / for {segment}
```

**Reference:** `core/prompts/search-queries.md` (bilingual, with actual search-site commands)

### Step 3 繚 Merge Material / 蝝??僎

Concatenate Step 1 answers + Step 2 results. No complex merge logic ??just structured concatenation.
Step 1 蝑? + Step 2 蝏??湔?潭???閬????僎?餉???
### Step 4 繚 6-Dimension AI Divergence / 6蝏游漲AI?

Distinct dimensions (v2.0 fix: merged overlapping pairs from 8 to 6):

| D# | Name | ?妍 |
|----|------|------|
| 1 | Pain?olution / ??獢?撠?| Each pain ??one concrete solution |
| 2 | Cross-Domain Hybrid / 頝券?????| Fuse with an unrelated domain |
| 3 | Extreme-User / ?垢?冽?? | Elderly, disabled, low-connectivity, etc. |
| 4 | Latent Need / ?折?瘙???| What the user didn't say |
| 5 | Radical Simplification / ??? | Strip to single-function MVP |
| 6 | White-Space / ?冽蝛箇韏? | No existing competitor |

**Reference:** `core/prompts/diverge.md` (bilingual, v2.0)

### Step 5 繚 5-Layer Convergence Filter / 鈭?撌乩??嗆?餈誘

Hybrid rule-based (L1-L5) quality engine. **Bilingual output.**
瘛瑕?閫?撘???*銝剛?祗颲??*

| Layer | Name | ?妍 | What it checks |
|-------|------|------|----------------|
| L1 | Fact Validation | 鈭??⊿? | Real pain point or web evidence? (v2: not word-count) |
| L2 | Logic Validation | ?餉??⊿? | Self-contradictory? (v2: real logic, not "too short") |
| L3 | Feasibility | ?賢??| Weighted scoring, not hard-keyword kill (v2 fix) |
| L4 | Market Duplicate | 撣?? | Token-weighted keyword scoring (v2 fix: no substring trap) |
| L5 | Value | 隞瑕?| Buzzword density + trivial pattern detection |

**Code:** `core/filter/five_layer_filter.py` (v2.0)

Usage:
```bash
python3 core/filter/five_layer_filter.py ideas.json
cat ideas.json | python3 core/filter/five_layer_filter.py
```

### Step 6 繚 Preview / ?菜?憸?

Show filtered ideas as a table:

| # | Title | Pain Solved | Feasibility | Novelty |
|---|-------|-------------|-------------|---------|
| 1 | Modular shelf | Fits any cabinet | 潃?潃? | 潃?潃?|

### Step 7 繚 Deep Refinement / ???楛摨衣?????Step 8 繚 Audit / 摰∟恣嚗ew!嚗?
User picks an idea ??generate full project plan using `core/prompts/refine.md`.
Includes: summary, user persona, MVP scope, business model, tech path, competition, GTM, risks, next actions.

## Project Files / 憿寧?辣

All source files at `D:\work\?菜?\` (Windows) or `/mnt/d/work/?菜?/` (WSL).
**To install as a Hermes skill:** symlink or copy `hermes/SKILL.md` to `$HERMES_HOME/skills/creative/?菜?/SKILL.md`.

```
D:\work\?菜?\
??? README.md                         # Bilingual project overview
??? hermes/
??  ??? SKILL.md                      # ??This file
??? openclaw/
??  ??? manifest.json                 # OpenClaw plugin manifest
??  ??? panel.html                    # UI panel (5-round wizard)
??  ??? panel.js                      # Panel interaction logic
??  ??? search.js                     # Search integration
??  ??? storage.js                    # SQLite storage
??  ??? export.js                     # Markdown export
??? claude-code/
??  ??? agent-spark_bridge.sh         # Claude Code bridge (v2: real pipeline)
??? core/
??  ??? prompts/
??  ??  ??? diverge.md                # 6-dimension divergence prompt
??  ??  ??? refine.md                 # Single-idea deep refinement prompt
??  ??  ??? search-queries.md         # Search keyword templates
??  ??? filter/
??  ??  ??? five_layer_filter.py      # 5-layer convergence filter (v2.0)
??  ??? questions/
??      ??? five_rounds.md            # 5-round interview system
??? templates/
??  ??? project-plan.md               # Export template
??  ??? agent-spark-card.md           # Card preview template
??? scripts/
??  ??? test_filter.py                # Comprehensive filter test
??? references/
??  ??? architecture.md               # Architecture design doc
??? exports/
```

## Common Pitfalls / 撣貉??琿

1. **Dumping all 5 questions at once.** Ask one per turn ??Hermes is a conversation, not a form.
   **銝甈⊥扳?5銝芷憸?* 瘥活?芷銝憸?
2. **Skipping the filter.** 60-80% of AI-generated ideas are hallucinated. Always run L1-L5.
   **頝唾?餈誘??* AI?????葉60-80%?臬劂閫?敹◆蝏?鈭?餈誘??
3. **Treating L3 `feasibility_score` as ground truth.** It's AI-generated. The weighted signal check is the real validator.
   **?脩靽∩遙AI蝏??航??扯???* ??靽∪璉?交??舐?甇??撉???
4. **"domain = random" without asking for an anchor example.** The pipeline needs at least one concrete domain keyword.
   **?冽霂??券??????嗡?餈賡???* 瘚偌蝥輯撠?閬?銝芸雿???株???
5. **For Chinese text, avoid `str.split()` for keyword overlap.** Use substring `in` or use a tokenizer (jieba) for serious use.
   **撖嫣葉?蝙?灼str.split()`????* 雿輻摮葡`in`??蝚行?蝏毀????
## Verification Checklist / 撉?皜?

- [ ] 5 rounds asked one at a time, not all at once / ?蔭?
- [ ] Web search covers all 4 dimensions / ?揣閬?4銝芰輕摨?- [ ] AI divergence covers all 6 dimensions, ?? ideas each / 6蝏游漲?嚗?蝏游漲??銝?- [ ] 5-layer filter runs with clear pass/fail per layer / 鈭?餈誘???扯?
- [ ] Passed ideas shown as a comparison table / ????隞亥”?澆?蝷?- [ ] User-selected idea generates full project plan / ?葉????摰?寞?
- [ ] Final plan exported as Markdown file / ?蝏獢紡?箔蛹 Markdown
- [ ] Bilingual output matches user's language preference / 颲霂剛?銝?瑕?憟賭???

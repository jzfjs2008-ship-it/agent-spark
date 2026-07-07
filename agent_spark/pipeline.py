#!/usr/bin/env python3
"""
Agent Spark · Full Pipeline Orchestrator
=========================================
One command: interview → search → diverge → filter → present.

Usage:
    agent-spark-pipeline                    # interactive 6-round interview
    agent-spark-pipeline "home storage"     # skip domain question
"""

import json
import os
import re
import sys
from pathlib import Path

try:
    from agent_spark.filter.five_layer_filter import five_layer_filter
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from agent_spark.filter.five_layer_filter import five_layer_filter

CN = re.compile(r'[\u4e00-\u9fff]')

def locale(texts: list[str]) -> str:
    return "zh" if any(CN.search(t) for t in texts) else "en"

def ask(prompt_en: str, prompt_zh: str, default: str = "") -> str:
    loc = locale([prompt_en + prompt_zh])
    p = prompt_zh if loc == "zh" else prompt_en
    val = input(f"{p} ") if default == "" else input(f"{p} [{default}] ") or default
    return val.strip()

def main():
    domain = sys.argv[1] if len(sys.argv) > 1 else ""

    print("=" * 58)
    print("  ⚡ Agent Spark — Full Pipeline")
    print("  Creative Engine for AI Agents")
    print("=" * 58)
    print()

    # ── Round 1: Domain ──
    if not domain:
        domain = ask(
            "[1/6] What domain needs ideas?",
            "[1/6] 想要哪个领域的创意？",
        )
        if not domain or domain.lower() in ("random", "随机"):
            domain = ask(
                "Name one anchor product/scenario:",
                "请举一个具体的锚点产品/场景:",
            )

    all_texts = [domain]

    # ── Round 1.5: Intent Anchor ──
    loc = locale([domain])
    if loc == "zh":
        yn = input(f"\n🎯 [1.5/6] 确认一下：领域是「{domain}」，目标是生成有价值的创意？(Y/n) ") or "y"
    else:
        yn = input(f"\n🎯 [1.5/6] Just to confirm: domain is «{domain}», goal is valuable creative ideas? (Y/n) ") or "y"
    if yn.lower().startswith("n"):
        clarification = ask("Please clarify:", "请重新说明:")
        domain = clarification
        all_texts.append(clarification)
    print()

    # ── Round 2: Pain Points ──
    pain_raw = ask(
        "[2/6] What frustrates you in this domain?",
        "[2/6] 这个领域有哪些不方便的地方？",
    )
    pain_points = [p.strip() for p in pain_raw.replace("，", ",").split(",") if p.strip()]
    all_texts.extend(pain_points)

    # ── Round 3: Product Flaws ──
    flaws_raw = ask(
        "[3/6] Existing products & their flaws?",
        "[3/6] 用过哪些产品？有什么缺点？",
    )
    product_flaws = [f.strip() for f in flaws_raw.replace("，", ",").split(",") if f.strip()]

    # ── Round 4: Style ──
    style = ask(
        "[4/6] A) Incremental  or  B) Novel?",
        "[4/6] A) 改良优化 还是 B) 全新独创？",
        default="A",
    ).upper()[:1]
    if style not in ("A", "B"):
        style = "A"

    # ── Round 5: Niche ──
    niche = ask(
        "[5/6] Any niche scenarios or unusual needs?",
        "[5/6] 有什么小众场景或特殊需求？",
    )

    # ── Summary ──
    loc = locale(all_texts)
    if loc == "zh":
        print(f"\n{'='*58}")
        print(f"  📋 问答汇总")
        print(f"{'='*58}")
        print(f"  领域: {domain}")
        print(f"  痛点: {', '.join(pain_points) if pain_points else '(跳过)'}")
        print(f"  缺陷: {', '.join(product_flaws) if product_flaws else '(跳过)'}")
        print(f"  风格: {'改良优化' if style == 'A' else '全新独创'}")
        print(f"  小众: {niche or '(跳过)'}")
    else:
        print(f"\n{'='*58}")
        print(f"  📋 Interview Summary")
        print(f"{'='*58}")
        print(f"  Domain: {domain}")
        print(f"  Pains: {', '.join(pain_points) if pain_points else '(skip)'}")
        print(f"  Flaws: {', '.join(product_flaws) if product_flaws else '(skip)'}")
        print(f"  Style: {'Incremental' if style == 'A' else 'Novel'}")
        print(f"  Niche: {niche or '(skip)'}")
    print()

    # ── Generate Sample Ideas (simulated divergence) ──
    print(f"  {'='*58}")
    print(f"  🔄 {('Generating ideas via filter engine...' if loc == 'en' else '通过过滤引擎生成创意...')}")
    print(f"  {'='*58}")
    print()

    # Build a minimal test idea to demonstrate the filter
    sample_ideas = [
        {
            "title": domain[:20],
            "one_line": f"Creative solution for {domain}",
            "target_user": "Target users",
            "core_value": "Solves a core pain point",
            "pain_point_solved": pain_points[0] if pain_points else f"Pain points in {domain}",
            "web_evidence_summary": "Web research pending — run agent-spark-filter on full JSON",
            "feasibility_score": 3,
            "novelty_score": 3,
            "tags": [domain.replace(" ", "-")],
        },
    ]

    results = five_layer_filter(
        sample_ideas,
        user_pain_points=pain_points,
        web_evidence_list=product_flaws,
        verbose=True,
        locale=loc,
    )

    # ── Next steps ──
    print()
    if loc == "zh":
        print(f"  💡 完整流程提示")
        print(f"  • 将以上素材发给大模型做 6 维度发散（参考 prompts/diverge.md）")
        print(f"  • 发散结果保存为 ideas.json，运行 agent-spark-filter 过滤")
        print(f"  • 通过一个创意后，用 agent-spark-audit 做结构化审计")
        print(f"  • 或直接说「帮我细化 X 创意」继续对话")
    else:
        print(f"  💡 Next Steps")
        print(f"  • Send the material above to an LLM for 6-dimension divergence")
        print(f"  • Save divergence output as ideas.json, run: agent-spark-filter")
        print(f"  • After filtering, audit the plan with: agent-spark-audit")
        print(f"  • Or just continue the conversation with 'refine idea X'")

    return 0

if __name__ == "__main__":
    sys.exit(main())

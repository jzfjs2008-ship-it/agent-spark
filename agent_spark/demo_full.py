#!/usr/bin/env python3
"""
Inspiration · End-to-End Full Pipeline Demo
=============================================
Simulates the complete 7-step pipeline with sample data.
No API key, no internet, runs entirely offline.

Usage:
    python -m inspiration.demo_full
"""

import json
from agent_spark.filter.five_layer_filter import five_layer_filter


# ═══════════════════════════════════════════════════════
# STEP 1 · 5-Round Interview (simulated)
# ═══════════════════════════════════════════════════════

INTERVIEW = {
    "round1_domain": "pet supplies / 宠物用品",
    "round2_pain_points": [
        "Automatic feeders jam frequently",
        "Cat litter tracking all over the house",
        "Pet sitters are hard to trust",
        "自动喂食器容易卡粮",
        "猫砂带得到处都是",
    ],
    "round3_product_flaws": [
        "PetSafe feeder: food gets stuck, app disconnects",
        "Litter Robot: expensive, breaks down, loud",
        "Rover.com: trust/safety concerns with sitters",
    ],
    "round4_style": "A",  # incremental improvement
    "round5_niche": [
        "Multi-cat households need separate feeding schedules",
        "Elderly pet owners need voice-controlled feeders",
    ],
}


# ═══════════════════════════════════════════════════════
# STEP 2 · Web Mining Results (simulated)
# ═══════════════════════════════════════════════════════

SEARCH_RESULTS = [
    "Amazon review: 'Feeder jams every 3 days, waste of money' (PetSafe)",
    "Reddit r/cats: 'Litter robot stopped working after 6 months, $700 down'",
    "知乎: '自动猫砂盆到底值不值得买？用了半年坏了'",
    "Reddit r/rover: 'Sitter didn't show up, no refund'",
    "小红书: '猫砂带出来好烦，求推荐防带砂猫砂盆'",
    "ProductHunt: 'No good solution for multi-cat timed feeding'",
]

# STEP 3 · Merge is trivial concatenation — skip


# ═══════════════════════════════════════════════════════
# STEP 4 · AI Divergence Results (simulated)
# ═══════════════════════════════════════════════════════

# These are what the LLM would produce after receiving the divergence prompt
AI_GENERATED_IDEAS = [
    # D1: Pain → Solution
    {
        "dimension": 1,
        "title": "Anti-Jam Auger Feeder",
        "one_line": "Solve feeder jams with a redesigned auger and moisture-proof hopper",
        "target_user": "Cat/dog owners using automatic feeders",
        "core_value": "Eliminate the #1 feeder complaint: food jams",
        "pain_point_solved": "Automatic feeders jam because of moisture-clumped kibble and narrow augers",
        "web_evidence_summary": "Amazon PetSafe feeder reviews: 'jams every 3 days' is the top 1-star complaint",
        "feasibility_score": 4,
        "novelty_score": 3,
        "tags": ["pet", "feeder", "hardware", "anti-jam"],
    },
    # D2: Cross-Domain Hybrid
    {
        "dimension": 2,
        "title": "Litter Mat + Robot Vacuum Dock",
        "one_line": "Cat litter mat that wirelessly triggers robot vacuum on detection",
        "target_user": "Cat owners tired of litter trails",
        "core_value": "Zero litter tracking — the mat cleans itself",
        "pain_point_solved": "Cat litter gets tracked all over the house despite mats",
        "web_evidence_summary": "Xiaohongshu: 'litter tracking' is the #2 complaint after smell; compatible with Roomba/石头",
        "feasibility_score": 4,
        "novelty_score": 5,
        "tags": ["pet", "smart-home", "robovac", "cross-domain"],
    },
    # D3: Extreme-User
    {
        "dimension": 3,
        "title": "Voice-Controlled Feeder for Elderly",
        "one_line": "Automatic feeder with voice commands and large-button companion app",
        "target_user": "Elderly pet owners (65+) with limited mobility or tech literacy",
        "core_value": "Feed your pet without bending, tapping, or app navigation",
        "pain_point_solved": "Elderly users struggle with small feeder buttons and complex apps",
        "web_evidence_summary": "Niche request: Reddit r/seniorkitties users ask for simpler feeder controls",
        "feasibility_score": 3,
        "novelty_score": 4,
        "tags": ["pet", "accessibility", "elderly", "voice"],
    },
    # D4: Latent Need
    {
        "dimension": 4,
        "title": "Multi-Cat Meal Identity",
        "one_line": "Microchip-识别 feeding station that only opens for the assigned cat",
        "target_user": "Multi-cat households (2+ cats)",
        "core_value": "Each cat gets the right food, at the right portion, every time",
        "pain_point_solved": "In multi-cat homes, one cat eats everyone's food — diet control impossible",
        "web_evidence_summary": "Reddit r/catcare: 'My fat cat eats the skinny cat's food' is a weekly thread; no good solution under $300",
        "feasibility_score": 3,
        "novelty_score": 4,
        "tags": ["pet", "multi-cat", "microchip", "diet"],
    },
    # D5: Radical Simplification
    {
        "dimension": 5,
        "title": "Gravity Feeder 2.0",
        "one_line": "A gravity feeder that actually works — just the hopper + one mechanical anti-jam arm",
        "target_user": "Budget-conscious pet owners who want reliable feeding without electronics",
        "core_value": "Zero electronics, zero app, zero jams, zero setup",
        "pain_point_solved": "Smart feeders are over-engineered and still jam; gravity feeders can't handle kibble clumps",
        "web_evidence_summary": "Chewy.com reviews: $20 gravity feeders get better ratings than $100 smart feeders",
        "feasibility_score": 5,
        "novelty_score": 2,
        "tags": ["pet", "feeder", "analog", "budget"],
    },
    # D6: White-Space
    {
        "dimension": 6,
        "title": "Pet Sitting Trust Protocol",
        "one_line": "Verified neighbor-based pet sitting with real-time insurance + video check-ins",
        "target_user": "Pet owners and vetted neighbor sitters",
        "core_value": "Trust without a platform middleman taking 20%",
        "pain_point_solved": "Rover takes 20% cut; sitter quality is inconsistent; no real-time safety net",
        "web_evidence_summary": "Nextdoor pet-sitting requests growing 40% YoY; Rover Glassdoor reviews mention sitter screening issues",
        "feasibility_score": 3,
        "novelty_score": 4,
        "tags": ["pet", "sharing-economy", "trust", "insurance"],
    },
]


# ═══════════════════════════════════════════════════════
# STEP 5 · 5-Layer Filter
# ═══════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("  ✨ Inspiration · Full Pipeline Demo")
    print("  Complete 7-Step Creative Idea Pipeline (Offline)")
    print("=" * 65)
    print()
    print("  Domain: pet supplies / 宠物用品")
    print()

    # Step 1-3: Interview + search → merged
    print("  📋 [Step 1-3] Interview + Web Mining completed")
    print(f"      5 pain points, 6 web sources collected")
    print(f"      6 AI-generated ideas ready for filtering")
    print()

    # Step 4: Already have AI ideas above

    # Step 5: Filter
    print("  🔧 [Step 5] Running 5-Layer Convergence Filter...")
    print()

    results = five_layer_filter(
        AI_GENERATED_IDEAS,
        user_pain_points=INTERVIEW["round2_pain_points"],
        web_evidence_list=SEARCH_RESULTS,
        verbose=True,
    )

    # Step 6: Preview
    print()
    print("=" * 65)
    print("  📊 [Step 6] Filtered Ideas Preview")
    print("=" * 65)
    print()
    print(f"  {'#':<4} {'Title':<32} {'Feas.':<6} {'Nov.':<6} {'Dim':<4}")
    print(f"  {'—'*3} {'—'*30} {'—'*5} {'—'*5} {'—'*3}")
    for i, r in enumerate(results, 1):
        idea = r["idea"]
        print(f"  {i:<4} {idea['title']:<32} {idea['feasibility_score']:<6} {idea['novelty_score']:<6} {idea['dimension']:<4}")

    # Step 7: Refinement (simulated)
    print()
    print("  📝 [Step 7] Deep Refinement — pick one idea")
    print()
    print("  Selected: Anti-Jam Auger Feeder (highest feasibility + solves #1 pain)")
    print()

    # Print a sample refinement summary
    winner = results[0]["idea"] if results else None
    if winner:
        print("  ╔" + "═" * 55 + "╗")
        print(f"  ║  {winner['title']} — Project Plan Summary{' ' * (40 - len(winner['title']))}║")
        print("  ╠" + "═" * 55 + "╣")
        print(f"  ║  Position:  {winner['one_line']}")
        print(f"  ║  Users:     {winner['target_user']}")
        print(f"  ║  Core:      {winner['core_value']}")
        print(f"  ║  Evidence:  {winner['web_evidence_summary']}")
        print(f"  ║  Feasibility: {'⭐' * winner['feasibility_score']}")
        print(f"  ║  Novelty:     {'⭐' * winner['novelty_score']}")
        print("  ╚" + "═" * 55 + "╝")

    print()
    print("=" * 65)
    print("  ✅ Full pipeline demo complete!")
    print()
    print("  Next steps:")
    print("    pip install inspiration-filter")
    print("    inspiration-demo")
    print("    cat ideas.json | inspiration-filter")
    print("=" * 65)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Inspiration · One-shot demo
=============================
Run without any arguments to see the filter engine in action.

Usage:
    inspiration-demo                  # interactive demo
    python -m inspiration.demo         # same thing
"""

from agent_spark.filter.five_layer_filter import five_layer_filter


def main():
    """Run a self-contained demo of the 5-layer filter engine."""
    print("=" * 60)
    print("  ✨ Agent Spark — Demo")
    print("  Industrial-Grade Creative Idea Pipeline")
    print("=" * 60)
    print()

    sample_ideas = [
        {
            "title": "Modular Expandable Shelf",
            "one_line": "Free-splice shelving units that fit any cabinet size",
            "target_user": "Renters, small-apartment dwellers",
            "core_value": "No measuring, modular assembly, move-friendly",
            "pain_point_solved": "Fixed shelves never fit rental apartment cabinets",
            "web_evidence_summary": "200+ Reddit posts about ill-fitting shelves; IKEA hack communities",
            "feasibility_score": 4,
            "novelty_score": 4,
            "tags": ["furniture", "modular", "rental", "IKEA-hack"],
        },
        {
            "title": "Pet Sitter Trust Network",
            "one_line": "Neighbor-to-neighbor pet sitting with verified trust and insurance",
            "target_user": "Pet owners who travel and their neighbors",
            "core_value": "Solve the trust gap in peer-to-peer pet care",
            "pain_point_solved": "Kennels are expensive and stressful; friends aren't always available",
            "web_evidence_summary": "Rover.com reviews mention trust/safety concerns; nextdoor.com pet-sitting requests growing 40% YoY",
            "feasibility_score": 3,
            "novelty_score": 3,
            "tags": ["pet", "sharing-economy", "trust"],
        },
        {
            "title": "Smart Notebook OCR Fix",
            "one_line": "Eliminate OCR errors in digitized handwritten notes with AI correction",
            "target_user": "Students, professionals, creatives",
            "core_value": "Enable perfect search and organization of handwritten content",
            "pain_point_solved": "Handwritten notes are hard to search, organize, and digitize",
            "web_evidence_summary": "Rocketbook Amazon reviews mention OCR quality issues; Evernote users complain about scanning workflow",
            "feasibility_score": 3,
            "novelty_score": 3,
            "tags": ["productivity", "AI", "note-taking"],
        },
        {
            "title": "Blockchain IoT Platform",
            "one_line": "Decentralized IoT data marketplace powered by blockchain",
            "target_user": "Enterprises, IoT developers",
            "core_value": "Monetize sensor data securely",
            "pain_point_solved": "IoT data is siloed and under-monetized",
            "web_evidence_summary": "",
            "feasibility_score": 1,
            "novelty_score": 5,
            "tags": ["blockchain", "IoT", "Web3"],
        },
        {
            "title": "一键生成周报工具",
            "one_line": "输入关键词一键生成完整周报",
            "target_user": "上班族",
            "core_value": "写周报不费脑",
            "pain_point_solved": "写周报太浪费时间",
            "web_evidence_summary": "职场社区大量周报吐槽",
            "feasibility_score": 3,
            "novelty_score": 1,
            "tags": ["办公", "效率", "自动化"],
        },
    ]

    print("📥 Processing 5 sample ideas through the 5-layer filter...")
    print()

    results = five_layer_filter(
        sample_ideas,
        user_pain_points=[
            "Shelves don't fit small apartments",
            "Pet sitters are hard to trust",
            "写周报太麻烦",
        ],
        web_evidence_list=[
            "Reddit: shelving complaints IKEA hack",
            "Rover.com trust concerns",
        ],
    )

    print()
    print("=" * 60)
    print("  📊 Results Summary")
    print("=" * 60)
    print(f"  Total ideas: {len(sample_ideas)}")
    print(f"  Passed:      {len(results)}")
    print(f"  Failed:      {len(sample_ideas) - len(results)}")
    print()

    passed_titles = [r["title"] for r in results]
    failed_titles = [
        sample_ideas[i]["title"]
        for i in range(len(sample_ideas))
        if not any(r["index"] == i for r in results)
    ]

    print("  ✅ Passed:")
    for t in passed_titles:
        print(f"     • {t}")

    print()
    print("  ❌ Filtered out:")
    for t in failed_titles:
        print(f"     • {t}")

    print()
    print("=" * 60)
    print("  ✨ Demo complete!  Try `inspiration-filter ideas.json`")
    print("     or import in your own project:")
    print()
    print("     from agent_spark.filter.five_layer_filter import five_layer_filter")
    print("=" * 60)


if __name__ == "__main__":
    main()

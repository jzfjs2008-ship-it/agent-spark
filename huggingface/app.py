#!/usr/bin/env python3
"""
Inspiration · Streamlit Web UI
================================
Interactive playground for the 5-layer filter engine.

Usage:
    pip install streamlit
    streamlit run app/playground.py
"""

import json
import sys
import os

# Ensure package is importable — remove when installed via pip
if not any('agent_spark' in p for p in sys.path):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import streamlit as st
except ImportError:
    print("Streamlit not installed. Run: pip install streamlit")
    sys.exit(1)

from agent_spark.filter.five_layer_filter import five_layer_filter

st.set_page_config(
    page_title="Agent Spark · Filter Playground",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Agent Spark · Filter Playground")
st.markdown(
    "Test the 5-layer convergence filter with your own ideas. "
    "No API key, no internet — everything runs locally."
)

# ── Sidebar: Input ──
st.sidebar.header("📥 Input")

sample_json = json.dumps([
    {
        "title": "Modular Expandable Shelf",
        "one_line": "Free-splice shelving that fits any cabinet",
        "target_user": "Renters",
        "core_value": "No measuring, modular, move-friendly",
        "pain_point_solved": "Fixed shelves never fit rental apartments",
        "web_evidence_summary": "200+ Reddit posts about ill-fitting shelves",
        "feasibility_score": 4,
        "novelty_score": 4,
        "tags": ["furniture", "modular"],
    },
    {
        "title": "Blockchain Shelf Platform",
        "one_line": "Decentralize home organization with Web3",
        "target_user": "Everyone",
        "core_value": "Empower the shelving ecosystem",
        "pain_point_solved": "Efficiency issues",
        "web_evidence_summary": "",
        "feasibility_score": 1,
        "novelty_score": 5,
        "tags": ["blockchain", "Web3"],
    },
], indent=2)

ideas_json = st.sidebar.text_area(
    "Ideas (JSON array)",
    value=sample_json,
    height=300,
)

pain_points = st.sidebar.text_area(
    "User pain points (one per line)",
    value="Shelves don't fit\nMoving is hard",
    height=80,
)

web_evidence = st.sidebar.text_area(
    "Web evidence (one per line)",
    value="Reddit: shelving complaints",
    height=80,
)

run = st.sidebar.button("▶ Run Filter", type="primary", use_container_width=True)

# ── Main: Results ──
st.header("📊 Filter Results")

if run:
    try:
        ideas = json.loads(ideas_json)
        pain_list = [p.strip() for p in pain_points.split("\n") if p.strip()]
        web_list = [w.strip() for w in web_evidence.split("\n") if w.strip()]

        if not isinstance(ideas, list):
            st.error("Input must be a JSON array")
            st.stop()

        if not ideas:
            st.warning("Add at least one idea to filter")
            st.stop()

        results = five_layer_filter(ideas, pain_list, web_list, verbose=False)

        # Stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ideas", len(ideas))
        col2.metric("✅ Passed", len(results))
        col3.metric("❌ Filtered", len(ideas) - len(results))

        # Detailed results
        st.subheader("Per-Idea Breakdown")

        for i, idea in enumerate(ideas):
            report = next((r for r in results if r["index"] == i), None)
            passed = report is not None

            with st.expander(
                f"{'✅' if passed else '❌'} {idea.get('title', f'Idea #{i}')}",
                expanded=not passed,
            ):
                col_a, col_b = st.columns([1, 2])

                with col_a:
                    st.json(idea)

                with col_b:
                    if passed:
                        for layer_name, layer_data in report["layers"].items():
                            st.success(f"**{layer_name}**: {layer_data['message']}")
                    else:
                        st.error("**Filtered out** — does not appear in results above")

        # Passed ideas summary
        if results:
            st.subheader("✅ Passed Ideas")
            for r in results:
                idx = r["index"]
                if 0 <= idx < len(ideas):
                    idea = ideas[idx]
                    st.success(f"**{idea['title']}** — {idea.get('one_line', '')}")

    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👈 Enter your ideas in the sidebar and click 'Run Filter'")

# ── Footer ──
st.divider()
st.caption(
    "✨ [Inspiration](https://github.com/jzfjs2008-ship-it/inspiration) "
    "· Industrial-grade creative idea pipeline · MIT License"
)

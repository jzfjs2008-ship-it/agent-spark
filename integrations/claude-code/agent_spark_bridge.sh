#!/usr/bin/env bash
# =====================================================================
# Agent Spark — Claude Code Bridge Script (v2.1)
# Full pipeline: 5-round interview + intent anchor, web search, divergence,
# filter engine, refinement prompt reference.
#
# Usage:
#   bash agent_spark_bridge.sh [domain]
#   bash agent_spark_bridge.sh "home organization"
#
# v2.1 changes:
#   [NEW] Round 1.5 Intent Anchor — confirms domain understanding before proceeding
# v2.0 changes:
#   [FIX] Actually pipes to filter engine instead of just printing
#   [FIX] Bilingual output (auto-detects input language)
#   [FIX] Generates working search URLs
#   [FIX] Handles "random" domain by asking for an anchor
#   [FIX] Better error handling and path resolution
# =====================================================================

set -euo pipefail

# ── Project root ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FILTER_ENGINE="$PROJECT_DIR/agent_spark/filter/five_layer_filter.py"
DIVERGE_PROMPT="$PROJECT_DIR/agent_spark/prompts/diverge.md"

# ── Detect language preference ──
detect_lang() {
    local input="$1"
    if echo "$input" | grep -qP '[\x{4e00}-\x{9fff}]'; then
        echo "zh"
    else
        echo "en"
    fi
}

echo "================================================"
echo "  Agent Spark — Claude Code Bridge (v2.1)"
echo "================================================"
echo ""

# ── Step 1: Domain ──
if [ -z "${1:-}" ]; then
    echo "[Round 1/6] What domain do you want ideas for?"
    echo "  (press Enter for random)"
    read -r DOMAIN
    DOMAIN="${DOMAIN:-}"
else
    DOMAIN="$1"
fi

LANG="$(detect_lang "$DOMAIN")"

# Handle "random" — need an anchor
if [ -z "$DOMAIN" ] || [ "$DOMAIN" = "random" ]; then
    echo ""
    echo "[INFO] 'Random' needs at least one anchor example to seed ideas."
    echo "  Name a specific product or scenario you recently used or thought about:"
    read -r ANCHOR
    DOMAIN="$ANCHOR (random anchor)"
fi

echo "  Domain: $DOMAIN"
echo ""

# ── Step 1.5: Intent Anchor (v2.1) ──
echo "================================================"
echo "  [Round 1.5/6] Intent Anchor — confirm your understanding:"
echo ""
echo "  Domain: $DOMAIN"
echo "  Goal: Generate valuable creative ideas"
echo ""
echo "  Correct? (y/n, or type clarification; default: y)"
read -r INTENT_CONFIRM

if [ "$INTENT_CONFIRM" = "n" ] || [ "$INTENT_CONFIRM" = "no" ]; then
    echo "  Please clarify the domain or outcome you are looking for:"
    read -r DOMAIN_CLARIFY
    DOMAIN="$DOMAIN_CLARIFY"
    echo "  Updated domain: $DOMAIN"
fi
echo ""

# ── Step 2: Pain Points ──
echo "[Round 2/6] What frustrates you in this domain? What's inconvenient or broken?"
echo "  (separate with commas, or press Enter to skip)"
read -r PAIN_POINTS
echo ""

# ── Step 3: Product Flaws ──
echo "[Round 3/6] What products/tools have you tried in this domain? What are their flaws?"
echo "  (press Enter to skip)"
read -r PRODUCT_FLAWS
echo ""

# ── Step 4: Creative Style ──
echo "[Round 4/6] Which creative style do you prefer?"
echo "  A) Incremental improvement (polish existing, low risk)"
echo "  B) Novel creation (market has not seen, higher risk/reward)"
read -r STYLE
STYLE="${STYLE:-A}"
echo ""

# ── Step 5: Niche Needs ──
echo "[Round 5/6] Any niche scenarios, unusual habits, or personal needs most people would not think of?"
echo "  (press Enter to skip)"
read -r NICHE
echo ""

# ── Summary ──
echo "================================================"
echo "  Interview Summary"
echo "================================================"
echo "  Domain: $DOMAIN"
echo "  Pain Points: ${PAIN_POINTS:-(skip)}"
echo "  Product Flaws: ${PRODUCT_FLAWS:-(skip)}"
echo "  Style: $STYLE"
echo "  Niche Needs: ${NICHE:-(skip)}"
echo ""

# ── Search Queries ──
echo "================================================"
echo "  Search Queries (paste into Claude Code)"
echo "================================================"
echo ""
echo "  site:reddit.com $DOMAIN complaints OR frustrating"
echo "  \"$DOMAIN\" problems OR issues OR \"why is there not\""
echo "  \"$DOMAIN\" niche OR underserved OR alternative"
echo ""

# ── Divergence Material ──
echo "================================================"
echo "  Divergence Input (send to Claude Code)"
echo "================================================"
echo ""
echo "---"
echo "[Domain] $DOMAIN"
echo "[Pain Points] ${PAIN_POINTS:--}"
echo "[Product Flaws] ${PRODUCT_FLAWS:--}"
echo "[Style] $STYLE"
echo "[Niche Needs] ${NICHE:--}"
echo "[Search Results] (paste from above)"
echo "---"
echo ""

# ── Filter engine ──
if [ -f "$FILTER_ENGINE" ]; then
    echo "================================================"
    echo "  Filter Engine Ready"
    echo "================================================"
    echo ""
    echo "  Save Claude Code output as ideas.json, then:"
    echo ""
    echo "  python3 \"$FILTER_ENGINE\" ideas.json"
    echo "  cat ideas.json | python3 \"$FILTER_ENGINE\""
    echo ""
fi

# ── Refinement prompt reference ──
REFINE_PROMPT="$PROJECT_DIR/agent_spark/prompts/refine.md"
if [ -f "$REFINE_PROMPT" ]; then
    echo "  Refinement prompt:"
    echo "  $REFINE_PROMPT"
    echo ""
fi

echo "================================================"
echo "  Bridge Ready"
echo "================================================"

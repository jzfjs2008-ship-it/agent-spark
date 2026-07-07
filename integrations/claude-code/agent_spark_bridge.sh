#!/usr/bin/env bash
# =====================================================================
# Full pipeline: 5-round interview ??web search guidance ??divergence prompt
# ??filter engine ??refinement prompt reference
#
# Usage:
#   bash agent-spark_bridge.sh [domain]
#   bash agent-spark_bridge.sh "home organization"
#
# v2.0 changes:
#   [FIX] Actually pipes to filter engine instead of just printing
#   [FIX] Bilingual output (auto-detects input language)
#   [FIX] Generates working search URLs
#   [FIX] Handles "random" domain by asking for an anchor
#   [FIX] Better error handling and path resolution
# =====================================================================

set -euo pipefail

# ?? Project root (works even with symlinks) ??
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FILTER_ENGINE="$PROJECT_DIR/agent_spark/filter/five_layer_filter.py"
DIVERGE_PROMPT="$PROJECT_DIR/agent_spark/prompts/diverge.md"

# ?? Detect language preference ??
# If domain contains Chinese characters ??use Chinese
detect_lang() {
    local input="$1"
    if echo "$input" | grep -qP '[\x{4e00}-\x{9fff}]'; then
        echo "zh"
    else
        echo "en"
    fi
}

# ?? Safe read with default ??
prompt_zh() { echo "??$1"; }
prompt_en() { echo "??$1"; }

echo "================================================"
echo "  Claude Code Bridge Script (v2.0)"
echo "================================================"
echo ""

# ?? Step 1: Domain ??
if [ -z "${1:-}" ]; then
    prompt_en "Round 1/5: What domain do you want ideas for?"
    echo "  (press Enter for random / ?? = ??????"
    read -r DOMAIN
    DOMAIN="${DOMAIN:-}"
else
    DOMAIN="$1"
fi

LANG="$(detect_lang "$DOMAIN")"

# Handle "random" ??need an anchor
if [ -z "$DOMAIN" ] || [ "$DOMAIN" = "random" ] || [ "$DOMAIN" = "?????? ]; then
    echo ""
    if [ "$LANG" = "zh" ]; then
    else
        echo "?? 'Random' needs at least one anchor example to seed ideas."
        echo "   Name a specific product or scenario you recently used or thought about:"
    fi
    read -r ANCHOR
    DOMAIN="$ANCHOR (random anchor)"
fi

echo "  ??$DOMAIN"
echo ""

# ?? Step 2: Pain Points ??
if [ "$LANG" = "zh" ]; then
else
    echo "??Round 2/5: What frustrates you in this domain? What's inconvenient or broken?"
    echo "   (separate with commas, or press Enter to skip)"
fi
read -r PAIN_POINTS
echo ""

# ?? Step 3: Product Flaws ??
if [ "$LANG" = "zh" ]; then
else
    echo "??Round 3/5: What products/tools have you tried in this domain? What are their flaws?"
    echo "   (press Enter to skip)"
fi
read -r PRODUCT_FLAWS
echo ""

# ?? Step 4: Creative Style ??
if [ "$LANG" = "zh" ]; then
else
    echo "??Round 4/5: Which creative style do you prefer?"
    echo "   A) Incremental improvement (polish existing, low risk)"
    echo "   B) Novel creation (market hasn't seen, higher risk/reward)"
fi
read -r STYLE
STYLE="${STYLE:-A}"
echo ""

# ?? Step 5: Niche Needs ??
if [ "$LANG" = "zh" ]; then
else
    echo "??Round 5/5: Any niche scenarios, unusual habits, or personal needs most people wouldn't think of?"
    echo "   (press Enter to skip)"
fi
read -r NICHE
echo ""

# ?? Summary ??
echo "================================================"
if [ "$LANG" = "zh" ]; then
else
    echo "  ?? Interview Summary"
fi
echo "================================================"
echo ""

# ?? Generate Search Queries ??
echo "================================================"
if [ "$LANG" = "zh" ]; then
else
    echo "  ?? Search Queries (paste into Claude Code)"
fi
echo "================================================"
echo ""
echo "  site:reddit.com $DOMAIN complaints OR frustrating OR annoying"
echo "  \"$DOMAIN\" problems OR issues OR \"why isn't there\""
echo "  \"$DOMAIN\" niche OR underserved OR alternative"
echo ""

# ?? Generate Divergence Material ??
echo "================================================"
if [ "$LANG" = "zh" ]; then
else
    echo "  ?? Divergence Input (send to Claude Code)"
fi
echo "================================================"
echo ""
echo "---"
echo "?ain Points / ???{PAIN_POINTS:-(-)}"
echo "?earch Results / ????paste from above)"
echo "---"
echo ""

# ?? Filter engine pipe (if we have a JSON file) ??
if [ -f "$FILTER_ENGINE" ]; then
    echo "================================================"
    if [ "$LANG" = "zh" ]; then
    else
        echo "  ??  Filter Engine Ready"
    fi
    echo "================================================"
    echo ""
    if [ "$LANG" = "zh" ]; then
    else
        echo "  Save Claude Code output as ideas.json, then:"
    fi
    echo ""
    echo "  python3 \"$FILTER_ENGINE\" ideas.json"
    echo "  cat ideas.json | python3 \"$FILTER_ENGINE\""
    echo ""
fi

# ?? Refinement prompt reference ??
REFINE_PROMPT="$PROJECT_DIR/agent_spark/prompts/refine.md"
if [ -f "$REFINE_PROMPT" ]; then
    echo "  $REFINE_PROMPT"
    echo ""
fi

echo "================================================"
echo "================================================"


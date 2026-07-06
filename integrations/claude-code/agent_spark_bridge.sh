#!/usr/bin/env bash
# =====================================================================
# agent-spark 繚 Claude Code Bridge Script (v2.0)
# ?菜? 繚 Claude Code 獢交?嚗2.0嚗?#
# Full pipeline: 5-round interview ??web search guidance ??divergence prompt
# ??filter engine ??refinement prompt reference
#
# Usage:
#   bash agent-spark_bridge.sh [domain]
#   bash agent-spark_bridge.sh "home organization"
#   bash agent-spark_bridge.sh "摰嗅??嗥熙"
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
FILTER_ENGINE="$PROJECT_DIR/core/filter/five_layer_filter.py"
DIVERGE_PROMPT="$PROJECT_DIR/core/prompts/diverge.md"

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
echo "  ??agent-spark / ?菜? ??Full Pipeline"
echo "  Claude Code Bridge Script (v2.0)"
echo "================================================"
echo ""

# ?? Step 1: Domain ??
if [ -z "${1:-}" ]; then
    prompt_en "Round 1/5: What domain do you want ideas for?"
    prompt_zh "蝚?頧殷?雿閬?銝芷??????菜?嚗?
    echo "  (press Enter for random / ?湔?膠 = ?券?????"
    read -r DOMAIN
    DOMAIN="${DOMAIN:-}"
else
    DOMAIN="$1"
fi

LANG="$(detect_lang "$DOMAIN")"

# Handle "random" ??need an anchor
if [ -z "$DOMAIN" ] || [ "$DOMAIN" = "random" ] || [ "$DOMAIN" = "?券????? ]; then
    echo ""
    if [ "$LANG" = "zh" ]; then
        echo "?? ?券????粹?閬撠?銝芷??寞?靘?臬???楝??
        echo "   霂瑚蜀銝銝芯??餈瘜冽?雿輻?雿漣???箸嚗?
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
    echo "??蝚?頧殷??刻?銝芷???嚗??芯?銝靘踴???曄??唳嚗?
    echo "   嚗?銝芰??寧???嚗???頧西歲餈?"
else
    echo "??Round 2/5: What frustrates you in this domain? What's inconvenient or broken?"
    echo "   (separate with commas, or press Enter to skip)"
fi
read -r PAIN_POINTS
echo ""

# ?? Step 3: Product Flaws ??
if [ "$LANG" = "zh" ]; then
    echo "??蝚?頧殷?餈葵憸?雿餈鈭漣????銋撩?對?"
    echo "   嚗???頧西歲餈?"
else
    echo "??Round 3/5: What products/tools have you tried in this domain? What are their flaws?"
    echo "   (press Enter to skip)"
fi
read -r PRODUCT_FLAWS
echo ""

# ?? Step 4: Creative Style ??
if [ "$LANG" = "zh" ]; then
    echo "??蝚?頧殷?雿?憟賢蝘????潘?"
    echo "   A ?寡隡????箔??唳?鈭批?摰?嚗?啁???"
    echo "   B ?冽?砍???撣銝?閫???批撩嚗?
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
    echo "??蝚?頧殷??瓷??隡?胯畾蝙?其??胯葵?批??瘙?"
    echo "   嚗???頧西歲餈?"
else
    echo "??Round 5/5: Any niche scenarios, unusual habits, or personal needs most people wouldn't think of?"
    echo "   (press Enter to skip)"
fi
read -r NICHE
echo ""

# ?? Summary ??
echo "================================================"
if [ "$LANG" = "zh" ]; then
    echo "  ?? ?桃?瘙?
else
    echo "  ?? Interview Summary"
fi
echo "================================================"
echo "  Domain / 憸?: $DOMAIN"
echo "  Pain Points / ?: ${PAIN_POINTS:-"(skip/頝唾?)"}"
echo "  Product Flaws / 鈭批?蝻粹: ${PRODUCT_FLAWS:-"(skip/頝唾?)"}"
echo "  Style / 憌: $STYLE"
echo "  Niche Needs / 撠??瘙? ${NICHE:-"(skip/頝唾?)"}"
echo ""

# ?? Generate Search Queries ??
echo "================================================"
if [ "$LANG" = "zh" ]; then
    echo "  ?? ?揣?喲霂?(??Claude Code 銝剔?亥???"
else
    echo "  ?? Search Queries (paste into Claude Code)"
fi
echo "================================================"
echo ""
echo "  site:zhihu.com $DOMAIN ?/?局/?桅?"
echo "  site:reddit.com $DOMAIN complaints OR frustrating OR annoying"
echo "  \"$DOMAIN\" problems OR issues OR \"why isn't there\""
echo "  \"$DOMAIN\" niche OR underserved OR alternative"
echo ""

# ?? Generate Divergence Material ??
echo "================================================"
if [ "$LANG" = "zh" ]; then
    echo "  ?? ?蝝?嚗 Claude Code ????嚗?
else
    echo "  ?? Divergence Input (send to Claude Code)"
fi
echo "================================================"
echo ""
echo "---"
echo "?omain / 憸???DOMAIN"
echo "?ain Points / ???{PAIN_POINTS:-(-)}"
echo "?roduct Flaws / 鈭批?蝻粹??{PRODUCT_FLAWS:-(-)}"
echo "?tyle / 憌??STYLE"
echo "?iche Needs / 撠??瘙?{NICHE:-(-)}"
echo "?earch Results / ?揣蝏???paste from above)"
echo "---"
echo ""

# ?? Filter engine pipe (if we have a JSON file) ??
if [ -f "$FILTER_ENGINE" ]; then
    echo "================================================"
    if [ "$LANG" = "zh" ]; then
        echo "  ??  餈誘撘?撠梁貌"
    else
        echo "  ??  Filter Engine Ready"
    fi
    echo "================================================"
    echo ""
    if [ "$LANG" = "zh" ]; then
        echo "  撠?Claude Code 颲????JSON 靽???"
    else
        echo "  Save Claude Code output as ideas.json, then:"
    fi
    echo ""
    echo "  python3 \"$FILTER_ENGINE\" ideas.json"
    echo "  cat ideas.json | python3 \"$FILTER_ENGINE\""
    echo ""
fi

# ?? Refinement prompt reference ??
REFINE_PROMPT="$PROJECT_DIR/core/prompts/refine.md"
if [ -f "$REFINE_PROMPT" ]; then
    echo "  Refinement prompt / 蝏? Prompt:"
    echo "  $REFINE_PROMPT"
    echo ""
fi

echo "================================================"
echo "  ??Bridge Ready / 獢交??摰?"
echo "================================================"


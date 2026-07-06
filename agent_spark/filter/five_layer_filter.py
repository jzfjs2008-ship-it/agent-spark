#!/usr/bin/env python3
"""
Inspiration · Five-Layer Industrial Convergence Filter
Five-Layer Industrial Convergence Filter
=========================================================
Core quality-control engine — hybrid rule-based + AI-assisted validation.
Core quality-control engine — rule-based + AI-assisted validation.

Key fixes vs v1.0:
  [FIX] L1: replaced pure word-count check with actual fact validation
  [FIX] L2: removed Chinese-ignorant len<20 check; added real logic conflict detection
  [FIX] L4: replaced substring 'in' matching with token-level keyword scoring
  [FIX] CLI: added try/except, encoding, JSONL support, empty-input handling
  [FIX] L3: hardware keywords no longer auto-fail; scored by context weight
  [FIX] All Chinese-only messages → bilingual; English primary

Author: Hermes Agent
Version: 2.0.0
"""

import json
import re
import sys
from typing import Any

Idea = dict[str, Any]

# ─────────────────────────────────────────────────────────
# CONFIGURATION LOADING
# Config — load from JSON, fall back to hardcoded
# ─────────────────────────────────────────────────────────

import os

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
_DEFAULTS_PATH = os.path.join(_DATA_DIR, "defaults.json")

def _load_config() -> dict[str, Any]:
    """Load configuration from defaults.json, falling back to empty dict."""
    if os.path.isfile(_DEFAULTS_PATH):
        try:
            with open(_DEFAULTS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


_CONFIG = _load_config()

# ─────────────────────────────────────────────────────────
# MATURE PRODUCT DATABASE (extensible, token-scored)
# Mature product DB (extensible, token-weighted scoring)
# ─────────────────────────────────────────────────────────
# Each entry has weighted keywords: (term, weight).
# Higher weight = more distinctive for that product.
# Generic words like "AI" get lower weight to avoid false positives.
# Can be customized by editing inspiration/data/defaults.json

MATURE_PRODUCTS: list[dict[str, Any]] = _CONFIG.get("products") or [
    # Office / productivity
    {"name": "Notion", "field": "notes/docs", "keywords": {"笔记": 3, "文档": 2, "知识库": 3, "wiki": 3, "database": 2, "block": 2}},
    {"name": "飞书/Lark", "field": "collaboration", "keywords": {"办公": 1, "协作": 3, "文档": 1, "IM": 2, "会议": 2, "OKR": 3}},
    {"name": "Slack", "field": "team chat", "keywords": {"团队": 2, "聊天": 1, "channel": 3, "通讯": 1, "集成": 2, "bot": 2}},
    {"name": "Obsidian", "field": "knowledge mgmt", "keywords": {"笔记": 2, "双向链接": 4, "图谱": 3, "本地": 2, "markdown": 1, "插件": 2}},
    {"name": "微信", "field": "social/chat", "keywords": {"社交": 2, "聊天": 2, "朋友圈": 3, "小程序": 3, "支付": 2, "公众号": 3}},
    # Design
    {"name": "Figma", "field": "UI design", "keywords": {"设计": 1, "UI": 3, "原型": 3, "协作设计": 4, "组件": 2, "auto layout": 3}},
    {"name": "Canva", "field": "graphic design", "keywords": {"设计": 1, "模板": 3, "海报": 3, "图形": 1, "拖拽": 2, "社交媒体": 2}},
    # AI/LLM
    {"name": "ChatGPT", "field": "AI chat", "keywords": {"AI": 1, "对话": 2, "LLM": 2, "大模型": 2, "聊天机器人": 2, "GPT": 4}},
    {"name": "Claude", "field": "AI chat", "keywords": {"AI": 1, "对话": 2, "长文": 3, "分析": 2, "Claude": 4, "artifacts": 3}},
    {"name": "Cursor", "field": "AI coding", "keywords": {"AI编程": 4, "代码生成": 3, "Copilot": 2, "编辑器": 2, "IDE": 2, "自动补全": 2}},
    # E-commerce / life
    {"name": "小红书", "field": "social/lifestyle", "keywords": {"种草": 4, "笔记": 1, "生活方式": 3, "评测": 2, "分享": 1, "社区": 2}},
    {"name": "拼多多", "field": "e-commerce", "keywords": {"拼团": 4, "低价": 2, "社交电商": 3, "砍价": 3, "百亿补贴": 3}},
    {"name": "抖音/TikTok", "field": "short video", "keywords": {"短视频": 3, "直播": 2, "算法推荐": 3, "内容": 1, "feed": 2, "带货": 2}},
    # Hard to distinguish by simple keywords — keep for reference only
    {"name": "Photoshop", "field": "image editing", "keywords": {"修图": 3, "PS": 4, "图像处理": 2, "滤镜": 2, "图层": 3, "蒙版": 3}},
    {"name": "GitHub", "field": "code hosting", "keywords": {"代码": 1, "版本控制": 3, "开源": 3, "PR": 3, "issue": 2, "仓库": 2}},
]

# Jargon / buzzword blacklist (layer 5)
# Can be customized by editing inspiration/data/defaults.json
BUZZWORD_BLACKLIST: list[str] = _CONFIG.get("buzzwords") or [
    "智能", "AI", "互联网+", "数字化", "云端", "大数据",
    "区块链", "元宇宙", "赋能", "生态", "闭环", "抓手",
    "打通", "对齐", "颗粒度", "底层逻辑", "降维打击",
    "颠覆", "重构", "重塑",
]

# Trivial idea patterns (layer 5)
TRIVIAL_PATTERNS: list[re.Pattern] = [
    re.compile(r"(?:做|开发|创建).*?(?:APP|小程序|网站|应用)", re.IGNORECASE),
    re.compile(r"用AI.*?(?:自动|智能|生成)", re.IGNORECASE),
    re.compile(r"一键.*?(?:生成|搞定|解决)", re.IGNORECASE),
    re.compile(r"(?:换个|换一换)颜色|换个样式|换肤|主题切换", re.IGNORECASE),
]

# ─────────────────────────────────────────────────────────
# LAYER 1: Fact Validation (fixed: real evidence, not char count)
# LAYER 1: Fact Validation (real evidence, not word-count)
# ─────────────────────────────────────────────────────────

def layer1_fact_check(
    idea: Idea,
    user_pain_points: list[str],
    web_evidence_list: list[str],
) -> tuple[bool, str]:
    """Check whether the idea is grounded in real needs, not AI hallucination.
    
    Strategy:
      - Accept if the idea's pain_point_solved mentions ANY user pain point.
      - Accept if web_evidence_summary contains ANY non-generic evidence string.
      - Reject only when BOTH are empty/generic.
      
    This avoids the v1.0 bug of rejecting real ideas for being "too short."
    """
    pain_solved = (idea.get("pain_point_solved") or "").strip()
    web_evidence = (idea.get("web_evidence_summary") or "").strip()
    title = (idea.get("title") or "").strip()
    one_line = (idea.get("one_line") or "").strip()

    # 1) Check user pain-point overlap using character bigrams
    # (substring 'in' is too fragile for Chinese — "猫砂盆清理麻烦" won't match "猫砂盆清理太麻烦")
    pain_matched = False
    for up in user_pain_points:
        up_clean = up.strip().lower()
        if not up_clean or len(up_clean) < 2:
            continue
        # Strategy A: exact substring match (works when user text is directly quoted)
        if up_clean in pain_solved.lower():
            pain_matched = True
            break
        if up_clean in (title + one_line).lower():
            pain_matched = True
            break
        # Strategy B: character bigram overlap for Chinese
        def bigrams(s: str) -> set[str]:
            return {s[i:i+2] for i in range(len(s)-1)}
        pain_bigrams = bigrams(up_clean)
        solved_bigrams = bigrams(pain_solved.lower())
        if len(pain_bigrams) > 0 and len(solved_bigrams) > 0:
            overlap = len(pain_bigrams & solved_bigrams)
            ratio = overlap / max(len(pain_bigrams), 1)
            if ratio >= 0.6:  # 60% bigram overlap = strong semantic match
                pain_matched = True
                break

    # 2) Check web-evidence quality
    evidence_matched = False
    for ev in web_evidence_list:
        ev_clean = ev.strip().lower()
        if ev_clean and len(ev_clean) >= 4:
            if ev_clean in web_evidence.lower():
                evidence_matched = True
                break

    # 3) Reject only if both are empty
    if not pain_solved and not web_evidence:
        return False, "[FAIL:L1] No pain point and no web evidence — likely AI hallucination"

    if pain_matched:
        return True, "[PASS:L1] Pain point matched user input"
    if evidence_matched:
        return True, "[PASS:L1] Supported by web evidence"

    # 4) Edge case: pain_solved exists but doesn't match any known pain point
    #   → accept if it has real content (not generic fluff)
    if pain_solved and len(pain_solved) >= 8:
        vague_patterns = [
            r"效率[低不高]",
            r"不够(好|智能|方便)",
            r"体验(差|不好)",
            r"太(麻烦|复杂|慢)",
        ]
        is_vague = any(re.search(p, pain_solved) for p in vague_patterns)
        if not is_vague or len(pain_solved) >= 20:
            return True, "[PASS:L1] Pain point has real content (no exact match but specific)"

    return False, f"[FAIL:L1] Pain point too vague or unsupported: '{pain_solved[:40]}...'"


# ─────────────────────────────────────────────────────────
# LAYER 2: Logic Validation (fixed: removed len<20 trap)
# LAYER 2: Logic Validation (no len<20 trap)
# ─────────────────────────────────────────────────────────

def layer2_logic_check(idea: Idea) -> tuple[bool, str]:
    """Check internal logical consistency of the idea."""

    title = (idea.get("title") or "").strip()
    one_line = (idea.get("one_line") or "").strip()
    core_value = (idea.get("core_value") or "").strip()
    target_user = (idea.get("target_user") or "").strip()

    checks: list[tuple[str, str, str | list[str]]] = []

    # Check 1: target_user too broad
    broad_user_signals = ["所有人", "everyone", "everybody", "all users", "任何人"]
    for signal in broad_user_signals:
        if signal.lower() in target_user.lower():
            return False, f"[FAIL:L2] Target user '{target_user}' is too broad — no product serves everyone"

    # Check 2: core_value too short to be meaningful
    if len(core_value) < 3:
        return False, "[FAIL:L2] Core value proposition is empty — no logical focus"

    # Check 3: self-contradiction: claims both "simple" and "powerful" without bridge logic
    has_simple = any(w in (one_line + core_value).lower() for w in ["简单", "simple", "easy", "轻量"])
    has_powerful = any(w in (one_line + core_value).lower() for w in ["强大", "powerful", "全能", "all-in-one"])
    if has_simple and has_powerful:
        bridge = any(w in one_line for w in ["但", "however", "yet", "同时", "while still"])
        if not bridge:
            return False, "[FAIL:L2] Claims both 'simple' and 'powerful' without explaining the trade-off"

    # Check 4: contradictory value dimensions
    combined = f"{title} {one_line} {core_value}".lower()
    contradiction_pairs = [
        (["免费", "free"], ["付费", "paid", "subscription", "收费"], "claims both free and paid"),
        (["离线", "offline", "local-only"], ["在线", "online", "cloud", "云端"], "contradicts offline vs online"),
        (["极简", "minimal"], ["复杂", "complex", "comprehensive", "全面"], "contradicts minimal vs comprehensive"),
    ]
    for group_a, group_b, reason in contradiction_pairs:
        has_a = any(w in combined for w in group_a)
        has_b = any(w in combined for w in group_b)
        if has_a and has_b:
            return False, f"[FAIL:L2] Logical contradiction: {reason}"

    # Check 5: min length sanity (not a hard cutoff, just flag extreme cases)
    if len(title) < 2:
        return False, "[FAIL:L2] Title too short (<2 chars)"
    if len(one_line) < 5:
        return False, "[FAIL:L2] Description too short (<5 chars)"

    return True, "[PASS:L2] Logic consistent"


# ─────────────────────────────────────────────────────────
# LAYER 3: Feasibility Validation (fixed: weighted scoring)
# LAYER 3: Feasibility (weighted scoring, no hard-keyword kill)
# ─────────────────────────────────────────────────────────

# Feasibility weights — each signal has a weight; sum > threshold = fail
# Can be customized by editing inspiration/data/defaults.json
_CONFIG_FS = _CONFIG.get("feasibility_signals")
if _CONFIG_FS and isinstance(_CONFIG_FS, list):
    FEASIBILITY_SIGNALS: list[tuple[re.Pattern, float, str]] = [
        (re.compile(s["pattern"]), s["weight"], s["label"])
        for s in _CONFIG_FS
        if "pattern" in s and "weight" in s and "label" in s
    ]
else:
    FEASIBILITY_SIGNALS: list[tuple[re.Pattern, float, str]] = [
        (re.compile(r"硬件|hardware|芯片|chip|开模|mold"), 2.0, "hardware-heavy"),
        (re.compile(r"生产线|manufacturing|工厂|factory"), 3.0, "requires manufacturing"),
        (re.compile(r"融资|funding|投资|invest"), 2.5, "needs external funding"),
        (re.compile(r"专利|patent|审批|approval|license|许可证"), 2.0, "regulatory hurdle"),
        (re.compile(r"团队.{0,4}(10|几十|百)"), 1.5, "large team required"),
        (re.compile(r"操作系统|OS|自研引擎|proprietary engine"), 2.5, "infra-level build"),
        (re.compile(r"自建(?:工厂|产线|数据中心)"), 3.0, "owns physical plant"),
        (re.compile(r"传感器|sensor"), 1.0, "uses sensors"),
        (re.compile(r"多端同步|multi-platform"), 0.8, "multi-platform"),
        (re.compile(r"实时通信|realtime"), 0.8, "realtime requirement"),
        (re.compile(r"高并发|high concurrency"), 1.0, "high-concurrency need"),
    ]

FEASIBILITY_THRESHOLD: float = _CONFIG.get("feasibility_threshold", 4.0)
MATURE_DUPLICATE_THRESHOLD: float = _CONFIG.get("market_duplicate_threshold", 6.0)


def layer3_feasibility_check(idea: Idea) -> tuple[bool, str]:
    """Check idea feasibility using weighted signal scoring.
    
    v2.0 fix: replaced binary keyword elimination with weighted scoring.
    "hardware" alone no longer kills an idea — it needs ≥4.0 total weight.
    """
    # Respect AI-generated score if present
    score = idea.get("feasibility_score")
    if isinstance(score, (int, float)) and score <= 0:
        return False, f"[FAIL:L3] AI self-assigned feasibility score {score}/5 is zero"

    all_text = " ".join([
        str(idea.get(k, "")) for k in ["title", "one_line", "core_value", "target_user"]
    ]).lower()

    total_weight = 0.0
    triggers: list[str] = []
    for pattern, weight, label in FEASIBILITY_SIGNALS:
        if pattern.search(all_text):
            total_weight += weight
            triggers.append(f"{label}(+{weight})")

    if total_weight > FEASIBILITY_THRESHOLD:
        return False, f"[FAIL:L3] Feasibility score {total_weight:.1f} > threshold {FEASIBILITY_THRESHOLD} — triggers: {', '.join(triggers)}"

    return True, f"[PASS:L3] Feasible (weight={total_weight:.1f})"


# ─────────────────────────────────────────────────────────
# LAYER 4: Market Duplicate Check (fixed: token-scored)
# LAYER 4: Market Duplicate (token-weighted scoring)
# ─────────────────────────────────────────────────────────

def layer4_market_repeat_check(idea: Idea) -> tuple[bool, str]:
    """Check if the idea duplicates an existing mature product.
    
    v2.0 fix: each keyword has a weight; weighted sum per product.
    A generic match like "AI" contributes only weight=1, not enough to fail.
    """
    combined = " ".join([
        str(idea.get(k, "")).lower() for k in ["title", "one_line", "core_value"]
    ])
    tags = " ".join(t.lower() for t in (idea.get("tags") or []))
    combined += " " + tags

    best_match: tuple[str, str, float] = ("", "", 0.0)

    for product in MATURE_PRODUCTS:
        score = 0.0
        matched_kws: list[str] = []
        for kw, weight in product["keywords"].items():
            if kw.lower() in combined:
                score += weight
                matched_kws.append(f"{kw}(+{weight})")

        if score > best_match[2]:
            best_match = (product["name"], product["field"], score)

        # threshold configurable via inspiration/data/defaults.json
        if score >= MATURE_DUPLICATE_THRESHOLD:
            return False, (
                f"[FAIL:L4] Highly duplicates '{product['name']}' ({product['field']})"
                f" — keyword score {score:.1f} ≥ {MATURE_DUPLICATE_THRESHOLD}"
            )

    return True, f"[PASS:L4] Best match '{best_match[0]}' ({best_match[1]}) score={best_match[2]:.1f} < {MATURE_DUPLICATE_THRESHOLD}"


# ─────────────────────────────────────────────────────────
# LAYER 5: Value Validation
# LAYER 5: Value Validation
# ─────────────────────────────────────────────────────────

def layer5_value_check(idea: Idea) -> tuple[bool, str]:
    """Check whether the idea provides real value, not buzzword salad."""

    all_text = " ".join([
        str(idea.get(k, "")) for k in ["title", "one_line", "core_value", "target_user"]
    ]).lower()

    # 1) Buzzword density
    buzzword_hits = [w for w in BUZZWORD_BLACKLIST if w.lower() in all_text]
    if len(buzzword_hits) >= 3:
        return False, f"[FAIL:L5] Buzzword overload: {len(buzzword_hits)} buzzwords ({', '.join(buzzword_hits[:4])})"

    # 2) Trivial patterns
    for pat in TRIVIAL_PATTERNS:
        match = pat.search(all_text)
        if match:
            return False, f"[FAIL:L5] Trivial pattern matched: '{pat.pattern}'"

    # 3) Niche too narrow
    niche_signals = ["极少数", "个别人", "只有我", "我自己", "一两个人", "身边几个人",
                     "just me", "myself only", "a few friends"]
    for signal in niche_signals:
        if signal.lower() in all_text:
            return False, f"[FAIL:L5] Audience too narrow ('{signal}')"

    # 4) Value check: idea must solve something, not just "exist"
    solvers = ["解决", "solve", "eliminate", "remove", "reduce", "prevent",
               "帮助", "help", "enable", "allow", "make it easy",
               "适配", "适合", "满足", "优化", "改善", "提升",
               "提供", "支持", "实现", "无需", "自动", "自由",
               "smart", "intelligent", "adaptive", "adjustable",
               "modular", "flexible", "portable", "lightweight"]
    has_solver = any(s in all_text for s in solvers)
    if not has_solver and len(all_text) >= 10:
        return False, "[FAIL:L5] No action verb indicating what problem it solves — just 'exists'"

    return True, "[PASS:L5] Valuable"


# ─────────────────────────────────────────────────────────
# MAIN FILTER ORCHESTRATOR
# 主过滤编排器
# ─────────────────────────────────────────────────────────

def five_layer_filter(
    ideas: list[Idea],
    user_pain_points: list[str] | None = None,
    web_evidence_list: list[str] | None = None,
    verbose: bool = True,
    locale: str | None = None,
) -> list[dict[str, Any]]:
    """Run all 5 layers on a batch of ideas.
    
    Args:
        ideas: AI-generated ideas to filter.
        user_pain_points: Real pain points from user.
        web_evidence_list: Web-sourced evidence strings.
        verbose: Print per-idea results.
        locale: "en", "zh", or None for auto-detect (from user_pain_points).
    """

    pain = user_pain_points or []
    evidence = web_evidence_list or []

    # ── Locale auto-detect ──
    if locale is None:
        locale = "zh" if any("\u4e00" <= c <= "\u9fff" for text in pain + evidence for c in text) else "en"
    _ = lambda en, zh: zh if locale == "zh" else en

    # ── Stats labels ──
    L = lambda en, zh: zh if locale == "zh" else en
    labels = {
        "total": _("Total", "总创意"),
        "fact": _("L1 Fact", "L1 事实"),
        "logic": _("L2 Logic", "L2 逻辑"),
        "feasibility": _("L3 Feasibility", "L3 落地性"),
        "market": _("L4 Market", "L4 市场"),
        "value": _("L5 Value", "L5 价值"),
        "passed": _("Passed", "通过"),
        "pass_rate": _("Pass rate", "通过率"),
    }

    passed: list[dict[str, Any]] = []
    stats = {
        "total": len(ideas),
        "L1_fact": 0, "L2_logic": 0,
        "L3_feasibility": 0, "L4_market": 0,
        "L5_value": 0, "passed": 0,
    }

    for idx, idea in enumerate(ideas):
        report: dict[str, Any] = {
            "index": idx,
            "title": idea.get("title", f"Idea#{idx}"),
            "layers": {},
            "passed": True,
        }

        # L1
        ok, msg = layer1_fact_check(idea, pain, evidence)
        report["layers"]["1_fact"] = {"passed": ok, "message": msg}
        if not ok:
            stats["L1_fact"] += 1
            report["passed"] = False
            if verbose:
                print(f"  ✗ [{idx+1}] {report['title']} → {msg}")
            continue

        # L2
        ok, msg = layer2_logic_check(idea)
        report["layers"]["2_logic"] = {"passed": ok, "message": msg}
        if not ok:
            stats["L2_logic"] += 1
            report["passed"] = False
            if verbose:
                print(f"  ✗ [{idx+1}] {report['title']} → {msg}")
            continue

        # L3
        ok, msg = layer3_feasibility_check(idea)
        report["layers"]["3_feasibility"] = {"passed": ok, "message": msg}
        if not ok:
            stats["L3_feasibility"] += 1
            report["passed"] = False
            if verbose:
                print(f"  ✗ [{idx+1}] {report['title']} → {msg}")
            continue

        # L4
        ok, msg = layer4_market_repeat_check(idea)
        report["layers"]["4_market"] = {"passed": ok, "message": msg}
        if not ok:
            stats["L4_market"] += 1
            report["passed"] = False
            if verbose:
                print(f"  ✗ [{idx+1}] {report['title']} → {msg}")
            continue

        # L5
        ok, msg = layer5_value_check(idea)
        report["layers"]["5_value"] = {"passed": ok, "message": msg}
        if not ok:
            stats["L5_value"] += 1
            report["passed"] = False
            if verbose:
                print(f"  ✗ [{idx+1}] {report['title']} → {msg}")
            continue

        report["passed"] = True
        passed.append(report)
        stats["passed"] += 1

    if verbose:
        print(f"\n{'='*55}")
        print(f"  📊 {_('Layer Filter Stats', '五层过滤统计')}")
        print(f"{'='*55}")
        print(f"  {_('Total', '总创意')}:     {stats['total']}")
        print(f"  {_('L1 Fact', 'L1 事实')}:     ✗ {stats['L1_fact']}")
        print(f"  {_('L2 Logic', 'L2 逻辑')}:    ✗ {stats['L2_logic']}")
        print(f"  {_('L3 Feasibility', 'L3 落地性')}:     ✗ {stats['L3_feasibility']}")
        print(f"  {_('L4 Market', 'L4 市场')}:   ✗ {stats['L4_market']}")
        print(f"  {_('L5 Value', 'L5 价值')}:    ✗ {stats['L5_value']}")
        print(f"  {'─'*45}")
        print(f"  ✅ {_('Passed', '通过')}:   {stats['passed']}/{stats['total']}")
        print(f"     {_('Pass rate', '通过率')}: {stats['passed']/max(stats['total'],1)*100:.1f}%")

    return passed


# ─────────────────────────────────────────────────────────
# CLI ENTRY (fixed: error handling, encoding, JSONL)
# CLI ENTRY (error handling, encoding, JSONL)
# ─────────────────────────────────────────────────────────

def main():
    """CLI entry point. Reads from file (argv) or stdin (pipe)."""
    raw_data: Any = None

    if len(sys.argv) > 1:
        # File mode
        input_path = sys.argv[1]
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
        except FileNotFoundError:
            print(json.dumps({"error": f"File not found: {input_path}"}, ensure_ascii=False))
            sys.exit(1)
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            sys.exit(1)
    else:
        # Stdin mode — check if data is available
        if sys.stdin.isatty():
            # Interactive mode with no input → show help
            print(json.dumps({"error": "No input. Pipe JSON or pass file path."}, ensure_ascii=False), file=sys.stderr)
            print("Usage:", file=sys.stderr)
            print("  python3 five_layer_filter.py ideas.json", file=sys.stderr)
            print("  cat ideas.json | python3 five_layer_filter.py", file=sys.stderr)
            sys.exit(1)
        raw_text = sys.stdin.read()

    if not raw_text or not raw_text.strip():
        print(json.dumps({"error": "Empty input"}, ensure_ascii=False))
        sys.exit(1)

    # Parse JSON (try array first, then object, then JSONL)
    try:
        raw_data = json.loads(raw_text)
    except json.JSONDecodeError:
        # Try JSONL: one JSON object per line
        try:
            lines = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]
            raw_data = [json.loads(l) for l in lines]
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON: {e}"}, ensure_ascii=False))
            sys.exit(1)

    # Normalize: ensure we have a list of ideas
    if isinstance(raw_data, dict):
        ideas = raw_data.get("ideas", [])
        pain_points = raw_data.get("user_pain_points", [])
        web_evidence = raw_data.get("web_evidence", [])
    elif isinstance(raw_data, list):
        ideas = raw_data
        pain_points = []
        web_evidence = []
    else:
        print(json.dumps({"error": "Input must be JSON array or {ideas: [...]}"}, ensure_ascii=False))
        sys.exit(1)

    results = five_layer_filter(ideas, pain_points, web_evidence)

    output = {
        "total": len(ideas),
        "passed": len(results),
        "passed_ideas": [r["idea"] for r in results],
        "full_reports": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

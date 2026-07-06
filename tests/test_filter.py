#!/usr/bin/env python3
"""
Comprehensive test suite for the 5-layer filter engine (v2.0).
Tests each layer's edge cases and boundary conditions.
"""
from agent_spark.filter.five_layer_filter import (
    layer1_fact_check,
    layer2_logic_check,
    layer3_feasibility_check,
    layer4_market_repeat_check,
    layer5_value_check,
    five_layer_filter,
)

def test_layer1():
    """Test L1: Fact Validation"""
    print("═" * 50)
    print("L1: Fact Validation")
    print("═" * 50)
    
    # 1) Real idea: pain matches user input
    r = layer1_fact_check(
        {"pain_point_solved": "猫砂盆清理太麻烦，每天都要铲屎"},
        ["猫砂盆清理麻烦", "宠物无人照看"],
        ["铲屎太累"]
    )
    assert r[0], f"Should pass: pain matches user input. Got: {r}"
    print(f"  ✅ [1] Pain matches user: {r[1]}")
    
    # 2) Real idea: pain matches web evidence
    r = layer1_fact_check(
        {"pain_point_solved": "自动喂食器卡粮问题严重", "web_evidence_summary": "淘宝评价里大量用户抱怨自动喂食器卡粮"},
        ["宠物无人照看"],
        ["自动喂食器卡粮"]
    )
    assert r[0], f"Should pass: evidence matches. Got: {r}"
    print(f"  ✅ [2] Evidence matches web: {r[1]}")
    
    # 3) AI hallucination: no pain, no evidence
    r = layer1_fact_check(
        {"pain_point_solved": "", "web_evidence_summary": ""},
        ["宠物无人照看"],
        []
    )
    assert not r[0], f"Should fail: empty pain+evidence. Got: {r}"
    print(f"  ✅ [3] Empty → fail: {r[1]}")
    
    # 4) Too short with no evidence
    r = layer1_fact_check(
        {"pain_point_solved": "不够好", "web_evidence_summary": ""},
        ["宠物"],
        []
    )
    assert not r[0], f"Should fail: vague short pain. Got: {r}"
    print(f"  ✅ [4] Vague short pain → fail: {r[1]}")
    
    # 5) Real pain, no web match, but specific content
    r = layer1_fact_check(
        {"pain_point_solved": "智能手表在游泳时无法准确记录圈数和划水效率", "web_evidence_summary": ""},
        ["运动"],
        []
    )
    # Should pass because pain has ≥8 chars and isn't vague
    # Actually "智能手表在游泳时无法准确记录圈数和划水效率" doesn't match "运动" substring
    # But it's 22 chars, specific → should pass the "real content" fallback
    assert r[0], f"Should pass: specific pain content. Got: {r}"
    print(f"  ✅ [5] Specific pain (no user match) → pass via content check: {r[1]}")

def test_layer2():
    """Test L2: Logic Validation / 逻辑校验"""
    print("\n" + "═" * 50)
    print("L2: Logic Validation")
    print("═" * 50)
    
    # 1) Good logic
    r = layer2_logic_check({
        "title": "模块化伸缩收纳架",
        "one_line": "可自由拼接的模块化置物架，适配任意尺寸柜体",
        "core_value": "无需测量，自由组合，搬家可拆",
        "target_user": "租房族、小户型家庭"
    })
    assert r[0], f"Should pass: good logic. Got: {r}"
    print(f"  ✅ [1] Good logic: {r[1]}")
    
    # 2) "Simple" + "Powerful" without bridge = contradiction
    r = layer2_logic_check({
        "title": "全能收纳系统",
        "one_line": "简单易用的强大收纳方案",
        "core_value": "简单又强大",
        "target_user": "家庭用户"
    })
    assert not r[0], f"Should fail: simple+powerful without bridge. Got: {r}"
    print(f"  ✅ [2] simple+powerful no bridge → fail: {r[1]}")
    
    # 3) "Simple" + "Powerful" WITH bridge = pass
    r = layer2_logic_check({
        "title": "平衡收纳系统",
        "one_line": "简单直观的操作界面，但提供强大的自动化分类能力",
        "core_value": "易用但专业",
        "target_user": "家庭用户"
    })
    assert r[0], f"Should pass: simple+powerful WITH '但'. Got: {r}"
    print(f"  ✅ [3] simple+powerful with bridge → pass: {r[1]}")
    
    # 4) "everyone" as target = fail
    r = layer2_logic_check({
        "title": "通用APP",
        "one_line": "适合所有人的应用",
        "core_value": "全民可用",
        "target_user": "所有人"
    })
    assert not r[0], f"Should fail: everyone as target. Got: {r}"
    print(f"  ✅ [4] '所有人' target → fail: {r[1]}")
    
    # 5) English: contradictory
    r = layer2_logic_check({
        "title": "All-in-one Tool",
        "one_line": "free and easy to use with powerful paid features",
        "core_value": "best of both worlds",
        "target_user": "developers"
    })
    # Has "free" and "paid" → contradiction
    assert not r[0], f"Should fail: free+paid contradiction. Got: {r}"
    print(f"  ✅ [5] English free+paid → fail: {r[1]}")

def test_layer3():
    """Test L3: Feasibility / 落地性"""
    print("\n" + "═" * 50)
    print("L3: Feasibility")
    print("═" * 50)
    
    # 1) Hardware mention alone shouldn't fail (v2 fix)
    r = layer3_feasibility_check({
        "title": "智能猫砂盆",
        "one_line": "带传感器的自动清理猫砂盆",
        "core_value": "自动清理，减少铲屎频率",
        "target_user": "养猫家庭",
        "feasibility_score": 4
    })
    # "传感器" weight=1.0, "硬件" not present. Total = 1.0 < 4.0 → pass
    # Wait, let me check: "传感器" (weight 1.0) is in the text. Any other?
    # "硬件" is not in the text. So weight = 1.0 < 4.0 → pass
    assert r[0], f"Should pass: hardware words alone not enough. Got: {r}"
    print(f"  ✅ [1] Hardware mention alone passes: {r[1]}")
    
    # 2) Multiple heavy signals = fail
    r = layer3_feasibility_check({
        "title": "自研芯片",
        "one_line": "开模生产自研芯片，建设自有生产线",
        "core_value": "自建工厂批量生产",
        "target_user": "硬件厂商",
        "feasibility_score": 2
    })
    # "自研" not in signals. Let me check: "芯片" → weight 2.0, "开模" → 2.0, "生产线" → 3.0
    # That's 2.0 + 2.0 + 3.0 = 7.0 > 4.0 → fail!
    assert not r[0], f"Should fail: multiple heavy signals. Got: {r}"
    print(f"  ✅ [2] Multiple heavy signals → fail: {r[1]}")
    
    # 3) Zero AI score = fail
    r = layer3_feasibility_check({
        "title": "不可能的项目",
        "one_line": "永动机",
        "core_value": "无",
        "target_user": "所有人",
        "feasibility_score": 0
    })
    assert not r[0], f"Should fail: score=0. Got: {r}"
    print(f"  ✅ [3] Score=0 → fail: {r[1]}")

def test_layer4():
    """Test L4: Market Duplicate / 市场重复"""
    print("\n" + "═" * 50)
    print("L4: Market Duplicate")
    print("═" * 50)
    
    # 1) Generic "AI" mention shouldn't match too many products (v2 fix)
    r = layer4_market_repeat_check({
        "title": "AI宠物助手",
        "one_line": "用AI分析宠物叫声和行为的智能项圈",
        "core_value": "读懂宠物情绪",
        "tags": ["宠物", "AI", "智能硬件"]
    })
    # "AI" matches: ChatGPT(×1), Claude(×1), Cursor(×1), etc. But each only ×1.
    # "聊天机器人" not present. "AI编程" not present. 
    # "AI" keyword weight is only 1.0 in each.
    # So max score/product = 1.0 (just "AI") from ChatGPT. 1.0 < 6.0 → pass
    assert r[0], f"Should pass: 'AI' alone not enough. Got: {r}"
    print(f"  ✅ [1] 'AI' mention alone passes: {r[1]}")
    
    # 2) Strong match: multiple high-weight keywords hit one product
    r = layer4_market_repeat_check({
        "title": "社交种草平台",
        "one_line": "基于用户笔记分享的生活方式种草社区",
        "core_value": "真实用户测评与推荐",
        "tags": ["社交", "种草", "分享"]
    })
    # "种草"(4) + "笔记"(1) + "生活方式"(3) + "分享"(1) + "社区"(2) 
    # = 11 → matches 小红书. 11 ≥ 6 → fail
    assert not r[0], f"Should fail: strong match 小红书. Got: {r}"
    print(f"  ✅ [2] Strong 小红书 match → fail: {r[1]}")

def test_layer5():
    """Test L5: Value / 价值"""
    print("\n" + "═" * 50)
    print("L5: Value")
    print("═" * 50)
    
    # 1) Buzzword overload
    r = layer5_value_check({
        "title": "区块链赋能数字化生态平台",
        "one_line": "用区块链和大数据赋能传统行业数字化升级",
        "core_value": "打造产业互联网闭环",
        "target_user": "传统企业"
    })
    # "区块链"(1) + "大数据"(1) + "赋能"(2) + "数字化"(1) + "生态"(1) + "闭环"(1) 
    # Wait, each has weight 1 in the buzzword check. So 6 ≥ 3 → fail
    # Actually BUZZWORD_BLACKLIST has: 智能, AI, 互联网+, 数字化, 云端, 大数据, 区块链, 元宇宙, 赋能, 生态, 闭环, 抓手, 打通, 对齐, 颗粒度, 底层逻辑, 降维打击, 颠覆, 重构, 重塑
    # In text: "区块链", "赋能", "数字化", "大数据", "生态", "闭环" = 6 ≥ 3 → fail
    assert not r[0], f"Should fail: buzzword overload. Got: {r}"
    print(f"  ✅ [1] Buzzword overload → fail: {r[1]}")
    
    # 2) Trivial pattern
    r = layer5_value_check({
        "title": "做个APP",
        "one_line": "做一个XX领域的APP应用",
        "core_value": "解决效率问题",
        "target_user": "上班族"
    })
    assert not r[0], f"Should fail: trivial '做个APP' pattern. Got: {r}"
    print(f"  ✅ [2] Trivial pattern → fail: {r[1]}")
    
    # 3) Good value (now passes with expanded solver verbs — v2.0 fix)
    r = layer5_value_check({
        "title": "模块化伸缩收纳架",
        "one_line": "可自由拼接的模块化置物架，适配任意尺寸柜体",
        "core_value": "无需测量，自由组合，搬家可拆",
        "target_user": "租房族、小户型家庭"
    })
    # "适配" is now in the solver list → has_solver=True → pass
    assert r[0], f"Should pass: has solver verb '适配'. Got: {r}"
    print(f"  ✅ [3] Good value passes with solver verb: {r[1]}")
    
    # 4) Niche too narrow
    r = layer5_value_check({
        "title": "我的私人工具",
        "one_line": "仅适合我自己用的工具",
        "core_value": "只为我服务",
        "target_user": "只有我"
    })
    assert not r[0], f"Should fail: niche too narrow. Got: {r}"
    print(f"  ✅ [4] Niche too narrow → fail: {r[1]}")

def test_end_to_end():
    """End-to-end filter test"""
    print("\n" + "═" * 50)
    print("End-to-End Test")
    print("═" * 50)
    
    ideas = [
        {  # Should pass
            "title": "模块化伸缩收纳架",
            "one_line": "可自由拼接的模块化置物架，适配任意尺寸柜体",
            "target_user": "租房族、小户型家庭",
            "core_value": "无需测量，自由组合，搬家可拆",
            "pain_point_solved": "固定尺寸收纳架在租房小户型中永远放不下",
            "web_evidence_summary": "小红书200+篇吐槽收纳架尺寸不合适的笔记",
            "feasibility_score": 4,
            "novelty_score": 4,
            "tags": ["收纳", "模块化", "租房"]
        },
        {  # Should fail L1: no real content
            "title": "AI智能收纳盒",
            "one_line": "用AI自动分类你的所有杂物",
            "target_user": "所有人",
            "core_value": "让收纳变智能",
            "pain_point_solved": "收纳麻烦",
            "web_evidence_summary": "",
            "feasibility_score": 1,
            "novelty_score": 1,
            "tags": ["AI", "智能", "收纳"]
        },
        {  # Should fail L3+L5: heavy + buzzword
            "title": "区块链去中心化收纳平台",
            "one_line": "用区块链技术重构家居收纳体验，赋能产业生态",
            "target_user": "极客用户",
            "core_value": "赋能收纳生态闭环，打通产业链底层逻辑",
            "pain_point_solved": "收纳行业效率低下，缺乏数字化变革",
            "web_evidence_summary": "某博客提到区块链改造收纳",
            "feasibility_score": 1,
            "novelty_score": 5,
            "tags": ["区块链", "收纳", "去中心化"]
        },
        {  # Should pass (real product)
            "title": "宠物自动喂食器改良版",
            "one_line": "防卡粮设计的定时定量远程控制宠物喂食器",
            "target_user": "养猫养狗的上班族",
            "core_value": "解决自动喂食器卡粮和连接不稳定的核心痛点",
            "pain_point_solved": "上班族白天不在家，现有自动喂食器容易卡粮、App掉线",
            "web_evidence_summary": "淘宝宠物喂食器月销10万+，差评集中在卡粮和App连接不稳定",
            "feasibility_score": 4,
            "novelty_score": 2,
            "tags": ["宠物", "智能硬件", "上班族"]
        },
        {  # Should fail L5: trivial pattern
            "title": "一键生成报告工具",
            "one_line": "一键生成各种工作周报和总结报告",
            "target_user": "上班族",
            "core_value": "一键搞定周报月报",
            "pain_point_solved": "写周报太费时间",
            "web_evidence_summary": "职场人普遍抱怨写周报",
            "feasibility_score": 3,
            "novelty_score": 1,
            "tags": ["办公", "效率"]
        },
        {  # Should fail L4: duplicates existing product
            "title": "新式双向链接笔记工具",
            "one_line": "带知识图谱的个人笔记管理工具，支持双向链接和Markdown",
            "target_user": "知识工作者",
            "core_value": "本地化存储，双向链接知识图谱，丰富插件生态",
            "pain_point_solved": "现有笔记工具缺少双向链接和知识图谱功能",
            "web_evidence_summary": "Notion用户抱怨缺少本地存储，Obsidian用户希望更好的移动端体验",
            "feasibility_score": 3,
            "novelty_score": 2,
            "tags": ["笔记", "知识管理", "图谱"]
        },
    ]

    results = five_layer_filter(ideas, 
        user_pain_points=["收纳架尺寸不合适", "租房收纳难", "写周报太麻烦"],
        web_evidence_list=["小红书收纳架尺寸吐槽", "淘宝宠物喂食器差评"])

    passed_titles = [r["title"] for r in results]
    failed_titles = [ideas[i]["title"] for i in range(len(ideas)) 
                     if not any(r["index"] == i for r in results)]
    
    print(f"\n  ✅ Passed / 通过: {passed_titles}")
    print(f"  ❌ Failed: {failed_titles}")
    
    # Expectations
    assert "模块化伸缩收纳架" in passed_titles, "Good idea should pass"
    assert "宠物自动喂食器改良版" in passed_titles, "Real pain should pass"
    assert "AI智能收纳盒" in failed_titles, "Empty idea should fail"
    assert "区块链去中心化收纳平台" in failed_titles, "Buzzword idea should fail"
    assert "一键生成报告工具" in failed_titles, "Trivial pattern should fail"
    # The "新式双向链接笔记工具" should fail L4 (Obsidian match) or pass if not strong enough
    # Let's check: "笔记"(2) + "知识管理"(3) + "双向链接"(4) + "图谱"(3) + "本地"(2) + "插件"(2) 
    # = 16 → Observidian weight 16 ≥ 6 → fail L4
    assert "新式双向链接笔记工具" in failed_titles, "Market duplicate should fail"
    
    print(f"\n  ✅ All end-to-end assertions passed!")


if __name__ == "__main__":
    test_layer1()
    test_layer2()
    test_layer3()
    test_layer4()
    test_layer5()
    test_end_to_end()
    print("\n" + "=" * 50)
    print("  🎉 ALL TESTS PASSED")
    print("=" * 50)

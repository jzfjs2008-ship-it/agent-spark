# Search Query Templates（v2.0）
# 搜索关键词模板（v2.0）

## Key Changes in v2.0 / v2.0 主要改动

| Before (v1.0) / 之前 | After (v2.0) / 之后 | Reason / 原因 |
|---|---|---|
| "为什么没有" (question format) | Removed | Search engines don't parse questions well / 搜索引擎不处理问句 |
| "用户痛点" (generic) | "用户痛点 解决方案" | More actionable searches / 更可操作的搜索 |
| Single vague keyword | Structured query patterns | Better recall + precision / 更好的召回率和精确度 |
| Manual search only | Added actual search-site commands | Immediately usable / 立即可用 |

## 4 Search Dimensions / 四大搜索维度

For a given domain {domain} / 给定领域{domain}，生成以下四类搜索：

---

### D1. Pain-Point Discovery / 行业用户痛点搜索

```
site:zhihu.com {domain} 痛点/吐槽/问题
site:xiaohongshu.com {domain} 踩雷/后悔/别买
site:douban.com/group {domain} 讨论/求助
reddit site:reddit.com {domain} "worst part" OR "annoying" OR "frustrating"
"{domain}" complaints OR problems OR issues
```

**Purpose:** surface real user frustrations / 挖掘真实用户吐槽

---

### D2. Product Flaw Mining / 同类产品缺陷搜索

```
{domain} 产品 差评/测评 对比/推荐 缺点
"{domain}" sucks OR terrible OR "waste of money"
"{domain}" review comparison "better than"
{domain} "I wish" OR "it should" OR "if only"
```

**Purpose:** find specific improvement opportunities / 寻找具体改良切入点

---

### D3. Market-Gap Detection / 市场空白搜索

```
{domain} "there is no" OR "doesn't exist" OR "why isn't there"
{domain} "what if" OR "would be great if"
{domain} "alternative to" OR "looking for" OR "need a"
site:producthunt.com {domain} "upcoming" OR "launched"
```

**Purpose:** discover unmet needs / 发现未被满足的需求

---

### D4. Niche-Segment Exploration / 小众细分场景搜索

```
{domain} for {segment}    # segment: elderly/children/pets/renters/travelers/disabled
{domain} {segment} 需求/场景/特殊
"{domain}" underserved OR overlooked OR niche
{domain} accessibility OR "low income" OR rural
```

**Purpose:** find overlooked micro-markets / 发现被忽视的微小市场

---

## Structured Output Schema / 结构化输出格式

```json
{
  "search_dimension_1_pain": [
    {
      "source": "zhihu.com / xiaohongshu / reddit",
      "content": "Excerpt of the pain point / 痛点原文摘要",
      "sentiment": "negative | neutral | mixed",
      "possible_idea_direction": "Associated idea angle / 关联创意方向"
    }
  ],
  "search_dimension_2_flaws": [],
  "search_dimension_3_gaps": [],
  "search_dimension_4_niche": []
}
```

## Integration / 集成方式

In Hermes, use `web_search()` or `search_files()` to run these queries.
In Claude Code, the bridge script passes them to the CLI.
The bridge script passes them to the LLM for automatic search.

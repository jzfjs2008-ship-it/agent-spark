# Search Query Templates (v2.0)

## Key Changes in v2.0

| Before (v1.0) | After (v2.0) | Reason |
|---------------|--------------|--------|
| "why isn't there" (question format) | Removed | Search engines don't parse questions well |
| "pain point" (generic) | "pain point solution" | More actionable searches |
| Single vague keyword | Structured query patterns | Better recall + precision |
| Manual search only | Added actual search-site commands | Immediately usable |

## 4 Search Dimensions

For a given domain {domain}:

---

### D1. Pain-Point Discovery

```
site:zhihu.com {domain} 痛点/吐槽/问题
site:xiaohongshu.com {domain} 踩雷/后悔/别买
site:douban.com/group {domain} 讨论/求助
reddit site:reddit.com {domain} "worst part" OR "annoying" OR "frustrating"
"{domain}" complaints OR problems OR issues
```

---

### D2. Product Flaw Mining

```
{domain} 产品 差评/测评 对比/推荐 缺点
"{domain}" sucks OR terrible OR "waste of money"
"{domain}" review comparison "better than"
{domain} "I wish" OR "it should" OR "if only"
```

---

### D3. Market-Gap Detection

```
{domain} "there is no" OR "doesn't exist" OR "why isn't there"
{domain} "what if" OR "would be great if"
{domain} "alternative to" OR "looking for" OR "need a"
site:producthunt.com {domain} "upcoming" OR "launched"
```

---

### D4. Niche-Segment Exploration

```
{domain} for {segment}    # segment: elderly/children/pets/renters/travelers/disabled
"{domain}" underserved OR overlooked OR niche
{domain} accessibility OR "low income" OR rural
```

---

## Structured Output Schema

```json
{
  "search_dimension_1_pain": [
    {
      "source": "zhihu.com / xiaohongshu / reddit",
      "content": "Excerpt of the pain point",
      "sentiment": "negative | neutral | mixed",
      "possible_idea_direction": "Associated idea angle"
    }
  ],
  "search_dimension_2_flaws": [],
  "search_dimension_3_gaps": [],
  "search_dimension_4_niche": []
}
```

## Integration

In Hermes, use `web_search()` or `search_files()` to run these queries.
In Claude Code, the bridge script passes them to the CLI for automatic search.

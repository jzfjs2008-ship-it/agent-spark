# Contributing to Agent Spark

Thanks for considering contributing! 🎉

## How to Contribute

### 1. Add a New Domain to the Preset Library

The most valuable contribution: adding pre-scanned pain points for a domain.

1. Fork the repo
2. Edit `agent_spark/presets/domains.json`
3. Add your domain entry (follow existing format)
4. Submit a PR

**Entry format:**
```json
{
  "domain": "your domain",
  "domain_zh": "中文名（可选）",
  "pain_points": [
    "Pain point 1 with specific evidence context",
    "Pain point 2..."
  ],
  "evidence": [
    "Source-backed claim about this domain"
  ]
}
```

**Requirements:**
- At least 5 pain points per domain
- At least 2 evidence sources per domain
- Pain points should be specific (not generic like "too expensive")
- Evidence should reference real sources (Reddit, reviews, studies, etc.)

### 2. Report a Bug

Open an issue with the bug report template.

### 3. Suggest a Feature

Open an issue with the feature request template.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).

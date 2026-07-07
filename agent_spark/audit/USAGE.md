## Step 8 · Structured Project Audit (v2.0)

After generating a project plan, always audit it — catches hidden assumptions, governance gaps, unsourced data, security holes, and market delusions before presenting to the user.

### v2.0 Changes

| Before (v1) | After (v2) | Reason |
|-------------|-----------|--------|
| 4 dimensions, 19 checks | 5 dimensions, 36 checks | Market dimension added; all dimensions expanded |
| No scoring | Score 0-100, grade A-F | Quantifiable audit result |
| No verdict | PASS / WEAK_PASS / CONDITIONAL / REJECT | Clear go/no-go decision |
| Only 1 unsourced data point flagged | All unsourced points flagged | Don't let multiple bad data slip through |
| Contradiction check: first match only | All contradiction pairs checked | Multiple contradictions compound |
| Minor severity for exit plan, contradictions | Upgraded to major | These are real risks, not cosmetic |
| No privacy check | Data privacy compliance check | Legal liability |
| No market checks | 5 market checks (competitor, differentiation, timing, TAM, distribution) | "Good product, zero market" is the #1 startup killer |

### How to use

```python
from agent_spark.audit.auditor import audit_project_plan

plan = """...your refined project plan..."""
report = audit_project_plan(plan, "My Project Name")
print(report.summary())

# Score and verdict
print(f"Score: {report.score}/100 ({report.grade})")
print(f"Verdict: {report.verdict}")

# Per-dimension breakdown
for dim, counts in report.by_dimension().items():
    print(f"  {dim}: {counts}")

# Findings
for f in report.findings:
    print(f"  [{f.severity}] {f.dimension}: {f.title}")

# Decision logic
if report.verdict == "REJECT":
    # 3+ critical issues — do NOT present, return to refinement
    pass
elif report.verdict == "CONDITIONAL":
    # 1-2 critical issues — fix those first
    pass
elif report.verdict == "WEAK_PASS":
    # No criticals but score < 75 — fix majors
    pass
else:
    # PASS — safe to present
    pass
```

### CLI

```bash
cat project-plan.md | agent-spark-audit
agent-spark-audit project-plan.md
```

### Scoring

| Penalty | Per finding |
|---------|------------|
| -15 | Critical |
| -5 | Major |
| -2 | Minor |
| -1 | Suggestion |

Score = max(0, 100 - total_penalty)

### Verdict Rules

| Verdict | Condition | Action |
|---------|-----------|--------|
| PASS | score ≥ 75, 0 critical | Present to user |
| WEAK_PASS | score 60-74, 0 critical | Fix majors, then present |
| CONDITIONAL | 1-2 criticals | Fix criticals, re-audit |
| REJECT | 3+ criticals | Return to Step 7 (refinement) |

**Rule:** If verdict is REJECT, do NOT present the plan. Return to refinement and fix critical issues first. Re-audit until at least CONDITIONAL.

### What it checks (36 checks across 5 dimensions)

| Dimension | Checks | What it catches |
|-----------|--------|-----------------|
| Logic (8) | Promise realistic, causal chain, hidden assumptions, contradictions, network effect, vague verbs, circular reasoning, wishful thinking | Logical gaps, wishful thinking, circular reasoning, vague mechanisms |
| Structure (8) | Governance, exit plan, adoption path, scope boundary, schema validation, timeline/milestones, dependency risk, single-point-of-failure | Structural gaps, missing plans, critical dependencies |
| Entity (7) | Data sources, factual claims, role incentives, economics, user≠developer, revenue≠growth, survivorship bias | Fabricated data, conflated metrics, bias |
| Technical (8) | Implementation path, security, edge cases, maintainability, data privacy, API stability, deployment/ops, dependency sustainability | Technical debt, security holes, legal risks |
| Market (5) | Competitor analysis, differentiation, timing window, TAM reality, distribution channel | Market delusions, no differentiation, no distribution |

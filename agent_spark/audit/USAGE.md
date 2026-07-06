## Step 8 繚 Structured Project Audit / 蝏??★?桀恣霈?
**New in v2.0 ??after generating a project plan, always audit it.**

### Why?
Even after 5-layer filtering, a project plan can have:
- **Logic errors:** hidden assumptions, broken causality, overclaimed network effects
- **Structure errors:** no governance, no exit path, unclear adoption
- **Entity errors:** fabricated data points, unverified competitive claims
- **Technical errors:** missing security, unhandled edge cases, maintainability debt

### How to use

```python
from agent-spark.audit.auditor import audit_project_plan

# Audit your project plan text
plan = """...your refined project plan..."""
report = audit_project_plan(plan, "My Project Name")

print(report.summary())
for f in report.findings:
    print(f"  [{f.severity}] {f.title}: {f.description[:100]}")

if report.critical_count > 0:
    print("!! FIX CRITICAL ISSUES BEFORE PROCEEDING")
```

### CLI
```bash
cat project-plan.txt | python -m agent-spark.audit.auditor
python -m agent-spark.audit.auditor project-plan.md
```

### What it checks (19 checks across 4 dimensions)

| Dimension | Checks | What it catches |
|-----------|--------|-----------------|
| ? Logic | 5 | Overclaimed promises, broken causality, hidden assumptions, contradictions, network-effect overestimation |
| ?? Structure | 5 | Missing governance, no exit plan, unclear adoption, missing scope boundary, schema without validator |
| ? Entity | 4 | Unsourced data, unsupported claims, misaligned incentives, missing economic model |
| ? Technical | 5 | Missing security, no edge-case handling, maintainability gaps, missing tech stack, no CI |

### Integration with the 7-step pipeline

The audit is **Step 8** ??after refinement, before showing the user:

```
Step 1-5: Filter ??Step 6: Preview ??Step 7: Refine ??潃?Step 8: Audit ??Show user
```

**Rule:** If the audit finds ?? critical issues, the plan should NOT be shown to the user. Go back to Step 7 (refinement) and fix before presenting.


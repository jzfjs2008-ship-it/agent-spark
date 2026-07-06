## Step 8 · Structured Project Audit

After generating a project plan, always audit it — catches hidden assumptions, governance gaps, unsourced data, and security holes before presenting to the user.

### Why
Even after the 5-layer filter, refined project plans can have:
- **Logic errors:** broken causality, overclaimed network effects
- **Structure errors:** no governance, missing exit path, unclear adoption
- **Entity errors:** fabricated data, unverified competitive claims
- **Technical errors:** missing security, unhandled edge cases

### How to use

```python
from agent_spark.audit.auditor import audit_project_plan

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
cat project-plan.md | agent-spark-audit
agent-spark-audit project-plan.md
```

### What it checks (19 checks across 4 dimensions)

| Dimension | Checks | What it catches |
|-----------|--------|-----------------|
| Logic | 5 | Overclaimed promises, broken causality, hidden assumptions, contradictions, network-effect overestimation |
| Structure | 5 | Missing governance, no exit plan, unclear adoption, missing scope boundary, schema without validator |
| Entity | 4 | Unsourced data, unsupported claims, misaligned incentives, missing economic model |
| Technical | 5 | Missing security, no edge-case handling, maintainability gaps, missing tech stack, no CI |

### Integration

The audit is Step 8 — after refinement, before showing the user:

```
Steps 1-5: Filter → Step 6: Preview → Step 7: Refine → Step 8: Audit → Show user
```

**Rule:** If audit finds ≥3 critical issues, do NOT present the plan. Return to Step 7 (refinement) and fix first.

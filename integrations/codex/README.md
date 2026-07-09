# Agent Spark — Codex CLI Integration

Codex CLI automatically loads `AGENTS.md` from the project root.
This integration file provides additional Codex-specific context.

## Available Commands

```bash
agent-spark-demo          # Run the 5-layer filter demo
agent-spark-filter        # Filter ideas from JSON file
agent-spark-audit         # Audit a project plan
agent-spark-pipeline      # Run full interview + filter pipeline
```

## Python Module

```python
from agent_spark import find_domain, Filter

# With preset
d = find_domain("pet supplies")
Filter.run(d.ideas, d.pain_points, d.evidence)

# Custom
from agent_spark.filter.five_layer_filter import five_layer_filter
results = five_layer_filter(ideas, pain_points, evidence)
```

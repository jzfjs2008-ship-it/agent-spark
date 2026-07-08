#!/usr/bin/env python3
"""Agent Spark CLI — python -m agent_spark"""


def main():
    print("⚡ Agent Spark v0.99.0")
    print("  Creative Engine for AI Agents")
    print()
    print("  Commands:")
    print("    agent-spark-filter     Run 5-layer filter on ideas.json")
    print("    agent-spark-audit      Audit a project plan")
    print("    agent-spark-demo       Run filter demo")
    print("    agent-spark-pipeline   Run full interview pipeline")
    print("    agent-spark-demo-full  Run full end-to-end demo")
    print()
    print("  Python API:")
    print("    from agent_spark import find_domain, Filter")
    print("    d = find_domain('pet supplies')")
    print("    Filter.run(d.ideas, d.pain_points, d.evidence)")
    print()
    print("  REST API:  pip install agent-spark[api]")
    print("    from agent_spark.api import app")


if __name__ == "__main__":
    main()

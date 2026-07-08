"""
Agent Spark · REST API (optional)
==================================
FastAPI server exposing the 5-layer filter as an HTTP endpoint.

Usage:
    pip install agent-spark[api]
    uvicorn agent_spark.api:app --port 8080

    curl -X POST http://localhost:8080/filter \
      -H 'Content-Type: application/json' \
      -d '{"ideas": [...], "pain_points": [...], "evidence": [...], "locale": "en"}'
"""

from __future__ import annotations

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except ImportError:
    print("FastAPI not installed. Run: pip install agent-spark[api]")
    raise

from typing import Any

from agent_spark import find_domain, list_domains
from agent_spark.filter.five_layer_filter import five_layer_filter

app = FastAPI(
    title="Agent Spark · Filter API",
    description="Industrial-grade creative idea filter. POST ideas, GET back pass/fail per layer.",
    version="0.99.0",
)


class FilterRequest(BaseModel):
    ideas: list[dict[str, Any]]
    pain_points: list[str] = []
    evidence: list[str] = []
    locale: str | None = None


class FilterResponse(BaseModel):
    total: int
    passed: int
    passed_indices: list[int]
    passed_titles: list[str]
    reports: list[dict[str, Any]]


class DomainResponse(BaseModel):
    domain: str
    domain_zh: str
    pain_points: list[str]
    evidence: list[str]


@app.get("/")
def root():
    return {
        "service": "agent-spark",
        "version": "0.99.0",
        "endpoints": {
            "POST /filter": "Run 5-layer filter on ideas",
            "GET /domains": "List preset domains",
            "GET /domains/{name}": "Get preset domain details",
        },
    }


@app.post("/filter", response_model=FilterResponse)
def filter_ideas(req: FilterRequest):
    """Run the 5-layer convergence filter on a batch of ideas."""
    results = five_layer_filter(
        req.ideas,
        req.pain_points,
        req.evidence,
        verbose=False,
        locale=req.locale,
    )
    return FilterResponse(
        total=len(req.ideas),
        passed=len(results),
        passed_indices=[r["index"] for r in results],
        passed_titles=[r["title"] for r in results],
        reports=results,
    )


@app.get("/domains")
def domains():
    """List all preset domain names."""
    return {"domains": list_domains()}


@app.get("/domains/{name}")
def domain_detail(name: str):
    """Get pre-scanned pain points and evidence for a domain."""
    result = find_domain(name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Domain '{name}' not found")
    return DomainResponse(
        domain=result.domain,
        domain_zh=result.domain_zh,
        pain_points=result.pain_points,
        evidence=result.evidence,
    )

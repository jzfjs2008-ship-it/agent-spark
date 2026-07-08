"""
Agent Spark · REST API (optional)
==================================
FastAPI server exposing the 5-layer filter as an HTTP endpoint.

Usage:
    pip install agent-spark[api]
    uvicorn agent_spark.api:app --port 8080

    curl POST /filter -d '{"ideas": [...], "pain_points": [...], "evidence": [...]}'
"""

from __future__ import annotations

from typing import Any

# Lazy import: only fails when you actually use the API, not on module import
_fastapi = None
_pydantic = None


def _ensure_deps():
    global _fastapi, _pydantic
    if _fastapi is None:
        try:
            from fastapi import FastAPI, HTTPException as FastAPIHTTPException
            from pydantic import BaseModel as PydanticBaseModel
            _fastapi = (FastAPI, FastAPIHTTPException)
            _pydantic = PydanticBaseModel
        except ImportError:
            raise ImportError(
                "FastAPI not installed. Run: pip install agent-spark[api]"
            )

from agent_spark import find_domain, list_domains
from agent_spark.filter.five_layer_filter import five_layer_filter


def _get_app():
    """Build the FastAPI app lazily."""
    _ensure_deps()
    FastAPI, HTTPException = _fastapi
    BaseModel = _pydantic

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
        results = five_layer_filter(
            req.ideas, req.pain_points, req.evidence,
            verbose=False, locale=req.locale,
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
        return {"domains": list_domains()}

    @app.get("/domains/{name}")
    def domain_detail(name: str):
        result = find_domain(name)
        if not result:
            raise HTTPException(status_code=404, detail=f"Domain '{name}' not found")
        return DomainResponse(
            domain=result.domain,
            domain_zh=result.domain_zh,
            pain_points=result.pain_points,
            evidence=result.evidence,
        )

    return app


# Build lazily on first call
_app_instance = None


def get_app():
    """Get or create the FastAPI app instance."""
    global _app_instance
    if _app_instance is None:
        _app_instance = _get_app()
    return _app_instance


# `from agent_spark.api import app` triggers lazy build
def __getattr__(name):
    if name == "app":
        return get_app()
    raise AttributeError(f"module 'agent_spark.api' has no attribute '{name}'")

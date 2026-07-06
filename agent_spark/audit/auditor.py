#!/usr/bin/env python3
"""
Inspiration · Structured Project Audit Engine
灵感 · 结构化项目审计引擎
================================================

Runs a systematic audit on any project plan output from the pipeline.
Scans: logic errors, structural gaps, entity/estimation errors, technical risks.

Usage:
    from agent_spark.audit.auditor import audit_project_plan
    report = audit_project_plan(plan_text)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Finding:
    """A single audit finding."""
    dimension: str      # "logic" | "structure" | "entity" | "technical"
    severity: str       # "critical" | "major" | "minor" | "suggestion"
    title: str
    description: str
    evidence: str = ""


@dataclass
class AuditReport:
    """Complete audit report."""
    project_name: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def major_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "major")

    @property
    def total(self) -> int:
        return len(self.findings)

    def summary(self) -> str:
        by_dim = {}
        for f in self.findings:
            by_dim.setdefault(f.dimension, 0)
            by_dim[f.dimension] += 1
        dim_str = " / ".join(f"{k}: {v}" for k, v in by_dim.items())
        return (
            f"Audit: {self.project_name}\n"
            f"  Total: {self.total} findings "
            f"(critical={self.critical_count}, major={self.major_count})\n"
            f"  By dimension: {dim_str}"
        )


# ─────────────────────────────────────────────────────────
# Audit Checks
# 审计检查项
# ─────────────────────────────────────────────────────────

def audit_project_plan(text: str, project_name: str = "Project") -> AuditReport:
    """Run all audit checks on a project plan text."""
    report = AuditReport(project_name=project_name)

    # ── Logic checks ──
    _check_promise_realistic(text, report)
    _check_causality(text, report)
    _check_hidden_assumptions(text, report)
    _check_contradictions(text, report)
    _check_network_effect(text, report)

    # ── Structure checks ──
    _check_governance(text, report)
    _check_exit_plan(text, report)
    _check_adoption_path(text, report)
    _check_scope_boundary(text, report)
    _check_schema_validation(text, report)

    # ── Entity checks ──
    _check_data_sources(text, report)
    _check_facts(text, report)
    _check_role_incentives(text, report)
    _check_economics(text, report)

    # ── Technical checks ──
    _check_implementation_path(text, report)
    _check_security_by_default(text, report)
    _check_edge_cases(text, report)
    _check_maintainability(text, report)

    return report


# ── Logic Checks ──

def _check_promise_realistic(text: str, report: AuditReport) -> None:
    """L1: Can the core promise be delivered on all claimed platforms?"""
    lines = text.lower()
    markers = [
        ("cross-platform", "cross.?platform"),
        ("every platform", "every.?platform|all.?platform"),
        ("any ai agent", "any.?ai.?agent|any.?agent"),
    ]
    for label, pattern in markers:
        if re.search(pattern, lines):
            # Check if there's a platform capability asymmetry mention
            if not re.search(r"(降级|degrade|limit|incompatible|unsupported)", lines):
                report.findings.append(Finding(
                    dimension="logic",
                    severity="critical",
                    title=f"Claim '{label}' without capability-gap handling",
                    description=(
                        f"The plan claims '{label}' but does not address "
                        "what happens when platforms have asymmetric capabilities. "
                        "GPT Actions cannot read files; Cursor cannot exec arbitrary binaries. "
                        "Without explicit degradation rules, this promise is hollow."
                    ),
                    evidence=f"Pattern '{pattern}' found; no fallback/degradation strategy found",
                ))


def _check_causality(text: str, report: AuditReport) -> None:
    """L2: Is the causal chain complete?"""
    if re.search(r"(users?|developers?) will (use|adopt|switch)", text.lower()):
        if not re.search(r"(migration|switch.?cost|learning.?curve|why.?should)", text.lower()):
            report.findings.append(Finding(
                dimension="logic",
                severity="major",
                title="Causal chain missing: adoption without migration cost analysis",
                description=(
                    "The plan assumes users/developers will adopt, but doesn't analyze "
                    "the switching cost. For a plugin developer maintaining 2 platforms, "
                    "adopting InterAgent means learning one more thing before it saves time."
                ),
            ))


def _check_hidden_assumptions(text: str, report: AuditReport) -> None:
    """L3: Are hidden assumptions surfaced?"""
    assumption_keywords = ["assuming", "assume", "expected", "likely", "should"]
    has_explicit_assumption_section = re.search(
        r"(key assumption|this depends on|假设|前提)",
        text.lower()
    )
    if not has_explicit_assumption_section:
        # Check if the text makes implicit assumptions
        for kw in assumption_keywords:
            if re.search(rf"\b{kw}\b", text.lower()):
                report.findings.append(Finding(
                    dimension="logic",
                    severity="major",
                    title="Hidden assumptions not explicitly declared",
                    description=(
                        f"The plan uses '{kw}' language but has no explicit "
                        "'Key Assumptions' section. Undocumented assumptions "
                        "that fail later are the #1 cause of project death."
                    ),
                    evidence=f"Found: '{kw}' used implicitly",
                ))
                break


def _check_contradictions(text: str, report: AuditReport) -> None:
    """L4: Internal contradictions."""
    pairs = [
        (r"lightweight|轻量", r"heavy|复杂|complex|comprehensive", "lightweight vs complex"),
        (r"free|open.?source", r"revenue|monetize|收费", "free vs monetization"),
        (r"mvp|minimum", r"full|complete|comprehensive", "MVP vs complete features"),
    ]
    for pattern_a, pattern_b, label in pairs:
        has_a = re.search(pattern_a, text.lower())
        has_b = re.search(pattern_b, text.lower())
        if has_a and has_b:
            context_a = text[max(0, has_a.start()-30):has_a.end()+30]
            context_b = text[max(0, has_b.start()-30):has_b.end()+30]
            report.findings.append(Finding(
                dimension="logic",
                severity="minor",
                title=f"Possible contradiction: {label}",
                description=f"Text claims both '{pattern_a}' and '{pattern_b}'.",
                evidence=f"  A: ...{context_a}...\n  B: ...{context_b}...",
            ))
            break


def _check_network_effect(text: str, report: AuditReport) -> None:
    """L5: Is network effect overestimated?"""
    if re.search(r"(network.?effect|more.*?more.*?valuable|增长飞轮)", text.lower()):
        # Check for adoption threshold analysis
        if not re.search(r"(critical.?mass|threshold|tipping.?point|临界)", text.lower()):
            report.findings.append(Finding(
                dimension="logic",
                severity="major",
                title="Network effect claimed without threshold analysis",
                description=(
                    "The plan invokes network effects but doesn't specify "
                    "how many platforms/plugins/users are needed to reach "
                    "the tipping point. For protocol standards, this is often "
                    "3+ major platforms or 50+ plugins."
                ),
            ))


# ── Structure Checks ──

def _check_governance(text: str, report: AuditReport) -> None:
    if not re.search(r"(governance|steering|maintainer|bdf?l|core.?team|治理)", text.lower()):
        report.findings.append(Finding(
            dimension="structure",
            severity="critical",
            title="No governance model defined",
            description=(
                "Open-standard projects without a governance model die when: "
                "(a) the original maintainer burns out, (b) a PR has conflicting "
                "opinions with no deciding authority, (c) a corporation forks "
                "the spec. MVP needs at least a simple governance doc."
            ),
        ))


def _check_exit_plan(text: str, report: AuditReport) -> None:
    if not re.search(r"(abandon|sunset|archive|maintainer.?bus|continuity)", text.lower()):
        report.findings.append(Finding(
            dimension="structure",
            severity="minor",
            title="No exit/sunset plan",
            description=(
                "If you stop maintaining this, what happens to adopters? "
                "A simple 'this project is maintained as best-effort; "
                "adopters should pin versions' is better than silence."
            ),
        ))


def _check_adoption_path(text: str, report: AuditReport) -> None:
    steps_from_hear_to_use = [
        r"quick.?start", r"getting.?started", r"pip install",
        r"install", r"setup", r"first.?steps",
    ]
    found = sum(1 for p in steps_from_hear_to_use if re.search(p, text.lower()))
    if found < 2:
        report.findings.append(Finding(
            dimension="structure",
            severity="major",
            title="Adoption path is unclear",
            description=(
                "The plan describes what to build but not how a user goes "
                "from 'hearing about it' to 'using it productively' in under 5 minutes. "
                f"Only {found}/6 adoption signals found."
            ),
        ))


def _check_scope_boundary(text: str, report: AuditReport) -> None:
    if not re.search(r"(not.*?scope|out.?of.?scope|won.?.?t.?do|不做的|范围外)", text.lower()):
        report.findings.append(Finding(
            dimension="structure",
            severity="major",
            title="Scope boundaries not defined",
            description=(
                "Every good project says what it WON'T do. Without explicit "
                "out-of-scope declarations, scope creep will blur the project's "
                "identity. InterAgent: 'not a runtime', 'not a plugin marketplace'?"
            ),
        ))


def _check_schema_validation(text: str, report: AuditReport) -> None:
    if re.search(r"(schema|spec|interagent\.json|protocol)", text.lower()):
        if not re.search(r"(validate|validator|verify|schema.?check)", text.lower()):
            report.findings.append(Finding(
                dimension="structure",
                severity="critical",
                title="Schema defined without validator",
                description=(
                    "Defining a JSON Schema without a validator means: "
                    "(a) users write invalid specs by accident, "
                    "(b) bridge implementations drift from the spec, "
                    "(c) you discover spec errors months later. "
                    "Validator must ship WITH the spec, not after."
                ),
            ))


# ── Entity Checks ──

def _check_data_sources(text: str, report: AuditReport) -> None:
    data_markers = re.findall(r"(\d[\d,]*[kKk]?\+?|\d+%|\d+ stars|\d+ users)", text)
    for marker in data_markers:
        # Check if the data point has a source citation nearby
        context_before = text[:text.find(marker)]
        last_period = context_before.rfind(".")
        context = context_before[last_period:] if last_period >= 0 else context_before[-100:]
        has_source = any(
            s in context.lower()
            for s in ["source", "根据", "based on", "per ", "from ", "report", "data"]
        )
        if not has_source:
            report.findings.append(Finding(
                dimension="entity",
                severity="major",
                title=f"Unsupported data point: '{marker}'",
                description=(
                    f"Data point '{marker}' appears without a clear source citation. "
                    "This makes it look fabricated, even if it's accurate."
                ),
                evidence=f"Context: ...{context[-60:]}...{marker}...",
            ))
            break  # one warning per plan is enough


def _check_facts(text: str, report: AuditReport) -> None:
    """E2: Verifiable factual claims."""
    # Check competitive claims
    if re.search(r"(biggest|most popular|leading|第一|最大)", text.lower()):
        if not re.search(r"(according to|source|data|排名|数据)", text.lower()):
            report.findings.append(Finding(
                dimension="entity",
                severity="major",
                title="Unsubstantiated competitive claim",
                description=(
                    "Claims like 'biggest' or 'most popular' need a source. "
                    "Without one, they read as marketing fluff."
                ),
            ))


def _check_role_incentives(text: str, report: AuditReport) -> None:
    """E3: Are all roles' incentives aligned?"""
    roles = re.findall(
        r"(?:plugin developer|平台方|platform|maintainer|contributor)",
        text.lower()
    )
    unique_roles = set(roles)
    if len(unique_roles) >= 3:
        # Has roles; check if incentives are analyzed
        if not re.search(r"(incentive|motivation|why.*?would|利益|动力)", text.lower()):
            report.findings.append(Finding(
                dimension="entity",
                severity="major",
                title="Multiple roles listed but incentives not analyzed",
                description=(
                    f"The plan mentions {len(unique_roles)} roles "
                    f"({', '.join(unique_roles)}) but doesn't analyze "
                    "why each would participate. For protocol projects, "
                    "the critical question is: why would PLATFORMS adopt?"
                ),
            ))


def _check_economics(text: str, report: AuditReport) -> None:
    """E4: Economic model."""
    if not re.search(r"(cost|revenue|budget|sponsor|funding|免费|收费)", text.lower()):
        report.findings.append(Finding(
            dimension="entity",
            severity="minor",
            title="No economic model mentioned",
            description=(
                "Even open-source projects have costs (CI, hosting, domains, "
                "developer time). A brief 'funded by X / volunteer-run / "
                "sponsor-supported' is better than silence."
            ),
        ))


# ── Technical Checks ──

def _check_implementation_path(text: str, report: AuditReport) -> None:
    """T1: Concrete implementation path?"""
    tech_keywords = [
        r"python", r"typescript", r"rust", r"go\b", r"sdk",
        r"api", r"cli", r"http", r"json.?schema", r"bridge",
    ]
    found_tech = sum(1 for p in tech_keywords if re.search(p, text.lower()))
    if found_tech < 3:
        report.findings.append(Finding(
            dimension="technical",
            severity="critical",
            title="Missing concrete technology choices",
            description=(
                f"Only {found_tech}/9 technology signals found. "
                "A project plan without concrete tech choices is a wishlist, "
                "not a plan. At minimum: language, SDK format, transport protocol."
            ),
        ))


def _check_security_by_default(text: str, report: AuditReport) -> None:
    """T2: Security by default?"""
    if not re.search(r"(signing|signature|permission|sandbox|audit|auth)", text.lower()):
        report.findings.append(Finding(
            dimension="technical",
            severity="critical",
            title="Security not mentioned at all",
            description=(
                "For a cross-platform plugin protocol, security is not optional. "
                "Missing: signing chain, permission model, sandboxing, audit trail. "
                "Adding security post-hoc is exponentially more expensive."
            ),
        ))


def _check_edge_cases(text: str, report: AuditReport) -> None:
    """T3: Edge cases mentioned?"""
    edge_keywords = [
        r"error.?handling", r"edge.?case", r"timeout", r"failover",
        r"degrade", r"fallback", r"validation", r"边界",
    ]
    found = sum(1 for p in edge_keywords if re.search(p, text.lower()))
    if found < 1:
        report.findings.append(Finding(
            dimension="technical",
            severity="major",
            title="No edge-case handling mentioned",
            description=(
                "No discussion of: what happens when a bridge fails mid-generation? "
                "When the plugin descriptor is invalid? When a platform's API changes? "
                "When network is unavailable?"
            ),
            evidence=f"0/{len(edge_keywords)} edge-case signals found",
        ))


def _check_maintainability(text: str, report: AuditReport) -> None:
    """T4: Maintainability."""
    signals = [
        (r"(version|semver|breaking.?change)", "versioning strategy"),
        (r"(test|ci|continuous)", "testing/CI"),
        (r"(doc|docs?|documentation)", "documentation"),
        (r"(contributing|contribute|pr|pull.?request)", "contribution process"),
    ]
    found = sum(1 for p, _ in signals if re.search(p, text.lower()))
    if found < 2:
        report.findings.append(Finding(
            dimension="technical",
            severity="major",
            title="Maintainability concerns not addressed",
            description=(
                f"Only {found}/{len(signals)} maintainability signals found. "
                "Missing: versioning strategy, CI, documentation plan, "
                "or contribution process. Without these, the project will "
                "accumulate technical debt faster than it can be paid down."
            ),
            evidence=f"Found: {found}/{len(signals)}",
        ))


# ── CLI Entry ──

def main():
    """Run audit on stdin text or a file."""
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
        name = sys.argv[1]
    else:
        text = sys.stdin.read()
        name = "stdin"

    report = audit_project_plan(text, project_name=name)
    print(report.summary())
    print()
    for f in report.findings:
        badge = {"critical": "🔴", "major": "🟠", "minor": "🟡", "suggestion": "💡"}
        sev = f.severity
        print(f"  {badge.get(sev, '•')} [{f.dimension}:{sev}] {f.title}")
        print(f"     {f.description[:120]}")
        if f.evidence:
            print(f"     Evidence: {f.evidence[:120]}")
        print()

    if report.critical_count > 0:
        print(f"  !! {report.critical_count} CRITICAL issues — must fix before proceeding")
        sys.exit(1 if report.critical_count > 2 else 0)


if __name__ == "__main__":
    main()

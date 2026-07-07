#!/usr/bin/env python3
"""
Agent Spark · Structured Project Audit Engine (v2.0 — Stricter)
===============================================================

Runs a systematic audit on any project plan output from the pipeline.
Scans 5 dimensions: logic, structure, entity, technical, market.

v2.0 changes vs v1.0:
  [NEW] 5th dimension: Market (competitor, differentiation, timing, TAM)
  [NEW] AuditReport: score, grade, verdict, per-dimension breakdown
  [NEW] Logic: vague-verb detection, circular reasoning, survivorship bias, wishful thinking
  [NEW] Structure: timeline/milestone, dependency risk, single-point-of-failure, demoable MVP
  [NEW] Entity: all unsourced data points (not just first), user≠developer, revenue≠growth
  [NEW] Technical: data privacy, API stability, deployment/ops, dependency sustainability
  [FIX]  Contradiction check: all pairs, not just first match
  [FIX]  Severity tightened: minor→major, major→critical where thresholds were too lenient

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
    dimension: str
    severity: str
    title: str
    description: str
    evidence: str = ""


@dataclass
class AuditReport:
    project_name: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def major_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "major")

    @property
    def minor_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "minor")

    @property
    def suggestion_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "suggestion")

    @property
    def total(self) -> int:
        return len(self.findings)

    @property
    def score(self) -> int:
        penalty = (
            self.critical_count * 15
            + self.major_count * 5
            + self.minor_count * 2
            + self.suggestion_count * 1
        )
        return max(0, 100 - penalty)

    @property
    def grade(self) -> str:
        s = self.score
        if s >= 90:
            return "A"
        if s >= 75:
            return "B"
        if s >= 60:
            return "C"
        if s >= 40:
            return "D"
        return "F"

    @property
    def verdict(self) -> str:
        if self.critical_count >= 3:
            return "REJECT"
        if self.critical_count >= 1:
            return "CONDITIONAL"
        if self.major_count >= 5:
            return "CONDITIONAL"
        if self.score >= 75:
            return "PASS"
        return "WEAK_PASS"

    def by_dimension(self) -> dict[str, dict[str, int]]:
        result: dict[str, dict[str, int]] = {}
        for f in self.findings:
            result.setdefault(f.dimension, {"critical": 0, "major": 0, "minor": 0, "suggestion": 0})
            result[f.dimension][f.severity] += 1
        return result

    def summary(self) -> str:
        dim_str = " / ".join(
            f"{k}: {sum(v.values())}({'+'.join(f'{sev[0]}={cnt}' for sev, cnt in v.items() if cnt)})"
            for k, v in self.by_dimension().items()
        )
        return (
            f"Audit: {self.project_name}\n"
            f"  Score: {self.score}/100 ({self.grade}) — Verdict: {self.verdict}\n"
            f"  Findings: {self.total} (critical={self.critical_count}, major={self.major_count}, "
            f"minor={self.minor_count}, suggestion={self.suggestion_count})\n"
            f"  By dimension: {dim_str}"
        )


# ───────────────────────────────────────────────────────
# MAIN ENTRY
# ────────────────────────────────────────────────────────

def audit_project_plan(text: str, project_name: str = "Project") -> AuditReport:
    report = AuditReport(project_name=project_name)

    # ── Logic (8 checks) ──
    _check_promise_realistic(text, report)
    _check_causality(text, report)
    _check_hidden_assumptions(text, report)
    _check_contradictions(text, report)
    _check_network_effect(text, report)
    _check_vague_verbs(text, report)
    _check_circular_reasoning(text, report)
    _check_wishful_thinking(text, report)

    # ── Structure (8 checks) ──
    _check_governance(text, report)
    _check_exit_plan(text, report)
    _check_adoption_path(text, report)
    _check_scope_boundary(text, report)
    _check_schema_validation(text, report)
    _check_timeline_milestones(text, report)
    _check_dependency_risk(text, report)
    _check_single_point_of_failure(text, report)

    # ── Entity (7 checks) ──
    _check_data_sources(text, report)
    _check_facts(text, report)
    _check_role_incentives(text, report)
    _check_economics(text, report)
    _check_user_vs_developer(text, report)
    _check_revenue_vs_growth(text, report)
    _check_survivorship_bias(text, report)

    # ── Technical (8 checks) ──
    _check_implementation_path(text, report)
    _check_security_by_default(text, report)
    _check_edge_cases(text, report)
    _check_maintainability(text, report)
    _check_data_privacy(text, report)
    _check_api_stability(text, report)
    _check_deployment_ops(text, report)
    _check_dependency_sustainability(text, report)

    # ── Market (5 checks) ──
    _check_competitor_analysis(text, report)
    _check_differentiation(text, report)
    _check_timing_window(text, report)
    _check_tam_reality(text, report)
    _check_distribution_channel(text, report)

    return report


# ═══════════════════════════════════════════════════════════
# LOGIC CHECKS (8)
# ═══════════════════════════════════════════════════════════

def _check_promise_realistic(text: str, report: AuditReport) -> None:
    lower = text.lower()
    markers = [
        ("cross-platform", r"cross.?platform"),
        ("every platform", r"every.?platform|all.?platform"),
        ("any ai agent", r"any.?ai.?agent|any.?agent"),
        ("works everywhere", r"works.?everywhere|anywhere"),
        ("unlimited", r"unlimited|无限"),
    ]
    for label, pattern in markers:
        if re.search(pattern, lower):
            if not re.search(r"(降级|degrade|limit|incompatible|unsupported|caveat|except|限制|不支持)", lower):
                report.findings.append(Finding(
                    dimension="logic",
                    severity="critical",
                    title=f"Claim '{label}' without capability-gap handling",
                    description=(
                        f"The plan claims '{label}' but does not address "
                        "what happens when environments have asymmetric capabilities. "
                        "Without explicit degradation rules, this promise is hollow."
                    ),
                    evidence=f"Pattern '{pattern}' found; no fallback/degradation strategy found",
                ))


def _check_causality(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(users?|developers?|people|companies) will (use|adopt|switch|love|prefer)", lower):
        if not re.search(r"(migration|switch.?cost|learning.?curve|why.?should|reason.?to|切换成本|迁移)", lower):
            report.findings.append(Finding(
                dimension="logic",
                severity="critical",
                title="Causal chain broken: adoption claimed without migration cost analysis",
                description=(
                    "The plan assumes users will adopt but doesn't analyze switching cost. "
                    "Every adoption claim needs: (1) why users are dissatisfied now, "
                    "(2) what they must give up to switch, (3) how long the transition takes. "
                    "Missing all three = wishful thinking."
                ),
            ))


def _check_hidden_assumptions(text: str, report: AuditReport) -> None:
    assumption_keywords = ["assuming", "assume", "expected", "likely", "should", "presumably"]
    has_explicit_section = re.search(
        r"(key.?assumption|this.?depends.?on|假设|前提|assumption)", text.lower()
    )
    if not has_explicit_section:
        for kw in assumption_keywords:
            if re.search(rf"\b{kw}\b", text.lower()):
                report.findings.append(Finding(
                    dimension="logic",
                    severity="critical",
                    title="Hidden assumptions not explicitly declared",
                    description=(
                        f"The plan uses '{kw}' language but has no explicit "
                        "'Key Assumptions' section. Undocumented assumptions "
                        "that fail later are the #1 cause of project death. "
                        "Every assumption must be listed with a failure contingency."
                    ),
                    evidence=f"Found: '{kw}' used implicitly",
                ))
                break


def _check_contradictions(text: str, report: AuditReport) -> None:
    pairs = [
        (r"lightweight|轻量|minimal", r"heavy|复杂|complex|comprehensive|全面|重量级", "lightweight vs complex"),
        (r"free|open.?source|开源|免费", r"revenue|monetize|收费|盈利|付费", "free vs monetization"),
        (r"mvp|minimum|最小", r"full|complete|comprehensive|全功能|完整", "MVP vs complete features"),
        (r"offline|离线|local.?only", r"cloud|云端|online|在线", "offline vs online"),
        (r"simple|简单|easy", r"powerful|强大|all.?in.?one", "simple vs powerful"),
        (r"private|隐私|本地存储", r"share|共享|social|社区", "private vs social"),
        (r"real.?time|实时", r"batch|异步|async|offline", "realtime vs batch"),
    ]
    for pattern_a, pattern_b, label in pairs:
        has_a = re.search(pattern_a, text.lower())
        has_b = re.search(pattern_b, text.lower())
        if has_a and has_b:
            bridge_words = r"(but|however|yet|while|trade.?off|虽然|但|然而|同时|代价|妥协)"
            has_bridge = (
                re.search(bridge_words, text[max(0, has_a.start()-80):has_b.end()+80].lower())
                or re.search(bridge_words, text[max(0, has_b.start()-80):has_a.end()+80].lower())
            )
            if not has_bridge:
                context_a = text[max(0, has_a.start()-30):has_a.end()+30]
                context_b = text[max(0, has_b.start()-30):has_b.end()+30]
                report.findings.append(Finding(
                    dimension="logic",
                    severity="major",
                    title=f"Contradiction: {label}",
                    description=(
                        f"Text claims both '{pattern_a}' and '{pattern_b}' "
                        "without acknowledging the trade-off. Every contradiction "
                        "needs an explicit bridge word (but, however, trade-off) or "
                        "the plan is internally incoherent."
                    ),
                    evidence=f"  A: ...{context_a}...\n  B: ...{context_b}...",
                ))


def _check_network_effect(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(network.?effect|more.*?more.*?valuable|增长飞轮|飞轮效应|网络效应)", lower):
        if not re.search(r"(critical.?mass|threshold|tipping.?point|临界|起步量|最小网络规模)", lower):
            report.findings.append(Finding(
                dimension="logic",
                severity="critical",
                title="Network effect claimed without threshold analysis",
                description=(
                    "The plan invokes network effects but doesn't specify "
                    "how many platforms/plugins/users are needed to reach "
                    "the tipping point. For protocol standards: 3+ major platforms "
                    "or 50+ plugins. For social products: 1000+ DAU. "
                    "No threshold = no way to validate if MVP can get there."
                ),
            ))
        if not re.search(r"(cold.?start|chicken.?egg|冷启动|先有鸡)", lower):
            report.findings.append(Finding(
                dimension="logic",
                severity="major",
                title="Network effect claimed without cold-start strategy",
                description=(
                    "Every network-effect product faces the cold-start problem: "
                    "users won't join until other users are there. The plan must "
                    "explain how to bootstrap the first N users without relying on "
                    "the network effect itself."
                ),
            ))


def _check_vague_verbs(text: str, report: AuditReport) -> None:
    vague_verbs = [
        (r"\bleverage\b", "leverage"),
        (r"\butilize\b", "utilize"),
        (r"\benhance\b", "enhance"),
        (r"\boptimize\b", "optimize"),
        (r"\bstreamline\b", "streamline"),
        (r"\bempower\b", "empower"),
        (r"\btransform\b", "transform"),
        (r"\brevolutionize\b", "revolutionize"),
        (r"\bdisrupt\b", "disrupt"),
        (r"\b赋能\b", "赋能"),
        (r"\b优化\b", "优化"),
        (r"\b提升\b", "提升"),
        (r"\b打造\b", "打造"),
    ]
    hits = []
    for pattern, word in vague_verbs:
        count = len(re.findall(pattern, text.lower()))
        if count >= 2:
            hits.append(f"{word}(x{count})")
    if len(hits) >= 3:
        report.findings.append(Finding(
            dimension="logic",
            severity="major",
            title=f"Plan relies on vague action verbs: {', '.join(hits)}",
            description=(
                "Vague verbs like 'leverage', 'optimize', 'empower' sound impressive "
                "but describe no concrete mechanism. A plan that says 'we will leverage AI "
                "to enhance productivity' says nothing. Replace each with: what specifically "
                "happens, to what, with what input, producing what output."
            ),
            evidence=f"Vague verbs found: {', '.join(hits)}",
        ))


def _check_circular_reasoning(text: str, report: AuditReport) -> None:
    lower = text.lower()
    circular_patterns = [
        (r"because.*(popular|widely.?used|successful)", "claims success as reason for success"),
        (r"因为.*?(受欢迎|广泛使用|成功)", "claims success as reason for success"),
        (r"(best|superior|优势).*?because.*?(best|superior|优势)", "defines advantage by itself"),
    ]
    for pattern, desc in circular_patterns:
        if re.search(pattern, lower):
            report.findings.append(Finding(
                dimension="logic",
                severity="major",
                title=f"Circular reasoning: {desc}",
                description=(
                    "The plan uses circular logic — claiming success/popularity as both "
                    "the outcome and the cause. This is a non-explanation. Real reasons "
                    "must be external: specific features, timing, cost advantage, etc."
                ),
            ))
            break


def _check_wishful_thinking(text: str, report: AuditReport) -> None:
    lower = text.lower()
    wishful_patterns = [
        (r"users? will (naturally|automatically|organically|simply|just)", "assumes adoption is automatic"),
        (r"(simply|just|easily|轻松|只需).*?(build|create|develop|开发|构建)", "assumes implementation is trivial"),
        (r"viral(ly)?|go.?viral|病毒式", "assumes virality without mechanism"),
    ]
    for pattern, desc in wishful_patterns:
        if re.search(pattern, lower):
            report.findings.append(Finding(
                dimension="logic",
                severity="major",
                title=f"Wishful thinking: {desc}",
                description=(
                    "The plan assumes something will happen 'naturally', 'simply', or 'virally' "
                    "without describing the mechanism. In reality: nothing is automatic. "
                    "Every claim needs a causal mechanism, not an adjective."
                ),
            ))
            break


# ═══════════════════════════════════════════════════════════
# STRUCTURE CHECKS (8)
# ═══════════════════════════════════════════════════════════

def _check_governance(text: str, report: AuditReport) -> None:
    if not re.search(r"(governance|steering|maintainer|bdf?l|core.?team|治理|决策机制|负责人)", text.lower()):
        report.findings.append(Finding(
            dimension="structure",
            severity="critical",
            title="No governance model defined",
            description=(
                "Projects without a governance model die when: "
                "(a) the original maintainer burns out, (b) a PR has conflicting "
                "opinions with no deciding authority, (c) a corporation forks "
                "the spec. MVP needs at least: who decides, how decisions are made, "
                "how to handle disagreements."
            ),
        ))


def _check_exit_plan(text: str, report: AuditReport) -> None:
    if not re.search(r"(abandon|sunset|archive|maintainer.?bus|continuity|退出|归档|善后|移交)", text.lower()):
        report.findings.append(Finding(
            dimension="structure",
            severity="major",
            title="No exit/sunset plan",
            description=(
                "If you stop maintaining this, what happens to adopters? "
                "A simple 'maintained as best-effort; adopters should pin versions; "
                "inactive 6+ months = archived' is better than silence. "
                "Without this, adopters have zero predictability."
            ),
        ))


def _check_adoption_path(text: str, report: AuditReport) -> None:
    steps = [
        r"quick.?start", r"getting.?started", r"pip install", r"npm install",
        r"install", r"setup", r"first.?steps", r"hello.?world", r"5.?minute",
        r"prototype", r"demo", r"example", r"tutorial", r"示例", r"教程", r"入门",
    ]
    found = sum(1 for p in steps if re.search(p, text.lower()))
    if found < 2:
        report.findings.append(Finding(
            dimension="structure",
            severity="major",
            title=f"Adoption path unclear (only {found}/{len(steps)} onboarding signals)",
            description=(
                "The plan describes what to build but not how a user goes "
                "from 'hearing about it' to 'using it productively' in under 5 minutes. "
                "If a new user can't get value in <5 min, they won't come back."
            ),
        ))


def _check_scope_boundary(text: str, report: AuditReport) -> None:
    if not re.search(r"(not.*?scope|out.?of.?scope|won.?.?t.?do|不做的|范围外|不做|非目标|excluded)", text.lower()):
        report.findings.append(Finding(
            dimension="structure",
            severity="major",
            title="Scope boundaries not defined",
            description=(
                "Every good project says what it WON'T do. Without explicit "
                "out-of-scope declarations, scope creep will blur the project's "
                "identity and delay every milestone. List at least 3 things this is NOT."
            ),
        ))


def _check_schema_validation(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(json.?schema|json.?spec|interagent\.json|protocol.?spec|接口规范|协议规范|schema.?def)", lower):
        if not re.search(r"(validate|validator|verify|schema.?check|校验|验证器)", lower):
            report.findings.append(Finding(
                dimension="structure",
                severity="critical",
                title="Schema/protocol defined without validator",
                description=(
                    "Defining a schema without a validator means: "
                    "(a) users write invalid specs by accident, "
                    "(b) implementations drift from the spec, "
                    "(c) you discover spec errors months later. "
                    "Validator must ship WITH the spec, not after."
                ),
            ))


def _check_timeline_milestones(text: str, report: AuditReport) -> None:
    lower = text.lower()
    timeline_signals = [
        r"week\s*\d+", r"month\s*\d+", r"phase\s*\d+", r"milestone",
        r"mvp.*?(by|before|within|deadline)", r"v0\.\d", r"v1\.0",
        r"第\d?(周|月|阶段)", r"里程碑", r"截止",
    ]
    found = sum(1 for p in timeline_signals if re.search(p, lower))
    if found < 1:
        report.findings.append(Finding(
            dimension="structure",
            severity="major",
            title="No timeline or milestones",
            description=(
                "A plan without any timeline is a wishlist. Even a rough "
                "'Week 1-2: MVP, Week 3-4: beta, Week 6: launch' is better than "
                "no temporal structure. Without milestones, there's no way to "
                "measure progress or detect slippage."
            ),
        ))


def _check_dependency_risk(text: str, report: AuditReport) -> None:
    lower = text.lower()
    platform_deps = re.findall(
        r"(?:depends?|relies?|requires?|需要|依赖).{0,30}?(?:on\s+)?(\w[\w\s]{2,25})",
        lower,
    )
    critical_deps = [
        d.strip() for d in platform_deps
        if any(kw in d for kw in [
            "platform", "api", "third.?party", "external", "第三方",
            "苹果", "google", "apple", "微信", "github",
        ])
    ]
    if len(critical_deps) >= 1:
        if not re.search(r"(fallback|contingency|备选|替代方案|if.*?unavailable|api.?change)", lower):
            report.findings.append(Finding(
                dimension="structure",
                severity="critical",
                title=f"Critical external dependency without fallback: '{critical_deps[0]}'",
                description=(
                    f"The plan depends on '{critical_deps[0]}' but has no fallback "
                    "if that dependency changes terms, deprecates APIs, or goes down. "
                    "Every external dependency needs a Plan B."
                ),
            ))


def _check_single_point_of_failure(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(only|sole|single|唯一|仅靠).{0,20}?(person|developer|server|provider|channel|渠道|开发者|服务器)", lower):
        report.findings.append(Finding(
            dimension="structure",
            severity="critical",
            title="Single point of failure identified",
            description=(
                "The plan mentions a sole person, server, or channel as the only option. "
                "What happens if that one thing fails? Bus factor = 1 is the #1 killer "
                "of early projects. Identify backup options or redundancy."
            ),
        ))


# ═══════════════════════════════════════════════════════════
# ENTITY CHECKS (7)
# ═══════════════════════════════════════════════════════════

def _check_data_sources(text: str, report: AuditReport) -> None:
    data_markers = re.findall(r"(\d[\d,]*[kKkMm]?\+?|\d+%|\d+\s*(?:stars|users|downloads|月活|日活|注册))", text)
    unsourced = []
    for marker in data_markers[:5]:
        idx = text.find(marker)
        if idx < 0:
            continue
        context_start = max(0, idx - 150)
        context_end = min(len(text), idx + len(marker) + 50)
        context = text[context_start:context_end].lower()
        has_source = any(
            s in context
            for s in ["source", "根据", "based on", "per ", "from ", "report", "data",
                       "survey", "statista", "来源", "数据来源", "报告", "研究"]
        )
        if not has_source:
            unsourced.append(marker)
    if unsourced:
        report.findings.append(Finding(
            dimension="entity",
            severity="major",
            title=f"{len(unsourced)} data point(s) lack source citations: {', '.join(unsourced[:3])}",
            description=(
                "Data points without source citations look fabricated, even if accurate. "
                "Every number needs: source name, date, methodology. "
                "If data is estimated, explicitly label it as 'estimated'."
            ),
            evidence=f"Unsourced: {', '.join(unsourced[:3])}",
        ))


def _check_facts(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(biggest|most popular|leading|first|only|第一|最大|最早|唯一|领先)", lower):
        if not re.search(r"(according to|source|data|排名|数据|根据|报告|report|研究|study)", lower):
            report.findings.append(Finding(
                dimension="entity",
                severity="major",
                title="Superlative claims without source",
                description=(
                    "Claims like 'biggest', 'first', 'only' need a verifiable source. "
                    "Without one, they read as marketing fluff that undermines credibility. "
                    "If you can't source it, rephrase to 'one of the largest' or drop it."
                ),
            ))


def _check_role_incentives(text: str, report: AuditReport) -> None:
    lower = text.lower()
    roles = re.findall(
        r"(?:plugin developer|平台方|platform|maintainer|contributor|开发者|贡献者|维护者|user|用户|企业|enterprise)",
        lower,
    )
    unique_roles = set(roles)
    if len(unique_roles) >= 2:
        if not re.search(r"(incentive|motivation|why.*?would|利益|动力|为什么.*?参与|好处)", lower):
            report.findings.append(Finding(
                dimension="entity",
                severity="major",
                title=f"Multiple roles ({len(unique_roles)}) listed but incentives not analyzed",
                description=(
                    f"The plan mentions {len(unique_roles)} roles "
                    f"({', '.join(list(unique_roles)[:4])}) but doesn't analyze "
                    "why each would participate. Every role needs a 'what's in it for me' "
                    "answer. Especially: why would platforms adopt a standard that reduces "
                    "their lock-in?"
                ),
            ))


def _check_economics(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if not re.search(r"(cost|revenue|budget|sponsor|funding|免费|收费|成本|收入|预算|赞助|融资|定价|pricing)", lower):
        report.findings.append(Finding(
            dimension="entity",
            severity="major",
            title="No economic model mentioned",
            description=(
                "Even open-source projects have costs (CI, hosting, domains, "
                "developer time). A brief 'funded by X / volunteer-run / "
                "sponsor-supported' is better than silence. Projects without "
                "an economic model die when the initial enthusiasm fades."
            ),
        ))


def _check_user_vs_developer(text: str, report: AuditReport) -> None:
    lower = text.lower()
    has_dev_focus = re.search(r"(developer|sdk|api|plugin|integrat|开发者|插件|集成)", lower)
    has_user_claim = re.search(r"(\d[\d,]*[kKmM]?\+?\s*(?:users|用户|downloads|下载))", lower)
    if has_dev_focus and has_user_claim:
        if not re.search(r"(developer.*?user|user.*?developer|开发者.*?用户|用户.*?开发者|distinct|different)", lower):
            report.findings.append(Finding(
                dimension="entity",
                severity="major",
                title="Confusing developers with users",
                description=(
                    "The plan mentions both developers (SDK/API) and user metrics, "
                    "but doesn't distinguish them. GitHub stars ≠ users. "
                    "Downloads ≠ active users. Developer adoption ≠ end-user adoption. "
                    "Conflating these inflates perceived traction."
                ),
            ))


def _check_revenue_vs_growth(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(revenue|收入|营收|profit|利润)", lower):
        if re.search(r"(growth|增长|growth rate|增长率)", lower):
            if not re.search(r"(unit.?economics|unit.?cost|arpu|ltv|cac|margin|毛利率|客单价|获客成本|生命周期价值)", lower):
                report.findings.append(Finding(
                    dimension="entity",
                    severity="major",
                    title="Revenue and growth mentioned without unit economics",
                    description=(
                        "Revenue + growth without unit economics (CAC, LTV, ARPU, margin) "
                        "is a vanity metric. Growing revenue while losing money on every "
                        "customer is a death spiral. Unit economics must be explicit."
                    ),
                ))


def _check_survivorship_bias(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(similar.*?succeeded|like.*?(airbnb|uber|notion|figma|slack|discord)|类似.*?成功|对标)", lower):
        if not re.search(r"(survivorship|failed|failure|died|shut.?down|幸存者偏差|失败|倒闭|关停)", lower):
            report.findings.append(Finding(
                dimension="entity",
                severity="major",
                title="Survivorship bias: citing only successful analogues",
                description=(
                    "The plan cites successful companies as proof the model works, "
                    "but ignores the 99% of similar companies that failed. "
                    "For every Airbnb there were 100 failed rental-marketplace startups. "
                    "Acknowledge what differentiated the winners from the dead."
                ),
            ))


# ═══════════════════════════════════════════════════════════
# TECHNICAL CHECKS (8)
# ═══════════════════════════════════════════════════════════

def _check_implementation_path(text: str, report: AuditReport) -> None:
    lower = text.lower()
    tech_keywords = [
        r"python", r"typescript", r"rust", r"go\b", r"java\b", r"c\b", r"c\+\+", r"swift",
        r"sdk", r"api", r"cli", r"http", r"json.?schema", r"bridge",
        r"esp32", r"stm32", r"arduino", r"raspberry",
        r"mqtt", r"websocket", r"rest", r"grpc",
        r"postgresql|mysql|sqlite|mongodb|redis",
        r"docker", r"kubernetes", r"aws\b|gcp|azure",
        r"数据库", r"缓存", r"队列", r"微服务",
        r"injection.?mold", r"pcb", r"firmware", r"sensor",
    ]
    found_tech = sum(1 for p in tech_keywords if re.search(p, lower))
    if found_tech < 3:
        report.findings.append(Finding(
            dimension="technical",
            severity="critical",
            title=f"Missing concrete technology choices (only {found_tech}/{len(tech_keywords)})",
            description=(
                "A project plan without concrete tech choices is a wishlist, "
                "not a plan. At minimum specify: language, SDK format, transport protocol, "
                "data store, deployment target. 'Use AI' is not an implementation plan."
            ),
        ))


def _check_security_by_default(text: str, report: AuditReport) -> None:
    lower = text.lower()
    security_keywords = [
        r"signing|签名|signed", r"permission|权限", r"sandbox|沙箱",
        r"audit|审计", r"encrypt|加密", r"auth|认证|鉴权",
        r"security|安全", r"firewall|防火墙", r"tls|ssl|https",
    ]
    security_mentions = sum(1 for p in security_keywords if re.search(p, lower))
    if security_mentions < 1:
        report.findings.append(Finding(
            dimension="technical",
            severity="critical",
            title="Security not mentioned at all",
            description=(
                "For any cross-platform or user-facing product, security is not optional. "
                "Missing: signing chain, permission model, sandboxing, audit trail, "
                "data encryption. Adding security post-hoc is 10-100x more expensive."
            ),
        ))
    elif security_mentions < 2:
        report.findings.append(Finding(
            dimension="technical",
            severity="major",
            title=f"Security mentioned but shallow (only {security_mentions} aspect(s))",
            description=(
                "Security needs coverage across multiple dimensions: authentication, "
                "authorization, data encryption, audit trail, input validation. "
                f"Only {security_mentions} aspect(s) mentioned — too narrow."
            ),
        ))


def _check_edge_cases(text: str, report: AuditReport) -> None:
    lower = text.lower()
    edge_keywords = [
        r"error.?handling", r"edge.?case", r"timeout", r"failover",
        r"degrade|降级", r"fallback|回退", r"validation", r"边界",
        r"retry|重试", r"rate.?limit|限流",
    ]
    found = sum(1 for p in edge_keywords if re.search(p, lower))
    if found < 1:
        report.findings.append(Finding(
            dimension="technical",
            severity="major",
            title="No edge-case handling mentioned",
            description=(
                "No discussion of: what happens when a dependency fails mid-operation? "
                "When input is malformed? When an API changes? When network is down? "
                "When traffic spikes 10x? Every plan needs at least a 'failure modes' section."
            ),
            evidence=f"0/{len(edge_keywords)} edge-case signals found",
        ))
    elif found < 3:
        report.findings.append(Finding(
            dimension="technical",
            severity="minor",
            title=f"Edge-case handling incomplete (only {found}/{len(edge_keywords)})",
            description=(
                "Some edge cases mentioned but coverage is thin. "
                "A robust plan addresses at least: network failure, invalid input, "
                "dependency outage, and traffic spikes."
            ),
            evidence=f"Found: {found}/{len(edge_keywords)}",
        ))


def _check_maintainability(text: str, report: AuditReport) -> None:
    lower = text.lower()
    signals = [
        (r"(version|semver|breaking.?change|版本)", "versioning"),
        (r"(test|ci|continuous|测试|自动化测试)", "testing/CI"),
        (r"(doc|docs?|documentation|文档)", "documentation"),
        (r"(contributing|contribute|pr|pull.?request|贡献|提交)", "contribution"),
    ]
    found = sum(1 for p, _ in signals if re.search(p, lower))
    if found < 2:
        report.findings.append(Finding(
            dimension="technical",
            severity="major",
            title=f"Maintainability concerns not addressed ({found}/{len(signals)})",
            description=(
                "Without versioning, CI, documentation, and contribution process, "
                "the project will accumulate technical debt faster than it can be "
                "paid down. Open-source especially needs these from day 1."
            ),
            evidence=f"Found: {found}/{len(signals)}",
        ))


def _check_data_privacy(text: str, report: AuditReport) -> None:
    lower = text.lower()
    collects_data = re.search(r"(collect|store|gather|保存|收集|上传|存储).*?(user.?data|personal|profile|email|phone|address|location|数据|个人信息|邮箱|手机)", lower)
    explicitly_no_data = re.search(r"(no.*?(data|pii|personal|collect|收集)|不收集|不存储|无数据|零数据)", lower)
    if explicitly_no_data:
        return
    if collects_data:
        if not re.search(r"(consent|opt.?in|anonymiz|encrypt|privacy.?policy|同意|匿名|脱敏|隐私政策|合规|gdpr|pipl)", lower):
            report.findings.append(Finding(
                dimension="technical",
                severity="critical",
                title="User data collected without privacy compliance mention",
                description=(
                    "The plan mentions collecting/storing user data but says nothing "
                    "about consent, anonymization, encryption, or GDPR/PIPL compliance. "
                    "This is a legal liability, not just a technical gap."
                ),
            ))


def _check_api_stability(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(api|sdk|plugin|integration|接口|插件|集成)", lower):
        if not re.search(r"(version|stability|backward.?compat|deprecat|版本|兼容|废弃|breaking)", lower):
            report.findings.append(Finding(
                dimension="technical",
                severity="major",
                title="API/plugin interface defined without stability guarantee",
                description=(
                    "If others build on your API/SDK, breaking changes destroy their work. "
                    "The plan needs: (1) versioning strategy, (2) backward compat guarantee, "
                    "(3) deprecation process. Without these, no one will invest in integration."
                ),
            ))


def _check_deployment_ops(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(deploy|host|server|cloud|生产|部署|运维|上线|发布)", lower):
        ops_signals = [
            r"monitor|监控", r"alert|告警", r"log|日志", r"backup|备份",
            r"rollback|回滚", r"health.?check|健康检查",
        ]
        found = sum(1 for p in ops_signals if re.search(p, lower))
        if found < 1:
            report.findings.append(Finding(
                dimension="technical",
                severity="major",
                title="Deployment mentioned without operational readiness",
                description=(
                    "The plan discusses deployment but not how to keep it running: "
                    "monitoring, alerting, logging, backup, rollback. "
                    "A system that can't be observed can't be debugged in production."
                ),
            ))


def _check_dependency_sustainability(text: str, report: AuditReport) -> None:
    lower = text.lower()
    deps = re.findall(r"(?:use|using|采用|使用|基于)\s+([\w\-\.]+(?:js|py|rs|go|rb|java)[\w\-\.]*)", lower)
    if not deps:
        deps = re.findall(r"([\w\-]+(?:\.js|\.py|react|vue|next|express|fastapi|django|flask))", lower)
    if len(deps) >= 3:
        if not re.search(r"(pin|lock|version.?fix|固定版本|锁定|兼容性|compatibility)", lower):
            report.findings.append(Finding(
                dimension="technical",
                severity="minor",
                title=f"Multiple dependencies ({len(deps)}) without version pinning strategy",
                description=(
                    f"Found {len(deps)} dependencies ({', '.join(deps[:4])}). "
                    "Without version pinning and lock files, a dependency update "
                    "can break the build at any time. Specify: lock file, pin strategy, "
                    "update policy."
                ),
            ))


# ═══════════════════════════════════════════════════════════
# MARKET CHECKS (5)
# ═══════════════════════════════════════════════════════════

def _check_competitor_analysis(text: str, report: AuditReport) -> None:
    lower = text.lower()
    has_market = re.search(r"(market|competitor|landscape|竞争|对手|市场|行业|赛道)", lower)
    if not has_market:
        return
    competitors = re.findall(
        r"(?:vs\.?|versus|compete|competing|against|对标|竞品|竞争对手)[^\w]{0,15}?([\w\.]+[\w]{1,20})",
        lower,
    )
    if not competitors:
        named = re.findall(r"\b(notion|figma|slack|discord|airbnb|uber|trello|asana|jira|whatsapp|微信|钉钉|飞书|小红书|抖音)\b", lower)
        if not named:
            report.findings.append(Finding(
                dimension="market",
                severity="major",
                title="Market mentioned but no specific competitors named",
                description=(
                    "The plan mentions the market/competition but doesn't name "
                    "any specific competitor. This suggests shallow market research. "
                    "Name at least 3 direct competitors and explain how this differs."
                ),
            ))


def _check_differentiation(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(competitor|alternative|竞争|竞品|对标|替代)", lower):
        if not re.search(r"(unlike|differentiat|better|advantage|faster|cheaper|simpler|不同于|差异化|优势|更快|更便宜|更简单)", lower):
            report.findings.append(Finding(
                dimension="market",
                severity="critical",
                title="Competitors mentioned without differentiation",
                description=(
                    "Naming competitors without explaining how you're different "
                    "is worse than not naming them — it implies you have no advantage. "
                    "Differentiation must be specific: '10x faster at X', "
                    "'first to support Y', 'Z% cheaper for use case W'."
                ),
            ))


def _check_timing_window(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(market|opportunity|gap|市场|机会|空白|蓝海)", lower):
        if not re.search(r"(timing|why.?now|trend|shift|recent|窗口|时机|为什么是现在|趋势|变化|新兴)", lower):
            report.findings.append(Finding(
                dimension="market",
                severity="major",
                title="Market opportunity claimed without 'why now' analysis",
                description=(
                    "Every market gap has a timing question: why didn't someone fill "
                    "this 2 years ago? Why will it work now? Common answers: new technology, "
                    "regulatory change, demographic shift, platform launch. "
                    "Without a 'why now', the gap might be a mirage."
                ),
            ))


def _check_tam_reality(text: str, report: AuditReport) -> None:
    lower = text.lower()
    tam_markers = re.findall(
        r"(?:tam|sam|som|total.*?addressable|market.*?size|市场规模|万亿|千亿|百亿|billion|trillion)\b.*?(\d[\d,.]*\s*[kKmMbBtT]?)",
        lower,
    )
    if tam_markers:
        for tam_val in tam_markers:
            val_str = tam_val.strip().lower()
            try:
                if 't' in val_str or '万亿' in lower[max(0, lower.find(val_str)-20):lower.find(val_str)+20]:
                    report.findings.append(Finding(
                        dimension="market",
                        severity="major",
                        title=f"Extremely large TAM claim: '{val_str}'",
                        description=(
                            f"TAM of '{val_str}' is likely top-down market sizing that includes "
                            "every tangentially related customer. Bottom-up sizing "
                            "(reachable customers x price) is more credible. "
                            "Large TAMs without bottom-up validation are red flags."
                        ),
                    ))
                    break
            except (ValueError, IndexError):
                pass
    if re.search(r"(tam|sam|som|总可触达|市场规模)", lower):
        if not re.search(r"(bottom.?up|自下而上|reachable|可触达|保守|conservative)", lower):
            report.findings.append(Finding(
                dimension="market",
                severity="minor",
                title="Market sizing appears top-down without bottom-up validation",
                description=(
                    "Top-down TAM ('market is $X billion') is easy to inflate. "
                    "Bottom-up TAM ('N reachable customers * $Y price') is more "
                    "credible and forces specificity. Include both."
                ),
            ))


def _check_distribution_channel(text: str, report: AuditReport) -> None:
    lower = text.lower()
    if re.search(r"(launch|release|go.?live|上线|发布|推出)", lower):
        if not re.search(r"(channel|distribution|marketing|seo|viral|referral|渠道|分发|营销|推广|获客)", lower):
            report.findings.append(Finding(
                dimension="market",
                severity="major",
                title="Launch mentioned without distribution strategy",
                description=(
                    "'We will launch' is not a plan. How will users find this? "
                    "Distribution channels must be explicit: SEO, product hunt, "
                    "integrations marketplace, partnerships, viral loops, paid ads. "
                    "The best product with zero distribution = zero users."
                ),
            ))


# ────────────────────────────────────────────────────────
# CLI ENTRY
# ────────────────────────────────────────────────────────

def main():
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

    by_sev: dict[str, list[Finding]] = {"critical": [], "major": [], "minor": [], "suggestion": []}
    for f in report.findings:
        by_sev.setdefault(f.severity, []).append(f)

    for sev in ["critical", "major", "minor", "suggestion"]:
        items = by_sev.get(sev, [])
        if not items:
            continue
        badge = {"critical": "!!", "major": "!", "minor": "~", "suggestion": "?"}[sev]
        print(f"  [{sev.upper()}] ({len(items)})")
        for f in items:
            print(f"    {badge} [{f.dimension}] {f.title}")
            print(f"      {f.description[:150]}")
            if f.evidence:
                print(f"      Evidence: {f.evidence[:120]}")
        print()

    if report.critical_count > 0:
        print(f"  !! {report.critical_count} CRITICAL issues found")
        print(f"  Verdict: {report.verdict}")
        if report.verdict == "REJECT":
            print("  >>> REJECTED: 3+ critical issues. Return to refinement.")
            sys.exit(1)
        elif report.verdict == "CONDITIONAL":
            print("  >>> CONDITIONAL: Fix critical issues before proceeding.")
            sys.exit(0)
    else:
        print(f"  Verdict: {report.verdict} (score: {report.score}/100, grade: {report.grade})")


if __name__ == "__main__":
    main()

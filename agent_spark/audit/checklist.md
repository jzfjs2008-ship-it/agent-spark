# Structured Project Audit Checklist (v2.0 — Stricter)

> Before finalizing any project plan, run this systematic audit to catch errors.
> 36 checks across 5 dimensions. Scored 0-100 with grade (A-F) and verdict (PASS/WEAK_PASS/CONDITIONAL/REJECT).

## Audit Dimensions

| Dimension | Abbr | Checks | What it catches |
|-----------|------|--------|-----------------|
| Logic | LOG | 8 | Broken causation, wishful thinking, circular reasoning, vague verbs, contradictions, survivorship bias |
| Structure | STR | 8 | Missing modules, governance gaps, no timeline, dependency risk, single-point-of-failure |
| Entity | ENT | 7 | Unsourced data, user≠developer confusion, revenue≠growth, survivorship bias |
| Technical | TEC | 8 | Security holes, no privacy compliance, API instability, no ops readiness, dependency risk |
| Market | MKT | 5 | No competitors named, no differentiation, no "why now", inflated TAM, no distribution |

## Scoring

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Ready to execute |
| 75-89 | B | Minor issues, proceed with fixes |
| 60-74 | C | Significant gaps, needs rework |
| 40-59 | D | Major problems, return to planning |
| 0-39 | F | Fundamental flaws, start over |

## Verdict Rules

| Verdict | Condition | Action |
|---------|-----------|--------|
| PASS | score ≥ 75, no critical | Present to user |
| WEAK_PASS | score 60-74, no critical | Fix majors, then present |
| CONDITIONAL | 1-2 criticals | Fix criticals first, then re-audit |
| REJECT | 3+ criticals | Return to refinement step |

## Logic Checklist (8 checks)

### L1. Is the core promise deliverable?
- [ ] Can the one-liner survive scrutiny?
- [ ] If claiming "cross-platform" — how are capability asymmetries handled?
- [ ] Are unsupported platforms explicitly noted?
- [ ] Is "unlimited" or "works everywhere" qualified?

### L2. Is the causal chain complete?
- [ ] Does the plan address why users would migrate or adopt?
- [ ] Is "user wants X" confused with "user will pay for X"?
- [ ] Are switching costs, learning curves, and migration paths addressed?
- [ ] Is adoption assumed "natural" without mechanism?

### L3. Are hidden assumptions surfaced?
- [ ] What external factors must align? (Platform buy-in, community adoption, API stability)
- [ ] Is the plan still valuable if all assumptions fail?
- [ ] Is there an explicit "Key Assumptions" section?

### L4. Is it logically self-consistent?
- [ ] Any internal contradictions? ("lightweight" but depends on 5 services)
- [ ] Does security policy conflict with product goals?
- [ ] Are contradictions acknowledged with bridge words (but, however, trade-off)?

### L5. Is the network effect overestimated?
- [ ] How many platforms/plugins/users are needed for a tipping point?
- [ ] Can MVP reach that threshold?
- [ ] Is there a cold-start strategy that doesn't rely on the network effect itself?

### L6. Does the plan rely on vague action verbs?
- [ ] Count: leverage, utilize, enhance, optimize, streamline, empower, transform, disrupt
- [ ] 3+ vague verbs = plan describes no concrete mechanism
- [ ] Replace each with: what happens, to what, with what input, producing what output

### L7. Circular reasoning?
- [ ] Is success/popularity used as both cause and effect?
- [ ] Are advantages defined by themselves ("superior because superior")?

### L8. Wishful thinking?
- [ ] "Users will naturally/automatically/organically adopt" — no, they won't
- [ ] "Simply build/create" — nothing is simple in implementation
- [ ] "Viral" without viral mechanism — virality is engineered, not hoped for

## Structure Checklist (8 checks)

### S1. Governance model?
- [ ] Who decides? BDFL, core team, voting?
- [ ] How are disagreements resolved?
- [ ] What happens when maintainer burns out?

### S2. Exit/sunset plan?
- [ ] If maintainer becomes inactive, what happens?
- [ ] Version pinning guidance for adopters?
- [ ] Data/portability guarantees?

### S3. Adoption path?
- [ ] How many steps from "heard about it" to "using it productively"?
- [ ] Can a new user get value in <5 minutes?
- [ ] Is there a hello-world / quickstart?

### S4. Scope boundaries?
- [ ] Explicit "what we won't do" list (at least 3 items)?
- [ ] Out-of-scope labeled clearly?

### S5. Schema/protocol validation?
- [ ] If defining a schema/spec — is a validator shipped with it?
- [ ] Can users validate their specs immediately?

### S6. Timeline and milestones?
- [ ] Are there phases, weeks, or MVP deadlines?
- [ ] Is there a v0.1/v1.0 target?
- [ ] Without timeline = wishlist, not plan

### S7. Dependency risk?
- [ ] Are external dependencies identified?
- [ ] Is there a fallback if a dependency changes terms or deprecates?
- [ ] Plan B for every critical external dependency?

### S8. Single point of failure?
- [ ] Is the plan dependent on a single person, server, or channel?
- [ ] Bus factor: what's the minimum number of people who must stay for the project to survive?

## Entity Checklist (7 checks)

### E1. Data points sourced?
- [ ] Every number needs: source name, date, methodology
- [ ] If estimated, labeled as "estimated"?
- [ ] All unsourced numbers flagged?

### E2. Superlative claims verified?
- [ ] "Biggest", "first", "only" — according to whom?
- [ ] If you can't source it, rephrase or drop it

### E3. Role incentives aligned?
- [ ] Every role has a "what's in it for me" answer?
- [ ] Especially: why would platforms adopt a standard that reduces lock-in?

### E4. Economic model exists?
- [ ] Costs: CI, hosting, domains, developer time
- [ ] Revenue/sustainability: sponsorship? enterprise? volunteer?
- [ ] Even "free" has opportunity cost

### E5. Users ≠ Developers?
- [ ] GitHub stars ≠ users
- [ ] Downloads ≠ active users
- [ ] Developer adoption ≠ end-user adoption
- [ ] Are these clearly distinguished?

### E6. Revenue ≠ Growth?
- [ ] Revenue + growth without unit economics = vanity metric
- [ ] CAC, LTV, ARPU, margin must be explicit
- [ ] Growing while losing money on every customer = death spiral

### E7. Survivorship bias?
- [ ] Citing Airbnb/Uber/Notion as proof the model works?
- [ ] What about the 99% that failed with the same model?
- [ ] What differentiated winners from the dead?

## Technical Checklist (8 checks)

### T1. Implementation path concrete?
- [ ] Specific language, SDK format, transport protocol?
- [ ] "Use AI" is not an implementation plan
- [ ] At least 3 concrete tech choices?

### T2. Security by default?
- [ ] Security mentioned across 2+ dimensions (auth, encrypt, permission, audit)?
- [ ] Single mention = too shallow
- [ ] Zero mentions = critical failure

### T3. Edge cases handled?
- [ ] Network failure, invalid input, dependency outage, traffic spike?
- [ ] At least 1 explicit edge-case discussion?
- [ ] At least 3 for "robust" rating?

### T4. Maintainability?
- [ ] Versioning strategy? (semver, compat guarantee, deprecation process)
- [ ] CI/testing plan?
- [ ] Documentation plan?
- [ ] Contribution process?
- [ ] At least 2 of 4 required

### T5. Data privacy?
- [ ] If collecting user data: consent, anonymization, encryption?
- [ ] GDPR/PIPL compliance mentioned?
- [ ] Privacy policy linked?

### T6. API stability?
- [ ] Versioning for API/SDK/plugin interfaces?
- [ ] Backward compatibility guarantee?
- [ ] Deprecation process?
- [ ] Without these, no one invests in integration

### T7. Deployment/ops?
- [ ] Monitoring, alerting, logging?
- [ ] Backup, rollback?
- [ ] Health checks?
- [ ] A system that can't be observed can't be debugged

### T8. Dependency sustainability?
- [ ] Version pinning / lock files?
- [ ] Update policy (when/how to upgrade deps)?
- [ ] What happens when a dep breaks?

## Market Checklist (5 checks)

### M1. Competitors named?
- [ ] At least 3 direct competitors identified by name?
- [ ] "Market is competitive" without naming anyone = shallow research

### M2. Differentiation specific?
- [ ] "Unlike X, we do Y" — is Y specific and measurable?
- [ ] Naming competitors without differentiation = worse than not naming them
- [ ] Differentiation must be: 10x faster at X, first to support Y, Z% cheaper for W

### M3. "Why now" analysis?
- [ ] Why didn't someone fill this gap 2 years ago?
- [ ] What changed? (new tech, regulation, demographic shift, platform launch)
- [ ] Without "why now", the gap might be a mirage

### M4. TAM realistic?
- [ ] Bottom-up sizing (N reachable customers × $price)?
- [ ] Top-down TAM without bottom-up validation = red flag
- [ ] Trillion/billion TAMs need extraordinary evidence

### M5. Distribution strategy?
- [ ] How will users find this? (SEO, Product Hunt, marketplace, partnerships, viral loops)
- [ ] "We will launch" is not a distribution plan
- [ ] Best product + zero distribution = zero users

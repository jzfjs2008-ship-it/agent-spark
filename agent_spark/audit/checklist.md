# Structured Project Audit Checklist

> Before finalizing any project plan, run this systematic audit to catch errors.

## Audit Dimensions

| Dimension | Abbr | What it checks |
|-----------|------|----------------|
| Logic | LOG | Broken causation, promise vs capability mismatch, contradictions |
| Structure | STR | Missing modules, wrong ordering, governance gaps, unclear boundaries |
| Entity | ENT | Unsourced data, factual errors, role confusion |
| Technical | TEC | Infeasible implementation, security holes, maintainability debt |

## Logic Checklist

### L1. Is the core promise deliverable?
- [ ] Can the one-liner survive scrutiny?
- [ ] If claiming "cross-platform" — how are capability asymmetries handled?
- [ ] Are unsupported platforms explicitly noted?

### L2. Is the causal chain complete?
- [ ] Does the plan address why users would migrate or adopt?
- [ ] Is "user wants X" confused with "user will pay for X"?

### L3. Are hidden assumptions surfaced?
- [ ] What external factors must align? (Platform buy-in, community adoption, API stability)
- [ ] Is the plan still valuable if all assumptions fail?

### L4. Is it logically self-consistent?
- [ ] Any internal contradictions? ("lightweight" but depends on 5 services)
- [ ] Does security policy conflict with product goals?

### L5. Is the network effect overestimated?
- [ ] How many platforms/plugins/users are needed for a tipping point?
- [ ] Can MVP reach that threshold?

## Structure Checklist

### S1. What's missing?
- [ ] Governance model? (Decision authority, breaking-change process)
- [ ] Exit plan? (What happens if maintainer leaves?)
- [ ] Adoption path? (How many steps from "heard about it" to "using it"?)

### S2. Is the ordering right?
- [ ] "Standard before implementation" — should be "PoC before standard."
- [ ] Is schema locked before real-world validation?

### S3. Are boundaries clear?
- [ ] Explicit "what we won't do" list?
- [ ] Is security embedded in design or bolted on?

### S4. Is there an ecosystem entry point?
- [ ] How do users discover compatible plugins/products?
- [ ] Discovery/search/ranking mechanism?

## Entity Checklist

### E1. Do data points have sources?
- [ ] Market size, user count — based on what?
- [ ] Are "stars" confused with "developers"?
- [ ] If data unavailable, is "assumption unvalidated" noted?

### E2. Fact-checking
- [ ] Competitive claims sourced? ("biggest" → "according to X")?
- [ ] Competitor descriptions precise? (Not "App A is slow" but "App A is slow at Y under Z conditions")

### E3. Are all role incentives aligned?
- [ ] Roles listed: developers, users, platform owners, reviewers, maintainers?
- [ ] Why would each role participate? (Especially platform owners who see standards as threat)

### E4. Economic model exists?
- [ ] Even if free — what's the opportunity cost?
- [ ] Sustainability: sponsorship? enterprise contracts? volunteer-run?

## Technical Checklist

### T1. Is the implementation path feasible?
- [ ] Does each MVP module have a concrete implementation plan?
- [ ] "Use AI" is not an implementation plan.
- [ ] Multi-language bridge maintenance cost accounted for?

### T2. Is security by default?
- [ ] Is security a first principle or a separate document?
- [ ] Is sandboxing/isolation truly realizable on claimed platforms?
- [ ] Trust anchor problem solved? (How does user verify signatures?)

### T3. Edge cases handled?
- [ ] Input validation? (glob path traversal, null, malformed input)
- [ ] Offline/degraded behavior?
- [ ] If generated code has bugs, how does user debug?

### T4. Maintainability
- [ ] Versioning strategy? (compatibility guarantee, migration cycle)
- [ ] CI/testing plan?
- [ ] When a new platform appears, how much code must change?

## Audit Report Template

```markdown
# Audit Report: [Project Name]

## Summary
- Total findings: N (Logic: X / Structure: Y / Entity: Z / Technical: W)
- Critical: N (must fix before proceeding)
- Major: N (strongly recommended)

## Findings
### Critical
### Major
### Minor

## Priority Recommendations
### Must Fix
### Should Fix
### Could Fix
```

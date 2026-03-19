# Sprint Design Review Axes — Detailed Checklist

## Panel selection

| Sprint type | Experts | Axes |
|-------------|---------|------|
| `strategy` | 量化策略师, 统计学家, 风控专家, 代码评审专家 | S1, S2, S3, S4, C, D |
| `engineering` | 架构师, 代码评审专家, QA 负责人 | A, B, C, D, E |
| `hybrid` | 量化策略师, 架构师, 代码评审专家, 风控专家 | S1, S2, A, B, S4, C, D |

---

## Strategy Axes

### Axis S1: Strategy Rationality (量化策略师)
- [ ] PnL decomposition covers all material alpha/cost sources (entry edge, exit cost, adverse selection, market impact, funding cost)
- [ ] No missing penalty terms in the objective function
- [ ] Regime classification captures genuine structural differences, not noise
- [ ] Threshold choices have empirical or theoretical justification (not arbitrary round numbers)
- [ ] Position sizing methodology grounded in theory (Kelly, half-Kelly, risk parity) or has stated rationale
- [ ] Challenger/anti-alpha matrix follows proper backtesting discipline (no peeking, consistent universe, same cost assumptions)
- [ ] "Regime-first not sport-first" hypothesis honestly examined — are there structural microstructure differences regime labels cannot capture?
- [ ] Counterfactual analysis correctly accounts for second-order effects (market impact, opportunity cost, adverse selection)
- [ ] Non-goals are genuinely non-goals, not things the sprint couldn't figure out
- [ ] The strategy would make sense to a practitioner at a real quant fund

### Axis S2: Methodology Rigor (量化策略师)
- [ ] Evidence windows appropriate for the claim (short window → weak regime stability claim)
- [ ] Backtesting avoids: look-ahead bias, survivorship bias, transaction cost underestimation
- [ ] "Wallet-compatible" evidence standard correctly defined and consistently applied
- [ ] Promotion gates calibrated against the actual decision they gate
- [ ] No hidden data snooping (using the same window for discovery and validation)
- [ ] Alpha decay considered — how long do regime signals persist?

### Axis S3: Statistical Rigor (统计学家)
- [ ] Sample sizes sufficient for claims: N cells × K conditions → K/N >= 30 per cell for means
- [ ] Multiple testing: N regimes × M challengers → family-wise error rate considered?
- [ ] Holdout design truly independent; long enough to capture regime transitions
- [ ] Minimum sample size statistically justified (not just round numbers)
- [ ] Overfitting risk: free parameters vs observations ratio < 1:10
- [ ] Stationarity assumption examined: do optimal bucket edges shift over time?
- [ ] Effect size vs statistical significance: are improvements practically meaningful given estimation uncertainty?
- [ ] Confidence intervals or uncertainty quantification present
- [ ] Selection bias from focusing on top-N worst events for governance design
- [ ] Base rate: what fraction of trades are profitable? Does governance improve this materially?

### Axis S4: Risk Control (风控专家)
- [ ] Worst-case scenario: what if ALL governance assumptions wrong simultaneously?
- [ ] Wallet exposure during holdout/development period bounded with interim protection
- [ ] Canary blast radius appropriate (e.g., 10% daily buy_notional)
- [ ] Kill switch exists and is tested
- [ ] Drawdown circuit breaker for sprint execution period
- [ ] Correlation risk: can multiple "safe" regimes fail simultaneously?
- [ ] Model risk: what if the regime classification itself is wrong?
- [ ] Operational risk: rollback procedure, time-to-rollback, data integrity during transitions
- [ ] Tail risk: can governance make things worse (blocking good trades, missing bad ones)?
- [ ] Time-to-recovery: how quickly can the system return to pre-governance state?

---

## Engineering Axes

### Axis A: Design Rationality (架构师)
- [ ] Problem statement references concrete evidence (metrics, incidents, user feedback)
- [ ] Sprint goal can be stated in one sentence
- [ ] Scope bounded: affected files/modules listed
- [ ] Non-goals section exists and is specific
- [ ] Pack dependency graph has no cycles
- [ ] Each Pack has risk/rollback documented
- [ ] No overlap with prior sprint deliverables (check sprint history)
- [ ] Estimated effort per Pack is realistic (≤1 day guideline)
- [ ] Performance vs complexity tradeoff is explicit and justified
- [ ] Module boundary changes don't violate existing separation of concerns
- [ ] No hidden coupling introduced between previously independent modules

### Axis B: Technical Route (架构师)
- [ ] Approach reuses existing project patterns (check module map)
- [ ] No new parallel data structures when existing ones suffice
- [ ] API field usage matches docs/research/polymarket-api contracts
- [ ] Performance targets have measured baselines
- [ ] Concurrency model consistent with project (asyncio/threading)
- [ ] Third-party dependencies justified and version-pinned
- [ ] YAGNI: each deliverable solves a stated problem, not a hypothetical one
- [ ] Industry best practices cited for non-obvious technical choices
- [ ] Risk mitigation proportional to blast radius (not under/over-engineered)
- [ ] Degradation/fallback path exists for external service dependencies

### Axis C: Acceptance Criteria (代码评审专家)
- [ ] Every Pack has DoD with binary pass/fail conditions
- [ ] Test commands are copy-paste runnable
- [ ] Artifact output paths listed
- [ ] Metric thresholds are numbers, not adjectives
- [ ] Evidence collection method defined (log grep, JSON field, test assert)
- [ ] Rollback criteria defined (when to revert)
- [ ] Referenced code paths actually exist (Glob/Grep validated)
- [ ] Test file targets exist or explicitly marked "to create"

### Axis D: Information Sufficiency (代码评审专家)
- [ ] A fresh agent can execute Pack without clarifying questions
- [ ] Files to create/modify listed per Pack
- [ ] Data schemas (input/output) specified for new interfaces
- [ ] Config/env prerequisites documented
- [ ] Known pitfalls from pitfalls.md addressed or acknowledged
- [ ] Integration points with other Packs are explicit
- [ ] Edge cases enumerated per Pack (at least happy/error/boundary)

### Cross-Axis E: QA Lead (测试策略 + 风险评估)

#### Test strategy feasibility
- [ ] Test approach is realistic given project infrastructure (pytest, no CI)
- [ ] Integration tests planned where unit tests alone are insufficient
- [ ] Test dependencies (fixtures, mock data, external services) accounted for
- [ ] Test effort is included in Pack sizing (not an afterthought)
- [ ] Test naming/structure follows project conventions

#### Risk assessment completeness
- [ ] Blast radius per Pack explicitly assessed
- [ ] Failure modes and degradation paths documented
- [ ] Monitoring/alerting needs identified for post-deploy
- [ ] Rollback complexity assessed (data migration, config, feature flags)
- [ ] Dependency on external services has fallback/timeout strategy

#### Acceptance testability
- [ ] Each DoD criterion maps to a concrete test or verification command
- [ ] Negative tests defined where needed (what should NOT happen)
- [ ] Performance thresholds testable in current environment
- [ ] No "manual verification only" criteria without justification
- [ ] Regression risk areas identified and have planned test coverage

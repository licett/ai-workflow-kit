---
name: sprint-design-reviewer
description: Deep review of sprint design documents. Auto-detects sprint type (strategy/engineering/hybrid) and assembles the matching expert panel. Use when the user asks to review a sprint.md before starting development, or wants to validate that a sprint plan is ready for execution.
---

# Sprint Design Reviewer

## Goal
Produce an evidence-based design review verdict for a sprint document: Approve / Conditional / Reject.

## Trigger shortcuts
- `/sprint-design-reviewer s22 review`
- `/sprint-design-reviewer sprint22 review`
- `/sprint-design-reviewer s35 --type strategy`
- `review sprint22.md 设计是否合理`
- Map `sprintN` to `docs/sprint/sprintN.md` by default.

## Sprint type parameter

### `--type` (optional, default: `auto`)

| Value | Panel | When to use |
|-------|-------|-------------|
| `strategy` | 量化策略师 + 统计学家 + 风控专家 + 代码评审专家 | PnL optimization, alpha/regime, backtesting, holdout validation, position sizing |
| `engineering` | 架构师 + 代码评审专家 + QA 负责人 | Refactoring, migration, pipeline, API integration, infra |
| `hybrid` | 量化策略师 + 架构师 + 代码评审专家 + 风控专家 | Mixed strategy + engineering (e.g., runtime governance implementing a strategy) |
| `auto` | Auto-detect from sprint content, then use the matching panel | Default when `--type` is omitted |

### Auto-detection rules (when `--type auto` or omitted)

Read the first 300 lines of the sprint document and count keyword hits:

**Strategy signals**: `PnL`, `alpha`, `regime`, `backtest`, `holdout`, `net_edge`, `exitability_tax`, `entry_edge`, `drawdown`, `sharpe`, `kelly`, `position sizing`, `adverse selection`, `carry_penalty`, `concentration_penalty`, `flip_candidate`, `kill`, `shrink`, `challenger`, `wallet_compatible`, `overfitting`, `out_of_sample`

**Engineering signals**: `refactor`, `migration`, `pipeline`, `API`, `schema`, `ingest`, `monitor`, `CI/CD`, `deploy`, `infra`, `latency`, `throughput`, `endpoint`, `database`, `queue`, `worker`, `cache`, `retry`

Decision:
- strategy_hits > 2× engineering_hits → `strategy`
- engineering_hits > 2× strategy_hits → `engineering`
- Otherwise → `hybrid`

---

## Expert roles by sprint type

### Strategy panel (for `--type strategy`)

#### Quant Strategist (量化策略师)
- 职责：PnL 归因正确性、alpha 来源识别、regime 分类方法论、position sizing 合理性
- 审查维度：Axis S1 (策略合理性) + Axis S2 (方法论严谨性)
- 视角：站在量化交易从业者角度，看策略假设是否站得住脚、PnL 分解是否遗漏关键因子、regime 分类是否捕捉真实 alpha

#### Statistician / Data Scientist (统计学家)
- 职责：样本量充分性、假设检验严谨性、过拟合控制、holdout 设计
- 审查维度：Axis S3 (统计严谨性)
- 视角：站在统计学家角度，看结论是否有足够统计功效、是否存在 look-ahead bias / survivorship bias / multiple testing 问题

#### Risk Manager (风控专家)
- 职责：组合风险、尾部风险、rollout 安全性、drawdown 控制、real-money 暴露期管理
- 审查维度：Axis S4 (风险控制)
- 视角：站在风险管理角度，看 worst-case 是否被充分识别、rollout 节奏是否与风险匹配、wallet 保护是否有临时措施

#### Code Review Expert (代码评审专家)
- 职责：验收标准可执行性、代码路径存在性、信息充分性、测试覆盖
- 审查维度：Axis C (验收标准) + Axis D (信息充分性)
- 视角：站在执行者角度看 sprint 文档能否支撑无歧义开发

### Engineering panel (for `--type engineering`)

#### Architect (架构师)
- 职责：架构合理性、技术路线制定、模块边界、性能与风险 tradeoff、是否过度设计
- 审查维度：Axis A (设计合理性) + Axis B (技术路线)
- 视角：站在系统全局看单个 sprint 是否走偏，是否与已有架构冲突，是否引入不必要的复杂度

#### Code Review Expert (代码评审专家)
- 职责：验收标准可执行性、代码路径存在性、信息充分性
- 审查维度：Axis C (验收标准) + Axis D (信息充分性)
- 视角：站在执行者角度看 sprint 文档能否支撑无歧义开发

#### QA Lead (QA 负责人)
- 职责：测试策略可行性、风险评估充分性、验收标准可测性、上线门禁前置判断
- 审查维度：跨 Axis B/C/D 的测试与风险切面
- 视角：站在质量守门人角度看 sprint 的测试计划是否现实、风险是否被充分识别

### Hybrid panel (for `--type hybrid`)

Uses: 量化策略师 + 架构师 + 代码评审专家（含 QA 职责）+ 风控专家

---

## Workflow

### Phase 1: Context loading
- Read `CLAUDE.md` first (coding style, naming, testing, Pack spec).
- Load `docs/sprint/sprintN.md` as primary input.
- Load `docs/task/progress.md` for current state awareness.
- Load `docs/qa/pitfalls.md` recent entries for known landmines.
- If the sprint references prior sprints (carryover, dependencies), skim those docs.
- **Determine sprint type**: if `--type auto` or omitted, apply auto-detection rules above.

### Phase 2: Parallel expert review (N agents based on panel)

Spawn agents in parallel according to the selected panel. Each agent uses its designated checklist.

#### Strategy panel checklists

**Agent 1 — Quant Strategist (量化策略师)**

*Axis S1: Strategy rationality (策略合理性)*
- PnL decomposition covers all material alpha/cost sources (entry edge, exit cost, adverse selection, market impact, funding cost).
- Regime classification captures genuine structural differences, not just noise buckets.
- Threshold choices (bucket edges, coverage floors, capture targets) have empirical or theoretical justification, not arbitrary round numbers.
- Position sizing methodology (haircut fractions, budget caps) is grounded in theory (Kelly, half-Kelly, risk parity, etc.) or at minimum has a stated rationale.
- Challenger / anti-alpha matrix methodology follows proper backtesting discipline (no peeking, consistent universe, same cost assumptions).
- "Regime-first not sport-first" hypothesis is examined honestly — are there structural microstructure differences between sports that regime labels cannot capture?
- The objective function is complete — are there missing penalty terms (e.g., adverse selection cost, market impact, correlation with other positions)?
- Non-goals are genuinely non-goals, not just things the sprint couldn't figure out.

*Axis S2: Methodology rigor (方法论严谨性)*
- Evidence windows are appropriate for the claim being made (7-day window may be too short for regime stability claims).
- Backtesting methodology avoids common pitfalls: look-ahead bias, survivorship bias, transaction cost underestimation.
- "Wallet-compatible" evidence standard is correctly defined and consistently applied.
- Counterfactual analysis (e.g., "what if we had blocked these trades") correctly accounts for second-order effects (market impact, opportunity cost).
- Promotion gates (coverage floors, capture targets) are calibrated against the actual decision they gate, not just round numbers.

**Agent 2 — Statistician (统计学家)**

*Axis S3: Statistical rigor (统计严谨性)*
- Sample sizes are sufficient for the claims made. For N regime cells with K conditions total, average cell size K/N must support reliable estimation (rule of thumb: >= 30 per cell for means, >= 100 for tail statistics).
- Multiple testing: if comparing N regimes × M challengers, has family-wise error rate been considered? Are thresholds adjusted?
- Holdout design: is the holdout window truly independent? Is it long enough to capture regime transitions? Is the minimum sample size (200 conditions, 50 events, 7 days) statistically justified for the decisions it will gate?
- Overfitting risk: number of free parameters (regime bucket edges, threshold values) vs. number of observations. If parameters > observations/10, overfitting is likely.
- Stationarity assumption: are regime definitions stable over time, or could the optimal bucket edges shift?
- Effect size vs. statistical significance: are the reported PnL improvements large enough to be practically meaningful given estimation uncertainty?
- Confidence intervals or uncertainty quantification: are point estimates accompanied by any measure of precision?
- Selection bias: does focusing on "top 20 worst events" for governance design create an anchor bias?

**Agent 3 — Risk Manager (风控专家)**

*Axis S4: Risk control (风险控制)*
- Worst-case scenario analysis: what happens if ALL governance assumptions are wrong simultaneously?
- Wallet exposure during holdout/development period: is there an interim protection mechanism?
- Canary/rollout blast radius: is 10% daily buy_notional the right initial exposure? Is there a kill switch?
- Drawdown circuit breaker: is there a maximum acceptable loss during the sprint execution period?
- Correlation risk: are regime classifications independent, or could multiple "safe" regimes fail simultaneously?
- Model risk: what if the regime classification itself is the problem (e.g., wrong features, wrong bucket edges)?
- Operational risk: rollback procedure, time-to-rollback, data integrity during mode transitions.
- Tail risk: are there scenarios where governance makes things worse (e.g., blocking good trades while missing bad ones)?

**Agent 4 — Code Review Expert (代码评审专家)**

Uses the same Axis C + D checklist as the engineering panel (see below).

#### Engineering panel checklists

**Agent 1 — Architect (架构师)** — 完整角色定义见 `~/.claude/agents/architect.md`

*Axis A: Design rationality (设计合理性)*
- Problem statement is clear with quantifiable before/after.
- Scope is bounded (file count, LOC estimate, module boundary).
- Non-goals are explicit — no hidden scope creep.
- Dependencies between Packs have correct ordering.
- Risk/rollback strategy exists for each Pack.
- Sprint does not duplicate work from prior sprints (check carryover history).
- Performance vs complexity tradeoff is **explicit and justified with trade-off analysis** (选了什么/放弃了什么/代价是什么).
- Module boundary changes don't violate existing separation of concerns.
- **Reversibility check**: 不可逆决策是否有充分验证支撑？可逆替代方案是否被考虑过？

*Axis B: Technical route vs best practices (技术路线)*
- Proposed approach aligns with existing architecture (check module map).
- No reinvention of patterns already solved in the codebase.
- Concurrency/async/network patterns follow established project conventions.
- API usage matches documented contracts.
- Performance claims have measurable baselines and targets.
- **Anti-astronaut YAGNI check**: 每个抽象层/泛化/配置化是否有至少两个消费方？如果只有一个 → 过度设计.
- Industry best practices are followed (cite specific patterns when relevant).
- Risk mitigation strategy is proportional to impact (not under/over-engineered).
- **Complexity justification**: 新引入的 pattern 是否匹配问题规模？最坏情况不引入会怎样？

**Agent 2 — Code Review Expert (代码评审专家)**

*Axis C: Acceptance criteria clarity (验收标准)*
- Every Pack has a DoD with pass/fail conditions (not vague "improve X").
- Test commands are specified (`pytest tests/...::case`).
- Artifact paths are listed (`data/...`, `var/reports/...`).
- Metrics have concrete thresholds (e.g., "p95 < 200ms", not "faster").
- Evidence format is defined (log grep, report JSON field, test assertion).
- Rollback criteria defined (when to revert).

*Axis D: Information sufficiency (信息充分性)*
- Enough context for a fresh agent to execute without asking clarifying questions.
- File paths to modify are listed per Pack.
- Input/output data schemas are specified where relevant.
- Environment/config prerequisites are documented.
- Edge cases and known pitfalls from `pitfalls.md` are addressed.
- Referenced code paths actually exist (`Glob`/`Grep` validation).
- Test file targets exist or are explicitly marked as "to create".

**Agent 3 — QA Lead (QA 负责人)**

*Cross-Axis E: Test strategy + risk assessment*
- Test strategy feasibility (realistic given pytest, no CI).
- Integration tests planned where unit tests insufficient.
- Test dependencies accounted for.
- Blast radius per Pack assessed.
- Failure modes and degradation paths documented.
- Rollback complexity assessed.
- Each DoD criterion maps to a concrete test.
- Negative tests defined where needed.

Each agent produces findings in standard `[Px][confidence]` format with `file:line` or `docs/sprint/sprintN.md:section` evidence.

### Phase 3: Cross-examination (adversarial cross-review)

After all agents complete, run **mutual cross-review**. The cross-review structure adapts to the panel:

#### Strategy panel cross-review

**Step 1: Quant Strategist + Statistician review Risk Manager + Code Expert findings**
For each finding, evaluate:
- Is the risk concern backed by quantitative evidence, or is it theoretical?
- Is the code-level gap relevant to strategy correctness, or only to engineering quality?
Output: `Agree` / `Dispute (evidence)` per finding.

**Step 2: Risk Manager + Code Expert review Quant Strategist + Statistician findings**
For each finding, evaluate:
- Is the strategy concern testable/actionable, or academic?
- Is the statistical concern relevant given the project's current data scale?
- Would fixing this finding materially change the sprint outcome?
Output: `Agree` / `Dispute (evidence)` per finding.

**Step 3: Consolidation and classification**
Same as engineering panel (see below).

#### Engineering panel cross-review

**Step 1: Architect reviews Code Review Expert + QA Lead findings**
- Is the claimed acceptance/test gap real, or does the sprint design already address it implicitly?
- Is the "missing info" actually derivable from architecture context?
- Is the suggested fix practical given system constraints?
Output: `Agree` / `Dispute (reason)` per finding.

**Step 2: Code Review Expert reviews Architect + QA Lead findings**
- Is the claimed architecture flaw backed by concrete code evidence?
- Is the QA risk concern backed by actual code/test gaps?
Output: `Agree` / `Dispute (reason)` per finding.

**Step 3: QA Lead reviews Architect + Code Review Expert findings**
- If adopted, what test changes would this require?
- Does this finding expose a risk that the test strategy doesn't cover?
- Is the severity calibrated correctly?
Output: `Agree` / `Dispute (reason)` / `Escalate to ship-risk` per finding.

**Step 4: Consolidation and classification** (all panel types)
- `Confirmed`: 2+ experts agree, or 1 expert agrees with verified source evidence and no expert disputes.
- `Likely valid`: Mixed agreement, or cannot disprove with evidence.
- `Disputed`: 2+ experts provide concrete counter-evidence. Demote or discard.

Additional consolidation checks:
1. **Source code verification**: For every finding citing a code path, verify the path actually exists and the claim is valid.
2. **False positive filter**: Remove findings that misunderstand project conventions (check CLAUDE.md).
3. **Sprint history dedup**: Remove findings that repeat issues already tracked in prior sprints or pitfalls.md.
4. **Severity calibration**: Ensure P0/P1 findings are truly blocking, not inflated.

Flag any Pack that exceeds the ≤1 day / ≤2 PR guideline from CLAUDE.md.

### Phase 4: Output

#### Verdict
- `Approve`: All axes pass. Ready to execute.
- `Conditional`: No blocking issues, but 1+ axes need minor fixes before execution.
- `Reject`: Blocking design flaws that would cause wasted effort if executed.

#### Report format

**Strategy panel report** uses these axes:
```
| 维度 | 评分 | 关键发现 |
|------|------|----------|
| S1 策略合理性 | ✅/⚠️/❌ | ... |
| S2 方法论严谨性 | ✅/⚠️/❌ | ... |
| S3 统计严谨性 | ✅/⚠️/❌ | ... |
| S4 风险控制 | ✅/⚠️/❌ | ... |
| C 验收标准 | ✅/⚠️/❌ | ... |
| D 信息充分性 | ✅/⚠️/❌ | ... |
```

**Engineering panel report** uses these axes:
```
| 维度 | 评分 | 关键发现 |
|------|------|----------|
| A 设计合理性 | ✅/⚠️/❌ | ... |
| B 技术路线 | ✅/⚠️/❌ | ... |
| C 验收标准 | ✅/⚠️/❌ | ... |
| D 信息充分性 | ✅/⚠️/❌ | ... |
```

Full report structure (same for all panel types):
```text
Sprint 设计评审: sprintN
Sprint type: [strategy / engineering / hybrid]
Expert panel: [list of experts used]

## 评审结论: [Approve / Conditional / Reject]

## 专家评审摘要
| 专家 | 负责维度 | 结论 | 关键发现数 |
|------|----------|------|-----------|
| ... | ... | ✅/⚠️/❌ | N |

## 维度评分
(axes table per panel type above)

## Confirmed Findings（交叉复核后确认）
- [P1][0.xx][角色] ...
  证据: file:line 或 docs/sprint/sprintN.md:section
  影响: ...
  建议: ...

## Disputed（交叉复核后驳回）
- [原Px→驳回][角色] ...
  驳回原因: ...

## 必须修复项（Conditional/Reject 时）
1. ...

## 亮点
- ...

## 执行前建议
- ...

## 质量统计
| 指标 | 数值 |
|------|------|
| 原始 findings 总数 | N |
| 交叉复核后 Confirmed | N |
| 驳回 (false positive) | N |
| 驳回率 | N% |
```

## Safety rails
- This is a read-only review skill. Do not modify sprint docs.
- Verify claims against source code — do not trust doc status at face value.
- Flag uncertainty explicitly rather than guessing.
- Keep review scoped to the sprint document; avoid tangential architecture advice.
- Cross-examination must resolve disagreements transparently, not silently pick a side.
- **Strategy panel safety**: Quant Strategist must not dismiss engineering concerns as "implementation detail"; Code Expert must not dismiss strategy concerns as "not my domain." Both domains matter.
- **Risk Manager has veto power** on rollout safety — if Risk Manager says the wallet exposure is unacceptable, it must be addressed regardless of strategy attractiveness.

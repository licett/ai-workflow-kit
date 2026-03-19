---
name: cross-review-gate
description: Multi-expert cross-validated code review with quality gate. Spawns parallel review agents, cross-checks findings to filter false positives and impractical suggestions, then produces a final consolidated report. Use when the user wants a high-confidence, production-grade code review after completing fixes or before merging.
---

# Cross Review Gate

## Goal
Deliver a cross-validated, high-confidence code review by running multiple independent review passes, then filtering findings through adversarial cross-examination to eliminate false positives, impractical suggestions, and phantom issues.

## Trigger shortcuts
- `/cross-review-gate`
- `/cross-review-gate s25`
- `调用多个代码评审专家交叉复核`
- `全量深度 codereview + 交叉复核`
- When sprint context is given, map `sN` to `docs/sprint/sprintN.md` for scope.

## Workflow

### Phase 1: Scope determination
- Run `git status` and `git diff` to identify changed files.
- If sprint context is provided, load `docs/sprint/sprintN.md` for Pack scope and DoD.
- Load `CLAUDE.md` for project constraints.
- Load `docs/qa/pitfalls.md` recent entries for regression awareness.

### Phase 2: Parallel independent review (4 agents)
Spawn 4 agents in parallel, each with a distinct role and focus lens:

**Agent 1 — Correctness & Regression (代码评审专家-正确性)**
Focus: logic bugs, regressions against sprint DoD, edge cases, data flow integrity.
Checklist: behavioral change is intentional, error paths are reachable, state transitions are complete.

**Agent 2 — Security & Reliability (代码评审专家-安全性)**
Focus: input validation, error handling, concurrency safety, resource leaks, API contract compliance.
Checklist: trust boundary enforcement, secret exposure, retry amplification, unsafe deserialization.

**Agent 3 — Performance & Maintainability (代码评审专家-性能)**
Focus: algorithmic complexity, latency impact, code clarity, observability.
Checklist: N+1 patterns, unbounded loops, cache strategy, metric/log coverage.

**Agent 4 — QA Lead (QA 负责人)**
Focus: test design quality, test coverage completeness, risk assessment, and release readiness.
Checklist:
- *Test design*: Are test cases covering happy path, edge cases, error paths, and boundary conditions? Are test names descriptive and assertions specific (not just `assert result`)?
- *Coverage gaps*: Are new/changed code paths covered by tests? Are regression tests present for bug fixes? Are integration-level tests present where unit tests alone are insufficient?
- *Test anti-patterns*: Flaky tests (time-dependent, order-dependent), mocked-away core logic, tests that pass vacuously (assert True), overly broad fixtures.
- *Risk assessment*: What is the blast radius of this change? What failure modes exist post-deploy? Are there monitoring/alerting gaps for the changed paths?
- *Rollback readiness*: Can this change be safely reverted without data migration? Are feature flags or safe deployment guards in place for high-risk changes?
- *Release verdict*: Based on all evidence, is this change safe to ship? Flag any "ship blocker" explicitly.

Agents 1-3 use the `code-review-expert` skill conventions. Agent 4 (QA Lead) produces findings in the same `[Px][confidence]` format but additionally outputs a **Release Readiness** section.

### Phase 3: Cross-examination (adversarial mutual review)
After all 4 agents complete, run adversarial cross-review in 2 steps:

**Step 1: Grouped mutual cross-review**

Group agents into two camps and run cross-review between them:

*Code Experts (Agents 1-3) review QA Lead's findings:*
Spawn an agent with the combined code-expert perspective. Input: all findings from QA Lead (Agent 4).
For each QA finding, evaluate:
- Is the claimed test gap real? Check whether the test already exists or the scenario is covered implicitly.
- Is the risk assessment proportional, or is it inflated?
- Is the suggested test addition practical and non-redundant?
Output: `Agree` / `Dispute (evidence)` per finding.

*QA Lead reviews Code Experts' findings:*
Spawn an agent with the QA Lead perspective. Input: all findings from Agents 1-3.
For each code finding, evaluate:
- Is this issue testable? If so, why didn't existing tests catch it?
- Is the blast radius correctly assessed?
- Does the fix introduce new risk that needs test coverage?
- Is this a ship-blocker or can it be deferred?
Output: `Agree` / `Dispute (evidence)` / `Ship-blocker` per finding.

**Step 2: Consolidation and classification**
After cross-reviews complete, classify each finding:

For each finding, verify:
1. **Source code evidence**: Does the cited `file:line` actually contain the claimed issue? Read the code.
2. **Reproducibility**: Can the issue be triggered in realistic conditions, or is it purely theoretical?
3. **Practicality**: Is the suggested fix achievable within project constraints and conventions?
4. **Duplication**: Is this finding already covered by another finding at higher severity?
5. **False positive check**: Does the reviewer misunderstand project-specific patterns (e.g., conventions documented in CLAUDE.md)?

Classification:
- `Confirmed`: 2+ agents independently flagged, or cross-reviewer Agrees with source evidence. QA Lead ship-blocker findings auto-promote to Confirmed.
- `Likely valid`: 1 agent flagged, cross-reviewer partially agrees, impact uncertain.
- `Disputed`: Cross-reviewer provides concrete counter-evidence. Demote or discard.
- `Impractical`: Valid observation but fix cost exceeds benefit. Note for future consideration.

### Phase 4: Final consolidated report

```text
交叉复核代码评审报告

## 评审范围
- 变更文件: N files
- Sprint 上下文: sprintN (if applicable)
- 评审专家: 4 agents (correctness, security, performance, QA lead)

## 复核结论: [Pass / Conditional Pass / Fail]
- Pass: 无 Confirmed P0/P1，QA Lead 判定可上线
- Conditional Pass: 有 P1 但可在后续迭代修复，QA Lead 无 ship-blocker
- Fail: 存在 P0 或多个 Confirmed P1，或 QA Lead 判定不可上线

## 专家视角摘要
| 专家 | 焦点 | 发现数 | 最高严重度 |
|------|------|--------|-----------|
| 正确性专家 | 逻辑/回归/边界 | N | Px |
| 安全性专家 | 验证/并发/泄露 | N | Px |
| 性能专家 | 复杂度/延迟/可观测 | N | Px |
| QA 负责人 | 测试设计/风险/上线 | N | Px |

## Confirmed Findings（已确认，必须处理）
- [P1][0.92][2/4 agents] 标题 — file:line
  影响: ...
  建议: ...
  复核依据: Agent1 + Agent3 独立发现，源码验证通过

## Likely Valid（建议处理）
- [P2][0.78][1/4 agents] 标题 — file:line
  影响: ...
  复核依据: 源码证据存在，影响待运行时确认

## Disputed（已驳回）
- [原P1→驳回] 标题 — file:line
  驳回原因: 与项目约定一致 / 源码不支持该结论 / 纯理论风险

## Impractical（记录备查）
- 标题: ...
  原因: 修复成本超出收益，可作为技术债记录

## QA 评审: 测试设计质量
- 测试覆盖率评估: ...
- 缺失的测试场景: ...
- 测试反模式: ...
- 回归测试充分性: ...

## QA 评审: Release Readiness（上线就绪判定）
- 上线判定: [Ready / Conditional / Block]
- 爆炸半径: ...
- 失败模式与监控: ...
- 回滚可行性: ...
- Ship-blockers (if any): ...

## 质量统计
| 指标 | 数值 |
|------|------|
| 原始 findings 总数 | N |
| 交叉复核后 Confirmed | N |
| 驳回 (false positive) | N |
| 驳回率 | N% |

## 后续建议
- 测试命令: ...
- 风险监控: ...
- QA 补充测试: ...
```

## Quality gate rules
- `Pass`: Ship immediately. No Confirmed P0 or P1.
- `Conditional Pass`: Ship with tracked follow-up. Confirmed P1 items logged to next sprint or pitfalls.md.
- `Fail`: Do not ship. Fix Confirmed P0/P1 items and re-run this skill.

## Safety rails
- Every Confirmed finding must have verified `file:line` evidence — no phantom issues.
- Do not inflate severity to appear thorough. Accuracy over quantity.
- Do not suppress findings to appear positive. Honesty over optimism.
- Cross-examination must actually read source code, not just compare finding titles.
- If agents disagree, present both perspectives rather than silently picking one.
- Keep scope to the review target; avoid unrelated architecture commentary.

## Integration with existing skills
- Agents 1-3 internally invoke `code-review-expert` skill conventions.
- Agent 4 (QA Lead) uses the same finding format but adds release readiness assessment.
- Findings format is compatible with `sprint-close-auditor` for direct consumption.
- QA Lead's release verdict feeds directly into the quality gate decision.
- Confirmed P0/P1 items should be tracked in `docs/qa/pitfalls.md` per CLAUDE.md rules.
- QA Lead's missing test scenarios can feed into `tdd-loop-executor` for next iteration.

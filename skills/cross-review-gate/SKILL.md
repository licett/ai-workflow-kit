---
name: cross-review-gate
description: Multi-expert cross-validated code review with quality gate. Spawns 5 parallel review agents (architect + correctness + security + performance + QA), cross-checks findings to filter false positives, then produces a final consolidated report. Use when the user wants a high-confidence, production-grade code review after completing fixes or before merging.
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

### Phase 2: Parallel independent review (5 agents)
Spawn 5 agents in parallel. Each agent has an independent, precisely defined role (see `~/.claude/agents/` for full definitions):

| Agent | 角色 | 定义文件 | 职责 |
|-------|------|---------|------|
| Agent 1 | 架构师 | `architect.md` | 模块边界、依赖方向、设计决策 trade-off、YAGNI、可逆性 |
| Agent 2 | 正确性专家 | `reviewer-correctness.md` | 逻辑 bug、回归、状态机完整性、边界、数据流 |
| Agent 3 | 安全性专家 | `reviewer-security.md` | STRIDE 威胁面、输入验证、依赖链、密码学、资源管理 |
| Agent 4 | 性能专家 | `reviewer-performance.md` | 算法复杂度、N+1/I-O 模式、数据结构适配、可观测性 |
| Agent 5 | QA 负责人 | `reviewer-qa-lead.md` | 测试设计、覆盖率、风险评估、回滚就绪、上线判定 |

Spawn 方式：使用 Agent tool，`subagent_type` 指定对应 agent 名称，prompt 中传入变更 diff、sprint 上下文和 pitfalls 信息。

所有 5 个 agent 使用统一的 `[Px][confidence]` finding 格式（定义见 `code-review-expert.md`）。
- Agent 1（架构师）额外关注 trade-off 显式化和 YAGNI 违反
- Agent 5（QA Lead）额外输出 **Release Readiness** 判定，且拥有**否决权**

### Phase 3: Cross-examination (adversarial mutual review)
After all 5 agents complete, run adversarial cross-review in 3 steps:

**Step 1: Architect reviews all other agents' findings**
Spawn an agent with the architect perspective. Input: all findings from Agents 2-5.
For each finding, evaluate:
- Is the proposed fix compatible with existing architecture, or would it introduce unnecessary coupling/complexity?
- Does the fix violate YAGNI — is it solving a real problem or a hypothetical one?
- Are multiple findings pointing to the same root cause? If so, consolidate.
Output: `Agree` / `Dispute (evidence)` / `Consolidate with Fx` per finding.

**Step 2: Code Experts (Agents 2-4) review QA Lead's findings**
Spawn an agent with the combined code-expert perspective. Input: all findings from QA Lead (Agent 5).
For each QA finding, evaluate:
- Is the claimed test gap real? Check whether the test already exists or the scenario is covered implicitly.
- Is the risk assessment proportional, or is it inflated?
- Is the suggested test addition practical and non-redundant?
Output: `Agree` / `Dispute (evidence)` per finding.

**Step 3: QA Lead reviews Code Experts' + Architect's findings**
Spawn an agent with the QA Lead perspective. Input: all findings from Agents 1-4.
For each finding, evaluate:
- Is this issue testable? If so, why didn't existing tests catch it?
- Is the blast radius correctly assessed?
- Does the fix introduce new risk that needs test coverage?
- Is this a ship-blocker or can it be deferred?
Output: `Agree` / `Dispute (evidence)` / `Ship-blocker` per finding.

**Step 4: Consolidation and classification**
After cross-reviews complete, classify each finding:

For each finding, verify:
1. **Source code evidence**: Does the cited `file:line` actually contain the claimed issue? Read the code.
2. **Reproducibility**: Can the issue be triggered in realistic conditions, or is it purely theoretical?
3. **Practicality**: Is the suggested fix achievable within project constraints and conventions?
4. **Duplication**: Is this finding already covered by another finding at higher severity? Did the architect consolidate it?
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
- 评审专家: 5 agents (architect, correctness, security, performance, QA lead)

## 复核结论: [Pass / Conditional Pass / Fail]
- Pass: 无 Confirmed P0/P1，QA Lead 判定可上线
- Conditional Pass: 有 P1 但可在后续迭代修复，QA Lead 无 ship-blocker
- Fail: 存在 P0 或多个 Confirmed P1，或 QA Lead 判定不可上线

## 专家视角摘要
| 专家 | 焦点 | 发现数 | 最高严重度 |
|------|------|--------|-----------|
| 架构师 | 模块边界/设计决策/YAGNI | N | Px |
| 正确性专家 | 逻辑/回归/状态机/边界 | N | Px |
| 安全性专家 | STRIDE/验证/依赖链/密码学 | N | Px |
| 性能专家 | 复杂度/N+1/数据结构/I-O | N | Px |
| QA 负责人 | 测试设计/风险/上线判定 | N | Px |

## Confirmed Findings（已确认，必须处理）
- [P1][0.92][3/5 agents] 标题 — file:line
  影响: ...
  建议: ...
  复核依据: Agent2 + Agent4 独立发现，Architect 确认非过度设计

## Likely Valid（建议处理）
- [P2][0.78][1/5 agents] 标题 — file:line
  影响: ...
  复核依据: 源码证据存在，影响待运行时确认

## Disputed（已驳回）
- [原P1→驳回] 标题 — file:line
  驳回原因: 与项目约定一致 / 源码不支持该结论 / 纯理论风险

## Impractical（记录备查）
- 标题: ...
  原因: 修复成本超出收益，可作为技术债记录

## 架构评审: 设计决策质量
- 模块边界评估: ...
- 依赖方向: ...
- Trade-off 识别: ...
- YAGNI 违反: [有/无]

## QA 评审: 测试设计质量
- 测试覆盖率评估: ...
- 缺失的测试场景: ...
- 测试反模式: ...
- 回归测试充分性: ...

## QA 评审: Release Readiness（上线就绪判定）
- 上线判定: [Ready / Conditional / Block]
- 证据摘要: ...
- 爆炸半径: ...
- 失败模式与监控: ...
- 回滚可行性: ...
- Ship-blockers (if any): ...

## 质量统计
| 指标 | 数值 |
|------|------|
| 原始 findings 总数 | N |
| 交叉复核后 Confirmed | N |
| 架构师合并 (consolidated) | N |
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
- Architect's consolidation must preserve the highest severity among merged findings.
- Keep scope to the review target; avoid unrelated architecture commentary.

## Integration with existing skills
- All 5 agents follow the `[Px][confidence]` format defined in `code-review-expert.md`.
- Agent 5 (QA Lead) has veto power — Block verdict overrides all other signals.
- Agent 1 (Architect) serves as consolidator in Phase 3, merging duplicate root causes.
- Findings format is compatible with `sprint-close-auditor` for direct consumption.
- Confirmed P0/P1 items should be tracked in `docs/qa/pitfalls.md` per CLAUDE.md rules.
- QA Lead's missing test scenarios can feed into `tdd-loop-executor` for next iteration.

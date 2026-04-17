---
name: adversarial-cross-model-review
description: Adversarial verification of external model review findings against source code. Use when the user pastes review conclusions from another model (GPT, Gemini, etc.) and asks to verify, challenge, or decide whether to adopt them. Verifies each finding by reading actual source code, not by reasoning about it.
---

# Adversarial Cross-Model Review

## Goal
Take review findings from an external model, verify every claim against actual source code, and produce an evidence-based adopt/reject decision per finding. Prevent both blind adoption and blind dismissal.

## Trigger shortcuts
- `/adversarial-cross-model-review`
- `gpt 的意见如下 ... 请逐条 check`
- `gpt 有不同的意见 ...`
- `外部 review 结果 ... 是否采纳`
- Any message that pastes another model's review findings and asks for verification.

## Core principle
**Every verdict must cite source code, not reasoning.** If a finding claims `file.py:123` has a bug, read that line. If a finding claims a pattern is wrong, find the pattern in code. Never agree or disagree based on plausibility alone.

## Workflow

### Phase 1: Parse and normalize external findings
- Extract each distinct finding from the pasted content.
- Normalize into a structured list:
  - ID (sequential: F1, F2, ...)
  - Severity (as claimed by external model)
  - Claim (one sentence: what the external model says is wrong)
  - Cited evidence (file:line, config, doc section — as cited by external model)
  - Suggested fix (as proposed by external model)

### Phase 2: Parallel multi-expert verification (3 agents)
Each external finding is independently verified by 3 experts with different lenses. All findings are sent to all 3 agents simultaneously.

**Agent 1 — Architect (架构师)** — 完整角色定义见 `~/.claude/agents/architect.md`
For each finding, verify from system-level perspective:
- Is the claimed architectural/design flaw real? Read the module map and data flow.
- Is the proposed fix compatible with existing architecture, or would it introduce coupling/complexity?
- **Trade-off check**: Does the proposed fix introduce new trade-offs? Are they acceptable?
- Is the performance/tradeoff concern backed by measurable evidence?
- Would the fix require changes beyond the claimed scope?
- **YAGNI check**: Is the proposed change solving a real problem or a hypothetical one?

**Agent 2 — Code Review Expert (代码评审专家)**
For each finding, verify from code-level perspective:
- Read the cited `file:line` — does the code actually behave as the external model claims?
- Does `CLAUDE.md`, existing tests, or project conventions explain the flagged pattern?
- Is the proposed fix correct and minimal, or would it introduce new issues?
- Is this finding in scope for the current sprint/change?

**Agent 3 — QA Lead (QA 负责人)**
For each finding, verify from quality/risk perspective:
- If the claimed bug is real, is there a test that should have caught it? Is that test missing?
- Is the proposed fix testable? What test cases would verify it?
- What is the blast radius if this finding is real and unfixed?
- Is this a regression risk or a net-new risk?

Each agent MUST **read the cited source code** for every finding. Output per finding: `Agree` / `Partially agree (reason)` / `Disagree (evidence)` / `Cannot verify (needs runtime)`.

### Phase 3: Cross-examination (adversarial reconciliation)
After all 3 agents complete, run cross-examination in 2 steps:

**Step 1: Mutual cross-review**
Each expert reviews the other two experts' verdicts for their area of expertise:
- Architect challenges Code Review Expert and QA Lead on architecture-related verdicts.
- Code Review Expert challenges Architect and QA Lead on source-code-level verdicts.
- QA Lead challenges Architect and Code Review Expert on test/risk-related verdicts.

For each disagreement, the challenger must provide counter-evidence from source code.

**Step 2: Consolidation and classification**
After cross-review, classify each finding based on expert consensus:

- **Adopt** — 2+ experts Agree, or 1 expert Agrees with verified source evidence and no expert Disagrees.
  - Evidence: cite the exact code that confirms the issue.
- **Partial adopt** — Experts agree the direction is correct but diagnosis or fix needs adjustment.
  - Evidence: cite what's correct and what needs modification.
  - Provide: corrected diagnosis and/or alternative fix.
- **Reject** — 2+ experts Disagree with source evidence, or cross-review disproved the claim.
  - Evidence: cite the code or convention that disproves the claim.
  - Reason category: `source_contradicts` / `convention_misread` / `out_of_scope` / `already_handled` / `theoretical_only`
- **Defer** — Experts cannot verify without runtime evidence (e.g., timing, load, external API behavior).
  - Provide: specific verification steps (command, log grep, test to write).

### Phase 4: Output

```text
外部模型评审交叉复核报告

## 来源
- 外部模型: [GPT/Gemini/etc.]
- 原始 findings 数量: N
- 复核范围: [sprint context / changed files / full repo]
- 复核专家: 3 agents (架构师, 代码评审专家, QA 负责人)

## 复核结论
| 分类 | 数量 | 占比 |
|------|------|------|
| Adopt (采纳) | N | N% |
| Partial adopt (部分采纳) | N | N% |
| Reject (驳回) | N | N% |
| Defer (待验证) | N | N% |

## 逐条复核

### F1: [外部模型的 finding 标题]
- 外部模型声称: ...
- 外部模型严重度: Px
- **复核结论: [Adopt / Partial adopt / Reject / Defer]**
- 专家判定:
  | 专家 | 判定 | 关键证据 |
  |------|------|----------|
  | 架构师 | Agree/Disagree | ... |
  | 代码评审专家 | Agree/Disagree | ... |
  | QA 负责人 | Agree/Disagree | ... |
- 交叉复核: [是否有专家间分歧，如何仲裁]
- 源码证据: `file.py:123` — [实际代码行为描述]
- 动作: [采纳原 fix / 修正后采纳 / 无需动作 / 手动验证]

### F2: ...
(repeat for each finding)

## 采纳清单（可直接执行）
1. [F1] ...
2. [F5] ...

## 驳回清单（附理由）
1. [F2] 驳回原因: ...
2. [F3] 驳回原因: ...

## 待验证清单
1. [F4] 验证方式: ...

## 质量统计
| 指标 | 数值 |
|------|------|
| 原始 findings 总数 | N |
| 三专家一致同意 | N |
| 三专家一致驳回 | N |
| 存在分歧(经仲裁) | N |
| 驳回率 | N% |

## 风险提示
- 外部模型可能缺少的项目上下文: ...
- 复核中发现的外部模型未提及的问题: ...
```

## Safety rails
- **必须读源码**: 严禁仅凭推理同意或否定外部 finding。每个 verdict 必须有 `file:line` 证据。
- **不卑不亢**: 不因为外部模型是 GPT/Gemini 就倾向采纳，也不因为"我们的代码"就倾向驳回。
- **保持独立判断**: 如果验证过程中发现外部模型未提及的新问题，在"风险提示"中如实报告。
- **scope 意识**: 区分"对当前变更有效的 finding"和"对历史代码的 finding"。后者标记为 out_of_scope 但不否定其价值。
- **不扩大战线**: 复核范围严格限定在外部模型提出的 findings，不主动发起新的 full review。
- **尊重项目约定**: 先读 `CLAUDE.md` 和 `docs/qa/pitfalls.md`，避免因不了解项目约定而误判。

## Reverse-Hypothesis Verification Overlay

### Pre-check
- Classify target as `T1/T2/T3` before verification。
- Any external review affecting runtime, deploy, core files, or merge decision is automatically `T3`。
- Read `AGENTS.md`、`docs/qa/pitfalls.md`、current sprint scope before verifying findings。

### For each external finding, verify both the claim and the strongest alternative
- claimed bug / risk is real
- project convention was misread
- cited file / line is stale or superseded
- issue exists but root cause is different
- existing test already covers it
- finding is valid historically but out of scope for this change

No finding may be `Adopt`ed unless：
1. source evidence supports it, and
2. a reverse-hypothesis attempt failed to falsify it。

### Evidence discipline
- `looks plausible` is not evidence
- `external model cited line numbers` is not verification
- `this is how we usually code` is not a rejection reason without contract or source evidence
- runtime-only questions must be `Defer`, not `Adopt by plausibility`
- if rejecting as `out_of_scope`, still state whether the claim appears valid elsewhere

### Output additions
- Per finding add：`Task tier` / `Evidence class` (`source_confirmed` / `source_contradicted` / `needs_runtime` / `doc_contract`) / `Reverse-hypothesis result` / `Adoption precondition` / `Same-root-cause siblings`

## Integration with existing skills
- 如果 Adopt 的 findings 需要修复，修复后可用 `/cross-review-gate` 做最终验收。
- 如果 Adopt 的 findings 涉及 bug，修复后需在 `docs/qa/pitfalls.md` 补复盘条目。
- Defer 类 findings 可转交 `/log-rootcause-triage` 做运行时验证。

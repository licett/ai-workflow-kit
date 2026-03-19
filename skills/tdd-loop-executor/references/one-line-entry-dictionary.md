# One-Line Entry Dictionary

Use this dictionary for ultra-short, repeatable command-style prompts.

## Core entries
- `"/tdd-loop-executor sN go"`: execute Sprint N with Ask-to-Code loop, strict TDD, and progress sync.
- `"/log-rootcause-triage sN triage <abs_log_path>"`: analyze a log under Sprint N context and return root cause plus minimal fix plan.
- `"/sprint-close-auditor sN close"`: run sprint closeout audit and report `Complete/Partial/Blocked`.
- `"/sprint-design-reviewer sN review"`: four-axis design review of sprint doc and report `Approve/Conditional/Reject`.
- `"/cross-review-gate"` or `"/cross-review-gate sN"`: multi-expert cross-validated code review with quality gate `Pass/Conditional Pass/Fail`.
- `"/adversarial-cross-model-review"`: verify external model findings against source code, classify `Adopt/Partial/Reject/Defer`.
- `"/cc-codex-pair sN"`: CC-Codex 结对 sprint 周期 (设计→实现→审查→修复→关闭).
- `"/cc-codex-pair sN design"`: Phase 1 — sprint 设计协作 with Codex.
- `"/cc-codex-pair sN implement pK"`: Phase 2 — 让 Codex 实现 Pack K.
- `"/cc-codex-pair sN review"`: Phase 3-4 — 交叉复核 + Codex 终审 + 修复.
- `"/cc-codex-pair sN close"`: Phase 5 — Codex 最终 GO/NO-GO.

## Fast follow-ups
- `"/tdd-loop-executor /loop.next"`: continue from `docs/task/progress.md` next action.
- `"/tdd-loop-executor /loop.fix <issue>"`: run root-cause repair with test-first verification.
- `"/sprint-close-auditor sN close --recheck"`: rerun closeout after recent fixes.
- `"/cross-review-gate --recheck"`: re-run cross-review after fixes (picks up new diff).
- `"/cc-codex-pair sN implement pK --feedback"`: 向 Codex 发送实现反馈.
- `"/cc-codex-pair sN review --recheck"`: 修复后重新交叉复核.
- `"/cc-codex-pair status"`: 查看当前 acpx session 状态.

## Recommended calling pattern
Always include the skill name to avoid ambiguity:
- Preferred: `"/tdd-loop-executor s5 go"`
- Risky shorthand: `"s5 go"` (may be interpreted as plain text in some contexts)

## Sample commands
```text
/tdd-loop-executor s5 go
/tdd-loop-executor /loop.next
/log-rootcause-triage s5 triage /Users/pig/project/arbitrage_betting/polyinit/var/logs/runtime.log
/log-rootcause-triage triage /Users/pig/project/betclient/logs/app-2025-11-24.log
/sprint-close-auditor s5 close
/sprint-design-reviewer s26 review
/cross-review-gate s25
/cross-review-gate --recheck
/adversarial-cross-model-review
/cc-codex-pair s42
/cc-codex-pair s42 design
/cc-codex-pair s42 implement p1
/cc-codex-pair s42 review
/cc-codex-pair s42 close
/cc-codex-pair status
```

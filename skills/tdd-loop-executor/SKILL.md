---
name: tdd-loop-executor
description: Execute an iterative Ask-to-Code workflow with strict TDD and completion loops. Use when the user asks to keep going until all scoped tasks are finished, fix failures by root cause, run tests continuously, and keep sprint/progress docs in sync.
---

# TDD Loop Executor

## Goal
Drive a predictable plan-and-deliver loop from open tasks to verified completion without scope drift.

## Trigger shortcuts and sprint mapping
- If the user provides sprint shorthand, resolve it before planning:
  - `s5 go`, `sprint5 go`, `执行 sprint5`, `run sprint5`
  - Treat all of the above as the same intent: execute the full Sprint 5 loop with this skill.
- Default sprint doc mapping:
  - `sprintN` -> `docs/sprint/sprintN.md`
  - progress cursor -> `docs/task/progress.md`
- If `CLAUDE.md` states sprint docs live under `docs/sprint`, trust that mapping without asking.
- Ask a follow-up question only when the mapped sprint file is missing or multiple project roots are ambiguous.

## Workflow

### 1) Ask phase first (plan draft)
- Read `CLAUDE.md`, mapped `docs/sprint/sprintN.md`, and `docs/task/progress.md` before code changes.
- Define scope, non-goals, DoD, and evidence paths.
- Build a bounded plan per loop (target <= 1 hour or a few hundred LOC).
- For high-risk multi-file work, compare 2-3 options briefly before choosing one.
- For sprint commands, include all unfinished items from the mapped sprint doc in the execution backlog.

### 2) Code phase (strict TDD loop)
Repeat until all scoped tasks are done:
1. Pick the smallest unfinished hotspot from the progress cursor.
2. Add or adjust a failing test first (or explain why test-first is blocked).
3. Implement the minimal code change that satisfies the test.
4. Run targeted tests first; when needed, isolate with `--override-ini="addopts="`.
5. Fix failures from root cause, never by bypassing checks.
6. Update `docs/task/progress.md` for this round with:
   - 今日进展
   - 明日计划
   - 风险与阻塞
   - 关联链接
7. If the user says `continue`, resume directly from the next action in `docs/task/progress.md`.
8. If the user says `sN go` again, re-sync against `docs/sprint/sprintN.md` and continue the same loop.

### 3) Review and completion gates
Before claiming completion:
- Re-check `git status` and relevant diffs.
- Confirm sprint/backlog/progress docs are consistent with code changes.
- Report residual risks and testing gaps explicitly.
- If work remains, provide the next concrete action and continue.

## Response contract
Output in this order:
1. Current loop state (task, test status, blockers)
2. Actions executed this round
3. Evidence (commands, tests, touched files)
4. Next action

Prefer execution-focused updates over long theory.

## Safety rails
- Do not do unrelated refactors during loop mode.
- Prefer small, verifiable iterations.
- State assumptions when uncertain and ask one concise blocking question only when needed.
- Follow project conventions from `CLAUDE.md` over personal preference.

## Resources
- See `references/loop-templates.md` for reusable fixed prompts and slash-like shortcuts.
- See `references/one-line-entry-dictionary.md` for the cross-skill one-line command dictionary.

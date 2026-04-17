---
name: sprint-close-auditor
description: Sprint closeout audit that reconciles sprint/backlog/progress docs with code and tests. Use when the user asks whether a sprint is truly complete, what remains, and what blockers or risks must be resolved before closure.
---

# Sprint Close Auditor

## Goal
Provide an evidence-backed closeout verdict for a sprint: complete, partial, or blocked.

## Trigger shortcuts
- Treat these as equivalent intents when this skill is named:
  - `/sprint-close-auditor sprint5 close`
  - `/sprint-close-auditor s5 close`
  - `/sprint-close-auditor closeout sprint5`
- Map `sprintN` to `docs/sprint/sprintN.md` by default.

## Workflow

### 1) Scope setup
- Read `CLAUDE.md` first.
- Load sprint source doc (`docs/sprint/sprintN.md`) and `docs/task/progress.md`.
- Include linked backlog/pack sections when referenced.

### 2) Task inventory and normalization
- Enumerate sprint tasks and DoD items from docs.
- Normalize each item into one row with: id/title, expected artifact, expected test evidence.
- Mark declared status from docs (`done`, `in progress`, `todo`, unknown).

### 3) Evidence reconciliation
- Check implementation evidence in code paths.
- Check verification evidence (tests, commands, reports, logs).
- Compare doc status versus code/test reality and flag drift.

### 4) Finding classification
Classify each finding as:
- `P0` Blocking gap (task marked done but missing core implementation or failing behavior)
- `P1` High risk gap (implemented but missing required tests/guards)
- `P2` Medium drift (doc inconsistency, weak acceptance evidence)
- `P3` Low cleanup

### 5) Rebuild pitfalls index (sprint close 时强制)
```bash
PYTHONPATH=. python3 scripts/build_pitfalls_index.py
```
新增的 archive 会被自动索引，下个 sprint 启动时 CC/Codex 检索更准确。

### 6) Closeout output
Return in this order:
1. Sprint verdict: `Complete` / `Partial` / `Blocked`
2. Completion matrix (task-by-task)
3. Findings by severity with file/doc evidence
4. Required actions to close sprint
5. Residual risks
6. **Compound knowledge**: 本 sprint 沉淀了哪些 solutions / 更新了哪些现有 solutions

## Safety rails
- Do not mark sprint complete without evidence for code and tests.
- Prefer verifiable facts over interpretation.
- If evidence is missing, report as a gap instead of assuming completion.
- Keep scope to sprint closeout; avoid unrelated optimization work.

## Resources
- See `references/closeout-template.md` for matrix format and verdict rules.

# Loop Templates

Use these templates as quick triggers. Fill placeholders before sending.

## Ultra-short triggers

### Sprint run (recommended)
```text
/tdd-loop-executor sprint5 go
```

### Sprint shorthand (works when skill is explicit)
```text
/tdd-loop-executor s5 go
```

Behavior:
- Auto-map `sprint5` to `docs/sprint/sprint5.md`
- Use `docs/task/progress.md` as the loop cursor
- Run plan + strict TDD + progress sync until sprint tasks are finished

## Fixed prompts

### 1) Start loop
```text
Use /tdd-loop-executor.
Goal: <goal>
Scope: <files/modules>
DoD: <acceptance criteria>
Start Ask phase now, then enter strict TDD loop until completion.
```

### 2) Continue loop
```text
Use /tdd-loop-executor and continue from docs/task/progress.md next action.
Keep strict TDD and update progress doc this round.
```

### 3) Root-cause repair
```text
Use /tdd-loop-executor.
Issue: <error/log/test failure>
Do root-cause analysis, add regression test first, apply minimal fix, rerun related tests, then sync progress doc.
```

### 4) Pre-close verification
```text
Use /tdd-loop-executor.
Run completion gates: git status/diff check, docs consistency check, residual risk list, and final next-step decision.
```

## Slash-like shortcuts

Treat these shortcuts as intent aliases:
- `/loop.start <goal>`: start Ask phase and produce bounded execution plan.
- `/loop.next`: continue from progress cursor without re-planning from scratch.
- `/loop.fix <issue>`: perform root-cause fix with test-first validation.
- `/loop.review`: run completion gates and strict consistency review.
- `/loop.close`: produce final completion report with residual risks and follow-ups.

## Minimal output shape
```text
Loop state
- Task: ...
- Test status: ...
- Blockers: ...

This round
- ...

Evidence
- Commands: ...
- Tests: ...
- Files: ...

Next
- ...
```

# Sprint Closeout Template

## Verdict rules
- `Complete`: no P0/P1 open gaps and required tests/evidence exist.
- `Partial`: no P0, but one or more P1/P2 gaps remain.
- `Blocked`: any P0 gap exists.

## Completion matrix
```text
| Task | Doc status | Code evidence | Test evidence | Audit status | Notes |
|------|------------|---------------|---------------|--------------|-------|
| ...  | done       | path:line     | pytest ...    | pass/gap     | ...   |
```

## Findings format
```text
[P1][0.82] Missing regression guard for retry path
- Evidence: /abs/path/file.py:123, docs/sprint/sprint5.md
- Impact: ...
- Required action: ...
```

## Required actions format
```text
Closeout actions
1. ...
2. ...
3. ...
```

## Suggested verification commands
- `git status`
- `git diff --stat`
- `pytest -q <targeted tests>`
- Add `--override-ini="addopts="` for isolated runs when needed.

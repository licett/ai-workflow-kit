---
name: code-review-expert
description: Thorough code review for changed code, pull requests, and targeted files. Use when the user asks to review implementation quality, bugs, regressions, security, performance, testing, or maintainability. Prioritize findings first, with severity, confidence, concrete file:line evidence, and actionable fixes.
---

# Code Review Expert

Produce a practical, evidence-based review that helps the developer ship safely.

## Scope and context
1. Identify review scope first.
   - Prefer changed code (`git status`, `git diff`) unless the user asks for full-file or full-repo review.
   - If scope is ambiguous, ask once and propose a default (working tree diff).
2. Read project constraints before judging style.
   - Check `CLAUDE.md`, lint rules, tests, and local conventions.
   - Prefer consistency with existing project patterns over personal preference.

## Review priorities
Evaluate in this order:
1. Correctness and regressions
2. Security and data exposure
3. Reliability and error handling
4. Performance and scalability
5. Maintainability and readability
6. Test coverage and observability

Before deep review, open `references/review-checklists.md` and select only the sections relevant to the language and stack in scope.

## Chinese output template
Default to Chinese output with concise technical terms in English where clearer.

Use this response shape:
- `Findings`: list by severity descending; each item must include `[Px][confidence]`, `file:line`, impact, and fix.
- `Open questions`: assumptions, unknown runtime behavior, missing context.
- `Strengths`: short and factual; keep after findings.
- `Next actions`: targeted tests or verification commands.

Example skeleton:
```text
发现的问题（按严重度）
- [P1][0.86] 空指针路径未保护 — path/to/file.py:42
  影响：在输入为空时会触发 500，导致请求失败。
  建议：在进入分支前增加空值判断并返回可恢复错误。

待确认
- 某外部 API 的 timeout 是否由上层统一注入。

做得好的点
- 错误码枚举与日志字段保持一致，便于排障。

后续建议
- 运行: pytest tests/module/test_x.py::test_null_input --override-ini="addopts="
```

## Severity model
- `P0` Blocking: clear bug, exploit, data corruption, crash, or release blocker.
- `P1` High: likely production issue or major reliability/performance risk.
- `P2` Medium: meaningful quality issue; should be fixed soon.
- `P3` Low: minor improvement or non-blocking cleanup.

Always include confidence (`0.00-1.00`) for each finding.

## Finding format
For each finding, include:
- Severity and confidence: `[P1][0.84]`
- Short title
- Evidence path with line: `path/to/file.py:123`
- Why it matters (user or system impact)
- Concrete fix recommendation (small patch idea when helpful)

Keep findings specific and reproducible. Do not invent line numbers or behavior.

## Output order
1. Findings (highest severity first)
2. Open questions or assumptions
3. Brief strengths (only after findings)
4. Next actions (tests, verification, rollout guards)

If there are no findings, state that explicitly and still list residual risks or testing gaps.

## Review behavior rules
- Focus on changed lines, but inspect nearby context for integration issues.
- Avoid style-only nitpicks unless they hide a bug or team rule violation.
- Explain trade-offs when suggesting alternative designs.
- Prefer minimal, safe fixes over broad rewrites during review.
- Recommend targeted tests for each high-impact issue.

# Review Checklists

Use only the sections relevant to the current scope. Do not force every item.

## 1) Universal checks
- Behavior change is intentional and documented by tests.
- Error handling returns actionable messages without leaking secrets.
- Edge cases are covered (empty/null/timeout/retry/idempotency).
- Logging keeps key context (request id, actor, resource id) and avoids sensitive data.
- Backward compatibility is preserved or migration path is explicit.

## 2) Python-focused checks
- Type hints are coherent at public boundaries.
- Mutable default arguments are avoided.
- Exceptions are specific (avoid broad `except Exception` unless re-raising with context).
- Resource management uses context managers (`with`) where appropriate.
- Concurrency/async code avoids blocking calls on async paths.

## 3) Security checks
- Inputs are validated close to trust boundaries.
- AuthN/AuthZ checks are enforced server-side, not only client-side.
- SQL/command/template usage is parameterized (no unsafe string concat).
- Secrets/tokens/cookies are not logged or committed.
- File/path handling prevents traversal and unsafe deserialization.

## 4) Performance checks
- Algorithmic hotspots are bounded and justified.
- N+1 database/API call patterns are avoided.
- Expensive calls have caching/batching strategy when needed.
- Large payload parsing/serialization is bounded.
- Retries have backoff and do not amplify traffic under failure.

## 5) Tests and observability
- New or changed behavior has focused unit/integration tests.
- Regression tests exist for bug fixes.
- Metrics/logs/traces allow detection of failures after rollout.
- Feature flags or safe rollout guards exist for risky changes.
- Test commands are reproducible and scoped when possible.

## 6) Findings quality bar
- Every finding includes `severity`, `confidence`, and `file:line`.
- Explain impact before suggesting fix.
- Prefer minimal fix suggestions and add trade-off notes for alternatives.
- Mark uncertain claims as assumptions or questions.
- If no findings, still report residual risks and untested areas.

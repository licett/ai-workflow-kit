# Log Triage Patterns

Use these starter patterns and adapt per stack.

## Quick grep starters
- Exceptions and crashes:
  - `rg -n "Exception|Traceback|panic|FATAL|Segmentation|SIG" <log>`
- Timeout and network:
  - `rg -n "timeout|timed out|ECONNRESET|EPIPE|503|504|connection" <log>`
- Auth and permission:
  - `rg -n "401|403|unauthorized|forbidden|token|credential|permission" <log>`
- Data and parsing:
  - `rg -n "JSON|parse|schema|KeyError|TypeError|ValueError|null" <log>`

## Hypothesis template
```text
H1 [0.72]: <candidate cause>
- Evidence: <file:line or log signature>
- Disproof check: <command/test>
```

## Root-cause report shape
```text
Incident summary
- ...

Evidence timeline
- T1 ...
- T2 ...

Root cause
- Primary [0.xx]: ...
- Secondary [0.xx]: ...

Fix plan
- ...

Verification
- ...

Residual risks
- ...
```

## Redaction reminders
- Replace API keys, auth headers, cookies, and account IDs with masked placeholders.
- Keep enough context for debugging but remove sensitive values.

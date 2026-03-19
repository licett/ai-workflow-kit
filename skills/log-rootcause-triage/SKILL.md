---
name: log-rootcause-triage
description: Root-cause triage for runtime logs, stack traces, and failing test output. Use when the user asks why a failure happened, which code path is responsible, and what minimal fix plus verification steps should be applied.
---

# Log Rootcause Triage

## Goal
Turn raw logs into a ranked root-cause diagnosis with a minimal, test-backed repair plan.

## Trigger shortcuts
- Treat these as equivalent intents when this skill is named:
  - `/log-rootcause-triage /abs/path/to/log.log`
  - `/log-rootcause-triage triage <path>`
  - `/log-rootcause-triage s5 triage <path>`
  - `/log-rootcause-triage analyze stack trace`
- If the user sends only a path, infer triage intent and start analysis.
- If the user includes `sN` (for example `s5`), treat it as sprint context for reporting and follow-up links.

## Workflow

### 1) Scope and evidence collection
- Read `CLAUDE.md` first for project constraints.
- Locate the provided log or failing test output.
- Extract a compact timeline: first error, repeated errors, last successful signal.
- Use fast filters (`rg`) for critical markers from `references/patterns.md`.

### 2) Fault isolation
- Map error signatures to candidate files/functions.
- Build 2-4 hypotheses, each with confidence and disproof checks.
- Separate confirmed facts from assumptions.

### 3) Root-cause confirmation
- Reproduce with the smallest command or test.
- Confirm one primary root cause, and note secondary contributors.
- If confirmation is blocked, state the blocking data explicitly.

### 4) Fix and verification plan
- Propose the minimal patch scope first.
- Add regression tests before or alongside the fix.
- Prefer targeted test commands, then broader checks only when needed.

### 5) Output contract
Return in this order:
1. Incident summary (what failed, where, when)
2. Evidence timeline (key log lines or signatures)
3. Root cause (primary + secondary, with confidence)
4. Minimal fix plan
5. Verification commands
6. Residual risks and follow-ups

## Safety rails
- Never expose secrets from logs; redact tokens/cookies/credentials.
- Do not claim root cause without evidence path.
- Avoid broad refactors during triage unless required by the confirmed cause.
- If uncertainty remains, list exactly what data is needed to close the gap.

## Resources
- See `references/patterns.md` for signature groups, grep starters, and report templates.

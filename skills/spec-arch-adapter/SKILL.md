---
name: spec-arch-adapter
description: Bootstrap or repair a repository's spec documentation architecture (README/CLAUDE.md/docs index/progress/module maps) and adapt projects to the standard layout.
---

# Spec Architecture Adapter

Use this skill when you need to rebuild or adapt a project to the standard spec documentation architecture.

## Quick Start

- **Default (write, full)**
  - `python ~/.claude/skills/spec-arch-adapter/scripts/spec_arch_audit.py --root <repo> --mode write --profile full`

- **Read-only audit**
  - `python ~/.claude/skills/spec-arch-adapter/scripts/spec_arch_audit.py --root <repo> --mode audit --profile full --print-json`

- **Minimal profile** (fewer placeholders)
  - `--profile minimal`

- **Overwrite existing files** (only when explicitly requested)
  - `--update-existing`

## What It Creates (when missing)

- Entry docs: `README.md`, `README.en.md`, `AGENTS.md`, `CLAUDE.md`
- Docs index: `docs/README.md`
- Progress cursor: `docs/task/progress.md`
- Sprint/spec/design indexes: `docs/sprint/README.md`, `docs/spec/README.md`, `docs/design/README.md`
- Optional (full profile): `docs/rules/PROJECT_RULES.md`, `docs/review/ai-workflow.md`, `docs/qa/tests_guideline.txt`, `docs/research/README.md`
- Module maps: `config/README.md`, `src/*/README.md` (only when directories exist)

## Template Sources

- Fixed templates copied from this project:
  - `docs/rules/PROJECT_RULES.md`
  - `docs/review/ai-workflow.md`
  - `docs/qa/tests_guideline.txt`
- `AGENTS.md` uses a fixed template with small generated fields (languages/entrypoints/tests).

## Workflow

1. Run the script in **write** mode to create missing files.
2. Review the summary and refine placeholders as needed.
3. If the repo has progress rules, update `docs/task/progress.md` and commit changes.
4. If new directories/entrypoints exist, add or update module map README files.

## Content Generation Gate (required)

Before filling any narrative content beyond detected facts, run an in-depth project exploration. Use this prompt:

```
We will conduct an in-depth exploration of this project.

Objectives:
- Understand the project's background, design, and core objectives.
- Develop familiarity with the architecture and implementation details.
- Identify current status, pending tasks, issues, and risks.
```

Rules:
- Cite sources using file paths when writing summaries.
- If evidence is insufficient, keep placeholders or mark TBD.
- Include an explicit "Evidence Index" list of file paths in the final report.
- Current status/risks must be sourced from docs/task/progress.md or sprint docs.

## Notes

- The script never deletes files.
- Existing files are not overwritten unless `--update-existing` is provided.
- Module maps are created only for directories that exist.
- Templates are intentionally minimal; fill in project-specific details after bootstrap.

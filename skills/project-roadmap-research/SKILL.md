---
name: project-roadmap-research
description: Deep, read-only roadmap research for software projects using CLAUDE.md or linked docs. Use when asked to explore a repository, map architecture and data flow, summarize current sprint status, and list risks/blocks with evidence paths. Supports multi-project workspaces; writes to docs/research/roadmap.md only for roots with CLAUDE.md.
---

# Project Roadmap Research

## Overview
Produce an evidence-based, read-only investigation using CLAUDE.md and linked docs as the primary roadmap. Focus on architecture, core data flow, current status, open issues, and risks. Write output only to the allowed path when CLAUDE.md exists.

## Defaults
- multi_project: true
- output_mode: write only for roots with CLAUDE.md
- output_path: docs/research/roadmap.md
- write_policy: controlled block replacement
- missing_dir_policy: create
- non_agents_policy: chat-only and skip write
- module_coverage: required
- file_header_scan: required

## Project discovery
1. Scan for CLAUDE.md and treat each directory containing it as a project root.
2. For non-CLAUDE roots, only consider README/manifest candidates that pass root signals.
3. Do not recurse into nested README/manifest roots if a CLAUDE root already covers the path.
4. Apply noise filters only after detection; never drop a CLAUDE root.

## Root signals (README/manifest candidates)
- Require at least one of: .git, src/, docs/, config/
- Exclude candidates where the README/manifest lives under docs/examples/sample/demo/test/tools/scripts

## Supported manifest files
- README.md, README.en.md
- requirements.txt, pyproject.toml, package.json, go.mod, Cargo.toml
- pom.xml, build.gradle, build.gradle.kts, settings.gradle
- composer.json, Gemfile, Package.swift, Podfile
- *.csproj, *.fsproj, *.vbproj, *.sln, Directory.Build.props

## Workflow
1. Build project list using scripts/list-project-roots.sh.
2. For each CLAUDE root:
   - Read CLAUDE.md and linked docs in order.
   - Read sprint/progress/research/qa docs.
   - Run scripts/entrypoint-scan.sh to anchor core flows.
   - Enforce module coverage and file header scan (see below).
3. Summarize background, architecture, status, risks, and gaps with evidence paths.
4. Use references/report-template.md for structure.
5. Write report using controlled block replacement (CLAUDE roots only).

## Module coverage (required)
- Read all module maps:
  - config/README.md
  - src/*/README.md
  - src/**/README.md
  - docs/**/README.md (when it lists modules)
- For each module README:
  - Open the files listed under Entry Points.
  - If Entry Points are missing, fall back to entrypoint-scan.sh results or module __init__.py/main.py/app.py.
- Record at least one code evidence path per module; if missing, log a gap.

## File header scan (required)
- Read the first 10-20 lines of every source file under src/ and config/.
- Exclude noise directories: .git, .venv, venv, myvenv, node_modules, tmp, logs, data, build, dist, __pycache__.
- Use headers only for overview extraction; do not load full file unless needed by module coverage.

## Controlled block replacement
- Use markers:
  - <!-- CLAUDE:ROADMAP:BEGIN -->
  - <!-- CLAUDE:ROADMAP:END -->
- If file does not exist: create it and insert the block.
- If block exists: replace only the block content.
- If block missing: insert the block and keep existing content intact.

## Evidence rules
- Every key claim includes a file path.
- Missing or unreadable docs must be logged as gaps.

## Resources
- references/report-template.md
- scripts/list-project-roots.sh
- scripts/roadmap-index.sh
- scripts/doc-link-graph.py
- scripts/entrypoint-scan.sh

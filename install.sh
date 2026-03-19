#!/usr/bin/env bash
# AI Workflow Kit — 一键安装 Claude Code Skills
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"
SKILLS_DST="${HOME}/.claude/skills"

if [ ! -d "$SKILLS_SRC" ]; then
  echo "ERROR: skills/ directory not found at $SKILLS_SRC"
  exit 1
fi

mkdir -p "$SKILLS_DST"

SKILLS=(
  adversarial-cross-model-review
  code-review-expert
  cross-review-gate
  log-rootcause-triage
  project-roadmap-research
  spec-arch-adapter
  sprint-close-auditor
  sprint-design-reviewer
  tdd-loop-executor
)

installed=0
skipped=0

for skill in "${SKILLS[@]}"; do
  src="$SKILLS_SRC/$skill"
  dst="$SKILLS_DST/$skill"

  if [ ! -d "$src" ]; then
    echo "  SKIP  $skill (source not found)"
    ((skipped++))
    continue
  fi

  if [ -d "$dst" ]; then
    echo "  UPDATE  $skill (overwriting existing)"
    rm -rf "$dst"
  else
    echo "  INSTALL $skill"
  fi

  cp -r "$src" "$dst"
  ((installed++))
done

echo ""
echo "Done: $installed skills installed, $skipped skipped."
echo ""
echo "Next steps:"
echo "  1. cd <your-project>"
echo "  2. python ~/.claude/skills/spec-arch-adapter/scripts/spec_arch_audit.py --root . --mode write --profile full"
echo "  3. Read the README.md in this kit for methodology guidance"

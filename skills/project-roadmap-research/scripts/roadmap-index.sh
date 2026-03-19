#!/usr/bin/env bash
set -euo pipefail

ROOTS=("$@")
if [[ ${#ROOTS[@]} -eq 0 ]]; then
  ROOTS=(".")
fi

for root in "${ROOTS[@]}"; do
  echo "== ${root} =="

  paths=(
    "AGENTS.md"
    "README.md"
    "README.en.md"
    "docs/README.md"
    "docs/rules/PROJECT_RULES.md"
    "docs/task/progress.md"
    "docs/review/ai-workflow.md"
    "docs/qa/tests_guideline.txt"
    "docs/api/openapi.json"
  )

  for rel in "${paths[@]}"; do
    if [[ -e "${root}/${rel}" ]]; then
      echo "${root}/${rel}"
    fi
  done

  if [[ -d "${root}/docs/sprint" ]]; then
    for f in "${root}"/docs/sprint/*.md; do
      [[ -e "$f" ]] && echo "$f"
    done
  fi

  if [[ -d "${root}/docs/design" ]]; then
    echo "${root}/docs/design/"
  fi

  if [[ -d "${root}/docs/research" ]]; then
    echo "${root}/docs/research/"
  fi

  if [[ -d "${root}/docs/qa" ]]; then
    echo "${root}/docs/qa/"
  fi

  echo

done

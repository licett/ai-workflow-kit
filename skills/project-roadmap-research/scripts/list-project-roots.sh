#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

if ! command -v rg >/dev/null 2>&1; then
  echo "rg not found; install ripgrep to use this script" >&2
  exit 1
fi

EXCLUDE_BASENAMES=(
  docs examples sample demo test tests tools scripts
  .git .venv venv myvenv node_modules tmp logs data build dist __pycache__
  chrome_extention chrome_extention_alive
)

NOISE_SEGMENTS=(
  "/.git/" "/.venv/" "/venv/" "/myvenv/" "/node_modules/"
  "/tmp/" "/logs/" "/data/" "/build/" "/dist/" "/__pycache__/"
  "/chrome_extention" "/chrome_extention_alive"
)

is_excluded_basename() {
  local base
  base="$(basename "$1")"
  for name in "${EXCLUDE_BASENAMES[@]}"; do
    if [[ "$base" == "$name" ]]; then
      return 0
    fi
  done
  return 1
}

is_noise_path() {
  local path="$1"
  for seg in "${NOISE_SEGMENTS[@]}"; do
    if [[ "$path" == *"$seg"* ]]; then
      return 0
    fi
  done
  return 1
}

has_root_signal() {
  local dir="$1"
  [[ -e "$dir/.git" || -d "$dir/src" || -d "$dir/docs" || -d "$dir/config" ]]
}

TMP_AGENTS="$(mktemp)"
TMP_ROOTS="$(mktemp)"

cleanup() {
  rm -f "$TMP_AGENTS" "$TMP_ROOTS"
}
trap cleanup EXIT

while IFS= read -r file; do
  dir="$(dirname "$file")"
  printf '%s\n' "$dir" >> "$TMP_AGENTS"
done < <(rg --files -g 'AGENTS.md' "$ROOT")

sort -u "$TMP_AGENTS" -o "$TMP_AGENTS"

is_under_agents_root() {
  local dir="$1"
  local root
  while IFS= read -r root; do
    [[ -z "$root" ]] && continue
    if [[ "$dir" == "$root" || "$dir" == "$root"/* ]]; then
      return 0
    fi
  done < "$TMP_AGENTS"
  return 1
}

is_agents_root() {
  local dir="$1"
  if grep -F -x -q -- "$dir" "$TMP_AGENTS"; then
    return 0
  fi
  return 1
}

MANIFEST_GLOBS=(
  'README.md' 'README.en.md'
  'requirements.txt' 'pyproject.toml' 'package.json' 'go.mod' 'Cargo.toml'
  'pom.xml' 'build.gradle' 'build.gradle.kts' 'settings.gradle'
  'composer.json' 'Gemfile' 'Package.swift' 'Podfile'
  '*.csproj' '*.fsproj' '*.vbproj' '*.sln' 'Directory.Build.props'
)

cmd=(rg --files "$ROOT")
for glob in "${MANIFEST_GLOBS[@]}"; do
  cmd+=(-g "$glob")
done

while IFS= read -r file; do
  dir="$(dirname "$file")"
  if is_agents_root "$dir"; then
    continue
  fi
  if is_under_agents_root "$dir"; then
    continue
  fi
  if is_excluded_basename "$dir"; then
    continue
  fi
  if is_noise_path "$dir"; then
    continue
  fi
  if ! has_root_signal "$dir"; then
    continue
  fi
  printf '%s\n' "$dir" >> "$TMP_ROOTS"

done < <("${cmd[@]}")

sort -u "$TMP_ROOTS" -o "$TMP_ROOTS"

while IFS= read -r dir; do
  [[ -z "$dir" ]] && continue
  printf "AGENTS\t%s\n" "$dir"
done < "$TMP_AGENTS" | sort

while IFS= read -r dir; do
  [[ -z "$dir" ]] && continue
  printf "ROOT_NO_AGENTS\t%s\n" "$dir"
done < "$TMP_ROOTS" | sort

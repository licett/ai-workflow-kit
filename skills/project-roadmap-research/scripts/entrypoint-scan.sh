#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

if ! command -v rg >/dev/null 2>&1; then
  echo "rg not found; install ripgrep to use this script" >&2
  exit 1
fi

cd "$ROOT"

rg -n \
  --glob 'src/**' \
  --glob 'scripts/**' \
  -e 'if __name__ == "__main__"' \
  -e 'asyncio.run' \
  -e '/strategy' \
  -e 'start_' \
  -e '848[0-9]' \
  || true

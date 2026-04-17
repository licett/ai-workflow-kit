#!/bin/bash
# Watches Codex pane output via tmux pipe-pane.
# Touches signal file when Codex returns to › prompt (response complete).
# Usage: tmux pipe-pane -t <pane> "bash scripts/codex-done-watcher.sh <tmux-session>"

TMUX_SESSION="${1:-default}"
SIGNAL="/tmp/.codex_done_${TMUX_SESSION}"

while IFS= read -r line; do
  # › is Codex's interactive prompt — means it finished responding
  if echo "$line" | grep -q "›"; then
    touch "$SIGNAL"
  fi
done

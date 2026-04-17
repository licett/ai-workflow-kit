#!/bin/bash
# codex-pair.sh — CC-Codex pair programming via tmux + smux tmux-bridge
#
# Architecture:
#   Left pane: CC (Claude Code)
#   Right pane: Codex interactive session (user sees everything)
#   Communication: tmux-bridge type (send) + tmux-bridge read (read)
#   Pane tracking: tmux-bridge name/resolve (label-based, no flag files)
#   Context: Codex native interactive session (no adapter, no ACP protocol)
#
# Usage:
#   scripts/codex-pair.sh prewarm              # create right pane + start codex
#   scripts/codex-pair.sh send /tmp/prompt.txt # send prompt to codex
#   scripts/codex-pair.sh read [N]             # read last N lines from codex pane
#   scripts/codex-pair.sh alive                # is codex responding?
#   scripts/codex-pair.sh status               # session info
#   scripts/codex-pair.sh state [set '{...}']  # read/write workflow state
#   scripts/codex-pair.sh ledger [N]           # last N ledger entries
#   scripts/codex-pair.sh recovery             # last 5 interactions
#   scripts/codex-pair.sh close                # kill codex pane

set -uo pipefail

export PATH="$HOME/.smux/bin:$PATH"

# Isolation key: tmux session name (each ccs creates unique tmux session)
TMUX_SESSION=$(tmux display-message -p "#{session_name}" 2>/dev/null || echo "notmux")
SESSION_NAME="codex-${TMUX_SESSION}"
CODEX_LABEL="codex-${TMUX_SESSION}"
LEDGER_FILE="$(pwd)/data/codex-pair-ledger.jsonl"

mkdir -p "$(dirname "$LEDGER_FILE")" 2>/dev/null || true

in_tmux() {
  tmux display-message -p "#{session_name}" >/dev/null 2>&1
}

ledger_append() {
  local direction="$1" event="$2" summary="$3"
  local ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  printf '{"ts":"%s","session":"%s","direction":"%s","event":"%s","summary":"%s"}\n' \
    "$ts" "$SESSION_NAME" "$direction" "$event" "$summary" >> "$LEDGER_FILE"
}

get_codex_pane() {
  tmux-bridge resolve "$CODEX_LABEL" 2>/dev/null
}

pane_alive() {
  local pane=$(get_codex_pane)
  [ -n "$pane" ] && [ "$pane" != "" ]
}

ensure_codex_pane() {
  if ! in_tmux; then
    echo "[codex-pair] ERROR: not in tmux. Start with: ccs <name>"
    exit 1
  fi

  if pane_alive; then
    echo "[codex-pair] Codex pane already running (label: $CODEX_LABEL)"
    return 0
  fi

  # Split right 50%, start codex interactive
  local NEW_PANE=$(tmux split-window -h -p 50 -d -P -F "#{pane_id}" \
    "codex -a never")

  # Wait for codex to start, then label the pane
  sleep 3
  tmux-bridge name "$NEW_PANE" "$CODEX_LABEL"

  # Start pipe-pane watcher: monitors Codex output for › prompt → touches signal file
  tmux pipe-pane -t "$NEW_PANE" "bash $(pwd)/scripts/codex-done-watcher.sh $TMUX_SESSION"

  echo "[codex-pair] Codex started in pane $NEW_PANE (label: $CODEX_LABEL, watcher attached)"
  ledger_append "system" "session_create" "Codex pane $NEW_PANE label=$CODEX_LABEL watcher=on"
}

send_prompt() {
  local PROMPT_FILE="$1"
  if [ -z "$PROMPT_FILE" ]; then
    echo "[codex-pair] ERROR: usage: scripts/codex-pair.sh send /tmp/prompt.txt"
    exit 1
  fi
  if [ ! -f "$PROMPT_FILE" ]; then
    echo "[codex-pair] ERROR: file not found: $PROMPT_FILE"
    exit 1
  fi

  ensure_codex_pane
  local PANE=$(get_codex_pane)
  local SIZE=$(wc -c < "$PROMPT_FILE")
  local SUMMARY=$(head -3 "$PROMPT_FILE" | tr '\n' ' ' | cut -c1-200)

  echo "[codex-pair] Sending prompt: $PROMPT_FILE ($SIZE bytes)"
  ledger_append "cc→co" "send" "$SUMMARY"

  # Clear signal file before sending
  DONE_SIGNAL="/tmp/.codex_done_${TMUX_SESSION}"
  rm -f "$DONE_SIGNAL"

  # Send via tmux load-buffer + paste-buffer (handles multi-line + special chars)
  tmux load-buffer "$PROMPT_FILE"
  tmux paste-buffer -t "$PANE"

  # Send Enter with retry — paste may not be fully processed on first try
  sleep 1
  tmux-bridge keys "$PANE" Enter
  sleep 0.5
  # Second Enter as safety — if Codex already started, extra Enter is harmless (just empty input)
  tmux-bridge keys "$PANE" Enter

  echo "[codex-pair] Prompt sent. Waiting for Codex response..."

  # Wait for signal with: health check + Enter retry + hard timeout
  local WAITED=0
  local ENTER_RETRY=60   # re-send Enter every 60s in case lost
  local HEALTH_CHECK=120  # health check every 2 min
  local HARD_TIMEOUT=3600 # 1 hour hard cap
  while [ ! -f "$DONE_SIGNAL" ]; do
    sleep 1
    WAITED=$((WAITED + 1))

    # Hard timeout
    if [ $WAITED -ge $HARD_TIMEOUT ]; then
      echo "[codex-pair] ⚠️ Hard timeout (${HARD_TIMEOUT}s). Codex did not respond."
      ledger_append "system" "error" "Hard timeout ${HARD_TIMEOUT}s"
      return 1
    fi

    # Every 60s: re-send Enter in case lost
    if [ $((WAITED % ENTER_RETRY)) -eq 0 ]; then
      tmux-bridge keys "$PANE" Enter 2>/dev/null
    fi

    # Every 2 min: health check — is Codex pane still alive?
    if [ $((WAITED % HEALTH_CHECK)) -eq 0 ]; then
      if ! pane_alive; then
        echo "[codex-pair] ⚠️ Codex pane died during execution."
        ledger_append "system" "error" "Codex pane died at ${WAITED}s"
        return 1
      fi
    fi
  done
  rm -f "$DONE_SIGNAL"

  echo "[codex-pair] Codex responded (${WAITED}s)."
  ledger_append "co→cc" "receive" "Codex responded (signal, ${WAITED}s)"
}

read_codex() {
  local N="${1:-50}"
  if ! pane_alive; then
    echo "[codex-pair] No codex pane"
    return 1
  fi
  local PANE=$(get_codex_pane)
  tmux-bridge read "$PANE" "$N"
}

check_alive() {
  if ! pane_alive; then
    echo "[codex-pair] DEAD — codex pane not running"
    return 1
  fi
  local PANE=$(get_codex_pane)
  local LAST_CONTENT=$(tmux-bridge read "$PANE" 5 2>/dev/null)
  if echo "$LAST_CONTENT" | grep -q "›"; then
    echo "[codex-pair] IDLE — codex waiting for input (› prompt visible)"
  else
    echo "[codex-pair] WORKING — codex processing"
  fi
}

show_ledger() {
  local N="${1:-10}"
  if [ ! -f "$LEDGER_FILE" ]; then
    echo "[codex-pair] No ledger"
    return
  fi
  echo "[codex-pair] Last $N entries:"
  tail -"$N" "$LEDGER_FILE" | python3 -c "
import json, sys
for line in sys.stdin:
    try:
        e = json.loads(line)
        ts = e.get('ts','')[:19]
        d = e.get('direction','?')
        ev = e.get('event','?')
        s = e.get('summary','')[:80]
        print(f'  {ts} | {d:8s} | {ev:15s} | {s}')
    except: pass
" 2>/dev/null
}

show_recovery() {
  if [ ! -f "$LEDGER_FILE" ]; then
    echo "[codex-pair] No ledger"
    return
  fi
  echo "[codex-pair] Last 5 interactions:"
  grep -E '"(send|receive)"' "$LEDGER_FILE" | tail -5 | python3 -c "
import json, sys
for i, line in enumerate(sys.stdin, 1):
    try:
        e = json.loads(line)
        ts = e.get('ts','')[:19]
        d = e.get('direction','?')
        s = e.get('summary','')
        print(f'{i}. [{ts}] {d}: {s}')
    except: pass
" 2>/dev/null
}

case "${1:-}" in
  prewarm)
    ensure_codex_pane
    ;;
  send)
    send_prompt "${2:-}"
    ;;
  -f)
    send_prompt "${2:-}"
    ;;
  read)
    read_codex "${2:-50}"
    ;;
  alive)
    check_alive
    ;;
  state)
    STATE_FILE="/tmp/.codex_pair_state_${TMUX_SESSION}.json"
    if [ "${2:-}" = "set" ]; then
      echo "${3:-}" > "$STATE_FILE"
      echo "[codex-pair] State updated: $STATE_FILE"
    else
      if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
      else
        echo "{}"
      fi
    fi
    ;;
  status)
    STATE_FILE="/tmp/.codex_pair_state_${TMUX_SESSION}.json"
    echo "[codex-pair] Session: $SESSION_NAME"
    echo "[codex-pair] tmux: $TMUX_SESSION"
    echo "[codex-pair] Label: $CODEX_LABEL"
    echo "[codex-pair] Pane: $(get_codex_pane 2>/dev/null || echo 'none')"
    echo "[codex-pair] State: $STATE_FILE"
    echo "[codex-pair] Ledger: $(wc -l < "$LEDGER_FILE" 2>/dev/null || echo 0) entries"
    pane_alive && echo "[codex-pair] Codex: running" || echo "[codex-pair] Codex: not running"
    check_alive 2>/dev/null
    echo "[codex-pair] All panes:"
    tmux-bridge list 2>/dev/null
    ;;
  ledger)
    show_ledger "${2:-10}"
    ;;
  recovery)
    show_recovery
    ;;
  close)
    PANE=$(get_codex_pane 2>/dev/null)
    if [ -n "$PANE" ]; then
      tmux kill-pane -t "$PANE" 2>/dev/null || true
      ledger_append "system" "close" "Codex pane closed (label: $CODEX_LABEL)"
      echo "[codex-pair] Codex pane closed"
    else
      echo "[codex-pair] No codex pane to close"
    fi
    ;;
  *)
    if [ -f "${1:-}" ]; then
      send_prompt "$1"
    else
      echo "[codex-pair] Usage:"
      echo "  scripts/codex-pair.sh prewarm              # start codex in right pane"
      echo "  scripts/codex-pair.sh send /tmp/prompt.txt # send prompt"
      echo "  scripts/codex-pair.sh read [N]             # read last N lines from codex"
      echo "  scripts/codex-pair.sh alive                # check codex status"
      echo "  scripts/codex-pair.sh status               # session info + all panes"
      echo "  scripts/codex-pair.sh state [set '{...}']  # read/write workflow state"
      echo "  scripts/codex-pair.sh ledger [N]           # ledger entries"
      echo "  scripts/codex-pair.sh recovery             # recent interactions"
      echo "  scripts/codex-pair.sh close                # kill codex pane"
      exit 1
    fi
    ;;
esac

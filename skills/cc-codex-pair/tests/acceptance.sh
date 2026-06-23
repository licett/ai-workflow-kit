#!/usr/bin/env bash
# acceptance.sh — cc-codex-pair 验收测试 (hardened v2)
# 修复了首版 9 处 review findings：JSON 断言、threadId 一致性、随机 token、
# 真正的 124 超时、status/result 套超时、写作用域负向测试、隔离式清理、
# 自定位 SKILL_DIR + vendored 文件集校验、禁止处方式 tmux/acpx。
# 覆盖 AC1-AC6 + AC8 + AC10。用法: bash tests/acceptance.sh
set -uo pipefail

# AC10/P3: 从脚本自身位置推导 SKILL_DIR，不硬编码
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CXC="$SKILL_DIR/scripts/codex-companion.mjs"
SKILL_MD="$SKILL_DIR/SKILL.md"
PER_TASK_TIMEOUT=180
RUN="ACC-$$-${RANDOM}${RANDOM}"          # P1b: 每轮随机 token，杜绝旧线程假通过

# P2: 把全部 companion state 隔离到测试私有目录 → 清理只动自己，绝不全局 pkill
WORK="$(mktemp -d "${TMPDIR:-/tmp}/cxc_acc.XXXXXX")"
export CLAUDE_PLUGIN_DATA="$WORK/.data"; mkdir -p "$CLAUDE_PLUGIN_DATA"

PASS=0; FAIL=0; declare -a RESULTS
ok(){  echo "  ✅ PASS: $1"; PASS=$((PASS+1)); RESULTS+=("PASS  $1"); }
bad(){ echo "  ❌ FAIL: $1"; FAIL=$((FAIL+1)); RESULTS+=("FAIL  $1"); }
hr(){  echo "------------------------------------------------------------"; }

# JSON 取值: jget <dotted.path> ，从 stdin 读
jget(){ node -e 'const fs=require("fs");let o;try{o=JSON.parse(fs.readFileSync(0,"utf8"))}catch(e){process.exit(3)}let v=o;for(const k of process.argv[1].split(".")){if(v==null){v=undefined;break}v=v[k]}if(v==null)process.exit(1);process.stdout.write(typeof v==="object"?JSON.stringify(v):String(v))' "$1"; }

# P2: 真正会返回 124 的超时（macOS 无 timeout/gtimeout 时用 flag-file，不靠 perl alarm 误判）
TO=""; command -v timeout >/dev/null 2>&1 && TO="timeout"
[ -z "$TO" ] && command -v gtimeout >/dev/null 2>&1 && TO="gtimeout"
run_to(){ local secs="$1"; shift
  if [ -n "$TO" ]; then "$TO" "$secs" "$@"; return $?; fi
  local fired="$WORK/.to.$$.$RANDOM"
  "$@" & local pid=$!
  ( sleep "$secs"; kill -0 "$pid" 2>/dev/null && { : >"$fired"; kill -TERM "$pid" 2>/dev/null; sleep 2; kill -KILL "$pid" 2>/dev/null; }; ) & local w=$!
  wait "$pid" 2>/dev/null; local rc=$?
  kill "$w" 2>/dev/null; wait "$w" 2>/dev/null
  if [ -f "$fired" ]; then rm -f "$fired"; return 124; fi
  return "$rc"; }

cleanup(){  # P2: 只杀本测试隔离目录下的 broker（按 broker.json 里的 pid），不全局 pkill
  local bj p
  for bj in "$CLAUDE_PLUGIN_DATA"/state/*/broker.json; do
    [ -f "$bj" ] || continue; p=$(jget pid <"$bj" 2>/dev/null) && [ -n "$p" ] && kill -9 "$p" 2>/dev/null
  done
  rm -rf "$WORK" 2>/dev/null; }
trap cleanup EXIT
cd "$WORK"; git init -q 2>/dev/null

echo "cc-codex-pair 验收 (hardened) | skill=$SKILL_DIR"; echo "run-token=$RUN | isolated state=$CLAUDE_PLUGIN_DATA"; hr

# ── AC10: vendored 文件集完整（含易漏的 plugin.json） ────────────────
echo "[AC10] vendored 文件集 + PROVENANCE"
MISS=0
for f in scripts/codex-companion.mjs scripts/app-server-broker.mjs scripts/lib/app-server.mjs \
         scripts/lib/codex.mjs scripts/lib/state.mjs .claude-plugin/plugin.json \
         skills-ref/gpt-5-4-prompting/references/prompt-blocks.md PROVENANCE.md; do
  [ -f "$SKILL_DIR/$f" ] || { echo "    缺: $f"; MISS=$((MISS+1)); }
done
[ "$MISS" -eq 0 ] && ok "AC10 vendored 文件集完整" || bad "AC10 缺 $MISS 个文件"

# ── AC4: SKILL.md 无处方式脆弱传输（含 bare tmux/acpx 命令形，排除负向声明行） ──
echo "[AC4] SKILL.md 无处方式脆弱传输"
BANNED='codex-pair\.sh|capture-pane|paste-buffer|tmux-bridge|done-watcher|load-buffer|\bsmux\b|\bprewarm\b|esc to interrupt|tmux (split|send|capture|paste|new-window|kill)|(^| )acpx '
AC4HITS=$(grep -nE "$BANNED" "$SKILL_MD" | grep -vE "❌|NEVER|严禁|无需|不需要|不再有|没有|no tmux|NO tmux" || true)
[ -z "$AC4HITS" ] && ok "AC4 无处方式脆弱机械" || bad "AC4 残留: $AC4HITS"

# ── AC8: 旧 wrapper=0 且各 Phase 有 companion 调用 ───────────────────
echo "[AC8] 传输全迁移"
OLD=$(grep -cE "codex-pair\.sh" "$SKILL_MD"); CALLS=$(grep -cE 'node "\$CXC" task' "$SKILL_MD")
[ "$OLD" -eq 0 ] && ok "AC8 旧 codex-pair.sh=0" || bad "AC8 残留 codex-pair.sh ×$OLD"
[ "$CALLS" -ge 7 ] && ok "AC8 companion task 调用 ×$CALLS" || bad "AC8 companion 调用过少 ×$CALLS"
hr

# ── AC12: 指引层防 footgun（2026-06-14 第2轮实战：status→grep 渲染文本误判完成） ──
# Q2 教训：验收只测机制、没测"跟随 skill 的 agent 会被引向什么写法"。本门槛静态审计指引层本身。
echo "[AC12] 指引层：完成判定只认结构化状态，不诱导 grep 渲染文本"
# 12a 反 footgun：不得有"把 status 输出管道进 grep 判完成"的处方示例（排除 ❌/死法/反例 警示行）
FOOTGUN=$(grep -nE 'status[^|]*\|[^|]*grep|grep[^|]*\$CXC.*status' "$SKILL_MD" \
          | grep -iE "complet|done|cancel|finish|running" \
          | grep -vE "❌|死法|反例|NEVER|严禁|绝不|勿|不要|不得" || true)
[ -z "$FOOTGUN" ] && ok "AC12a 无 'status→grep 渲染判完成' 处方" || bad "AC12a footgun 处方残留: $FOOTGUN"
# 12b 完成判定铁律在位（结构化字段 + 明确禁止 grep 渲染）
if grep -qE "完成判定|只认.*JSON|\.job\.status" "$SKILL_MD" && grep -qE "严禁.*grep.*渲染|绝不.*渲染文本|不要 grep 渲染" "$SKILL_MD"; then
  ok "AC12b 完成判定铁律(读 .job.status + 禁 grep 渲染) 在位"
else bad "AC12b 缺完成判定铁律"; fi
# 12c 无 grep 的安全主路径已记载
grep -qE "status .*--wait --json" "$SKILL_MD" && ok "AC12c 安全主路径 status --wait --json 已记载" || bad "AC12c 缺 --wait --json 主路径"
# 12d result 取输出也走结构化字段（不诱导 grep 渲染块）
grep -qE "storedJob\.result\.rawOutput" "$SKILL_MD" && ok "AC12d result 走 .storedJob.result.rawOutput" || bad "AC12d result 未指明结构化取值"
hr

# ── AC1 + AC6: 单轮往返(JSON 断言) + 真有界 ───────────────────────────
echo "[AC1/AC6] task --fresh --json 单轮往返 (seed token)"
TOK1="$RUN-A"
run_to "$PER_TASK_TIMEOUT" node "$CXC" task --fresh --json "Remember token $TOK1. Do not read files or run commands. Reply exactly: ACK $TOK1" >a.json 2>>"$WORK/codex.log"; RC=$?
TID1=$(jget threadId <a.json 2>/dev/null); ST=$(jget status <a.json 2>/dev/null); RAW=$(jget rawOutput <a.json 2>/dev/null)
echo "    status=$ST threadId=$TID1 rawOutput=$RAW"
if   [ "$RC" -eq 124 ]; then bad "AC6 fresh 超时(${PER_TASK_TIMEOUT}s)=卡死";
elif [ "$RC" -ne 0 ];   then bad "AC1 fresh node 退出码 $RC (见 codex.log)";
elif [ "$ST" = "0" ] && [ -n "$TID1" ] && echo "$RAW" | grep -q "$TOK1"; then
     ok "AC1 单轮往返 (status=0, rawOutput 含 token, threadId 非空)"; ok "AC6 fresh 界内完成";
else bad "AC1 断言失败 status=$ST tid=$TID1 raw=$RAW"; fi
hr

# ── AC2: 线程持久 — 3 次 resume 必须 threadId 一致 且 召回随机 token ──
echo "[AC2] --resume-last 同 threadId + 召回 3/3"
AC2OK=0
for i in 1 2 3; do
  run_to "$PER_TASK_TIMEOUT" node "$CXC" task --resume-last --json "What token did I ask you to remember? Reply with exactly that token only. Do not read files." >"r$i.json" 2>>"$WORK/codex.log"; rc=$?
  tid=$(jget threadId <"r$i.json" 2>/dev/null); raw=$(jget rawOutput <"r$i.json" 2>/dev/null)
  if   [ "$rc" -eq 124 ]; then echo "    recall#$i ❌ 超时";
  elif [ "$tid" = "$TID1" ] && echo "$raw" | grep -q "$TOK1"; then echo "    recall#$i ✅ 同线程 $tid + 召回"; AC2OK=$((AC2OK+1));
  else echo "    recall#$i ❌ tid=$tid(期望$TID1) raw=$raw"; fi
done
[ "$AC2OK" -eq 3 ] && ok "AC2 线程持久 3/3 (threadId 一致 + 随机 token 召回)" || bad "AC2 仅 $AC2OK/3"
hr

# ── AC3: 后台 → status/result 全 JSON 断言，failed/cancelled 判失败 ──
echo "[AC3] task --background → status(--json) → result(--json)"
TOK3="$RUN-BG"
run_to 40 node "$CXC" task --background --resume-last --json "Reply exactly: $TOK3. Do not read files." >bg.json 2>>"$WORK/codex.log"
JOB=$(jget jobId <bg.json 2>/dev/null)
if [ -z "$JOB" ]; then bad "AC3 未返回 jobId";
else
  ok "AC3 后台返回 jobId=$JOB"
  st=""
  for t in $(seq 1 40); do
    run_to 20 node "$CXC" status "$JOB" --json >st.json 2>>"$WORK/codex.log"
    st=$(jget job.status <st.json 2>/dev/null)
    case "$st" in completed|failed|cancelled|error) break;; esac
    sleep 3
  done
  if [ "$st" != "completed" ]; then bad "AC3 job 终态=$st (非 completed → 判失败，不再当 done)";
  else
    run_to 20 node "$CXC" result "$JOB" --json >rs.json 2>>"$WORK/codex.log"
    rraw=$(jget storedJob.result.rawOutput <rs.json 2>/dev/null); rst=$(jget job.status <rs.json 2>/dev/null)
    if [ "$rst" = "completed" ] && echo "$rraw" | grep -q "$TOK3"; then ok "AC3 result rawOutput 含期望 (status=completed)";
    else bad "AC3 result 断言失败 status=$rst raw=$rraw"; fi
  fi
fi
hr

# ── AC5: write 正向 + 两条负向(只读默认不写 / --write 不越界) ──────────
echo "[AC5] --write 写模式 + 负向安全"
SCRATCH="$WORK/scratch"; mkdir -p "$SCRATCH"; ( cd "$SCRATCH" && git init -q )
# 5a 正向
( cd "$SCRATCH" && run_to "$PER_TASK_TIMEOUT" node "$CXC" task --fresh --write --json "Create a file named acc_touch.txt containing exactly the text WRITE-OK. Then report which files you touched." >"$WORK/w.json" 2>>"$WORK/codex.log" )
if [ -f "$SCRATCH/acc_touch.txt" ] && grep -q "WRITE-OK" "$SCRATCH/acc_touch.txt"; then ok "AC5a write 创建文件且内容正确";
else bad "AC5a write 未产生预期文件 (内容: $(cat "$SCRATCH/acc_touch.txt" 2>/dev/null || echo 缺失))"; fi
# 5b 负向：不带 --write 默认只读，绝不应写文件
( cd "$SCRATCH" && run_to "$PER_TASK_TIMEOUT" node "$CXC" task --fresh --json "Create a file named SHOULD_NOT_EXIST.txt containing X. Do it now." >"$WORK/ro.json" 2>>"$WORK/codex.log" )
if [ -f "$SCRATCH/SHOULD_NOT_EXIST.txt" ]; then bad "AC5b 只读默认竟写了文件 (sandbox 失效)"; else ok "AC5b 不带 --write 默认只读，未写文件"; fi
# 5c 负向：--write 不应越界写到 workspace 之外
( cd "$SCRATCH" && run_to "$PER_TASK_TIMEOUT" node "$CXC" task --fresh --write --json "Create a file at ../escape_acc.txt (one level above the workspace) containing ESC. If you cannot write outside the workspace, just say so." >"$WORK/esc.json" 2>>"$WORK/codex.log" )
if [ -f "$WORK/escape_acc.txt" ]; then bad "AC5c --write 越界写到 workspace 之外"; else ok "AC5c --write 未越界 (workspace 受限)"; fi
hr

# ── AC11: 后台结果持久化 & 可重取（长任务"漏读"兜底，scriptable 部分） ──
# 注：harness task-notification 的"真 push"是 Claude Code harness 行为，bash 无法观测，
#     须在会话内 live 验证（见验收报告）。本用例验证可脚本化的兜底：结果落盘、可重复取、不消费。
echo "[AC11] 后台结果持久化 + 可重复取（漏读不丢）"
TOK11="$RUN-DUR"
run_to 40 node "$CXC" task --background --resume-last --json "Reply exactly: $TOK11. Do not read files." >bg2.json 2>>"$WORK/codex.log"
JOB2=$(jget jobId <bg2.json 2>/dev/null)
if [ -z "$JOB2" ]; then bad "AC11 未返回 jobId";
else
  st=""
  for t in $(seq 1 40); do
    run_to 20 node "$CXC" status "$JOB2" --json >s2.json 2>>"$WORK/codex.log"
    st=$(jget job.status <s2.json 2>/dev/null)
    case "$st" in completed|failed|cancelled|error) break;; esac; sleep 3
  done
  if [ "$st" != "completed" ]; then bad "AC11 job 终态=$st";
  else
    # 模拟"CC 当时没取，过后才回来取" → 取两次证明持久且可重复读（非消费式）
    sleep 2
    run_to 20 node "$CXC" result "$JOB2" --json >r2a.json 2>>"$WORK/codex.log"; r1=$(jget storedJob.result.rawOutput <r2a.json 2>/dev/null)
    run_to 20 node "$CXC" result "$JOB2" --json >r2b.json 2>>"$WORK/codex.log"; r2=$(jget storedJob.result.rawOutput <r2b.json 2>/dev/null)
    if echo "$r1" | grep -q "$TOK11" && echo "$r2" | grep -q "$TOK11"; then ok "AC11 结果落盘+可重复取（漏读也不丢，两次取均含期望）";
    else bad "AC11 重取失败 r1=$r1 r2=$r2"; fi
  fi
fi
hr

# ── 汇总 ─────────────────────────────────────────────────────────────
echo "验收汇总:"; for r in "${RESULTS[@]}"; do echo "  $r"; done; hr
echo "PASS=$PASS  FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && { echo "🎉 全部硬门槛通过"; exit 0; } || { echo "⛔ 有失败项"; exit 1; }

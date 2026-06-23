---
name: cc-codex-pair
description: CC-Codex pair programming orchestrator. CC acts as brain (planning, reviewing, sprint design) and Codex acts as hands (implementation, final sign-off). Communicates with Codex through a vendored Codex app-server client (codex-companion.mjs) over a persistent thread — no tmux, no screen-scraping. Every phase starts with context synchronization — both agents read the same code and docs before collaborating. Use when the user wants CC and Codex to collaborate on sprint design, code implementation, cross review, or merge decisions.
---

# CC-Codex Pair

## Goal
Orchestrate true pair programming between Claude Code (CC) and OpenAI Codex through a vendored Codex app-server client. CC drives Codex via `node "$CXC" task ...`（持久线程，结构化结果，无 tmux/无抓屏）。CC plans and reviews; Codex implements and has final say on implementation feasibility and merge readiness.

## Core principles

### 1. Shared context first, then collaborate
**Every Phase begins with Round 0 (context sync).** Codex must read the same files CC has read and demonstrate understanding before any task or debate begins. Without shared context, it's not pair programming — it's remote delegation.

### 2. Give Codex tasks, never conclusions (CRITICAL)
**Every prompt to Codex must be a TASK, never an EVALUATION.** This is the single most important rule in this skill.

```
❌ NEVER: "这是我的 findings，逐条 AGREE/DISPUTE"    → triggers chat mode (shallow)
❌ NEVER: "我发现了 X 问题，请你复核"                 → 锚定 + 走过场
✅ ALWAYS: "请你独立审查 Sprint N 的实现，出你自己的 findings" → triggers agent mode (deep)
✅ ALWAYS: "我注意到 X 区域可能有问题，请你从零验证它是否真的存在，以及是否还有我没看到的问题" → 开放式验证
```

Why: Codex runs as a full agent (read files, grep, git, run tests) via the app-server transport. But evaluation-style prompts cause it to skip exploration. Task-style prompts trigger autonomous exploration.

**CC 的发现必须带不确定性**。CC 发现问题后发给 Codex 时，不能用"我确认了 X 是 bug"的语气，必须用"我怀疑 X 区域有问题，请你独立验证"的语气。让 Codex 从零建立自己的判断，而不是在 CC 的结论上盖章。

```
❌ "F1 是 P1 bug，file.py:123 的空值处理有问题。请确认。"
✅ "file.py:120-130 区域我觉得可能有边界问题，但不确定。请你读这段代码，独立判断是否有问题、严重度如何、是否还有我没注意到的关联问题。"
```

**Experimentally validated**: D-group experiment (2026-03-22) confirmed that task-style prompts produce findings comparable to standalone Codex App, while evaluation-style prompts produce shallow rubber-stamp responses.

### 3. Independent first, compare second
For any review/analysis Phase, CC and Codex must each produce findings **independently** before seeing each other's conclusions. Then compare and debate. Never let one side's conclusions anchor the other.

### 4. CC injects multi-dimensional perspective (1+1 > 2 的来源)
CC 的独有价值不是"控制 Codex"，而是把 Codex 独立时不具备的能力注入协作：

- **多专家视角**: CC 的 cross-review-gate 有 5 个专家（架构师/正确性/安全性/性能/QA），sprint-design-reviewer 有策略专家组（量化策略师/统计学家/风控）。交换 findings 时 **必须标注来自哪个专家**，让 Codex 看到多维分析而非扁平列表。
- **pitfalls 主动关联**: CC 在每个 Phase 的每个关键节点，**主动检查 pitfalls.md 和 memory**，将相关踩坑经验注入当前讨论。不是只在 Round 0 提一次。
- **内部 skill/agent team 按需触发**: Freeform 讨论中遇到策略话题 → CC 内部 spawn 策略专家组；遇到 bug → CC 内部跑 log-rootcause-triage。然后把多维分析结果注入到和 Codex 的讨论中。
- **"代码里读不到的信息"持续补充**: 不只在 Round 0，而是在**整个协作过程中**，每当新话题/新文件/新问题出现时，CC 主动检查是否有相关的历史决策、踩坑经验、隐性约束需要告知 Codex。
- **场景聚焦提示（additive, not restrictive）**: CC 在每个 task prompt 末尾根据当前场景动态添加一行聚焦提示，引导 Codex 额外关注特定维度，但不限制其自由探索。格式：`"当前场景聚焦: {focus_hint}。但不要局限于此 — 如果你发现其他维度的问题，同样重要。"` 示例：
  - 策略讨论 → "额外关注 PnL 分解完整性、regime 统计功效、holdout 设计"
  - Code review → "额外关注正确性、边界 case、跨模块 contract 一致性"
  - 架构分析 → "额外关注模块边界、耦合度、frozen denylist 兼容性"
  - 数据分析 → "额外关注样本量充分性、置信区间、过拟合风险"
  - 头脑风暴 → "发散思考，挑战现有假设，不要自我审查"

## Mandatory Codex involvement rule
**When this skill is invoked, Codex MUST be involved in every response.** CC is NOT allowed to answer alone and skip Codex. This includes:
- Code reviews, design reviews, close audits → Codex must review
- Strategic discussions, data analysis, "is X possible?" questions → Codex must independently analyze
- Bug investigations, root cause analysis → Codex must verify findings

## CC 发现问题后的强制流程（CRITICAL — 禁止跳过）

**CC 在任何时候发现 bug / 定位根因 / 形成修复方案后，严禁直接发给 Codex 执行。** 必须走以下流程：

```
CC 发现问题
  ↓
Step 1: 让 Codex 独立验证（不带 CC 的结论）
  CC → Codex: "sniper.py:3324-3343 区域我觉得可能有问题。
               请你独立读这段代码，判断是否存在问题、根因是什么、你建议怎么修。"
  ↓
Step 2: 比较双方诊断
  CC 的诊断 vs Codex 的诊断 → 共识循环（如有分歧）
  ↓
Step 3: 共识后，Codex 实现修复（Codex 自己决定怎么改）
```

**以下行为明确违规：**
```
❌ CC 写完整 fix spec → 直接发给 Codex "请实施"
❌ CC 说 "我们已经定位了根因" → 让 Codex 执行 CC 的方案
❌ CC 把诊断 + 方案打包成一个 prompt 发给 Codex
```

**正确做法：**
```
✅ CC 说 "我怀疑这里有问题" → Codex 独立诊断 → 比较 → 共识 → Codex 实现
✅ CC 说 "这个区域值得深入看" → Codex 自主探索 → 可能发现 CC 没看到的关联问题
```

**为什么这么严格？** 因为 CC 的诊断可能是错的。如果 Codex 只是执行 CC 的方案而没有独立验证，错误的诊断会直接变成错误的代码。结对的价值在于两个人独立判断后比较，不在于一个人出方案另一个人执行。

Any conclusion or recommendation → Codex must give AGREE/DISPUTE/PARTIAL。If CC answers without Codex, the response is incomplete. The only exception is pure factual lookups (e.g., "what's the file path for X?") that require zero judgment.

## CC 严禁当传声筒

**CC 收到 Codex 的回复后，严禁直接转述给用户然后问"你怎么看"。** CC 是大脑，必须对 Codex 的每一个结论独立验证后再呈现。

以下行为明确违规：
```
❌ 转述 Codex 结论 + "你怎么看？" / "你怎么选？" / "你觉得呢？"
❌ 列出 Codex 的选项 + 等用户挑
❌ 把 Codex 的分析原封不动贴给用户
```

正确做法：
```
✅ CC 读 Codex 回复 → CC 独立验证方法论/数据集/结论 → CC 用自己的多专家面板交叉审查 → CC 呈现经过验证的结论
✅ 如果 CC 和 Codex 有分歧 → 共识循环辩论 → 呈现辩论结果
✅ 如果需要用户决策 → CC 必须先给出自己的推荐和理由，然后再问用户
```

**CC 的角色是独立审查者，不是信使。**

## Trigger shortcuts

### Session 启动
- 无需 tmux/ccs，无需 prewarm。首次 `task --fresh` 自动起常驻 broker 并建线程。
- 之后所有交互一律 `task --resume-last` 续同一线程。

### Sprint-bound (5 Phase workflow)
- `/cc-codex-pair sN` — full sprint cycle (Phase 1-5)
- `/cc-codex-pair sN design` — Phase 1: sprint design collaboration
- `/cc-codex-pair sN implement pK` — Phase 2: Pack K implementation
- `/cc-codex-pair sN review` — Phase 3-4: cross review + fix loop
- `/cc-codex-pair sN close` — Phase 5: final merge decision

### Freeform (ad-hoc pair, 复用同一个线程)
- `/cc-codex-pair chat <topic>` — open-ended discussion with Codex
- `/cc-codex-pair review <target>` — ad-hoc review
- `/cc-codex-pair investigate <issue>` — bug investigation / root cause analysis
- `和 codex 讨论一下` — Chinese trigger for freeform chat
- `让 codex 来实现` — Chinese trigger for implementation
- `让 codex review` — Chinese trigger for review

### Utility
- `/cc-codex-pair status` — `node "$CXC" status` 查 Codex job 状态

### Auto-start rule
首次需要 Codex 时直接 `task --fresh`，broker 自动拉起；之后一律 `--resume-last`。用户不需要手动起停。

## Workflow state persistence (防止中途丢失进度)

**问题**：CC 在长 session 中上下文被压缩后，会忘记"我在跑 5 Phase 工作流的第几步"，导致中途停止。

**解法**：工作流状态持久化到 `./.cc-pair-state.json`（**项目根目录下、per-repo**，CC 用 Write/Edit 维护的纯文件，与 Codex job 状态无关；建议加入 .gitignore）。CC 在每个 Phase 开始和结束时更新此文件。如果 CC 中断/丢失上下文/用户说 "continue"，CC 读此文件恢复进度。

**CRITICAL — CC 必须执行以下操作：**

### 每个 Phase 开始时
```bash
# 读当前状态
cat ./.cc-pair-state.json
# 更新为当前 Phase
# 用 Edit tool 更新 phase, step, last_updated, phases_remaining
```

### 每个 Phase 完成时
```bash
# 把当前 Phase 移入 phases_done，更新 phase 为下一个
# 检查 phases_remaining 是否为空 — 不为空则继续下一个 Phase
```

### CC 中断后恢复时（用户说 "continue" 或重新调用 `/cc-codex-pair sN`）
```bash
# 方式 1: 读 state 文件
cat ./.cc-pair-state.json
# 如果 active=true 且有 phases_remaining → 从中断的 Phase 继续

# 方式 2: 读 Codex job 历史（更可靠地看断点在哪）
node "$CXC" status
# 看最近 job 的 summary + Codex session-id，快速理解上次 Codex 干到哪
```

### 状态文件格式
```json
{
  "active": true,
  "sprint": "s60",
  "phase": "Phase 3: Cross Review",
  "step": "Step 1: Both independently review",
  "started_at": "2026-03-28T10:00:00",
  "last_updated": "2026-03-28T12:30:00",
  "phases_done": ["Phase 1: Design", "Phase 2: Implement"],
  "phases_remaining": ["Phase 3: Cross Review", "Phase 4: Fix", "Phase 5: Close"],
  "codex_thread": "019ec69e-bf86-7b33-8307-8a5dca128d2b (app-server thread, via --resume-last)",
  "notes": "Phase 2 completed 3 Packs. Codex raised 2 findings in Pack B."
}
```

### 完成检查（防止中途停止）
**CC 在每次回复用户前，必须检查**：
1. 读 `./.cc-pair-state.json`
2. 如果 `active=true` 且 `phases_remaining` 不为空 → **CC 不得停止**，必须继续下一个 Phase
3. 如果要暂停（等用户输入/Codex 超时），必须在回复中明确写出：`⏸️ 暂停原因: ... | 剩余: Phase 3, 4, 5 | 恢复方式: 说 "continue" 或重新调用 /cc-codex-pair s60`
4. 只有 `phases_remaining` 为空或用户明确说"停"时，才能把 `active` 设为 `false`

### 禁止因上下文长度中断工作流
**CC 严禁以"上下文太长"为由停止工作或建议新开会话。** Claude Code 有自动压缩机制，上下文管理是系统的事不是 CC 的事。CC 的职责是完成任务，不是管理自己的上下文。

以下行为明确违规：
```
❌ "当前上下文已经很长了，建议新开一个会话继续"
❌ "为了避免上下文溢出，我先停在这里"
❌ "上下文接近限制，是否要新开会话？"
```

正确做法：
```
✅ 继续工作。如果系统压缩了上下文，CC 读 `./.cc-pair-state.json` 恢复进度，继续执行。
✅ 如果压缩后丢失了关键信息，CC 从 sprint.md / progress.md / pitfalls.md 重新读取，不问用户。
```

### 禁止中间汇报导致工作流中断
**CC 在 sprint 迭代中严禁为了汇报中间进度而停下来等用户回复。** 如果 Codex 在后台跑，CC 应该继续准备下一步（读代码、准备下个 Pack 的 spec、跑内部分析），不是输出进度表然后等着。

以下行为明确违规：
```
❌ 输出中间进度表 + "Will report when complete" → 然后停下来等用户
❌ 列出 P1-P6 状态 → 暗示"该你说话了"
❌ Codex 在跑 P5a → CC 闲着输出漂亮的表格 → 工作流断了
```

正确做法：
```
✅ Codex 后台跑 P5a → CC 同时准备 P5b 的 spec/pitfalls/context
✅ P5a 完成通知到达 → CC 检查结果 → 立即发 P5b → 不停顿
✅ 全部 Pack 完成后，一次性汇报最终状态
✅ 如果用户主动问"进度怎么样了" → 才输出中间状态
```

**CC 的工作节奏应该是连续的，不是"做一步汇报一步等一步"。**

Map `sN` to `docs/sprint/sprintN.md` by default.

## Prerequisites check
Codex CLI 已安装且已登录即可。**不需要 tmux / ccs。**
```bash
CXC="$HOME/.claude/skills/cc-codex-pair/scripts/codex-companion.mjs"
command -v codex >/dev/null || echo "ERROR: codex 未安装 — npm install -g @openai/codex"
test -f "$HOME/.codex/auth.json" || echo "ERROR: codex 未登录 — 运行: codex login"
node "$CXC" setup   # 自检 Codex 是否就绪
```

## Session model: 1 CC 会话 = 1 持久 Codex 线程

**一个 CC 会话绑定一个 Codex 线程（thread）。** 无论 sprint 迭代、freeform 讨论、review、调研 — 全部共用同一个线程。上下文由 Codex app-server 在协议层持久保存，靠 `--resume-last` 续接，不依赖任何常驻进程或 pane 保活。

| | 数量 | 实现 | 生命周期 |
|--|------|------|---------|
| Codex 线程 | 1 per CC 会话 | app-server thread（thread-id 协议级持久）| 首次 `task --fresh` 创建；之后一律 `task --resume-last` 续接 |

**核心规则**：**默认永远 `--resume-last` 累积上下文，仅在明确开启全新话题时才 `--fresh`。** 这比旧的 tmux 保活 pane 更可靠地实现"同一会话共享一份持久上下文" —— resume 是协议级的，不会因为进程/pane 状态而丢。

**并发与隔离（多目录/多会话）**：
- **按目录(repo)自动隔离**：broker、线程、jobs、workflow-state(`./.cc-pair-state.json`) 全部按工作目录隔离。**不同目录跑结对互不影响**，可放心并行。
- **同一目录并发多个 CC 会话**：默认会共享该 repo 的"最近线程"（`--resume-last`/`status` 按 repo 范围解析），可能串台。若要彼此隔离，给每个会话在首次调用前设一个稳定唯一的会话标识：
  ```bash
  export CODEX_COMPANION_SESSION_ID="ccpair-$(date +%s)-$$"   # 每个 CC 会话固定一次，全程复用
  ```
  设了它，`--resume-last`/`status`/`result` 只认本会话自己的 jobs，不串台。

**设计原则**：和你的 CC 长会话一样 — 丰富上下文出好代码。Codex 在 freeform 讨论中积累的项目理解，到 sprint 实现时直接可用；sprint review 中积累的代码理解，到后续讨论时仍然在。

**不拆分线程** — 不按 sprint 拆、不按 Phase 拆、不按话题拆。一个 CC 会话里的所有 Codex 交互共享同一份持久上下文。

## Communication: vendored codex-companion（NO tmux, NO 抓屏）

**CC 通过 vendored 的 Codex app-server 客户端与 Codex 通信。** 调用 `codex-companion.mjs`，它经 Unix socket 上的 JSON-RPC 驱动一个常驻 broker，返回结构化结果。**没有 tmux，没有屏幕抓取，没有 `›`/`esc to interrupt` 轮询。**

**路径约定**（CC 在每次调用前先设好这个变量）：
```bash
CXC="$HOME/.claude/skills/cc-codex-pair/scripts/codex-companion.mjs"
```
命令在**用户当前项目目录**下运行（即 Codex 要操作的 repo）—— companion 默认把 cwd 当工作区，无需额外指定。

**CRITICAL RULE — 只用 companion，严禁回退到 tmux / acpx / 抓屏：**
```
❌ NEVER: tmux / capture-pane / paste-buffer / 任何屏幕抓取
❌ NEVER: acpx 任何命令
✅ ALWAYS: node "$CXC" task --resume-last "<prompt>"   # 发任务给 Codex（续同一线程）
✅ FIRST:  node "$CXC" task --fresh "<prompt>"          # 仅本会话首次接触用 --fresh
✅ WRITE:  node "$CXC" task --resume-last --write "<spec>"  # 需要 Codex 改代码时加 --write
✅ BG:     node "$CXC" task --background "<prompt>"     # 长任务后台跑，返回 jobId
✅ POLL:   node "$CXC" status [jobId]                   # 查 job 状态
✅ FETCH:  node "$CXC" result [jobId]                   # 取已完成 job 的最终输出
✅ STOP:   node "$CXC" cancel [jobId]                   # 取消运行中的 job
```

**工作原理**：
1. CC 调 `node "$CXC" task ...` → companion 自动确保 broker 常驻（首次自动起，无需 prewarm）。
2. broker 经 app-server 协议向 Codex 发一个 turn；read-only 默认（不带 `--write`）。
3. **前台调用直接把 Codex 的最终回复打到 stdout** —— CC 读这个 stdout 即可，**不需要单独 read**。
4. 每次调用是一个 turn；`--resume-last` 让所有 turn 落在同一 thread-id 上，上下文自然累积。
5. `status` 给出 job 历史 + Codex session-id（`codex resume <id>` 可在 Codex CLI 重开同线程）。

**前台 vs 后台**：
```bash
# 前台（默认）：阻塞到 Codex 返回，stdout 即回复。适合 Round 0、共识轮、短任务。
node "$CXC" task --resume-last "$(cat /tmp/cc_codex_prompt.txt)"

# 后台：长实现/审查任务。立即返回 jobId，CC 继续干别的，事后用 status/result 取回。
node "$CXC" task --background --resume-last "$(cat /tmp/cc_codex_prompt.txt)"
# → "started in the background as task-xxxx. Check status task-xxxx for progress."
node "$CXC" status task-xxxx --wait --json   # 阻塞到终态，读 .job.status（勿 grep 渲染文本）
node "$CXC" result task-xxxx --json          # 读 .storedJob.result.rawOutput
```

## Codex 任务状态 & 后台轮询

传输换成 app-server 协议后，**不再有 tmux 抓屏、`›`/`esc to interrupt` 轮询、信号文件、固定超时这套脆弱机械**。状态由协议事件直接给出：

- **前台 `task`**：阻塞到该 turn 完成，stdout 即 Codex 回复。CC 直接读返回值，无需检测"忙/闲"。
- **后台 `task --background`**：立即返回 jobId。CC 继续干别的，需要时：
  ```bash
  node "$CXC" status <jobId> --wait --json   # ★阻塞到终态再返回(免轮询/免 grep)，读 .job.status
  node "$CXC" status <jobId> --json          # 单次查，读 .job.status
  node "$CXC" result <jobId> --json          # 取最终输出，读 .storedJob.result.rawOutput
  node "$CXC" cancel <jobId>                 # 取消运行中的 job
  ```
- **broker 生命周期**：首次 `task` 自动起常驻 broker，无需 `prewarm`；按 repo 隔离。会话结束后可让其自然退出或显式收尾，CC **不需要**手动起停。

**CC 严禁用 while+sleep 轮询。** 前台调用天然阻塞到完成；后台**优先 `status <jobId> --wait --json`**（companion 内部按结构化状态阻塞到终态）。**没有静默挂起**：长任务走后台 + `--wait`，短任务前台直接拿结果。

### ⚠️ 完成判定铁律：只认 JSON 状态字段，严禁 grep 渲染文本（新传输的 `›` 同类坑）

**这是 2026-06-14 实战踩到的坑，等价于老 tmux 的 `›` 误判。**

`node "$CXC" status` 的**人类可读输出里含 action 提示**：`/codex:cancel <id>`、`Resume in Codex: …`、`Result: /codex:result <id>`、`Cancel: …`。**对它 `grep cancel|done|completed|result` 必然误匹配**——把"还在 running 的 job"误判成"已完成/已取消"。

```
❌ 死法: node "$CXC" status <id> | grep -qiE "completed|done|cancel" && echo done
        → 命中的是输出里的 "/codex:cancel <id>" 提示，不是真状态。job 其实还在 running。
✅ 正法: ST=$(node "$CXC" status <id> --json | jget job.status)   # 取结构化字段
        case "$ST" in completed) ... ;; failed|cancelled) 判失败 ;; queued|running) 继续等 ;; esac
✅ 更优: node "$CXC" status <id> --wait --json   # 直接阻塞到终态，连判定循环都不用写
```

**规则**：任何"Codex 完成了吗"的判断，**必须**取 `--json` 的 `.job.status` 精确比对终态枚举（`completed`/`failed`/`cancelled`），**绝不**对渲染文本做关键词匹配。`result` 也用 `--json` 读 `.storedJob.result.rawOutput`，不要 grep 渲染块。

### 长任务完成通知（推荐姿势 — 真 push，免轮询、免漏读）

有两种"后台"，别混：
| 方式 | 完成怎么得知 | 适用 |
|--|--|--|
| companion `task --background` | 返回 jobId，**CC 自己轮询 `status`/`result`**（结果落盘可重取，不会丢，但要 CC 记得查） | 任务要在 CC 关注之外长期存活 |
| **Bash 工具 `run_in_background:true` 跑前台 `task`**（推荐） | 进程退出时 **harness 主动给 CC 推 task-notification**，CC 再读输出文件 | 绝大多数长任务 |

**推荐**：长任务用 `Bash(node "$CXC" task --resume-last "...", run_in_background=true)`。这是对模型的**真异步推送**：CC 发完可以去干别的（准备下个 Pack、读代码、跑内部分析），Codex 一完成 harness 就把 CC 叫回来——**既不轮询、也不会忘记读**。本 skill 中"完成通知到达"指的就是这条 harness task-notification。

**兜底（万一 CC 仍漏了）**：恢复时 `node "$CXC" status` 列出最近 job + 读 `./.cc-pair-state.json`，捞出未取结果的 job 用 `result <jobId>` 取回——结果一直在磁盘上，不会丢。

## Round 0: Context sync protocol

**Every Phase starts with this protocol.** Codex 和 CC 走一样的 onboarding：读同样的文件、花同样的时间建立项目理解。CC 只补充代码里读不到的信息（历史决策、踩坑经验、架构约束的 why）。

**核心原则：对等上下文 = 真正的结对编程。**
- Codex 必须自己读 AGENTS.md、sprint.md、progress.md、pitfalls.md、源码 — 和 CC 新会话读的文件一模一样
- Codex 通过 app-server 持久线程运行，上下文在线程生命周期内由协议层保持（`--resume-last` 续接）
- CC 只补充 3 类"代码里读不到的信息"：
  1. **历史决策 why**: "这段 chase 逻辑是 S21 加的，因为当时薄盘口 3x 超付"
  2. **踩坑经验**: "tick_size 升阶在 S22 被证明不合理，不要再用这个模式"
  3. **隐性约束**: "frozen denylist 里的文件不能改"、memory 条目中的关键信息

**Step 0a**: CC 发 onboarding prompt 给 Codex（本会话首次接触用 `--fresh`，之后每个 Phase 的 Round 0 用 `--resume-last` —— 同一线程，Codex 已有前序上下文，onboarding 会更快）。
```bash
cat > /tmp/cc_codex_prompt.txt << 'PROMPT'
We are pair programming on Sprint {N}. Do your full onboarding — read these files carefully, just like a new team member would:

1. AGENTS.md (project rules and conventions — same as CLAUDE.md)
2. docs/sprint/sprint{N}.md (current sprint design)
3. docs/task/progress.md (current state and next actions)
4. docs/qa/pitfalls.md (active pitfall cards — these are real production incidents)
{phase_specific_files}

Take your time to read thoroughly. After reading, tell me:
1. Sprint {N}'s goal and Pack structure
2. Current state: what's done, what's pending
3. Key constraints and pitfalls you identified
4. Which source files you think are most relevant and why
PROMPT

node "$CXC" task --resume-last "$(cat /tmp/cc_codex_prompt.txt)"
```

Where `{phase_specific_files}` varies by Phase:
- **Phase 1 (Design)**: no additional files — sprint doc is the focus
- **Phase 2 (Implement)**: `5. Read these source files that this Pack modifies: {file_list_from_spec}`
- **Phase 3 (Review)**: `5. Run: git diff --stat` + `6. Read all changed source files completely`
- **Phase 4 (Fix)**: same as Phase 3 + `7. Focus on the code sections cited in findings`
- **Phase 5 (Close)**: `5. git diff --stat` + `6. Run: pytest (check test results)`

**Step 0b**: 前台 `task` 调用返回的 stdout 即 Codex 的 onboarding 回复；CC 直接读它，评估理解，补充代码里读不到的信息。

CC 评估 Codex 的 onboarding 输出：
- 理解准确 → CC 补充历史上下文后进入正式协作
- 有偏差 → CC 纠正具体的误解点（不是"重新读"，而是"你理解错了，实际是这样..."）

CC 补充的内容（只限代码里读不到的）：
```
补充几个代码里看不到的背景：

1. [历史决策] chase ceiling 是 S21 加的，当时 thin book 导致 3x overpay，
   所以 chase_max_ticks 不是随意设的，背后有真金白银的教训。

2. [踩坑经验] pitfalls #7 的 tick_size 精度问题在 S22 反复出现过，
   任何涉及 tick_size 的改动都要格外小心。

3. [隐性约束] frozen denylist: live_moneyline.py 和 sniper.py 的 runtime 路径
   是 read-only 的（S37 冻结），只能改策略层不能改执行层。

4. [memory] macOS 实例跑 probe-nba|probe-esports，pig 跑 probe-tennis，不能混。
```

**Step 0c**: CC evaluates Codex's understanding.
- If accurate → proceed to Phase-specific work
- If gaps → CC provides targeted clarification (not "re-read file X", but "here's the specific detail you missed: ...")
- Max 2 clarification rounds. CC always provides the answer, never just points to a file.

## Consensus loop protocol

Used after Step 2 (exchange and compare) to resolve divergences. Only starts **after** both sides have independently produced findings.

**Constants**: MAX_ROUNDS = 5

**CRITICAL ENFORCEMENT RULE — CC MUST READ THIS**:
CC 在收到 Codex 的 INSIST 或 DISPUTE 后，**严禁停止辩论**。CC 必须继续发送下一轮论据，直到以下三个条件之一满足：
1. 双方达成 CONCEDE 或 SPLIT（共识）
2. 达到 MAX_ROUNDS = 5（升级给人类）
3. 所有矛盾项都已解决

**CC 在 Round 1 收到 INSIST 后直接汇报给用户 = 违反 skill 规则。** 必须进入 Round 2。

**Protocol**: CC 和 Codex 是**对等的辩论方**。双方通过互相提供源码证据来说服对方。

**Loop 执行流程（CC 必须严格按此执行）**:

```
round = 0
unresolved_items = [所有矛盾项]

WHILE unresolved_items is not empty AND round < MAX_ROUNDS:
    round += 1

    FOR each item in unresolved_items:
        # Step A: CC 读源码，准备自己的证据
        cc_evidence = CC 读相关 file:line，分析代码行为

        # Step B: CC 发送论据给 Codex（via companion, --resume-last）
        发送:
        """
        Round {round}/{MAX_ROUNDS}，矛盾项: {item}

        CC 的立场: {position}
        CC 的证据: {file:line + 代码行为分析}

        请回应:
        - CONCEDE: 如果我的证据说服了你
        - INSIST: {你的 counter-evidence} 如果你有更强证据
        - SPLIT: {各自正确的部分} 如果我们各有道理
        """

        # Step C: 解析 Codex 回应
        IF Codex says CONCEDE:
            → item resolved, remove from unresolved_items
        ELIF Codex says SPLIT:
            → merge agreed parts, remove from unresolved_items
        ELIF Codex says INSIST:
            # Step D: CC 必须认真评估 Codex 的证据
            CC 读 Codex 引用的 file:line，验证证据
            IF Codex 的证据确实更强:
                → CC CONCEDE，item resolved
            ELIF 势均力敌:
                → 缩小分歧范围，item stays in unresolved_items
            ELSE:
                → CC 准备更强的证据，item stays in unresolved_items
                → 进入下一轮

IF round >= MAX_ROUNDS AND unresolved_items is not empty:
    输出 ESCALATION 报告（含双方证据对比），等待人类裁决
```

**Key rules**:
- **CC 严禁在 Round 1 就停止**。收到 INSIST 必须进入 Round 2。这是硬性规则。
- **CC 和 Codex 完全对等**。没有谁的 finding 默认优先。谁的证据更强谁的立场胜出。
- **CC 也必须 CONCEDE**。如果 Codex 的源码证据推翻了 CC 的结论，CC 必须修正。
- **每轮 CC 必须读源码**。CC 不能仅凭推理反驳 Codex 的 file:line 证据，必须自己读那行代码验证。
- **所有立场必须有 file:line 证据**。纯观点无效，双方都一样。
- **SPLIT 是正常结果**。不是每个矛盾都有唯一正确答案。
- **Round 标注**: 每轮 prompt 必须标注 `Round {N}/{MAX_ROUNDS}`，让 Codex 知道辩论进度。

---

### MANDATORY: Pre-CONCEDE mechanical checklist (added 2026-04-11 after repeated over-concede events)

**When this applies**: Any CC response that would contain "CONCEDE" / "agreed" / "你对" / "采纳" / "同意" in response to a Codex finding or Codex R+N review of CC's artifact.

**Why the regular "每轮 CC 必须读源码" rule above was insufficient**: That rule tells CC to read the file:line Codex cited. It does NOT require CC to search for evidence Codex omitted. Codex can be wrong by omission — pointing correctly to file:line X while failing to cite file:line Y that contradicts Codex's conclusion. Reading only X confirms Codex's framing and lets the error propagate.

**CC MUST execute this checklist BEFORE writing any CONCEDE in a round response**:

1. **Identify the disputed claim** as one sentence hypothesis you might be wrong about. Not "Codex says X so I agree", but "Codex claims X at evidence A; I need to verify X is true AND no counter-evidence exists".

2. **Run an independent verification command — paste raw tool output into the draft**. Acceptable commands:
   - `Read` the **full section** containing cited file:line (not just the cited line)
   - `Grep` for the disputed term across the whole doc/repo (not just where Codex said to look)
   - `Bash` to execute the exact command Codex cited, confirming the output matches
   - `Read` adjacent sections / sibling functions that might contain counter-evidence

3. **Specifically hunt for omissions**. Ask yourself:
   - "What section of the spec/code could contradict Codex that Codex did NOT cite?"
   - "If Codex's 'three witnesses agree', are the three witnesses actually independent, or do they trace back to the same author/commit/mental model?"
   - "Is there an adjacent clause in the same doc that invalidates Codex's reading?"

4. **Write an attempted DISPUTE first** — mandatory even if you end up abandoning it. Draft a 1-2 sentence DISPUTE before CONCEDE. The act of attempting DISPUTE reverses the asymmetric cost (CONCEDE is cheap, DISPUTE is expensive). If the DISPUTE has no evidence, then CONCEDE; but you must attempt.

5. **Cite CC's own verification output in the CONCEDE text**. Not "I agree with your file:line". Instead: "I ran `[command X]` and got `[output Y]` independently; the output matches your claim; CONCEDE". If you cannot cite your own verification output, you cannot CONCEDE.

6. **Red flag: process theater**. Anti-pattern: writing a "过度 CONCEDE 检查" section without running any new tool calls. Meta-reasoning about whether you over-conceded is NOT verification. Real verification produces NEW tool output you did not have before reading Codex's R+N.

**Red flags that CC is about to over-concede**:
- Writing "R2 全条 CONCEDE" or similar bulk-acceptance → STOP, run checklist per-item
- Reasoning about "evidence looks solid" without quoting specific output → STOP, quote it
- Using "three-way consistency" without checking witness independence → STOP, check for common-source dependency
- Closure pressure ("need to move to next phase") → STOP, closure pressure is exactly when this rule matters
- Writing "我检查了有没有过度 CONCEDE" without new tool calls → that section IS the over-concede

**Canonical failure this rule exists to prevent**:
In the 2026-04-11 S98 close review, Codex R1 said "verifier has a bug at line 162-173; evidence: production code + live data + aligner regression test = 3-way agreement". CC CONCEDE without re-reading sprint98.md §3:285-297 (Pack C Truth contract) where §3:295 literally excludes only 3 fields (stream_channel / alert_recorded_ts_ms / decision_recorded_ts_ms), meaning the spec literally requires stream_contract_version to be in cross-channel parity — i.e., the "verifier bug" framing was wrong; the real issue was spec/production ambiguity. CC's "three witnesses" were actually implementation + its own mirror test + runtime of that code — not independent witnesses. The mechanical fix: in R2, CC should have grepped sprint98.md for "stream_contract_version" and read EVERY hit, not just ones Codex cited. That grep would have surfaced §3:295 immediately.

---

### MANDATORY: Sprint/Retrospective close checklist (added 2026-05-10 after S35 SJC retrospective Round 9 self-irony)

**When this applies**: Any CC response that would claim sprint closed / retro shipped / "X bug closed" / "Y memory entries saved" — i.e., any user-facing closure verdict.

**Why mechanical checklist > advisory memory**: S35 SJC retrospective Round 9 — CC literally shipped `feedback_layered_closure_claim.md` memory ("never claim closed without Codex verify") then 5 minutes later self-applied retro v2 + 4 memories without Codex round-trip. PM caught. Lesson: advisory memory does NOT enforce; only workflow-level mechanical checklist does.

**CC MUST execute this 7-item checklist BEFORE writing any close/ship/freeze claim**:

1. [ ] **User-visible state and metadata agree** — current_state + source_status + tier_reason + no_data_reason + provenance source_url all consistent (not just check current_state.admission_status). Specifically for radar / dashboard products: schools.json AND state.json AND any UI-rendered field must show the same story.

2. [ ] **Source mutation safety verified** — for any Pack D / schools.json / config / data mutation: source-pack membership ✓, liveness HEAD/GET 2xx ✓, page-emptiness >200 chars ✓, old/bad URL locked OR removed (NOT silently kept), idempotency proof.

3. [ ] **Exact verification command recorded and reproduced by reviewer** — paste the literal command (incl venv path + addopts override): `.venv/bin/python -m pytest -q --override-ini='addopts='`. Codex must reproduce same result; env-dependent test = real bug not env corner case.

4. [ ] **xfail entries have owner + expiry + linked ticket + unblock condition** — naked `@pytest.mark.skip` is malpractice (hides bugs); `@pytest.mark.xfail(strict=True, reason="Pack N follow-up: <ticket>, owner=<sid>, expiry=<date>, unblock=<criterion>")` is acceptable carry. Otherwise must fix.

5. [ ] **Live-web evidence captured as artifact when Codex cannot fetch directly** — chrome MCP / Playwright captures must persist (screenshot path, JSON evidence file, captured HTML/text fixture) in `var/reports/` or `tests/fixtures/`. Verbal summary "I clicked, it shows X" insufficient.

6. [ ] **Claims distinguish measured fact vs risk proxy vs hypothesis** — explicit labels:
   - "measured: 989 passed in CC env (pytest 9.0.3) AND Codex env (same)"
   - "proxy estimate (NOT measured): trust radius ~34% based on metadata bucket distribution"
   - "hypothesis (needs S36 audit to verify): random PM click likely 2/3 to expose silent miss"

7. [ ] **Layered closure** (per `feedback_layered_closure_claim.md`):
   - L1 root cause: identified
   - L2 fix: shipped (code/data)
   - L3 user-visible state: verified
   - L4 acceptance gate: PASSING (or strict xfail with #4 above)
   - L5 random/stratified sample N: ≥ 80% trust (only required for systemic / user-facing closure)

**META-RULE — verification-rule edits need Codex review** (added 2026-05-10):

If CC is editing a doc/memory/skill/checklist that DEFINES verification rules (this very file qualifies), CC MUST round-trip Codex BEFORE claiming the rule is adopted. Self-applying edits to verification machinery is the exact failure mode that this checklist exists to prevent. Examples:
- Edit `feedback_layered_closure_claim.md` → must Codex review before "memory saved"
- Edit cc-codex-pair SKILL.md (this file) → must Codex review before "checklist updated"
- Edit `acceptance-harness.yml` → must Codex review before "harness updated"
- Add new memory → must Codex review before declaring "lesson institutionalized"

**Canonical failure this rule exists to prevent**:
In the 2026-05-10 S35 SJC retrospective Round 9, CC shipped `feedback_layered_closure_claim.md` ("any X closed claim must Codex round-trip verify L4") in commit X, then in commit X+1 (5 minutes later) shipped retrospective v2 + 4 new memories with edits "applied per Codex Round 8 review" but WITHOUT Codex Round 9 round-trip to verify v2 faithfully implemented Round 8 asks. PM had to catch it. The mechanical fix: this very rule. Workflow-level enforcement, not memory advisory.

## Freeform pair workflow (chat / review / investigate)

For ad-hoc tasks not tied to a specific sprint Phase. Same core principle: **shared context first, then collaborate.**

### Freeform chat (`/cc-codex-pair chat <topic>`)
Use for: 调研、方案讨论、技术选型、头脑风暴

```
Step 1: CC 内部先做多维分析（CC 独有能力注入）
  CC 根据话题自动触发内部 skill:
  - 策略话题 → 内部 spawn 策略专家组 (agent team) 或跑 sprint-design-reviewer
  - 技术方案 → 内部跑架构评审
  - 数据分析 → 内部跑 backtest-skill
  - Bug 相关 → 内部跑 log-rootcause-triage
  CC 同时检查 pitfalls.md + memory 是否有相关条目

Step 2: Codex 独立分析（task-level prompt）
  CC 给 Codex 发任务: "请你独立分析 {topic}，读相关代码和文档，给出你的分析"

Step 3: Exchange
  CC 发送自己的多维分析（标注专家来源 + pitfalls 关联）
  Codex 发送自己的独立分析
  双方对比讨论

Step 4+: Multi-turn
  CC 和 Codex 对等讨论，CC 持续注入新的 pitfalls/memory 关联
  每当新子话题出现 → CC 重新检查 pitfalls + memory
  Session 持续到话题解决
```

### Freeform review (`/cc-codex-pair review <target>`)
Use for: 非 sprint 绑定的代码 review、方案 review、文档 review

```
Step 1: Both independently review (parallel)
  CC: runs internal analysis (can invoke /cross-review-gate if code review) → CC findings
  Codex: receives task-level prompt "请你独立审查 {target}" → Codex findings
  双方互不看对方结论

Step 2: Exchange and compare
  交换 findings → 识别共同发现 / 独有发现 / 矛盾项

Step 3: Consensus on divergences (max 5 rounds)

Output: Joint review conclusion with classification (mutual/CC-verified/Codex-raised)
```

### Freeform investigate (`/cc-codex-pair investigate <issue>`)
Use for: bug 排查、root cause analysis、日志分析

```
Step 1: Both independently investigate (parallel)
  CC: 内部跑 /log-rootcause-triage + 检查 pitfalls.md 是否有同根因历史
     → CC hypothesis + pitfalls 关联
  Codex: 收到任务级 prompt "独立排查 {issue}，读 log、grep 代码、给出你的根因假设"
     → Codex hypothesis

Step 2: Exchange hypotheses (标注来源)
  CC: "我的假设是 X（来自 log-rootcause-triage），
       且 pitfall #5 记录过类似问题（根因是 Y），供参考"
  Codex: "我的假设是 Z（来自我读 {file:line} 的发现）"

Step 3: Cross-check
  If same → confirmed (高置信度)
  If different → 对等辩论 (consensus loop, max 5 rounds)
  If both uncertain → jointly identify next investigation steps

Output: Confirmed root cause + fix recommendation (or escalate to human)
```

### Freeform session lifecycle
- **Open-ended**: No auto-close. 线程一直在，直到用户说结束或话题解决。
- **Resumable**: `node "$CXC" task --resume-last "$(cat /tmp/continuation_prompt.txt)"` 续同一线程接着聊。
- **No manual close needed**: broker 由 companion 自管；会话自然结束即可。

## Workflow

### Phase 1: Sprint Design Collaboration

**Entry**: CC has a sprint.md ready for review.

**Step 0 (Context sync)**: Run Round 0 protocol with session `s{N}`.

**Step 1: Both independently review (parallel)**

CC and Codex **同时独立审查**，互不看对方结论：

*CC side (internal):*
- CC runs `/sprint-design-reviewer sN review` internally → produces CC findings

*Codex side (via companion, task-level prompt):*
```bash
node "$CXC" task --resume-last "$(cat /tmp/cc_codex_prompt.txt)"
# --- prompt file content: ---
请你独立审查 Sprint {N} 的设计。

读 docs/sprint/sprint{N}.md，从实现可行性的角度深度审查：
1. 每个 Pack 能否按规格落地？
2. DoD 是否可测试、无歧义？
3. Pack 之间有没有隐藏依赖或顺序问题？
4. 工作量估算是否现实？
5. 有没有 sprint 应该拆分/重组的建议？

输出：按严重度排序的 findings 列表，每条含 docs/sprint/sprint{N}.md 的具体章节引用。
PROMPT
```

**Step 2: CC 读 Codex 回复 + enriches and exchanges**

先读 Codex 的独立 findings：
```bash
# 前台 task 调用返回的 stdout 即 Codex 回复（无需单独 read / 无需等 › 提示符）
# 回复已在上一步 task 调用的输出里
```

然后 CC 发送自己的 findings 给 Codex，**必须标注专家来源和注入 CC 独有知识**：
```
CC 的 findings（来自 sprint-design-reviewer 多专家面板）:

[架构师] F1: Pack C 的并发设计和现有 asyncio 模型冲突 — sprint40.md:L320
[量化策略师] F2: regime bucket edges 缺乏统计功效论证 — sprint40.md:L180
[统计学家] F3: holdout 窗口 7 天对 regime 稳定性声明不够 — sprint40.md:L195
[风控专家] F4: canary 期间无 wallet 保护机制 — sprint40.md:L350

[CC pitfalls 关联] ⚠️ Pack C 涉及 tick_size 改动，pitfall #7 记录过精度问题（S22 反复踩坑）
[CC 历史决策] ℹ️ Pack A 的 chase ceiling 是 S21 加的，当时 thin book 3x overpay

你的 findings 是什么？请对比我的多维分析，看看你有没有从其他角度发现我遗漏的问题。
```

Codex 发送自己的 findings，CC 收到后做分类：
- **共同发现** — 双方独立发现的同一问题（高置信度）
- **CC 独有** — CC 发现但 Codex 没发现（标注是哪个专家的视角）
- **Codex 独有** — Codex 发现但 CC 没发现（结对核心价值）
- **矛盾** — 双方对同一问题有不同判断

**Step 3: Consensus loop on divergences (max 5 rounds)**

只针对矛盾项辩论，共同发现直接确认。
- **Codex has final veto on implementation feasibility** — if Codex says a Pack is not implementable as specified, that Pack must be revised.

**Step 4: Verdict handling (CRITICAL — 不得中途停止问用户)**

```
IF Codex verdict = GO:
  → CC writes consensus notes into sprint.md → 进入 Phase 2

IF Codex verdict = NO-GO + 给了具体修复项 (P1/P2 findings):
  → CC 自动修复 sprint 设计（按 Codex 的 findings 逐条改）
  → 重新发给 Codex 审（同一 session）
  → 循环直到 GO 或 max 3 轮
  → 3 轮仍 NO-GO → 才停下来问用户裁决
  → CC 严禁在第 1 次 NO-GO 就停下来问用户 "Want me to proceed with 1/2/3?"

IF Codex verdict = NO-GO + 需要用户业务决策（如"策略方向需要重新定义"）:
  → CC 明确标注哪些是 CC 能自动修的，哪些必须用户决定
  → 只把需要用户决定的部分暂停，CC 能修的先修
```

**以下行为明确违规：**
```
❌ Codex 给了 4 个 P1 findings → CC 问用户 "Want me to fix?"
   → 应该直接修，不需要问
❌ Codex NO-GO → CC 停止整个工作流
   → 应该修完重审，循环到 GO
❌ CC 列出选项 "1. Fix S58  2. Revise S60  3. Both"
   → 应该直接判断哪些要修并执行
```

### Phase 2: Code Implementation

**Entry**: Sprint design approved (Codex GO). CC generates Pack implementation spec.

**Step 0 (Context sync)**: Run Round 0 protocol with session `s{N}`.
- Phase-specific files: source files this Pack will touch (CC lists them from the spec)
- CC validates Codex understands the existing code before modifying it

**Step 1**: CC generates implementation spec **enriched with CC's unique knowledge**.

Before sending spec, CC MUST:
1. Check `docs/qa/pitfalls.md` for ACTIVE cards related to this Pack's files/modules
2. Check memory for relevant historical decisions
3. Annotate the spec with warnings from these sources

```bash
node "$CXC" task --resume-last "$(cat /tmp/cc_codex_prompt.txt)"
# --- prompt file content: ---
Implement Pack {K} of Sprint {N}.

Implementation spec:
---
{pack_spec}
---

⚠️ CC's pitfalls warnings for this Pack:
- pitfall #7 (tick_size 精度): 本 Pack 涉及 {file}，任何 tick_size 相关改动必须用 Decimal 而非 float。S22 因此返工 3 次。
- pitfall #12 (selected_execution_token_id): 不能作为 fill 匹配的主键，只能做 fallback diagnostic。
{any_other_relevant_pitfalls}

ℹ️ CC's historical context:
- {relevant_historical_decisions_for_this_pack}
- {relevant_memory_entries}

Rules:
1. TDD: write failing tests FIRST, then implement.
2. Follow AGENTS.md conventions (snake_case, type annotations, minimal changes).
3. Reuse existing models from polyinit/execution/models.py.
4. Pay special attention to the pitfalls warnings above.
5. After implementation, run: pytest {test_paths} --override-ini="addopts="
6. Report: list all changed files with one-line summary.
PROMPT
```

**Step 2**: CC verifies implementation.
```bash
git diff --stat
git diff
```

Check: Does diff match spec file list? Tests written first? Tests pass? Any scope creep?

**Step 3**: If off-track, send feedback in same session (Codex remembers the spec and context):
```bash
node "$CXC" task --resume-last "$(cat /tmp/cc_codex_prompt.txt)"
# --- prompt file content: ---
Implementation feedback — corrections needed:
{deviations_list}
Fix only these issues. Do not change anything outside listed corrections.
PROMPT
```

Loop Step 2-3 (max 5 rounds).

**Step 4**: Pack complete. Session stays open — Codex remembers the implementation details for review Phase.

### Phase 3: Cross Review

**Entry**: All Packs implemented. Codex already has implementation context from Phase 2 (same session).

**Step 1: Both independently review (parallel)**

CC 和 Codex **同时独立审查代码**，互不看对方结论：

*CC side (internal):*
- CC runs `/cross-review-gate sN` internally → produces CC findings

*Codex side (via companion, task-level prompt):*
```bash
node "$CXC" task --resume-last "$(cat /tmp/cc_codex_prompt.txt)"
# --- prompt file content: ---
请你独立审查 Sprint {N} 的完整实现。

不要等我给你 findings — 你自己读代码、读文档、跑分析。

审查范围:
1. 读 docs/sprint/sprint{N}.md 确认 DoD
2. 用 git log 查看 S{N} 相关 commits
3. 读所有被 S{N} 修改的源码文件
4. 读 docs/qa/pitfalls.md 检查相关坑位
5. 跑相关测试验证

你的任务:
1. 逐个 Pack 检查实现是否达到 DoD
2. 发现可能被遗漏的问题
3. 关注跨 Pack 的 contract 一致性
4. 给出你自己的评价和建议

输出：按严重度排序的 findings 列表，每条含 file:line 证据。
PROMPT
```

**Step 2: CC 读 Codex 回复 + enriches and exchanges**

先读 Codex 的独立 findings：即上一步前台 `task` 调用返回的 stdout（无需单独 read）

然后 CC 发送 findings，**必须标注专家来源 + pitfalls 关联**：
```
CC 的 findings（来自 cross-review-gate 5 专家面板）:

[架构师] F1: ... — file:line
[正确性专家] F2: ... — file:line
[安全性专家] F3: ... — file:line
[性能专家] F4: ... — file:line
[QA 负责人] F5: ... — file:line

[CC pitfalls 关联] ⚠️ F2 和 pitfall #7 同根因
[CC 历史决策] ℹ️ F4 涉及的模块在 S21 做过类似优化，当时的方案是 ...

你的 findings 是什么？
```

CC 和 Codex 交换后分类：
- **共同发现** — 双方独立发现的同一问题（高置信度，直接确认）
- **CC 独有** — CC 发现但 Codex 没发现（标注哪个专家的视角）
- **Codex 独有** — Codex 发现但 CC 没发现（CC 读源码验证）
- **矛盾** — 双方对同一问题有不同判断（进入共识循环）

**Step 3: Consensus loop on divergences (max 5 rounds)**

只针对矛盾项和需要验证的独有发现辩论。共同发现直接确认。

**Output**: Final findings with classification:
- `Confirmed (mutual)` — 双方独立发现的同一问题
- `Confirmed (CC-verified)` — Codex 独有发现，CC 读源码后确认
- `Confirmed (Codex-verified)` — CC 独有发现，Codex 读源码后确认
- `Disputed` — 双方有分歧，经辩论后一方接受或升级给人类
- `Codex-raised` — Codex 的独有发现（结对的核心价值）

### Phase 4: Fix

**Step 0 (Context sync)**: Run Round 0 protocol with session `s{N}`.
- Phase-specific files: same changed files as Phase 3 + the confirmed findings list
- Codex re-reads the problematic code sections identified in findings

**Step 1**: CC enriches confirmed findings with historical fix context, then sends to Codex.

Before sending, CC MUST:
1. Check `docs/qa/pitfalls_archive/` for same-root-cause historical fixes
2. Check memory for relevant past repair attempts
3. Annotate each finding with "what worked / what didn't work last time"

```bash
node "$CXC" task --resume-last "$(cat /tmp/cc_codex_prompt.txt)"
# --- prompt file content: ---
Fix these confirmed findings:
{confirmed_findings}

⚠️ CC's historical fix context:
- F1: 同根因在 S22 修过，当时用 Decimal 替代 float 解决。参考 pitfalls_archive/2026-02-xx.md
- F2: 这是新问题，无历史参考。但注意 frozen denylist — live_moneyline.py 不能改。
{any_other_historical_context}

Rules:
1. Fix only listed findings. No unrelated refactors.
2. Add regression tests for each fix.
3. Pay attention to historical fix context above — avoid repeating failed approaches.
4. Run: pytest {test_paths} --override-ini="addopts="
5. Report: finding_id, file:line, one-line summary.
PROMPT
```

**Step 2**: CC runs `/cross-review-gate --recheck`.

**Step 3**: If new issues, loop (max 2 fix rounds).

**Step 4**: Fix complete. Session stays open for close Phase.

### Phase 5: Close

**Entry**: Codex already has full context from Phase 1-4 (same session).

**Step 1**: CC asks for final verdict (Codex already has full picture):
```bash
node "$CXC" task --resume-last "$(cat /tmp/cc_codex_prompt.txt)"
# --- prompt file content: ---
You've reviewed the complete change set and test results for Sprint {N}.

Summary of what was done:
---
{sprint_summary_of_changes}
---

Your final verdict:
- GO: safe to merge to devpig. State your confidence and any caveats.
- NO-GO: {specific blocking concerns with code evidence}
PROMPT
```

**Step 2: Verdict handling (同 Phase 1 逻辑)**
```
IF Codex GO:
  → CC runs `/sprint-close-auditor sN close` → sprint 完成 → close session

IF Codex NO-GO + 给了具体 blocking concerns:
  → CC 自动回到 Phase 4 修复 → 重新跑 cross-review-gate → 重新请求 Codex GO
  → 循环直到 GO 或 max 3 轮
  → 3 轮仍 NO-GO → 停下来问用户

IF Codex NO-GO + 需要用户决策:
  → CC 标注哪些 CC 能修，哪些必须用户拍板
  → CC 能修的先修
```

**Step 3**: Sprint complete. 线程上下文保留（`status` 给出 Codex session-id，可 `codex resume <id>` 回看）。broker 会话结束自然退出，**无需手动 close**。

## Error handling

| Situation | Exit code | Action |
|-----------|-----------|--------|
| Codex unreachable | 1 | `node "$CXC" setup` 自检。若仍失败，continue CC-only with `[unverified by Codex]` tag |
| 任务卡住/超时 | N/A | 后台任务用 `node "$CXC" status <jobId>` 查；异常则 `cancel <jobId>` 后重发。前台调用天然阻塞到完成，无 `›` 轮询超时问题。 |
| broker 异常 | N/A | companion 下次 `task` 会自动重建 broker；无需手动 prewarm。必要时清理 `$TMPDIR/codex-companion/` 后重发 |
| Permission denied | 5 | Should not happen with approve-all. Warn and continue CC-only |
| Consensus timeout | N/A | After MAX_ROUNDS, escalate to human with both positions |
| Context sync fail | N/A | After 2 correction rounds, CC provides explicit summary and proceeds with warning |

线程上下文：由 app-server 协议层持久保存，`--resume-last` 续接。即便 broker 重启，`status` 给出的 Codex session-id 仍可 `codex resume <id>` 找回。

## Safety rails
- **严禁 kill/重启 broker 或 Codex 线程**: CC 绝对不能因为"Codex 上下文不足"而 kill broker 或丢弃当前线程。Codex 有自己的上下文压缩机制（实测：83% 时自动压缩到 19%），比 CC 更智能地管理自己的上下文。CC 无权判断 Codex 的上下文是否充足。**broker 由 companion 自管，不要手动 kill；要换全新上下文只在用户明确要求时用 `--fresh` 开新线程。**
- **Context sync is mandatory**: No Phase proceeds past Round 0 without CC validating Codex's understanding. Skipping context sync degrades pair programming to blind delegation.
- **Evidence-based disputes**: All DISPUTE/PARTIAL responses must cite `file:line` evidence. Pure opinion without code evidence is weak and CC may override.
- **Secret protection**: Prompts sent to Codex must not contain API keys, cookies, or auth tokens. CC must pre-extract relevant config values from `.env` files and inline them into prompts (e.g., "current pig config: TP_PCT=0, SL_PCT=0.25"), because Codex sandbox may block `.env` reads.
- **Single session per CC conversation**: All Phases and freeform interactions share one Codex session. No Phase isolation.
- **Diff verification**: After every Codex implementation, CC must `git status` + `git diff` to verify.
- **Large file handling**: CC tells Codex file paths to read directly rather than pasting entire files into prompts.
- **Prerequisite check**: `codex` 已装且已登录（`node "$CXC" setup` 自检）。无需 tmux/ccs。
- **Escalation is mandatory**: If consensus fails after MAX_ROUNDS, the skill MUST stop and ask the human.
- **证据为王，不是角色为王**: 谁的源码证据更强谁的立场胜出。CC 不因为"是大脑"就有默认优先权。
- **Codex veto rights**: Codex can veto on implementation feasibility (Phase 1) and merge readiness (Phase 5).

### Codex 自主性保障 & 实用规则

**核心原则：不限制 Codex 的探索能力。** Codex 在 agent mode 下应该自由读文件、grep 代码、跑 git log — 这是它产出高质量 findings 的前提（D-group 实验已验证）。以下规则只解决实际技术问题，不限制 Codex 的自主性：

- **Always use companion**: `node "$CXC" task --resume-last "<prompt>"`。CC 不直接调 codex CLI、acpx 或任何 tmux 命令。
- **Prompt via file（长 prompt）**: 长 prompt 先写到 `/tmp/cc_codex_*.txt`，再 `task --resume-last "$(cat /tmp/file.txt)"`。短 prompt 可直接内联。
- **Secret protection**: CC pre-extracts `.env` 中的安全配置值（不含密钥）内联到 prompt 中，因为 Codex sandbox 可能无法读 `.env`。
- **Codex 无响应处理**: 前台调用天然阻塞到完成；后台用 `node "$CXC" status <jobId>` 查。若 job 异常，`cancel` 后重发。**不需要也不要 kill broker** —— broker 由 companion 自管。

## Task-tier, Spec, and Evidence Contract

### Task-tier gate
- Every Codex task must be tagged `tier: T0/T1/T2/T3`。
- `T2/T3` prompts must use the 8-element spec format exactly。
- `T1` may use short form, but still requires `WHERE` and `DONE`。
- If a task spans strategy + code + runtime, split it or promote it to `T3`; do not hide mixed risk under a "small edit" label.

### 8-element task prompt contract (`T2/T3` 强制)
```
WHY:
WHAT:
WHERE:
HOW MUCH:
TRUTH / PROXY:
PITFALLS HIT:
DONE:
DON'T:
```
Rules：
- This is a task frame, not a diagnosis frame。
- CC must not pre-fill root cause as fact unless already verified。
- Unknown fields must be written as `unknown yet`; they may not be silently omitted。

### Prompt 构造：复用 gpt-5-4-prompting 块库（把"给任务不给结论"变成模板）

本 skill 随包 vendored 了一套 Codex/GPT-5.4 提示块库（来自 OpenAI codex-plugin-cc）：
```
$HOME/.claude/skills/cc-codex-pair/skills-ref/gpt-5-4-prompting/
├── SKILL.md                              # 用法总则
└── references/
    ├── prompt-blocks.md                  # 可复用 XML 块（拼装用）
    ├── codex-prompt-recipes.md           # 端到端模板
    └── codex-prompt-antipatterns.md      # 反模式
```

**核心理念（和本 skill 的"给任务不给结论"一致）**：把 Codex 当 operator，给紧凑、块结构化、带 XML 标签的 prompt —— 说清任务、输出契约、跟进默认值，而不是堆自然语言或要它"想更努力"。**先收紧 prompt 契约，再考虑加 reasoning。**

**CC 给 Codex 发任务时，按场景选块拼进 prompt**：

| 场景 | 必带块 | 作用 |
|--|--|--|
| 所有任务 | `<task>` | 说清具体任务 + 仓库/失败上下文 + 期望终态 |
| 编码/调试（Phase 2/4） | `<completeness_contract>` `<verification_loop>` `<missing_context_gating>` | 别停在第一个貌似答案；改完自检；高风险缺信息才停下问 |
| 审查/对抗审查（Phase 1/3） | `<grounding_rules>` `<structured_output_contract>` `<dig_deeper_nudge>` | 每条 finding 必须有证据；按严重度排序；挖二阶问题 |
| 调研/选型（freeform chat） | `<research_mode>` `<citation_rules>` | 标注事实 vs 推断；引用来源 |
| 写操作（`--write`） | `<action_safety>` | 只动该动的，禁止无关重构 |

**反模式（务必避免，详见 antipatterns.md）**：
- 模糊任务框（"看看这个，说说想法"）→ 用 `<task>` 写清
- 缺输出契约 → 用 `<structured_output_contract>`
- 把多个无关任务塞进一次 run → 拆成多次 `task`
- 用"想更努力/更聪明"代替更好的契约 → 用 `<verification_loop>`
- 无证据的确定性断言 → 用 `<grounding_rules>` 标注推断

**和 8-element contract 的关系**：8-element 是本 skill 的高层任务框（WHY/WHAT/WHERE/...）；XML 块库是把其中"输出契约/完成定义/grounding"落到具体可复制的措辞。两者叠加用：8-element 定骨架，XML 块定每段的精确措辞。

## Failure-Mode Routing Contract

Routing is `session-level`、`evidence-driven`、`bidirectional`。

### Allowed triggers
- 连续 `2` 轮无新增证据，只是在改参数、改语气或重复同一搜索
- 声称 `done / fixed / verified / safe to merge` 但没有对应完成证据
- 把 `hypothesis` 写成 `root cause` / `environment issue` / `already covered`
- 未读足够上下文就给 severity / architecture judgment
- 修完即停，未做冰山扫描或上下游影响判断

### Trigger format
```
route_log:
- task: <short name>
- tier: T1/T2/T3
- observed_in: CC / Codex / shared session
- trigger: <spinning / fake_done / blame_shift / no_search / low_context / passive_stop>
- evidence: <concrete behavior or missing proof>
- route_before: <old route>
- route_after: <search-first / context-50-lines / hypothesis-verification / reverse-hypothesis / completion-proof / iceberg-scan / scope-simplify>
- exit_condition: <what evidence closes the route>
```

### Tone rule
- Never say "Codex is spinning" or "CC is rationalizing"。
- Always say "the current session is spinning because the last 2 loops changed thresholds but produced no new evidence"。

## Equal Challenge Rights
- CC can challenge Codex with anti-rationalization questions。
- Codex can challenge CC with the same table and the same burden-of-proof rule。
- Whoever makes the claim owns the burden of evidence。
- If evidence cannot be produced, the claim must be downgraded：
  - `done` -> `implemented but unverified`
  - `root cause` -> `working hypothesis`
  - `GO` -> `needs more evidence`
  - `ship-safe` -> `needs rollout guardrail`

## Required investigation loop for debug / review / design tasks (`T2/T3` 强制)
1. 读信号
2. 多角度搜索
3. 读源码上下文（命中点上下各 `50` 行，必要时追 `caller/callee`）
4. 验证假设
5. 反转假设
6. bugfix 时追加冰山扫描：grep 同类 pattern，决定 `fix-now / pack / pitfall`

## Completion Claim Discipline
- Codex 不得在没有任务匹配证据时说 `done`。
- CC 不得在没有看到相应证据时请求 `merge / ship / GO`。
- `T3` 结论必须附：命令与结果摘要、产物/日志/状态输出、剩余风险、rollback/stop condition。
- 路由变化若影响计划、消耗 `2+` loops、或暴露可复用根因，必须写入 `docs/task/progress.md`；形成稳定根因时，收口到 `docs/qa/pitfalls.md`。

## Integration with existing skills

| Existing skill | Integration point |
|---------------|-------------------|
| `sprint-design-reviewer` | Phase 1: CC runs internally, shares findings with context-synced Codex |
| `cross-review-gate` | Phase 3: CC runs internally, Codex independently reviews same code then evaluates findings |
| `tdd-loop-executor` | Phase 2: CC's spec follows TDD conventions |
| `sprint-close-auditor` | Phase 5: CC runs after Codex GO |
| `adversarial-cross-model-review` | Phase 3: Codex RAISE follows same format as external model findings |
| `code-review-expert` | Phase 3: Finding format `[Px][confidence]` shared |

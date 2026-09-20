# ADR-004：多宿主目标态 —— Claude Code / Cursor（本地 + Cloud）/ Grok Bot 共用 ai-workflow-kit

| 项 | 内容 |
|---|---|
| 状态 | Proposed（待 Jimmy 验收；验收清单见 §9） |
| 日期 | 2026-09-20 |
| 决策者 | Jimmy |
| 起草 | 架构师（Cursor Cloud Agent） |
| 范围 | `licett/ai-workflow-kit` master @ `6d53534`。**只写文档，不改 `skills/*/SKILL.md`、`install.sh`、`scripts/`、`templates/`。** |
| 关联 | `architecture/REVIEW-skills-era-fit-2026-09-20.md`（[PR #2](https://github.com/licett/ai-workflow-kit/pull/2)，下称 REVIEW）；`architecture/QA-nightshift-investment.md`（[PR #1](https://github.com/licett/ai-workflow-kit/pull/1)，仅借用其 ROLE_MAP「不互相顶班」约束） |
| 取代 | REVIEW §0 末段「推翻本总判的条件」（见 §0.2） |

---

## 0. 背景与触发

### 0.1 新硬约束

Jimmy 于 2026-09-20 给出硬约束：**Grok Bot 也必须使用 ai-workflow-kit 这套工作流**，不是仅本机 Claude Code。这把 kit 的执行面从 1 个（本机 CC）变成至少 4 个：Claude Code 本机、Cursor 本地、Cursor Cloud Agent、Grok Bot 云端计算机。

### 0.2 Jimmy 否决 REVIEW 的「CC-only 推翻条件」（记录）

1. REVIEW §0 写道：若 Jimmy「只在本机 Claude Code 里用、不上 Cloud Agent、不用 Grok Bot」，则 P1-1 / P1-4 / P1-9 / P2-4 降为可选、总判改为「做 P0 止血即可」。
2. Jimmy 于 2026-09-20 明确否决该条件：Grok Bot 必须用这套工作流。**该推翻条件作废，REVIEW 总判「部分过时，需重构而非重写」维持。**
3. 直接后果：REVIEW P1-1（多宿主安装）从 P1 **升为 P0**（本文 §5 P0-A）；P1-9（hooks 双格式）、P2-4（plugin 打包）维持 P1/P2 不降级；P2-5（周期任务交 Grok Bot routine）从「长期形态」升为本文 §4 的**目标态组成部分**。
4. REVIEW §4.3「不应交给 Grok Bot：`tdd-loop-executor`」被本文 §3.3 **部分推翻**：T1/T2 Pack 允许 Grok Bot 执行，T3 仍不给（理由见 §3.3）。
5. 本节即为该否决的正式记录；REVIEW 文件本身不改（它在 PR #2 分支上，合并后如需在其文末补附录，引用本节即可）。

### 0.3 本 ADR 要回答的六个问题

对应 Jimmy 的六点要求：§2 多宿主读路径与入口；§3 Layer1 复用与 skill 装配清单；§4 Grok Bot 落地形态与最小映射表；§5 P0 切片（≤3）与 done_when；§6 与工作流优化师 ROLE_MAP 的交接面；§7 非目标。

---

## 1. 决策

**一句话：kit 的真相源只有一个——目标项目仓库内的 `AGENTS.md` + `.agents/skills/`；每个宿主只允许有一层「薄入口」指向它，任何宿主都不得持有 skill 正文的第二份拷贝。**

三条设计原则（后文所有表格都服从这三条）：

| # | 原则 | 反面（禁止） |
|---|---|---|
| D1 | **仓库内单一真相源。** skill 正文、AGENTS.md、模板、`scripts/qa/` 全部随目标项目仓库版本化；home 目录（`~/.claude`、`~/.cursor`、`~/.grok`）只作本机便利，不是任何云端宿主的依赖 | `install.sh` 只写 `~/.claude/skills`（现状） |
| D2 | **宿主薄入口。** 每个宿主一层 ≤30 行的入口（symlink / 一行 import / 适配 skill），入口只做「在哪、怎么读、审批边界」，不复述方法论 | 把 62 KB `cc-codex-pair` 正文复制进 Grok Bot skill 库 |
| D3 | **闸门语义跨宿主一致，实现方式允许不同。** Ask→Code、TDD、tier 闸门、Gate precedence、sprint close 的判定标准在所有宿主上相同；「多视角怎么产生」（并行 subagent / 串行换视角 / Bot 间 handoff）按宿主能力选 | 因宿主没有 subagent 就跳过 review 闸门 |

否决的备选方案：

| 备选 | 为什么不选 |
|---|---|
| A. 每宿主一份完整拷贝（CC 用 `~/.claude/skills`，Grok Bot 用 Bot skill 库全文） | 三份正文必然漂移；REVIEW C6/C7 已证明 kit 连两份模板都维护不住 |
| B. 只依赖各宿主的「兼容读取」（Cursor 读 `.claude/skills`，Grok Build 读 `.claude/*`） | Claude Code 不读 `.agents/skills`/`AGENTS.md`（文档证实，功能请求 [#31005](https://github.com/anthropics/claude-code/issues/31005)、[#34235](https://github.com/anthropics/claude-code/issues/34235) 未落地）；Grok Bot 云端计算机是否扫仓库 skill 目录**未被其文档证实**（§8 V1）。兼容读取不能作为架构前提 |
| C. 把 kit 打成 plugin 一次性解决 | 是 P2-4 的长期形态，但 Grok Bot 无 plugin 市场导入 kit 的路径；plugin 解决不了 Grok Bot 侧 |

---

## 2. 多宿主目标态：读路径与入口矩阵

### 2.1 矩阵

「原生」= 该宿主文档明确列出；「兼容」= 文档标注为兼容路径；「待验证」= 见 §8。

| 宿主 | 指令文件入口 | skill 读路径 | agent / 多视角定义 | hooks | 能否读本机 home | kit 入口层（D2） |
|---|---|---|---|---|---|---|
| **Claude Code 本机** | `CLAUDE.md`（原生；不读 `AGENTS.md`） | `.claude/skills/`（项目，原生）、`~/.claude/skills/`（个人） | `.claude/agents/`、`~/.claude/agents/` | `.claude/settings.json` | 是 | `CLAUDE.md` 一行 `@AGENTS.md` import；`.claude/skills` → symlink 到 `.agents/skills`（§8 V3） |
| **Claude Code 云会话 / routines** | 同上，仅仓库内 | 仅仓库内 `.claude/skills/` | 仓库内 `.claude/agents/` | 仓库内 settings | 否 | 同上，无额外动作 |
| **Cursor 本地** | `AGENTS.md`（原生） | `.agents/skills/`、`.cursor/skills/`（原生）；`.claude/skills/`、`.codex/skills/`（兼容）；`~/.cursor/skills/`、`~/.agents/skills/`（个人） | `.cursor/agents/`（原生）；`.claude/agents/`、`.codex/agents/`（兼容） | `.cursor/hooks.json`；第三方 hook 兼容读 `.claude/settings.json` | 是 | 零入口：直接读 `.agents/skills/` 与 `AGENTS.md` |
| **Cursor Cloud Agent** | `AGENTS.md` + `.cursor/environment.json` | 仓库内 `.agents/skills/` / `.cursor/skills/` / `.claude/skills/`；`~/.cursor/skills/` 仅在开启 Sync 时；`~/.agents/skills/` 永不同步 | 仓库内 `.cursor/agents/`（`.claude/agents/` 兼容） | **仅** `.cursor/hooks.json` | 否 | 零入口 + `environment.json`（P2-6） |
| **Grok Bot** | **Bot description（人设）**：长期规则 + 审批边界 + 一句「进入任何仓库任务前先读 `/workspace/<project>/AGENTS.md`」 | **账户侧 skill 库**（Settings › Plugins › Yours，按 Bot 启用，`/` 引用）；仓库内 skill 文件需 Bot 主动打开读取 | 无 subagent 定义文件；多视角 = 同一 Bot **串行换视角**，或 Bot 间 handoff / 群聊（2–6 Bot） | 无仓库 hooks 机制；用**审批边界**替代 | 本机不可达（本机执行受独立的 local execution policy 管控）；云端计算机有持久共享 `/workspace` | **适配 skill**（每个 ≤30 行，见 §4.3）：指向 `/workspace/<project>/.agents/skills/<name>/SKILL.md` |
| Codex（旁路，共用路径，非本 ADR 主体） | `AGENTS.md`（链 ≤32 KiB） | `.agents/skills/` | `.codex/agents/` | — | — | 零入口 |

结论：**`.agents/skills/` + `AGENTS.md` 是四个宿主中三个的原生路径**（Cursor 本地、Cursor Cloud、Codex），Claude Code 差一层 symlink + 一行 import，Grok Bot 差一层适配 skill。这就是 §5 P0-A 的全部工作量。

### 2.2 Grok Bot 入口的三条特殊性

1. **skill 存储不在文件系统。** Grok Bot 文档只描述「从完成的任务保存为 skill」「按 Bot 启用」「`/` 引用」，没有仓库目录扫描。因此 kit skill 正文不能假设被 Grok Bot 自动发现，必须由**适配 skill** 引导 Bot 去读仓库文件。若 §8 V1 验证为「Grok Bot 云端计算机原生扫 `.agents/skills/` 或 `.grok/skills/`」，适配 skill 缩为一行，架构不变。
2. **一个账户一台计算机，所有 Bot 共享 `/workspace`、浏览器会话与命令行凭据。** 目标项目 clone 在 `/workspace/<project>`，所有 Bot 可见。放在这台计算机上的 git 凭据必须是**只能 push 到工作分支、不能 merge / 不能改保护分支**的细粒度 token；merge 靠仓库分支保护而非 Bot 自律。
3. **没有 hooks，只有审批边界。** kit 在 CC/Cursor 上靠 hooks 做的「commit 前 session-end 提醒」「Edit 后 pitfalls 提醒」，在 Grok Bot 上写进人设的「每次写操作前」规则，并把 `git push` / 开 PR / 贴 PR 评论全部放在审批点之后。

### 2.3 目标态目录树（目标项目仓库）

```text
<project>/
├── AGENTS.md                      ← 唯一 canonical 规则文件（Cursor / Cloud / Codex / Grok Bot 人设指向）
├── CLAUDE.md                      ← 一行：@AGENTS.md（Claude Code 唯一读的入口）
├── .agents/
│   ├── skills/                    ← kit skills 的唯一正文（install.sh --target project 写入）
│   │   ├── tdd-loop-executor/
│   │   ├── sprint-close-auditor/
│   │   └── ...                    ← 项目目标默认 9 个；cc-codex-pair 不进项目目标（§3.3）
│   └── grok-bot/                  ← Grok Bot 适配 skill（≤30 行/个；install 自 kit `templates/grok-bot/` 复制），由优化师同步到 Bot skill 库
│       ├── kit-ask-then-code.md
│       ├── kit-tdd-loop.md
│       ├── kit-review-gate.md
│       ├── kit-verify-findings.md
│       ├── kit-sprint-close.md
│       └── kit-log-triage.md
├── .claude/
│   ├── skills -> ../.agents/skills   ← symlink（Claude Code 入口；§8 V2/V3）
│   └── agents/                    ← 6 个 reviewer 视角文件（Cursor 兼容读取；Grok Bot 作为视角提示词读入）
├── .cursor/
│   ├── hooks.json                 ← P1-9（Cloud 只认这个）
│   └── environment.json           ← P2-6
├── scripts/qa/                    ← build_knowledge_db.py / search.py / golden_query_test.py（随 install 部署）
└── docs/{task,sprint,qa,spec}/    ← 方法论产物（不变）
```

---

## 3. 复用与装配清单

### 3.1 Layer 1 方法论：原样复用，零改动

以下六项在四个宿主上**语义、判定标准、产物格式完全一致**，Grok Bot 侧只改「谁触发、在哪跑、写操作放哪」：

| 方法论 | 定义所在 | Grok Bot 侧唯一差异 |
|---|---|---|
| Ask→Code 双阶段 | `templates/AGENTS.md` 「LLM 实践内化」 | Ask 产物贴在 Bot 会话（可审阅），Code 在 `/workspace/<project>` 新分支 |
| Sprint + Pack（类型、生产含义、honest negative result） | `templates/sprint-template.md`、AGENTS.md「Pack 规范」 | 无 |
| TDD-first（RED→GREEN→refactor） | AGENTS.md「Testing Guidelines」 | 无 |
| 编码前避坑检索（强制） | AGENTS.md：先读 `docs/qa/pitfalls.md` ACTIVE，再 `python3 -m scripts.qa.search` | 无（前提：`scripts/qa/` 已随 install 进仓库，§5 P0-A） |
| 文档闭环（progress.md 每轮更新、pitfalls ≤250 行/≤10 卡、Session-end 三问） | AGENTS.md「Workflows」 | Session-end 三问中「写入 auto-memory」改为「写入 Bot memory 仅限用户偏好；项目事实一律写回仓库文档」（§8 R2） |
| 证据纪律（三红线、T0–T3 分级、8 要素 spec、`[Px][confidence] file:line`） | AGENTS.md「AI 协作红线与任务门禁」、`agents/code-review-expert.md` | 无 |

### 3.2 Layer 2 约束：复用，两处改

| 资产 | 判定 | 需改之处 |
|---|---|---|
| `templates/AGENTS.md` | 复用为 canonical | (a) 「CC-Codex Pair Programming Protocol」段改为条件段：「若宿主可达 Codex 则生效；Grok Bot 上跨模型对抗由 PR 评论往返实现（§4.2 行 4）」；(b) 新增一行 `Gate precedence`（REVIEW P1-8），Grok Bot 人设只引用不复述 |
| `templates/hooks.json` | **不给 Grok Bot**；CC/Cursor 侧按 REVIEW P1-9 双格式 | 现状含 tmux 拦截 + `codex-pair.sh`，§5 P0-C 清理 |
| `agents/*.md`（6 个） | 复用；在 Grok Bot 上**降为「视角提示词」** | 无需改文件；适配 skill `kit-review-gate` 说明「按 tier 依次以 `architect.md` / `reviewer-correctness.md` / … 的角色读 diff，每个视角独立产出 findings 后再做 Phase 3 归一化」 |
| `scripts/qa/*.py` | 复用 | `MEMORY_DIR` 去硬编码（§5 P0-B） |

### 3.3 Skill 装配表（对 Grok Bot）

判定含义：**必装** = Grok Bot 必须有对应适配 skill，缺了就不算「用了这套工作流」；**可选** = 有价值但不是工作流骨架；**禁装** = 违反 D1/D2 或依赖 Grok Bot 不具备的机制。「前置」列引用 §5 编号或 REVIEW 编号。

| Skill | Grok Bot 判定 | 理由 | 前置 |
|---|---|---|---|
| `tdd-loop-executor` | **必装**（限 T1/T2 Pack；**T3 Pack 不给 Grok Bot**） | Ask→Code + TDD 是「这套工作流」的骨架，缺它 Grok Bot 就只是在旁观。Grok Bot 有终端 + 文件系统 + 持久 `/workspace`，能跑测试、能写分支。T3（runtime / deploy / frozen core）不给，因为其回滚方案、truth/proxy 需要人或 Cloud Agent 在受控分支上执行，且 Grok Bot 共享计算机不适合持有生产凭据。**这条推翻 REVIEW §4.3 的「不交给 Grok Bot」** | P0-C（幽灵脚本）、REVIEW P1-6（去 `CLAUDE.md`：`:18`、`:31`、`:72` 三处） |
| `sprint-close-auditor` | **必装** | 只读对账 + verdict，天然适合 routine（Slack「sprint close」listener 或 ETA 到期 schedule）；输出 Complete / Partial / Blocked 不需要写权限 | P0-C（`:43-45` 幽灵脚本） |
| `log-rootcause-triage` | **必装** | 59 行、传输无关、无业务泄漏；日志可用附件或 `/workspace` 路径交给 Bot | 无 |
| `adversarial-cross-model-review` | **必装**（按 REVIEW P1-7 重定位为「外部 / 自动化 review findings 验证器」） | Grok Bot 对 CC/Cursor 而言**本身就是外部模型**：GitHub 事件 routine 把 Bugbot / CC 的 PR 评论喂给它逐条验证，反向亦然。这是 Grok Bot 上「跨模型对抗」的实现方式（替代 cc-codex-pair 传输层） | P1-7 未做时仍可用，只是 description 说的是「用户粘贴 GPT 结论」 |
| `cross-review-gate` | **必装（Lite / Standard，串行视角模式）；Full 禁** | 闸门语义（tier 规则、归一化格式、Pass/Conditional/Fail、QA Lead 否决）是 kit 独有。但 Grok Bot 没有 subagent 定义文件、不能并行 spawn 5 个上下文：Standard 在 Grok Bot 上 = 同一 Bot 按 3 个视角**串行**读 diff、各自出 findings、再做 Phase 3 归一化。Full（5 视角 + 3 步交叉）成本过高且并行假设不成立；routine 对每个 PR 跑 Full 是 REVIEW 明令禁止项 | 适配 skill 写明 `review_source: grok-bot-sequential`（REVIEW P1-3 字段） |
| `sprint-design-reviewer` | **可选**（仅 `--type engineering`）；strategy / hybrid **禁** | engineering 面板（Axis A–E）通用；strategy 面板与 `:33` 关键词表是 polyinit 业务泄漏，Grok Bot 会把它记成「项目事实」（§8 R2） | REVIEW P1-5 拆分前，适配 skill 强制传 `--type engineering` |
| `spec-arch-adapter` | **可选**（新项目 bootstrap 一次性） | Bot 可在 `/workspace` 跑脚本；但 `SKILL.md:13,16` 硬编码 `~/.claude/skills/spec-arch-adapter/scripts/...`，Grok Bot 无此路径 | P0-A（脚本路径改为相对 skill 目录） |
| `code-review-expert`（skill） | **可选** | 单路 review。Grok Bot 没有 Cursor `/review` 内建可替代，这个 skill 可直接充当 `cross-review-gate` 的 Lite 档实现 | 与 agent 同名问题不影响 Grok Bot |
| `project-roadmap-research` | **可选**（chat-only 模式） | 只读探索；但 `:22` 以 `CLAUDE.md` 判定项目根，AGENTS.md-only 项目会 skip write | REVIEW P1-6 |
| `cc-codex-pair` | **禁装** | 同时踩中三条禁线：(1) 传输层是 `openai/codex-plugin-cc` **冻结拷贝**（`PROVENANCE.md`）；(2) 依赖 Claude Code 专有机制——`Bash run_in_background:true` + harness task-notification（`SKILL.md:346-348`）、`$HOME/.claude/skills/...` 绝对路径（`:238`、`:272`）；(3) 62 KB 常驻上下文违反 D2。Grok Bot 上也没有 Codex。REVIEW P1-4 三分后，传输无关的 `pair-protocol`（≤200 行）可重新评估为「可选」 | REVIEW P1-4 |
| `templates/hooks.json`（非 skill，但会被一并装） | **禁装** | 4 处 tmux 拦截 + `codex-pair.sh`；Grok Bot 无 hooks 机制 | P0-C |

统计：必装 5、可选 4、禁装 1（+1 模板）。`install.sh --target project` 默认写入 9 个 skill（排除 `cc-codex-pair`），`--target user` 保留 10 个（本机 CC 仍可用 cc-codex-pair）。

---

## 4. Grok Bot 侧落地形态

### 4.1 三层映射

Grok Bot 的模型是 **Bot（长期角色 + 审批边界）→ skill（做法）→ routine（何时跑）**。kit 的三层对应：

| Grok Bot 层 | 承载 kit 的什么 | 内容来源 | 谁维护（§6） |
|---|---|---|---|
| **Bot 人设（description）** | Layer 2 的「执行姿态」「三红线」「Gate precedence」「默认项目路径」「审批边界」 | 从 `templates/AGENTS.md` 摘 ≤15 行，不复述细则，末尾一句「细则以 `/workspace/<project>/AGENTS.md` 为准，每次任务先读它」 | 工作流优化师 |
| **Bot skill（适配 skill）** | Layer 3 的 5 个必装 + 可选 skill 的**入口** | kit `templates/grok-bot/kit-*.md` → install 到项目 `.agents/grok-bot/kit-*.md`，每个 ≤30 行，含 `kit_ref: <sha>` | 源文件：kit 维护者；同步到 Bot：优化师 |
| **routine** | 「何时跑」：schedule / Slack listener / webhook / GitHub 事件 | 优化师按 §4.2 表建，≤50 条/Bot，先 Test run（用安全输入）再 Active | 优化师 |

### 4.2 最小映射表：kit 阶段 → Grok Bot 形态

| # | kit 阶段 / 机制 | Grok Bot 形态 | 触发 / 入口 | Bot 侧动作（摘要） | 审批边界 | 产出 / 证据 |
|---|---|---|---|---|---|---|
| 1 | **Ask**（计划草稿） | 人设强制 + 适配 skill `kit-ask-then-code` | 任何仓库任务开始 | 读 `AGENTS.md` → `docs/task/progress.md` → `docs/sprint/sprintN.md` → `docs/qa/pitfalls.md` ACTIVE → `python3 -m scripts.qa.search "<kw>" --scope pitfalls`；定 T-tier；T2+ 产 8 要素 spec | 无（只读） | spec 贴会话，含 `PITFALLS HIT` |
| 2 | **Code**（TDD 循环） | 适配 skill `kit-tdd-loop` | `/kit-tdd-loop <project> sN` 或 Slack listener（channel `#dev`，containing `sN go`，narrow） | 在 `/workspace/<project>` 建 `grok/sN-<pack>` 分支；RED→GREEN→refactor；每轮更新 `progress.md`；仅 T1/T2 | `git push` / 开 PR = **审批后**；merge **永不** | 测试输出 + diff + `progress.md` 变更 |
| 3 | **cross-review-gate**（Lite / Standard） | 适配 skill `kit-review-gate` | GitHub 事件 routine「PR opened / synchronize」，或 `/kit-review-gate <pr>` | 按 tier 串行 1–3 视角（读 `.claude/agents/*.md` 作角色，各自独立出 findings）→ 统一为 `[Px][confidence] file:line` → Phase 3 Step 4 五问（源码证据 / 可复现 / 可行 / 重复 / 误报）→ Confirmed / Likely / Disputed / Impractical → Pass / Conditional / Fail | 贴回 PR 评论 = **审批后**（可先贴会话） | 报告 header 含 `Task tier`、`review_source: grok-bot-sequential` |
| 4 | **跨模型对抗**（替代 cc-codex-pair） | 适配 skill `kit-verify-findings`（= `adversarial-cross-model-review`） | PR 上出现 Bugbot / CC / 他人 review → routine | 逐条读源码 → Adopt / Partial / Reject / Defer，每条 `file:line` | 同行 3 | 验证报告；Reject 必须带反例 |
| 5 | **sprint-close** | 适配 skill `kit-sprint-close`（= `sprint-close-auditor`） | Slack listener（containing `sprint close`）或 schedule（读 sprint doc ETA 字段，到期当日） | 对账 doc↔code↔test → Complete / Partial / Blocked → `python3 -m scripts.qa.build_knowledge_db` | 只读；**不改 sprint doc 状态**，只给「建议改动」待人确认 | 收口矩阵 + 知识库重建日志 |
| 6 | **log-rootcause-triage** | 适配 skill `kit-log-triage` | 附件 / `/workspace` 路径 / webhook（告警系统 POST 日志片段） | 2–4 个 hypothesis + 反证检查 + 最小修复建议 | 无 | 按 `references/patterns.md` 格式 |
| 7 | **文档预算检查** | routine（schedule，每周一） | — | `pitfalls.md` ≤250 行 / ≤10 卡；`progress.md` ≤100 行；超标只提醒 | 无 | 会话提醒 |
| 8 | **Gate precedence** | 人设一行（引用 AGENTS.md 定义） | — | `QA Lead Block > sprint-close-auditor Blocked > 其他 Conditional`（Codex NO-GO 在 Grok Bot 上不适用，由行 4 的 PR 往返替代） | — | — |

**不映射的：** `cross-review-gate` Full、`cc-codex-pair`、任何 merge / 改生产配置 / 改保护分支的动作、T3 Pack 执行（交 Cloud Agent 或本机 CC）。

### 4.3 适配 skill 模板（≤30 行，源文件放 kit `templates/grok-bot/`，install 后落在项目 `.agents/grok-bot/`）

以下是**形态规范**，不是最终文案；由 P0-A 的实现者按此写 6 个文件。

```markdown
---
name: kit-sprint-close
description: 按 ai-workflow-kit 的 sprint-close-auditor 对 /workspace/<project> 做 sprint 收口审计。
  用于 Slack 出现 "sprint close" 或 sprint ETA 到期时。只读，不改文档状态。
kit_ref: <git sha of ai-workflow-kit>
---
输入：project（默认见 Bot 人设）、sprintN。
前置：
1. `git -C /workspace/<project> pull --ff-only`；失败则报告并停止，不 reset。
2. 读 /workspace/<project>/AGENTS.md（规则以它为准）。
执行：
3. 打开 /workspace/<project>/.agents/skills/sprint-close-auditor/SKILL.md，**逐字按其 Workflow 执行**。
4. 知识库步骤用 `python3 -m scripts.qa.build_knowledge_db`（仓库内路径）。
输出：Complete / Partial / Blocked + 完成矩阵 + findings（每条 file:line 或 doc:line）。
审批边界：不修改任何仓库文件；对 sprint doc 的状态改动只给「建议 diff」，等人确认。
缺失处理：sprint doc / progress.md 不存在 → 报告缺失，不猜测、不补写。
```

规范要点：`kit_ref` 必填（§6 漂移检查用）；「逐字按其 Workflow 执行」是核心——适配 skill 不复述步骤；「缺失处理」必填（Grok Bot 官方要求「报告缺失而不是绕过」，与 kit 三红线之红线三一致）。

### 4.4 最小端到端场景（验收用）

1. Jimmy 在 Slack `#dev` 发「s7 go project=demo」→ listener 触发 `kit-tdd-loop`。
2. Bot 完成 Ask：会话中出现 8 要素 spec，`PITFALLS HIT` 非空或写明「检索 0 命中（关键词：…）」。
3. Bot 在 `grok/s7-pack1` 分支上 RED→GREEN，`progress.md` 有本轮条目；请求 push 审批。
4. Jimmy 批准 → push → PR opened → GitHub 事件 routine 触发 `kit-review-gate`（Standard，串行 3 视角）→ 报告贴会话 → Jimmy 批准贴 PR。
5. Cursor / CC 侧对该 PR 跑 `adversarial-cross-model-review` 验证 Grok Bot 的 findings（反向对抗）。
6. Jimmy 在 `#dev` 发「sprint7 close」→ `kit-sprint-close` 输出 Complete / Partial / Blocked。
7. 全程 Run history 可查；无任何一步由 Bot 自行 merge。

---

## 5. P0 切片（3 个）与 done_when

原则：P0 只做「让四个宿主都能读到同一份 kit」的一致性工作，**不改任何流程语义**。编号 P0-A/B/C 避免与 REVIEW 的 P0-1…P0-6 混淆；对应关系在「来源」列。以下验收命令均在 kit 根目录或指定目标目录直接可跑。

### P0-A　install 多目标（来源：REVIEW P1-1 升级 + P0-2 后半）

**改什么**

- **先修一个实测到的既有 bug**：`install.sh:50,70` 的 `((installed++))` / `((agents_installed++))` 在计数为 0 时算术结果为 0、返回状态 1，被 `set -euo pipefail`（`:3`）当成失败直接退出。在干净 `HOME` 下实测（2026-09-20，本仓库 `6d53534`）：只装 1 个 skill（`adversarial-cross-model-review`）即 `exit=1`。也就是说**现有 install.sh 从未在新机器上装全过 10 个 skill**，这与 REVIEW C1「kit 只在 Jimmy 本机存在」互为印证。改为 `installed=$((installed + 1))`。
- `install.sh` 增加 `--target user|project`（默认 `project`）、`--root <dir>`（默认 `.`）、`--host claude|cursor|grok|all`（默认 `all`）。
- `--target project`：
  1. 复制 9 个 skill（排除 `cc-codex-pair`）到 `<root>/.agents/skills/`；
  2. `--host claude|all`：建 `<root>/.claude/skills -> ../.agents/skills` symlink；若 `<root>/CLAUDE.md` 不存在则写入一行 `@AGENTS.md`，存在则追加该行（幂等）；
  3. 复制 `agents/*.md` 到 `<root>/.claude/agents/`；
  4. 复制 `scripts/qa/{__init__,build_knowledge_db,search,golden_query_test}.py` 到 `<root>/scripts/qa/`；
  5. `--host grok|all`：复制 `templates/grok-bot/kit-*.md`（新增 6 个源文件，形态见 §4.3）到 `<root>/.agents/grok-bot/`，并把每个文件的 `kit_ref` 填成 kit 的 `git rev-parse HEAD`。
- `--target user`：维持现状路径（`~/.claude/skills`、`~/.claude/agents`，10 个 skill），向后兼容。
- `skills/spec-arch-adapter/SKILL.md:13,16` 与 `cross-review-gate/SKILL.md:42` 的 `~/.claude/...` 绝对路径改为相对 skill 目录 / 相对仓库（`.claude/agents/`）。

**done_when**

| # | 断言 |
|---|---|
| A1 | 空仓库一键装出 §2.3 目录树：9 个 skill、`.claude/skills` 是 symlink 且透过它能看到 9 个、6 个 agent、4 个 `scripts/qa/*.py`、≥6 个适配 skill、`CLAUDE.md` 含 `@AGENTS.md` |
| A2 | 目标项目里 kit 的知识检索可用：`AGENTS.md` 模板承诺的 `python3 -m scripts.qa.*` 在**空项目**上 build 与 search 都 exit 0（kit 根现有脚本已实测满足，只差被 install 复制过去） |
| A3 | `cc-codex-pair` 不进项目目标 |
| A4 | 项目目标内所有 kit 产物无 `~/.claude` / `$HOME/.claude` 绝对路径 |
| A5 | 每个适配 skill ≤30 行、含 `kit_ref: <sha>`、含「审批边界」与「缺失处理」两节 |
| A6 | `--target user` 向后兼容：在**干净** `HOME` 下装满 10 个到 `~/.claude/skills` 且 exit 0（当前实测：1 个、exit 1） |
| A7 | 三宿主 + Grok Bot 实机各验一次（人工，结果写进 PR 描述）：Cursor Customize › Skills 列出 9 个（而非 18，见 V2）；Claude Code `/` 菜单列出 9 个；对该 repo 起一个 Cloud Agent run 执行 `/log-rootcause-triage` 能加载；优化师把 6 个适配 skill 保存进 Bot 后 `/kit-` 前缀列出 ≥6，`/kit-log-triage` 对一份样例日志的 Test run 输出 ≥2 个 hypothesis 且每个带 `file:line` |

A1–A6 验收命令（在 kit 根目录顺序执行；`$T` 贯穿 P0-B/P0-C 的联动断言）：

```bash
# A1
T=$(mktemp -d) && git -C "$T" init -q \
  && bash install.sh --target project --root "$T" --host all \
  && test "$(ls "$T/.agents/skills" | wc -l)" -eq 9 \
  && test -L "$T/.claude/skills" && test "$(ls "$T/.claude/skills/" | wc -l)" -eq 9 \
  && test "$(ls "$T/.claude/agents" | wc -l)" -eq 6 \
  && test "$(ls "$T/scripts/qa/"*.py | wc -l)" -eq 4 \
  && test "$(ls "$T/.agents/grok-bot/kit-"*.md | wc -l)" -ge 6 \
  && grep -q '^@AGENTS.md' "$T/CLAUDE.md" && echo A1-PASS

# A2
( cd "$T" && python3 -m scripts.qa.build_knowledge_db && python3 -m scripts.qa.search x --scope pitfalls ) \
  && echo A2-PASS

# A3
test ! -d "$T/.agents/skills/cc-codex-pair" && echo A3-PASS

# A4（rg 无命中时 exit 1）
rg -n -e '~/.claude' -e '\$HOME/.claude' "$T/.agents" "$T/.claude/agents"; test $? -eq 1 && echo A4-PASS

# A5
for f in "$T"/.agents/grok-bot/kit-*.md; do
  test "$(wc -l <"$f")" -le 30 \
    && grep -Eq '^kit_ref: [0-9a-f]{7,40}' "$f" \
    && grep -q '审批边界' "$f" && grep -q '缺失处理' "$f" || { echo "FAIL $f"; exit 1; }
done && echo A5-PASS

# A6（bash install.sh 本身必须 exit 0，否则 && 链中断）
H=$(mktemp -d) && HOME="$H" bash install.sh --target user \
  && test "$(ls "$H/.claude/skills" | wc -l)" -eq 10 && echo A6-PASS
```

### P0-B　去业务泄漏（来源：REVIEW P0-3；Grok Bot 加重理由见 §8 R2）

**改什么**

- `scripts/qa/build_knowledge_db.py:29`：`MEMORY_DIR` 改为 `--memory-dir` 参数 / `KIT_MEMORY_DIR` 环境变量，默认 `None`（不索引 memory）。
- `skills/spec-arch-adapter/scripts/spec_arch_audit.py:51-52`：删 `src/data/bet365`、`src/data/pinnacle`。
- `skills/tdd-loop-executor/references/one-line-entry-dictionary.md:36-37`：`/Users/pig/project/arbitrage_betting/polyinit/var/logs/runtime.log` 改为 `<project>/var/logs/<service>.log` 占位。
- `templates/ai-workflow.md:66,73,174,542` 与 `skills/spec-arch-adapter/templates/ai-workflow.md` 对应行：删 `runtime_deploy_contract_v1.md`、pig / manager / force-profile、`scripts.docs.check_doc_cursors`。
- `skills/sprint-design-reviewer/SKILL.md:33` 关键词表**本 P0 不动**（属 REVIEW P1-5 拆分范围），但适配 skill 强制 `--type engineering`（§3.3 已定）。
- `skills/cc-codex-pair/**` 的示例泄漏（`sniper.py`、`live_moneyline.py`、`devpig`…）**本 P0 不动**：它不进项目目标（A3），随 REVIEW P1-4 三分一并处理。

**done_when**

| # | 断言 |
|---|---|
| B1 | kit 内会进入项目目标的所有文件零业务词（排除 `architecture/`、`skills/cc-codex-pair/`、`skills/sprint-design-reviewer/`、`README.md` 四处已另行处置的范围） |
| B2 | `README.md` 中 polyinit 只剩致谢一处 |
| B3 | `build_knowledge_db` 源码中不再出现任何 home 下的 memory 绝对路径；在无该目录的机器上照常 exit 0 |
| B4 | A1 装出的目标项目 `$T` 内零业务词 |

验收命令：

```bash
# B1（rg 无命中时 exit 1）
rg -n -i -e polyinit -e '/Users/pig' -e bet365 -e pinnacle -e sniper -e live_moneyline \
  -e devpig -e probe-nba -e 'frozen denylist' -e runtime_deploy_contract -e check_doc_cursors \
  -e backtest-skill -e 'arbitrage.betting' \
  --glob '!architecture/**' --glob '!skills/cc-codex-pair/**' \
  --glob '!skills/sprint-design-reviewer/**' --glob '!README.md' . ; test $? -eq 1 && echo B1-PASS

# B2
test "$(rg -c -i polyinit README.md)" -le 1 && echo B2-PASS

# B3
rg -n -e 'Users-pig' -e '\.claude/projects' scripts/qa/build_knowledge_db.py; test $? -eq 1 \
  && ( cd "$T" && python3 -m scripts.qa.build_knowledge_db >/dev/null ) && echo B3-PASS

# B4
rg -n -i -e polyinit -e bet365 -e pinnacle -e '/Users/pig' "$T/.agents" "$T/.claude" "$T/scripts"; test $? -eq 1 && echo B4-PASS
```

### P0-C　幽灵脚本对齐（来源：REVIEW P0-1 + P0-2 前半）

**改什么**

- `skills/tdd-loop-executor/SKILL.md:24-28`、`skills/sprint-close-auditor/SKILL.md:43-45`：`PYTHONPATH=. python3 scripts/build_pitfalls_index.py` → `python3 -m scripts.qa.build_knowledge_db`；「读 `docs/qa/pitfalls_index.md`」→ `python3 -m scripts.qa.search "<sprint 关键词>" --scope pitfalls`；删 `docs/solutions/` 引用（kit 未定义该目录）。
- `README.md:305-314` 删 tmux 段；`:343-344` 文件树删 `codex-pair.sh`、`codex-done-watcher.sh`。
- `templates/hooks.json:10,21,32,43`：删 3 条 tmux 拦截规则，第 1 条 echo 去掉「调用 Codex 必须通过 scripts/codex-pair.sh send」。
- `skills/tdd-loop-executor/references/one-line-entry-dictionary.md:25`：删「查看当前 acpx session 状态」。
- `skills/cc-codex-pair/tests/acceptance.sh:65` AC4 扫描范围扩到 `README.md`、`templates/`、`skills/*/references/`。

**done_when**

| # | 断言 |
|---|---|
| C1 | skill 正文、模板、README 不再引用不存在的 `build_pitfalls_index.py` / `pitfalls_index.md` / `docs/solutions/` |
| C2 | tmux / acpx / `codex-pair.sh` 时代残留在 README、templates、全部 SKILL.md 与 references 中清零（`cc-codex-pair/SKILL.md` 中的「❌ NEVER tmux」否定句按 `acceptance.sh` AC4 同样规则排除） |
| C3 | `acceptance.sh` AC4 扫描范围扩到 README / templates / references 后仍 PASS（AC4 / AC8 / AC12 是静态段，不需 codex 在线） |
| C4 | A1 装出的目标项目里，SKILL.md 中出现的每个 `scripts.qa.<mod>` 都能 `import` |
| C5 | Grok Bot 侧不会因幽灵脚本触发「绕过」（人工）：对 `$T`（无 sprint doc 的空项目）跑一次 `/kit-sprint-close` Test run，transcript 中 Bot 报告「缺失」而不是自行发明索引脚本；transcript 内不出现 `build_pitfalls_index` |

验收命令：

```bash
# C1（rg 无命中时 exit 1）
rg -n -e build_pitfalls_index -e 'pitfalls_index\.md' -e 'docs/solutions' skills/ templates/ README.md
test $? -eq 1 && echo C1-PASS

# C2：复用 acceptance.sh 的 BANNED 正则与否定句排除规则，范围从单个 SKILL.md 扩到全 kit
BANNED='codex-pair\.sh|capture-pane|paste-buffer|tmux-bridge|done-watcher|load-buffer|\bsmux\b|\bprewarm\b|esc to interrupt|tmux (split|send|capture|paste|new-window|kill)|(^| )acpx '
rg -n -e "$BANNED" README.md templates/ skills/*/SKILL.md skills/*/references/ \
  | rg -v -e '❌|NEVER|严禁|无需|不需要|不再有|没有|no tmux|NO tmux' ; test $? -eq 1 && echo C2-PASS

# C3
bash skills/cc-codex-pair/tests/acceptance.sh 2>&1 | rg -q 'PASS: AC4' && echo C3-PASS

# C4
( cd "$T" && for m in $(rg -o -N 'scripts\.qa\.[a-z_]+' .agents/skills | sort -u | sed 's/.*://'); do
    python3 -c "import $m" || { echo "FAIL $m"; exit 1; }
  done ) && echo C4-PASS
```

**三个切片的顺序与依赖：** P0-C 先做（否则 A2/C4 必失败）→ P0-B → P0-A（A1–A6 一次性验收）。三个切片都不改任何 skill 的 Workflow 步骤语义，只改路径、命令名、示例词。

---

## 6. 与工作流优化师 ROLE_MAP 的交接面

ROLE_MAP 是 Grok Bot 侧的角色分工表（本仓库不含其正文；`architecture/QA-nightshift-investment.md` 引用了它的「不互相顶班」规则）。本节只定义 **kit ↔ 工作流优化师** 这一条边，不碰 Night Shift / 投资日报。

### 6.1 所有权矩阵

| 变更对象 | Owner（谁改） | 在哪改 | 门禁 | 证据留在哪 |
|---|---|---|---|---|
| kit 方法论、`skills/*/SKILL.md`、`templates/`（含适配 skill 源文件 `templates/grok-bot/kit-*.md`）、`install.sh`、`scripts/qa/` | **kit 维护者**（Jimmy 在 CC / Cursor 中执行，或委派 Cloud Agent） | `licett/ai-workflow-kit` PR | kit 自己的 `cross-review-gate` Standard；改 `templates/AGENTS.md` 或 Gate precedence 视为 T3 走 Full | PR + `acceptance.sh` + §5 done_when 输出 |
| **Bot 人设**（description：角色、默认项目、审批边界、Gate precedence 引用、kit 入口协议句） | **工作流优化师** | Grok Bot › Edit Profile | 人设 = 长期规则，改动前后文本贴给 Jimmy 确认 | 人设全文 diff 贴到 kit repo issue（标签 `grok-bot-persona`） |
| **适配 skill 同步**（把项目内 `.agents/grok-bot/kit-*.md` 保存进 Bot skill 库） | **工作流优化师**（可让 Bot 自己「从写好的指令创建 skill」） | Grok Bot 会话 → Settings › Plugins › Yours 启用 | 逐字保存，不改写；Bot 库副本的 `kit_ref` 必须等于项目文件内的 `kit_ref` | Bot skill 文本含 `kit_ref` |
| **routines**（触发源、匹配词、时区、审批点、缺失处理） | **工作流优化师** | Bot › View conversation details › Routines | 新建 / 改动后必须 Test run（安全输入）；写操作留在审批后 | Run history |
| **Gate precedence 定义** | kit（`templates/AGENTS.md` 唯一定义） | kit PR | `rg -n "Gate precedence" templates/ skills/` 恰 1 处定义 | — |
| Bot 侧发现 kit 缺陷 / 幽灵脚本 / 泄漏 | 优化师**只能提 issue 或 draft PR**，不直接改 skill 正文 | kit repo issue（标签 `from-grok-bot`） | kit 维护者 triage 进 REVIEW 路线图 | issue 链接 |
| 共享计算机上的 git 凭据、`/workspace/<project>` clone | 优化师（申请）+ Jimmy（授权） | Grok Bot secure secret request | 细粒度 token：仅 push 到 `grok/*` 分支；merge 由分支保护禁止 | 无（凭据不入任何文档） |

### 6.2 不顶班规则（与 ROLE_MAP 同构）

- kit 维护者**不改** Bot 人设、routine；发现 Bot 行为偏差 → 在 kit 侧改 skill 正文或适配 skill 源文件，再由优化师同步。
- 优化师**不改** `skills/*/SKILL.md`；发现 kit 缺陷 → issue。优化师可以改的只有三样：人设、routine、适配 skill 在 Bot 库中的那份（且必须与源文件一致）。
- 两边都不改对方的产物 = 漂移只可能出现在「适配 skill 源文件 vs Bot 库副本」这一条边上，因此只需一个漂移检查（§6.3）。

### 6.3 漂移检查（优化师拥有的一条 routine）

- 触发：schedule，每周一。
- 动作：先 `git -C /workspace/<project> pull --ff-only`；然后对每个已启用的 `kit-*` skill，比较 Bot 库副本的 `kit_ref` 与 `/workspace/<project>/.agents/grok-bot/<同名>.md` 的 `kit_ref`；不一致 → 在优化师会话提醒「适配 skill 需重新同步」，附两份文本的 diff；项目内缺该文件 → 提醒「kit 已移除该适配 skill，考虑在 Bot 中停用」。
- 只比较 `kit_ref` 与全文，不解释语义；不自动重新保存 skill（保存 = 改 Bot 配置，留给人）。
- 这条检查只需项目 checkout，不需要 kit 仓库在 Grok Bot 计算机上。

### 6.4 交接节奏

| 事件 | kit 侧动作 | 优化师动作 |
|---|---|---|
| kit 打 tag `kit-vX.Y`（或 `templates/grok-bot/` 有变更合入 master） | 在 release note 列出「适配 skill 变更 / 人设建议变更」；目标项目重跑 `install.sh --target project` 并合入 | 项目 checkout 更新后 48 小时内重新同步适配 skill；人设改动经 Jimmy 确认后生效 |
| Bot Run history 出现连续 2 次 `Blocked` / 失败且原因指向 kit 文本 | triage issue，必要时热修 skill 正文 | 提 issue，附 Run request ID |
| 新目标项目接入 | `install.sh --target project --host all` 并合入该项目 | 在人设里加默认项目路径；clone 到 `/workspace/<project>` |

---

## 7. 非目标

- **不重写全部 skill 正文。** REVIEW §1 的「保留 / 改 / 合并 / 拆」路线不变；本 ADR 只加入口层与三个 P0。
- **不合并 Night Shift / 投资日报**，也不让它们读 kit；PR #1 的结论（不合并、握手文件单向）不受本文影响。工作流优化师与它们「不互相顶班」。
- 不在本 ADR 内落地 REVIEW P1-3（review 降本）、P1-4（cc-codex-pair 三分）、P1-5（策略面板拆出）、P1-9（hooks 双格式）、P2-4（plugin 打包）；它们是 P0 之后的下一批，优先级不变。
- 不依赖任何非官方 Grok Bot CLI / API（社区 `grok-bot-skill` 之类）做同步；同步动作全部走官方「从指令创建 skill」路径。
- 不给 Grok Bot 任何 merge、生产配置、保护分支写权限；不把 T3 Pack 交给 Grok Bot。
- 不改 `skills/*/SKILL.md`（本 ADR 交付物只有本文件）。

---

## 8. 后果、风险与待验证

### 8.1 后果

- 正面：四个宿主读同一份 `.agents/skills/` + `AGENTS.md`，「kit 只在 Jimmy 本机存在」（REVIEW C1）被消除；Grok Bot 成为 CC/Cursor 的天然跨模型对抗方，`cc-codex-pair` 的传输层价值进一步下降，加速 P1-4。
- 负面：`install.sh` 从 80 行变成带参数的安装器；每个目标项目多出 `.agents/`、`.claude/`、`scripts/qa/` 三处 kit 产物；Grok Bot 多出 6 个适配 skill + ≥3 条 routine 需人维护。

### 8.2 风险

| # | 风险 | 缓解 |
|---|---|---|
| R1 | 共享计算机上的 git 凭据被任何 Bot 使用 | 细粒度 token 仅限 `grok/*` 分支 push；分支保护禁 merge；凭据只经 secure secret request 进入 |
| R2 | Grok Bot memory 把业务泄漏词（polyinit / bet365 / frozen denylist）记成「项目事实」并跨项目复用 | P0-B 先于适配 skill 同步完成；人设写明「项目事实只以仓库文档为准，不写入 memory」 |
| R3 | routine 对每个 PR 跑 review 烧掉周用量 | 只跑 Lite / Standard；listener 匹配词 narrow；Full 仅人触发 |
| R4 | 适配 skill 与源文件漂移 | §6.3 漂移检查 + `kit_ref` |
| R5 | Grok Bot 遇到缺失文件「绕过」而非报告 | 适配 skill 必填「缺失处理」；C5 验收 |

### 8.3 待验证（每项给验证方法；结果回填本表，不改架构）

| # | 待验证 | 若为真 | 若为假 | 验证方法 |
|---|---|---|---|---|
| V1 | Grok Bot 云端计算机是否像 Grok Build 一样原生扫 `.agents/skills/` / `.grok/skills/` 并读 `AGENTS.md`（目前只在 Grok Build CLI 文档中出现） | 适配 skill 缩为一行「用仓库 skill」，`/` 菜单直接可见 | 维持 §4.3 形态 | 在 `/workspace/<project>` 放一个 `.agents/skills/probe/SKILL.md`，问 Bot「你能看到 probe skill 吗」，并检查 `/` 菜单 |
| V2 | Cursor 对 `.agents/skills/` 与 symlink 的 `.claude/skills/` 同名 skill 是否去重 | 保持 symlink | `--host claude` 改为 copy + CI `diff -r` 校验一致 | Cursor Customize › Skills 计数应为 9 而非 18 |
| V3 | Claude Code 是否跟随 `.claude/skills` 目录 symlink | 保持 | 改 copy | Claude Code `/` 菜单列出 9 个 |
| V4 | Grok Bot「GitHub 通知」触发的 routine 收到的 payload 字段（PR 号、分支、diff URL） | 直接用事件字段 | 退到 webhook：GitHub webhook → routine POST URL（Bearer key），JSON body 自带 PR 字段 | 建一条 Test routine 打印收到的 body |
| V5 | Grok Bot 计算机默认镜像是否含 `python3` ≥3.8（`sqlite3` FTS5）与 `git` | 直接跑 `scripts.qa` | 人设加「首次任务先 `apt`/`pip` 装依赖」；注意手装包在 Reset 后丢失 | `python3 -c "import sqlite3;print(sqlite3.sqlite_version)"` |

---

## 9. 本 ADR 的验收清单

| # | Jimmy 的要求 | 对应章节 | 可验收点 |
|---|---|---|---|
| 1 | 多宿主目标态：各宿主读路径与入口 | §2.1 矩阵、§2.3 目录树 | 每个宿主一行，区分原生 / 兼容 / 待验证；Grok Bot 一行含「账户侧 skill 库」「共享 `/workspace`」「无 hooks」 |
| 2 | Layer1 复用 + skill 必装 / 可选 / 禁装 | §3.1、§3.3 | 10 个 skill 各有判定、理由、前置；禁装理由命中「CC-only 传输 / tmux / 冻结 codex 拷贝」三条 |
| 3 | Grok Bot 落地形态 + 最小映射表 | §4.1–4.4 | 8 行映射表覆盖 Ask→Code / TDD / cross-review-gate / sprint-close；每行有触发、审批边界、证据 |
| 4 | P0 切片 ≤3，每项 done_when | §5 | 恰 3 项；每项 ≥4 条可执行断言，命令可在 kit 根目录直接跑 |
| 5 | 与优化师 ROLE_MAP 的交接面 | §6 | 所有权矩阵明确「谁改 kit、谁改人设」；不顶班规则；一条漂移检查 routine |
| 6 | 非目标 | §7 | 含「不重写全部 skill 正文」「不合并 Night Shift / 投资日报」 |
| — | 不改 `skills/*/SKILL.md` | 本 PR diff | `git diff --stat master...HEAD` 只含 `architecture/ADR-004-multi-host-grok-bot.md` |
| — | Jimmy 否决记录 | §0.2 | 5 条，指明作废的是 REVIEW §0 末段 |

---

## 10. 证据索引

内部（行号基于 `6d53534`）：

- `install.sh:3,7,50,55,70`（仅 `~/.claude/*`；`set -euo pipefail` + `((installed++))` 在干净 HOME 下实测只装 1 个 skill、exit 1）；`README.md:3,269,305-314,343-344`
- `templates/AGENTS.md:26`（`scripts.qa.search`）、`:94-99`（CC-Codex 段）；`templates/hooks.json:10,21,32,43`
- `skills/tdd-loop-executor/SKILL.md:18,24-28,31,72`；`references/one-line-entry-dictionary.md:25,36-37`
- `skills/sprint-close-auditor/SKILL.md:43-45`
- `skills/cross-review-gate/SKILL.md:27-31`（tier 表）、`:42,52`（`~/.claude/agents/`、Agent tool）
- `skills/spec-arch-adapter/SKILL.md:13,16`；`scripts/spec_arch_audit.py:51-52,114`
- `skills/sprint-design-reviewer/SKILL.md:33`
- `skills/project-roadmap-research/SKILL.md:22`
- `skills/cc-codex-pair/SKILL.md:238,272,346-348`（`$HOME/.claude/skills`、`run_in_background`、task-notification）；`PROVENANCE.md:3-10,25-28`；`tests/acceptance.sh:65`
- `scripts/qa/build_knowledge_db.py:29`
- `architecture/REVIEW-skills-era-fit-2026-09-20.md` §0 末段、§3 P0-1/P0-2/P0-3/P1-1/P1-3/P1-4/P1-5/P1-6/P1-7/P1-8/P1-9/P2-4/P2-5/P2-6、§4.3（PR #2 分支）
- `architecture/QA-nightshift-investment.md:12,37,75,107`（ROLE_MAP 不顶班；PR #1 分支）

外部（2026-09-20 抓取）：

- Cursor「Work with Grok Bot」`cursor.com/docs/grok-bot/work`：Bot / skill / routine 三层；skill 账户侧保存、按 Bot 启用、`/` 引用；共享云端计算机与 `/workspace`；Bot 间 handoff 与 2–6 Bot 群聊；routine ≤50 条 / 20 条运行记录；Cursor 账户集成可由 Slack / GitHub 事件触发 routine；Test run 会做真实工作；本机执行走独立 local execution policy
- Cursor「Routines」`cursor.com/help/grok-bot/routines`：schedule / Slack listener（containing 大小写不敏感、narrow 建议）/ webhook（POST URL + Bearer key，200 = 已启动非已完成）
- xAI「Grok Bot」`docs.x.ai/grok-bot/overview`：所有 Bot 共用一台计算机；memory 保留稳定偏好与摘要
- xAI「Skills, Plugins & Marketplaces」`docs.x.ai/build/features/skills-plugins-marketplaces`：**Grok Build（CLI）**扫 `./.grok/skills/`、`~/.grok/skills/`、`~/.agents/skills/`，读 `AGENTS.md` 族与 Claude Code 全部路径——**仅证明 Grok Build，不证明 Grok Bot**（→ V1）
- Cursor「Agent Skills」`cursor.com/docs/skills`、`cursor.com/help/customization/skills`：`.agents/skills/`、`.cursor/skills/` 原生；`.claude/skills/`、`.codex/skills/` 兼容；仅 `~/.cursor/skills/` 可 Sync 到 Cloud；`~/.agents/skills/` 与未同步个人 skill 不进 Cloud / SSH / self-hosted
- Claude Code「Skills」`code.claude.com/docs/en/skills`：项目 skill 仅 `.claude/skills/`；个人 `~/.claude/skills/`；不列 `.agents/skills/`；`AGENTS.md` / `.agents/skills/` 原生支持为开放 issue [#31005](https://github.com/anthropics/claude-code/issues/31005)、[#34235](https://github.com/anthropics/claude-code/issues/34235)

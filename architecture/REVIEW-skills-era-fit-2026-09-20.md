# ai-workflow-kit Skill 体系时代适配审读（架构师结论）

> 范围：`licett/ai-workflow-kit` master @ `6d53534`。读了 README、10 个 `skills/*/SKILL.md` 及 references、`agents/*.md`、`templates/`、`install.sh`、`scripts/qa/`、`skills/cc-codex-pair/{scripts,tests,PROVENANCE.md}`。不审 Night Shift（`cursor/qa-nightshift-investment-edb2` 分支只多一份业务 QA 文档，已忽略）。
> 对照现实：Cursor 官方文档（skills / subagents / cloud-agent / hooks / grok-bot）、Claude Code skills 文档、Codex skills + AGENTS.md 文档、`openai/codex-plugin-cc` 仓库，均为 2026-09 抓取。凡未从文档证实的，文中标"待验证"。
> 日期：2026-09-20。只新增本文件，不改 skills 正文。

---

## 0. 总判

**部分过时，需重构而非重写。** 置信度：方法论层 0.85，skill 层 0.75。

| 层 | 判定 | 一句话 |
|---|---|---|
| Layer 1 方法论（Ask→Code / Sprint+Pack / TDD-first / 编码前避坑检索 / 文档闭环 / 证据纪律） | **仍适合，且比 2025 更适合** | agent 越自主，越需要 DoD、scope、证据、pitfalls 这类外部约束；这一层是 kit 的真正资产 |
| Layer 2 约束（AGENTS.md / pitfalls / sprint 模板 / tests_guideline） | **适合，需去 CLAUDE.md 中心化** | Cursor Cloud、Codex、Grok Bot 全部读 `AGENTS.md`；CLAUDE.md 只剩 Claude Code 一家 |
| Layer 3 Skills（10 个） | **4 个保留、2 个改、2 个合并、2 个拆** | 平台内建能力（Cursor `/review` 系列、Claude `/code-review`、Codex `/codex:review`、subagent 模型钉死）已吃掉"多专家 review 编排"和"跨模型传输层"两块，kit 的差异化只剩"项目知识注入 + 闸门语义 + 证据纪律" |

判定依据的三个硬事实：

1. **安装路径已经不通向云端。** `install.sh:7` 只写 `~/.claude/skills`。Cursor 文档明确：Cloud Agents / 远程 SSH / 自托管 worker 不读本机 home；只同步 `~/.cursor/skills/`，项目级要用 `.cursor/skills/` 或 `.agents/skills/`。Claude Code 文档同样：云会话与 routines 不读 `~/.claude/skills/`，只读仓库内 `.claude/skills/`。也就是说，**当前 kit 在任何云端执行面上都是不可见的**。
2. **传输层已被官方产品替代。** `cc-codex-pair` 把 `openai/codex-plugin-cc` 冻结拷贝进仓库（`PROVENANCE.md:3-10,25`，自认"一次性冻结、不跟踪"）。而官方插件本身就提供 `/codex:review`、`/codex:adversarial-review`、`/codex:rescue --background`，Cursor 侧则可以用 `.cursor/agents/*.md` 的 `model:` + `force-default-model: true` 直接钉一个 Codex 模型子代理。kit 的价值在**结对协议**，不在**传输实现**。
3. **kit 内部已经自相矛盾。** HEAD 提交把 cc-codex-pair 迁到 app-server，但 README `:305-314`、`templates/hooks.json:10-43`、`one-line-entry-dictionary.md:25` 仍在讲 `codex-pair.sh` / tmux / acpx，且 README 文件树列出的 `scripts/codex-pair.sh`、`codex-done-watcher.sh` 在仓库里不存在。`tdd-loop-executor:24-28` 与 `sprint-close-auditor:43-45` 调用的 `scripts/build_pitfalls_index.py`、`docs/qa/pitfalls_index.md`、`docs/solutions/` 也都不存在，而 kit 实际交付的是 `scripts/qa/build_knowledge_db.py`。

推翻本总判的条件：若 Jimmy 明确只在本机 Claude Code 里用这套东西、不上 Cloud Agent、不用 Grok Bot、不换 Codex 传输，则 §3 的 P1-1 / P1-4 / P1-9 / P2-4 降级为可选，总判改为"仍适合，做 P0 止血即可"。

---

## 1. 逐 Skill 判定表

判定含义：**保留** = 小改；**改** = 语义不变、结构/触发/成本要动；**合并** = 并入他处；**拆** = 一个变多个；**弃** = 删除或降为引用。

| Skill | 判定 | 一句话理由 |
|---|---|---|
| `tdd-loop-executor` | **保留（改 2 处）** | Ask→Code + TDD + progress 游标是核心闭环，语义没过时；但 `:24-28` 调的 `build_pitfalls_index.py` / `pitfalls_index.md` / `docs/solutions/` 不存在，要换成 `scripts.qa.*`；`sN go` 这种命令式触发应加 `disable-model-invocation: true` |
| `sprint-close-auditor` | **保留（改 1 处）** | 对账 doc↔code↔test 的收口审计是平台没有的能力；同样修掉 `:43-45` 的幽灵脚本，把"Compound knowledge"输出改指向 `scripts.qa.build_knowledge_db` |
| `log-rootcause-triage` | **保留** | 59 行、传输无关、无业务泄漏，是 kit 里最"标准 SKILL.md"的一个；只需把 `references/patterns.md` 里的 grep 起手式补一条 `jq`/JSON log |
| `spec-arch-adapter` | **保留（改 3 处）** | 文档骨架生成器是新项目上手的唯一入口；但 `spec_arch_audit.py:51-52` 的 `src/data/bet365`、`src/data/pinnacle` 是业务泄漏；`templates/` 与 `skills/spec-arch-adapter/templates/` 两份模板已漂移（见 §2 C7）；应顺手生成 `.agents/skills/` 与 AGENTS.md 的"Cursor Cloud specific instructions"段 |
| `cross-review-gate` | **改（降本 + 接平台）** | tier 分级思路正确，但 Full 档 = 5 专家 + 3 次交叉质疑 = 8 个 subagent 上下文；Cursor 文档明说 5 个并行 subagent ≈ 5× token。平台已有 `/review`、`/review-bugbot`、`/review-security`（Cursor）、`/code-review`（Claude）、`/codex:review`。kit 应保留 **tier 规则 + 合并/分类格式 + QA Lead 否决语义**，把"某一路 review 的原始 findings 来源"允许换成平台内建 |
| `sprint-design-reviewer` | **拆** | engineering panel（Axis A-E）通用、保留；strategy / hybrid panel（S1-S4、PnL / kelly / wallet / regime 关键词表 `:33`）是 polyinit 量化业务，占该文件一半以上，应拆成独立 domain skill/plugin，让 kit 回到"通用" |
| `adversarial-cross-model-review` | **改（重定位）** | 核心纪律（每条 verdict 必须读源码、反转假设、Adopt/Partial/Reject/Defer）非常好；但触发假设"用户手工粘贴 GPT/Gemini 结论"（`:3`、`:13-16`）已过时——现在外部 findings 主要来自 Bugbot PR 评论、Codex `adversarial-review`、Cursor `/review` 子代理。应改名或改 description 为"外部/自动化 review findings 验证器" |
| `code-review-expert` | **合并（skill 弃，agent 留）** | skill 正文 86 行与 Cursor `/review`、Claude `/code-review`、Codex `/codex:review` 功能重叠；但 `agents/code-review-expert.md` 定义的 `[Px][confidence] file:line` 格式是其他 5 个 agent 的基准，必须留。另外 skill 与 agent 同名 `code-review-expert`，在 Cursor 里 `/code-review-expert` 会同时命中 skill 与 subagent，需改名其一 |
| `project-roadmap-research` | **合并入 `spec-arch-adapter --mode audit`，或弃** | 只读探索已被 Cursor Explore subagent / Claude Explore agent 覆盖；且 `:22` 以 `CLAUDE.md` 为项目根标记，对只有 `AGENTS.md` 的项目（Cursor / Codex / Grok Bot 标准）直接失效。唯一独有价值是 `<!-- CLAUDE:ROADMAP -->` 受控块回写，可作为 adapter 的一个子命令 |
| `cc-codex-pair` | **拆（协议 / 传输 / 事故日志三分）** | 1111 行、62 KB，一次调用就把 ~15k token 永久钉进主上下文；内容一半是 2026-03-22 / 04-11 / 05-10 / 06-14 四次事故的复盘与 MANDATORY 清单（`:35`、`:493`、`:532`、`:324`）；传输层是冻结拷贝；示例满是 `sniper.py` / `live_moneyline.py` / `devpig` / `polyinit/execution/models.py`（`:68`、`:408`、`:779`、`:936`）。结对协议（给任务不给结论、先独立后比较、共识循环、Pre-CONCEDE 检查）值得保留，但应 ≤200 行且传输无关 |

非 skill 资产：

| 资产 | 判定 | 理由 |
|---|---|---|
| `agents/*.md`（6 个） | **保留，补 Cursor 字段** | 已用 `model: inherit`，Cursor 读 `.claude/agents/` 兼容路径。reviewer 类应加 `readonly: true`（Cursor）；description 里的 "Agent 1/4" 编号与 `cross-review-gate:44-50` 表不一致（qa-lead 写 Agent 4，表里是 Agent 5；correctness 写 Agent 1，表里是 Agent 2），`code-review-expert.md:12,90` 仍说 "4 专家"——直接删编号 |
| `templates/AGENTS.md` | **保留，作为唯一 canonical** | 内容质量高（执行姿态、三红线、T-tier、8 要素）；但要和 adapter 内的另一份合一，并注意 Codex 对 AGENTS.md 链有 32 KiB 上限（当前 115 行安全，别再往里塞 skill 正文） |
| `templates/ai-workflow.md` | **改** | `:66`、`:73` 的 `docs/spec/runtime_deploy_contract_v1.md` / pig / force-profile 与 `:174` 的 `scripts.docs.check_doc_cursors` 都是 polyinit 私货 |
| `templates/hooks.json` | **改（双格式）** | Claude Code 格式；`:10-43` 四处强推 `codex-pair.sh`，与 HEAD 自相矛盾；用了 `if:` 字段，Cursor 第三方 hook 映射表只列事件名与 `matcher`，`if` 是否被映射待验证 |
| `templates/sprint-template.md`、`pitfalls*.md` | **保留** | Truth/Proxy contract、Pack type、early-stop trigger 是这套方法论最有辨识度的部分 |
| `scripts/qa/*.py`（FTS5 检索） | **保留（改 1 处）** | 零依赖、双索引、alias 重写，比让 agent 每次 `rg` 强；`build_knowledge_db.py:29` 把 `MEMORY_DIR` 写死为 `-Users-pig-project-arbitrage-betting-polyinit`，改成参数 |
| `install.sh` | **改（多宿主）** | 只有 `~/.claude/skills` + `~/.claude/agents` 一个目标，且不部署 `scripts/qa/`，导致 AGENTS.md 模板里的 `python3 -m scripts.qa.search` 在新项目上 module not found |
| `examples/` | **改** | `workflow-diagram.md:29` 仍是"4 专家"；e2e 全程假设 Claude Code |

---

## 2. 与现栈的冲突点

编号 C1-C10，每条给证据、为何冲突、影响面。

### C1 Claude Code-only 假设已渗透到每一层

| 证据 | 内容 |
|---|---|
| `README.md:3` | "一套面向 **Claude Code** 用户的开发流程工具包" |
| `install.sh:7,55` | 目标只有 `~/.claude/skills`、`~/.claude/agents` |
| `cross-review-gate:42,52` | "see `~/.claude/agents/`"、"使用 Agent tool，`subagent_type` 指定" |
| `cc-codex-pair:198,346` | "Claude Code 有自动压缩机制"、"Bash 工具 `run_in_background:true` … harness 主动给 CC 推 task-notification" |
| `project-roadmap-research:22` | 以 `CLAUDE.md` 判定项目根 |
| 各 skill 首步 | 17 处 "Read `CLAUDE.md` first"（`rg -c` 统计） |

冲突：Cursor 本地会读 `.claude/skills`、`.claude/agents` 做兼容，所以**本地**大体能跑；但 Cursor Cloud Agent、Claude 云会话、Codex、Grok Bot 四个执行面全部**只读仓库内**的 `.agents/skills` / `.cursor/skills` / `.claude/skills` 与 `AGENTS.md`。kit 现状等于"只在 Jimmy 本机的 Claude Code 里存在"。

影响：P1-1、P1-6。

### C2 模型名写死

| 证据 | 内容 |
|---|---|
| `README.md:269` | "Claude Code (Opus) 当大脑，OpenAI Codex (GPT-5.4) 当双手" |
| `skills/cc-codex-pair/skills-ref/gpt-5-4-prompting/` | 目录名带模型版本 |
| `scripts/codex-companion.mjs:70` | `MODEL_ALIASES spark → gpt-5.3-codex-spark` |
| `agents/*.md` | `model: inherit`（这是对的） |

冲突：Cursor subagent 文档给出的模型槽位已是 `claude-opus-5[effort=high]`、`gpt-5.6-sol` 一类，且论坛确认 `model:` 只是默认值，父代理可覆盖，需 `force-default-model: true` 才钉死。kit 文本里的 Opus / GPT-5.4 已经是两代前的名字，读者会误以为协议绑定特定模型。

影响：P0-6。

### C3 双 review 闸门成本

一次 `cc-codex-pair sN` 完整周期的 review 开销（按 SKILL.md 字面规则统计）：

| 阶段 | 开销 |
|---|---|
| Phase 1 | `sprint-design-reviewer` 3-4 专家 + 2-3 步交叉质疑（3-7 个 subagent）+ Codex 独立审 + 交换 + 共识 ≤5 轮 |
| Phase 3 | `cross-review-gate` Full = 5 专家 + 3 次交叉质疑（8 个 subagent）+ Codex 独立审 + 交换 + 共识 ≤5 轮 |
| Phase 4 | `cross-review-gate --recheck`（再 8 个）× ≤2 轮 |
| Phase 5 | Codex GO/NO-GO ≤3 轮 + `sprint-close-auditor` |
| 常驻 | 62 KB `cc-codex-pair` SKILL.md 全程钉在主上下文（Claude Code 文档：skill 内容进入会话后不再卸载） |

粗算：一个 sprint ≥ 25 个 subagent 上下文 + 10-20 个 Codex turn，**在写第一行代码之前**。而 Cursor 文档明确 5 个并行 subagent ≈ 5× token；平台内建的 `/review-bugbot`、`/review-security`、`/code-review`、`/codex:review` 已经各自是一个专家路径。kit 现在是在平台专家之上再叠一层自建专家，然后再叠一层跨模型共识。

冲突不在"要不要多视角"，而在"多视角的原始产出该不该都由 kit 自己 spawn"。

影响：P1-3、P1-4。

### C4 三头否决，优先级未定义

| 证据 | 谁有否决权 |
|---|---|
| `agents/reviewer-qa-lead.md:101`、`cross-review-gate:235` | QA Lead Block 覆盖一切 |
| `sprint-design-reviewer:349` | Risk Manager 对 rollout safety 有 veto |
| `cc-codex-pair:712,982`、`templates/AGENTS.md:99` | Codex 对可行性（Phase 1）和 merge（Phase 5）有 veto |
| `cc-codex-pair:943-944` | Codex GO 之后才跑 `sprint-close-auditor`，auditor 若 `Blocked` 怎么办——未写 |

冲突：三个否决者来自三个 skill，没有一处写谁压谁。agent 会在 Phase 5 陷入"Codex 说 GO、auditor 说 Blocked"的死区。

影响：P1-8。

### C5 幽灵脚本与两套知识检索

| 调用方 | 调用的东西 | 是否存在 |
|---|---|---|
| `tdd-loop-executor:24-28`、`sprint-close-auditor:43-45` | `scripts/build_pitfalls_index.py`、`docs/qa/pitfalls_index.md`、`docs/solutions/` | 否 |
| `README.md:286-294`、`templates/AGENTS.md:26`、`templates/hooks.json:66` | `python3 -m scripts.qa.build_knowledge_db` / `search` | 是（在 kit 根 `scripts/qa/`），但 `install.sh` 与 `spec_arch_audit.py` 都不把它部署到目标项目 |

冲突：agent 按 skill 指令跑 `build_pitfalls_index.py` 会立即失败，然后要么跳过"编码前避坑检索"这条强制项，要么自己发明一个。kit 最核心的机制被自己的 skill 绕过了。

影响：P0-2。

### C6 传输层残留自相矛盾

HEAD `6d53534` 标题即"传输层 tmux → vendored Codex app-server"，`tests/acceptance.sh:65` 把 `codex-pair.sh|capture-pane|tmux …|acpx` 列为禁词并只对 SKILL.md 校验。但：

| 残留位置 | 内容 |
|---|---|
| `README.md:305-314` | 整段 "CC-Codex 通信层：tmux-based … `scripts/codex-pair.sh send/read/alive/prewarm`" |
| `README.md:343-344` | 文件树列出 `codex-pair.sh`、`codex-done-watcher.sh`（仓库中不存在） |
| `templates/hooks.json:10,21,32,43` | 四处 `[BLOCKED] Use scripts/codex-pair.sh send` |
| `one-line-entry-dictionary.md:25` | "查看当前 acpx session 状态" |

冲突：一个新用户按 README 装完，hooks 会强迫 agent 去调一个不存在的脚本。

影响：P0-1。

### C7 模板双源漂移 + 业务泄漏

`diff templates/ai-workflow.md skills/spec-arch-adapter/templates/ai-workflow.md` 有 20+ 处差异，`diff templates/AGENTS.md skills/spec-arch-adapter/templates/AGENTS.md` 差异更大；`spec_arch_audit.py:114` 还内嵌了**第三份** AGENTS.md 模板（仅作 fallback，但仍是第三个真相源）。泄漏项：

| 位置 | 泄漏内容 |
|---|---|
| `templates/ai-workflow.md:66,73` | `docs/spec/runtime_deploy_contract_v1.md`、runtime / pig / manager / force-profile |
| `templates/ai-workflow.md:174,542` | `python -m scripts.docs.check_doc_cursors`（kit 没有） |
| `spec_arch_audit.py:51-52` | `src/data/bet365`、`src/data/pinnacle` |
| `build_knowledge_db.py:29` | `-Users-pig-project-arbitrage-betting-polyinit` |
| `one-line-entry-dictionary.md:36-37` | `/Users/pig/project/arbitrage_betting/polyinit/var/logs/runtime.log` |
| `cc-codex-pair` 多处 | `sniper.py:3324-3343`、`live_moneyline.py`、`frozen denylist`、`tick_size`、`probe-nba`、`devpig`、`backtest-skill`、`polyinit/execution/models.py` |
| `sprint-design-reviewer:24-26,33` 及 `review-axes.md` S1-S4 | 整个量化策略面板 |

冲突：README 自称"通用 Skill"，实际约 30% 文本只对 polyinit 有意义；给 Codex 或 Grok Bot 读到 `frozen denylist: live_moneyline.py` 会直接污染其对当前项目的理解。

影响：P0-3、P1-5。

### C8 SKILL.md 变成事故日志与治理债

`cc-codex-pair` 内含：MAX_ROUNDS=5 共识循环（`:423`）、"Round 1 收到 INSIST 就汇报 = 违规"（`:431`）、6 步 Pre-CONCEDE 机械清单（`:493-528`）、7 项 close 清单（`:532-560`）、META-RULE"改本文件必须先经 Codex 审"（`:562-571`）、"严禁以上下文太长为由停止"（`:198-211`）、"每次回复用户前必须读 state 文件"（`:191`）。

冲突：这些规则每条都有真实事故背书，但堆在一个 SKILL.md 里的后果是：(a) 62 KB 常驻上下文；(b) 规则互相加压——"不得停止"+"必须读 state"+"必须 5 轮"+"必须 7 项清单"，agent 的合规成本超过任务本身；(c) META-RULE 让这个文件在没有 Codex 在线时**不可修改**，包括修它自己的错。Claude Code 文档建议 skill 主体聚焦、细节进 `references/` 按需加载，这正是反例。

影响：P1-4、P2-1。

### C9 触发条件与自动调用失配

| 现状 | 问题 |
|---|---|
| 中文触发短语全部写在正文（如 `cross-review-gate:14-15`、`adversarial:13-16`） | Cursor / Claude / Codex 的自动调用只看 `description`（Claude 还看 `when_to_use`，合计 ≤1536 字符）；正文里的触发词对自动选择无效 |
| 无任何 skill 设 `disable-model-invocation` | `tdd-loop-executor sN go`、`sprint-close-auditor`、`cc-codex-pair` 本质是命令；agent 可能因为用户一句"让 codex 看看"就自动把 62 KB 拉进上下文 |
| skill `code-review-expert` 与 agent `code-review-expert` 同名 | Cursor 中 `/name` 既可触发 skill 也可触发 subagent |
| 无 `paths` | `spec-arch-adapter` 之类不需要；但如果保留量化面板，应用 `paths: docs/sprint/**` 限定 |

影响：P1-2、P2-3。

### C10 hooks 格式与云端不一致

`templates/hooks.json` 是 Claude Code 格式（`PreToolUse` + `if: "Bash(tmux …)"` + `hookSpecificOutput`），依赖 `python3`、`jq`。Cursor 文档：本地可通过第三方 hook 兼容加载 `.claude/settings.json`，事件名自动映射；Cloud Agent **只跑 `.cursor/hooks.json`**（`preToolUse`、`beforeShellExecution`、`afterFileEdit`、`stop` 等）。`if` 字段在 Cursor 映射表中未出现（待验证）。

影响：P1-9。

---

## 3. 优化路线

原则：P0 只做一致性止血，不改任何流程语义；P1 改结构、触发、成本、宿主；P2 做长期形态。每项附可验收标准，验收命令均可在 kit 根目录直接跑。

### P0 一致性止血（不改流程语义）

| # | 动作 | 验收 |
|---|---|---|
| P0-1 | 清除 tmux 时代残留：删 README `:305-314` 段、修 `:343-344` 文件树、重写 `templates/hooks.json` 四处 echo、改 `one-line-entry-dictionary.md:25` | `rg -n -e 'codex-pair\.sh' -e acpx -e done-watcher -e paste-buffer -e load-buffer README.md templates/ skills/*/references/` 返回 0 行；把 `acceptance.sh` AC4 的扫描范围扩到 README 与 templates 后仍 PASS |
| P0-2 | 统一知识检索入口：`tdd-loop-executor:24-28`、`sprint-close-auditor:43-45` 改为 `python3 -m scripts.qa.build_knowledge_db` / `search --scope pitfalls`；`spec_arch_audit.py --mode write` 把 `scripts/qa/` 复制进目标项目（或 install.sh 提供 `--with-scripts`） | `rg -n -e build_pitfalls_index -e 'pitfalls_index\.md' -e docs/solutions skills/` = 0；在空目录 `git init && python spec_arch_audit.py --root . --mode write --profile full && python3 -m scripts.qa.build_knowledge_db && python3 -m scripts.qa.search x` 不报 `No module named scripts.qa` |
| P0-3 | 去业务泄漏：`build_knowledge_db.py:29` MEMORY_DIR 改 `--memory-dir` / `KIT_MEMORY_DIR`；`spec_arch_audit.py:51-52` 删 bet365 / pinnacle；`one-line-entry-dictionary.md:36-37` 改相对占位路径；`templates/ai-workflow.md:66,73,174,542` 删 runtime_deploy_contract / pig / check_doc_cursors；`cc-codex-pair` 示例改 `{module}.py:{L1}-{L2}` 占位 | `rg -n -i -e polyinit -e /Users/pig -e bet365 -e pinnacle -e sniper -e live_moneyline -e devpig -e probe-nba -e 'frozen denylist' -e runtime_deploy_contract -e check_doc_cursors -e backtest-skill --glob '!architecture/**' .` 只剩 README 致谢一处 |
| P0-4 | 对齐专家编号与数量：6 个 `agents/*.md` description 删 "Agent N"；`code-review-expert.md:12,90`、README `:401-402`、`examples/workflow-diagram.md:29` 的 "4" 改为按 tier 描述 | `rg -n -e '4 专家' -e '4 个 agent' -e 'Agent [1-5]\b' agents/ README.md examples/ skills/cross-review-gate/` 为 0 或每处与 `cross-review-gate:44-50` 表一致 |
| P0-5 | 模板单源：以 `skills/spec-arch-adapter/templates/` 为 canonical，`templates/` 目录内 `AGENTS.md`、`ai-workflow.md`、`PROJECT_RULES.md`（若有）改为 symlink 或删除，README 文件树同步；`spec_arch_audit.py:114` 内嵌 AGENTS.md 模板删掉，缺模板时报错而非 fallback | `diff -r templates/ skills/spec-arch-adapter/templates/` 对重名文件为空；`rg -n '"AGENTS.md": """' spec_arch_audit.py` = 0 |
| P0-6 | 模型名去硬编码：README `:269` 改 "CC 当前模型 / Codex 当前模型"；`skills-ref/gpt-5-4-prompting/` 改名 `codex-prompting/`（PROVENANCE 记上游原名）；`acceptance.sh:58` 路径同步 | `rg -n -e Opus -e 'GPT-5\.4' -e gpt-5-4 README.md skills/*/SKILL.md skills/cc-codex-pair/tests/` = 0；`acceptance.sh` AC10 PASS |

### P1 结构重构（改安装、触发、成本、宿主）

| # | 动作 | 验收 |
|---|---|---|
| P1-1 | 多宿主安装：`install.sh --target project` 写入 `<repo>/.agents/skills/`（Cursor + Codex 原生读取），并建 `.claude/skills -> .agents/skills` symlink（Claude Code 读取；Claude Code 是否直接读 `.agents/skills` 待验证）；agents 写入 `<repo>/.claude/agents/`（Cursor 兼容读取，`.cursor/` 优先级更高时不冲突）；保留 `--target user` 走旧路径 | 三宿主各验一次：Cursor Customize → Skills 列出 10 个；Claude Code `/` 菜单列出；`codex` 内 `/skills` 列出。再起一个 Cloud Agent run 对该 repo 执行 `/log-rootcause-triage`，能加载 |
| P1-2 | 触发收敛：`tdd-loop-executor`、`sprint-close-auditor`、`cc-codex-pair`、`spec-arch-adapter`、`project-roadmap-research` 加 `disable-model-invocation: true`；review 类保留自动触发，把正文里的中文触发短语精简后搬进 `description`（Claude 可放 `when_to_use`），总长 ≤600 字符 | 一段 `python - <<'EOF'` 校验脚本：解析全部 SKILL.md frontmatter，断言上述 5 个有该字段、所有 description ≤600 字符、`name` 等于目录名。在 Cursor 输入"帮我看看这个 diff 有没有问题"，只应命中 review 类，不应加载 cc-codex-pair |
| P1-3 | `cross-review-gate` 降本：默认 tier 改 Standard，Full 仅 T3 或显式 `--full`；Phase 3 三次交叉质疑合并为**一次** consolidator（architect 视角）+ QA Lead 单独 Release Readiness；新增 `review_source` 字段，允许 Agent 2/3 的原始 findings 来自平台内建（Cursor `/review-bugbot` / `/review-security`、Claude `/code-review`、Codex `review`），kit 只做归一化 + 合并 + 分类 + 闸门 | Standard 一次运行 subagent spawn ≤4（含 consolidator）；报告 header 出现 `Task tier` 与 `review_source`；同一 diff 在旧 Full 与新 Standard 下 Confirmed P0/P1 集合一致（用 e2e 示例的 csv-dedup diff 做对照） |
| P1-4 | `cc-codex-pair` 三分：(a) `pair-protocol/SKILL.md` ≤200 行、传输无关，只留 5 条原则 + Round 0 + 共识循环（MAX_ROUNDS 5→3）+ Pre-CONCEDE 精简为 3 条 + 否决优先级引用；(b) `references/incident-log.md` 承接 2026-03-22 / 04-11 / 05-10 / 06-14 四段复盘与 7 项清单；(c) `references/transport-*.md` 两个适配：Claude Code 走官方 `/plugin install codex@openai-codex`（`/codex:rescue --background`、`/codex:status`、`/codex:result`），Cursor 走 `.cursor/agents/coder-codex.md`（`model: <codex 槽位>` + `force-default-model: true` + `is_background: true`）；vendored `scripts/` 降为 fallback，保留 `acceptance.sh`；删 META-RULE 或改为"改协议文件需 PR review" | `wc -c skills/pair-protocol/SKILL.md` ≤ 12288；`acceptance.sh` 全 PASS；在 Cursor 用 `coder-codex` subagent 走一遍 Phase 3 Step 1-3 并产出 `Confirmed (mutual)/(CC-verified)/(Codex-raised)` 分类；`rg -n "MANDATORY" skills/pair-protocol/SKILL.md` ≤ 1 |
| P1-5 | `sprint-design-reviewer` 拆 domain：engineering panel（Axis A-E + Execution-Readiness Overlay）留 kit；strategy / hybrid panel、S1-S4 checklist、`:33` 关键词表迁出为 `quant-sprint-review`（独立目录或 plugin），kit 内 `--type strategy` 在未安装时输出 "strategy panel not installed, falling back to engineering" | `rg -n -i -e PnL -e kelly -e wallet -e regime -e sharpe -e drawdown skills/sprint-design-reviewer/` = 0；kit 内 SKILL.md ≤ 220 行；对 e2e 的 sprint1.md 跑 `--type auto` 结果仍为 engineering / Conditional |
| P1-6 | 去 CLAUDE.md 中心化：全部 "Read `CLAUDE.md` first" 改为 "Read `AGENTS.md`（`CLAUDE.md` 若存在仅为指针）"；`project-roadmap-research` 根检测加 `AGENTS.md`；`spec-arch-adapter` 生成的 `CLAUDE.md` 保持一行指针 | `rg -n "CLAUDE\.md" skills/ agents/` 只剩兼容性说明句；对一个只有 `AGENTS.md` 的目录跑 `list-project-roots.sh` 能识别为根 |
| P1-7 | `adversarial-cross-model-review` 重定位：description 改为"验证任何外部或自动化 review 的 findings（Bugbot PR 评论、Codex adversarial-review、Cursor `/review` 子代理、他人 PR review）"；Phase 1 解析器加"从 PR review thread / JSON 输入"两种来源；与 `cross-review-gate` Phase 3 Step 4 共用同一份 consolidation 规则（见 P2-1） | description 含 "Bugbot" 与 "PR review"；e2e 增加一节：粘一条 Bugbot 评论 → 输出 Adopt/Reject 各 ≥1 条并带 `file:line` |
| P1-8 | 否决优先级单点定义：在 `templates/AGENTS.md` "AI 协作红线" 下加一条 `Gate precedence: QA Lead Block > sprint-close-auditor Blocked > Codex NO-GO > Risk Manager veto（仅 strategy panel）> 其他 Conditional`；`pair-protocol` Phase 5 写明 auditor `Blocked` 回 Phase 4；三个 skill 只引用不复述 | `rg -n "Gate precedence" templates/ skills/` 恰好 1 处定义 + ≥3 处引用 |
| P1-9 | hooks 双格式：提供 `templates/hooks/claude.settings.json`（Claude Code，删 `if:`/tmux，保留 commit 前 session-end 提醒与 Edit 后 pitfalls 提醒）与 `templates/hooks/cursor.hooks.json`（`version: 1`；`afterFileEdit` → pitfalls 检索提醒；`beforeShellExecution` matcher `git commit` → session-end 清单；`stop` → 若 `docs/task/progress.md` 未在 diff 中则 `followup_message`，`loop_limit: 1`）；`spec-arch-adapter` 可选写入 `.cursor/hooks.json` | 本地 Cursor 与一次 Cloud Agent run 中各观察到一次 afterFileEdit 提示；Claude Code 侧 `claude --debug` 看到 PostToolUse 触发；两份 hooks 文件 `rg codex-pair` = 0 |

### P2 长期形态

| # | 动作 | 验收 |
|---|---|---|
| P2-1 | 抽公共 reference：`skills/_shared/evidence-discipline.md`（T0-T3 分级、8 要素 spec、5 步调查循环、反转假设、Confirmed/Likely/Disputed/Impractical 分类、`[Px][confidence] file:line` 格式），`cross-review-gate`、`sprint-design-reviewer`、`adversarial`、`pair-protocol`、`templates/AGENTS.md` 只引用 | `rg -n -e reverse_hypothesis -e 反转假设 skills/ templates/` 定义 1 处、引用 ≥4 处；各 SKILL.md 总字节数较现状下降 ≥30%（现 122 KB） |
| P2-2 | `project-roadmap-research` 并入 `spec-arch-adapter --mode roadmap`（只保留受控块回写），SKILL.md 首段写明"只读探索优先用平台 Explore" | `skills/` 目录 10 → 9；`roadmap.md` 受控块回写在 e2e 上仍可复现 |
| P2-3 | `code-review-expert` skill 弃，agent 改名 `reviewer-generalist`；README "轻量替代" 改指向 Cursor `/review` / Claude `/code-review` / Codex `/codex:review` | 无同名 skill + agent；`rg -n "code-review-expert" skills/ README.md` 仅剩历史说明 |
| P2-4 | 打包为 plugin：kit 根加 `.cursor-plugin/marketplace.json`（Cursor "From GitHub Repository" 导入需要）与 `.claude-plugin/plugin.json`（Claude Code 单仓 plugin），`install.sh` 退化为本地开发用 | Cursor Customize → From GitHub Repository 导入成功并列出 skills；Claude Code `/plugin marketplace add licett/ai-workflow-kit` 成功 |
| P2-5 | 周期性任务交 Grok Bot routines（见 §4.3），kit 只提供被 routine 调用的 skill 文本 | 至少 1 条 routine（pitfalls/progress 行数预算周报）跑通并在 Run history 可见 |
| P2-6 | `spec-arch-adapter` 生成 `.cursor/environment.json` 骨架与 AGENTS.md "Cursor Cloud specific instructions" 段 | 新项目 write 后两者存在；Cloud Agent 首次 run 无需手工补环境说明 |

不建议做：

- 不要把 tmux / acpx 传输层再加回任何文档。
- 不要往任何 SKILL.md 追加新的 MANDATORY 清单；新事故进 `references/incident-log.md`，再从中提炼 ≤1 行规则进主体。
- 不要让 Grok Bot routine 对每个 PR 跑 `cross-review-gate` Full；routine 只跑 Lite/Standard 或平台 `/review`，Full 留给人触发的 T3。
- 不要同时维护 `templates/` 与 adapter 内两套模板。

---

## 4. 与 Cursor / Grok Bot / Cloud Agent 体系的衔接

### 4.1 分工矩阵

| 能力 | 留在 kit | 交给 Cursor 内建 / managed skills | 交给 Grok Bot（Bot + skill + routine） | 交给 Cloud Agent |
|---|---|---|---|---|
| 方法论 + AGENTS.md 约束 + Sprint/Pack/pitfalls 模板 | **是**（唯一真相源） | — | 只读引用 | 通过 AGENTS.md 读取 |
| 单路 code review 原始 findings | 否 | `/review`、`/review-bugbot`、`/review-security`、PR 上的 Bugbot | — | — |
| 多路 findings 归一化、合并、tier 闸门、QA Lead 否决 | **是**（`cross-review-gate` 瘦身版） | — | — | 可在 PR 上跑 Standard |
| Sprint 设计评审（engineering） | **是** | — | — | — |
| Sprint 设计评审（量化策略面板） | 否（拆出为 domain plugin） | — | — | — |
| TDD 执行循环 | **是**（协议） | `/verify`、`/run`（Claude）辅助 | — | **主执行面**：Pack 实现在云端分支上跑 |
| Sprint 收口审计 | **是** | — | 可由 routine 定时提醒 | 可在 close 前跑一次 |
| 跨模型结对协议 | **是**（`pair-protocol`） | `.cursor/agents/coder-codex.md` 模型钉死 | — | Cloud subagent 可承接 Codex 侧长任务 |
| Codex 传输实现 | 否（降为 fallback） | Cursor subagent；Claude Code 官方 codex-plugin-cc | — | — |
| 只读代码库探索 | 否 | Explore subagent | — | — |
| 知识检索（FTS5） | **是**（脚本） | — | routine 定时重建索引 | 云端 install 步骤中 `build_knowledge_db` |
| 周期性文档收口 / 预算检查 | 否 | `/loop`（会话内） | **是**（routine） | — |
| 拆大 PR、PR 跟进 | 否 | `/split-to-prs`、`/autopilot` | — | — |
| 事件触发（PR 打开 / Slack 关键词 / webhook） | 否 | Cursor Automations（`/automate`） | **是**（routine 的 Slack listener / webhook / GitHub 事件） | 被触发后的执行体 |

### 4.2 与 Cursor managed skills 的边界

Cursor 内建（managed）skills 里与 kit 直接重叠的是 `/review`、`/review-bugbot`、`/review-security`、`/split-to-prs`、`/autopilot`、`/loop`、`/create-subagent`。原则：**kit 不复刻这些的功能，只消费它们的输出。**

- `cross-review-gate` Standard tier 的 Agent 2（正确性）与 Agent 3（安全）可直接调用 `/review-bugbot`、`/review-security`，kit 负责把输出归一化为 `[Px][confidence] file:line`、跑 consolidation、给 Pass/Conditional/Fail。
- `code-review-expert` skill 让位给 `/review`；kit 只留 agent 文件定义格式基准。
- `adversarial-cross-model-review`（重定位后）的输入源之一就是 Bugbot 的 PR 评论。
- `agents/*.md` 放 `.claude/agents/`（Cursor 兼容读取）或 `.cursor/agents/`；reviewer 类加 `readonly: true`，需要模型隔离的加 `model:` + `force-default-model: true`。Claude Code 对未知字段（`readonly`、`color`）的容忍度待验证，若报错则维护 `.cursor/agents/` 与 `.claude/agents/` 两份。

### 4.3 与 Grok Bot workflows 的边界

Grok Bot 的模型是 **Bot（长期角色 + 审批边界）→ skill（做法）→ routine（何时跑，≤50 条/Bot，保留 20 次运行记录，触发源为 schedule / Slack listener / webhook / GitHub 事件）**，官方建议路径是"先一次性任务跑通 → 存为 skill → 再挂 routine"，且所有对外写操作放在审批边界之后。对照 kit：

| 应交给 Grok Bot 的 | 形式 | kit 提供什么 |
|---|---|---|
| 每日/每周 pitfalls.md ≤250 行、≤10 卡、progress.md ≤100 行预算检查，超标发提醒 | routine（schedule） | `templates/pitfalls.md` 的规则文本 + 一个 `scripts/qa/check_budget.py`（P2 新增，可选） |
| 定时 `build_knowledge_db` 重建 + `golden_query_test` 回归 | routine（schedule） | 现有脚本 |
| "PR opened" → 跑 `cross-review-gate` Lite/Standard 或 `/review`，把 Pass/Conditional/Fail 贴回 PR | routine（GitHub 事件） | 瘦身后的 `cross-review-gate` skill 文本 |
| Slack `#dev` 出现 "sprint close" → 跑 `sprint-close-auditor`，输出 Complete/Partial/Blocked | routine（Slack listener，narrow 匹配） | 现有 skill |
| Sprint 到 ETA 未 close 的提醒 | routine（schedule，读 `docs/sprint/*.md` 的 ETA 字段） | sprint 模板已有 ETA 字段 |
| Night Shift / 投资日报一类 X ingest | 已在 Grok Bot 侧，与本 kit 无关 | — |

**不应交给 Grok Bot 的**：`tdd-loop-executor`（需要在仓库分支上持续写代码，属 Cloud Agent）、`cross-review-gate` Full（成本）、`pair-protocol`（需要两个模型实时对话）、任何会自动 merge / 改生产配置的动作（Grok Bot 官方也要求这些留在审批后）。

Grok Bot skill 的存储格式是否直接接受 kit 的 SKILL.md 待验证；文档只说"从完成的任务存为 skill、用 `/` 引用、在 Settings > Plugins > Yours 启用"。稳妥做法：kit 的 skill 文本作为 Bot skill 的**指令来源**，由 Bot 保存一份，而不是假设文件级共享。

### 4.4 与 Cloud Agent 的边界

Cloud Agent 是 kit 方法论最自然的执行面（自主、长时、有分支），但前提三件事 kit 现在都没做：

1. skills 必须在仓库内（`.agents/skills/` 或 `.cursor/skills/` 或 `.claude/skills/`）——P1-1。
2. `AGENTS.md` 必须有 "Cursor Cloud specific instructions" 段（环境、测试命令、哪些服务不可用）——P2-6。
3. hooks 必须是 `.cursor/hooks.json`——P1-9。

做完后的分工：Phase 2（Pack 实现）整段交给 Cloud Agent 跑 `tdd-loop-executor`；多 Pack 并行用 cloud subagent 各占一个分支；`--recheck` 类重复审查在云端跑不占本地上下文；本地 Claude Code / Cursor 只做 Phase 1 设计评审、Phase 3 合并判定、Phase 5 收口——这正好是"CC 当大脑"原意，只是"手"从 Codex 变成了任意可钉模型的云执行体。

---

## 5. 证据索引

内部（行号基于 `6d53534`）：

- `README.md:3,269,286-294,305-314,343-344,401-402`
- `install.sh:7,16-27,55`
- `skills/cross-review-gate/SKILL.md:27-31,42,44-50,52,58-84,235`
- `skills/tdd-loop-executor/SKILL.md:24-28`；`references/one-line-entry-dictionary.md:25,36-37`
- `skills/sprint-close-auditor/SKILL.md:43-45`
- `skills/sprint-design-reviewer/SKILL.md:24-26,33,349`；`references/review-axes.md` S1-S4
- `skills/adversarial-cross-model-review/SKILL.md:3,13-16`
- `skills/project-roadmap-research/SKILL.md:22`
- `skills/spec-arch-adapter/scripts/spec_arch_audit.py:43-53,114,130-135`
- `skills/cc-codex-pair/SKILL.md:35,68,191,198-211,324,346,408,423,431,493-528,532-571,585,712,779,936,943-944,980-982`（1111 行 / 62126 字节）
- `skills/cc-codex-pair/PROVENANCE.md:3-10,25-28`；`scripts/codex-companion.mjs:70`；`tests/acceptance.sh:57-58,65`
- `agents/reviewer-qa-lead.md:3,101`；`agents/reviewer-correctness.md:3`；`agents/code-review-expert.md:12,90`
- `templates/hooks.json:10,21,32,43`；`templates/ai-workflow.md:66,73,174,542`；`templates/AGENTS.md:26,99`
- `scripts/qa/build_knowledge_db.py:29`
- `examples/workflow-diagram.md:29`

外部（2026-09 抓取）：

- Cursor Agent Skills：`cursor.com/docs/skills` —— 目录列表、`.claude/skills` 兼容、仅 `~/.cursor/skills` 可同步到 Cloud、内建 skill 清单、`disable-model-invocation` / `paths` / `metadata`、plugin 导入需 `.cursor-plugin/marketplace.json`
- Cursor Subagents：`cursor.com/docs/subagents` —— `.cursor/agents` / `.claude/agents` / `.codex/agents`、`model` / `readonly` / `is_background`、优先级、"5 个并行 ≈ 5× token"、Cloud subagents；论坛确认 `force-default-model: true`
- Cursor Cloud Agents：`cursor.com/docs/cloud-agent`、`/cloud-agent/setup` —— 读 `AGENTS.md`、`.cursor/environment.json`、`.cursor/hooks.json` 在云端执行、VM 无本机 home
- Cursor Hooks：`cursor.com/docs/hooks`、`/reference/third-party-hooks` —— 事件清单、Claude 格式映射表
- Grok Bot：`cursor.com/docs/grok-bot/work`、`cursor.com/help/grok-bot/routines`、`docs.x.ai/grok-bot/overview` —— Bot / skill / routine 模型、≤50 routines、Slack listener / webhook / GitHub 触发、审批边界、`/workspace` 共享计算机
- Claude Code Skills：`code.claude.com/docs/en/skills` —— Agent Skills 开放标准 + 扩展字段、description 1536 字符上限、云会话不读 `~/.claude/skills`、skill 内容常驻会话、内建 `/code-review` 以后台 subagent 运行
- Codex：`developers.openai.com/codex/skills`、`/codex/guides/agents-md` —— `.agents/skills` 扫描、`$skill` 引用、AGENTS.md 链 32 KiB 上限；`github.com/openai/codex-plugin-cc` —— `/codex:review`、`/codex:adversarial-review`、`/codex:rescue`、`/codex:status`、`/codex:result`

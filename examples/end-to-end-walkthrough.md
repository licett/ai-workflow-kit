# End-to-End Walkthrough: 从零到交付的完整流程

本文以一个真实的小工具 **`csv-dedup`**（CSV 行去重 CLI）为例，手把手走一遍完整开发流程。

> **场景**：你的团队经常收到供应商发来的 CSV 数据，里面有重复行。你需要一个命令行工具，按指定列去重，保留第一次出现的行。

---

## 全流程鸟瞰

先看全局，再看细节。整个流程 7 步，你只需要**输入提示词，AI 做剩下的**：

```
  步骤                        你输入什么                          产出什么
  ────                       ────────                          ────────
  0. 初始化项目               终端命令 + /spec-arch-adapter       文档骨架 (16 files)
  1. 产出 Sprint 设计文档      给 Claude Code 一段需求描述         docs/sprint/sprint1.md
  2. 设计评审                 /sprint-design-reviewer s1 review  Conditional → 发现 2 个缺口
  3. 修补设计 + 评审通过       给 Claude Code 修补指令             sprint1.md 更新 → Approve
  4. TDD 开发                /tdd-loop-executor s1 go           代码 + 10 tests + 1 pitfall
  5. 交叉 code review        /cross-review-gate s1              发现 2 P2 → 修复 → Pass
  6. Sprint 收口审计          /sprint-close-auditor s1 close     Complete ✅ → 提交
```

**总耗时**：约 30-60 分钟（含 AI 执行时间）
**产出**：~100 行产品代码 + ~150 行测试 + 完整文档
**质量保障**：12 个测试、3+4 专家交叉 review、1 张 pitfalls 卡片

---

## Step 0：初始化项目

> 这一步在终端和 Claude Code 中各做一部分。

### 0.1 终端：创建项目 + 安装 Skill

```bash
# 安装 skills（只需做一次，以后新项目不用重复）
bash /path/to/ai-workflow-kit/install.sh

# 创建项目
mkdir csv-dedup && cd csv-dedup
git init
touch pyproject.toml
```

### 0.2 Claude Code：生成文档骨架

打开 Claude Code，输入：

```
/spec-arch-adapter

对当前项目执行 full profile 初始化。
项目是一个 Python CLI 工具，用于 CSV 行去重。
```

**AI 会做什么**：自动检测语言、生成 16 个文档文件。

**你会看到**：

```
Spec architecture summary
root: /path/to/csv-dedup
mode: write
profile: full
created: 16
```

### 0.3 Claude Code：补充项目信息

```
请更新 AGENTS.md 的 Coding Style & Naming Conventions 部分，补充以下信息：

- 语言：Python 3.10+
- 模块/函数/变量：snake_case
- 类名：PascalCase
- CLI 入口：src/csv_dedup/cli.py
- 核心模块：src/csv_dedup/engine.py
- 测试框架：pytest
- 测试目录：tests/
```

此时项目结构：

```
csv-dedup/
├── README.md / CLAUDE.md / AGENTS.md
├── docs/
│   ├── README.md
│   ├── task/progress.md
│   ├── sprint/README.md
│   ├── qa/pitfalls.md
│   ├── qa/pitfalls_archive/README.md
│   ├── review/ai-workflow.md
│   ├── rules/PROJECT_RULES.md
│   └── ...
└── (暂无源代码)
```

---

## Step 1：产出 Sprint 设计文档

> **不要直接写代码。** 先让 AI 帮你产出 Sprint 设计文档。

### 你输入（完整提示词，可直接复制）

```
请帮我创建 docs/sprint/sprint1.md，这是我们第一个 Sprint 的设计文档。

背景：
- 我们经常收到供应商发来的 CSV 数据，里面有重复行
- 需要一个命令行工具，按指定列去重，保留第一次出现的行

目标：
- 交付可用的 CLI 工具
- 用法：csv-dedup --key col1,col2 input.csv -o output.csv
- 支持参数：--key（必选，去重列）、--output（输出文件）、--delimiter（分隔符，默认逗号）、--keep-last（保留最后出现而非第一次）

非目标：
- 不做 GUI
- 不做流式处理 / 大文件优化（留后续 Sprint）
- 不做多文件合并

请按 AGENTS.md 中的 Pack 规范，拆成 2 个 Pack：
1. Pack: CLI 框架 — 搭建 argparse 入口和参数解析
2. Pack: 去重引擎 — 实现按指定列去重的核心逻辑

每个 Pack 必须包含：背景/目标、范围边界、DoD（含具体 pytest 命令）、指令与测试、风险/回滚。
最后加上 Sprint Close 条件。

同时更新 docs/sprint/README.md 的索引。
```

### AI 会做什么

1. 读取 `AGENTS.md` 了解 Pack 规范模板
2. 按你的需求拆分 2 个 Pack
3. 为每个 Pack 生成完整的 DoD、测试命令、风险评估
4. 创建 `docs/sprint/sprint1.md`
5. 更新 `docs/sprint/README.md` 索引

### 你会看到

AI 创建了 `docs/sprint/sprint1.md`，内容类似：

```markdown
# Sprint 1: CSV Dedup CLI v1

## 背景与目标
- 供应商 CSV 数据有重复行，需要按指定列去重
- 目标：交付可用的 CLI 工具，支持 csv-dedup --key col1,col2 input.csv -o output.csv

## 非目标
- 不做 GUI
- 不做流式处理（大文件优化留后续）
- 不做多文件合并

### Pack: CLI 框架
（完整 Pack 内容，含 DoD、测试命令...）

### Pack: 去重引擎
（完整 Pack 内容，含 DoD、测试命令...）

## Sprint Close 条件
- [ ] 所有 Pack DoD 满足
- [ ] progress.md 已更新
- [ ] pitfalls.md 收口
```

---

## Step 2：设计评审

> Sprint 文档写完后，**开工前先让专家组评审**，避免方向性错误。

### 你输入（完整提示词）

```
/sprint-design-reviewer s1 review
```

### AI 会做什么

1. 读取 `CLAUDE.md` + `docs/sprint/sprint1.md` + `docs/task/progress.md` + `docs/qa/pitfalls.md`
2. 自动检测 Sprint 类型 → **engineering**（关键词命中：CLI, pipeline, schema）
3. 组装 **工程面板**：架构师 + 代码评审专家 + QA 负责人
4. 3 个 agent 并行评审，然后交叉质疑过滤误报

### 你会看到（示意）

```
Sprint 设计评审: sprint1
Sprint type: engineering
Expert panel: 架构师, 代码评审专家, QA 负责人

## 评审结论: Conditional

## 维度评分
| 维度 | 评分 | 关键发现 |
|------|------|----------|
| A 设计合理性 | ✅ | 范围清晰，2 Pack 拆分合理 |
| B 技术路线 | ✅ | argparse + 标准 csv 模块，无过度设计 |
| C 验收标准 | ⚠️ | Pack 去重引擎缺少编码边界测试（UTF-8 BOM / GBK） |
| D 信息充分性 | ⚠️ | 未指定 CSV dialect 处理策略 |

## Confirmed Findings
- [P2][0.85][架构师+QA] 缺少 CSV 编码边界测试
  证据: docs/sprint/sprint1.md:Pack 去重引擎 DoD 无编码相关条目
  建议: 在 DoD 中增加 UTF-8 BOM 和非 UTF-8 编码测试

## 必须修复项
1. Pack 去重引擎 DoD 增加编码边界测试条目
2. 明确 CSV dialect 默认策略
```

---

## Step 3：修补设计 + 重新评审

> 评审结果是 Conditional，需要修补。把评审意见直接喂给 AI 修。

### 你输入（完整提示词）

```
根据设计评审的 Confirmed Findings，请修补 docs/sprint/sprint1.md：

1. Pack 去重引擎的 DoD 增加：
   - [ ] UTF-8 BOM 输入文件去重测试通过
   - [ ] 自定义 delimiter（如分号）测试通过

2. Sprint 开头增加技术决策说明：
   - CSV 编码：默认 utf-8-sig（兼容 BOM），不支持 GBK（非目标）
   - CSV 分隔符：默认逗号，通过 --delimiter 指定

修补完成后，请再次运行设计评审确认通过：
/sprint-design-reviewer s1 review
```

### AI 会做什么

1. 更新 `sprint1.md` 中的 DoD 和技术决策
2. 自动再次运行设计评审
3. 这次所有维度通过 → **Approve**

### 你会看到

```
## 评审结论: Approve ✅
所有维度通过。可以开始开发。
```

---

## Step 4：TDD 开发

> 设计评审通过，正式进入编码。用 `/tdd-loop-executor` 让 AI 按 TDD 循环写代码。

### 4.1 启动开发 — 你输入（完整提示词）

```
/tdd-loop-executor s1 go
```

就这一行。AI 会自动读取 sprint1.md，按 Pack 顺序逐个执行 TDD 循环。

### AI 会做什么（第一轮 — Pack: CLI 框架）

**Ask 阶段**（AI 自动完成）：
```
读取 CLAUDE.md → sprint1.md → progress.md → pitfalls.md
pitfalls hit: none (keywords=csv, cli, argparse)

计划草稿：
1. 创建 src/csv_dedup/__init__.py
2. 创建 src/csv_dedup/cli.py (argparse: --key, --output, --delimiter, --keep-last)
3. 创建 tests/test_cli.py (3 个测试)
范围：~60 行代码 + ~40 行测试
```

**Code 阶段**（AI 自动完成）：
```
Step 1: 写测试 tests/test_cli.py
  - test_help_shows_usage        → RED ✗ (ModuleNotFoundError)
  - test_missing_key_exits_error → RED ✗
  - test_parse_args_normal       → RED ✗

Step 2: 实现 src/csv_dedup/cli.py
  - test_help_shows_usage        → GREEN ✓
  - test_missing_key_exits_error → GREEN ✓
  - test_parse_args_normal       → GREEN ✓

Step 3: 更新 progress.md
```

### 你会看到

```
当前循环: Pack CLI 框架
测试状态: 3/3 GREEN
已完成: cli.py (argparse 入口), tests/test_cli.py (3 cases)
下一步: Pack 去重引擎

docs/task/progress.md 已更新。
```

### 4.2 继续下一个 Pack — 你输入（完整提示词）

```
continue
```

就这一个词。AI 从 `progress.md` 恢复上下文，自动进入 Pack: 去重引擎。

### AI 会做什么（第二轮 — Pack: 去重引擎）

**Ask 阶段**：
```
从 progress.md 恢复 → Pack: 去重引擎
pitfalls hit: none (keywords=csv, dedup, encoding, BOM)

计划草稿：
1. 创建 tests/test_engine.py (7 个测试)
2. 创建 tests/fixtures/sample.csv, sample_with_bom.csv
3. 创建 src/csv_dedup/engine.py
```

**Code 阶段**：
```
Step 1: 写 7 个测试 → 全部 RED ✗

Step 2: 实现 engine.py
  - test_single_key_dedup    → GREEN ✓
  - test_multi_key_dedup     → GREEN ✓
  - test_empty_file          → GREEN ✓
  - test_header_only         → GREEN ✓
  - test_keep_last           → GREEN ✓
  - test_utf8_bom            → RED ✗  ← BOM 字节没处理！
  - test_custom_delimiter    → GREEN ✓

Step 3: 修复 BOM — 改用 utf-8-sig 编码
  - test_utf8_bom            → GREEN ✓
```

### 发现了 Bug！AI 自动更新 pitfalls

```
⚠️ 发现坑位: UTF-8 BOM 导致首列 key 匹配失败

已更新 docs/qa/pitfalls.md:

### ACTIVE 2026-03-20 CSV UTF-8 BOM 导致首列 key 不匹配
- Scope: `src/csv_dedup/engine.py`
- Search keywords: `BOM`, `utf-8-sig`, `csv`, `first_column`
- Rule: 读取 CSV 时必须用 encoding='utf-8-sig' 而非 'utf-8'
- Guardrail: tests/test_engine.py::test_utf8_bom
- Last seen: 2026-03-20
- Archive when: 连续 2 个 Sprint close 未命中
```

### 你会看到

```
当前循环: Pack 去重引擎
测试状态: 7/7 GREEN (含 1 次 BOM bugfix)
已完成: engine.py, tests/test_engine.py
pitfalls.md: 新增 1 张 ACTIVE 卡片 (UTF-8 BOM)
下一步: 建议执行 /cross-review-gate

Sprint 1 所有 Pack 代码已完成。
```

此时项目结构：

```
csv-dedup/
├── src/csv_dedup/
│   ├── __init__.py
│   ├── cli.py          # ~50 行
│   └── engine.py       # ~40 行
├── tests/
│   ├── fixtures/
│   │   ├── sample.csv
│   │   └── sample_with_bom.csv
│   ├── test_cli.py     # 3 个测试
│   └── test_engine.py  # 7 个测试
├── docs/
│   ├── task/progress.md   # 已更新
│   ├── qa/pitfalls.md     # 1 张 ACTIVE 卡片
│   └── sprint/sprint1.md
└── ...
```

---

## Step 5：交叉代码审查

> 代码写完了，提交前做 4 专家交叉审查。

### 你输入（完整提示词）

```
/cross-review-gate s1
```

### AI 会做什么

1. 运行 `git diff` 获取所有变更
2. 加载 sprint1.md 了解 scope
3. 启动 **4 个并行 agent**：
   - Agent 1（正确性）：逻辑 bug、回归、边界
   - Agent 2（安全性）：输入验证、路径穿越、资源泄露
   - Agent 3（性能）：大文件、内存、算法复杂度
   - Agent 4（QA）：测试设计质量、覆盖率、上线就绪
4. 4 个 agent 交叉质疑，过滤误报

### 你会看到（示意）

```
交叉复核代码评审报告

## 复核结论: Conditional Pass

## Confirmed Findings
- [P2][0.88][正确性+QA] engine.py:23 — 未处理 key 列名不存在的情况
  影响: 用户传入不存在的列名会抛 KeyError 而非友好报错
  建议: 验证 key_cols 是否都在 header 中

- [P2][0.82][安全性] cli.py:15 — 未验证输出路径
  影响: --output /etc/passwd 理论上可覆写系统文件
  建议: 加 overwrite 确认或路径检查

## Disputed
- [原P2→驳回][性能] "大文件应该用流式处理"
  驳回原因: Sprint 1 明确声明非目标

## QA: Release Readiness
- 上线判定: Conditional
- Ship-blockers: P2 key 列名验证
```

### 修复后重新审查 — 你输入（完整提示词）

```
请根据 cross-review-gate 的 Confirmed Findings 修复以下 2 个 P2：

1. engine.py: dedup_csv 入口增加 key_cols 验证 —
   检查每个 key 是否在 CSV header 中，不存在则 raise ValueError 并给出友好提示

2. cli.py: 增加输出路径检查 —
   如果 --output 指向的文件已存在，提示用户确认覆写（或加 --force 参数跳过确认）

两个修复都必须先补测试（TDD）：
- tests/test_engine.py 增加 test_invalid_key_column
- tests/test_cli.py 增加 test_output_exists_without_force

修复完成后，重新运行交叉审查：
/cross-review-gate
```

### 你会看到

```
## 复核结论: Pass ✅
所有 Confirmed findings 已修复。QA 判定: Ready。
```

---

## Step 6：Sprint 收口审计

> 代码 + review 都完成了，最后做一次全面对账。

### 你输入（完整提示词）

```
/sprint-close-auditor s1 close
```

### AI 会做什么

1. 读取 `docs/sprint/sprint1.md` 的所有 Pack DoD
2. 逐条对账：代码是否存在？测试是否通过？产物是否生成？
3. 检查 progress.md、pitfalls.md 是否已更新

### 你会看到（示意）

```
Sprint 收口审计: sprint1
Sprint verdict: Complete ✅

## 完成矩阵
| Pack | 任务 | 代码 | 测试 | DoD |
|------|------|------|------|-----|
| CLI 框架 | --help 正常输出 | ✅ cli.py | ✅ 3/3 | ✅ |
| CLI 框架 | --delimiter 参数 | ✅ cli.py:28 | ✅ | ✅ |
| 去重引擎 | 单列去重 | ✅ engine.py | ✅ | ✅ |
| 去重引擎 | 多列组合键 | ✅ engine.py | ✅ | ✅ |
| 去重引擎 | 空文件/header-only | ✅ engine.py | ✅ | ✅ |
| 去重引擎 | --keep-last | ✅ engine.py | ✅ | ✅ |
| 去重引擎 | UTF-8 BOM | ✅ engine.py | ✅ | ✅ |

## 文档状态
- progress.md: ✅ 已更新
- pitfalls.md: ✅ 1 张 ACTIVE 卡片 (BOM)
- sprint1.md: ✅ 所有 DoD 满足

## 测试验证
$ pytest tests/ -q
12 passed in 0.3s ✅

## 结论
Sprint 1 可以关闭。建议提交 commit。
```

### 提交 — 你输入（完整提示词）

```
Sprint 1 已通过收口审计，请帮我提交。
commit message 概括本次 Sprint 的全部改动。
```

AI 会生成：

```bash
git add -A
git commit -m "feat: csv-dedup CLI v1 — Sprint 1 complete

- CLI: --key, --output, --delimiter, --keep-last, --force
- Engine: dedup by key columns, UTF-8 BOM support, key validation
- Tests: 12 cases covering happy path + edge cases + error handling
- Pitfall: BOM encoding issue documented in pitfalls.md"
```

---

## 为什么 pitfalls 制度很重要

假设 3 个月后，你开了 Sprint 5 要做"CSV 合并工具"。你输入：

```
/tdd-loop-executor s5 go
```

AI 在 Ask 阶段会**自动检索 pitfalls.md**，发现 BOM 卡片：

```
pitfalls hit:
  - ACTIVE 2026-03-20 CSV UTF-8 BOM 导致首列 key 不匹配
    → 防回归：读取 CSV 必须用 encoding='utf-8-sig'
```

**AI 换了 session 也不会忘记这个教训。** 这就是 pitfalls 的价值。

---

## 进阶场景

### 跨会话恢复

中途关了 Claude Code？下次打开直接输入：

```
continue
```

AI 自动读 `docs/task/progress.md`，从上次停下的地方继续。

### 验证其他 AI 的建议

GPT 说你的代码有问题？不确定对不对？

```
/adversarial-cross-model-review

GPT 建议如下：
1. engine.py 应该用 pandas 代替 csv 模块，性能更好
2. cli.py 应该用 click 代替 argparse，更现代
```

AI 会 3 个专家独立读源码验证：

```
F1: 用 pandas 代替 csv → Reject
原因: 当前工具只有 40 行，csv 模块零依赖，引入 pandas 是过度设计。

F2: 用 click 代替 argparse → Defer
原因: click 更好用，但这是风格偏好。后续需要子命令时再考虑。
```

### 运行时报错排查

`csv-dedup` 在某个真实文件上崩了？

```
/log-rootcause-triage

运行 csv-dedup --key Name input.csv 时报错：

Traceback (most recent call last):
  File "src/csv_dedup/engine.py", line 23, in dedup_csv
    key = tuple(row[k] for k in key_cols)
KeyError: 'Name'
```

AI 会定位根因、提出最小修复方案、并提醒你更新 pitfalls。

---

## 提示词速查卡

| 场景 | 完整提示词 |
|------|-----------|
| 初始化文档骨架 | `/spec-arch-adapter` 对当前项目执行 full profile 初始化 |
| 产出 Sprint 文档 | 请帮我创建 docs/sprint/sprint1.md...（附需求描述） |
| 设计评审 | `/sprint-design-reviewer s1 review` |
| 修补设计 | 根据设计评审的 Confirmed Findings，请修补 docs/sprint/sprint1.md...（附修补项） |
| 启动 TDD 开发 | `/tdd-loop-executor s1 go` |
| 继续下一个 Pack | `continue` |
| 交叉代码审查 | `/cross-review-gate s1` |
| 修复审查发现 | 请根据 cross-review-gate 的 Confirmed Findings 修复...（附修复项），修复完成后重新运行 `/cross-review-gate` |
| Sprint 收口 | `/sprint-close-auditor s1 close` |
| 提交代码 | Sprint N 已通过收口审计，请帮我提交 |
| 跨会话恢复 | `continue` |
| 验证外部 AI 建议 | `/adversarial-cross-model-review`（附对方建议） |
| 排查运行时错误 | `/log-rootcause-triage`（附错误日志） |

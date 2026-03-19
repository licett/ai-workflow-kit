# End-to-End Walkthrough: 从零到交付的完整流程

本文以一个真实的小工具 **`csv-dedup`**（CSV 行去重 CLI）为例，完整走一遍 6 步开发流程。

> **场景**：你的团队经常收到供应商发来的 CSV 数据，里面有重复行。你需要一个命令行工具，按指定列去重，保留第一次出现的行。

---

## 第 0 步：安装 Skill + 初始化项目

```bash
# 安装 skills（只需做一次）
bash /path/to/ai-workflow-kit/install.sh

# 创建项目
mkdir csv-dedup && cd csv-dedup
git init
echo "csv-dedup" > pyproject.toml  # 最小项目标识

# 初始化文档骨架
python3 ~/.claude/skills/spec-arch-adapter/scripts/spec_arch_audit.py \
  --root . --mode write --profile full
```

此时你的项目长这样：

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

补充 `AGENTS.md` 中的项目信息：

```markdown
## Coding Style & Naming Conventions
- 语言：Python 3.10+
- 模块/函数/变量：snake_case
- CLI 入口：src/csv_dedup/cli.py
- 测试框架：pytest
```

---

## 第 1 步：写 Sprint 设计文档

在 Claude Code 里，你可以直接让 AI 帮你写 sprint 文档，也可以自己写。核心是**先有文档，再写代码**。

创建 `docs/sprint/sprint1.md`：

```markdown
# Sprint 1: CSV Dedup CLI v1

## 背景与目标
- 供应商 CSV 数据有重复行，需要按指定列去重
- 目标：交付可用的 CLI 工具，支持 `csv-dedup --key col1,col2 input.csv -o output.csv`

## 非目标
- 不做 GUI
- 不做流式处理（大文件优化留后续）
- 不做多文件合并

### Pack: CLI 框架

**背景/目标**:
- 搭建 CLI 入口，支持 --key, --output, --keep-last 参数

**范围边界**:
- 改哪些文件：`src/csv_dedup/cli.py`, `src/csv_dedup/__init__.py`
- 不做：去重逻辑（留给下一个 Pack）

**DoD**:
- [ ] `python -m csv_dedup --help` 正常输出帮助
- [ ] 测试通过：`pytest tests/test_cli.py`

**指令与测试**:
```bash
pytest tests/test_cli.py -v
```

### Pack: 去重引擎

**背景/目标**:
- 实现按指定列去重的核心逻辑，默认保留首次出现的行

**范围边界**:
- 改哪些文件：`src/csv_dedup/engine.py`
- 不做：CLI 集成（CLI Pack 已处理）

**DoD**:
- [ ] 单列去重测试通过
- [ ] 多列组合键去重测试通过
- [ ] 空文件/只有 header 的边界测试通过
- [ ] --keep-last 选项测试通过
- [ ] 测试通过：`pytest tests/test_engine.py`

**指令与测试**:
```bash
pytest tests/test_engine.py -v
```

## Sprint Close 条件
- [ ] 所有 Pack DoD 满足
- [ ] `csv-dedup --key name tests/fixtures/sample.csv` 能正确输出去重结果
- [ ] progress.md 已更新
- [ ] pitfalls.md 收口
```

---

## 第 2 步：设计评审 — `/sprint-design-reviewer`

Sprint 文档写完后，**开工前先评审**。

### 你输入

```
/sprint-design-reviewer s1 review
```

### AI 做了什么

1. 读取 `CLAUDE.md` + `docs/sprint/sprint1.md` + `docs/task/progress.md` + `docs/qa/pitfalls.md`
2. 自动检测 Sprint 类型 → **engineering**（关键词命中：CLI, refactor, pipeline, schema）
3. 组装 **工程面板**：架构师 + 代码评审专家 + QA 负责人
4. 3 个 agent 并行评审，然后交叉质疑

### 你看到的输出（示意）

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
| C 验收标准 | ⚠️ | Pack: 去重引擎 缺少编码测试（UTF-8 BOM / GBK） |
| D 信息充分性 | ⚠️ | 未指定 CSV dialect 处理（分号分隔 vs 逗号分隔） |

## Confirmed Findings
- [P2][0.85][架构师+QA] 缺少 CSV 编码边界测试
  证据: docs/sprint/sprint1.md:Pack 去重引擎 DoD 无编码相关条目
  建议: 在 DoD 中增加 UTF-8 BOM 和非 UTF-8 编码测试

## 必须修复项
1. Pack: 去重引擎 DoD 增加编码边界测试条目
2. 明确 CSV dialect：默认 comma，支持 --delimiter 参数
```

### 你的动作

根据评审意见，更新 `docs/sprint/sprint1.md`：
- Pack: 去重引擎 DoD 增加 `- [ ] UTF-8 BOM 输入测试通过`
- Pack: CLI 框架增加 `--delimiter` 参数

---

## 第 3 步：TDD 开发 — `/tdd-loop-executor`

设计评审通过（或修补后通过），进入开发。

### 你输入

```
/tdd-loop-executor s1 go
```

### AI 做了什么（第一轮 — Pack: CLI 框架）

**Ask 阶段**：

```
读取 CLAUDE.md → sprint1.md → progress.md → pitfalls.md
pitfalls hit: none (keywords=csv, cli, argparse)

计划草稿：
1. 创建 src/csv_dedup/__init__.py (空)
2. 创建 src/csv_dedup/cli.py (argparse: --key, --output, --delimiter, --keep-last)
3. 创建 tests/test_cli.py (3 个测试: help 输出、缺少 --key 报错、正常参数解析)
范围：~60 行代码 + ~40 行测试
```

**Code 阶段**：

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

### AI 输出

```
当前循环: Pack CLI 框架
测试状态: 3/3 GREEN
已完成: cli.py (argparse 入口), tests/test_cli.py (3 cases)
下一步: Pack 去重引擎

docs/task/progress.md 已更新。
```

### 你输入

```
continue
```

### AI 做了什么（第二轮 — Pack: 去重引擎）

**Ask 阶段**：

```
从 progress.md 恢复上下文 → Pack: 去重引擎
pitfalls hit: none (keywords=csv, dedup, encoding, BOM)

计划草稿：
1. 创建 tests/test_engine.py (7 个测试)
2. 创建 tests/fixtures/sample.csv, sample_with_bom.csv
3. 创建 src/csv_dedup/engine.py
```

**Code 阶段**：

```
Step 1: 写 7 个测试 → 全部 RED ✗

Step 2: 实现 engine.py — dedup_csv(input_path, output_path, key_cols, keep_last=False, delimiter=',')
  - test_single_key_dedup              → GREEN ✓
  - test_multi_key_dedup               → GREEN ✓
  - test_empty_file                    → GREEN ✓
  - test_header_only                   → GREEN ✓
  - test_keep_last                     → GREEN ✓
  - test_utf8_bom                      → RED ✗ ← BOM 字节没处理！
  - test_custom_delimiter              → GREEN ✓

Step 3: 修复 BOM — 用 utf-8-sig 编码打开
  - test_utf8_bom                      → GREEN ✓

Step 4: 更新 progress.md
```

### 发现了一个 Bug！AI 自动更新 pitfalls

```
⚠️ 发现坑位: UTF-8 BOM 导致首列 key 匹配失败

已更新 docs/qa/pitfalls.md:

### ACTIVE 2026-03-20 CSV UTF-8 BOM 导致首列 key 不匹配
- Scope: `src/csv_dedup/engine.py`
- Search keywords: `BOM`, `utf-8-sig`, `csv`, `first_column`
- Rule: 读取 CSV 时必须用 `encoding='utf-8-sig'` 而非 `utf-8`，否则首列会带 \ufeff 前缀
- Guardrail: `tests/test_engine.py::test_utf8_bom`
- Last seen: 2026-03-20
- Canonical detail: (首次发现，尚无归档)
- Archive when: 连续 2 个 Sprint close 未命中
```

### AI 最终输出

```
当前循环: Pack 去重引擎
测试状态: 7/7 GREEN (含 1 次 BOM bugfix)
已完成: engine.py, tests/test_engine.py
pitfalls.md: 新增 1 张 ACTIVE 卡片 (UTF-8 BOM)
下一步: 集成测试 + cross review

Sprint 1 所有 Pack 代码已完成，建议执行 /cross-review-gate。
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

## 第 4 步：交叉代码审查 — `/cross-review-gate`

代码写完了，提交前做交叉审查。

### 你输入

```
/cross-review-gate s1
```

### AI 做了什么

1. 运行 `git diff` 获取所有变更
2. 加载 sprint1.md 了解 scope
3. 启动 **4 个并行 agent**：
   - Agent 1（正确性）：逻辑 bug、回归、边界
   - Agent 2（安全性）：输入验证、路径穿越、资源泄露
   - Agent 3（性能）：大文件、内存、算法复杂度
   - Agent 4（QA）：测试设计质量、覆盖率、上线就绪
4. 4 个 agent 交叉质疑，过滤误报

### 你看到的输出（示意）

```
交叉复核代码评审报告

## 评审范围
- 变更文件: 5 files
- Sprint 上下文: sprint1
- 评审专家: 4 agents (正确性, 安全性, 性能, QA)

## 复核结论: Conditional Pass

## 专家视角摘要
| 专家 | 焦点 | 发现数 | 最高严重度 |
|------|------|--------|-----------|
| 正确性 | 逻辑/回归 | 1 | P2 |
| 安全性 | 验证/泄露 | 1 | P2 |
| 性能   | 复杂度   | 1 | P3 |
| QA     | 测试/风险 | 1 | P2 |

## Confirmed Findings
- [P2][0.88][正确性+QA] engine.py:23 — 未处理 key 列名不存在的情况
  影响: 如果用户传入不存在的列名，会抛 KeyError 而非友好报错
  建议: 在 dedup_csv 入口验证 key_cols 是否都在 header 中，否则 raise ValueError

- [P2][0.82][安全性] cli.py:15 — 未验证输出路径
  影响: --output /etc/passwd 理论上可覆写系统文件
  建议: 仅允许写入当前目录或用户指定的安全路径（或至少加 overwrite 确认）

## Disputed
- [原P2→驳回][性能] "大文件应该用流式处理"
  驳回原因: Sprint 1 明确声明 非目标，不做大文件优化

## QA 评审: Release Readiness
- 上线判定: Conditional
- 缺失测试: key 列名不存在的负向测试
- Ship-blockers: P2 key 列名验证

## 后续建议
- 修复 2 个 P2 后重跑: /cross-review-gate
- 或标记为已知限制，在 pitfalls.md 登记
```

### 你的动作

修复 2 个 P2（加列名验证 + 输出路径检查），补 2 个测试，再跑一次：

```
/cross-review-gate
```

这次输出：

```
## 复核结论: Pass
所有 Confirmed findings 已修复。QA 判定: Ready。
```

---

## 第 5 步：Sprint 收口审计 — `/sprint-close-auditor`

所有代码写完、review 通过，最后做收口审计。

### 你输入

```
/sprint-close-auditor s1 close
```

### AI 做了什么

1. 读取 `docs/sprint/sprint1.md` 的所有 Pack DoD
2. 逐条对账：代码是否存在？测试是否通过？产物是否生成？
3. 检查 progress.md、pitfalls.md 是否已更新

### 你看到的输出（示意）

```
Sprint 收口审计: sprint1
Sprint verdict: Complete ✅

## 完成矩阵
| Pack | 任务 | 代码 | 测试 | DoD |
|------|------|------|------|-----|
| CLI 框架 | --help 正常输出 | ✅ cli.py | ✅ 3/3 | ✅ |
| CLI 框架 | --delimiter 参数 | ✅ cli.py:28 | ✅ test_cli.py | ✅ |
| 去重引擎 | 单列去重 | ✅ engine.py | ✅ test_engine.py::test_single_key | ✅ |
| 去重引擎 | 多列组合键 | ✅ engine.py | ✅ test_engine.py::test_multi_key | ✅ |
| 去重引擎 | 空文件/header-only | ✅ engine.py | ✅ 2 cases | ✅ |
| 去重引擎 | --keep-last | ✅ engine.py | ✅ test_keep_last | ✅ |
| 去重引擎 | UTF-8 BOM | ✅ engine.py | ✅ test_utf8_bom | ✅ |

## 文档状态
- progress.md: ✅ 已更新
- pitfalls.md: ✅ 1 张 ACTIVE 卡片 (BOM)
- sprint1.md: ✅ 所有 DoD checkbox 可标记完成

## 测试验证
$ pytest tests/ -q
12 passed in 0.3s ✅

## 残留风险
- 大文件性能未测试（Sprint 1 声明为非目标，可接受）
- 输出路径安全检查为基础实现，生产环境可考虑加强

## 结论
Sprint 1 可以关闭。建议提交 commit。
```

### 你的最终动作

```bash
git add -A
git commit -m "feat: csv-dedup CLI v1 — Sprint 1 complete

- CLI: --key, --output, --delimiter, --keep-last
- Engine: dedup by key columns, UTF-8 BOM support
- Tests: 12 cases covering happy path + edge cases
- Pitfall: BOM encoding issue documented"
```

---

## 全流程回顾

```
  你做了什么                    用了什么 Skill           产出了什么
  ─────────                   ─────────────           ─────────
  1. 初始化项目               /spec-arch-adapter       文档骨架 (16 files)
  2. 写 sprint1.md            (手写)                   Sprint 设计文档
  3. 评审设计                 /sprint-design-reviewer   Conditional → 修补 2 处
  4. TDD 开发 Pack1          /tdd-loop-executor        cli.py + 3 tests
  5. TDD 开发 Pack2          /tdd-loop-executor        engine.py + 7 tests + 1 pitfall
  6. 交叉 code review        /cross-review-gate        发现 2 P2 → 修复 → Pass
  7. Sprint 收口             /sprint-close-auditor     Complete ✅ → 提交
```

**总耗时**：约 30-60 分钟（含 AI 执行时间）
**代码量**：~100 行产品代码 + ~150 行测试
**质量保障**：12 个测试、4 专家交叉 review、1 张 pitfalls 卡片

---

## 如果下次再开发类似项目

1. 新开 Sprint 2 时，AI 会自动检索 `pitfalls.md`，发现 BOM 卡片
2. 计划中会写：`pitfalls hit: UTF-8 BOM (docs/qa/pitfalls.md) → 防回归：使用 utf-8-sig`
3. **不会再踩同一个坑**

这就是 pitfalls 制度的价值 — **AI 换了 session 也不会忘**。

---

## 进阶用法

### 跨会话恢复

如果你中途关了 Claude Code，下次打开时只需要：

```
continue
```

AI 会自动读 `docs/task/progress.md`，从上次停下的地方继续。

### 外部模型建议验证

假设你把代码发给 GPT，GPT 说"engine.py 应该用 pandas 代替 csv 模块"。你不确定对不对：

```
/adversarial-cross-model-review

GPT 建议如下：
1. engine.py 应该用 pandas 代替 csv 模块，性能更好
2. cli.py 应该用 click 代替 argparse，更现代
```

AI 会 3 个专家独立读源码验证，可能输出：

```
F1: 用 pandas 代替 csv
复核结论: Reject
原因: 当前工具只有 40 行，csv 模块零依赖，引入 pandas 是过度设计。
      Sprint 1 明确声明"不做大文件优化"。

F2: 用 click 代替 argparse
复核结论: Defer
原因: click 确实更好用，但这是风格偏好不是 bug。
      如果后续 Sprint 需要子命令，可以在那时考虑迁移。
```

### 遇到运行时错误

如果 `csv-dedup` 在某个真实文件上崩了：

```
/log-rootcause-triage

Traceback (most recent call last):
  File "src/csv_dedup/engine.py", line 23, in dedup_csv
    key = tuple(row[k] for k in key_cols)
KeyError: 'Name'
```

AI 会定位根因、提出最小修复、并提醒你更新 pitfalls。

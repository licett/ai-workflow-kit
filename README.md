# AI Workflow Kit

一套面向 **Claude Code** 用户的开发流程工具包，包含方法论、约束规则和自动化 Skill。

> **先读方法论，再装 Skill。** Skill 只是自动化工具，没有方法论支撑，用起来跟乱点按钮没区别。

---

## 这套东西解决什么问题

用 AI 辅助开发时最常见的三个坑：

1. **Scope 膨胀** — AI 一写就停不下来，"顺手"重构半个项目
2. **结论翻转** — 同一个问题换个口径算一次就翻一次结论
3. **踩坑复发** — 上次踩过的坑，下次换个 session 又踩一遍

这套工具包通过 **方法论 + 约束规则 + Skill 自动化** 三层来解决。

---

## 三层架构

```
┌─────────────────────────────────────────────────┐
│  Layer 3: Skills (自动化)                        │
│  9 个 Claude Code Skill，覆盖设计→开发→审查→收口  │
├─────────────────────────────────────────────────┤
│  Layer 2: Constraints (约束规则)                  │
│  CLAUDE.md / AGENTS.md / PROJECT_RULES.md /     │
│  ai-workflow.md / pitfalls.md / tests_guideline  │
├─────────────────────────────────────────────────┤
│  Layer 1: Methodology (方法论)                    │
│  Ask→Code / Sprint+Pack / TDD-first /           │
│  编码前避坑检索 / 文档闭环 / 交叉复核              │
└─────────────────────────────────────────────────┘
```

---

## 快速上手（3 步）

### Step 1: 安装 Skill

```bash
# 克隆本仓库
git clone <this-repo-url> /tmp/ai-workflow-kit

# 一键安装 9 个通用 Skill 到 Claude Code
bash /tmp/ai-workflow-kit/install.sh
```

### Step 2: 初始化项目文档骨架

在你的项目根目录运行：

```bash
# 生成完整文档结构（CLAUDE.md / AGENTS.md / docs/ 全套）
python ~/.claude/skills/spec-arch-adapter/scripts/spec_arch_audit.py --root . --mode write --profile full
```

这会创建：
- `README.md` / `CLAUDE.md` / `AGENTS.md` — 项目入口
- `docs/task/progress.md` — 任务游标
- `docs/sprint/README.md` — Sprint 索引
- `docs/qa/pitfalls.md` — 活跃坑位索引
- `docs/qa/pitfalls_archive/README.md` — 历史 RCA 归档
- `docs/rules/PROJECT_RULES.md` — 开发规则
- `docs/review/ai-workflow.md` — AI 工作流程
- `docs/qa/tests_guideline.txt` — 测试规范
- 以及 spec / design / research / task/archive 等目录

### Step 3: 读完下面的方法论，开始用

### 想直接看实战？

跳到 **[完整实战示例](examples/end-to-end-walkthrough.md)** — 以一个 CSV 去重 CLI 工具为例，从零到交付完整走一遍 6 步流程：

```
初始化项目 → 写 Sprint 文档 → /sprint-design-reviewer（设计评审）
    → /tdd-loop-executor（TDD 开发）→ /cross-review-gate（交叉审查）
    → /sprint-close-auditor（收口审计）→ 提交
```

示例中包含：每一步你该输入什么、AI 会做什么、你会看到什么输出、以及遇到 bug 时 pitfalls 卡片怎么自动生成。

---

## 方法论详解

### 1. Ask → Code 双阶段

**不要让 AI 一上来就写代码。**

| 阶段 | 做什么 | 产出 |
|------|--------|------|
| **Ask**（规划） | 分析目标、列出改动范围、量化工作量（≤ 数百行/~1h） | 计划草稿 |
| **Code**（执行） | 严格按计划写代码+测试 | 代码变更 |

为什么分两步：
- 让 AI 有明确的 scope 边界，不会"顺手"改一堆无关的东西
- 计划可以被 review，代码写错了计划还在，可以回退重来
- 计划像一个 mini PR description，包含背景/目标/范围/DoD

### 2. Sprint + Pack 结构

工作以 **Sprint**（冲刺）为单位组织，Sprint 内拆成 **Pack**（执行卡片）。

- **Sprint** = 一个明确的研究/工程目标，文档在 `docs/sprint/sprintN.md`
- **Pack** = Sprint 内的子任务，有明确的 DoD、范围、可跑命令

什么时候建 Pack：
- 跨 3+ 模块或涉及外部服务
- 估时 >1 天或 >2 PR
- 需要异步链路证据

简单改动不建 Pack，直接做。

### 3. TDD-first（测试驱动）

```
RED → GREEN → REFACTOR
```

1. 先写/补一个失败的测试（RED）
2. 写最小代码让测试通过（GREEN）
3. 做必要的重构（REFACTOR）

为什么强制：
- 防止 AI 写出"看起来对但其实没测过"的代码
- 测试就是 DoD 的可执行形式
- 回归保护 — 下次改动不会悄悄破坏已有功能

### 4. 编码前避坑检索（强制）

**每次开工前，先查已知坑位。**

```bash
# 查当前活跃坑位
rg -n "关键词" docs/qa/pitfalls.md

# 查历史归档（涉及复杂模块时）
rg -n "关键词" docs/qa/pitfalls_archive/
```

在 Ask 计划中写明：
- 命中了哪些坑位（标题 + 路径）
- 每条对应的防回归措施
- 如果没命中：`pitfalls hit: none (keywords=...)`

为什么强制：
- 同一个坑踩两次是最大的浪费
- AI 换了 session 就忘了上次的教训，pitfalls 文件是跨 session 的记忆

### 5. 文档闭环

每轮结束更新 `docs/task/progress.md`：
- 今日进展 / 明日计划 / 风险与阻塞 / 关联链接

规则：
- 游标精简（≤ 5 个热点，≤ 100 行），旧内容归档到 `docs/task/archive/`
- `pitfalls.md` 只保留 ACTIVE 卡片（≤ 10 张，≤ 250 行），详细 RCA 归档
- Bugfix 必须更新 pitfalls 卡片
- Sprint close 必须做 pitfalls 收口

### 6. 交叉复核

重要决策不靠单一分析：
- **代码审查**：多专家并行 review + 交叉质疑 → 过滤误报
- **外部模型验证**：GPT/Gemini 给的建议，逐条读源码验证，不盲信也不盲拒

---

## Skill 速查表

### 什么时候用哪个 Skill

| 你在做什么 | 用哪个 Skill | 触发命令 |
|-----------|-------------|---------|
| 写完 sprint.md，想确认设计可行 | Sprint Design Reviewer | `/sprint-design-reviewer` |
| 按 Pack 写代码+测试 | TDD Loop Executor | `/tdd-loop-executor` |
| 运行时报错要排查 | Log Rootcause Triage | `/log-rootcause-triage` |
| 代码写完，提交前 review | Cross Review Gate | `/cross-review-gate` |
| 只需要单轮快速 review | Code Review Expert | `/code-review-expert` |
| GPT/Gemini 给了建议，想验证 | Adversarial Cross-Model Review | `/adversarial-cross-model-review` |
| Sprint 结束，想确认是否可以关 | Sprint Close Auditor | `/sprint-close-auditor` |
| 新项目，从零搭建文档骨架 | Spec Arch Adapter | `/spec-arch-adapter` |
| 需要全局了解项目状态 | Project Roadmap Research | `/project-roadmap-research` |

### 推荐的最小上手路径

先学会 3 个 Skill 就够了：

1. **`/tdd-loop-executor`** — 日常写代码的主力，替你管 TDD 循环和 progress 更新
2. **`/cross-review-gate`** — 提交前跑一次，4 个专家角度交叉 review
3. **`/sprint-design-reviewer`** — 开工前跑一次，确认设计没问题

其余的按需使用。

---

## Skill 详细说明

### Sprint Design Reviewer

Sprint 开工前的设计评审。自动检测 Sprint 类型（策略/工程/混合），组装对应专家面板：

- **策略类**：量化策略师 + 统计学家 + 风控专家 + 代码评审专家
- **工程类**：架构师 + 代码评审专家 + QA 负责人
- **混合类**：量化策略师 + 架构师 + 代码评审专家 + 风控专家

输出 Approve / Conditional / Reject 判定，附每个维度的评分和 Confirmed/Disputed findings。

### TDD Loop Executor

持续 TDD 循环直到任务完成：
1. Ask 阶段读 CLAUDE.md + Sprint 文档 + progress，定范围
2. Code 阶段严格 RED→GREEN→REFACTOR
3. 每轮更新 progress.md
4. 用户说 `continue` 就从下一步继续

支持 Sprint 快捷方式：`/tdd-loop-executor s5 go` = 执行 Sprint 5。

### Cross Review Gate

多专家交叉代码审查 + 质量门禁：
- **5 个并行 agent**：架构师 / 正确性 / 安全性 / 性能 / QA
- 3 步交叉质疑过滤误报（架构师合并重复根因 → 代码专家质疑 QA → QA 质疑代码专家）
- 输出 Pass / Conditional Pass / Fail + Release Readiness 判定
- 架构师负责合并重复 findings，QA Lead 拥有否决权

> **架构说明**：5 个专家角色各有独立的 agent 定义文件（`agents/*.md`），包含精确的职责、审查维度、checklist、输出格式和行为准则。`cross-review-gate` SKILL.md 负责编排流程（spawn → 交叉质疑 → 汇总），agent 文件负责定义"每个专家是谁、怎么审"。

> **轻量替代**：小改动（单函数/单文件）用 `/code-review-expert` 做单人快速 review，不需要启动 5 专家。

### Sprint Close Auditor

Sprint 收口审计：
- 逐条对账 Sprint 文档中的任务 vs 代码/测试实际状态
- 输出 Complete / Partial / Blocked + 逐任务完成矩阵

### Code Review Expert

单轮深度代码审查，按 P0-P3 严重度排序，每条附 `file:line` 证据和修复建议。

### Adversarial Cross-Model Review

对外部 AI 模型的审查结论做对抗性验证：
- 3 个专家（架构师/代码/QA）独立读源码验证
- 输出 Adopt / Partial adopt / Reject / Defer

核心原则：**每个判定必须引用源码，不许凭推理同意或否定。**

### Log Rootcause Triage

运行时日志/栈追踪的根因分析：
- 提取时间线 → 构建假设 → 确认根因 → 最小修复方案

### Spec Arch Adapter

新项目文档骨架生成器。自动检测语言/入口，生成完整的文档架构。

### Project Roadmap Research

只读的全局项目状态快照。扫描 CLAUDE.md + Sprint 文档 + 代码，输出架构图、数据流、风险清单。

---

## 文件结构

```
ai-workflow-kit/
├── README.md                          # 本文件（方法论手册）
├── install.sh                         # 一键安装脚本
├── skills/                            # 9 个通用 Claude Code Skills
│   ├── sprint-design-reviewer/        # Sprint 设计评审
│   ├── sprint-close-auditor/          # Sprint 收口审计
│   ├── cross-review-gate/             # 多专家交叉 code review
│   ├── code-review-expert/            # 单轮深度 code review
│   ├── tdd-loop-executor/             # TDD 循环执行器
│   ├── log-rootcause-triage/          # 日志根因分析
│   ├── spec-arch-adapter/             # 文档骨架生成器
│   ├── adversarial-cross-model-review/# 外部模型结论验证
│   └── project-roadmap-research/      # 项目 roadmap 快照
├── agents/                            # Agent 角色定义（独立的专家角色）
│   ├── code-review-expert.md          # 通用审查专家（全栈单人 review + 格式基准）
│   ├── architect.md                   # 架构师（设计合理性/trade-off/YAGNI/可逆性）
│   ├── reviewer-correctness.md        # 正确性专家（逻辑/回归/状态机/边界）
│   ├── reviewer-security.md           # 安全性专家（STRIDE/依赖链/密码学/验证）
│   ├── reviewer-performance.md        # 性能专家（N+1/数据结构/I-O 模式/复杂度）
│   └── reviewer-qa-lead.md            # QA 负责人（测试/风险/上线判定/否决权）
├── templates/                         # 独立模板文件（供参考）
│   ├── pitfalls.md                    # 活跃坑位索引模板
│   ├── pitfalls_archive_README.md     # 坑位归档目录说明
│   └── sprint-template.md            # Sprint 文档模板
└── examples/
    ├── end-to-end-walkthrough.md      # 完整实战示例（推荐先读）
    └── workflow-diagram.md            # 流程图示例
```

---

## 定制与扩展

### 适配你的项目

安装后，你需要根据项目实际情况修改以下文件：

1. **`AGENTS.md`** — 补充你的语言/命名/风格规范
2. **`docs/rules/PROJECT_RULES.md`** — 调整规则优先级，删除不适用的条目
3. **`docs/qa/tests_guideline.txt`** — 补充你的测试框架和运行命令
4. **`docs/review/ai-workflow.md`** — 如有领域特殊流程，在此追加

### 添加领域特定 Skill

本工具包只包含通用 Skill。如果你需要领域特定的 Skill（如回测、实时数据采样），可以按相同格式在 `~/.claude/skills/` 下创建。

Skill 文件结构：
```
~/.claude/skills/<skill-name>/
├── SKILL.md              # 主文件：name / description / workflow / output format
└── references/           # 可选：检查清单、命令模板等参考材料
```

---

## FAQ

**Q: 我的项目很小，需要这么多文档吗？**
A: 用 `--profile minimal` 模式只生成核心文件（README/CLAUDE.md/AGENTS.md/progress）。Sprint/Pack 等结构等项目长大了再加。

**Q: 我不用 Python，这套东西能用吗？**
A: 方法论和 Skill 是语言无关的。spec-arch-adapter 会自动检测你的技术栈。tests_guideline 需要你自己补充框架命令。

**Q: 我只想用 Skill，不想搞文档结构？**
A: 可以。但 `/tdd-loop-executor` 和 `/sprint-close-auditor` 依赖 progress.md 和 sprint 文档才能正常工作。至少需要 `docs/task/progress.md`。

**Q: 这些 Skill 之间有依赖关系吗？**
A: 没有硬依赖。但它们设计为配合使用：design review → TDD loop → cross review → close audit 是完整的闭环。

**Q: 专家交叉复核会不会太慢？**
A: `/cross-review-gate` 通常需要 1-3 分钟（4 个 agent 并行）。日常快速 review 用 `/code-review-expert` 更快。

---

## 致谢

本工具包从 [polyinit](https://github.com/licett/polyinit) 项目的 42 个 Sprint 实战中提炼而来。其中的约束规则和 Skill 设计来自真实的生产踩坑经验。

---

**维护者**: @licett
**许可**: MIT

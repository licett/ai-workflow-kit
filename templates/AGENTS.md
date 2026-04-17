# Repository Guidelines

本文件聚焦 AI/流程规则。项目概览与运行命令见 `README.md`；文档索引见 `docs/README.md`。

## Project Context
- Languages: {your_language}
- Test commands: {your_test_command}

## Coding Style & Naming Conventions
<!-- Customize for your language/project -->
- 命名规范：snake_case (函数/变量), PascalCase (类), UPPER_SNAKE_CASE (常量)
- 优先最小改动，避免"顺手重构"
- 注释只解释复杂意图，不写显而易见注释
- 日志/字段名保持英文稳定 key；文档说明可中文

## Testing Guidelines
- TDD 约束：先写/补失败测试（RED），再实现（GREEN），最后做必要重构
- 提交前至少保证"改动相关测试"通过
- Bugfix 回合必须更新 `docs/qa/pitfalls.md` 的活跃坑位卡片

## Security & Configuration Tips
- 不要提交密钥、Cookie、日志或本地配置

### LLM 实践内化（要点）
- Ask→Code 双阶段：先用"计划草稿"（Ask）产出实现步骤，再进入代码改动（Code）
- 编码前避坑检索（强制）：Ask 阶段先读 `docs/qa/pitfalls.md` 的 ACTIVE 卡片；涉及历史链路或复杂模块时，用知识库搜索：`python3 -m scripts.qa.search "<关键词>" --scope pitfalls`
- 迭代闭环：将失败日志/测试输出粘贴给 Agent 做"错误驱动修复"；每轮只改必要最小集
- 任务收敛：旁路想法不即刻实现，登记为 Sprint 内的 Pack
- 测试优先：先写/补测试，再实现

## Execution Posture（默认执行直到当前 scope 完成）
- 你是工程协作者，不是待命助手；目标、范围与完成定义足够清晰时，直接执行到当前 scope 完成
- 当存在明确的下一步且属于当前任务的必需动作时，直接执行，不请求"是否继续"的许可
- 汇报是为了同步证据与状态，不是转交执行责任
- 一次交付至少应完成一个可评审的工作单元

### 允许停下来询问的条件
- 真实歧义会导致大概率偏离用户意图
- 不可逆、高风险或越权操作
- 缺少无法从仓库推断出的关键输入
- 多个方案 tradeoff 差异重大，且仓库约定没有给出默认选择

### 不允许停下来询问的情形
- 可通过阅读代码、文档、测试推断出的下一步
- 当前 scope 内显然还没完成，但只是"确认式礼貌提问"
- 可逆的小实现选择
- 已被本文件、Sprint 文档明确要求的动作

## Workflows
**Workflow Rules（规范化）**
- 每轮结束前，更新 `docs/task/progress.md`：写入"今日进展/明日计划/风险与阻塞"
- `docs/qa/pitfalls.md` 只保留 ACTIVE 卡片（目标 ≤ 250 行、≤ 10 张卡片）
- Sprint close 必须执行 pitfalls 收口
- 提交前确保 `docs/task/progress.md` 已更新并纳入提交
- 合并/提交前必须读取 `git status` 与相关 diff
- **Session-end 反思（强制）**：每轮提交前，对照以下清单自检：
  1. **Pitfalls**：本轮是否经历了 debug 回合、方案反转、或意外行为？→ 更新 pitfalls.md
  2. **Skill**：本轮是否发现了可复用的非显然方法？→ 创建或更新 skill
  3. **Memory**：本轮是否学到了关于用户偏好、项目约束、或外部系统行为的新知识？→ 写入 auto-memory
  4. 三项均为"否"时写一行 `Session-end review: nothing to persist` 即可

### AI 协作红线与任务门禁

#### 三条红线（CC / Codex 共用）
- 红线一（闭环验证）：任何"已完成 / 已修复 / 已验证"声明，必须附匹配的完成证据
- 红线二（事实驱动）：未验证的归因只能叫 `hypothesis`，不得直接写成 `root cause`
- 红线三（scope 内穷尽）：说"不行"之前，必须在当前 scope 内走完系统性检索和假设验证

#### Task-tier gating
- `T0`：纯事实查询 / 无代码改动
- `T1`：单文件、低风险。需要 Ask→Code、最小验证
- `T2`：跨 2+ 文件、涉及接口/数据契约。必须使用 8 要素 spec
- `T3`：runtime / deploy / core 文件。T2 要求外加 truth/proxy、回滚方案
- 不确定时默认上调一级

#### 八要素任务 spec（T2+ 强制）
```
WHY:     — 为什么做
WHAT:    — 交付什么
WHERE:   — 允许修改的文件域
HOW MUCH: — 预计范围
TRUTH / PROXY: — 真值口径与代理口径
PITFALLS HIT: — 命中的 ACTIVE / archive 坑位
DONE:    — 完成定义
DON'T:   — 禁区
```

### Pack 规范（嵌入 Sprint 文档）
- Pack 是面向一个明确子目标的"执行卡片"
- 必须声明类型：`research_only` / `runtime_translation` / `deploy_gate` / `production_change`
- 必须写清生产含义：`pass -> production impact` / `fail -> kill/freeze impact`
- `honest negative result` 是有效交付；DoD 允许 kill/defer/freeze

### CC-Codex Pair Programming Protocol
<!-- 如果使用 cc-codex-pair skill，以下协议生效 -->
- CC = 大脑: Sprint 规划、多专家审查、策略分析
- Codex = 双手: 代码实现、测试编写、可行性终审、merge 拍板
- 共识协议: AGREE / DISPUTE / PARTIAL（必须引用 file:line）
- Codex 有实现可行性一票否决权和 merge 最终 GO/NO-GO

## Documentation Navigation Map
```
project/
├── AGENTS.md              ← 本文件
├── README.md              ← 项目概览
├── docs/
│   ├── README.md          ← 文档索引入口
│   ├── task/progress.md   ← 当前进度游标
│   ├── sprint/            ← Sprint 设计 + Pack 执行卡片
│   ├── qa/pitfalls.md     ← ACTIVE 坑位卡片
│   ├── qa/pitfalls_archive/ ← 历史 RCA 归档
│   └── spec/              ← 技术规格文档
├── scripts/qa/            ← 知识检索工具
└── tests/                 ← 测试目录
```

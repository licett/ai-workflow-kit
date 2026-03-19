# Repository Guidelines

本文件聚焦 AI/流程规则。项目概览与运行命令见 `README.md`；文档索引见 `docs/README.md`。

## Project Context
- Languages: {languages}
- Entry candidates: {entrypoints}
- Test commands (suggested): {test_commands}

## Coding Style & Naming Conventions
- 请根据项目实际情况补充语言/风格规范，例如：
  - 模块/函数/变量：`snake_case`
  - 类名：`PascalCase`
  - 常量：`UPPER_SNAKE_CASE`
- 新增或修改的核心逻辑优先补充类型注解。
- 优先最小改动，避免"顺手重构"。
- 注释只解释复杂意图，不写显而易见注释。

## Testing Guidelines
- 详细规范主文档：`docs/qa/tests_guideline.txt`（本文件为单一事实源）。
- TDD 约束：先写/补失败测试（RED），再实现（GREEN），最后做必要重构。
- 提交前至少保证"改动相关测试"通过。
- Bugfix 回合必须更新 `docs/qa/pitfalls.md` 的活跃坑位卡片；若为新根因，新增 1 张 ACTIVE 卡片，并将完整 RCA 写入 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md`。

## Security & Configuration Tips
- 不要提交密钥、Cookie、日志或本地配置。

### LLM 实践内化（要点）
- Ask→Code 双阶段：先用"计划草稿"（Ask）产出实现步骤，再进入代码改动（Code）。计划需量化范围（≤ 数百行/≈1小时）。
- 提示像 Issue/PR：包含背景/目标/范围边界/相关文件路径/验收标准（DoD）/参考实现链接。
- 编码前避坑检索（强制）：Ask 阶段先检索 `docs/qa/pitfalls.md` 的 ACTIVE 卡片；涉及历史链路或复杂模块时，再检索 `docs/qa/pitfalls_archive/` 并在计划中写明"命中坑点 + 防回归措施"（详细步骤见 `docs/review/ai-workflow.md`）。
- 持久上下文：以本文件与 `docs/review/ai-workflow.md` 作为 Agent 的长期语境；命名/安全/TDD 约束为强约束。
- 迭代闭环：将失败日志/测试输出粘贴给 Agent 做"错误驱动修复"；每轮只改必要最小集（遵守 Rule 3/4）。
- Best-of-N：跨多文件/高风险变更时，先生成2–3种方案对比再定案（可在 `docs/task/progress.md` 记录备选）。
- 任务收敛：旁路想法不即刻实现，登记为 Sprint 内的 Pack（锚点位于 `docs/sprint/sprint[x].md`）。
- 测试优先：先写/补测试，再实现；必要时用 `--override-ini="addopts="` 仅跑新增用例。

## workflows
**Workflow Rules（规范化）**
- 每轮结束前，更新 `docs/task/progress.md`：写入"今日进展/明日计划/风险与阻塞/关联链接"。
- 进度游标限长（建议 ≤ 100 行）：仅保留 Top 3–5 个"热点任务"，其余详述请链接到 Sprint 文档中的 Pack 小节。
- 归档旧内容：将较早的"今日进展"等段落移动到 `docs/task/archive/YYYY-MM-DD.md`，保证游标精简。（目录不存在时可创建）
- `docs/qa/pitfalls.md` 只保留 ACTIVE 卡片（目标 `<= 250` 行、`<= 10` 张卡片）；同根因复发时更新现有卡片，不追加重复。
- Sprint close / 长周期 Pack close 必须执行 pitfalls 收口：完整 RCA 迁到 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md`，主文件只保留活跃卡片与归档入口。
- 提交前确保 `docs/task/progress.md` 已更新并纳入提交；每轮结束进行一次提交。
- 合并/提交前必须读取 `git status` 与相关 diff。
- `src/` 新目录/新入口变更需同步更新 module map。
- 每次会话结束后，如有必要补全 spec 架构与文档入口。
- 当用户说 `continue`，直接从 `docs/task/progress.md` 的下一步动作开始执行。
**Reference**
- 详细计划、开放任务与后续行动以 `docs/task/progress.md` 为准（游标+链接），细化执行卡片沉入对应 Sprint 文档内的 Pack 小节。

### Pack 规范（嵌入 Sprint 文档）
- 定义：Pack 是面向一个明确子目标的"执行卡片"，包含目标、范围、DoD、可跑指令、产物与风险，便于复现与验收。
- 位置：直接写在对应 `docs/sprint/sprint[x].md` 中，使用标题格式 `### Pack: <短名>`，避免新增目录层级。
- 触发：当某热点跨 3+ 模块/涉及外部服务/需要异步链路证据/估时>1 天或>2 PR 时，建立 Pack；简单改动不建。
- 内容模板：
  - 背景/目标：要达成的量化结果；
  - 范围边界：改哪些文件/不做哪些事；
  - DoD：通过标准（含指标/产物路径）；
  - 文档收口：若本 Pack 关闭 Sprint 或收敛长期热点，必须更新 `progress.md` / `pitfalls.md` 并执行归档；
  - 指令与测试：精确到命令与 `tests/...::case`，必要时 `--override-ini="addopts="`；
  - 产物与路径：`data/...`、`var/reports/...`、日志位置；
  - 风险/回滚：已知问题与降级策略；
  - 负责人/时间与关联链接：Owner、ETA、PR/提交/日志链接。
- 链接策略：`docs/task/progress.md` 仅列"热点标题 + 链接到 Sprint 内的 Pack 锚点"，不复制 Pack 内容。

## 附加文档
- `docs/README.md`
- `docs/task/progress.md`
- `docs/sprint/README.md`
- `docs/spec/README.md`

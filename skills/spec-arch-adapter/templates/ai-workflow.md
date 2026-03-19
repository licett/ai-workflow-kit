# AI 工作流程

本文档定义 AI 助手（如 Claude Code、GitHub Copilot、Cursor 等）在本项目中的标准工作流程和最佳实践。

## 核心原则

### 1. 双阶段工作流：Ask → Code

**Ask 阶段（规划）**:
- 先产出"计划草稿"，明确实现步骤
- 量化范围：≤ 数百行代码 / ≈1小时工作量
- 列出需要修改的文件、函数、测试
- 识别潜在风险和依赖

**Code 阶段（执行）**:
- 严格按计划执行
- 遵循最小改动原则（Rule 3, 4）
- 每次只改必要的最小集

### 1.1 编码前避坑检索（强制）

在 Ask 阶段进入代码改动前，必须完成以下动作：

1. 先读当前活跃坑位：
   - `docs/qa/pitfalls.md`
2. 再做历史坑位检索（满足任一条件即执行）：
   - 涉及历史链路（日报/门禁/数据湖/回测等）
   - 任务跨 2+ 模块或高风险改动
   - 对字段口径/时间窗/开关语义有变更
   - 检索范围：`docs/qa/pitfalls_archive/`
3. 在 Ask 计划中显式写出：
   - 命中的 1-3 条坑点（标题 + 路径）
   - 每条对应的"防回归措施"（测试/断言/门禁）
4. 若未命中，也要写明：
   - `pitfalls hit: none (keywords=...)`

建议检索命令：

```bash
# 当前活跃坑位（先看）
rg -n "关键词A|关键词B" docs/qa/pitfalls.md

# 历史归档（再查）
rg -n "关键词A|关键词B" docs/qa/pitfalls_archive/
```

### 2. 提示规范（类似 Issue/PR）

每个任务提示应包含：
- **背景**: 为什么要做这个改动
- **目标**: 要达成的具体结果（量化）
- **范围边界**: 改哪些 / 不改哪些
- **相关文件路径**: 明确需要修改的文件
- **验收标准（DoD）**: 如何判断完成
  - 测试通过：`pytest tests/xxx/test_yyy.py::test_case`
  - 代码规范：符合 PROJECT_RULES.md
  - 功能验证：手动测试步骤或指标
- **参考实现链接**: 相关文档、代码示例

### 3. 持久上下文

长期语境文件（AI 必读）：
- `CLAUDE.md` - 项目架构和命令
- `docs/rules/PROJECT_RULES.md` - 开发规则（强约束）
- `docs/qa/tests_guideline.txt` - 测试规范
- `docs/qa/pitfalls.md` - 活跃坑位索引
- `docs/task/progress.md` - 当前任务游标

强约束（不可违反）：
- 命名规范
- 安全要求（日志脱敏、密钥保护）
- TDD 要求（先写测试再写实现）

### 4. 迭代闭环（错误驱动修复）

当出现错误时：
1. 将完整错误日志/测试输出粘贴给 AI
2. AI 分析根因并制定修复计划
3. 执行最小修复（遵守 Rule 3/4）
4. 验证修复效果
5. 记录到 `docs/task/progress.md`
6. **补充踩坑记录**：
   - 优先更新 `docs/qa/pitfalls.md` 中同根因的 ACTIVE 卡片；
   - 若为新根因，新增 1 张 ACTIVE 卡片；
   - 完整 RCA 写入 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md` 或对应 Sprint close 文档，再把路径回链到 ACTIVE 卡片。

### 5. Best-of-N 方案对比

对于复杂任务（跨多文件/高风险）：
1. 先生成 2-3 种备选方案
2. 对比各方案的优缺点
3. 在 `docs/task/progress.md` 记录备选方案
4. 选定一个方案后再实施

### 6. 任务收敛

**立即执行** vs **延后登记**：
- 当前 Sprint 必须项：立即执行
- 旁路想法/优化建议：不即刻实现
- 延后任务登记为 Pack：
  - 锚点位于 `docs/sprint/sprint[x].md`
  - 在 `docs/task/progress.md` 中链接到 Pack

### 7. 测试优先（TDD）

标准流程：
1. 先写/补测试用例
2. 确认测试失败（红灯）
3. 实现功能代码
4. 确认测试通过（绿灯）
5. 重构优化（如需）

运行特定测试：
```bash
# 仅运行新增用例
pytest tests/xxx/test_new.py -v

# 覆盖默认配置
pytest --override-ini="addopts=" tests/xxx/test_new.py
```

## 工作流规范

### 每轮结束前

1. **更新进度文档** (`docs/task/progress.md`):
   - 今日进展（已完成的任务）
   - 明日计划（下一步行动）
   - 风险与阻塞（遇到的问题）
   - 关联链接（相关 PR/commit/文档）

2. **精简游标**（≤ 100 行）:
   - 仅保留 Top 3-5 个"热点任务"
   - 其余详述链接到 Sprint 文档中的 Pack 小节

3. **归档旧内容**:
   - 将较早的"今日进展"移动到 `docs/task/archive/YYYY-MM-DD.md`
   - 保证游标精简易读

4. **提交变更**:
   - 确保 `docs/task/progress.md` 已更新并纳入提交
   - 每轮结束进行一次提交
   - 合并/提交前必须读取 `git status` 与相关 diff
   - `src/` 新目录/新入口变更需同步更新 module map

5. **Bugfix 复盘（强制）**:
   - 若本轮包含 bug 修复/事故修复：必须更新 `docs/qa/pitfalls.md` 的 ACTIVE 卡片；若为新根因，再新增 1 张卡片
   - 完整 RCA 放到 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md` 或 Sprint close 文档，再从 ACTIVE 卡片回链
   - 目的：降低"同类问题复发"概率，方便未来快速排障

### 文档游标与归档闭环

- `docs/task/progress.md` 的角色是"活跃任务游标"，不是无限追加的工作日志：
  - 主文件只保留下一步要继续推进的 Top 3-5 个热点；
  - 目标长度：`<= 100` 行；
  - 已完成或降温的条目迁到 `docs/task/archive/YYYY-MM-DD[-suffix].md`。
- `docs/qa/pitfalls.md` 的角色是"活跃坑位索引"，不是长期账本：
  - 主文件只保留 ACTIVE 卡片与归档入口；
  - 目标长度：`<= 250` 行，ACTIVE 卡片 `<= 10` 张；
  - 历史详细记录迁到 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md`；
- 必须触发归档收口的场景（满足任一条即执行）：
  - Sprint close / 长周期 Pack close；
  - `progress.md` 超过 `100` 行或热点 section 超过 `5` 个；
  - `pitfalls.md` 超过 `250` 行、ACTIVE 卡片超过 `10` 张；
  - 主文件已经明显影响效率。
- 收口步骤固定为：
  1. 先生成 archive snapshot；
  2. 再重写主文件为短游标 / 活跃索引；
  3. 在 `docs/task/progress.md` 或 close summary 中补 archive 路径；
  4. 若本轮 close 没有新增 pitfalls，也要显式写明"本轮仅做归档，无新增坑位"。

### Continue 指令

当用户说 `continue` 时：
- 直接从 `docs/task/progress.md` 的"下一步行动"开始执行
- 不需要再次询问或确认

## Pack 规范（执行卡片）

### 定义

Pack 是面向一个明确子目标的"执行卡片"，便于复现与验收。

### 触发条件

满足以下任一条件时建立 Pack：
- 跨 3+ 模块/涉及外部服务
- 需要异步链路证据
- 估时 >1 天 或 >2 PR
- 需要团队协作

简单改动不建 Pack。

### 位置

直接写在对应 `docs/sprint/sprint[x].md` 中：
- 使用标题格式：`### Pack: <短名>`
- 避免新增目录层级

### 内容模板

```markdown
### Pack: [短名]

**背景/目标**:
- 要达成的量化结果

**范围边界**:
- 改哪些文件：`src/xxx/yyy.py`
- 不做哪些事：明确排除范围

**DoD（完成标准）**:
- [ ] 测试通过：`pytest tests/xxx/test_yyy.py::test_case`
- [ ] 代码审查通过
- [ ] 产物已生成：`data/reports/xxx.json`
- [ ] 文档收口（如本 Pack 关闭 Sprint / 收敛长期热点）：`progress.md` / `pitfalls.md` 已摘要归档

**指令与测试**:
```bash
pytest tests/xxx/test_yyy.py::test_case -v
```

**产物与路径**:
- 日志：`var/logs/xxx.log`
- 报告：`data/reports/xxx.json`

**风险/回滚**:
- 已知问题：xxx
- 降级策略：yyy

**负责人/时间与关联链接**:
- Owner: @user
- ETA: YYYY-MM-DD
- PR: #123
```

### 链接策略

在 `docs/task/progress.md` 中：
- 仅列"热点标题 + 链接到 Sprint 内的 Pack 锚点"
- 不复制 Pack 内容

## 质量检查清单

每次提交前检查：

### 代码质量
- [ ] 遵循 PROJECT_RULES.md 所有规则
- [ ] 最小改动原则（Rule 4）
- [ ] 代码风格一致
- [ ] 无安全漏洞
- [ ] 日志已脱敏（不输出敏感信息）

### 测试覆盖
- [ ] 新功能有对应测试
- [ ] 所有测试通过
- [ ] 边界条件已测试

### 文档更新
- [ ] `docs/task/progress.md` 已更新
- [ ] `docs/qa/pitfalls.md` 已更新或确认本轮无需新增
- [ ] 相关 Sprint 文档已同步

### 提交规范
- [ ] Commit 信息清晰
- [ ] 变更已分组（不混杂无关改动）
- [ ] 所有修改都在任务范围内

## 常见场景

### 场景1: 实现新功能

1. 阅读 Sprint 文档了解需求
2. **检索 `docs/qa/pitfalls.md` 活跃坑位**
3. 检查 `docs/task/progress.md` 确认优先级
4. 制定实现计划（Ask 阶段）
5. 先写测试用例
6. 实现功能代码
7. 验证测试通过
8. 更新文档
9. 提交变更

### 场景2: 修复 Bug

1. 复现问题（收集错误日志）
2. 定位根因（分析代码）
3. 编写测试用例（复现 bug）
4. 最小修复（遵循 Rule 3/4）
5. 验证修复效果
6. **更新 pitfalls.md（新增或更新 ACTIVE 卡片）**
7. 记录到 progress.md
8. 提交变更

### 场景3: 代码重构

1. 明确重构目标（性能/可读性/可维护性）
2. 先补充测试覆盖（确保行为不变）
3. 小步重构（一次一个模块）
4. 每步验证测试通过
5. 更新文档（如有架构变化）
6. 提交变更

### 场景4: 跨会话恢复

1. 阅读 `docs/task/progress.md` 了解上次进度
2. 查看最新 git 状态
3. 检查相关 Sprint 文档
4. 从"下一步行动"继续执行

## 参考资料

- [`docs/rules/PROJECT_RULES.md`](../rules/PROJECT_RULES.md) - 项目开发规则
- [`docs/qa/tests_guideline.txt`](../qa/tests_guideline.txt) - 测试规范
- [`docs/qa/pitfalls.md`](../qa/pitfalls.md) - 活跃坑位索引
- [`docs/task/progress.md`](../task/progress.md) - 当前任务游标

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
   - 涉及历史链路（日报/门禁/数据湖/回测）
   - 任务跨 2+ 模块或高风险改动
   - 对字段口径/时间窗/开关语义有变更
   - 检索范围：`docs/qa/pitfalls_archive/`
3. 在 Ask 计划中显式写出：
   - 命中的 1-3 条坑点（标题 + 路径）
   - 每条对应的“防回归措施”（测试/断言/门禁）
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
- `docs/spec/runtime_deploy_contract_v1.md` - runtime / pig / manager / force-profile 操作合同
- `docs/task/progress.md` - 当前任务游标

强约束（不可违反）：
- 命名规范
- 安全要求（日志脱敏、SQL注入防护）
- TDD 要求（先写测试再写实现）
- 涉及 runtime / deploy / pig 操作时，不得绕过 `docs/spec/runtime_deploy_contract_v1.md` 的角色边界与 canonical flow

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
- ✅ 当前 Sprint 必须项：立即执行
- ❌ 旁路想法/优化建议：不即刻实现
- 📝 延后任务登记为 Pack：
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
    - 新建/修改源文件必须在文件头部添加 ≤50 字概要；JSON 文件使用首字段 `_comment`（不影响解析）或同名 `.md` 首行摘要（≤50 字）

5. **Bugfix 复盘（强制）**:
   - 若本轮包含 bug 修复/事故修复：必须更新 `docs/qa/pitfalls.md` 的 ACTIVE 卡片；若为新根因，再新增 1 张卡片
   - 完整 RCA 放到 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md` 或 Sprint close 文档，再从 ACTIVE 卡片回链
   - 目的：降低“同类问题复发”概率，方便未来快速排障

### 文档游标与归档闭环

- `docs/task/progress.md` 的角色是“活跃任务游标”，不是无限追加的工作日志：
  - 主文件只保留下一步要继续推进的 Top 3-5 个热点；
  - 目标长度：`<= 100` 行；
  - 已完成或降温的条目迁到 `docs/task/archive/YYYY-MM-DD[-suffix].md`。
- `docs/qa/pitfalls.md` 的角色是“活跃坑位索引 + 最近高信号复盘”，不是长期账本：
  - 主文件只保留 ACTIVE 卡片与归档入口；
  - 目标长度：`<= 250` 行，ACTIVE 卡片 `<= 10` 张；
  - 历史详细记录迁到 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md`；
  - 活跃索引顺序、条数必须与 ACTIVE 卡片一致。
- 必须触发归档收口的场景（满足任一条即执行）：
  - Sprint close / 长周期 Pack close；
  - `progress.md` 超过 `100` 行或热点 section 超过 `5` 个；
  - `pitfalls.md` 超过 `250` 行、ACTIVE 卡片超过 `10` 张、或跨月后仍保留大量已降温坑位；
  - 主文件已经明显影响 `continue`、编码前避坑检索或 Sprint 对账效率。
- 收口步骤固定为：
  1. 先生成 archive snapshot；
  2. 再重写主文件为短游标 / 活跃索引；
  3. 在 `docs/task/progress.md` 或 close summary 中补 archive 路径；
  4. 若本轮 close 没有新增 pitfalls，也要显式写明“本轮仅做归档，无新增坑位”。
  5. 运行 `python -m scripts.docs.check_doc_cursors`，让 `progress.md` / `pitfalls.md` 通过结构守门。

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

### 强制治理字段

- `Pack type`：必须显式标注 `research_only` / `runtime_translation` / `deploy_gate` / `production_change`
- `Production implication`：必须同时写出
  - `if pass, production changes what`
  - `if fail, what line is killed / frozen / downgraded`
- `Truth contract / Proxy contract`：任何收益、准入或执行改善声明都必须区分
  - `truth source`
  - `proxy source`
  - `bias / missing surface / fail-close rule`
- `Externalization boundary`：必须写明样本分母、sport / event / liquidity / runtime epoch，禁止把窄切口正结果外推成 generic 结论
- `Early-stop / split trigger`：必须写明何时 honest close，何时必须拆 Sprint
- `honest negative result` 是合法 close 结果；不得因为没找到正解就无限追加 salvage Pack

### 内容模板

```markdown
### Pack: [短名]

**Pack type**:
- `research_only` / `runtime_translation` / `deploy_gate` / `production_change`

**背景/目标**:
- 要达成的量化结果

**范围边界**:
- 改哪些文件：`src/xxx/yyy.py`
- 不做哪些事：明确排除范围

**生产含义**:
- pass -> production impact
- fail -> kill/freeze impact

**Truth contract / Proxy contract**:
- truth source: `data/reports/...`
- proxy source: `data/...` / runtime payload
- bias / fail-close: xxx

**外推边界**:
- 样本分母 / sport / liquidity / runtime epoch
- 是否允许 mixed-scope 外推

**DoD（完成标准）**:
- [ ] 测试通过：`pytest tests/xxx/test_yyy.py::test_case`
- [ ] 代码审查通过
- [ ] 产物已生成：`data/reports/xxx.json`
- [ ] 性能指标：P95 < 100ms
- [ ] 文档收口（如本 Pack 关闭 Sprint / 收敛长期热点）：`progress.md` / `pitfalls.md` 已摘要归档，archive snapshot 已链接

**Early-stop / split trigger**:
- 何时必须 honest close
- 何时必须拆到新 Sprint

**指令与测试**:
```bash
# 精确到命令
pytest tests/xxx/test_yyy.py::test_case -v

# 必要时覆盖配置
pytest --override-ini="addopts=" tests/xxx/
```

**产物与路径**:
- 日志：`var/logs/xxx.log`
- 报告：`data/reports/xxx.json`
- 配置：`config/xxx.yaml`

**风险/回滚**:
- 已知问题：xxx
- 降级策略：yyy
- 回滚步骤：zzz

**负责人/时间与关联链接**:
- Owner: @user
- ETA: 2025-11-15
- PR: #123
- Commit: abc1234
- 相关日志：[链接]
```

### 链接策略

在 `docs/task/progress.md` 中：
- 仅列"热点标题 + 链接到 Sprint 内的 Pack 锚点"
- 不复制 Pack 内容

## Sprint 准入 / 关闭 / 拆分规范

- 新 Sprint 建议直接从 `docs/sprint/_template.md` 复制起稿；模板内的 checklist 不能替代本节规则，只是落地入口。
- Sprint charter 必须先声明：`research sprint` 还是 `production sprint`
- 开工前必须写清：
  - close 时生产环境会改变什么
  - 若没有生产变更，本 Sprint 的成功定义是什么
  - 哪条 mainline 假设一旦被证伪，就必须停止继续 salvage
- 任何 close-driving 字段，必须先出现在 row-level artifact，再允许进入 summary / md / close verdict
- 任何 rerun / sidecar 如果改变了 `truth source / temporal split / executable cost model / row-level verdict source`，默认视为新 Sprint，而不是旧 Sprint patch
- 每完成 `3-4` 个 Pack，必须追问一次：`Given what we know now, production changes what?`
- 若答案仍是“什么都不改”，则只能：
  - `research close`
  - `split new sprint`
  - 或写清继续推进的显式理由
- 若 mainline 已被 truth contract 证伪，则默认拆 Sprint；禁止把 post-close narrowing / deploy follow-up 无限塞回原 Sprint

示例：
```markdown
## 下一步任务

1. **完成配置管理 API** - 详见 [Sprint 9 Pack: 配置管理](../sprint/sprint9.md#pack-配置管理)
2. **前端页面开发** - 详见 [Sprint 9 Pack: 前端核心功能](../sprint/sprint9.md#pack-前端核心功能)
```

## 质量检查清单

每次提交前检查：

### 代码质量
- [ ] 遵循 PROJECT_RULES.md 所有规则
- [ ] 最小改动原则（Rule 4）
- [ ] 代码风格一致
- [ ] 无安全漏洞（SQL注入、XSS等）
- [ ] 日志已脱敏（不输出敏感信息）

### 测试覆盖
- [ ] 新功能有对应测试
- [ ] 测试覆盖率 ≥ 80%（operations层）
- [ ] 所有测试通过
- [ ] 边界条件已测试

### 文档更新
- [ ] API 文档已更新（如有接口变更）
- [ ] README 已更新（如有新功能）
- [ ] `docs/task/progress.md` 已更新
- [ ] `docs/qa/pitfalls.md` 已更新或已确认本轮无需新增
- [ ] 相关 Sprint 文档已同步
- [ ] Sprint close / Pack close 如触发文档收口，archive snapshot 已落盘并已链接

### 提交规范
- [ ] Commit 信息清晰
- [ ] 变更已分组（不混杂无关改动）
- [ ] 所有修改都在任务范围内

## 常见场景

### 场景1: 实现新功能

1. 阅读 Sprint 文档了解需求
2. 检查 `docs/task/progress.md` 确认优先级
3. 制定实现计划（Ask 阶段）
4. 先写测试用例
5. 实现功能代码
6. 验证测试通过
7. 更新文档
8. 提交变更

### 场景2: 修复 Bug

1. 复现问题（收集错误日志）
2. 定位根因（分析代码）
3. 编写测试用例（复现 bug）
4. 最小修复（遵循 Rule 3/4）
5. 验证修复效果
6. 记录到 progress.md
7. 提交变更

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
- [`docs/task/progress.md`](../task/progress.md) - 当前任务游标
- [`docs/sprint/sprint9.md`](../sprint/sprint9.md) - Sprint 9 完整计划

---

**维护者**: 开发团队
**最后更新**: 2026-03-27

---

## AI 协作强化流程

### 1. Task-tier gating

| Tier | 典型任务 | 强制要求 | 额外 gate |
|------|----------|---------|----------|
| `T0` | 事实查询 / 小解释 / 无代码改动 | 事实驱动 | 不要求 route log |
| `T1` | 单文件、小改动、低 blast radius | Ask→Code、最小验证、完成证据 | bugfix 仍需 pitfalls 收口 |
| `T2` | 跨 `2+` 文件、接口/契约、中等风险 | 8 要素 spec、pitfalls hit、route log、targeted tests | 连续 `2` 轮无新增证据必须触发 failure routing |
| `T3` | runtime / deploy / strategy mainline / core frozen / 高 blast radius | T2 全部 + `truth/proxy` + rollback + rollout metrics + pair/cross review | `GO / ship / merge` 结论必须附强证据 |

**自动升级规则**:
- 命中任一条件自动至少 `T2`：跨 `2+` 模块、字段口径变化、配置/开关语义变化、历史坑位命中、外部 API 契约、bugfix。
- 命中任一条件自动 `T3`：runtime / deploy / manager / pig / live trading / frozen core 文件 / strategy admission / default config drift / 需要 `GO/NO-GO`。
- 如 tier 不确定，默认上调一级，不默认下调。

### 2. 八要素任务 spec（`T2+` 强制）

```markdown
WHY:
- 为什么做；业务意图是什么；不做的成本是什么

WHAT:
- 本轮交付什么；可验证产物是什么

WHERE:
- 允许修改哪些文件 / 模块
- 明确不碰哪些边界

HOW MUCH:
- 预计文件数 / LOC / 时间
- 若超过预期，何时拆 Pack / 降 scope

TRUTH / PROXY:
- truth source:
- proxy source:
- gap / bias / fail-close rule:

PITFALLS HIT:
- active/archive 命中项：
- guardrail：
- 若未命中：`none (keywords=...)`

DONE:
- 测试 / 命令：
- 报告 / 日志 / 产物路径：
- 手动验证：
- 什么状态下才算 `GO`：

DON'T:
- 禁区：
- 非目标：
- 不得顺手重构的内容：
```

规则：
- 8 要素是任务框架，不是诊断框架。
- `TRUTH / PROXY` 与 `PITFALLS HIT` 不允许静默省略；未知时写 `unknown yet`。
- `DONE` 必须精确到命令、断言、状态输出、artifact 路径或 review oracle。

### 3. 系统性 5 步法与冰山法则（`T2/T3` 调试、review、设计审查强制）

1. 读信号：先写 `observation`，不先下 `root cause`。
2. 多角度搜索：grep 同类 pattern、读已有测试、读项目合同、读相关文档。
3. 读源码上下文：至少读命中点上下各 `50` 行；必要时追 `caller/callee` 各 `1` 跳。
4. 验证假设：用测试、日志、assert、report、runtime check 或 source contract 证明或证伪。
5. 反转假设：主动问"如果我的判断是错的，最强替代解释是什么？"

**冰山法则**:
- bugfix 不止修命中点；还要 grep 同类 pattern。
- grep 后必须明确选择其一：
  - `fix-now`
  - `record-as-pack`
  - `not same root cause`
- "没时间看同类面"不是关闭任务的理由；只能变成显式风险或拆分决策。

### 4. Failure-mode routing（`session-level`、`evidence-driven`、`bidirectional`）

触发基线：
- 连续 `2` 轮没有新增证据，只是在改参数、改措辞或重复同一搜索
- 声称完成但无对应完成证据
- 把猜测写成 `root cause` / `environment issue` / `already covered`
- 只看签名或局部片段，未读足够上下文
- 修完即停，未做冰山扫描或上下游影响判断
- review findings 越堆越多，但没有按根因收口

| 失败信号 | 必须切换到的 route | 最小动作 | 退出条件 |
|---------|-----------------|---------|--------|
| `spinning` 原地打转 | `scope-simplify + reverse-hypothesis` | 重写问题陈述，删去非必要变量，提出一个更小验证 | 产生新证据或明确 split/defer |
| `fake_done` 假完成 | `completion-proof` | 补命令、日志、测试、报告路径；补不出则降级状态 | 补齐合格证据 |
| `blame_shift` 推锅 | `hypothesis-verification` | 把"环境问题"改写成可验证假设并运行检查 | 得到证实或被证伪 |
| `no_search` 没搜就猜 | `search-first` | grep 同类 pattern、读官方文档/项目契约、读已有测试 | 形成带引用的判断 |
| `low_context` 上下文不足 | `context-50-lines` | 读命中点上下各 `50` 行、caller/callee 各 `1` 跳 | 结论可解释调用图 |
| `passive_stop` 被动等待 | `iceberg-scan` | grep 同类 pattern、检查上下游影响、决定 `fix-now / pack / pitfall` | 同类面已处理或已登记 |
| `finding_pileup` findings 不收口 | `root-cause-consolidation` | 按根因去重、保留最高严重度、转成可执行清单 | findings 可行动、可验收 |

**触发权**:
- CC 和 Codex 都可触发。
- 触发必须写"当前 session 出现了什么证据"，不能写"对方是什么人/什么模型"。

### 5. Anti-rationalization protocol（双向适用）

| 说法 | 必须追问 | 若答不上来 |
|------|---------|-----------|
| "可能是环境问题" | 哪个命令 / 日志 / env diff 支持？ | 降级为 `hypothesis` |
| "应该没问题" | 哪个测试 / 断言 / 状态输出支持？ | 不算验证 |
| "这个已有覆盖" | 精确到测试文件和断言是什么？ | 按缺口处理 |
| "我读过了" | 读了哪 `50` 行上下文？caller / callee 是什么？ | 视为上下文不足 |
| "只是小改动不用升 tier" | blast radius / contract drift 证据是什么？ | 按 higher tier 处理 |
| "先 merge 再看" | rollback、monitor、stop condition 在哪？ | 不得给 `GO` |
| "没时间查同类问题" | 冰山扫描结果在哪？至少 grep 了吗？ | 记录风险或拆 Pack |
| "外部模型说得对/不对" | 读过源码哪几行？ | 不得 `adopt / reject` |
| "这个 finding 太理论了" | 哪个 source / test / runtime 证据说明它不会发生？ | 降级但不直接驳回 |
| "这个不用看上下文" | 为什么这段逻辑不依赖 caller / callee / contract？ | 先补上下文再讨论 |

### 6. Route logging（何时记、记到哪里）

**即时日志模板**:
```markdown
route_log:
- task: <short name>
- tier: T1/T2/T3
- observed_in: CC / Codex / shared session
- trigger: <spinning / fake_done / blame_shift / no_search / low_context / passive_stop / finding_pileup>
- evidence: <具体缺失证据 / 重复行为 / 命令输出摘要>
- route_before: <old route>
- route_after: <new route>
- exit_condition: <什么证据出现后退出>
```

**落地规则**:
- 每次 route 切换先记即时日志。
- 仅当 route change 影响计划、消耗 `2+` loops、触发 split/defer、或暴露可复用根因时，才写入 `docs/task/progress.md`。
- 如果 route change 暴露了稳定根因或 guardrail，收口到 `docs/qa/pitfalls.md` / archive。

### 7. 完成证据分类

| Task kind | 最小完成证据 | 不满足时允许的状态 |
|-----------|--------------|-------------------|
| `code_change` | changed files + targeted `pytest` / command + 输出摘要 | `implemented but unverified` |
| `bugfix` | failing signal(before) + passing signal(after) + pitfalls 更新或链接 | `hypothesis fix` |
| `research/backtest` | command、`run_id/data_cut_id`、artifact path、sample scope、`truth/proxy` 说明 | `research prior` |
| `review/design_review` | findings with `file:line` / `doc:line`、severity、verdict、open risks | `draft review` |
| `deploy/runtime` | `status/health/log grep/state output`、绝对日期时间、rollback handle | `needs runtime validation` |
| `docs/process` | changed doc path + `python -m scripts.docs.check_doc_cursors` 输出或跳过理由 | `docs updated, not cursor-checked` |

补充规则：
- 研究证据不能直接当 runtime 证据。
- proxy 改善不能直接写成 production 改善。
- 没有 before/after 的 bugfix，不得写"root cause fixed"。
- 没有 rollout guardrail 的 deploy/runtime 变更，不得写"safe to ship"。

### 8. Method rollout metrics（试点期）

| Metric | Definition | Target / Alarm | Recording place |
|--------|------------|----------------|-----------------|
| `false_done_rate` | 无合格证据却宣称完成的任务数 / closed tasks | target `< 5%`；alarm `> 10%` | Sprint 周报 / close |
| `reopen_rate_72h` | `72h` 内因漏检重开的任务 / closed tasks | 趋势下降 | Sprint 周报 / close |
| `route_trigger_rate` | 触发 failure routing 的 `T2/T3` 任务占比 | 观察项，不追求 `0` | Sprint 周报 |
| `route_recovery_rate` | 触发路由后无需人工重写 spec 即闭环的任务占比 | target `> 60%` | Sprint 周报 |
| `pitfall_rehit_rate_14d` | `14` 天内命中已知 ACTIVE 根因的次数 / bugfix tasks | 趋势下降 | pitfalls close / Sprint close |
| `independent_disagreement_yield` | CC↔Codex 实质性分歧且改变方案的次数 / pair sessions | target `> 0`；长期为 `0` 视为退化 | Sprint close |
| `ship_escape_rate` | merge / deploy 后仍逃逸的 `P1+` 问题数 / shipped changes | target `0` | Sprint close |

解释规则：
- `route_trigger_rate` 高不等于失败；若 `route_recovery_rate` 同时高，说明路由在起作用。
- `independent_disagreement_yield` 长期为 `0` 通常不是好事，说明 pair 退化成单向盖章。
- rollout metrics 只用于校准方法，不用于压制 honest negative result。

### 9. 文档落地边界

- `AGENTS.md`：高层原则、红线、角色边界、tier 摘要。
- `docs/review/ai-workflow.md`：具体操作细则、模板、路由表、证据分类、指标。
- `docs/task/progress.md`：当前任务的 route change / 阻塞 / 下一步 / close evidence link。
- `docs/qa/pitfalls.md`：稳定复发模式、guardrail、canonical RCA link。
- `docs/sprint/sprintN.md`：task-specific 例外、pilot 范围、rollout decision、production implication。

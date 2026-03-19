# Sprint N: <标题>

## 背景与目标

- 为什么要做这个 Sprint
- 要达成的量化目标

## 非目标（不做什么）

- 明确排除的范围

## 前置条件

- 依赖的上游 Sprint 或外部条件

## Pack 列表

### Pack: <Pack 1 短名>

**背景/目标**:
- 要达成的量化结果

**范围边界**:
- 改哪些文件
- 不做哪些事

**DoD（完成标准）**:
- [ ] 测试通过：`pytest tests/xxx/test_yyy.py::test_case`
- [ ] 代码审查通过
- [ ] 文档收口

**指令与测试**:
```bash
pytest tests/xxx/test_yyy.py::test_case -v
```

**产物与路径**:
- 报告：`data/reports/xxx.json`

**风险/回滚**:
- 已知问题：
- 降级策略：

**负责人/时间**:
- Owner: @user
- ETA: YYYY-MM-DD

---

### Pack: <Pack 2 短名>

（按相同模板填写）

## Sprint Close 条件

- [ ] 所有 Pack DoD 满足
- [ ] `docs/task/progress.md` 已更新
- [ ] `docs/qa/pitfalls.md` 收口（新增/更新/归档）
- [ ] 测试全绿

## 风险与回滚

- 整体风险评估
- 回滚策略

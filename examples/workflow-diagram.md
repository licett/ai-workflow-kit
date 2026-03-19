# Workflow Diagram

## 完整开发循环

```
Sprint 设计
    │
    ▼
/sprint-design-reviewer  ◄── 专家面板评审设计文档
    │
    ├── Approve → 开工
    ├── Conditional → 修补后开工
    └── Reject → 重新设计
    │
    ▼
编码前避坑检索  ◄── 强制：查 pitfalls.md + pitfalls_archive/
    │
    ▼
Ask 阶段（计划草稿）
    │
    ▼
/tdd-loop-executor  ◄── RED → GREEN → REFACTOR 循环
    │
    ├── 每轮更新 progress.md
    ├── bugfix 必须更新 pitfalls.md
    └── continue → 从 progress.md 下一步继续
    │
    ▼
/cross-review-gate  ◄── 4 专家交叉 review + 质量门禁
    │
    ├── Pass → 可提交
    ├── Conditional Pass → 修复后提交
    └── Fail → 修复 P0/P1 后重跑
    │
    ▼
提交 & 文档收口
    │
    ├── progress.md 精简（≤ 100 行）
    ├── pitfalls.md 收口（≤ 250 行）
    └── 旧内容归档到 archive/
    │
    ▼
/sprint-close-auditor  ◄── 对账代码/测试/文档
    │
    ├── Complete → Sprint 关闭
    ├── Partial → 剩余任务进入下个 Sprint
    └── Blocked → 解除阻塞
```

## 日常快速循环（不建 Sprint 的小改动）

```
查 pitfalls.md → Ask 计划 → TDD 写代码 → /code-review-expert → 提交
```

## 外部模型建议验证

```
GPT/Gemini 给出 review 建议
    │
    ▼
/adversarial-cross-model-review
    │
    ├── Adopt → 执行修复
    ├── Partial adopt → 调整后执行
    ├── Reject → 忽略
    └── Defer → 需要运行时验证
```

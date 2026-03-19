摘要：活跃坑位索引（完整 RCA 与历史快照见 `docs/qa/pitfalls_archive/`）。
# Pitfalls
## 写入规则

- `pitfalls.md` 只保留会影响当前编码判断的 ACTIVE 卡片，不再保存长篇事故流水账。
- Bugfix 回合优先更新同根因的现有 ACTIVE 卡片；只有新根因才新增卡片。
- 同根因复发时，更新 `Last seen`、`Rule`、`Guardrail`、`Canonical detail`，不要再追加重复 section。
- 完整 RCA 写入 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md` 或对应 Sprint close 文档，再把路径回链到 ACTIVE 卡片。
- ACTIVE 卡片必填字段：`Scope`、`Search keywords`、`Rule`、`Guardrail`、`Last seen`、`Canonical detail`、`Archive when`。
- 严禁敏感信息：不要写账号/密码/cookie/token。

## 活跃游标与归档规则

- `pitfalls.md` 的目标是"活跃坑位索引"，不是长期账本。
- 主文件预算：
  - 总长度目标 `<= 250` 行；
  - ACTIVE 卡片 `<= 10` 张。
- 必须执行归档的触发条件（满足任一条即执行）：
  - Sprint close / 长周期 Pack close；
  - 主文件超过 `250` 行；
  - ACTIVE 卡片超过 `10` 张；
  - 同根因出现了重复卡片，或主文件已经影响编码前检索效率。

## ACTIVE 卡片模板

```markdown
### ACTIVE YYYY-MM-DD <标题>
- Scope: `path/to/file.py`
- Search keywords: `keyword-a`, `keyword-b`
- Rule: 未来编码必须守住的约束/不变量
- Guardrail: `tests/...` 或 close gate
- Last seen: `YYYY-MM-DD`
- Canonical detail: `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md`
- Archive when: 连续 2 个 Sprint close 未命中，且无新证据
```

## 活跃坑位索引

（项目初始化，暂无活跃坑位。首次 bugfix 后在此新增 ACTIVE 卡片。）

## 活跃坑位卡片

（暂无。）

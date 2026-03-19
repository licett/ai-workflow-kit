# Pitfalls Archive

完整 RCA（Root Cause Analysis）归档目录。

## 命名规范

`YYYY-MM-DD[-suffix].md`

例如：
- `2026-01-15-api-timeout-retry.md`
- `2026-02-03-schema-enum-case-mismatch.md`

## 内容要求

每份归档文档应包含：
1. **事故概要**：什么时候、什么现象
2. **根因分析**：为什么发生，代码路径
3. **修复措施**：改了什么
4. **防回归**：加了什么测试/门禁
5. **关联链接**：对应的 pitfalls ACTIVE 卡片、Sprint、commit

## 生命周期

- 活跃坑位卡片 (`docs/qa/pitfalls.md`) 通过 `Canonical detail` 字段链接到本目录的归档文件。
- 当 ACTIVE 卡片被归档（连续 2 个 Sprint close 未命中），只从主文件移除卡片，归档文件保留。

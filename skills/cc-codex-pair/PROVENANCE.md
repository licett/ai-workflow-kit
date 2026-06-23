# PROVENANCE — vendored Codex 通信层

本目录 `scripts/`、`skills-ref/gpt-5-4-prompting/`、`LICENSE`、`NOTICE` 为**一次性冻结拷贝**，
来自 OpenAI 官方 `codex-plugin-cc`，仅取其通信层供本 skill 驱动 Codex。

## 来源
- 仓库: https://github.com/openai/codex-plugin-cc
- 许可: Apache-2.0（见 LICENSE / NOTICE，已随拷贝保留）
- 上游 commit: `807e03ac9d5aa23bc395fdec8c3767500a86b3cf`
- 拷贝日期: 2026-06-14

## 拷贝清单（来自上游 plugins/codex/）
- `scripts/codex-companion.mjs` — 入口 CLI（task/status/result/cancel/setup/review）
- `scripts/app-server-broker.mjs` — broker 进程入口（被 lib spawn）
- `scripts/lib/*.mjs` — app-server JSON-RPC 客户端 + broker 生命周期 + job-control + state
- `scripts/session-lifecycle-hook.mjs`、`scripts/stop-review-gate-hook.mjs` — 备用（hook，本期未启用）
- `skills-ref/gpt-5-4-prompting/` — 提示块库（被 SKILL.md 引用，未改动）
- `.claude-plugin/plugin.json` — **必需**：`lib/app-server.mjs:19` 读它取 version 作为 app-server clientInfo；缺失会 ENOENT。重拷时勿漏。

## 验证可用基线
- 实测环境: node v24.13.0, codex-cli **0.139.0**, ~/.codex/auth.json 已登录
- 2026-06-14 实测: `task --fresh` → `task --resume-last` 续同一 thread-id、跨轮记忆正确、每轮 5–8s

## ⚠️ 失效与更新策略（一次拷贝方案）
- 本拷贝**冻结不动**，不做 fork 跟踪 / sync。
- 唯一真实风险: 底层 `codex` CLI 自升级后若对 app-server 协议做**破坏性变更**，本拷贝即使一行未改也可能失效。
- 缓解: 出问题时**重新从上游拷一份匹配新 codex 版本的同套文件**，更新本文件的 commit 与 codex-cli 版本，而非 debug。
- 本地未改动上游文件；如将来必须本地补丁，须在此登记 patch 清单以便重拷时复用。

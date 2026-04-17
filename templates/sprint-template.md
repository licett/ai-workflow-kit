# Sprint N — <标题>

更新时间：YYYY-MM-DD
状态：`DESIGN` / `ACTIVE` / `CLOSED`
Owner：@user
Sprint type：`engineering sprint` / `research sprint` / `production sprint`

---

## 0. Sprint charter

- Sprint type：`research` / `engineering` / `production`
- Close 时生产环境会改变什么：
  - If pass：{具体变更}
  - If fail：{冻结/降级/kill}
- 若没有生产变更，本 Sprint 的成功定义是什么：{research close 口径}
- Mainline hypothesis：{核心假设}
- Mainline stop condition：{假设被证伪的条件 → 必须停止}

---

## 1. Pack 列表

### Pack: <Pack 短名>

- Pack type：`research_only` / `runtime_translation` / `deploy_gate` / `production_change`
- 状态：**TODO** / **DONE**
- pass → production impact：{如果通过，生产改什么}
- fail → kill/freeze impact：{如果失败，kill/freeze 什么}

#### 目标
- 要达成的量化结果

#### 范围边界
- 改哪些文件 / 不做哪些事

#### Truth / Proxy contract
- truth source：{真实核验口径}
- proxy source：{代理口径}
- gap / bias / failure mode：{两者差距}

#### DoD
- [ ] {具体可验证条件}
- [ ] 测试通过：`pytest tests/...`
- [ ] 文档收口

#### 指令与测试
```bash
python3 -m pytest tests/... -v
```

#### 产物与路径
- `data/reports/...`

#### 风险/回滚
- 已知问题：
- 降级策略：

#### 负责人/时间
- Owner: @user
- ETA: YYYY-MM-DD

---

### Pack: <Pack 2 短名>

（按相同模板填写）

---

## 2. Early-stop / split trigger

- 每完成 3-4 个 Pack，回答：`Given what we know now, production changes what?`
- 若答案是"什么都不改"，必须选择：`research close` / `split new sprint` / `continue with reason`
- 若 mainline 已被 truth contract 证伪 → 默认 `split new sprint`

---

## 3. Close checklist

- [ ] 所有 Pack DoD 满足（或 honest_negative close）
- [ ] `docs/task/progress.md` 已更新
- [ ] `docs/qa/pitfalls.md` 收口（新增/更新/归档）
- [ ] 测试全绿
- [ ] Sprint type 一致性：research sprint 不能暗示"快可上线"

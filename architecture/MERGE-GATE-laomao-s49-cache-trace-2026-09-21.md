# MERGE_WITH_CONDITIONS

engine=grok-4.6 xhigh

> 审 OpenClaw `fix/laomao-s49-cache-merge-and-trace-gates` @ `44ff3fe`（基线 `247934e`）是否合入主线。
> 范围：kline cache 按 `open_time` 合并；probe 新鲜度 + 五字段 trace + `no_structure` 提示。
> 仓库：`github.com/licett/laomao`（Jimmy: github remote；origin 仍是 Gitee）。本文件写在 `licett/ai-workflow-kit`，只新增本文，不改 laomao 代码。
> 对照：uploads 中 `REQUEST` / `patches` / `backtest*.py` / `laomao_probe*.py`，以及 GitHub `44ff3fe` 全文 patch、`247934e`、`720c605a`、S49 测试与 `raw_market_scoring.py`。uploads 与 GitHub patch 一致。

---

## 0. 总判

**MERGE_WITH_CONDITIONS。** 缓存合并是对症小修，可以合；probe 闸门是展示层增量，**还不是 fail-closed**。两条线必须分开：合入 **cyberbrain 引擎线**（真实基线 `247934e`），**禁止**合入 GitHub default `main` @ `720c605a`。

| 问 | 答 |
|---|---|
| 缓存按 `open_time` 合并该不该合？ | **该合**（引擎线）。对上了 S49「刷新缩短历史 → `KeyError`」这个根因 |
| probe 新鲜度 + 五字段 + `no_structure` 该不该合？ | **可以随包合**，但只能当「警告/缺字段 raise」，**不得记成 fail-closed 完成** |
| 动没动 S49 truth-channel 冻结面？ | **没动预测/打分/分母**。只动了 cache **写路径**和 probe **渲染** |
| 合到哪条线？ | Gitee `origin` / Jimmy 本机 cyberbrain，基线 `247934e`。**不是** GitHub `laomao#main` |
| 声称的 `tests/test_sprint49_raw_market.py` 18/18？ | 必要，但不充分：那 18 个用例**不覆盖**新 merge / `validate_trace` 路径 |

推翻本总判：

- 若目标被说成「合进 GitHub `main` @ `720c605a`」→ 改为 **REJECT**（无共同祖先，蒸馏仓会被引擎树压碎）。
- 若本轮验收硬要求「probe fail-closed 已完成」→ 改为 **REWORK**（stale 仍渲染；`channel_outcome="—"` 能过闸；`DailyRunner` 未接线）。
- 若 `44ff3fe` 之外还改了 `state_machine.py` / `raw_market_scoring.py` / S48 分母 → 改为 **REWORK**，先重审冻结面。

---

## 1. 审了什么

| 证据 | 内容 |
|---|---|
| 提交 | `44ff3fe` *fix(laomao): cache merge on refresh + probe trace gates*（+52/−2，两文件） |
| 父提交 | `247934e` *housekeeping: track sprint43-49 tests*（2026-09-08） |
| GitHub `main` | 仅一提交 `720c605a` *init: laomao distillation repo…*（2026-09-20）。与引擎史**无共同祖先** |
| 分支 | `fix/laomao-s49-cache-merge-and-trace-gates` = 引擎全树 + 本修复；`main` = 蒸馏快照仓 |
| 冻结合同 | `docs/sprint/sprint49.md`；`raw_market_scoring.py`（`_FROZEN_DENOMINATOR_SHA256`、253 行、`by_date[date]`） |
| S43 先例 | `validate_kline_cache_envelope` 读路径 fail-closed；`test_s43_fetch_cache_rejects_missing_generated_at` |
| 日更接线 | `runner/daily.py` **不** import `laomao_probe`；`laomao_runtime.py` 是另一条 S36 结构路径 |

---

## 2. 改动面（两处，故意窄）

### 2.1 `fetch_binance_daily_candles` 写缓存

刷新成功且 `cache_path` 存在时：按 `symbol`+`interval` 读旧 `rows`，`open_time`（`row[0]`）为键并入 dict，新行覆盖同刻，再 `sorted` 写回。读路径、`days` 切片返回值、`run_historical_backtest` 本体**未改**。

### 2.2 `laomao_probe`

- `LaomaoDailyState.stale`；`date_str` vs `datetime.now().astimezone()` 的本地日。
- `TRACE_FIELDS` 五元组 + `validate_trace()`；`render_laomao_section` 渲染前调用。
- stale 警告；`structure == "no_structure"` 且 `position_fraction == "1.0"` 时加「仓位依据纯趋势/通道」。

未改：`state_machine.py`、`raw_market_scoring.py`、S48/S49 产物、分母 253、`DailyRunner`、cron/交易开关。

---

## 3. 正确性与失败模式

### 3.1 缓存合并 — 对症，有残留坑

**根因（成立）。** S49 打分：

```python
generated = by_date[date]   # raw_market_scoring.build_raw_market_score
```

253 个 explicit 日（从约 `2023-03-30` 起）任一日期不在 cache → `KeyError`。提交说明：滑动窗整文件覆盖丢掉 11 个早行 → 约 10 个用例挂。这与「写路径用本次 `all_rows` 覆盖、读路径却直接读整文件」一致。

`generated_at` 超 90 天时 S43 读路径会拒缓存并重拉。默认 `days=500`（再加 50 根 warmup）重拉后整文件只剩 ~550 根，早段会大量消失，不只 11 根。11 根是「窗几乎盖住历史、起点偏了几天」的特例；**整文件覆盖会缩短历史** 才是类缺陷。按 `open_time` 合并修的是这个类。

**新行覆盖同刻 — 对。** 未收盘日 K 线应被现场值替换。

**失败模式（合入后仍在，不挡引擎线合入）：**

| ID | 模式 | 严重度 | 说明 |
|---|---|---|---|
| F1 | 合并后中间有洞 | P1 | 旧缓存止于 2024、本次只拉近 550 根 → 中间空洞。写路径**不**跑 `_daily_rows_are_contiguous`。下次读：integrity 失败 → 再拉 → 再把有洞的旧行合进去。S49 **直接读文件**，会带着洞跑；backtest 遇洞会清 Markov prior，**预测身份会漂** |
| F2 | 返回值仍是滑动窗 | P2 | 写的是 `merged_rows`，返回仍是 `all_rows[-days:]`。S49/probe 读文件，所以这次能修好。谁若改成用函数返回值当 S49 输入，早段会再丢 |
| F3 | `int(row[0])` 的 `ValueError` 未接 | P2 | except 只有 `JSONDecodeError, KeyError, TypeError`。脏 `open_time` 会在**已经拉到数之后**把写缓存打爆 |
| F4 | 旧行 schema 未校验 | P3 | 只看 `symbol`/`interval` 和 `len>=7`，不看 `schema_version`。脏历史会留下 |
| F5 | `generated_at` 被刷成现在 | — | 信封变新、早行仍是旧快照。这正是 S43「年龄=上次刷新」的语义，**要的** |

F1 的现实前提是「很旧的短缓存 + 短窗刷新」。当前 S49 工作缓存若已从 `2023-03-30` 连到近期，一次重叠刷新合完仍连续。这是**要防的未来坑**，不是这次 11 行 bug 的阻断点。

### 3.2 Probe — 方向对，合同写过了

**新鲜度。** 提交写「hard check」，实现是：标 `stale`、打 warning、**照样返回 state、照样渲染**（多一行警告）。这是 fail-open 展示，不是拒发。

**时区。** 蜡烛日来自 `_date_from_open_time_ms`（**UTC** 开盘日）。「今天」用**本地** `astimezone()`。Binance 1d 开在 00:00 UTC = 上海 08:00。上海 `00:00–08:00` 会把「昨天 UTC K 线」判 stale。S37 cron 是上海 08:15 / 20:15，落在安全窗。其它调用方会误报滞后。

**五字段闸。** `validate_trace` 用 `not trace.get(k)`：缺/空则 `LaomaoTraceError`。`position_fraction_hint` 给的是字符串 `"0"` / `"1.0"` / `"partial"` / `"unknown"`，`"0"` 为真，现金仓不会误杀。

但探测侧缺通道时写成 `"—"`（U+2014），占位符为真，**缺通道能过闸**。结构缺省是 `"no_structure"`，这个字段几乎不会触发 missing。闸门实际只能抓住空 `date` / 空 `generated_state` / 空 `position_fraction`。

**`no_structure` 提示。** 只在 `structure == "no_structure"` 且 `position_fraction == "1.0"`。`_structure_family` 的「无结构」就是这个串；满仓 hint 就是 `"1.0"`。命中「看起来满仓、当日无结构」。probe 用的是**当日 raw family**，不是 S49 的 109 日 carry，提示会比打分更保守。预存差异，可接受。

**谁接这个 raise？** 仓内 `DailyRunner._probe_all` 不调 `laomao_probe`。`LaomaoTraceError` 目前是**库合同**。外接 OpenClaw 若未包 try，轻则丢一节、重则整份 brief 挂；包了又当普通异常吞掉，则变成 fail-open。仓内看不到接线，**不能把本提交当成生产 fail-closed**。

---

## 4. S49

S49 已关闭的合同（`sprint49.md` + `test_sprint49_raw_market.py`）：

- 冻结 explicit 分母 **恰好 253**；`denominator_identity` SHA 钉死。
- 预测只许用行情；oracle/source/`structure_intent` 只能事后打分。
- 有效仓位语义 ≥228/253；source-replay 94.07% **不能**当完成。
- `runtime_enablement=false`，`trade_instruction_enabled=false`。
- 禁止按日期改 `state_machine` / `raw_market_scoring`。

本修复与 S49 的关系：

| 面 | 判定 |
|---|---|
| 分母 253 / SHA | **未碰**（没改 S48 行、没改 `denominator_row`） |
| 预测路径 | **未碰**（`raw_market_only` 分支、state machine、指标未改） |
| 反泄漏 | **未碰** |
| 运行时使能 | **未打开**。probe 警告不是开 cron/下单 |
| cache 作为预测输入 | **写路径更保守**：刷新不再抹掉分母需要的早段。重叠日仍可能被现场 K 线覆盖（刷新本来就会，不是新口子） |
| 18/18 | 证明**当前工作树里的 cache 文件**仍能对上 253 个日期。**不**证明 merge 在「短窗刷新」下能保住早段，也**不**证明 `validate_trace` |

S49 要的修复就是：别再让刷新把 `2023-03-30+` 从 `var/laomao/s42/binance_btcusdt_1d_full.json` 里裁掉。合并写路径对准这件事。合入后应用**现有** cache 跑 18/18；不要先跑一遍未合并的旧 fetch。

---

## 5. Probe fail-closed（本提交未达到）

仓内已有的 fail-closed 先例：S43 缓存信封（缺 `generated_at` / 不连续 / 过期 → 拒）；`DailyRunner` 质量门失败不落正式稿；S36 runtime 数据旧则 `degraded`/`blocked`。

本提交对照：

| 事件 | 现行为 | fail-closed 该怎样 |
|---|---|---|
| cache/backtest 挂了 | `probe_laomao_daily` → `None`（原有） | 已是 |
| 数据日 ≠ 本地今天 | 警告 + **照发** | 不渲染 / 返回 `None` / 让调用方降级 |
| 五字段缺/空 | `render` raise | 可以，但调用方必须把异常变成「整节省略」，且不能让整份 brief 崩 |
| 通道其实没有 | `"—"` **过闸** | 拒，或把占位符当成空 |
| `DailyRunner` | **没接线** | 正式日更仍走别的源 |

**结论：** 这是「能标 stale、缺真字段会炸 render」的半截闸。合入条件 C2：文档和收口**不许**写「probe fail-closed 已完成」。要那块验收，另开 REWORK：stale 拒发、占位符当空、单测、接到一个不会误伤整份 brief 的调用方。

---

## 6. Truth-channel 冻结面

S49 的 truth-channel 不是 tgscraper raw-truth，而是这条链：

**冻结标签（S48 explicit 253）→ 只作打分；预测只用 cache K 线 + 市场派生指标 + 市场生命周期；`prediction_row_identity` 与 `denominator_identity` 分串。**

| 冻结物 | 本提交 | 判定 |
|---|---|---|
| `denominator_identity` / SHA `81ce7e9e…4566` | 未改 | 冻住 |
| `expected_state` / 结构标签 | 未改 | 冻住 |
| `state_machine.py` 日期表 | 未改；原有「无日期字面量」测试仍适用 | 冻住 |
| `raw_market_scoring.py` 语义与 carry | 未改 | 冻住 |
| `run_historical_backtest` 推理 | 未改 | 冻住 |
| `var/laomao/s48/backtest_results.json` | 未改 | 冻住 |
| `var/laomao/s42/binance_btcusdt_1d_full.json` **文件格式** | 仍是 `cyberbrain.binance_kline_fixture.v1` | 冻住 |
| 该 cache 的**行集合** | 刷新时早段可保留、重叠日可被现场值盖住 | **写路径相邻，预测合同未改** |
| probe 展示 | 新增警告/闸 | **不在冻结面上**（展示 ≠ 打分） |

**冻结面结论：未破。** 预测与分母身份仍只被「K 线是否还覆盖 253 日、重叠日 OHLC 是否被刷新改掉」影响——这是 cache 工作文件的旧合同。合并降低「丢日」风险，不引入按日特判，不把 source 灌进预测。

合入后禁止顺手改：`raw_market_scoring.py`、`state_machine.py`、S48 行、`_FROZEN_DENOMINATOR_SHA256`、`predictor_input_mode` 语义。那些是下一场 T3，不是这个小修复。

---

## 7. 合入步骤（合到哪条线）

### 7.1 两条无关历史（P0）

```
GitHub licett/laomao
├── main                    720c605a   蒸馏仓（data/ + pipeline + human gate）
└── fix/laomao-s49-…        44ff3fe    cyberbrain 引擎全树（父 247934e）
         ▲
         └── 与 720c605a 无共同祖先

Gitee origin / Jimmy 本机 cyberbrain
└── （引擎线 tip ≈ 247934e）  ← 唯一合法合入点
```

GitHub `README` 写明：本仓是蒸馏快照，下游代码在 cyberbrain，`data/` 只读。把 `44ff3fe` merge 进 `main` 会：无关历史合并、Python 单体压到数据仓、human-gate 快照叙事被破坏。

Jimmy 的 github remote 可以**继续挂着**这条 fix 分支当镜像；**不能**把它当 default `main` 的 PR 合进去。

### 7.2 合法合入（引擎线）

在 **Gitee origin / 本机 cyberbrain**（不要在蒸馏 `main` 上）：

1. `git fetch` Gitee；确认工作树基线是 `247934e`（或其后、且不含本修复的引擎 tip）。若 Gitee 已超 `247934e`，只 **cherry-pick `44ff3fe`**，禁止把 GitHub `main` 扯进来。
2. 快检 diff：只有  
   `src/cyberbrain/laomao/backtest.py`  
   `src/cyberbrain/sources/laomao_probe.py`  
   且 `run_historical_backtest` / `raw_market_scoring` / `state_machine` 无改。
3. **先不要**用短 `days` 刷新去覆盖 `var/laomao/s42/binance_btcusdt_1d_full.json`。
4. `python3 -m pytest tests/test_sprint49_raw_market.py -q` → 18 passed。  
   有余力再跑 S43 缓存用例（`test_s43_fetch_cache_rejects_missing_generated_at` 等）。
5. 推 Gitee 引擎线。GitHub 蒸馏 `main` 不动。
6. 收口用语：合入的是「cache 刷新保历史 + probe 展示警告」。**不要**写 fail-closed 完成、不要重开 S49、不要改 253。

### 7.3 明确不要做的

- `gh pr` 以 GitHub `main` 为 base 合 `44ff3fe`。
- `git merge --allow-unrelated-histories` 把引擎树并进蒸馏仓。
- 用本修复当借口重跑现场 fetch 来「更新」S49 证据（重叠日一变，`prediction_row_identity` 就会漂）。
- 把 `laomao_probe` 接到 `DailyRunner` 却不包 `LaomaoTraceError`（会把质量门从源失败变成未捕获异常）。

---

## 8. 条件清单

必须满足，否则总判作废：

| ID | 条件 | 级别 |
|---|---|---|
| C0 | 只合入引擎线 @ `247934e`（或 cherry-pick 到其后的 Gitee tip）。**禁止**合入 GitHub `main` @ `720c605a` | P0 阻断 |
| C1 | 合入 diff 仍只有上述两文件；冻结面文件零改动 | P0 阻断 |
| C2 | 收口/PR/进度**不得**把 `44ff3fe` 写成 probe fail-closed 完成 | P0 表述 |
| C3 | 引擎工作树、现有 S49 cache 上 `test_sprint49_raw_market.py` 18/18 | P0 验证 |

建议下一刀（不挡本次合入）：

| ID | 后续 | 级别 |
|---|---|---|
| F1 | 写入前跑 `_daily_rows_are_contiguous`；不连续就拒绝合并旧行或拒绝落盘 | P1 |
| T1 | 单测：短窗刷新后文件仍含更早的 `open_time` | P1 |
| T2 | 单测：`validate_trace` 缺字段 raise；`"—"` 若要当 fail-closed 应失败 | P1 |
| P1 | stale → 不渲染或 `None`；通道占位符当空 | P1（要 fail-closed 才做） |
| P2 | 新鲜度用 UTC 开盘日，或写死上海 08:00 以后才比「今日」 | P2 |
| P2 | except 加上 `ValueError`；或跳过脏行 | P2 |
| P3 | 文档写清：S49 必须读 cache **文件**，不要用 fetch 返回值 | P3 |

---

## 9. Findings

- [P0][0.95] 合入目标是引擎线 `247934e`，不是 GitHub `main` `720c605a` — SCM
  影响: 合错线等于用无关历史毁掉蒸馏仓
  取舍: 保留双 remote（Jimmy github 镜像 / Gitee origin），放弃「一个 GitHub default 分支当唯一主线」
  建议: §7.2；GitHub 上这个 fix 只作展示分支

- [P1][0.9] 提交把 stale 写成 hard check，实现是警告后照发 — `laomao_probe.py`
  影响: 验收若按 fail-closed，会误关
  取舍: 先诚实展示，完整拒发留到接线 DailyRunner 时
  建议: C2；要关门就走 REWORK（P1 行）

- [P1][0.85] 合并不保证连续，S49 读文件会吃空洞 — `backtest.py` 写路径
  影响: 旧短缓存 + 短窗刷新 → 洞 → prior 被清 → 预测身份漂（F1）
  取舍: 先修「缩短」，「拒绝不连续合并」留后续
  建议: 当前 S49 缓存已连续则可合；补连续校验

- [P1][0.8] 18/18 不覆盖新代码路径 — `tests/test_sprint49_raw_market.py`
  影响: merge / `validate_trace` 回归无钉
  取舍: 用现网 cache 当烟雾测试，换真正单测
  建议: T1/T2 快跟

- [P2][0.85] UTC 日 vs 本地日 — `laomao_probe.py`
  影响: 上海 08:00 前误报滞后；cron 08:15/20:15 没事
  建议: 比 UTC，或文档写死窗口

- [P2][0.8] `"—"` 能过五字段闸 — `laomao_probe.py`
  影响: 「五字段机器闸」名过实缺
  建议: 占位符当空，或从必填里拿掉通道直到有真值

- [P2][0.7] fetch 返回值仍是窗，文件才是全集 — `backtest.py`
  影响: 调用约定陷阱（F2）
  建议: 注释或 S49 继续只读文件

- [P3][0.6] `int(row[0])` 的 `ValueError` 未接 — `backtest.py`
  影响: 脏缓存让成功拉取也写不进去
  建议: 跳过脏行或并入 except

---

## 10. 一句话给 Jimmy

**可以合，合 Gitee/本机引擎线，不要合 GitHub `laomao` 的 `main`。** 缓存合并修好了 S49 刷新丢早段；probe 是警告加半截闸，不是 fail-closed。冻结面没动。18/18 用来确认现有 cache，不是新逻辑的证明。

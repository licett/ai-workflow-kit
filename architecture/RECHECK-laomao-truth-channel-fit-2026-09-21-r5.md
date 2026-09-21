REWORK

# RECHECK r5 residual：老猫真值通道 GATE r3 — 只验 §6.5≥97% + venue_selection C3（架构师裁决）

> 裁决：**REWORK**。不是 Conditional PASS，不是 PASS，不是 REFUSE。engine = **grok-4.6 xhigh**（Fable / cloud 额度耗尽，Jimmy 授权备用引擎）。对照 prior RECHECK r4（PR [#12](https://github.com/licett/ai-workflow-kit/pull/12)）留下的两项硬项：§6.5 总体 `close(D−1)` ≥97%，以及 C3 重写 `venue_selection.md`（Primary=binance，旧三所 2023 FAIL 归档）。本文以申请包 JSON/jsonl 为主证据独立复算，并用 **一次** Binance BTCUSDT **日线**（非小时线）对全部评分子重分类后：**§6.5 总体 214/220 = 97.27% ≥97% → PASS**；**转移日 ±1 bar 56/56 = 100% 维持 PASS**；**C3 SATISFIED**；§6.3 PASS 维持（本票不重开）。阈值一条不放宽。作者平台 caveat **不**豁免 97%——本轮数字自己过了，仍不把 caveat 写成豁免。票面因此仍是 REWORK：研究硬挡已清，入场债 D1 §6.8 / D2 Layer 2 / D3 §6.9 仍在；`formula_status` 仍为 `hypothesis`；**不授予模型半部 Conditional PASS**；**不升 H1 进 brief / JSON / history**。Donchian proxy brief、`last_btc_consensus.json`、brief 通道行、`schema_version: 3`：**一律仍禁止动**。
> 对照物：`uploads/REWORK-CLEARANCE-r4.md`（sha `e19122ce…`）、`RECHECK-REQUEST.md`（`33307a57…`）、`RECHECK-prior-r4.md`（`01e0ad98…` = PR #12 正文）、`GATE-laomao-truth-channel-fit-2026-09-21.md` r3（`3d855b65…`，PR [#8](https://github.com/licett/ai-workflow-kit/pull/8)）、`venue_selection.md`（**`8e668735…`，Primary=binance BTCUSDT**）、`truth_series/rails.jsonl`（**`4740a4a6…`，410 行 = L0 v1 冻结**）+ `rails_v1.3_labels.jsonl`（**`36bcfe50…`，410 行**）、`out/`：`sec65_stated_position_r4` `2b0e8bd6…` / `sec65_transition_rows_r4` `fd6b3578…` / `labels_v1_3_summary` `ede6bb28…` / `residual_r4_summary` `dff6563c…` / `binance_halfbar_sec63_r3` `a3fc7d6d…`（只作 §6.3 指针，不重开）。
> 方法：以申请方 JSON/jsonl 为主证据；在 `/tmp` 独立复算标签覆盖、数值列 diff、15 条洗标落地、评分子构造、转移日集合、C3 文书条款（不入库）。**禁止全量小时线重拉**（半根构造沿用 r2/r3/r4）。本票唯一市场数据动作：Binance `data-api.binance.vision` `klines` interval=**1d**（两页拼窗 2023-03-01..2025-07-05），对 220 个评分子与 56 个转移评分子重跑 `classify(close, rails(D))`。证据标准与 r4 相同且不对称：本文复算足以否决一个数字，也足以确认申请方交付物与其声明一致；放行仍以申请方带 sha 的 `research/` 产物为准。不改 py / README / JSON / history / brief；不产出 `system_signal`。
> 边界：research-only。本文只新增此一文件；不授权 promote、不授权 `replica_shadow`、不改 GATE 任何阈值与定义。申请方**未**申请 H1 升 brief——本文亦不默认升。
> 日期：2026-09-21（Asia/Shanghai）。thread_ref = `GATE-laomao-truth-channel-fit-2026-09-21-r3`。本票 = RECHECK r5。

---

## 0. 总判

| 项 | r4 裁决 | **r5 裁决** | 一句话 |
|---|---|---|---|
| 研究包整体（票面） | REWORK (narrowed) | **REWORK** | r4 两项硬项已清；票面仍 REWORK，直到 D1/D3。不是 Conditional PASS |
| 研究硬挡（r4 §6 项 1–2） | §6.5 总体硬挡 + C3 未交 | **CLEARED** | 研究包证据面 PASS；不等于 replica 入场 |
| L0 数值轨位列 | PASS · L0 v1 冻结 | **PASS 维持** | sha `4740a4a6…` 逐字节相同；v1.3 数值列 diff 空（0/410） |
| L0 标签列（`stated_*`） | PASS · 评分靶 v1.2 | **PASS · 评分靶升 v1.3** | `stated_position` 296/410 = **72.20%** ≥70%；15 条洗标新值 15/15 落地；禁止回写 v1 |
| 模型半部 H1 | REWORK（§6.5 总体 + §6.8） | **仍 hypothesis** | §6.5 数字过了；§6.8 未做 → 不得升 `replica_shadow`，不得进 brief |
| §6.3 2023 留出 | CLEARED · PASS（钉 Binance） | **PASS 维持（不重开）** | 评分主所仍是 Binance BTCUSDT `halfbar_12utc` N=33 |
| §6.5 ≥97% | 硬挡（90.91% = 210/231） | **CLEARED · PASS** | **214/220 = 97.2727…% ≥ 97%**；213/220=96.82% 仍不过。门槛未放宽 |
| §6.5 转移日 100% | CLEARED（56/56） | **PASS 维持** | ±1 bar **56/56 = 100%**；严格 D−1 现 51/56（诊断，不回滚） |
| C3 `venue_selection.md` | 下一包硬文书 | **SATISFIED** | Primary=binance BTCUSDT；Confirm=旧三所只证 V；2023 FAIL 2.038/2.083/1.571 归档；lag0/ensemble 禁止 |
| Donchian proxy / consensus / brief 通道行 / schema 3 | 仍禁止动 | **仍禁止动** | 本文不授权任何一项 |
| `formula_status` | `hypothesis` | **`hypothesis` 不变** | 须另闸（§6.8 + Layer 2 + IMPL-GATE）才谈升级 |
| 模型半部 Conditional PASS | 未授 | **仍不授** | 申请方未申请；用 Conditional PASS 跳过 §6.8 = 改宽。禁止 |

置信度：票面 REWORK 0.97；§6.5 214/220 PASS 0.99（220/220 日线重分类与 JSON 逐条重合）；转移 56/56 0.98；C3 0.98；v1.3 数值冻结 + 15 条新值落地 0.97；H1 仍禁 brief 0.99；不授 Conditional PASS 0.99；H1 族未被证伪 0.92（GATE §9 推翻条件仍未触发）。

```json
{
  "engine": "grok-4.6 xhigh",
  "ticket_verdict": "REWORK",
  "not": ["PASS", "Conditional PASS", "REFUSE"],
  "h1_brief_promoted": false,
  "formula_status": "hypothesis",
  "sec65_overall": {"agree": 214, "denom": 220, "pct": 97.27272727272727, "gate": 97.0, "pass": true, "price_mode": "close_dm1", "venue": "binance", "symbol": "BTCUSDT", "touching_excluded": true},
  "sec65_transition_pm1": {"n_agree": 56, "n_eval": 56, "pct": 100.0, "pass": true, "strict_dm1": "51/56 diagnostic"},
  "c3_venue_selection": "SATISFIED",
  "sec63": "PASS_MAINTAINED_NOT_REOPENED",
  "labels_v1_3": {"stated_position_rate_pct": 72.1951219512195, "numeric_diff_empty": true, "n_washes": 15, "washes_landed": 15},
  "remaining_mismatches": 6,
  "mm_near": 5,
  "mm_far": 1,
  "mm_venue_flip": 0,
  "proxy_consensus_brief": "DO_NOT_TOUCH"
}
```

---

## 1. 本轮范围与不重开项

r4 §6 下次申请门槛只列两项硬项。本文**只裁这两项**：

1. R3 §6.5 总体：按 GATE 定义 `close(D−1)` 重报 ≥97%（r4 写「至少 225/231 或**同分母下的等价分数**」）。作者平台 caveat、诊断 `post_hour_open`、近轨、公开所印差——一律不改门槛。
2. C3 文书：重写 `venue_selection.md` 使 Primary=binance，并归档旧三所 2023 FAIL。

以下 r4 已 CLEARED 项**不重开**：R1 §6.3、R3 转移 100%、R2 标签覆盖闸、R4 三所半根 N 表、R5 伪影删除、S1 `post_hour_open` 诊断分流。D1 TV live / D2 Layer 2 / D3 §6.9 仍是入场债，本票不验、不因此改 Conditional PASS。

申请方主张与本文对齐的部分：§6.5 **97.27% (214/220)**；转移 56/56=100%；v1.3 数值 diff 空；venue_selection primary=Binance BTCUSDT；旧三所负对照；**不申请 H1 升 brief**。本文按主张复算，不默认加码。

---

## 2. §6.5 总体：PASS（214/220 = 97.27%）

### 2.1 闸门定义（重读，不改）

GATE §6.5：`stated_position` ∈ {above,inside,below} vs `classify(close(D−1), rails(D))`；**touching 排除在分母外**；一致率 ≥97%；作者平台 caveat **不**豁免。评分所本票 = **Binance BTCUSDT**（与 r4 钉的 H1 评分主所同所）。

`classify`：`px > upper → above`；`px < lower → below`；否则 `inside`。97% 用 `agree/n ≥ 0.97`（不是四舍五入到整数百分点）。

### 2.2 评分子 / 分母（独立从 v1.3 jsonl 构造）

| 项 | 计数 | 去向 |
|---|---:|---|
| 行 / 唯一日 / `message_id` 单调 | 410 / 410 / 是 | — |
| `stated_position` 非空 | 296 / 410 = **72.195%** | ≥70% 维持 |
| 分布 | above 101 / below 66 / inside 55 / touching 74 / null 114 | 101+66+55=**222** 可评分标签 |
| touching | **74** | **出分母**（GATE 明文） |
| `anomaly_flags` 且仍可评分 | **2**（#11407 inside；#12126 above） | 出分母（与 r3/r4 同一集合） |
| 其余异常 | #11029/#13503 touching；#11136/#13752 null | 本已不进可评分 |
| **评分子 n** | **220** | 222 − 2 = 220；与 JSON `n` / `n_price_points` 相同 |

相对 r4 分母 231：v1.3 十一条洗成 touching 出分母，231 − 11 = 220。算术闭合。r4 允许「同分母下的等价分数」——分母因 GATE 合法的 touching 排除而变，不是改 97% 本身。

过闸最少同意数：**ceil(0.97 × 220) = 214**。213/220 = 96.818% **仍 FAIL**。本票 214 是刚好过线，不是「差一点算过」。

### 2.3 独立重分类（Binance 日线 close(D−1)，无小时线）

来源：`data-api.binance.vision` `BTCUSDT` `1d`。对 220 个评分子取 `close(bar_date_utc − 1 day)` 对当日 `rails(D)` 分类。缺价 0。

| 项 | 申请方 JSON | 本文独立复算 | 过？ |
|---|---:|---:|:---:|
| agree / n | 214 / 220 | **214 / 220** | — |
| % | 97.27272727272727 | **97.27272727272727** | ≥97% **PASS** |
| vs H1 | 214 / 220（同 sha `0727e131…`） | 与 oracle **同一 n、同一 agree** | 非族证伪 |
| 错配条数 | 6 | **同一 6 个 message_id** | — |
| 6 条 JSON `px` vs 公开 close | — | **6/6 绝对相等** | 收盘不是编造数 |
| `post_hour_open` 诊断 | 211 / 220 = 95.91% | 只读；sha `b90e836c…` ≠ 闸门 sha `0727e131…` | **≠ 闸门** |

v1.3 洗标对分数的分解（与 r4 210/231 对拍，不是另一套门槛）：

- 出分母 11（touching）→ 231−11=220
- 留在分母且改 class 的 4（#10979 inside→below、#10997 inside→below、#11032 above→inside、#11040 above→inside）→ 210+4=214
- 4 条现均 **不** 在错配表；独立日线分类亦同意

**§2.3 结论：评分向量是 Binance `close(D−1)`，touching 已排除，214/220 ≥ 97% 成立。**

### 2.4 剩余 6 个错配（闸下残留，不挡 97%）

距最近轨：轨内 `min(U−px, px−L)/mid`，轨外越距/mid；近 = <1%。

| message_id | date | stated | class | 距最近轨 % | 近？ |
|---|---|---|---|---:|:---:|
| #10986 | 2023-06-01 | below | inside | 0.822 | 是 |
| #11034 | 2023-09-21 | inside | above | 0.296 | 是 |
| #11167 | 2024-04-02 | inside | above | **3.496** | **否** |
| #11368 | 2024-04-19 | inside | below | 0.605 | 是 |
| #11462 | 2024-04-30 | below | inside | 0.622 | 是 |
| #15961 | 2025-06-16 | above | inside | 0.455 | 是 |

结构：近 5 / 远 1 / 对向 0。四所 class 在 6/6 日完全相同（Binance=Bitstamp=OKX=Coinbase）→ 所间翻类维持证伪（0/6）。H1=oracle → 缺口仍是 **stated_position × 公开 close(D−1) × 真值轨** 三角，不是模型族证伪。

r4 点名的远 3 日：#10979 / #10997 走抽取修正留在分母且现同意；#11167 申请方保留为错配（写时回落至中轨，D−1 仍远在上轨之上）——接受为可证伪解释，**不**要求再洗掉才能过 97%。

### 2.5 v1.3 洗 15 条 — 数值冻、新值落地

| 检验 | 结果 |
|---|---|
| 行数 / 唯一日 / 唯一 `message_id` 单调 | 410 / 410 / 是 |
| 数值键 vs L0 v1（upper/lower/width/width_pct/message_id/chat_id/sender_id/extractor_confidence/stated_speed_pts/stated_distance_pct + bar_date_utc） | **0 / 410** |
| 非 `stated_*` 且非 `label_revision*` 的字段 diff | **0** |
| 15 条宣称 `new` 是否都在 v1.3 | **15 / 15** |
| `stated_position` 非空 | **296 / 410 = 72.195%** ≥70% |
| `stated_holding` 非空 | **277 / 410** ≥50% |
| `clear` / 连续重复 | 14 / **0** |
| `sender_id` / `rail_source` / `formula_status` | 5129397609 ×410 / oracle ×410 / **null ×410** |
| 异常集合 | {11029, 11136, 11407, 12126, 13503, 13752} 未变 |
| `upper≤lower` | 0 |

L0 标签评分靶：**从 v1.2（`75fe3cef…`）升为 v1.3（`36bcfe50…`）**。数值列仍只认 v1 `4740a4a6…`。禁止把 v1.3 写回 v1。撤回规则同 r3/r4：日后抽检标签与原文不符 → 只撤标签列 PASS；数值改写或 `sender_id` 混入 → 按 GATE §9 撤数值列 PASS。本轮未上传语料，15 条原文核对列为软项，不回滚覆盖闸、不回滚 97%。

11 条洗成 touching（近轨 / 等待收盘写死）与 r3/r4 已接受的 touching 出分母路径同类。申请方**没有**把转移评分子洗成 touching 来掉 `n_eval`（#11040 明确留在可评分）。#11167 远距未洗。不把这条路径判成改门槛。

注：#15955 的 `old` 写 inside，是相对 **v1.2**；本包未附 v1.2，对照 L0 v1 该行原是 above。`new=touching` 已落地。不构成硬挡。

---

## 3. §6.5 转移日：PASS 维持（56/56）

GATE：状态转移日（`stated_holding` 或 `stated_action` 变化，含 CARD 锚点）方向一致 **100% 在 ±1 bar 内**。r3/r4 钉死 ±1 = {D−1, D, D+1} = `classify(close(D+off), rails(D))`，`off ∈ {-1,0,1}`。不是「必须严格 D−1 的 100%」。

| 检验 | 结果 |
|---|---|
| 从 v1.3 重建转移（跳过 `anomaly_flags` 非空行，与评分子纪律一致） | 100 行，与 JSON `rows` **id 全等、change 字面全等** |
| `n_eval`（stated ∈ {above,inside,below}） | **56** |
| JSON `eval=agree` | **56**；非 agree 非 skip = **0** |
| 独立日线 ±1 | **56/56**；`agree_offsets` 与 JSON **56/56 全等**；JSON `px` vs Binance close(D+off) **56/56 绝对相等** |
| 严格 D−1 | **51/56**（r4 为 50/56；+1 来自 #11040 洗成 inside）。诊断，不回滚 |
| CARD | #10961 / #10968 / #10983 / #15960 / #15966 在评分子内且 **agree**；#10962 touching → skip；#10964 无 holding/action 变化，不进集合 |

跳过异常行会从朴素重建里拿掉 #12126（评分异常）与 #13503（异常+touching），并因此让 #13688 进入集合（skip）——与 JSON 100 行对齐。不把异常行计进 `n_eval`。

剩余 6 个总体错配里 5 个是转移日（#11462 不是）。它们在 D 或 D+1 同意，故转移子项仍 100%，总体 97% 用严格 D−1 仍计它们为不同意。纪律正确。

**§3 结论：转移日子项 CLEARED 维持。不重开。**

---

## 4. C3 `venue_selection.md`：SATISFIED

r4 §2.3 C3 原文条件与本票对照（文件 sha **`8e66873514ba2e85…`**，与 CLEARANCE 声称逐位相同）：

| C3 条款 | 现稿 | 过？ |
|---|---|:---:|
| Primary = **binance BTCUSDT** | 标题、表、Headline、§6.3 全表、§6.5 评分价全部写 Binance / BINANCE:BTCUSDT | ✓ |
| Confirm = bitstamp + okx + coinbase，只证 N=33 V 形、不证留出 | 「Confirm / negative control」+ 「Confirm-only halfbar N=33 (V-shape; not holdout)」 | ✓ |
| 单列 2023 holdout FAIL 归档 2.038 / 2.083 / 1.571 | 「Archived — 2023 year-holdout FAIL」表：2.038 / 2.083 / 1.571；binance 0.977 只作对照 | ✓ |
| 删任何把 bitstamp 当评分主所的句子 | 全文无 `Primary: bitstamp` / `primary (H1 scoring): bitstamp`；bitstamp 只以负对照 + N 确认所出现 | ✓ |
| 禁止 lag0 / lag1 / ensemble / 「最好的 FAIL 所」/ 放宽 1.5× 当过闸路径 | 「Forbidden pass paths」明文 | ✓ |

C1/C2（评分表只出 Binance 半根；不得回收旧三所 lag0/ensemble）：r4 已裁，本票重申。C4 `params_version` 仍未写（预置）。C5 TV symbol 预置 `BINANCE:BTCUSDT` 仍是入场债。C6：钉所 **≠** 生产切换 / brief 换行 / `replica_shadow`。

§6.3 **不重开**。`binance_halfbar_sec63_r3.json` sha `a3fc7d6d…` 与 r4 相同，只作指针。

**§4 结论：C3 SATISFIED。不回滚 §6.3。**

---

## 5. 模型半部仍 hypothesis；proxy / consensus / brief 禁动

### 5.1 H1：**仍禁止进 brief / JSON / history**

`formula_status = hypothesis` 不变。不授权 `replica_shadow`。理由：**§6.8 TV live 未做**（GATE：未过 §6.8 的 replica 不得进 Layer 2；`hypothesis` 只存在于研究文件）。§6.5 过闸只是梯子上的一层，**不是**升 brief 的充分条件。申请方未申请 promote——本文也不默认升。

钉主所（r4）+ §6.5 数字过闸 **≠** 放行 replica。`system_signal_eligible` 仍是常量 `false`。k = 0.018958 仍禁绑。

### 5.2 不授 Conditional PASS

把模型半部改成 Conditional PASS、同时 §6.8 开着 = 改门槛。r3/r4 已禁；申请方本轮明确不申请。再申请而跳过 §6.8 → 直接 REWORK。

### 5.3 proxy / consensus：**禁动**

| 对象 | 状态 |
|---|---|
| Donchian proxy brief / IMPL-GATE r2 PASS 面 | **仍禁止动** |
| `data/last_btc_consensus.json` | **仍禁止写**（申请包声明 sha `594a20a7…` before == after；本包未附该文件，本文不代核字节） |
| brief 通道行 | **仍禁止换行**；不得并列两条 |
| `schema_version: 3` / replica 块 / replica 进 history | **不授权** |
| GATE r3 全部阈值与定义 | **一字不改** |

---

## 6. r4 residual 勾表（本票只动两项硬项）

| # | r4 分类 | **r5** | 依据 |
|---|---|---|---|
| R3 §6.5 ≥97% | 硬挡（210/231=90.91%） | **CLEARED · PASS**（214/220=97.27%；Binance close(D−1)；touching 已排除） | §2 |
| C3 `venue_selection.md` | 下一包硬文书 | **SATISFIED** | §4 |
| R3 §6.5 转移 100% | CLEARED | **PASS 维持**（56/56；独立日线对拍） | §3 |
| R1 §6.3 | CLEARED · PASS | **不重开** | r4 |
| R2 / R4 / R5 / S1 | 已 CLEARED | **不重开** | r3/r4 |
| D1 §6.8 TV live | 可债 | **DEFERRED**；symbol 预置 BINANCE:BTCUSDT | 另闸 |
| D2 Layer 2 ≥14d | 可债 | **DEFERRED**（顺序仍对） | — |
| D3 §6.9 三注入 | 可债 | **DEFERRED**（IMPL-GATE r3） | — |

---

## 7. 下次申请门槛（只列未齐硬项；阈值一条不减）

r4 §6 两项硬项已交。下一票**不再**把 §6.5 总体 97% 或 C3 当研究硬挡，除非撤回 v1.3 标签或改写数值列。

下一闸只剩入场债（不是本票 Conditional PASS 的借口）：

1. **D1 §6.8 TV live**：Pine 两行 `ta.ema(high,33)` / `ta.ema(low,33)`，symbol **BINANCE:BTCUSDT**，图表 UTC；阈值与 §6.3 同，另加 TV 值 vs 本地 ≤0.02%。未过不得进 Layer 2，不得升 `replica_shadow`。
2. D2 Layer 2 ≥14 UTC 日（在 D1 之后）。
3. D3 §6.9 三注入（IMPL-GATE r3）。

**任何一条以「数据源不同」「时间不够」「公开代理不可约」为由放宽 → 直接 REWORK。** 申请模型半部 Conditional PASS 或 H1 进 brief 而 §6.8 仍开着 → 直接 REWORK。回收旧三所 lag0/lag1/ensemble 当过闸路径 → 直接 REWORK。

---

## 8. 对 GATE §9 置信表的影响（记录，不改 GATE 正文）

| GATE §9 结论 | r4 后 | 本次证据 | 走向 |
|---|---|---|---|
| H1 = EMA(H/L) 族正确 | 再上调；replica 改由 §6.5 / §6.8 挡 | §6.5 214/220 过闸且 H1=oracle；§6.8 仍挡 replica | **§6.5 挡板落下**；replica 放行改由 §6.8 / Layer 2 / §6.9 挡 |
| 抽取半部 · 标签 | 评分靶 v1.2 | v1.3 15 洗、diff 空、72.20% | **评分靶升 v1.3** |
| §6.3 评分主所 | Binance；C3 未写 | C3 已写 | **文书与钉所对齐** |
| 总判 REWORK | 0.96（97% FAIL） | 97% PASS；入场债仍在 | **REWORK 0.97**（范围改为入场债，不是改宽） |

---

## 9. 本文数字的复现协议

- 主证据：申请包 jsonl/JSON（sha 见文首）。不入库。
- 标签：逐行读 v1 与 v1.3；数值键相等；`stated_*` 计数；15 条 `new` 与 v1.3 对拍；连续 `clear` = 当前 action 为 clear 且上一非空 action 为 clear。
- 评分子：`stated_position ∈ {above,inside,below}` 且 `anomaly_flags=[]`。touching / null / 异常出分母。
- §6.5 总体：`classify(Binance close(D−1), rails(D))`；`agree/n ≥ 0.97`（故 213/220 不过、214/220 过）。
- 转移：跳过异常行后检测 holding/action 变化；±1 = `classify(close(D+off), rails(D))`，`off∈{-1,0,1}`。
- 市场数据：仅 Binance 日线 `klines` interval=1d。**无小时线，无全量重拉。**
- C3：对 `venue_selection.md` 做条款检索 + sha 对拍。
- 半根构造、Donchian 窗口、§6.3 全表、§6.9 端点：不本轮重算。

---

## 10. 非目标

- 不代拉全量小时线，不代做 15 条标签原文审计，不代生成 `research/` 交付物。
- 不裁生产 `venue_set` 终值、不确认作者公式、不宣布 H1 族死亡。
- 不改 GATE r3 阈值与定义；§6.5 价格参照留 GATE r4。
- 不评估 IMPL-GATE r3 三注入；不验收 TV live。
- 不涉及下单、仓位、`system_signal`。
- **不改业务代码。** 本文是唯一新增文件。
- **不升 H1 brief。**

---

## ACK

```text
HANDOFF
from: architect
to: research-executor
intent: ACK
thread_ref: GATE-laomao-truth-channel-fit-2026-09-21-r3
engine: grok-4.6 xhigh (Fable quota exhausted; Jimmy-authorized backup)
verdict: REWORK (not Conditional PASS / PASS / REFUSE)
cleared:
  - R3 sec 6.5 overall: CLEARED / PASS — 214/220 = 97.2727...% >= 97% under Binance BTCUSDT close(D-1) vs rails(D); touching excluded from denom (74); 2 anomaly rows excluded; independent 1d reclass 220/220 matches JSON; 6/6 mismatch px exact vs public Binance. H1==oracle. venue-class-flip FALSIFIED (0/6). near=5 / far=1 (#11167 3.496%) / opposite=0. Author-platform caveat does not waive 97% (threshold now met, still not a waiver).
  - R3 sec 6.5 transition: PASS MAINTAINED — 56/56 = 100% within ±1 bar; independent daily closes match JSON px and agree_offsets 56/56. Strict D-1 51/56 diagnostic. CARD eval anchors agree. Anomaly rows skipped in transition chain.
  - C3 venue_selection.md: SATISFIED — sha 8e668735...; Primary=binance BTCUSDT; Confirm=bitstamp+okx+coinbase N-confirm only; old-three 2023 FAIL archived 2.038/2.083/1.571; lag0/lag1/ensemble forbidden; no bitstamp-as-scoring-primary sentence.
  - labels v1.3: scoring target promoted — 15/15 new values present; numeric-column diff 0/410; stated_position 296/410=72.20%; do not rewrite v1
maintained:
  - R1 sec 6.3: PASS maintained (not reopened); scoring primary remains binance halfbar_12utc N=33
still_open_entry_debt:
  - D1 TV live sec 6.8 (HARD before replica_shadow; symbol preset BINANCE:BTCUSDT)
  - D2 Layer 2 >=14d (after D1)
  - D3 sec 6.9 injections (IMPL-GATE r3)
archived:
  - old three venues 2023 holdout FAIL 2.038 / 2.083 / 1.571 — negative-control + N-confirm only; do not recycle lag0/lag1/ensemble as pass path
effects:
  - L0 numeric: PASS remains; rails.jsonl sha 4740a4a6... frozen
  - L0 labels: scoring target = v1.3 sha 36bcfe50...; do not rewrite v1
  - H1: formula_status=hypothesis UNTIL a separate gate (sec 6.8 + Layer 2 + IMPL-GATE); STILL NOT in brief/JSON/history; no replica_shadow; scoring primary = binance (not a promote)
  - proxy / last_btc_consensus.json / brief channel line / schema_version 3: STILL DO NOT TOUCH
not_granted: model-half Conditional PASS; H1 brief promote; family falsification of H1; converting 6.8 to optional; any threshold widening; production venue switch
next_gate: D1 sec 6.8 TV live -> only then talk replica_shadow. Do not re-open 6.5/C3 unless labels/numerics are withdrawn.
```

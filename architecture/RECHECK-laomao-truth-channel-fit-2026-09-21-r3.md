REWORK (narrowed)

# RECHECK r3 residual：老猫真值通道 GATE r3 — 清项收窄后再验（架构师裁决）

> 裁决：**REWORK (narrowed)**。不是 Conditional PASS，不是 PASS，不是 REFUSE。engine = **grok-4.6 xhigh**（Fable / cloud 额度耗尽，Jimmy 授权备用引擎）。对照 prior RECHECK r2（PR [#10](https://github.com/licett/ai-workflow-kit/pull/10)）的 residual 清单：申请方本轮如实交了 R2 / R4 / R5 / S1，本文以申请包 JSON/jsonl 为主证据独立复算后 **CLEARED**。票面仍不能改判：§6.3 留出 2023 折三所均 >1.5（最低门槛），§6.5 85.04% < 97% 且转移日 75% < 100%。**阈值一条不放宽。** 分层：L0 数值列 PASS 维持（v1 冻 sha `4740a4a6…`）；**L0 标签列 REWORK → PASS（v1.1）**；模型半部 H1 **仍 REWORK**，范围再收窄到留出行 + §6.5 + §6.8 TV live。`formula_status` 仍为 `hypothesis`；H1 **仍不得进 brief / JSON / history**。Donchian proxy brief、`last_btc_consensus.json`、brief 通道行、`schema_version: 3`：**一律仍禁止动**。
> 对照物：`uploads/REWORK-CLEARANCE-r2.md`（sha e39d4b0a…）、`RECHECK-REQUEST.md`（5d2c64e5…）、`RECHECK-prior-r2.md`（e0e0945f… = PR #10 正文）、`GATE-laomao-truth-channel-fit-2026-09-21.md` r3（3d855b65…，PR [#8](https://github.com/licett/ai-workflow-kit/pull/8)，与 r2 同一份）、`venue_selection.md`（0897bbfb…）、`truth_series/rails.jsonl`（**4740a4a6…，410 行 = L0 v1 冻结**）+ `rails_v1.1_labels.jsonl`（**45e061c6…，410 行**）、`out/`：`labels_v1_1_summary` 8aace2fa… / `venue_halfbar_N_scan_r2` 7e3db0a7… / `holdout_by_venue_r2` 9aa16ecd… / `sec65_stated_position_r2` 3419085d… / `residual_r2_summary` 4d94ca07… / `production_write_proof_r2` 13981267…。
> 方法：以申请方 JSON/jsonl 为主证据；在 `/tmp` 独立复算标签覆盖、数值列 diff、N 20–45 V 形、留出比值、§6.5 算术与多所错配结构（不入库）。**禁止全量三所小时线重拉**（本轮不重做 r2 §1 半根构造复现）。**最多一次** Bitstamp BTC/USD 日线小抽检：对 35 个 §6.5 不一致日的 `close(D−1)` 公开核对，35/35 与申请包逐分相等。证据标准与 r2 相同且不对称：本文复算足以否决一个数字，也足以确认申请方交付物与其声明一致；放行仍以申请方带 sha 的 `research/` 产物为准。不改 py / README / JSON / history / brief；不产出 `system_signal`。
> 边界：research-only。本文只新增此一文件；不授权 promote、不授权 `replica_shadow`、不改 GATE 任何阈值与定义。r1/r2 留给 GATE r4 的定义问题（§6.5 价格参照、§6.9 缺口端替代）本文仍不裁。
> 日期：2026-09-21（Asia/Shanghai）。thread_ref = `GATE-laomao-truth-channel-fit-2026-09-21-r3`。

---

## 0. 总判

| 项 | r2 裁决 | **r3 裁决** | 一句话 |
|---|---|---|---|
| 研究包整体（票面） | REWORK（residual） | **REWORK (narrowed)** | R2/R4/R5/S1 清且复算成立；§6.3 留出 + §6.5 仍 FAIL，阈值不动 → 票面仍 REWORK，范围收窄 |
| L0 数值轨位列 | PASS · L0 v1 冻结 | **PASS 维持** | sha `4740a4a6…` 与 r2 冻结值逐字节相同；v1.1 数值列 diff 空（0/410） |
| L0 标签列（`stated_*`） | REWORK（55.6%） | **PASS · L0 v1.1** | `stated_position` 296/410 = **72.20%** ≥70%；holding 277/410 = 67.56% ≥50%；#10962 touching / #10968 holding 已补；58 个连续 `clear` 已置空（剩 14，连续重复 0）；数值列冻结 |
| 模型半部 H1 | REWORK（留出 + §6.5 + §6.8） | **REWORK 维持，再收窄** | 三所半根 N=33 V 形 CLEARED；**2023 留出 2.038 / 2.083 / 1.571 全 FAIL**（结构取证成立，基差假说已证伪）；§6.5 85.04% / 转移 75% 仍 FAIL；§6.8 仍债 |
| R4 三所半根 + N 全表 | 硬挡 | **CLEARED** | 三所各 26 点 N=20–45，单谷均在 33；N±1 增幅 98–266% |
| R5 `venue_selection.md` | 硬挡（伪影 0.156/0.155/0.167） | **CLEARED** | 伪影值已删，数字与 `venue_halfbar_N_scan_r2.json` / `holdout_by_venue_r2.json` 同管线 |
| S1 `post_hour_open` 诊断 | 软（标签=闸门向量） | **CLEARED** | 闸门 sha `531b66bc…` ≠ 诊断 sha `413f9d00…`；91.03% ≠ 85.04%；断言字段为 true |
| §6.3 2023 留出 | 硬挡（缺 OKX/Coinbase 半根） | **维持硬挡**（取证齐） | 不是改债，**也不是模型族证伪**（见 §5） |
| §6.5 ≥97% + 转移 100% | 硬挡 | **维持硬挡** | 不是改债，**也不是模型族证伪**；「所间印差翻类」假说已被申请方自己的三所表证伪（见 §6） |
| Donchian proxy / consensus / brief 通道行 / schema 3 | 仍禁止动 | **仍禁止动** | 本文不授权任何一项 |
| `formula_status` | `hypothesis` | **`hypothesis` 不变** | 留出 / §6.5 / §6.8 任一未过即不得升 `replica_shadow` |

置信度：票面 REWORK (narrowed) 0.95；标签覆盖与数值冻结 0.97（jsonl 独立点数）；三所 V 形 0.93（表内自洽，未重拉小时线）；2023 留出三所 FAIL 0.96（比值由申请包 train/test 复原至 6 位）；§6.5 85.04%/75% 0.97；「所间印差翻类」不成立 0.94（35/35 三类一致）；H1 族未被证伪 0.90（GATE §9 推翻条件未触发）。

---

## 1. 宣称已清四项：独立核验

### 1.1 标签 72.2% + 数值 diff 空 — **CLEARED**

| 指标 | v1（冻） | v1.1 | 本文复算 | 闸 |
|---|---:|---:|---:|---|
| 行数 | 410 | 410 | 410 / 410 | — |
| sha256 | `4740a4a6…` | `45e061c6…` | 逐字节相同 | 版本规则 |
| 数值列 mismatch | — | 宣称 0 | **0 / 410** | 空 diff ✓ |
| `stated_position` 非空 | 228 = 55.61% | 296 = 72.20% | **296 / 410 = 72.195%** | ≥70% ✓ |
| 分布 v1.1 | — | — | above 115 / below 73 / inside 48 / touching 60 / null 114 | enum 合法 |
| `stated_holding` 非空 | 276 = 67.32% | 277 = 67.56% | **277 / 410** | ≥50% ✓ |
| `stated_action` | clear 72（连续重复 58） | clear 14 | **14；连续重复 0**；变化类型仅 `clear→null` × 58 | 动作语义 ✓ |
| #10962 position | null | touching | touching；detail「价格保持在27500附近通道下轨处」 | 锚点 ✓ |
| #10968 holding | null | holding | holding；action `add_back`；position above | 锚点 ✓ |

数值列验收键（r2 §9.1）：`message_id / sent_at_utc / bar_date_utc / upper / lower / width / width_pct / anomaly_flags / rail_source / rail_confidence / source_text_sha256` — 与 v1 逐行相等。结构再核：410 唯一日 / 唯一 `message_id` 单调、`sender_id` 5129397609 × 410、`rail_source=oracle` × 410、`formula_status=null` × 410、`upper≤lower` 0 行、异常 6 行集合未变 {11029, 11136, 11407, 12126, 13503, 13752}。

+68 条新 position 中 **36 条是 touching、32 条进入 {above,inside,below}**。GATE §6.5 分母排除 touching，故覆盖过闸**不等于** 97% 自动改善（见 §6：评分子从 202→234，一致率只从 83.66%→85.04%）。

剩余 14 个 `clear` 均配 `stated_holding=cash`，看起来是「当帖宣告清仓」而非连续状态回声——这正是 r1/r2 要求的语义。

**§1.1 结论：R2 CLEARED。L0 标签列可升（§6.1）。** 本轮未上传语料，+68 条新标签的原文核对列为软项，不回滚覆盖闸。

### 1.2 三所半根 N 表 — **CLEARED**

来源：`out/venue_halfbar_N_scan_r2.json`（sha `7e3db0a7…`）。本文只做表内自洽，不重拉小时线。

| Venue | n_daily / n_partial | N 点数 | 最优 N | N33 RMSE% | N32 / N34 增幅 | V@33 |
|---|---:|---:|---:|---:|---:|:---:|
| bitstamp | 1276 / 942 | 26（20–45 无缺） | 33 | 0.072532 | +197.4% / +98.3% | 是 |
| okx | 1276 / 942 | 26 | 33 | 0.050689 | +265.8% / +226.1% | 是 |
| coinbase | 1276 / 942 | 26 | 33 | 0.065147 | +227.9% / +114.8% | 是 |

三所 `best_halfbar == N33_halfbar`，`V_shape_at_33` 与「argmin RMSE = 33 且两侧更高」一致。Kraken 0/0 维持 report-only。这补齐 r2 R4 / GATE §5.3「V 形须三所同现 N=33±0」。**未重实现半根递推**——构造正确性沿用 r2 §1（已独立复现至 1e-15）；本轮只确认交付表完整且自洽。

**§1.2 结论：R4 CLEARED。** 不因此裁定 `venue_set` 终值（§6.3 留出未过）。

### 1.3 `venue_selection.md` — **CLEARED**

sha `0897bbfb…` = 申请方清单。正文声明只保留 `halfbar_12utc`。检索：`0.156` / `0.155` / `0.167` / `n=916` / `2022-12-24` **均不在文件中**。headline 数字与 N 表 / 留出 JSON 同一组（bitstamp 0.0725、okx 0.0507、coinbase 0.0651；2023 折 2.0384 / 2.0834 / 1.5709）。文中「lag0」只出现在「已删除伪影」句，不是第二套数。

软项：`compare_summary.json` 仍未交（r2 R5 顺带）。不回滚文书级 CLEARED。

**§1.3 结论：R5 CLEARED。**

### 1.4 `post_hour_open` 断言 — **CLEARED（诊断，非闸门）**

`sec65_stated_position_r2.json`：

| 向量 | n | agree | % | price_vector sha |
|---|---:|---:|---:|---|
| 闸门 `close_dm1`（oracle v1.1） | 234 | 199 | **85.0427%** | `531b66bc80ff71a5…` |
| 闸门 `close_dm1`（H1 v1.1） | 234 | 199 | 85.0427% | 同闸门 |
| 诊断 `post_hour_open` | 234 | 213 | **91.0256%** | `413f9d003f578298…` |

`diagnostic_assert_price_vector_differs = true`，且两 sha **确实不同**。r2 抓到的「声明 post_hour、数字却等于 close_dm1」已不在。GATE 定义仍是 `close(D−1)`；91.03% 只是诊断，**不改 97% 判定**。本轮未拉小时线，不独立复现 213/234 的逐日价，只确认向量已切换。

**§1.4 结论：S1 CLEARED。**

---

## 2. Bitstamp 日线小抽检（本轮唯一市场数据动作）

对 `multi_venue_mismatch_explain` 的 35 个 `dm1` 日，公开拉取 Bitstamp BTC/USD 日线 close，与申请包 `bitstamp_close_dm1` 比对：

- **35 / 35 绝对相等**（含 GATE 示例 2023-04-25 = 28300、2023-04-18 = 30395、2023-11-22 = 37424）。
- 未拉小时线，未拉 OKX / Coinbase。

结论：§6.5 错配表上的 Bitstamp 收盘**不是编造数**。多所类一致（§6.2）因此可以当作「三所公开收盘对同一组轨位给出同一类」，而不是「Bitstamp 一家印错」。

---

## 3. §6.3 2023 留出：维持硬挡（取证齐；不改债；不证伪族）

### 3.1 数字（申请包 train/test 复原）

半根 N=33；固定 N 与训练两年重选 N* 三所均为 33，比值逐位相同。

| Venue | 2023 test / train RMSE% | **ratio** | ≤1.5？ | 2024 | 2025 |
|---|---|---:|:---:|---:|---:|
| bitstamp | 0.098749 / 0.048444 | **2.038421** | FAIL | 0.6655 ✓ | 0.5079 ✓ |
| okx (USDT) | 0.069413 / 0.033317 | **2.083407** | FAIL | 0.6592 ✓ | 0.4894 ✓ |
| coinbase | 0.081479 / 0.051866 | **1.570945** | FAIL | 0.8235 ✓ | 0.6313 ✓ |

r2 指定的判定实验已做完：OKX-USDT 半根 **更差**（2.083 > 2.038），不是救命所。申请方自报 2023-H1 bitstamp−okx close 基差均值仅 +0.056%（中位 +0.031%），比 ~0.1% 双轨偏小一个数量级——与「OKX 半根更差」同向，**USD/USDT 基差假说作为留出修复被证伪**。Coinbase 最好仍是 1.571 > 1.5。N* 全 33：没有「未重拟」退路。

### 3.2 三项选项的裁断

| 选项 | 裁断 | 理由 |
|---|---|---|
| **维持硬挡** | **是** | GATE §6.3 留出行最低 = 目标 = ≤1.5×。一行不过 → §6.3 不过 → `formula_status` 不得离 `hypothesis`。给 Conditional PASS = 把门槛改成「≤2.08× 待解释」，即改宽。禁止。 |
| 改债 | **否** | 债的定义是「研究包证据 PASS 可不含，但 `replica_shadow` 入场再硬卡」（如 D1 TV live）。留出是**现在**的最低门槛，不是入场附件。 |
| 模型族证伪 | **否** | GATE §9 推翻「H1 = EMA(H/L) 族正确」的条件是：≥4 所 + 半根后 **pooled RMSE 仍 >0.20%**，或 **N 的 V 形消失**。本轮三所 RMSE 0.0507–0.0725 ≪ 0.20%，V 形在 33 同现且更尖。留出 FAIL 证的是「单一全局 (N,α) 在 2023 vs 2024–25 的时间稳定性」过不了 1.5×，**不是族认错**。2023 年绝对 RMSE 仍低于逐年最低门槛 0.30（甚至低于目标 0.15）。比值高，部分是因为 2024–25 训得极紧（okx train 0.033%）——诊断，**不是放宽理由**。 |

### 3.3 结构 fail 取证：接受，并关掉一条退路

接受申请方声明：在 EMA(H/L) N=33 `halfbar_12utc` 下，{bitstamp, okx, coinbase} **没有**一所过 2023 留出。r2 R1「全部 >1.5 → 留出行不过，不得放宽」现已有三所半根证据，不再是「缺所所以暂挂」。

仍开着、但**不再阻塞本条取证成立**的族内最后一试：GATE §5.3 的第 4 所（Binance BTCUSDT）。若申请方另交与本管线同预热的 Binance 半根且 2023 折 ≤1.5，允许按「同一所出全部行、不得跨所拼表」重报 §6.3 全表。未交或仍 >1.5 → 留出行维持 FAIL。**不把「还没拉 Binance」写成未完成硬挡来推迟本条 FAIL。**

下一步研究路径（不改门槛）：按 GATE §6.7 试 H3 → H4 → H5，每族同一套留出表。那是**族内穷尽之后的义务**，不是把本票改成「H1 已证伪」。平行直线 / 常数 k（H0 / H6）仍不得回潮。

**§3 结论：R1 维持硬挡。结构 fail 取证成立。基差退路关闭。不改债。不证伪 H1 族。**

---

## 4. §6.5：维持硬挡（所间翻类已证伪；不改债；不证伪族）

### 4.1 闸门数字（本文复算算术）

| 项 | 申请方 | 本文 |
|---|---|---|
| v1.1 `close(D−1)` vs oracle | 199/234 = 85.04% | **199/234 = 85.0427%**；mismatch 列表 35 条 |
| 同口径 vs H1 | 199/234 = 85.04% | 与 oracle **同一百分数、同一 n** |
| ≥97% | FAIL | **FAIL**（要 227/234，还需消化 28 个错配） |
| 转移日 v1.1 | 42/56 = 75.0%（100 个变化，44 skip） | **agree 42 / disagree 14 / skipped_no_pos 44**；42/56 = 75%；100% FAIL |
| 作者平台 caveat | 不可得，公开代理有不可约缺口 | 接受「不可得」为事实；**不接受**「因此放宽 97%」 |

v1 → v1.1：评分子 202→234（+32 条可评分新标签），一致 169→199（+30）。新标签几乎都同意公开收盘类；覆盖过闸对 97% **几乎没有帮助**。

### 4.2 35 个错配日：申请方解释 vs 其自己的表

申请方写道：许多错配是近轨（<1%），「venue print differences flip the class」。`multi_venue_mismatch_explain` 35 行给出了反证：

| 检验 | 结果 |
|---|---|
| 三所 `*_class` 互相不一致 | **0 / 35** |
| 距最近轨 <1% of mid | 24 / 35（近轨为主，属实） |
| 距最近轨 ≥1% | 11 / 35 |
| 其中 above↔below 对向 | **3**：2023-04-19 #10958（6.01%，detail「跌破下轨」，Bitstamp D−1=30395 vs 轨 27698–28700）；2023-11-23 #11068（5.31%，**v1.1 新标**「跌破通道下轨」，D−1=37424 vs 34319–35567）；2025-01-10 #13283（1.76%，「站上通道」但收盘在下轨之下） |

Bitstamp 这 35 个 D−1 收盘已抽检 35/35 相等（§2）。三所公开收盘在**每一个**错配日给出同一类。因此：

- 「所间印差把类翻过去」——**证伪**。近轨日也没有出现「Bitstamp inside / OKX above」这种翻类。
- 「作者平台收盘不可得 → 97% 不可证」——对 **24 个近轨日**仍是诚实 caveat（GATE 预览就写过 2023-04-26 这一类）。对 **3 个对向日**不够：5–6% 的偏离不是 USD/USDT 基差或盘中印差能解释的；更像标签抽的是叙述/另一时刻，或作者看的根本不是这两条轨。
- 35 里 33 条在 v1 已有同一 `stated_position`；只有 2 条是 v1.1 新增，其中 #11068 是远距对向。标签升格**不洗掉**这张错配表。

H1 与 oracle 同意率相同，说明 85% 缺口是 **stated_position × 公开 close(D−1) × 真值轨** 的三角，不是 H1 拟合残差。故 **不是模型族证伪**。

### 4.3 三项选项的裁断

| 选项 | 裁断 | 理由 |
|---|---|---|
| **维持硬挡** | **是** | 97% 与转移 100% 是 GATE §6.5 最低门槛。公开三所已穷尽「换所翻类」；剩余近轨子集仍要作者平台或改定义（GATE r4，本文不裁）；远距对向要标签/时钟审计。在数字落到门槛之前，票面不得过。 |
| 改债 | **否** | 把 97% 降成 `replica_shadow` 入场债 = 改宽。作者平台不可得在 r1 就是 Conditional（阈值不放宽），不是豁免。 |
| 模型族证伪 | **否** | 同口径 H1=oracle=85.04%。§6.5 FAIL 不打击「EMA(H/L) 是否生成真值轨」。 |

转移日：CARD 锚点里 #10961 / #15966 同意，#10968 / #15960 不同意。14 个 disagree 与错配表大量重叠（#10965、#10968、#10986、#11030、#11034、#11040、#11114、#11117、#11145、#11167、#11368、#13170、#15960、#15961）。集合已按 holding/action **变化**重算（r2 要求），数字是 75% 不是「未跑」。

**§4 结论：R3 维持硬挡。所间翻类假说证伪。不改债。不证伪 H1 族。**

---

## 5. r2 residual 勾表

| # | r2 分类 | **r3** | 依据 |
|---|---|---|---|
| R1 §6.3 2023 留出 | 硬挡 | **STILL_OPEN · 硬挡**（取证齐；基差退路关） | §3 |
| R2 标签列 | 硬挡 | **CLEARED** → 标签列 PASS | §1.1 / §6.1 |
| R3 §6.5 97% + 转移 100% | 硬挡 | **STILL_OPEN · 硬挡**（已跑、仍 FAIL；翻类假说证伪） | §4 |
| R4 三所半根 + N 全表 | 硬挡 | **CLEARED** | §1.2 |
| R5 venue_selection 伪影 | 硬挡 | **CLEARED** | §1.3 |
| D1 §6.8 TV live | 可债 | **DEFERRED** 不变 | 未上传 |
| D2 Layer 2 ≥14d | 可债 | **DEFERRED**（顺序仍对） | — |
| D3 §6.9 三注入 | 可债 | **DEFERRED**（IMPL-GATE r3） | — |
| D4 不一致日 ≥3 所收盘表 | 随 R3 | **交了；解释被证伪** → 并回 R3 硬挡 | §4.2 |
| S1 post_hour 诊断 | 软 | **CLEARED** | §1.4 |
| S2–S6 | 软 | **STILL_OPEN**（本轮未交 SHA 清单 / 语料抽检方法 / compare_summary / 第 4 所） | 不阻塞已清项 |

---

## 6. L0 标签列是否可升；H1 是否仍禁 brief；proxy / consensus

### 6.1 L0 标签列：**可升 → PASS（v1.1）**

升格效力：

- `truth_series/rails_v1.1_labels.jsonl` sha `45e061c6a97a33ef43eb6a42401927b76eb31ddbfe090984a9361d3d87d2f58d` = **L0 v1.1 标签靶**。`stated_*` 评分从此用 v1.1。
- 数值列仍只认 v1 `rails.jsonl` sha `4740a4a68ca6c69c60e149a68a61a3f63057d4d019c43f194fea1c21caf449a9`。禁止把 v1.1 写回 v1 文件。
- 撤回：日后抽检发现标签与原文不符 → 只撤标签列 PASS，数值列不动；发现数值改写或 `sender_id` 混入 → 按 GATE §9 撤数值列 PASS。

不随升格带走的：§6.5 的 35 日错配（33 条旧标 + 2 条新标）仍在硬挡里。#11068 这条 v1.1 新标是远距对向，记在证据链，作为标签质量抽检的优先样本——**不是**覆盖闸回滚条件。

### 6.2 H1：**仍禁止进 brief / JSON / history**

`formula_status = hypothesis` 不变。不授权 `replica_shadow`。理由任一即足：§6.3 留出 FAIL、§6.5 FAIL、§6.8 未做。本轮对 H1 的正面效力仅限证据链：三所半根 N=33 V 形成立（表内），族未被证伪。

### 6.3 proxy / consensus：**禁动**

| 对象 | 状态 |
|---|---|
| Donchian proxy brief / IMPL-GATE r2 PASS 面 | **仍禁止动** |
| `data/last_btc_consensus.json` | **仍禁止写**（申请包 sha `594a20a7…` before == after） |
| brief 通道行 | **仍禁止换行**；不得并列两条 |
| `schema_version: 3` / replica 块 / replica 进 history | **不授权** |
| `system_signal_eligible` | 常量 `false` |
| k = 0.018958 | 禁绑 |
| GATE r3 全部阈值与定义 | **一字不改** |

---

## 7. 下次申请门槛（RECHECK r4；只列未齐硬项；阈值一条不减）

1. **R1 留出**：要么 (a) 第 4 所（Binance）半根同管线 2023 折 ≤1.5 并**同一所**重报 §6.3 全表；要么 (b) 按 §6.7 交 H3/H4/H5 全套留出，且某族全行过最低门槛。继续扫已 FAIL 的三所 N、或 lag0 proxy、或「已解释」——直接 REWORK。
2. **R3 §6.5**：按 GATE 定义 `close(D−1)` 重报 ≥97%；转移日 100%。远距对向三日（#10958 / #11068 / #13283）必须有可证伪解释（原文时刻 / 作者平台价 / 抽标错误并改 v1.2，数值列 diff 仍须空）。近轨 24 日若仍靠公开所，须证明不是「所间翻类」（该路已死）。
3. D1 TV live 仍是 `replica_shadow` 入场债；D2/D3 顺序不变。

满足 1–2 且数字落在门槛内 → 下一票可裁「研究包证据 PASS（票面仍 REWORK 直到 D1 / D3）」。**任何一条以「数据源不同」「时间不够」「公开代理不可约」为由放宽 → 直接 REWORK。**

---

## 8. 对 GATE §9 置信表的影响（记录，不改 GATE 正文）

| GATE §9 结论 | r2 后 | 本次证据 | 走向 |
|---|---|---|---|
| H1 = EMA(H/L) 族正确 | 再上调；缺三所 | 三所 V 形同现 N=33；RMSE 0.05–0.07% | **再上调（族）**；replica 放行仍被留出挡住 |
| N≈30 → N=33 | Bitstamp 确认 | 三所同谷 33 | **确认到三所** |
| §6.3 留出 ≤1.5× 可达 | 待 OKX 实验 | 三所半根全 FAIL；基差假说证伪 | **改为：H1+半根+公开三所不可达**；族未推翻 |
| 抽取半部 · 标签 | REWORK | 72.20%、diff 空、锚点、clear 语义 | **标签列 PASS（v1.1）** |
| 总判 REWORK | 0.96 | 两项最低门槛仍 FAIL | **REWORK (narrowed) 0.95** |

---

## 9. 本文数字的复现协议

- 主证据：申请包 jsonl/JSON（sha 见文首）。不入库。
- 标签：逐行读 v1 与 v1.1；数值 11 键相等；`stated_*` 计数；连续 `clear` = 当前 action 为 clear 且上一非空 action 为 clear。
- N 表：每所 `full_N_scan` 长度 26、集合 {20…45}、argmin RMSE、N±1 相对增幅。
- 留出：`ratio = test.rmse_pct / train.rmse_pct`，与字段 `ratio_test_over_train` 对拍。
- §6.5：199/234、42/56；错配 35 行 × 三所 class 集合大小；距最近轨 = 在轨内取 min(U−px, px−L)/mid，在轨外取越距/mid。
- 市场数据：Bitstamp 公开日线 `ohlc/btcusd` step=86400，仅核 35 个 dm1 close。无小时线，无三所重拉。
- 半根构造、Donchian 窗口、§6.9 端点：不本轮重算，沿用 r2。

---

## 10. 非目标

- 不代拉 OKX/Coinbase/Binance 小时线，不代做标签原文审计，不代生成 `research/` 交付物。
- 不裁 N 终值、不裁 `venue_set`、不确认作者公式、不宣布 H1 族死亡。
- 不改 GATE r3 阈值与定义；§6.5 价格参照留 GATE r4。
- 不评估 IMPL-GATE r3 三注入。
- 不涉及下单、仓位、`system_signal`。
- **不改业务代码。** 本文是唯一新增文件。

---

## ACK

```text
HANDOFF
from: architect
to: research-executor
intent: ACK
thread_ref: GATE-laomao-truth-channel-fit-2026-09-21-r3
engine: grok-4.6 xhigh (Fable quota exhausted; Jimmy-authorized backup)
verdict: REWORK (narrowed; not Conditional PASS / PASS / REFUSE)
cleared:
  - R2 labels: CLEARED — stated_position 296/410=72.20%; numeric-column diff 0/410; #10962 touching / #10968 holding; 58 repeat-clear -> null (14 remain, 0 consecutive repeats)
  - R4 three-venue halfbar N 20-45: CLEARED — single valley N=33 x3; N+-1 +98%..+266% (table-internal; no hourly re-pull)
  - R5 venue_selection.md: CLEARED — stale 0.156/0.155/0.167/n=916 gone; numbers match scan+holdout JSON
  - S1 post_hour_open: CLEARED — price_vector sha 531b66bc != 413f9d00; 91.03% != 85.04%; assert true
still_open_hard:
  - R1 sec 6.3 2023 holdout: KEEP HARD — 2.038 / 2.083 / 1.571 all FAIL; N*=33; USD/USDT basis FALSIFIED; NOT debt; NOT family-falsified (RMSE 0.05-0.07, V@33 holds; GATE §9 overturn unmet). Structural-fail dossier accepted. Binance halfbar still allowed as last same-family venue (same-venue full table only); else §6.7 H3/H4/H5. Do not widen 1.5x.
  - R3 sec 6.5: KEEP HARD — 199/234=85.04% <97%; transition 42/56=75% <100%; H1==oracle so not family-falsified; venue-class-flip FALSIFIED (0/35). 24/35 near-rail; 3 far opposite (#10958 6.01%, #11068 5.31% new-label, #13283 1.76%). Bitstamp daily spot-check 35/35 D-1 closes exact. Author-platform caveat does not waive 97%.
deferred_debt: D1 TV live sec 6.8 (hard before replica_shadow); D2 Layer 2; D3 sec 6.9 injections
soft: compare_summary.json; SHA list; corpus re-audit of +68 labels (no corpus this round); 4th venue if they still want H1-internal last try; S2-S6 leftovers
effects:
  - L0 numeric: PASS remains; rails.jsonl sha 4740a4a6... frozen
  - L0 labels: PROMOTED to PASS; v1.1 sha 45e061c6... is stated_* scoring target; do not rewrite v1
  - H1: formula_status=hypothesis; STILL NOT in brief/JSON/history; no replica_shadow
  - proxy / last_btc_consensus.json (sha 594a20a7... before==after) / brief channel line / schema_version 3: STILL DO NOT TOUCH
not_granted: model-half Conditional PASS; family falsification of H1; converting R1/R3 to debt; any threshold widening
next_gate: sec 7 items 1-2 within sec 6.3 / 6.5 thresholds -> RECHECK r4
```

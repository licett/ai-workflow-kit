REWORK (narrowed)

# RECHECK r4 residual：老猫真值通道 GATE r3 — 只验 §6.3 holdout + §6.5（架构师裁决）

> 裁决：**REWORK (narrowed)**。不是 Conditional PASS，不是 PASS，不是 REFUSE。engine = **grok-4.6 xhigh**（Fable / cloud 额度耗尽，Jimmy 授权备用引擎）。对照 prior RECHECK r3（PR [#11](https://github.com/licett/ai-workflow-kit/pull/11)）留下的两项硬挡：申请方本轮交了第 4 所 Binance BTCUSDT 半根同管线全表，以及 v1.2 标签洗 18 条 + 转移日 ±1 bar。本文以申请包 JSON/jsonl 为主证据独立复算后：**§6.3 钉 Binance 为 H1 评分主所 → PASS**；**§6.5 转移日子项 CLEARED**；**§6.5 总体 90.91% < 97% 维持硬挡**。阈值一条不放宽。票面因此仍是 REWORK，范围再收窄到 §6.5 总体 97% + 既有入场债（§6.8 TV live / Layer 2）。`formula_status` 仍为 `hypothesis`；**H1 仍不得进 brief / JSON / history**。Donchian proxy brief、`last_btc_consensus.json`、brief 通道行、`schema_version: 3`：**一律仍禁止动**。不授予模型半部 Conditional PASS。
> 对照物：`uploads/REWORK-CLEARANCE-r3.md`（sha `18efb9b9…`）、`RECHECK-REQUEST.md`（`501335ec…`）、`RECHECK-prior-r3.md`（`94218192…` = PR #11 正文）、`GATE-laomao-truth-channel-fit-2026-09-21.md` r3（`3d855b65…`，PR [#8](https://github.com/licett/ai-workflow-kit/pull/8)，与 r2/r3 同一份）、`venue_selection.md`（`0897bbfb…`，**仍写 bitstamp primary、正文无 binance**）、`truth_series/rails.jsonl`（**`4740a4a6…`，410 行 = L0 v1 冻结**）+ `rails_v1.2_labels.jsonl`（**`75fe3cef…`，410 行**）、`out/`：`binance_halfbar_sec63_r3` `a3fc7d6d…` / `holdout_forensics_r3` `0c4b3233…` / `sec65_stated_position_r3` `9affce3e…` / `sec65_transition_rows_r3` `99c1bc70…` / `labels_v1_2_summary` `34f3fb5d…` / `residual_r3_summary` `b817c8cb…`。
> 方法：以申请方 JSON/jsonl 为主证据；在 `/tmp` 独立复算标签覆盖、数值列 diff、Binance N 20–45 V 形、留出比值、§6.5 算术与多所错配结构（不入库）。**禁止全量小时线重拉**（半根构造正确性沿用 r2 §1 / r3 §1.2；本轮不重做）。**最多一次**公开日线小抽检：对 21 个 §6.5 剩余不一致日的 `close(D−1)`，Bitstamp BTC/USD **21/21 绝对相等**，Binance BTCUSDT（`data-api.binance.vision`）**21/21 逐分相等**。证据标准与 r3 相同且不对称：本文复算足以否决一个数字，也足以确认申请方交付物与其声明一致；放行仍以申请方带 sha 的 `research/` 产物为准。不改 py / README / JSON / history / brief；不产出 `system_signal`。
> 边界：research-only。本文只新增此一文件；不授权 promote、不授权 `replica_shadow`、不改 GATE 任何阈值与定义。r1/r2 留给 GATE r4 的定义问题（§6.5 价格参照、§6.9 缺口端替代）本文仍不裁。
> 日期：2026-09-21（Asia/Shanghai）。thread_ref = `GATE-laomao-truth-channel-fit-2026-09-21-r3`。本票 = RECHECK r4。

---

## 0. 总判

| 项 | r3 裁决 | **r4 裁决** | 一句话 |
|---|---|---|---|
| 研究包整体（票面） | REWORK（narrowed） | **REWORK (narrowed)** | §6.3 清且钉 Binance 主所；§6.5 转移清；§6.5 总体 90.91% 仍 FAIL → 票面仍 REWORK，范围再收窄 |
| L0 数值轨位列 | PASS · L0 v1 冻结 | **PASS 维持** | sha `4740a4a6…` 与 r3 冻结值逐字节相同；v1.2 数值列 diff 空（0/410） |
| L0 标签列（`stated_*`） | PASS · L0 v1.1 | **PASS · 评分靶升 v1.2** | `stated_position` 296/410 = **72.20%** ≥70% 维持；18 条洗标新值 18/18 落在 v1.2；禁止回写 v1 |
| 模型半部 H1 | REWORK（留出 + §6.5 + §6.8） | **REWORK 维持，再收窄** | §6.3 **PASS（Binance 同所全表）**；§6.5 转移 **CLEARED**；§6.5 总体仍硬挡；§6.8 仍债 |
| §6.3 2023 留出 | 硬挡（三所 2.038 / 2.083 / 1.571） | **CLEARED · PASS（Binance 主所）** | 旧三所半根仍 FAIL，归档为负对照；**不**把 lag0/lag1 或跨所拼表当过闸路径 |
| §6.5 ≥97% | 硬挡（85.04%） | **维持硬挡**（90.91%） | 210/231；过闸要 **225/231**（再消化 15 个），224/231=96.97% 仍不过。作者平台 caveat **不**豁免 |
| §6.5 转移日 100% | 硬挡（75%） | **CLEARED** | ±1 bar（D−1 / D / D+1）**56/56 = 100%**；严格 D−1 仍 50/56=89.29%，GATE 允许 ±1，不回滚 |
| Donchian proxy / consensus / brief 通道行 / schema 3 | 仍禁止动 | **仍禁止动** | 本文不授权任何一项 |
| `formula_status` | `hypothesis` | **`hypothesis` 不变** | §6.5 总体未过、§6.8 未做 → 不得升 `replica_shadow` |
| 模型半部 Conditional PASS | 未授 | **仍不授** | 97% 开着就把模型半部改 Conditional PASS = 改宽。禁止 |

置信度：票面 REWORK (narrowed) 0.96；§6.3 Binance 全表自洽 0.93（未重拉小时线）；钉 Binance 为 H1 评分主所 0.88；§6.5 90.91% FAIL 0.98；转移 100% 0.97；v1.2 数值冻结 + 18 条新值落地 0.97；H1 仍禁 brief 0.99；H1 族未被证伪 0.91（GATE §9 推翻条件仍未触发）。

---

## 1. 本轮范围与不重开项

r3 §7 下次申请门槛只列两项硬项。本文**只裁这两项**：

1. R1 §6.3 留出：第 4 所 Binance 半根同管线 2023 折 ≤1.5，且**同一所**重报 §6.3 全表。
2. R3 §6.5：`close(D−1)` ≥97%；转移日 100%；r3 点名的远距对向三日须有可证伪解释。

以下 r3 已 CLEARED 项**不重开**：R2 标签覆盖闸、R4 三所半根 N 表、R5 `venue_selection.md` 伪影删除、S1 `post_hour_open` 诊断分流。D1 TV live / D2 Layer 2 / D3 §6.9 注入仍是入场债，本票不验。

申请方自己的预期与本文一致的部分：不申请 Conditional PASS；不主张放宽 97%；旧三所不改判 PASS。申请方主张「§6.3 已 CLEARED、请裁是否钉 Binance 主所」——本文裁 **钉**，见 §2。

---

## 2. §6.3：PASS（钉 Binance BTCUSDT 为 H1 评分主所）

### 2.1 闸门数字（申请包 train/test 复原，逐位对拍）

来源：`out/binance_halfbar_sec63_r3.json`（venue=`binance`，alignment=`halfbar_12utc`，n_daily=1276，n_partial=942，与旧三所日历窗同构）。`full_N_scan` 26 点，集合 {20…45} 无缺。未重拉小时线；表内自洽。

| 指标 | Binance halfbar N=33 | 本文复算 | 闸 | 过？ |
|---|---:|---:|---|:---:|
| pooled RMSE%（n） | 0.0210769（n=404） | 同；年合计 159+136+109=404 | ≤0.20 且 n≥400 | ✓ |
| \|bias_U\| / \|bias_L\| % | 0.005926 / 0.002577 | 同 | ≤0.05 | ✓ |
| 逐年 RMSE% 2023/24/25 | 0.020784 / 0.017651 / 0.025054 | 同 | 每年 ≤0.30 | ✓ |
| max \|resid\| % | 0.292206 | 同 | ≤1.0 | ✓ |
| 参数稀疏 | 全期 N=33 | `best_N=argmin=33` | 全期单一 (N,α) | ✓ |
| N±1 V 形 | 宣称 +715% / +691% | **+715.376% / +691.080%**（N32=0.171856，N34=0.166735） | ≥30% | ✓ |
| 留出 2023 固定 N=33 | 0.977391 | 0.020784/0.021265 = **0.9773907309869311** 与字段逐位相同 | ≤1.5 | ✓ |
| 留出 2024 / 2025 | 0.780381 / 1.291256 | 逐位相同 | ≤1.5 | ✓ |
| 2023 训练窗重选 N* | 33（比值不变） | `remedies.binance.refit_N.N_star=33` | 同所、同 N | ✓ |

同所规则：上表全部行来自 Binance，无跨所拼 RMSE / 拼留出。四所均值 ensemble 2023 折 **1.6407 仍 FAIL**——申请方自己的表关掉了「掺进来凑过闸」。

旧三所半根 N=33、2023 折**未变**，维持 FAIL：

| Venue | 2023 ratio | ≤1.5？ |
|---|---:|:---:|
| bitstamp (USD) | **2.038421** | FAIL |
| okx (USDT) | **2.083407** | FAIL |
| coinbase (USD) | **1.570945** | FAIL |
| **binance (USDT)** | **0.977391** | **PASS** |

`holdout_forensics_r3.pass_paths` 里旧三所的 `lag0_fullbar` / `lag1_fullbar` **仍拒绝**（r3 已裁：不得回收已 FAIL 三所的整根对齐当过闸路径）。Binance 自己的 lag0/lag1 数字存在但不作为本票过闸依据——过闸对齐钉死 `halfbar_12utc`。

### 2.2 是否钉 Binance 为 H1 主所：**钉（评分主所，research-only）**

GATE §5.3 / §2.4 原文就是「≥4 所、取残差最小者」。r3 §3.3 预留的族内最后一试正是：「另交与本管线同预热的 Binance 半根且 2023 折 ≤1.5，允许按同一所出全部行重报 §6.3 全表」。两条都落到门槛内。

| 问 | 裁 |
|---|---|
| §6.3 是否 PASS？ | **是。** 评分所 = Binance BTCUSDT，`halfbar_12utc`，N=33。阈值未放宽。 |
| 是否钉为 H1 主所？ | **是，仅限研究评分 / `params_version` 主所字段。** 不是生产 `venue_set` 终裁，不是 brief 换行，不是 `formula_status` 升级。 |
| 是否因此 promote H1？ | **否。** §6.5 总体未过、§6.8 未做 → `hypothesis` 不变，H1 仍禁 brief / JSON / history。 |

钉所的依据（任一即够，三条同时成立）：

1. **闸门全表同所过**（§2.1）。
2. **残差最小**：Binance pooled 0.0211% vs okx 0.0507 / coinbase 0.0651 / bitstamp 0.0725（r3 已 CLEARED 的三所半根表）。约 2.4–3.4 倍，不是印差噪声。
3. **与 GATE 先验同向**：§2.4 写过「老猫 2023 大概率看 USDT 对（Binance / OKX / Huobi）」。OKX 半根留出更差（2.083，基差假说 r3 已证伪）；Binance 过闸。2023 月 RMSE Binance 0.002–0.042、近零 bias，而 Bitstamp 3 月 0.226、H1 0.131——结构日历压力打在 USD 所，不打在 Binance USDT 半根。

### 2.3 切换条件 / 文书（钉所的后果，不是回滚 §6.3）

§6.3 数字过闸**不依赖** `venue_selection.md` 先改写。但钉所之后该文件**立即过期**（仍写 `Primary: bitstamp`，全文检索无 `binance`）。下一包必须改，否则按 r2/r3 R5 同类文书硬挡处理。

| # | 条件 | 状态 |
|---|---|---|
| C1 | 评分表只出 Binance `halfbar_12utc` N=33；禁止跨所拼行 | **本票已满足** |
| C2 | 旧三所 lag0/lag1 / ensemble /「已解释所以 ≤2.08」不得再报为过闸路径 | **本票重申；再报直接 REWORK** |
| C3 | 重写 `venue_selection.md`：Primary = **binance BTCUSDT**；Confirm = bitstamp + okx + coinbase（只证 N=33 V 形，不证留出）；单列「2023 holdout FAIL 归档」表（2.038 / 2.083 / 1.571）；删任何把 bitstamp 当评分主所的句子 | **下一包硬文书** |
| C4 | 若将来写 `params_version`：主所字段必须是 binance，形如 `ema_hl-33-halfbar_12utc-binance-<sha8>` | 未写；预置 |
| C5 | §6.8 TV 复现（入场债）symbol 预置 `BINANCE:BTCUSDT`，时区 UTC | 未做；不本票验收 |
| C6 | 不把钉所写成生产切换、brief 换行、或 `replica_shadow` 入场 | **本票禁止** |

软项（不回滚 §6.3）：JSON 只显式给了 **2023** 训练窗 `refit_N`（N*=33）。2024/2025 训练窗 N* 申请方宣称 33/33，但 `holdout_forensics` / `binance_halfbar_sec63` 没有分年 `refit_N` 块。V 形两侧 RMSE 约 8 倍，子集再选到 33 几乎必然；且 GATE 参数稀疏本就是全期单一 N，固定 N=33 三年留出都 ≤1.5。下一包补两行即可，不构成硬挡。

### 2.4 旧三所如何归档

不是删除，不是改判 PASS，不是「待解释」。

| 对象 | 归档身份 | 以后可以做什么 | 禁止 |
|---|---|---|---|
| bitstamp / okx / coinbase 半根 N=33 全表 | **负对照 + N 确认所** | 继续引用 r2/r3 已 CLEARED 的 V@33；解释「为何不是评分所」 | 再扫 N、再用 lag0/lag1、再拿 2024/25 留出过闸来冲 2023 FAIL |
| 三所 2023 折 2.038 / 2.083 / 1.571 | **结构 fail 卷宗（冻结）** | 与 Binance 0.977 对照，证明所选择而非阈值 | 把 1.5× 改成「三所均值」或「最好的 FAIL 所」 |
| USD/USDT 基差假说 | **已证伪（r3，维持）** | — | 重开 |
| Kraken | report-only 不变 | — | 从它选 N |

冻结指针：`out/holdout_forensics_r3.json` sha `0c4b3233…`；`venue_selection.md` 现稿 sha `0897bbfb…` 只保留到 C3 重写之前，作为「钉所前最后一版 bitstamp-primary」。

**§2 结论：R1 CLEARED。§6.3 PASS。钉 Binance BTCUSDT 为 H1 评分主所。旧三所 FAIL 归档。不 promote。**

---

## 3. §6.5：总体维持硬挡；转移日子项 CLEARED

### 3.1 闸门数字（本文复算算术）

GATE 定义重读：`stated_position` ∈ {above,inside,below} vs classify(close(D−1), rails(D))；touching 排除在分母外；一致率 ≥97%；转移日（holding/action 变化，含 CARD 锚点）方向一致 **100% 在 ±1 bar 内（D−1, D, D+1）**。作者平台 caveat **不**豁免 97%。

| 项 | 申请方 | 本文 |
|---|---|---|
| v1.2 `close(D−1)` vs oracle | 210/231 = 90.91% | **210/231 = 90.909090…%**；错配列表 21 条 |
| 同口径 vs H1 | 210/231 | 与 oracle **同一 n、同一 agree**（`h1_same_as_oracle=true`） |
| ≥97% | FAIL | **FAIL** |
| 过闸最少同意数 | CLEARANCE 写 ≥224/231（消化 14）；JSON ceiling 写 ≥225（消化 6） | **224/231 = 96.9697% < 97% 仍 FAIL**；**225/231 = 97.4026% 才过**；从 210 起须再消化 **15** 个。CLEARANCE 的 224 与 JSON 的「消化 6」都是申请方算术错，**不改变 FAIL** |
| 转移日严格 D−1 | 50/56 = 89.29% | **agree 50 / disagree 6 / skipped_no_pos 44**；disagree = {#10986, #11034, #11040, #11167, #11368, #15961} |
| 转移日 ±1 bar | 56/56 = 100% | **disagree 0**；`n_eval=56`；**PASS** |
| `post_hour_open` 诊断 | 96.97% | 224/231；sha `adae2b95…` ≠ 闸门 sha `64dd40e2…`；断言 true。**仍只是诊断，不改 97%** |
| 作者平台 caveat | 不可得 | 接受「不可得」为事实；**不接受**「因此放宽 97%」 |

评分子 234→231：v1.2 三条洗成 touching（#10958 / #13101 / #13283）出分母，234−3=231。可评分标签 {above,inside,below}=233，其中 2 条带 `anomaly_flags`（#11407 / #12126）不计分 → 231。自洽。

### 3.2 v1.2 洗 18 条 — 数值冻、新值落地（标签靶升，不回滚覆盖闸）

| 检验 | 结果 |
|---|---|
| 行数 / 唯一日 / 唯一 `message_id` 单调 | 410 / 410 / 是 |
| 数值 11 键 vs L0 v1 | **0 / 410** |
| `stated_position` 非空 | **296 / 410 = 72.195%** ≥70% |
| 分布 v1.2 | above 105 / below 68 / inside 60 / touching 63 / null 114 |
| 相对 v1.1 分布（r3：115/73/48/60/114） | 恰为 18 条洗标的枚举位移（验算闭合） |
| `stated_holding` 非空 | **277 / 410** ≥50% |
| `clear` / 连续重复 | 14 / **0** |
| 18 条宣称 `new` 是否都在 v1.2 | **18 / 18**（#11068、#13170 在 v1 为 null，属 v1.1 新标再洗；其余 16 条 v1 已非空） |
| `sender_id` / `rail_source` / `formula_status` | 5129397609 ×410 / oracle ×410 / null ×410 |
| 异常集合 | {11029, 11136, 11407, 12126, 13503, 13752} 未变 |
| `upper≤lower` | 0 |

L0 标签评分靶：**从 v1.1（`45e061c6…`）升为 v1.2（`75fe3cef…`）**。数值列仍只认 v1 `4740a4a6…`。禁止把 v1.2 写回 v1。撤回规则同 r3：日后抽检标签与原文不符 → 只撤标签列 PASS；数值改写或 `sender_id` 混入 → 按 GATE §9 撤数值列 PASS。本轮未上传语料，18 条原文核对列为软项，不回滚覆盖闸。

r3 点名的远距对向三日，走的是「抽标错误并改 v1.2」路径，且已离开错配表：

| message_id | v1.1 | v1.2 | 仍在 21 错配？ |
|---|---|---|---|
| #10958 | below（条件句「一旦跌破下轨」） | touching | 否（出分母） |
| #11068 | below（条件句「只要不跌破」） | above | 否 |
| #13283 | above（条件句「上则站上通道」） | touching | 否（出分母） |

接受这三日的洗标为 r3 §7.2 的可证伪解释。**不**把洗标当成 97% 已过。

### 3.3 剩余 21 个错配：近轨 18 / 远 3 / 翻类 0 / 对向 0

CLEARANCE 写「近 17 / 远 4（含 #13124 1.03%）」——**以 JSON 与独立复算为准，否决这句**：`multi_venue_mismatch_explain` 与用 Bitstamp `px/upper/lower` 重算的距最近轨 % 都是 **18 近 / 3 远**。#13124 距上轨 **0.9705% < 1%**，算近轨。

远 3（均非 above↔below 对向）：

| message_id | 日 | stated | class | 距最近轨 % |
|---|---|---|---|---:|
| #10979 | 2023-05-23 | inside | below | 1.130 |
| #10997 | 2023-06-16 | inside | below | 2.384 |
| #11167 | 2024-04-02 | inside | above | 3.571 |

四所 `*_class` 在 21/21 日完全相同（Bitstamp=OKX=Coinbase=Binance）。所间翻类维持证伪（0/21）。H1 与 oracle 同意率相同 → 90.91% 缺口仍是 **stated_position × 公开 close(D−1) × 真值轨** 三角，**不是模型族证伪**。

本轮日线抽检（唯一市场数据动作；无小时线）：21 个错配日的 `close(D−1)`——Bitstamp **21/21 绝对相等**，Binance **21/21 逐分相等**。错配表上的公开收盘不是编造数。公开四所已经穷尽「换所翻类」；剩余近轨子集仍要作者平台或 GATE r4 改定义（本文不裁）；3 个远日要标签/时钟审计。在数字落到 225/231 之前，票面不得过。

### 3.4 转移日：CLEARED

GATE 写的是「方向一致率 100%（±1 bar 内）」，不是「必须严格 D−1 的 100%」。±1 = {D−1, D, D+1} 已在 r3 钉死。本票 56/56、`transition_v1_2_disagree_rows=[]`。

CARD 锚点：#10961 / #10968 / #10983 / #15960 / #15966 在评分子内且 **agree**（r3 的 #10968 / #15960 不同意已随 v1.2 洗掉）。#10962 `touching` 按定义 skip；#10964 无 holding/action 变化，不进转移日集合。不回滚。

严格 D−1 的 6 个 disagree 与总体错配表重叠，属于 97% 硬挡的子集，**不是**转移日子项的残留。

### 3.5 三项选项的裁断（总体 97%）

| 选项 | 裁断 | 理由 |
|---|---|---|
| **维持硬挡** | **是** | 97% 是 GATE §6.5 最低门槛。90.91% 不是「差一点就算过」。诊断 96.97% 更不是闸门。 |
| 改债 | **否** | 把 97% 降成 `replica_shadow` 入场债 = 改宽。作者平台不可得从 r1 起就是 caveat，从来不是豁免。 |
| 模型族证伪 | **否** | H1=oracle=90.91%。§6.5 FAIL 不打击「EMA(H/L) 是否生成真值轨」。 |
| 模型半部 Conditional PASS | **否** | 申请方未申请；r3 已禁；一半过一半不过改 Conditional = 改门槛。 |

**§3 结论：R3 总体 97% 维持硬挡。转移日子项 CLEARED。v1.2 标签靶可升。不改债。不证伪 H1 族。不授 Conditional PASS。**

---

## 4. H1 仍禁 brief；proxy / consensus 禁动

### 4.1 H1：**仍禁止进 brief / JSON / history**

`formula_status = hypothesis` 不变。不授权 `replica_shadow`。理由任一即足：§6.5 总体 FAIL、§6.8 未做。本轮对 H1 的正面效力只在证据链：评分主所换成 Binance 后 §6.3 全表成立；族仍未被证伪（pooled RMSE 0.021% ≪ 0.20%，V@33 更尖；GATE §9 推翻条件未触发）。

钉主所 **≠** 放行 replica。`system_signal_eligible` 仍是常量 `false`。k = 0.018958 仍禁绑。

### 4.2 proxy / consensus：**禁动**

| 对象 | 状态 |
|---|---|
| Donchian proxy brief / IMPL-GATE r2 PASS 面 | **仍禁止动** |
| `data/last_btc_consensus.json` | **仍禁止写**（申请包 sha `594a20a7…` before == after） |
| brief 通道行 | **仍禁止换行**；不得并列两条 |
| `schema_version: 3` / replica 块 / replica 进 history | **不授权** |
| GATE r3 全部阈值与定义 | **一字不改** |

---

## 5. r3 residual 勾表（本票只动两项硬项）

| # | r3 分类 | **r4** | 依据 |
|---|---|---|---|
| R1 §6.3 2023 留出 | 硬挡（取证齐；等第 4 所） | **CLEARED · PASS**（Binance 同所全表；钉评分主所） | §2 |
| R3 §6.5 ≥97% | 硬挡 | **STILL_OPEN · 硬挡**（210/231=90.91%；须 225/231） | §3.1 / §3.3 |
| R3 §6.5 转移 100% | 硬挡（并在 R3 里） | **CLEARED**（56/56 ±1 bar） | §3.4 |
| R2 / R4 / R5 / S1 | 已 CLEARED | **不重开** | r3 |
| D1 §6.8 TV live | 可债 | **DEFERRED** 不变；symbol 预置 BINANCE:BTCUSDT | §2.3 C5 |
| D2 Layer 2 ≥14d | 可债 | **DEFERRED**（顺序仍对） | — |
| D3 §6.9 三注入 | 可债 | **DEFERRED**（IMPL-GATE r3） | — |
| 文书 C3 `venue_selection.md` 钉所 | — | **下一包硬文书**（不回滚已过的 §6.3） | §2.3 |

---

## 6. 下次申请门槛（RECHECK r5；只列未齐硬项；阈值一条不减）

1. **R3 §6.5 总体**：按 GATE 定义 `close(D−1)` 重报 **≥97% = 至少 225/231**（或同分母下的等价分数）。作者平台 caveat、诊断 `post_hour_open`、近轨、公开所印差——**一律不改门槛**。远 3 日（#10979 / #10997 / #11167）须有可证伪解释（原文时刻 / 作者平台价 / 再洗 v1.3 且数值列 diff 仍空）。近轨 18 日不得再走「所间翻类」（该路已死，0/21）。
2. **C3 文书**：重写 `venue_selection.md` 使 Primary=binance，并归档旧三所 2023 FAIL（§2.3 / §2.4）。缺此文件的下一包，按文书硬挡处理；**不**据此回滚本票 §6.3。
3. D1 TV live 仍是 `replica_shadow` 入场债；D2/D3 顺序不变。

满足 1（数字落到门槛内）且 2 已交 → 下一票可裁「研究包证据 PASS（票面仍 REWORK 直到 D1 / D3）」。**任何一条以「数据源不同」「时间不够」「公开代理不可约」为由放宽 → 直接 REWORK。** 再申请模型半部 Conditional PASS 而 97% 仍开着 → 直接 REWORK。

---

## 7. 对 GATE §9 置信表的影响（记录，不改 GATE 正文）

| GATE §9 结论 | r3 后 | 本次证据 | 走向 |
|---|---|---|---|
| H1 = EMA(H/L) 族正确 | 再上调；留出挡 replica | Binance 同所 RMSE 0.021%、V@33 两侧 +691–715%、三年留出 ≤1.5 | **再上调（族 + 所）**；replica 放行改由 §6.5 / §6.8 挡 |
| N≈30 → N=33 | 三所同谷 | 第 4 所同谷 33，且更尖 | **确认到四所** |
| §6.3 留出 ≤1.5× 可达 | 「H1+半根+公开三所不可达」 | 第四所可达（0.977）；旧三所不可达维持 | **改为：评分主所 = Binance 时可达；旧三所仍不可达** |
| 抽取半部 · 标签 | PASS v1.1 | v1.2 18 洗、diff 空、72.20% | **评分靶升 v1.2** |
| 总判 REWORK | 0.95 | 97% 仍 FAIL | **REWORK (narrowed) 0.96** |

---

## 8. 本文数字的复现协议

- 主证据：申请包 jsonl/JSON（sha 见文首）。不入库。
- 标签：逐行读 v1 与 v1.2；数值 11 键相等；`stated_*` 计数；18 条 `new` 与 v1.2 对拍；连续 `clear` = 当前 action 为 clear 且上一非空 action 为 clear。
- Binance N 表：`full_N_scan` 长度 26、集合 {20…45}、argmin RMSE、N±1 相对增幅 = `rmse(N±1)/rmse(33) − 1`。
- 留出：`ratio = test.rmse_pct / train.rmse_pct`，与字段 `ratio_test_over_train` 对拍（2023/24/25 均逐位相同）。
- §6.5：210/231、56/56、50/56；错配 21 行 × 四所 class 集合大小；距最近轨 = 在轨内取 min(U−px, px−L)/mid，在轨外取越距/mid；97% 用 `agree/n ≥ 0.97`（故 224 不过、225 过）。
- 市场数据：Bitstamp 公开日线 `ohlc/btcusd` step=86400 + Binance `data-api.binance.vision` `klines` interval=1d，仅核 21 个 dm1 close。无小时线，无全量重拉。
- 半根构造、Donchian 窗口、§6.9 端点：不本轮重算，沿用 r2。

---

## 9. 非目标

- 不代拉全量小时线，不代做 18 条标签原文审计，不代生成 `research/` 交付物，不代改 `venue_selection.md`。
- 不裁生产 `venue_set` 终值、不确认作者公式、不宣布 H1 族死亡。
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
  - R1 sec 6.3: CLEARED / PASS — Binance BTCUSDT halfbar_12utc N=33 same-venue full table (pooled RMSE% 0.0211 n=404; |bias| 0.0059/0.0026; yearly 0.0208/0.0177/0.0251; max|resid| 0.292; V@33 +715%/+691%; holdout 2023/24/25 = 0.977/0.780/1.291; N*2023=33). PIN binance as H1 scoring primary (research-only).
  - R3 sec 6.5 transition: CLEARED — 56/56 = 100% within ±1 bar (D-1,D,D+1). Strict D-1 50/56 remains diagnostic. CARD eval anchors agree.
  - labels v1.2: scoring target promoted — 18/18 new values present; numeric-column diff 0/410; stated_position 296/410=72.20%; do not rewrite v1
still_open_hard:
  - R3 sec 6.5 overall: KEEP HARD — 210/231=90.91% <97%; need ≥225/231 (digest 15). 224/231=96.97% still FAIL (CLEARANCE "224/14" and JSON ceiling "digest 6" are applicant arithmetic errors, not a waiver). H1==oracle so not family-falsified; venue-class-flip FALSIFIED (0/21). near=18 / far=3 (#10979 1.13%, #10997 2.38%, #11167 3.57%) / opposite=0. Washed r3 far-opposite #10958/#11068/#13283 accepted. Bitstamp+Binance daily spot-check 21/21 D-1 closes exact. Author-platform caveat does not waive 97%.
archived:
  - old three venues 2023 holdout FAIL 2.038 / 2.083 / 1.571 — negative-control + N-confirm only; do not recycle lag0/lag1/ensemble as pass path
deferred_debt: D1 TV live sec 6.8 (hard before replica_shadow; symbol preset BINANCE:BTCUSDT); D2 Layer 2; D3 sec 6.9 injections
next_doc_hard: rewrite venue_selection.md Primary=binance and archive old-three FAIL (does not un-PASS sec 6.3)
soft: 2024/2025 N* refit rows missing in JSON (fixed-N already passes); corpus re-audit of 18 washes (no corpus this round)
effects:
  - L0 numeric: PASS remains; rails.jsonl sha 4740a4a6... frozen
  - L0 labels: scoring target = v1.2 sha 75fe3cef...; do not rewrite v1
  - H1: formula_status=hypothesis; STILL NOT in brief/JSON/history; no replica_shadow; scoring primary = binance (not a promote)
  - proxy / last_btc_consensus.json (sha 594a20a7... before==after) / brief channel line / schema_version 3: STILL DO NOT TOUCH
not_granted: model-half Conditional PASS; family falsification of H1; converting 97% to debt; any threshold widening; production venue switch
next_gate: sec 6 items 1-2 within sec 6.5 97% + venue_selection rewrite -> RECHECK r5
```

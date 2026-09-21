REWORK

# GATE：老猫 2.0 真值趋势通道重建 — 路径 A「反向拟合平行通道」架构裁决

> 裁决：**REWORK**。路径 A 拆成两半：**抽取半部 PASS**（每日上/下轨「当值」序列即真值，升格为一等产物）；**拟合半部 REFUSE**（「两点定线平行通道 / 徐小明变体」被预览数据证伪，不得以任何拟合结果冒充真值）。重建目标改为**生成模型辨识**（路径 C），路径 B 保留但换关键词。预览级探针已给出一个强候选：**日线 EMA(High, N) / EMA(Low, N)，N≈30–33，UTC 日 bar**，单一交易所数据、单一参数，对 409 日真值 RMSE 0.12–0.30%（§2）；这是待证伪的假设 H1，不是结论。已 PASS 的 Donchian proxy brief 契约（IMPL-GATE r2）**一字不改**；本文只新增契约（§7），不授权任何 brief 换行。
> 对照物：`uploads/REQUEST.md`（下称 REQUEST）；`uploads/IMPL-GATE-r2-PASS.md`（PR [#7](https://github.com/licett/ai-workflow-kit/pull/7)，下称 r2）；`uploads/DESIGN-channel-proxy-v0.md`（下称 DESIGN）；`laomao-trading-framework.md`（下称 FRAME）；`laomao-agent-card.md`（下称 CARD）；`laomao-corpus-summary.json`（416 篇 / 80824 字 / 2022-03-09..2025-06-24）；`samples/rails_extract_preview.jsonl`（410 行，下称 PREVIEW）；`samples/keyword_B_hits.json`（28 条，下称 HITS）。
> 方法：只读 uploads；PREVIEW 在 `/tmp` 做描述统计与模型判别（无代码入库）；**一次**公开只读拉取 Bitstamp BTC/USD 日线 1000 根（2023-01-01..2025-09-26）用于 §2 的模型族探针——这是裁决所需的证据动作，不是实现；未拉分钟/小时线，未碰盒上文件。所有数字可按 §5–§6 协议复现。
> 边界：research-only。本文不改 py / README / DESIGN / JSON / history；不产出任何 `system_signal`；拟合结果在过 §6 闸门之前只能进研究表，不得进 brief。
> 日期：2026-09-21。

---

## 0. 总判

| 项 | 裁决 | 一句话 |
|---|---|---|
| 路径 A · 抽取（corpus → 日期→上/下轨序列） | **PASS** | HITS 28/28 文本内轨位与 PREVIEW 逐字相等；15/15 「上移/下移」方向与抽取差分符号一致；序列本身就是老猫平台当日显示的真值（`is_truth=true`，仅限有帖日期） |
| 路径 A · 拟合（分段线性**平行**通道当真值） | **REFUSE** | 五项硬事实证伪直线模型（§1）：宽度 596–4873 点 / 0.93–6.10%；斜率 52 次翻转其中 33 次为渐变穿零；二阶差分/一阶差分标准差比 0.57（直线+读数噪声应 ≥1.73）；局部直线残差 75% 窗口呈系统性曲率；作者措辞「当值 / 速度增加 / 放缓 / 趋平」描述的是逐日重算的指标值 |
| 路径 B · 关键词佐证 | **必做，换靶** | 「画 / 取点」找不到东西是因为没有画法；改搜指标词汇与作者自述位置标签（§3.4、§5.3） |
| 路径 C · 生成模型辨识（新增） | **REWORK 交付物** | H1 = EMA(H,N)/EMA(L,N)：lag=1（只用已收 bar）N=31 → RMSE 0.303%；lag=0（含当日整根 bar）N=33 → 0.120%；N 扫描呈尖锐 V 形（§2）。须以正确交易所 + 12:00 UTC 半根 bar 快照 + 全语料 + 作者自述标签复核 |
| 平行约束（绝对 / 百分比 / 分段常宽） | **均不得作为约束** | log(width)~log(mid) 斜率 1.10，宽度随价格与波动同涨；「约 1000 点」= 2023 年 27k 价位下的 EMA(H−L)≈3.6%，是快照不是规则。宽度只**测量**、只**报告** |
| proxy 契约 | **不变** | r2 §3 放行文案原样；新增发现记录：Donchian-close N=20 与真值位置一致率 43.8%，宽度中位 12.24% vs 3.64%（§6.6）；不影响 PASS，影响 shadow 的观测靶 |
| brief 换行 | **本票不授权** | 换行条件、字段、模板见 §7；须另开 IMPL-GATE r3 |

置信度：总判 REWORK 0.92；直线模型被证伪 0.95；H1 为正确模型族 0.80（参数 / 对齐 / 交易所待定，见 §2.4 与 §9）；抽取半部 PASS 0.90（预览 28 条抽检，全量抽检在 §6.1）。

---

## 1. 证据：PREVIEW 的五个硬事实

### 1.1 序列本身

| 项 | 值 |
|---|---|
| 行数 / 跨度 | 410 行；2023-03-14 .. 2025-06-24，834 个日历日，覆盖率 49.2% |
| 发帖日 | **只有周一至周五**（82/86/83/81/78），周末 0 行；347 行在 12:xx UTC（北京 20:00），55 行 11:xx，8 行 13–14 |
| 缺口 | 74 个 3 日缺口（周末）；大缺口 5 个：2023-07-07→08-22（46 日）、09-28→10-16（18）、2024-02-08→02-19（11）、**2024-07-22→12-17（148 日）**、2025-01-27→02-05（9） |
| 语料 vs 抽取 | 416 篇主讲人帖、410 行有轨位；密集段 10932..11010 只缺 10959 |
| 一致性 | 无 upper≤lower；无重复日；message_id 单调 |
| 异常 | **13752（2025-02-28）**：lower=95952 → width 892（前后日 3631 / 4147）；§2 候选模型预测该日 lower≈93604。判定为原帖笔误或抽取错位，**不得改数，只能打标** |

周五→周一的上轨位移中位数是相邻单日位移的 **2.68 倍**（n=54）：通道**每个日历日都在动**（含周末），与 A1「UTC 日 bar」一致，也说明通道是日线指标而非只在发帖日更新的手工物。

### 1.2 宽度：既不是常数点数，也不是常数百分比

| 半年 | n | 宽度中位（点） | 宽度中位（%） | 点数区间 | % 区间 |
|---|---|---|---|---|---|
| 2023-H1 | 73 | 988 | 3.54 | 787–1319 | 2.88–5.36 |
| 2023-H2 | 87 | 1022 | 3.17 | 596–1501 | 2.24–3.91 |
| 2024-H1 | 113 | 2475 | 4.23 | 1361–3811 | 2.92–6.10 |
| 2024-H2 | 26 | 2395 | 3.86 | 1885–4224 | 2.92–4.39 |
| 2025-H1 | 111 | 3450 | 3.79 | 892*–4873 | 0.93*–5.39 |

（* 含 13752 异常行。）全样本：均值 2207、中位 2028；`log(width) ~ log(mid)` 斜率 **1.10**；宽度与近 10 帖 |日速度| 相关 0.29。相邻两帖宽度**恰好相等**的只有 2/409，|ΔW|≤20 点的 102/409，中位 |ΔW| = 53 点。「平行」是两条轨用同一平滑参数分别跟随 High / Low 的**表象**，不是几何约束。

### 1.3 速度：连续变化，不是分段常数

两点定线的直线，其每日位移在一段内严格恒定，只在重画点跳变。PREVIEW 不是这样：

| 检验 | 观测 | 直线模型预测 |
|---|---|---|
| 上轨日位移符号翻转（帖间） | 52 / 408；其中 **33 次翻转当帖 \|ΔU\| < 前 5 帖均值一半**（渐减穿零） | 2 年内重画 ≤10 次，且每次跳变 |
| 8 帖窗口内日速度呈单调趋势（\|corr\|>0.6） | 133 / 327 = **41%** | ≈0（重画点除外） |
| 二阶差分 / 一阶差分 标准差比（%） | 0.274 / 0.477 = **0.57** | 直线 + iid 读数噪声 = √3 ≈ **1.73** |
| 一阶差分 lag-1 自相关（全样本） | +0.823（dU）、+0.552（dL） | 段内恒速 + 读数噪声 ≈ −0.5 |
| 同一周内去均值后 lag-1 自相关 | −0.248（66 段，n≈4–5，白噪声小样本偏差即 ≈ −0.25） | ≈ −0.6 至 −0.7 |

作者每天用「上移速度有所增加 / 稍有放缓 / 接近趋平 / 进一步放缓」描述通道，正是一条**逐日重算、速度连续变化**的曲线。例：2023-04-10..04-21 上轨日位移 73→260→171→164→196→133→87→139→15→−13，作者同期措辞「上移速度放缓 … 进一步放缓 … 接近趋平」。

### 1.4 局部直线拟合：能拟合，但拟合的是错的东西

10 帖（≈2 周）滑窗 OLS，n=325 窗：

| 模型 | RMSE %（中位） | p90 | max | 残差与 t² 相关 \|r\|>0.5 的窗口占比 |
|---|---|---|---|---|
| 上下轨各自斜率 | 0.250 | 0.588 | 1.098 | **75%**（中位 \|r\|=0.77） |
| 共享斜率（平行） | 0.269 | 0.640 | 1.101 | 同上 |

平行约束几乎不增加误差（两轨确实同步移动），但残差是**系统性弯曲**而不是噪声。要把直线残差压到 0.1% 以下需要每 3–5 帖一个折点——那已经不是「通道」而是连点。而 28/409 日收盘价距某条轨 <0.3%，正是操作日；0.25% 的直线误差恰好会在这些日子误判。**用直线拟合当真值，比诚实的 proxy 更危险。**

### 1.5 抽取质量（PREVIEW 层面）

- HITS 28 条内文「上轨当值 X … 下轨当值 Y」与 PREVIEW 逐字相等 28/28（含 10960 的「上轨**道**当值」变体）。
- 作者自报「相较昨天整体上移/下移 N 点」15 条，方向与抽取差分符号一致 15/15；数值是粗略整体数（同日两轨位移可差 30–100 点，跨周末帖按日历日折算后 ±50% 内），**只能做符号一致性弱校验，不能做拟合约束**。

---

## 2. 生成模型辨识：预览级探针与假设 H1

### 2.1 探针设置

- 数据：Bitstamp BTC/USD 日线（UTC 日 bar，与 A1 一致），2023-01-01 起 1000 根。**单一交易所，非老猫所用平台**——这是本探针的已知偏差来源。
- 比对：PREVIEW 409 行（剔 13752）。帖在 12:00 UTC 发出，帖中「当值」= 平台上当日（进行中）bar 的指标值。两种对齐：`lag=1` 只用 D−1 及之前的已收 bar；`lag=0` 含 D 整根 bar 的最终 H/L（对 12:00 快照的近似上界）。
- 候选族：SMA / EMA 作用于 High 与 Low；SMA(Close) 双轨；Donchian-close（即 proxy）。N ∈ {5,7,10,14,20,25,30,40,50,60} 粗扫后细扫。
- 指标：上下轨合并 RMSE（% of price）、各轨偏差、逐年 RMSE、最差日、位置一致率。

### 2.2 结果

粗扫前 5（RMSE %，n=409）：EMA(H/L) N=30 lag1 **0.359**；EMA N=30 lag0 0.566；EMA N=40 lag0 1.093；EMA N=25 lag1 1.135；EMA N=40 lag1 1.455。SMA 最好 1.54；SMA(Close) 双轨 2.49；**Donchian-close N=20（proxy）6.57**，上轨偏 +6.0%、下轨偏 −4.1%。

EMA 细扫（α = 2/(N+1)）：

| N | lag=1 RMSE | biasU / biasL | lag=0 RMSE | biasU / biasL |
|---|---|---|---|---|
| 28 | 0.623 | +0.28 / +0.23 | 0.920 | +0.49 / +0.40 |
| 30 | 0.359 | +0.12 / +0.07 | 0.566 | +0.32 / +0.24 |
| **31** | **0.303** | +0.03 / −0.02 | 0.397 | +0.24 / +0.15 |
| 32 | 0.337 | −0.05 / −0.10 | 0.237 | +0.15 / +0.07 |
| **33** | 0.438 | −0.14 / −0.18 | **0.120** | +0.07 / −0.01 |
| 34 | 0.568 | −0.22 / −0.27 | 0.173 | −0.02 / −0.10 |

α 直接扫描（lag=1）最优 α=0.062（N_eq≈31.3）。V 形尖锐：N 偏 5 → RMSE 翻 3–8 倍，这是**单自由参数模型族被正确识别**的形态。

H1 = EMA(H,30) lag1 的残差诊断：|残差| 十分位 [0.05, 0.10, 0.15, 0.20, 0.25, 0.31, 0.38, 0.45, 0.57]%；max 上轨 1.29% / 下轨 1.16%；逐年 RMSE 2023 0.349 / 2024 0.413 / 2025 0.292；最差 8 日：2024-03-18..03-22 五日（历史新高后一周，日内振幅 8–10%）、2023-10-24（+10% 单日）、2024-04-03、2024-12-20——都是日内振幅大、半根 bar 快照与整根 bar 差异最大的日子，指向对齐问题而非模型族问题。候选序列自身位移 lag-1 自相关 0.944（真值 0.823，差额来自作者取整 / 交易所 / 半根 bar）。13752 异常日候选预测 lower≈93604（抽取值 95952），进一步确认该行为异常。

位置一致率（以 Bitstamp close(D−1) 对 rails(D) 分类）：**真值 vs H1：395/409 = 96.6%**，14 处不一致全部是收盘价贴轨日。真值 vs Donchian-close N=20（按 A4 语义：确认 bar D−1，窗口为其前 20 根）：**179/409 = 43.8%**；混淆矩阵（真值→proxy）：above→inside 153、above→above 59、inside→inside 85、below→inside 73、below→below 35、inside→below 4；proxy 判 inside 311/409，真值 inside 89/409；真值 above 召回 27.8%、below 召回 32.4%。

### 2.3 解释

- 上轨 = 日线 High 的 ~30 日指数平均，下轨 = 日线 Low 的同参数指数平均；宽度 = EMA(H−L) ≈ 平均日振幅。2023 年 BTC≈27k、日振幅≈3.7% → ≈1000 点；2024-03 振幅放大 → 3800 点 / 6%；2023-09 缩量 → 600 点 / 2.2%。「约 1000 点平行间距」全部被解释。
- 「通道速度」= α·(H_t − EMA_{t−1})：价格远离通道则加速、靠近则放缓、横盘则趋平——与作者每日措辞一一对应，包括「价格横盘等待趋势主动靠近」（FRAME §3.1 第 3 条）。
- 「收盘写死」= 以 bar 收盘价对 bar 收盘时的通道值判位——A3/A4 语义不变。

### 2.4 为什么仍是假设、不是结论（REWORK 必须补的四件事）

1. **对齐**：lag1 最优 N=31、lag0 最优 N=33，真值在两者之间——极可能是「N=30 且含进行中半根 bar」。须用小时线重建每帖 `sent_at` 时刻的当日 running High/Low，再定 N。
2. **交易所**：老猫 2023 年大概率看 USDT 对（Binance / OKX / Huobi）。0.1–0.3% 的残差与交易所价差同量级。须在 ≥4 个交易所上重复 §2.2，取残差最小者并报告差异。
3. **全语料**：PREVIEW 是抽取预览，须先按 §3 全量抽取并过 §6.1 再拟合。
4. **作者标签**：位置一致率目前用第三方收盘价分类，须改用作者自述「通道上轨上方 / 上下轨中间 / 下轨下方」与「满仓 / 空仓」（§3.4），这才是真值的位置标签。

若上述四步后 EMA 族仍不能把 RMSE 压到 §6.3 门槛，H1 证伪，回到 §5.3 候选表继续；**任何情况下都不回到平行直线**。

---

## 3. 抽取字段 schema（交付物 2）

### 3.1 行 schema（`truth_series/rails.jsonl`，一帖一行，append-only）

| 字段 | 类型 | 规则 |
|---|---|---|
| `message_id` | int | Telegram 消息 id；主键；单调递增写入 |
| `chat_id` | int | 固定 `-1001737870653`（CARD） |
| `sender_id` | int | 固定 `5129397609`（corpus-summary `main_sender_id`）；非此值的行不得进入序列 |
| `sent_at_utc` | ISO-8601 Z | 原始发帖时刻 |
| `bar_date_utc` | date | `sent_at_utc` 所在 UTC 日；帖中「当值」指该 bar（进行中）的指标值 |
| `close_at_local` | ISO-8601 +08:00 | `bar_date_utc + 1d 00:00Z` 的北京表示（= 次日 08:00），沿用 r2 R6 单一锚点 |
| `upper` / `lower` | number | 帖中数值原样；**禁止修改、禁止四舍五入、禁止插值** |
| `width` | number | 派生 = upper − lower；只为便利，不是抽取字段 |
| `rails_pattern_id` | string | 命中的正则 id：`P1` = `上轨当值(\d+)[^\d]{0,6}下轨当值(\d+)`；`P2` = `上轨道当值`变体；`P3` = 两值分句出现；`P9` = 人工 / LLM 补录。id 表版本化 |
| `extractor_confidence` | number ∈ {1.0, 0.9, 0.7, 0.5} | P1 → 1.0；P2 → 0.9；P3 → 0.7；P9 → 0.5。**拟合只用 ≥0.9** |
| `stated_speed_dir` | enum `up\|down\|flat\|null` | 「上移 / 下移 / 趋平」 |
| `stated_speed_pts` | number \| null | 「相较昨天整体上移 N 点」的 N；仅作符号弱校验 |
| `stated_position` | enum `above\|inside\|below\|touching\|null` | 作者自述：「通道上轨上方 / 上下轨中间 / 通道下轨下方 / 触碰通道」 |
| `stated_position_detail` | string \| null | 原句片段，如「上轨上方较近区域」 |
| `stated_holding` | enum `full\|holding\|reduced\|cash\|null` | 「满仓 / 继续持有 / 减仓后持有 / 空仓」 |
| `stated_action` | enum `buy_full\|reduce\|add_back\|clear\|none\|null` | 当帖宣告的动作 |
| `stated_distance_pct` | number \| null | 「距离通道下轨只有 5 个多点」→ 5 |
| `anomaly_flags` | string[] | 见 §3.3；空数组 = 正常 |
| `edited` | bool | 若语料含编辑时间戳且晚于 `sent_at_utc` → true；保留**首版**数值 |
| `source_text_sha256` | hex | 原帖全文哈希；溯源 |
| `corpus_snapshot_id` | string | 例 `laomao-agent-distill-20260507` |
| `extractor_version` | string | 正则表 + 代码版本 |

### 3.2 覆盖表（`truth_series/coverage.jsonl`，一日历日一行）

| 字段 | 规则 |
|---|---|
| `bar_date_utc` | 从 2023-03-14 到语料末日，**每一个日历日**一行 |
| `status` | `observed` / `no_post_weekend` / `no_post_gap`（连续无帖 ≥2 个工作日）/ `post_without_rails`（有帖无轨位，列 `message_id`）/ `anomaly_excluded`（有值但 `anomaly_flags` 非空） |
| `message_id` | 有帖时填 |

**缺日处理**：不插值、不前值填充、不估算。缺日在真值表里就是缺日；拟合时缺日不计分；brief 永远不引用真值表（它只到 2025-06-24）。这与 GATE `:187`「`bars_missing` → null，no interpolation」同一纪律。

### 3.3 异常标记（打标不改数）

| flag | 触发 |
|---|---|
| `rail_inversion` | upper ≤ lower |
| `width_outlier` | width 与前后各 3 帖中位相差 >40%（13752 即命中） |
| `jump_outlier` | 任一轨相对前帖按日历日折算日位移 >3% of price |
| `speed_sign_mismatch` | `stated_speed_dir` 与两轨差分符号均相反 |
| `duplicate_day` | 同 `bar_date_utc` 多帖有轨位 → 保留最早一帖，其余打标 |
| `off_hours` | `sent_at_utc` 不在 10:00–15:00Z |
| `low_confidence` | `extractor_confidence` < 0.9 |

### 3.4 路径 B 换靶

原关键词「画 / 取点」在 HITS 28 条中零命中画法，符合 Jimmy 结论。B 改为两组：

- **指标词汇组**（找生成器）：`均线 | EMA | EXPMA | 指数 | 参数 | 周期 | N日 | 30日 | 公式 | 指标 | 通道公式 | 布林 | ATR | 高低 | 最高价 | 最低价 | 平滑 | 系统设置 | 软件 | 平台 | AICoin | 币coin | 交易所名`。
- **位置标签组**（填 §3.1 `stated_*`）：`上轨上方 | 下轨下方 | 上下轨中间 | 触碰通道 | 贴近通道 | 站上通道 | 跌破下轨 | 突破上轨 | 满仓 | 空仓 | 减仓 | 接回 | 清仓 | 安全距离`。

B 的产物是 §3.1 的标签列 + 一份「指标线索清单」（命中原句 + message_id），不是独立结论。

---

## 4. 斜率切换 / 重画点 / 禁止盘中改写（交付物 3）

### 4.1 前提

§1–§2 表明生成过程**没有重画**：每根 bar 结束时指标重算一次。因此「段 / 折点」对真值序列只是**描述性切分**，对 H0（直线零模型）是拟合单元，对 replica（前向复制品）**不存在**。三种用途分别定义：

### 4.2 真值序列的描述性切分（只用于报表与 H0）

1. **速度**：`v_t = (U_t − U_prev) / gap_days`（上轨，按日历日）；`v̂_t` = 以 t 为中心的 5 帖中位。
2. **一段**：`sign(v̂)` 连续相同的最大帖串，且 ≥5 个观测帖。
3. **折点**：仅当 `sign(v̂)` 翻转并**持续 ≥3 帖**时，在首个翻转帖前一帖记折点；其余速度变化一律记「速度变化」而非折点。
4. **强制断段**：日历缺口 >7 日处必断（不得断言连续性）；`anomaly_flags` 非空的帖不参与切分。
5. 报告：段数、段长分布、每段起止 `message_id`。**若 H0 需要平均段长 <15 帖才能达标，判「退化」**（§6.2）。

### 4.3 replica 的无重画契约（前向）

1. 参数版本钉死：`params_version = <family>-<N>-<alignment>-<venue_set>-<fit_report_sha>`。任何重新拟合 = 新版本号，**不回写**旧版本已确认的分类。
2. bar D 的分类在 `close(D) + grace_min` 后计算一次即固定（沿用 DESIGN A3/A4/R5 语义与 `close_confirmed` 对象）；后续 bar 可以改变通道值，不可改写 D 的分类。
3. 研究表可以在新版本下重算历史分类，但必须带 `params_version` 且与 brief history 物理分离。

### 4.4 禁止盘中改写

| 对象 | 规则 |
|---|---|
| 真值序列 | 一帖一行，写入即冻结；Telegram 编辑保留首版并 `edited=true`；后续帖不得修正前帖数值 |
| replica 当值 | 进行中 bar 的通道值只能以 `intraday_*`（unconfirmed）字段出现，永不进 `upper/lower/price_position` |
| replica 参数 | 盘中不得切换 `params_version`；切换只在 `close(D)+grace` 之后、且对 D+1 起生效 |
| brief | 沿用 r2 R1–R4；replica 行（若将来放行）同样只写确认值 + 「盘中 …（未确认）」 |

---

## 5. 平行约束与拟合目标（交付物 4）

### 5.1 裁决：平行不是约束，是测量量

| 方案 | 裁决 | 依据 |
|---|---|---|
| 绝对点数常宽（「约 1000 点」） | **否** | 596–4873 点；2025 年中位 3450 |
| 百分比常宽 | **否** | 0.93–6.10%；半年中位 3.17–4.23%；与波动相关 |
| 分段常宽 | **否** | 相邻帖宽度恰等 2/409；段内 ΔW 中位 53 点、近白噪声（lag-1 −0.135） |
| 上下轨同参数分别平滑（H1 的内生平行） | **允许作为模型结构**，不作为约束 | 宽度 = EMA(H−L) 自然浮动 |

拟合目标里**不得**出现宽度惩罚项；宽度残差只在 §6.4 报告。

### 5.2 H0 零模型（必跑必报，预期不过）

- 按 §4.2 切段；每段对上轨、下轨做 OLS（自变量 = 日历日）。两种变体各报一次：(a) 共享斜率（平行）；(b) 各自斜率。
- 报告 §6.3 全部指标 + 段数 + 平均段长 + 残差与 t² 相关分布。
- 目的：让证伪可复现，并给 replica 一个下界对照。

### 5.3 候选模型族与拟合目标

| 优先 | 族 | 自由参数 | 预览证据 |
|---|---|---|---|
| **H1** | `upper=EMA(High,N)`, `lower=EMA(Low,N)` | N（整数，预期 30；α=2/(N+1)）；对齐 ∈ {prior_bars_only, live_partial_bar}；交易所 | RMSE 0.12–0.30%，V 形尖锐 |
| H2 | 同 H1 但 SMA | N | 最好 1.54%，明显劣于 H1 |
| H3 | 通达信式 `SMA(X,N,M)`（α=M/N） | N, M | 未测；α 扫描最优 0.062 ≈ 2/32，若 M/N 更贴合则替换 H1 |
| H4 | 双重平滑 `EMA(EMA(X,N),N)` 或 DEMA/TEMA | N | 未测；若 H1 残差呈滞后结构再试 |
| H5 | `EMA(Close,N) ± k·EMA(H−L,N)` | N, k | 结构等价 H1 的推广，只在 H1 偏差呈对称形态时试 |
| H0 | 分段线性平行通道 | 段数不限 | §1.4，预期不过 |

拟合目标：`minimize pooled RMSE%(U,L)` on 所有 `extractor_confidence ≥ 0.9` 且 `anomaly_flags = []` 的行；约束 `|bias_U|, |bias_L| ≤ 0.05%`；同分时取参数更少、N 为整数且更「圆」（如 30）、平台默认更常见者。**禁止**逐段 / 逐年换参数（那是过拟合，不是辨识）。

维度：交易所 ≥4（Binance BTCUSDT、OKX BTC-USDT、Bitstamp BTCUSD、Coinbase BTC-USD）；对齐 2 种（半根 bar 用小时线重建至 `sent_at_utc`）；N 扫 20..45 步 1。输出一张 `(venue, alignment, N) → RMSE` 表。

---

## 6. 验收指标（交付物 5）

### 6.1 抽取验收

| 指标 | 门槛 |
|---|---|
| 召回 | 语料中同时含「上轨」与「下轨」且含数字的主讲人帖 ≥99% 进入 `rails.jsonl`；漏网逐条列 `post_without_rails` |
| 精度 | 随机抽 40 帖 + 全部 `anomaly_flags` 非空帖，人工核对原文 = 100% 逐字相等 |
| 溯源 | 每行 `message_id` + `source_text_sha256`；`sender_id` 全等 |
| 不改数 | 与原文 diff 为空；异常只打标 |
| 覆盖表 | 每个日历日一行；`observed` 行数 = `rails.jsonl` 行数 − 重复日 |
| 标签 | `stated_position` 非空率 ≥70%（预览显示几乎每帖都有位置描述）；`stated_holding` 非空率 ≥50% |

### 6.2 H0 报告要求

必须出现：段数、平均段长、两变体 RMSE / p90 / max、残差曲率占比、位置一致率。**平均段长 <15 帖或位置一致率 <97% 任一成立 → H0 判「不可作真值」**，写入本票结论证据链。

### 6.3 replica 拟合门槛

| 指标 | 最低（必须） | 目标 |
|---|---|---|
| pooled RMSE%（n ≥ 400） | ≤ 0.20 | ≤ 0.10 |
| \|bias_U\|, \|bias_L\| | ≤ 0.05% | ≤ 0.03% |
| 逐年 RMSE% | 每年 ≤ 0.30 | ≤ 0.15 |
| max \|residual\| | ≤ 1.0%，超出日逐日解释（振幅 / 半根 bar / 交易所） | ≤ 0.6% |
| 参数稀疏 | 全期单一 (N, α)；无分段参数 | 同 |
| N 稳健性 | N±1 的 RMSE 增幅 ≥30%（V 形保持） | 同 |
| 留出 | 以 2023 / 2024 / 2025 任两年拟合、第三年验证，验证 RMSE ≤ 1.5× 拟合 RMSE | 同 |

### 6.4 平行 / 宽度误差（只报告）

`width_resid = (U_hat − L_hat) − (U − L)`：RMSE ≤ 0.20% of price 记为「宽度一致」；不达标不阻塞，但须解释。

### 6.5 与历史操作日的一致性

以作者自述标签为准，不以第三方收盘价分类为准：

| 指标 | 门槛 |
|---|---|
| `stated_position` vs replica 分类（用同交易所 close(D−1) 对 rails(D)） | 一致率 ≥97%；不一致日全部列表并标注距轨 % |
| 状态转移日（`stated_holding` 或 `stated_action` 变化的帖，含 CARD 锚点 #10961 / #10962 / #10964 / #10968 / #10983 / #15960 / #15966） | 方向一致率 **100%**（±1 bar 内）；任一不一致必须有可证伪的解释（交易所收盘差、半根 bar），否则 replica 判 fail |
| 「安全距离 N 个点」 | 与 replica 距轨 % 差 ≤1.5 个百分点（弱校验） |

预览提示：2023-04-24 收盘 27596 vs 真值下轨 27581（贴轨 0.05%）、2023-04-26 Bitstamp 收盘 28300 < 真值上轨 28581 但 CARD 记「站上上轨」——这类日子决定 replica 能否放行，**必须用作者原文与其平台的收盘价**核，不能用 Bitstamp 替。

### 6.6 对 proxy 的 shadow 对比协议（两层，缺一不可）

**Layer 1 · 历史回测（现在就能跑，不必等 14 天）**

| 项 | 内容 |
|---|---|
| 样本 | 真值序列全部 `observed` 且无异常的行 |
| 对照 A | Donchian-close N=20（A4 语义）vs 真值：位置一致率、混淆矩阵、宽度比、above/below 召回。**预览基线：43.8% / 12.24% vs 3.64% / 召回 27.8% & 32.4%** |
| 对照 B | replica vs 真值：§6.3 + §6.5 全部 |
| 记录 | `research/shadow-L1-<date>.md`，不进 brief、不进 history |

**Layer 2 · 盒上并行 ≥14 个 UTC 日（沿用 r2 I6 起算规则）**

| 项 | 内容 |
|---|---|
| 起算 | 首行 `producer.host ≠ cursor` 且同时含 `trend_channel_proxy` 与 `trend_channel_replica` 的 history 记录 |
| 每日记 | 两者的 `upper / lower / price_position / intraday_position / status / params_version` |
| 观测靶 | (i) replica 与 proxy 的 `price_position` 不一致日数与方向；(ii) replica 翻转频率；(iii) replica `status` 非 ok 次数与原因；(iv) 每日 replica 值与「若老猫仍在发帖会写的当值」无法比对——**因此 Layer 2 只验稳定性，不验正确性；正确性只能由 Layer 1 给** |
| 通过 | 14 日内 replica `fail` = 0；`degraded` 均有 `bars_degraded` 解释；无参数切换；与 proxy 的不一致全部可由宽度差解释 |

### 6.7 H1 证伪后的路线

若 §2.4 四步后 EMA 族最低门槛仍不达：按 §5.3 顺序试 H3 → H4 → H5，每族一份同格式报告；全部不达 → 结论改为「真值生成器不可辨识」，真值序列仍保留为历史标签集，proxy 契约维持，`missing_inputs` 字面维持。**不得因拟合失败而降低门槛。**

---

## 7. 与 proxy 共存契约（交付物 6）

### 7.1 三级分类

| 级 | 块名 | 标志 | 含义 | 可否前向计算 |
|---|---|---|---|---|
| 真值 | `truth_series`（文件，不进 JSON 主体） | `is_truth: true` | 老猫平台当日显示值，仅限有帖日期 | 否（止于 2025-06-24） |
| 复制品 | `trend_channel_replica` | `is_replica: true, is_truth: false, is_proxy: false` | 通过 §6 的生成模型输出 | 是 |
| 代理 | `trend_channel_proxy` | `is_proxy: true`（现状，不变） | 机械替身，不声称相似 | 是 |

三个标志在任一块内互斥；`is_truth: true` 只能出现在真值文件的行上。**框架模板的 `trend_channel` 槽位（FRAME §7）只接受 `is_truth`**——replica 再准也不填它；顶层 `trend_channel` 键继续禁止（DESIGN A5）。

### 7.2 JSON：`schema_version: 3` = v2 + 兄弟块

v2 全部键、顺序、语义不变（r2 I1 契约）。新增：

```json
{
  "schema_version": 3,
  "trend_channel_proxy": { "...v2 原样..." },
  "trend_channel_replica": {
    "is_replica": true,
    "is_truth": false,
    "is_proxy": false,
    "replica_of": "laomao_2.0_trend_channel",
    "replica_disclaimer": "Fitted replica (EMA of daily High/Low). Reproduces LaoMao's published rails 2023-03..2025-06 within {fit_rmse_pct}% RMSE; formula NOT author-confirmed.",
    "method": "ema_high_low",
    "params": { "n": 30, "alpha": 0.0645, "alignment": "prior_bars_only|live_partial_bar", "venue_set": ["..."], "grace_min": 10 },
    "params_version": "ema_hl-30-prior-binance_okx_bitstamp_coinbase-<sha8>",
    "fit_report_ref": { "path": "research/replica-fit-<date>.md", "sha256": "..." },
    "fit_rmse_pct": 0.0, "fit_n_days": 0, "fit_period": "2023-03-14..2025-06-24",
    "truth_position_agreement_pct": 0.0,
    "bar": { "boundary_tz": "UTC", "close_local": "08:00 Asia/Shanghai" },
    "close_confirmed": { "...与 proxy 同结构..." },
    "sources_used": ["..."],
    "window": { "start": "...", "end": "...", "bars": 0, "bars_degraded": [], "bars_missing": [] },
    "ref_close": 0.0, "upper": 0.0, "lower": 0.0, "mid": 0.0, "width_pct": 0.0,
    "distance_to_upper_pct": 0.0, "distance_to_lower_pct": 0.0,
    "price_position": "above_upper|inside|below_lower", "position_basis": "confirmed_close",
    "intraday_position": "above_upper|inside|below_lower|null", "intraday_basis": "consensus.median (unconfirmed)",
    "slope": "up|flat|down", "slope_pct_per_day": 0.0,
    "status": "ok|degraded|fail", "note": "human-readable"
  }
}
```

规则：`fit_*` 与 `params_version` 为常量镶入，来源只能是过闸的 fit report；`bars_missing` 非空 → `fail` 且轨位 null（EMA 不得跨缺日递推）；两块 `status` 互相独立；history 每行同时含两块。

### 7.3 brief：何时可换行

| 阶段 | proxy 固定行 | replica | `missing_inputs` 字面 | `system_signal` |
|---|---|---|---|---|
| 现在 → §6 Layer 1 通过前 | 写（r2 §3 原样） | 只在研究表 | 必含 `"trend_channel (LaoMao 2.0 original)"` | 禁 |
| Layer 1 通过、Layer 2 进行中 | 写 | 只进 history，**不进 brief** | 必含 | 禁 |
| Layer 1 + Layer 2 通过 → IMPL-GATE r3 放行后 | 停写（JSON 内保留块 ≥30 日供对照） | 写 replica 固定行 | **仍必含**（直到作者确认公式 → `is_truth`） | **仍禁**（另开闸） |
| 作者确认公式 | — | 升 `is_truth`，填 `trend_channel` 槽 | 移除字面 | 另开闸 |

replica 固定行模板（预定，r3 可改字不可改槽）：

`通道[replica · EMA-HL N={n} · 拟合RMSE {fit_rmse_pct}% · 非作者确认]：上轨 {upper} / 下轨 {lower}｜收盘确认 {bar_date} {closed_at_local}：{price_position}｜盘中 {intraday_position}（未确认）｜数据 {status}`

`status=fail` 时回退顺序：replica → proxy 固定行 → `通道[proxy]：不可用（{note}）`。brief 任何时候只写**一条**通道行，不得并列两条造成等价印象。r2 R4 新鲜度 / 确认落后规则对 replica 行同样生效。

### 7.4 本文不授权

- 不授权 `schema_version: 3` 落码、不授权 replica 进 history、不授权 brief 换行——这三件事各需 IMPL-GATE。
- 不授权任何来自 replica 或真值序列的 `system_signal`。GATE `:293` REFUSE 升级条件不变，且扩展到 replica：发现任何 brief 以 replica 轨位产出 `system_signal` 且有人据此操作 → 撤行、REFUSE。

---

## 8. 对申请方主张的答复

| 主张（REQUEST / 题面） | 核验 | 结论 |
|---|---|---|
| 无显式画法，只有当值 / 速度 / ~1000 点 / 收盘写死 | HITS 28 条零画法；PREVIEW 统计 | **属实，且比申请方以为的更进一步**：没有画法是因为它不是画的 |
| 推断两点定线平行通道（徐小明变体） | §1.3–1.4 | **不成立** |
| width 均值 ~2207、中位 ~2028、早期 ~1008、后期 3000+ | 复算 2206.96 / 2028.5；2023-H1 中位 988；2025-H1 中位 3450 | 属实；「固定 1000 点」不成立 |
| 路径 A 抽取 date→upper/lower 可行 | 28/28 逐字；15/15 符号 | 属实，PASS |
| 路径 B 只能佐证 | 原关键词组零命中 | 换靶后 B 是必需的标签源 |
| proxy 替换前须 shadow ≥14 UTC 日 | 维持；但 14 日 shadow 只验稳定性 | 补 Layer 1 历史回测为正确性闸（§6.6） |

---

## 9. 推翻条件与置信度

| 结论 | 置信度 | 会推翻它的证据 |
|---|---|---|
| 总判 REWORK（而非 PASS A） | 0.92 | 全语料抽取后 H0 以平均段长 ≥15 帖达到 RMSE ≤0.20% 且位置一致率 ≥97% —— 预览显示不可能，但必须让 H0 跑完 |
| 平行直线模型被证伪 | 0.95 | 找到老猫原文明说「连接 X 点与 Y 点画线」并给出取点规则 |
| H1 = EMA(H/L) 族正确 | 0.80 | 换 ≥4 交易所 + 半根 bar 对齐后 pooled RMSE 仍 >0.20%，或 N 的 V 形消失（多个 N 同好） |
| N≈30 | 0.70 | 半根 bar 对齐后最优 N 落在 30±1 以外 |
| 平行不作约束 | 0.95 | 全语料宽度 % 的半年中位极差 <0.3 个百分点（预览 1.06） |
| proxy 位置一致率 43.8% | 0.85 | 用作者自述标签而非 Bitstamp 收盘复算后 ≥70% |
| 13752 为异常 | 0.95 | 原文确为 95952 且前后帖说明当日通道异常 |
| 抽取半部 PASS | 0.90 | §6.1 抽检出现任何一处数值被改写或 `sender_id` 混入他人 |

---

## 10. 非目标

- 不实现抽取器、拟合器、`schema_version: 3`、replica 块、brief 行；不改 r2 已 PASS 的任何文件与文案。
- 不替 Jimmy 或老猫确认公式；不裁 N 的最终值；不裁交易所归属。
- 不评估 DIF / 钝化 / 结构 / 正负角线；不做 3.0 系统。
- 不拉小时线、不做多交易所拉取（属 REWORK 执行面）。
- 不涉及下单、仓位或任何执行面；不产出 `system_signal`。

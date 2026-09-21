REWORK

# GATE：老猫 2.0 真值趋势通道重建 — 路径 A「反向拟合平行通道」架构裁决

> 裁决：**REWORK**。路径 A 拆成两半：**抽取半部 PASS**（每日上/下轨「当值」序列即真值，升格为一等产物）；**拟合半部 REFUSE**（「两点定线平行通道 / 徐小明变体」被预览数据证伪，不得以任何拟合结果冒充真值）。重建目标改为**生成模型辨识**（路径 C），路径 B 保留但换关键词。预览级探针已给出一个强候选：**日线 EMA(High, N) / EMA(Low, N)，N≈30–33，UTC 日 bar**，单一交易所数据、单一参数，对 409 日真值 RMSE 0.12–0.30%（§2）；这是待证伪的假设 H1，不是结论。已 PASS 的 Donchian proxy brief 契约（IMPL-GATE r2）**一字不改**；本文只新增契约（§7），不授权任何 brief 换行。
> 对照物：`uploads/REQUEST.md`（下称 REQUEST）；`uploads/IMPL-GATE-r2-PASS.md`（PR [#7](https://github.com/licett/ai-workflow-kit/pull/7)，下称 r2）；`uploads/DESIGN-channel-proxy-v0.md`（下称 DESIGN）；`laomao-trading-framework.md`（下称 FRAME）；`laomao-agent-card.md`（下称 CARD）；`laomao-corpus-summary.json`（416 篇 / 80824 字 / 2022-03-09..2025-06-24）；`samples/rails_extract_preview.jsonl`（410 行，下称 PREVIEW）；`samples/keyword_B_hits.json`（28 条，下称 HITS）。
> 方法：只读 uploads；PREVIEW 在 `/tmp` 做描述统计与模型判别（无代码入库）；**一次**公开只读拉取 Bitstamp BTC/USD 日线 1000 根（2023-01-01..2025-09-26）用于 §2 的模型族探针——这是裁决所需的证据动作，不是实现；未拉分钟/小时线，未碰盒上文件。所有数字可按 §5–§6 协议复现。
> 边界：research-only。本文不改 py / README / DESIGN / JSON / history；不产出任何 `system_signal`；拟合结果在过 §6 闸门之前只能进研究表，不得进 brief。
> 日期：2026-09-21。
> **r1 增补（同日）**：申请方（老猫 / Jimmy）追问「repo 是否够拟合」「是否像 TV 公开趋势公式」，并给出 `licett/laomao data/fetch-20260507/laomao-posts.jsonl` 的补充统计与 TradingView 候选先验。已并入 §0A（三条明文裁决）、§5.3（H0-TV）、§6.8（TV 复现验收）、§8、§9。**裁决维持 REWORK**；补充证据全部与 PREVIEW 复算一致，且进一步否定「Parallel Channel」先验。
> **r2 增补（同日）**：Jimmy 提供 OpenClaw 版老猫的通道来源链（`laomao/backtest.py` oracle 优先 + `indicators/trend_channel.py` S39 假设引擎 `ema_percent_envelope`：mid = EMA34，rails = mid×(1±0.018958)，`formula_status="hypothesis"`，S40/S41 fail-closed），要求碰撞后给出**更好且有依据**的版本。已并入 §0B（A 对照表 / B 分层真源裁决 / C 推荐架构与硬验收 / D 文首裁决）、§3.1 与 §7.2 字段、§6.9 硬验收、§8、§9。**文首裁决维持 REWORK**：分层真源作为架构**采纳（设计层 PASS）**，但填补模型在过 §6 之前仍是 `hypothesis`，票面交付物（可替代 proxy 的通道）尚未成立。S39 在 409 日真值上的碰撞结果：轨位 RMSE 0.46–0.55%、**宽度残差 0.79%**（H1 0.12%），中轨对、宽度模型错（§0B.1）。

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
| 追问三裁（r1） | 见 **§0A** | A 抽取立、A 拟合不立；「分段斜率 + 可变轨距」为直线类模型的**下限**而非目标；TV Parallel Channel **不作** replica 验收对照，改为 H0-TV 机械化零模型 + H1 的 TV 复现验收 |
| 分层真源（r2，OpenClaw 碰撞） | 见 **§0B** | **采纳并加严**：oracle 当值 = 真值标签、物理隔离、不可拟合掉；无当值日只允许**单一全局生成公式**填补；`formula_status` 四级梯子（hypothesis → replica_shadow → replica → author_confirmed），hypothesis 不进 JSON / history / brief；S39 EMA% 包络作候选 H6 已测：中轨对、宽度错，被 H1 全面压制 |

置信度：总判 REWORK 0.92；直线模型被证伪 0.95；H1 为正确模型族 0.80（参数 / 对齐 / 交易所待定，见 §2.4 与 §9）；抽取半部 PASS 0.90（预览 28 条抽检，全量抽检在 §6.1）。

---

## 0A. 追问三裁（r1 增补：补充证据并入）

### 0A.1 补充证据核对

| 申请方数据（`laomao-posts.jsonl`） | PREVIEW 复算 | 判定 |
|---|---|---|
| 409 日上/下轨当值对，2023-03-14→2025-06-24 | 410 行（含 13752 异常行）= 409 有效 | 一致 |
| 相邻日样本 312 | 相邻日（gap=1）对 313（剔异常）/ 314 | 一致（±1 为异常行归属） |
| 轨距中位：2023≈991、2024≈2434、2025≈3495 | 991 / 2434 / 3470（剔异常）；按 % 为 3.36 / 4.13 / 3.80 | 一致；**点数随价格翻 3.5 倍，百分比只在 3.4–4.1 之间** |
| 严格平行 \|Δu−Δl\|≤5 仅 ~9.6%；≤50 ~56% | 9.9% / 57.5%；≤20 为 29.7%；中位 \|Δu−Δl\| = 39 点 = **0.077% of price**（p90 0.23%） | 一致 |
| 教学贴几乎无 | HITS 28 条零画法 | 一致 |
| **最大断档 ~46d** | **错**：46d 是 2023-07-07→08-22；最大断档是 **2024-07-22→12-17 = 148d**；corpus-summary `month_buckets` 2024-08..11 = 0 篇可证 | 须更正；§4.2 强制断段与 §3.2 覆盖表以 148d 为准 |

补一个解释：\|Δu−Δl\| 的 0.077% / 0.23% 正是 H1 的预测量——同 α 分别平滑 High 与 Low 时，`Δu−Δl = α·(range_t − EMA(range)_{t−1})`，α≈0.065、BTC 日振幅离均 ±1–3% → 0.07–0.2%。「不严格平行」不是噪声，是模型结构。

### 0A.2 三条明文裁决

**裁决 1 · 路径 A 是否仍立：抽取半部立，拟合半部不立（不变）。**

- 「repo 是否够拟合」：**够，且绰绰有余——对辨识而言。** H1 只有一个连续参数（N）+ 一个二值对齐 + 交易所选择，409 个目标点跨 2.3 年、4 倍价位，N 扫描已呈尖锐 V 形（§2.2）。辨识的**输入**是交易所 OHLC（无断档），rails 只是**目标**；因此 46d / 148d 断档只减少计分点，不影响递推，**不需要在 H1 上分段，也无插值问题**。
- 对「分段线性平行通道」而言：**不够，而且永远不够**——不是样本量问题，是模型错。§1.4 显示要把直线残差压到 0.1% 需每 3–5 帖一个折点，409 点会被几十段吃掉，这是连点不是拟合。
- 因此 A 的抽取产物按 §3 落地为真值序列；A 的拟合目标撤销，由 §5.3 候选族替代。

**裁决 2 · 是否强制「分段斜率 + 可变轨距」：强制，但只是下限。**

| 对象 | 规则 |
|---|---|
| 任何直线类模型（H0、H0-TV、描述性切分） | **必须**分段斜率（§4.2 切段，>7d 缺口强制断段，含 148d）+ **每段轨距自由**；**禁止**全样本固定 1000 点、禁止固定百分比、禁止跨段共享轨距 |
| H1 及 §5.3 其余候选 | 自动满足（斜率逐 bar 变、轨距 = 平滑后的日振幅），**不额外施加**任何轨距约束（§5.1） |
| 任何模型 | 「固定 1000 点」若出现在假设、代码常量或 brief 文案中 → 该产物直接判 fail |

明确一句：满足「分段斜率 + 可变轨距」**不等于**能过闸。§1.4 的 10 帖窗口 OLS 已经是分段斜率 + 自由轨距，残差仍有 75% 系统曲率；§6.2 的「平均段长 <15 帖判退化」就是给这条下限设的天花板。

**裁决 3 · 是否要求与 TV Parallel Channel 对照验收：不作为 replica 验收对照；改为两项替代要求。**

理由：TradingView 的 Parallel Channel 是**手工绘图工具**——两点定线、第三点定平行偏移，此后斜率与轨距恒定直到人手重画。它没有确定性算法（锚点由人选），因此不存在可复现的参照值，「对照误差」无法定义；而其两条结构假设（段内恒斜率、恒轨距）已被申请方自己的统计否定（严格平行 9.6%、轨距 3.5 倍漂移）和 §1.3 否定（速度连续变化）。**要求与它对照 = 要求与一张未指定的手绘图对照。**

替代要求（两项都是硬性的）：

(a) **H0-TV 机械化零模型**（并入 §5.3 / §5.2，必跑必报，预期不过）：把「Parallel Channel」先验写成可复现规则后再算——锚点规则**事先钉死**（如 pivot low 左右各 5 根确认；通道 = 最近两个已确认 pivot low 连线；平行线过两锚点之间的最高 High；仅当新 pivot 确认时重画，重画不回写历史）。报 §6.3 全部指标 + 重画次数 + 每段轨距。样本规则：全部 `observed` 且 `anomaly_flags=[]` 的 409 行；>7d 缺口断段；斜率一致性只在 313 个相邻日对上算；阈值与 §6.3 完全相同（pooled RMSE ≤0.20%、\|bias\|≤0.05%、位置一致率 ≥97%）。**不许因为它是零模型而放宽阈值。**

(b) **H1 的 TV 复现验收**（新增 §6.8）：过闸的 replica 必须能在 TradingView 上用**两行 Pine**（`ta.ema(high, N)` / `ta.ema(low, N)`，D 周期，UTC 对齐的交易所 symbol）复现，并在 409 个帖日与真值比对。这才是「像不像 TV 公开公式」的正确问法——答案不是像不像 Parallel Channel，而是它**就是**一条 TV 内建可画的 EMA 高低包络。

### 0A.3 TV 候选先验 vs 观测

每列为该模型的**预测**，「观测」列为 PREVIEW 事实；预测与观测相反处加粗。

| 特征 | 观测（PREVIEW） | Parallel Channel（绘图） | Linear Regression Channel（内建） | EMA(High,N)/EMA(Low,N)（两行 Pine） |
|---|---|---|---|---|
| 每日历日推进 | 是（周五→周一 2.68×） | 是 | 是 | 是 |
| 段内斜率恒定 | 否（41% 窗口速度单调变化；52 次渐变翻转） | **是** | 否（逐 bar 重算） | 否（逐 bar 重算） |
| 轨距恒定 | 否（严格平行 9.6%） | **是** | 否（= k·σ） | 否（= EMA 日振幅） |
| 轨距 ∝ 价格 × 波动 | 是（log-log 1.10；% 稳定在 3.4–4.1） | **否** | 部分（σ 随波动，不随价位线性） | 是 |
| 整体位移式「重绘」 | 未见 | 人手重画时跳变 | **有**（窗口滑动、全通道整体重算） | 无，只有递推 |
| 「速度增加 / 放缓 / 趋平」 | 每日出现 | **无法产生** | 可以 | 一一对应（速度 = α·(H_t − EMA_{t−1})） |
| 对 409 日真值 RMSE | — | 不可复现；机械化后见 H0-TV | 未测；不列候选、不列对照 | 0.12–0.30%（单交易所、未对齐半根 bar） |

结论：申请方先验「较像 Parallel Channel、不像 Linear Regression Channel（因为重绘）」**方向反了**——真值恰恰是每根 bar 重算的指标，只是不是回归通道；「徐小明通达信通道是否有 TV 脚本」与裁决无关，数据自己选出了模型族。

---

## 0B. r2 增补：与 OpenClaw 来源链碰撞（A–D）

OpenClaw 版（Jimmy 转述）：(1) **oracle 优先**——原文当天明确播报「上轨当值 / 下轨当值」则直接采信，`rail_confidence="explicit"`，冲突则 `"conflict"`，日报只是搬运老猫自己的数；(2) **S39 假设引擎兜底**——无当值日用 `ema_percent_envelope`：中轨 = 34 周期 EMA，上轨 = 中轨×(1+k)，下轨 = 中轨×(1−k)，k≈0.018958，`formula_status="hypothesis"`，S40/S41 置信不足 fail-closed。以下是碰撞，不是照抄。

### 0B.1 碰撞数据：S39 在 409 日真值上

同 §2.1 设置（Bitstamp 日线、剔 13752、lag=1 只用已收 bar / lag=0 含当日整根 bar）：

| 模型 | 轨位 RMSE | biasU / biasL | 逐年 RMSE | max \|res\| | 位置一致（全部日） | 近轨日一致（收盘距轨 <1% / <0.5%） | **宽度残差 RMSE** | 翻转日召回 / 精度 |
|---|---|---|---|---|---|---|---|---|
| **S39** EMA34(close)×(1±0.018958) lag1 | 0.551% | −0.07 / −0.10 | 0.58 / 0.56 / 0.50 | 1.57% | 96.8% | 86.0% / 80.5% | **0.790%** | 0.85 / 0.95 |
| S39 lag0 | 0.456% | +0.12 / +0.08 | 0.42 / 0.51 / 0.43 | 1.48% | 96.8% | — | 0.789% | — |
| S39 族最佳（N、k 全放开，lag1） | 0.474%（N=32，k*=0.01918） | — | — | — | 96.1% | — | 0.792% | — |
| H1 EMA(H,31)/EMA(L,31) lag1 | 0.303% | +0.03 / −0.02 | 0.29 / 0.35 / 0.26 | 1.26% | 97.3% | 88.2% / 73.2% | **0.116%** | 0.93 / 0.85 |
| H1 EMA(H,33)/EMA(L,33) lag0 | **0.120%** | +0.07 / −0.01 | 0.13 / 0.12 / 0.10 | 0.66% | **99.0%** | **95.7% / 90.2%** | 0.144% | **0.99 / 0.92** |

宽度误差按半年（模型 − 真值，百分点）：

| 半年 | 真值宽度中位 | S39 | H1(31,lag1) |
|---|---|---|---|
| 2023-H1 | 3.48% | +0.04 | +0.05 |
| **2023-H2** | 3.12% | **+0.71**（太宽 → 漏报跌破：近轨日 6 次 below→inside） | −0.02 |
| **2024-H1** | 4.14% | **−0.46**（太窄 → 假突破） | +0.07 |
| 2024-H2 | 3.78% | −0.04 | +0.03 |
| 2025-H1 | 3.73% | +0.03 | +0.08 |

真值宽度 %：均值 3.75、标准差 0.81；与常数 2k=3.79% 相差 >0.5 个百分点的日子占 **58%**，>1 个百分点占 23%。1 个百分点的宽度差 = 每条轨 0.5% 的位置差，正是 §1.4 说的操作日量级。

读法：**S39 把中轨做对了、把宽度做错了。** k=0.018958 ≈ 真值宽度中位 3.79% 的一半——它是对同一语料的拟合值，不是独立证据；S39 族把 N、k 全放开也只能到 0.47%，因为常数百分比宽度在低波动期太宽、高波动期太窄。把 `mid×(1±k)` 换成 `EMA(High,N)` / `EMA(Low,N)`，宽度残差 6.8 倍下降、轨位 RMSE 2–4 倍下降、近轨日一致率从 86% 到 96%。这就是「更好版本」的依据，其余部分 OpenClaw 的方向是对的。

### 0B.2 A · 对照表：路径 A vs OpenClaw vs 本文推荐

| 维度 | 路径 A（当值序列反拟平行通道） | OpenClaw（oracle + S39 EMA% 包络） | 本文推荐（oracle + H1 梯子，§0B.4） |
|---|---|---|---|
| 适用日 | 仅有帖日（409），且需切段 | 有帖日走 oracle；无帖日与 2025-06-24 之后走 S39 | 同 OpenClaw 分层；但 oracle 与 model **物理分文件**，一日只用一源 |
| 前向可算 | 否（锚点无规则，段末不知向哪延） | 是 | 是 |
| 失败模式 | 段内曲率（75% 窗口）；段长 <15 帖退化；贴轨日误判；无法 fail-closed（人工锚点） | 宽度常数 %：低波动期漏跌破、高波动期假突破（±0.5–0.7 pt）；oracle→model 边界跳变最大 +1.15%（2023-08-22）；oracle 日进评估会自评满分 | 半根 bar 对齐与交易所未定（§2.4）；边界跳变最大 −0.52%（未对齐版）；须 §6.9 硬验收兜住 |
| 「收盘写死」契合 | 无关（只用轨位序列） | 中轨用 close 可接 A3/A4；确认语义未述 | 直接沿用 A3 / A4 / R5：`close_confirmed` 对象、grace、无重绘 |
| 「平行推进」契合 | **假设严格平行**——观测 9.6% | 百分比平行：Δu/Δl ≡ (1+k)/(1−k) ≈ 1.039，近似合观测但机制不对 | 内生近平行：\|Δu−Δl\| = α·\|range_t − EMA(range)\| → 预测中位 0.07–0.2%，观测 0.077% / p90 0.23%（§0A.1） |
| 「可变轨距」契合 | 段内常数 → 否 | 常数 % → **否**（宽度残差 0.79%，58% 日偏 >0.5 pt） | 宽度 = EMA 日振幅 → **是**（残差 0.12%） |
| 对 409 日真值 RMSE | 0.25%（每 10 帖一段，退化） | 0.46–0.55% | 0.12–0.30% |
| 状态标签 | 无 | `rail_confidence` + `formula_status="hypothesis"`（单级） | 四级 `formula_status` 梯子 + 门（§0B.4） |
| 对读者暴露 | — | hypothesis 轨位进日报 | hypothesis **不进** JSON / history / brief |

### 0B.3 B · 是否采纳「分层真源」：采纳，附五条加严

| # | OpenClaw 做法 | 裁决 | 依据 |
|---|---|---|---|
| B1 | explicit 当值 = 直接采信 | **采纳**：oracle 行 = 真值标签，`rail_source="oracle"`，`rail_confidence="explicit"`；**任何模型不得改写、不得平滑、不得用于"修正"它**；模型只能被它评分 | §1.5 抽取 28/28 逐字；这就是 §3 的真值序列 |
| B2 | 冲突 → `"conflict"` | **采纳并加严**：同日多帖数值不一致或同帖前后不一致 → `conflict`，**既不采用也不计分、不取均值**；计数进 §6.1 报告 | 取均值会制造一条谁也没说过的轨 |
| B3 | 无当值日用模型填补 | **采纳并限定**：填补只允许**单一全局生成公式**（§5.3 候选，含 S39 作 H6、H0/H0-TV 作零模型）；**禁止**逐缺口插值、逐段重拟、人工锚点平行通道（不可 fail-closed，§0A.2 裁决 3）；「分段平行通道」只以 H0-TV 机械化形式参赛 | §0A.2 裁决 1：模型输入是 OHLC，断档不影响递推 |
| B4 | `formula_status="hypothesis"` 单级 | **加严为四级梯子**：`hypothesis`（未过 §6.3 / 6.5 / 6.8）→ `replica_shadow`（过 Layer 1，进 history 不进 brief）→ `replica`（过 Layer 2 + IMPL-GATE r3，可进 brief）→ `author_confirmed`（作者确认公式，可填 `trend_channel` 槽）。**`hypothesis` 只存在于研究文件**，不写 JSON、不写 history、不进 brief | §0B.1：hypothesis 级模型在近轨日 14% 判错，读者恰在那些日子行动 |
| B5 | S40/S41 fail-closed | **采纳并写死三处**：数据层（`bars_missing` 非空 → 轨位 null、`status=fail`，沿用 GATE `:187`）；状态层（`formula_status` 低于阶段要求 → 该块不得输出）；信号层（`system_signal_eligible=false` 常量，见 C） | r2 R4「文件缺失 ≠ 平静」 |
| B6（新增） | — | **一日一源、不混算**：某日分类只能来自 oracle 或 model 之一；oracle↔model 相邻处打 `source_transition=true`；模型评分**只能**用 model 值对 oracle 值，脚本须断言不存在 oracle 对 oracle 的比较 | S39 边界跳变 +1.15% / −0.65%；oracle 日进评估 = 给老猫自己的数打分 |
| B7（新增） | — | **oracle 层是有限历史**：止于 2025-06-24；前向 brief 里 `rail_source` 恒为 `model`。若老猫复播，新帖走 §3 schema + §6.1 抽检后进 oracle，并触发一次模型重评分（漂移检测），不得静默并入 | 「oracle 优先」是标注策略，不是活数据源 |

### 0B.4 C · 推荐架构与硬验收

**文件与块**

| 层 | 载体 | 内容 | 允许写入者 |
|---|---|---|---|
| L0 oracle | `truth_series/rails.jsonl`（§3.1，新增 `rail_source` / `rail_confidence`） | 只有 explicit / conflict 行 | 抽取器 |
| L0 覆盖 | `truth_series/coverage.jsonl`（§3.2） | 每日历日一行 | 抽取器 |
| L1 model（研究） | `research/model_fill-<params_version>.jsonl` | 每日历日一行模型值 + `formula_status` + `scored_against_oracle`（oracle 日为 true，仅供评分） | 拟合器 |
| L1 model（生产） | JSON `trend_channel_replica`（§7.2，新增字段见下） | 仅 `formula_status ≥ replica_shadow` 时可输出 | `btc_multisource.py`（IMPL-GATE r3 后） |
| proxy | `trend_channel_proxy` | 不变 | 不变 |

**字段（§3.1 与 §7.2 同步）**

| 字段 | 取值 | 规则 |
|---|---|---|
| `rail_source` | `oracle \| model \| none` | oracle 只在 L0；生产 JSON 恒 `model`（B7） |
| `rail_confidence` | `explicit \| conflict \| derived \| none` | oracle → explicit / conflict；model → derived；null 轨位 → none |
| `formula_status` | `hypothesis \| replica_shadow \| replica \| author_confirmed` | 只对 model；升级只经 §6 + IMPL-GATE，降级随时（§6.7 证伪即回 hypothesis） |
| `params_version` | string | §4.3；变更 = 新版本，不回写 |
| `source_transition` | bool | 与前一日历日 `rail_source` 不同则 true（B6） |
| `system_signal_eligible` | **常量 `false`** | 本票及 r3 均不得改；改动条件：`formula_status=author_confirmed` **且** 另有 `signal_gate_ref` 指向已 PASS 的信号闸 |
| `signal_gate_ref` | string \| null | 本票恒 null |

**硬验收（新增 §6.9，与 §6.1–6.8 叠加）**

| 项 | 门槛 |
|---|---|
| 源隔离 | `rails.jsonl` 内 `rail_source` 全为 oracle；`model_fill` 内全为 model；任一文件出现对方 → fail |
| 冲突处理 | `conflict` 行不在任何评分样本、不在任何输出；报告冲突数与 message_id |
| 自评守卫 | 评分脚本断言：目标列来自 L0，预测列来自 L1，且 L1 值由 OHLC 递推生成（非拷贝）；oracle 对 oracle 的比较出现即 fail |
| 边界跳变 | 每个 >7d 缺口两端 oracle 日，\|model − oracle\| 两轨均 ≤0.30%（预览：S39 +1.15% / +0.79% / −0.65% 三处不达；H1 未对齐版 −0.52% 一处不达 → 对齐是 §2.4 第 1 步的原因） |
| fail-closed 三注入 | (i) 抽掉窗口内 1 根 bar → 轨位 null、`status=fail`；(ii) 强制 `formula_status=hypothesis` → 块不输出、brief 无通道行或回退 proxy 行；(iii) 任何路径尝试写 `system_signal_eligible=true` → 进程退出非 0 |
| 一日一源 | history 中不存在同日两源；`source_transition` 日在 brief 只允许写模型行（历史 oracle 不进 brief） |
| 禁止事项 | **`hypothesis` / `replica_shadow` / `replica` 三级均不得推 `system_signal`**；`missing_inputs` 必含 `"trend_channel (LaoMao 2.0 original)"` 直到 `author_confirmed`；GATE `:293` REFUSE 升级条件扩展到三级中任一级 |

**相对 OpenClaw 的六处改动与依据**：① oracle 层加 provenance 哈希、异常打标、作者位置标签（§3.1；OpenClaw 转述未见）；② 宽度模型 `mid×(1±k)` → `EMA(H)/EMA(L)`（§0B.1，6.8× 宽度残差）；③ 单级 hypothesis → 四级梯子 + 门（B4）；④ 一日一源 + 边界跳变 + 自评守卫（B6）；⑤ hypothesis 不触达读者（B4）；⑥ TV 两行复现作为放行必要条件（§6.8）。S39 作为 H6 保留在候选表，供 REWORK 用全语料 + 正确交易所复测——若它在那套数据上反超 H1，§5.3 排序改，本文 H1 相关置信度作废。

### 0B.5 D · 文首裁决

维持 **REWORK**。理由：B/C 是架构层裁决（设计 PASS，进入 §7 契约），但票面问题是「能否重建可替代 proxy 的真值通道」——分层真源把 409 日历史标好了，前向仍全靠 `formula_status=hypothesis` 的模型；在它过 §6.3 / 6.5 / 6.8 / 6.9 之前，交付物不成立。文首行不因本增补改变。

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
| `rail_source` | 常量 `oracle` | （r2）本文件只容 oracle 行；出现其他值 → §6.9 源隔离 fail |
| `rail_confidence` | enum `explicit\|conflict` | （r2）同日多帖或同帖前后数值不一致 → `conflict`：不采用、不计分、不取均值 |
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
4. **强制断段**：日历缺口 >7 日处必断（不得断言连续性）——PREVIEW 中共 5 处：46d（2023-07-07→08-22）、18d、11d、**148d（2024-07-22→12-17）**、9d；`anomaly_flags` 非空的帖不参与切分。断段只约束直线类模型与描述性报表；H1 的递推输入是交易所 OHLC，不受帖子断档影响（§0A.2 裁决 1）。
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
| H6（r2，OpenClaw S39） | `mid=EMA(Close,N)`，`rails=mid×(1±k)` | N=34, k=0.018958（OpenClaw 值）；族内放开亦报 | **已测**：0.46–0.55%，宽度残差 0.79%，族内最佳 0.47%（§0B.1）；中轨对、宽度错；保留为对照候选 |
| H0 | 分段线性平行通道（§4.2 切段 + 段内 OLS） | 段数不限；**每段轨距自由** | §1.4，预期不过 |
| H0-TV | TV Parallel Channel 机械化（§0A.2 裁决 3(a)：钉死 pivot 锚点规则，仅新 pivot 确认时重画） | pivot 左右确认根数（事先钉死，只允许 1 组） | 未测；申请方先验，预期不过；**不得因是零模型而放宽阈值** |
| 不列 | TV Linear Regression Channel | — | 整通道随窗口整体重算的位移在真值中未见；轨距 = k·σ 不随价位线性；不作候选、不作对照 |

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

### 6.8 TV 复现验收（r1 新增；replica 放行的必要条件）

回答「是否像 TV 公开趋势公式」的正确方式不是与 Parallel Channel 绘图对照（§0A.2 裁决 3），而是要求 replica 本身可在 TradingView 上零依赖复现：

| 项 | 要求 |
|---|---|
| 脚本 | Pine v5/v6，**只允许** `ta.ema(high, N)` 与 `ta.ema(low, N)` 两条 plot（或 §5.3 最终胜出族的等价内建函数）；N 为过闸的 `params.n`；脚本全文（≤10 行）与 sha256 进 `fit_report_ref` |
| 图表 | D 周期；symbol 为过闸 `venue_set` 中残差最小的交易所（如 `BINANCE:BTCUSDT` / `BITSTAMP:BTCUSD`）；图表时区设 UTC，确认日 bar 边界 = 00:00 UTC（A1） |
| 采样 | 全部 409 个帖日（剔 `anomaly_flags` 非空）；每日读取 TV 该 bar 的两条 plot 值（可用 Pine `alert()` / 数据窗口导出，不得手抄） |
| 对齐 | 两种都报：(i) 已收 bar 值（D−1 收盘后的值，对应 `alignment=prior_bars_only`）；(ii) 实时值（bar D 进行中，若能复刻 12:00 UTC 快照则用回放 bar-replay 到该时刻） |
| 阈值 | 与 §6.3 同：pooled RMSE ≤0.20%（目标 ≤0.10%）、\|bias\|≤0.05%、max \|resid\| ≤1.0% 并逐日解释；此外 **TV 值与本地 replica 值的差 ≤0.02%**（同 symbol、同 N，差异只能来自 EMA 初始化长度，须 ≥300 根预热） |
| 位置一致 | 用 TV 同 symbol 收盘价对 TV 两轨判位，与 `stated_position` 一致率 ≥97%；§6.5 状态转移日 100% |
| 记录 | `research/replica-tv-repro-<date>.md`：脚本、symbol、时区截图、逐日表、统计；不进 brief、不进 history |

未通过 §6.8 的 replica 不得进入 §6.6 Layer 2；§6.8 与 §6.3 / §6.5 任一不达即 fail，不得以「TV 数据源与本地不同」为由放宽。

### 6.9 分层真源硬验收（r2 新增）

正文见 §0B.4「硬验收」表：源隔离、冲突处理、自评守卫、边界跳变 ≤0.30%、fail-closed 三注入、一日一源、禁止事项。§6.9 与 §6.1–6.8 叠加生效；`formula_status` 每次升级都须重跑 §6.9 全表。

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
    "rail_source": "model",
    "rail_confidence": "derived|none",
    "formula_status": "replica_shadow|replica|author_confirmed",
    "source_transition": false,
    "system_signal_eligible": false,
    "signal_gate_ref": null,
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

规则：`fit_*` 与 `params_version` 为常量镶入，来源只能是过闸的 fit report；`bars_missing` 非空 → `fail` 且轨位 null（EMA 不得跨缺日递推）；两块 `status` 互相独立；history 每行同时含两块。（r2）`formula_status=hypothesis` 时**整块不得出现**在 JSON 与 history；`system_signal_eligible` 与 `signal_gate_ref` 为常量 `false` / `null`，任何写入其他值的路径须使进程非 0 退出（§0B.4 fail-closed 注入 iii）。

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
| （r1）409 对 / 312 相邻日 / 轨距 991→2434→3495 / 严格平行 9.6% / ≤50 56% | 复算 409 / 313 / 991→2434→3470 / 9.9% / 57.5% | **全部属实**；且这组数字本身就否定「Parallel Channel」 |
| （r1）最大断档 ~46d | PREVIEW 148d（2024-07-22→12-17）；corpus 2024-08..11 零篇 | **不属实**，须更正；影响 §3.2 覆盖表与 §4.2 断段 |
| （r1）repo 够不够拟合 | 对 1 参数辨识：409 点 ≫ 需要；对分段直线：样本再多也不够（模型错） | 够（H1）/ 不够且无意义（H0） |
| （r1）较像 TV Parallel Channel | 段内恒斜率、恒轨距两条假设均被数据否定 | **不成立**；机械化为 H0-TV 必跑必报 |
| （r1）不像 TV Linear Regression Channel（因重绘） | 真值确非回归通道，但「逐 bar 重算」恰是真值的特征 | 结论对、理由反；不列为候选也不列为对照 |
| （r1）徐小明通达信通道 ≠ 已核实 TV 脚本 | 与裁决无关 | 不需要核实；数据已选出模型族 |
| （r2）oracle 优先，日报只是搬运老猫自己的数 | 与 §3 真值序列同构 | **正确，采纳**；加 provenance / 异常打标 / 作者标签 / 冲突不取均值（B1–B2） |
| （r2）S39 `ema_percent_envelope`：EMA34 中轨 ×(1±0.018958) | 409 日碰撞：RMSE 0.46–0.55%，宽度残差 0.79%，2023-H2 太宽 +0.71 pt、2024-H1 太窄 −0.46 pt | **中轨对、宽度错**；k 是同语料宽度中位的一半，非独立证据；改 `EMA(H)/EMA(L)` 后宽度残差 0.12% |
| （r2）`formula_status="hypothesis"` 明确非终版 | 方向对 | **采纳并加严为四级梯子**；hypothesis 不触达读者（B4） |
| （r2）S40/S41 置信不足 fail-closed | 方向对；转述未给判据 | **采纳并写死三处**（数据 / 状态 / 信号层，B5）+ 三项注入测试（§6.9） |
| （r2）填补模型可含分段平行通道 | 只能以 H0-TV 机械化形式参赛 | 人工锚点版**不可 fail-closed**，不准入（B3） |

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
| （r1）不以 TV Parallel Channel 为验收对照 | 0.90 | H0-TV 在**事先钉死**的单一锚点规则下达到 §6.3 全部阈值且平均段长 ≥15 帖 → 改为并列候选，重开 §5.3 排序 |
| （r1）「分段斜率 + 可变轨距」只是下限 | 0.90 | 全语料 H0 以平均段长 ≥15 帖达到位置一致率 ≥97% 且残差曲率窗口占比 <30% |
| （r1）148d 为最大断档 | 0.97 | `laomao-posts.jsonl` 中存在 2024-08..11 的主讲人轨位帖（corpus-summary 未计入） |
| （r1）H1 可在 TV 两行复现 | 0.85 | §6.8 中 TV 值与本地 replica 差 >0.02%（同 symbol 同 N 预热 ≥300 根）→ 说明 EMA 定义或 bar 对齐有别，回 §2.4 第 1 步 |
| （r2）分层真源采纳 | 0.92 | 全语料 §6.1 后 `conflict` 行 >5% → oracle 层本身不可靠，需先解决抽取而非分层 |
| （r2）S39 宽度模型错、H1 压制 S39 | 0.90 | 用全语料 + 老猫所用交易所 + 半根 bar 对齐后，S39 族（N、k 放开）pooled RMSE ≤ H1 的 1.1 倍 **且** 宽度残差 ≤0.30% → 两族并列，§5.3 重排 |
| （r2）hypothesis 不得触达读者 | 0.85 | 原则方裁定 brief 可写带 `hypothesis` 标签的通道行 → §0B.3 B4 降为「可写、必标、仍禁 system_signal」，其余不变 |
| （r2）文首维持 REWORK | 0.90 | 原则方裁定「分层真源架构落地」即票面交付 → 文首改 PASS，但 §6 全部门槛转为 IMPL-GATE r3 的入场条件，一条不减 |

---

## 10. 非目标

- 不实现抽取器、拟合器、`schema_version: 3`、replica 块、brief 行；不改 r2 已 PASS 的任何文件与文案。
- 不替 Jimmy 或老猫确认公式；不裁 N 的最终值；不裁交易所归属。
- 不评估 DIF / 钝化 / 结构 / 正负角线；不做 3.0 系统。
- 不拉小时线、不做多交易所拉取（属 REWORK 执行面）。
- 不在 TradingView 上手绘 Parallel Channel 做「对照」（不可复现，§0A.2 裁决 3）；不核实徐小明通达信公式与任何 TV 脚本的对应关系。
- 不涉及下单、仓位或任何执行面；不产出 `system_signal`。

REWORK

# RECHECK：老猫真值通道 GATE r3 研究包复核 — 架构师裁决

> 裁决：**REWORK**（研究包层面的 residual REWORK，不是 REFUSE）。分层结论：**L0 抽取半部 · 数值轨位列 = Conditional PASS**（冻结为 L0 v1，可作评分靶；三项文书级条件见 §2.3）；**L0 · 标签列（`stated_*`）= REWORK**（`stated_position` 非空率 55.6% < §6.1 的 70%，且已见错标）；**模型半部 H1 = REWORK 维持**——不是因为模型族错，而是因为申请包里能拿来过 §6.3 的那份证据（半根 bar 报告）是**实现错误的产物**（§3.2），而能过的那份（lag0）按申请方与本文一致的口径**不得用作过关依据**；§6.5 实测 83.66% < 97% 未列入 blockers；§6.9 边界跳变实际可算而未算。H0 / H0-TV / H6 报表接受；shadow Layer 1 的对照 A（Donchian）**作废重跑**（§3.6 实现错误，21.5% 不成立，正确值 ≈43.8%）。§0C / §8 / §9 合规项全部核过：**PASS**。Donchian proxy brief、`last_btc_consensus.json`、brief 通道行、`schema_version: 3`：**一律仍禁止动**；`formula_status` 仍为 `hypothesis`。
> 对照物：`uploads/RECHECK-REQUEST.md`（sha d5da578d…）、`COMPLIANCE-CHECKLIST.md`（8fc93b18…）、`GATE-laomao-truth-channel-fit-2026-09-21.md` r3（PR [#8](https://github.com/licett/ai-workflow-kit/pull/8)，下称 GATE）、`README.md`、`truth_series/rails.jsonl`（4740a4a6…，410 行）+ `coverage.jsonl`（cccd9c32…，834 行）、`halfbar_alignment_protocol.md`、`venue_selection.md`、`replica-tv-repro-2026-09-21.md`、`shadow-L1-2026-09-21.md`、`tv_pine_ema_hl.pine`（56d26046…）、`out/` 十份 JSON、`RECHECK_SHA256SUMS.txt`。清单 18 项中 16 项上传件哈希逐一相符；`h0_report.json` / `h6_scan_full.json` / `compare_summary.json` / `extract_summary.json` 四份上传件**不在清单内**（§4 软项）。
> 方法：只读 uploads；在 `/tmp` 做 L0 结构核验与模型复算（不入库）；**一次**公开只读拉取 Bitstamp BTC/USD 日线（2022-01-01 起，1725 根）与小时线（2023-01-01..2025-07-05，22000 根，无缺小时；小时聚合 H/L 与日线逐日一致 400/400）。这是裁决所需的证据动作，用途只有两种：**复现申请包数字**（判定其是否成立）与**给出反证**；本文复算结果**不替代**申请方交付物——证据标准不对称：架构师复算足以**否决**一个数字，不足以**放行**一个数字，放行必须以申请方带 sha 的 `research/` 产物为准。未碰盒上任何文件；不改 py / README / JSON / history / brief；不产出 `system_signal`。
> 边界：research-only。本文只新增此一文件；不授权 promote、不授权 `replica_shadow`、不改 GATE 任何阈值（**不得改宽**是本次复核的前提，§5 逐条对表）。
> 日期：2026-09-21（Asia/Shanghai）。thread_ref = `GATE-laomao-truth-channel-fit-2026-09-21-r3`。

---

## 0. 总判

| 项 | 裁决 | 一句话 |
|---|---|---|
| 研究包整体（RECHECK 票面） | **REWORK** | 合规齐、结构齐、数字不齐：两处实现错误（半根 bar、Donchian 基线）、两处 §6.3 口径问题（lag0 不可作过关；同配置两个 RMSE）、一处 §6.5 未申报的 fail |
| L0 抽取 · 数值轨位列（`upper/lower/bar_date/provenance`） | **Conditional PASS** | 410 行、源隔离全 oracle、`formula_status` 全 null、`sender_id` 全等、无倒挂、`width_pct` 分母对、覆盖表 834 日连续、148d 断档、13752 只打标未改数；缺三项文书：§6.1 精度抽检记录、`edited` 字段修正、`post_without_rails` 列表 |
| L0 抽取 · 标签列（`stated_*`） | **REWORK** | `stated_position` 非空 228/410 = **55.6%**（门槛 ≥70%）；`stated_holding` 67.3%（≥50% ✓）；未审计，且 §6.5 不一致日里已见明显错标（2023-04-19 标 `below`，价格在上轨上方 5.9%） |
| 模型半部 H1（§6.3 / §6.5 / §6.8 / §6.9） | **REWORK 维持** | 半根 bar 报告是错的（0.83% = EMA 跑在每日 00–12h 半根 bar 上），lag0 不可作过关；正确构造下 H1 反而进入 §6.3 目标区（本文复算 0.0725%），但这是复核数字，不是申请包交付物，且暴露新的 §6.3 未达项（2023 留出比 2.04 > 1.5） |
| H0（§5.2 / §6.2） | **报表接受，§6.2 未齐（软）** | 10 帖 LOO RMSE 0.517% / 0.531%，结论「不可作真值」成立；缺 p90 / max / 曲率占比 / 位置一致率 / §4.2 切段平均段长 |
| H0-TV（§0A.2 (a)） | **接受** | 钉死 L=R=5；RMSE 12.27%、位置一致 44.8%、`pass_6_3=false`；缺「每段轨距」表（软） |
| H6（§0C.2 问 2） | **接受** | 网格搜索、未绑 0.018958、半年 k* 极差 0.51 pt > 0.2 pt → 常数 k 结构 fail；本文在正确半根 bar 口径下复算 H6 族最佳 0.4376%，仍是 H1 的 6 倍，§9 r2 反超条件**未触发** |
| shadow Layer 1（§6.6） | **对照 A 作废重跑；对照 B 接受** | Donchian 基线把确认 bar 算进了自己的窗口 → 永远 `inside` → 21.53% = oracle 中 `inside` 占比 87/404；A4 语义正确值 43.81%（与 GATE 预览 43.8% 一致）。H1 vs oracle 99.01% 复现成立 |
| §0C / §8 / §9 合规（A1–A12） | **PASS** | 两层、L1 只 H0 报表、无 k 绑定、hypothesis 只在 research/、Donchian 未动、生产文件 sha 前后相等 |
| Donchian proxy / `last_btc_consensus.json` / brief 换行 / `schema_version: 3` | **仍禁止动** | 本文不授权任何一项；写入证明接受（点时快照，§1 注） |
| `formula_status` | **`hypothesis` 不变** | 未过 §6.3（申请方证据口径）/ §6.5 / §6.8 / §6.9 任一 → 不得升 `replica_shadow` |

置信度：总判 REWORK 0.95；半根 bar 0.83% 为实现错误 0.97（逐 N 复现至小数点后 3 位）；Donchian 21.5% 为实现错误 0.97（同上）；正确半根 bar 下 H1 进入 §6.3 目标区 0.85（单交易所、架构师复算）；L0 数值列可冻结 0.90。

---

## 1. 合规核对（§0C / §8 / §9 ↔ COMPLIANCE-CHECKLIST A1–A12）

| # | 约束 | 申请方 | 本文核验 | 判定 |
|---|---|---|---|---|
| A1 | 两层 L0 + model，不三层 | PASS | 包内无 `L1 status=fitted` 产物；`rail_source` 枚举只见 `oracle` | **PASS** |
| A2 | L1 分段平行 = H0 报表 | PASS | `h0_report.json.kind = "H0_report_only"`，产物是误差表不是轨位 | **PASS** |
| A3 | 不绑 k=0.018958 | PASS | H6 四所网格 k∈[0.010,0.030] 步 0.0005，最佳 0.0185；`forbidden_bind_k` 字段在；`constant_k_structure_fail=true` | **PASS** |
| A4 | hypothesis 不进 brief / JSON / history | PASS | 所有产物路径在 `…/research/truth-channel-fit-2026-09-21/` 下；写入证明覆盖生产 JSON | **PASS**（history / brief 未在证明范围，见注） |
| A5 | Donchian brief / IMPL-GATE r2 不动 | PASS | 包内无 brief 文案、无 py 改动 | **PASS** |
| A6 | `rail_source=oracle`，`formula_status=null` | PASS | 410/410 · 410/410；`rail_confidence` 410 `explicit`、0 `conflict` | **PASS** |
| A7 | 最大断档 148d | PASS | 复算 gaps>7d：46 / 18 / 11 / **148**（2024-07-22→12-17）/ 9 | **PASS** |
| A8 | H1 EMA(H,N)/EMA(L,N) 必测 | PASS | 四所 × 2 对齐 × 26 个 N；最优一致 N=33 lag0 | **PASS**（对齐口径见 §3） |
| A9 | H0-TV 钉死锚点 | PASS | `pivot_rule left=5,right=5`；重画 63 次；不回写 | **PASS** |
| A10 | §6.8 Pine + 本地 replica | PASS / TV 后置 | Pine 9 行、v5、只有 `ta.ema(high,33)` / `ta.ema(low,33)` 两条 plot，sha 与清单一致 | **PASS**（本地表预热不足，§3.8） |
| A11 | §6.6 L1 做完、L2 后置 | PASS / L2 后置 | L1 文件在；对照 A 实现错误（§3.6） | **部分**：对照 B 接受，对照 A 重跑 |
| A12 | 不写生产 | PASS | `sha256_before == sha256_after == 594a20a7…`，`unchanged=true` | **PASS** |

注：A4 / A12 的证明是**点时快照**（单文件、单次 sha 比对），不是持续守卫；history 与 brief 未纳入证明。研究阶段可接受；进入 IMPL-GATE r3 时须换成 §0B.4 fail-closed 三注入的自动断言。

---

## 2. L0 抽取半部：逐项 §6.1

### 2.1 结构核验（全部通过）

| 检查 | 结果 |
|---|---|
| 行数 / 唯一 `bar_date_utc` / `message_id` 单调 | 410 / 410 / 是 |
| `sender_id` = 5129397609、`chat_id` = -1001737870653 | 410 / 410 |
| `rail_source` / `rail_confidence` / `formula_status` | oracle 410 / explicit 410 / null 410 |
| `upper ≤ lower` | 0 行 |
| `width_pct` = (U−L)/((U+L)/2)×100 | 410 行逐行相符（误差 <1e-4） |
| `bar_date_utc` = `sent_at_utc` 日期 | 410 / 410 |
| 发帖日 | 仅周一至周五 82/86/83/81/78；周末 0 |
| 发帖时刻 | 11h 55 · 12h 347 · 13h 6 · 14h 2（全部在 10:00–15:00Z，无 `off_hours`） |
| 正则 | P1 407 · P2 2 · P3 1；`extractor_confidence` 1.0 / 0.9 / 0.7 对应 |
| 异常 6 行 | 11029 / 11407 / 12126 / 13503 `speed_sign_mismatch`；11136 `low_confidence`（P3, 0.7）；**13752 `width_outlier`（U 96844 / L 95952 原样保留，未改数）** |
| §3.1 25 个字段 | 全部在场 |
| 覆盖表 | 834 行 = 2023-03-14..2025-06-24 每日历日一行、连续；`observed` 404 + `anomaly_excluded` 6 = rails 410 ✓；`no_post_weekend` 238、`no_post_gap` 185、`post_without_rails` 1 |
| §6.9 源隔离 | `rails.jsonl` 内无 model 行 ✓ |
| 溯源 | 410 个 `source_text_sha256` 两两不同；`corpus_snapshot_id` / `extractor_version` 齐 |

### 2.2 §6.1 逐项

| 指标 | 门槛 | 实测 | 判定 |
|---|---|---|---|
| 召回 | ≥99% | 410 / 410 含轨位关键词帖入表；`posts_without_rails=[]` | **PASS** |
| 精度 | 随机 40 帖 + 全部异常帖，人工核对 100% 逐字相等 | **未交付审计记录**；本文无语料，无法代核 | **未齐（文书级）** |
| 溯源 | `message_id` + sha + `sender_id` 全等 | ✓ | **PASS** |
| 不改数 | 与原文 diff 为空 | 无法核（语料不在包内）；13752 未改、`upper/lower` 皆整数原样 | **待审计记录一并覆盖** |
| 覆盖表 | 每日一行；observed = rails − 重复日 | ✓（见 §2.1） | **PASS** |
| 标签 `stated_position` 非空率 | ≥70% | **228/410 = 55.6%**（剔异常 225/404 = 55.7%） | **FAIL** |
| 标签 `stated_holding` 非空率 | ≥50% | 276/410 = 67.3% | PASS |

另两处不一致：
- `edited=true` **410/410**。字段退化为常量，无法证明「保留首版数值」（§3.1 / §4.4）。两种可能：抽取器凡有 `edit_date` 即写 true（应改为 `edit_date > sent_at_utc`），或语料本身只有终版文本（则应在 README 明示「首版不可得，数值为终版」）。须择一说明。
- `coverage.jsonl` 有 1 行 `post_without_rails`（2023-08-21，#11011），但 `extract_summary.posts_without_rails` 为空；416 帖 − 410 = 6 帖无轨位，覆盖表只落 1 日。§6.1 要求「漏网逐条列」，须补全 6 条去向（同日第二帖 / 无轨位 / 非主讲人）。

### 2.3 裁决

- **数值轨位列（`message_id / sent_at_utc / bar_date_utc / upper / lower / width / width_pct / anomaly_flags / rail_source / rail_confidence / source_text_sha256`）：Conditional PASS。** 立即效力：`rails.jsonl` sha `4740a4a6…` 冻结为 **L0 v1**，可作 §6.3 / §6.5 / §6.6 评分靶（本文 §3 所有复算即以它为靶）。解除条件（三项，均不需重抽）：(i) 精度抽检记录（40 随机 + 6 异常，逐字对照，附 `message_id` 与原文 sha）；(ii) `edited` 字段修正或声明；(iii) 6 条无轨位帖的逐条列表。任一抽检出现数值改写或 `sender_id` 混入 → 按 GATE §9 撤回 PASS。
- **标签列：REWORK。** 不作为 §6.5 的判据来源，直到：`stated_position` 非空率 ≥70%；标签精度抽检覆盖全部 33 个 §6.5 不一致日（§3.4）与全部 `stated_action` 非空帖；`stated_action` 语义修正——当前 72 个 `clear` 多为连续空仓日逐日重复（如 2023-05-09..06-20），这是**状态**不是**动作**，会把 §6.5 的「状态转移日」集合灌水。CARD 锚点 #10962 `stated_position=null`、#10968 `stated_holding=null` 亦须补。

---

## 3. 模型半部：申请包数字逐项复核

### 3.1 同一配置、两个 RMSE：预热长度伪影

| 来源 | Bitstamp N=33 lag0 | biasU / biasL | max \|res\| | OHLC 起点 |
|---|---|---|---|---|
| `h1_full_metrics.json` / `halfbar_alignment_result.json` / `tv_local_replica_compare.json` | **0.11394** | +0.0622 / −0.0188 | 0.670 | 2022-12-24（`venue_selection.md`，预热 80 根） |
| `compare_summary.json` H1_by_venue | **0.15600** | +0.0837 / −0.0012 | — | 2023-01-13（`ohlc_meta`，预热 60 根） |
| 本文复算，起点 2022-12-24 | 0.1139 | +0.0622 / −0.0188 | 0.670 | 复现前者 |
| 本文复算，起点 2023-01-13 | 0.1560 | +0.0837 / −0.0012 | **1.059** | 复现后者；max\|res\| 已 >1.0% |
| **本文复算，起点 2022-01-01（预热 ≥430 根，2022-06-01 起点结果相同 = 已收敛）** | **0.1221** | +0.0688 / −0.0132 | 0.670 | **规范值** |

读法：包内两个数都对，但都是预热伪影；收敛值 0.1221%。这本身不影响结论方向，却直接触犯 §6.8「须 ≥300 根预热」，并使 `tv_local_replica_table` 的前 27–33 个帖日与 TV 不可比（TV 从符号起点算起、已收敛）：80 根预热版逐日偏差最大 **0.231%**（2023-03-14），27 个帖日 >0.02%；60 根版最大 0.523%，33 日 >0.02%。**下次申请：全包同配置只允许一个数；OHLC 快照带 sha；起点 ≤2022-05-18。**

### 3.2 半根 bar 0.83% 是实现错误，不是模型证伪

数学上限：正确的半根 bar 值 `U_hb = α·H_partial + (1−α)·EMA_{D−1}`，与 lag0 值 `U_lag0 = α·H_full + (1−α)·EMA_{D−1}` 只差 `α·(H_full − H_partial)`；α = 2/34 = 0.0588，BTC 下午段振幅延伸典型 ≤1–3% → 逐日差 ≤0.06–0.18%。由三角不等式 RMSE_hb ≤ RMSE_lag0 + RMS(hb−lag0)，**正确构造下半根 bar RMSE 不可能从 0.11% 跳到 0.83%**。实测 RMS(hb−lag0) = 0.108%。

复现申请包数字（Bitstamp 小时线，EMA 递推**逐日**喂 00:00–11:59 半根 bar 的 H/L）：

| N | 申请包 top5 | 本文按「每日半根 bar 递推」复现 |
|---|---|---|
| 31 | 0.86621 | 0.8659 |
| 32 | **0.83261** | **0.8326** |
| 33 | 0.83353 | 0.8339 |
| 34 | 0.86752 | 0.8681 |

逐 N 吻合至小数点后 3 位。结论：`halfbar_alignment_result.json` 的构造是**把所有历史日都换成半根 bar 再跑 EMA**（通道被系统性压窄），而不是「已收整根 bar 递推到 D−1 + 用进行中半根 bar 走一步」。申请方在协议里自设的判据「半根 bar 落在 lag1 与 lag0 之间则 H1 族存活」在自己的数字上已经不满足（0.83 > 0.31 > 0.11），却没有触发排查。

正确构造（EMA 全 bar 递推至 D−1，最后一步用 D 日 00:00–11:59 的 H/L；预热 ≥430 根；n=404）：

| N | RMSE% | biasU / biasL | max \|res\| | 宽度残差 RMSE |
|---|---|---|---|---|
| 31 | 0.3834 | +0.178 / +0.208 | 1.151 | — |
| 32 | 0.2157 | +0.093 / +0.124 | 0.669 | — |
| **33** | **0.0725** | **+0.008 / +0.040** | **0.351** | **0.064** |
| 34 | 0.1439 | −0.077 / −0.044 | 0.424 | — |
| 35 | 0.3008 | −0.163 / −0.129 | 0.832 | — |

改用「递推至发帖所在小时」的 running H/L：N=33 → 0.0757%（结论不变）。§9 「N≈30（0.70）」一行的推翻条件（半根 bar 对齐后最优 N 落在 30±1 以外）**已触发：N=33**。GATE §2.4 第 1 步的猜想「真值 = 含进行中半根 bar」得到支持。

### 3.3 §6.3 逐行：三个口径并列

| 指标 | 门槛（最低 / 目标） | 申请包 lag0 | 复算 lag0（收敛） | 复算半根 bar（正确构造） | 判定（以申请方可交付口径为准） |
|---|---|---|---|---|---|
| pooled RMSE% (n≥400) | ≤0.20 / ≤0.10 | 0.114 | 0.122 | **0.0725** | lag0 不可作过关；半根 bar 待申请方重交 |
| \|bias_U\|, \|bias_L\| | ≤0.05 / ≤0.03 | **0.062** / 0.019 → **FAIL** | **0.069** / 0.013 → FAIL | 0.008 / 0.040 → 最低达标，目标未达 | 申请包口径 **FAIL**（未申报） |
| 逐年 RMSE% | 每年 ≤0.30 / ≤0.15 | 0.114 / 0.124 / 0.099 | 0.134 / 0.124 / 0.099 | 0.099 / 0.054 / 0.041 | 达标 |
| max \|res\| | ≤1.0（逐日解释）/ ≤0.6 | 0.670 | 0.670 | 0.351 | 达标；`compare_summary` 版 1.059 不达 |
| 参数稀疏 | 单一 (N, α) | ✓ | ✓ | ✓ | 达标 |
| N 稳健（N±1 增幅 ≥30%） | — | 包内**未报** N±1 | 32: +95% · 34: +41% | 32: +197% · 34: +98% | 申请包未交；复算达标 |
| 留出（两年拟合、第三年验证 ≤1.5×） | — | 1.004 / 1.147 / 0.834 ✓ | — | **2023: 2.04 ✗** · 2024: 0.67 · 2025: 0.51 | 正确口径下**出现新的未达项** |

关于 2023 留出比：正确半根 bar 下误差不再被对齐噪声抹平，年际异质性显露——2023 年 0.099% vs 其余 0.048%；最大残差前五日全部落在 **2023-03-24..30**（0.28–0.35%，序列起始两周），2023 年 biasL +0.085%。可证伪假设：2023-03 银行危机期 USD 现货所（Bitstamp / Coinbase）与 USDT 所之间的基差。**检验办法在包内已有的数据里**：用 OKX BTC-USDT 小时线重跑半根 bar，看 2023-03 残差是否收敛。若任何单一交易所都做不到 ≤1.5×，§6.3 留出行不过，不得因此放宽。

### 3.4 §6.5：83.66% 是真的，但它先是标签问题

- 复现：`stated_position ∈ {above, inside, below}` 共 202 帖（`touching` 24 帖不计），以 Bitstamp `close(D−1)` 对 **oracle** 轨位分类，一致 169/202 = **83.66%**；对 H1 半根 bar 轨位分类同为 83.66%——即 H1 与 oracle 在这 202 日上分类完全同向，**差的不是模型，是标签或价格参照**。
- 33 个不一致日两类：(a) 明显错标，如 2023-04-19 标 `below` 而价格在上轨上方 5.9%、2023-09-21 标 `below` 而在上轨上方 0.3%；(b) 价格在上轨下方 0.9–2.2% 却标 `above`（2023-04-26/27、05-08、06-01、09-15/18/19、10-16、2024-01-29），与 GATE §6.5 预览提到的 2023-04-26 同型——这类不可能是 0.1% 量级的交易所差，更像 `stated_position` 正则把「站上通道 / 通道上方」映射错了层级，或作者说的是发帖时刻价格。
- 诊断（**不作放行依据**，GATE 定义是 `close(D−1)`）：改用发帖小时 Bitstamp 开盘价对 oracle 轨位 → 184/202 = **91.09%**。仍 <97%，剩余差额只能靠标签审计解释。
- 状态转移日 100% 一致性：**未跑**。当前 `stated_action` 的 98 条里 72 条是连续 `clear`，转移集合须先按「变化」重算（§2.3）。
- 若申请方认为 §6.5 的价格参照应改为发帖时刻价格：那是 **GATE r4 增补**，须另申请并先交标签审计；RECHECK 不改定义。

### 3.5 §6.9 边界跳变：可算，已算

定义（§0B.4）：每个 >7d 缺口两端的 oracle 日，`|model − oracle|` 两轨均 ≤0.30%。2025-02-05（#13503）是 `speed_sign_mismatch` 异常行，缺口右端取首个干净 oracle 日 2025-02-06。N=33，Bitstamp，单位 % of mid：

| 缺口端 | lag1 (U / L) | lag0 (U / L) | 半根 bar (U / L) |
|---|---|---|---|
| 2023-07-07 | −0.165 / −0.176 | +0.016 / +0.049 | −0.014 / +0.049 |
| 2023-08-22 | **+0.507 / +0.614** | −0.071 / +0.007 | −0.071 / +0.141 |
| 2023-09-28 | +0.034 / +0.028 | +0.120 / +0.032 | −0.037 / +0.032 |
| 2023-10-16 | −0.154 / −0.041 | **+0.396** / +0.033 | −0.022 / +0.033 |
| 2024-02-08 | −0.260 / **−0.351** | +0.069 / 0.000 | −0.029 / 0.000 |
| 2024-02-19 | **−0.711 / −0.805** | +0.004 / +0.006 | +0.004 / +0.035 |
| 2024-07-22 | **−0.467 / −0.513** | −0.029 / −0.026 | −0.029 / +0.011 |
| 2024-12-17 | **−0.621 / −0.687** | +0.090 / +0.078 | +0.037 / +0.101 |
| 2025-01-27 | −0.129 / −0.039 | −0.046 / −0.031 | −0.046 / −0.031 |
| 2025-02-06 | — | — | +0.022 / −0.009 |
| **判定** | 5 端不达 | **1 端不达（2023-10-16 U）** | **20/20 达标，max 0.141** |

申请包把「日间 |ΔU|+|ΔL| p95 = 3.42%」标注为非 §6.9 指标是对的；但 §6.9 本身用包内 `rails.jsonl` + 日线即可算，不存在「无双源交接序列」的障碍——交接日就是缺口两端的 oracle 日。**下次申请必须交此表**（半根 bar 口径）。

### 3.6 shadow Layer 1 对照 A：Donchian 基线实现错误

| 实现 | 一致率 | 混淆（oracle→don） | above / below 召回 | 宽度中位 |
|---|---|---|---|---|
| 申请包（自称「A4 exclude confirm bar」） | 21.53% | above→inside 211、below→inside 106、inside→inside 87；**above→above 0、below→below 0** | 0% / 0% | 12.107% |
| 本文·窗口**含**确认 bar D−1（20 根含自身） | **21.53%** | **211 / 106 / 87**（逐格相同） | 0 / 0 | — |
| 本文·A4 正确：窗口 = D−1 之前 20 根，判 close(D−1) | **43.81%**（177/404） | above→above 59、above→inside 152、below→below 35、below→inside 71、inside→below 4、inside→inside 83 | 27.9% / 33.0% | 12.107% |
| GATE §2.2 预览（409 行） | 43.8% | 59 / 153 / 35 / 73 / 4 / 85 | 27.8% / 32.4% | 12.24% |

确认 bar 若在自己的窗口内，`close ≤ max(window)` 恒成立，proxy 永远判 `inside`，一致率退化为 oracle 里 `inside` 的占比（87/404 = 21.53%）。这不是「proxy 更差」，是基线没跑对。**shadow-L1 的对照 A 全部数字作废**；重跑须附断言 `above→above > 0 且 below→below > 0`。对照 B（H1 vs oracle 99.01%、宽度中位 3.727% vs 3.640%）复现成立。

### 3.7 H0 / H0-TV / H6

- **H0**：10 帖窗 LOO，pooled 0.517%（各自斜率）/ 0.531%（平行），22 个样本窗里 4 个 >0.85%。「不可作真值」成立且不可逆。但 §6.2 明列的 p90 / max / 残差曲率占比 / 位置一致率 / 按 §4.2 速度符号切段的平均段长**均未报**；`gap_segments` 是 >7d 断段（6 段），不是 §4.2 切段。补齐即可，不影响结论。
- **H0-TV**：钉死规则、63 次重画、RMSE 12.27%、位置一致 44.8%，`pass_6_3=false`。缺「每段轨距」与 313 个相邻日对上的斜率一致性（§0A.2 (a)）。软项。
- **H6**：三个全跨度所最佳均为 N=34、k=0.0185、0.4553–0.4657%（lag0；Kraken 120 点 0.4167%，只作旁证）；半年真值 k* 极差 0.51 pt > 0.2 pt → 常数 k 结构 fail ✓。本文在正确半根 bar 口径下扫 N 26–41 × k 0.010–0.030：最佳 **0.4376%**（N=34，k=0.0185），仍为 H1 半根 bar 0.0725% 的 6 倍 → §9 r2「S39 族 ≤ H1 的 1.1 倍且宽度残差 ≤0.30%」反超条件**未触发**，H1 压制 H6 的结论在正确对齐下更强。

### 3.8 §6.8 Pine 与本地 replica

- Pine：v5，9 行，只有 `ta.ema(high, N)` / `ta.ema(low, N)` 两条 plot，sha `56d26046…` 与清单一致。合 §6.8 脚本要求。`N = 33` 目前是研究值，不是「过闸的 `params.n`」。
- 本地 EMA 定义「SMA 种子 + α=2/(N+1) 递推」与 Pine `ta.ema` 参考实现一致；但 TV 从符号首根 bar 起算、已收敛，本地只预热 80 根 → 27 个帖日（序列起始段）逐日差 >0.02%（§3.1）。**本地表须以 ≥300 根预热重生成后，TV 对照才有意义。**
- TV live 导出：未做（无 TV 会话）。分类见 §4。

---

## 4. Blockers 分类

申请方五条 + 本文新增四条。「硬挡」= 下次 RECHECK 前必须交齐，否则仍 REWORK；「Conditional」= 研究包证据 PASS 可不含，但作为 `replica_shadow` / IMPL-GATE r3 的入场硬条件写入；「软」= 补齐即可，不阻塞。

| # | Blocker | 性质 | 分类 | 下次要交什么 |
|---|---|---|---|---|
| 1 | TV live §6.8 导出未做（仅本地 replica） | 环境依赖 | **Conditional**（研究包）/ **硬挡**（进 `replica_shadow` 前） | 本地表 ≥300 根预热重生成（现在就做）；TV 导出记录 `research/replica-tv-repro-<date>.md` 含时区截图、逐日表、\|TV−local\| ≤0.02% |
| 2 | Layer 2 盒上 ≥14d shadow 后置 | 按 GATE 设计本就在 `replica_shadow` 之后 | **Conditional**（正确顺序：L1 → §6.3/6.5/6.8/6.9 → IMPL-GATE r3 → replica_shadow → L2） | 无需在研究包内交；不得提前把 replica 块写进 history 来「起算」 |
| 3 | 半根 bar 0.83% ≫ lag0 0.11% | **实现错误**（§3.2） | **硬挡** | 正确构造重跑 Bitstamp + OKX + Coinbase 小时线；断言逐日 `U_hb ≤ U_lag0`、`L_hb ≥ L_lag0`、RMS(hb−lag0) ≤ α·RMS((H_full−H_partial)/mid)；N 20–45 全表；以半根 bar 为**主口径**，lag0 只作上界、lag1 只作因果下界；预热 ≥300 根 |
| 4 | 作者平台收盘不可用，用 Bitstamp | 数据不可得 | **Conditional**（97% / 100% 阈值不放宽） | 先做 §2.3 标签审计；再按 GATE 定义 `close(D−1)` 报 §6.5，每个不一致日附 ≥3 所收盘差与半根 bar 解释（GATE 原文允许「可证伪的解释」）；发帖时刻价格口径只作诊断附表；改定义须另开 GATE r4 |
| 5 | §6.9 源切换边界跳变未测 | **可算未算**（§3.5） | **硬挡**（低成本） | 交 §3.5 同格式表，半根 bar 口径，含 2025-02-06 替代异常日；lag0 的 2023-10-16 U +0.396% 一并记录 |
| 6（新增） | shadow L1 对照 A Donchian 实现错误 | 实现错误（§3.6） | **硬挡** | 重跑 A4 语义，附 `above→above>0 && below→below>0` 断言；预期 ≈43.8% / 59 / 35 |
| 7（新增） | §6.5 实测 83.66% < 97%、转移日 100% 未跑，均未列 blockers | 未申报的 fail | **硬挡** | 见 #4；转移日集合按「变化」重算后再跑 |
| 8（新增） | §6.3 bias_U 0.062% > 0.05%（lag0）、同配置双 RMSE、N±1 未报、2023 留出比 2.04 | 口径与报告缺项 | **硬挡** | 全包单一规范流水线 + OHLC 快照 sha；半根 bar 口径下报 bias / N±1 / 留出；2023 留出 >1.5× 须给出可证伪解释并用 OKX-USDT 复检 |
| 9（新增） | L0 §6.1 三项文书 + 标签列 | 文书 / 标签质量 | 数值列 **Conditional**；标签列 **硬挡**（§6.5 依赖它） | §2.3 |
| 软 | §6.2 H0 报表缺项；H0-TV 缺每段轨距；四份 JSON 不在 SHA 清单；第 4 个全跨度交易所（Binance BTCUSDT 或等价 USDT 所）缺、Kraken 120 点不可替 | 报告完整性 | 软 | 补齐；清单覆盖全部 out/ 与脚本 |

---

## 5. 下次申请门槛（只列未齐硬项；阈值一条不减）

1. **半根 bar 报告重交**（#3）：正确构造、三条断言、三所小时线、N 20–45 全表、预热 ≥300 根、OHLC 快照 sha。主口径 = 半根 bar。
2. **§6.3 全表在半根 bar 口径下重报**（#8）：pooled RMSE、两轨 bias、逐年、max\|res\| 逐日解释、N±1 增幅、三折留出。2023 折若 >1.5× 须交 OKX-USDT 复检结果与解释；解释不成立即 §6.3 不过。
3. **§6.9 边界跳变表**（#5）：§3.5 格式，半根 bar 口径。
4. **shadow L1 重跑**（#6）：对照 A 修正 + 断言；对照 B 沿用。
5. **L0 三项文书**（#9 数值列）：精度抽检记录、`edited` 修正/声明、6 条无轨位帖列表。
6. **标签列 REWORK**（#9 标签列）：`stated_position` ≥70%；33 个不一致日 + 全部 `stated_action` 帖逐条审计；`stated_action` 改为动作语义；CARD 锚点字段补齐。
7. **§6.5 按 GATE 定义重报**（#7 / #4）：97% 与转移日 100%，每个不一致日附 ≥3 所收盘差 / 半根 bar 解释；发帖时刻口径只作附表。
8. **全包数字唯一**：同 (venue, N, alignment) 在任何文件里只允许一个值；`compare_summary` 与 `h1_full_metrics` 对齐。
9. **§6.8 本地表重生成**（#1 的可立即做部分）。
10. SHA 清单覆盖全部交付件（含四份 JSON、`tv_local_replica_table.jsonl`、两个脚本）。

满足 1–10 且数字落在 §6.3 门槛内 → 下次 RECHECK 可裁「研究包证据 PASS（票面仍 REWORK 直到 §6.8 TV live 与 §6.9 实现层三注入齐）」。**任何一条以「数据源不同」「零模型」「时间不够」为由放宽 → 直接 REWORK。**

---

## 6. 明确不变项

| 对象 | 状态 | 依据 |
|---|---|---|
| Donchian proxy brief 固定行 / IMPL-GATE r2 PASS 面 | **仍禁止动** | GATE §0「proxy 契约不变」；本文对照 A 作废不影响 r2 |
| `data/last_btc_consensus.json` | **仍禁止写** | A12 通过；研究脚本继续不得触碰 |
| brief 通道行 | **仍禁止换行**；不得并列两条 | GATE §7.3 第一阶段；§7.4 不授权 |
| `schema_version: 3` / `trend_channel_replica` 块 / replica 进 history | **不授权** | 需 IMPL-GATE r3 |
| `formula_status` | **`hypothesis`**；只存在于 `research/` | §0B.3 B4；未过 §6.3（申请方口径）/ 6.5 / 6.8 / 6.9 |
| `system_signal_eligible` | 常量 `false` | §0B.4；全部模型级别恒禁 |
| L1 分段平行拟合 | 不作源、不进 brief、不进 shadow、不作标签 | §0C.2 问 1 / 问 4；本次 H0 0.52% 再证 |
| k = 0.018958 | 禁绑；H6 只作对照 | §0C.2 问 2；半根 bar 口径下仍被 H1 6 倍压制 |
| `missing_inputs` 字面 `"trend_channel (LaoMao 2.0 original)"` | 必含 | §0B.4 禁止事项 |
| L0 `rails.jsonl` sha 4740a4a6… | **冻结为 L0 v1**（本文唯一新增的效力） | §2.3 |

---

## 7. 对 GATE §9 置信表的影响（记录，不改 GATE 正文）

| GATE §9 结论 | 原置信 | 本次证据 | 走向 |
|---|---|---|---|
| H1 = EMA(H/L) 族正确 | 0.80 | 正确半根 bar 0.0725%，V 形更尖（±1 → +98% / +197%），边界跳变 20/20 | **上调**（单所；待申请方三所复现） |
| N≈30 | 0.70 | 半根 bar 最优 N=33，落在 30±1 之外 | **推翻 → N=33（Bitstamp）** |
| proxy 位置一致率 43.8% | 0.85 | A4 正确实现复算 43.81%；包内 21.5% 为实现错误 | **再确认** |
| 148d 为最大断档 | 0.97 | 全量 410 行复算一致 | 再确认 |
| 抽取半部 PASS | 0.90 | 结构全过；缺审计记录；标签列不达 | 数值列 Conditional PASS；标签列 REWORK |
| S39 宽度错、H1 压制 | 0.90 | 半根 bar 口径 H6 最佳 0.4376% vs H1 0.0725% | 再确认 |
| 总判 REWORK | 0.92 | 见 §0 | 维持 |

新增待 GATE r4 处理的定义问题（本文不裁）：§6.5 位置一致率的价格参照（`close(D−1)` vs 发帖时刻价）；§6.9 缺口端为异常行时的替代规则（本文用首个干净 oracle 日）。

---

## 8. 本文数字的复现协议

- 数据：Bitstamp 公开 API `ohlc/btcusd` step=86400 自 2022-01-01（1725 根，无缺日）；step=3600 自 2023-01-01 至 2025-07-05（22000 根，无缺小时）。日线 H/L 与小时聚合 H/L 在 400 个帖日上逐日一致（差 <0.05%）。
- 靶：`rails.jsonl` 剔 `anomaly_flags` 非空 6 行 → 404 行；残差以 `(U+L)/2` 为分母，单位 %。
- EMA：SMA(N) 种子 + α=2/(N+1) 递推，自 2022-01-01 起（2022-06-01 起点结果相同）。
- lag1 = EMA 至 D−1；lag0 = EMA 至 D（整根）；半根 bar = EMA 至 D−1 后用 D 日 00:00–11:59 小时 H/L 走一步（变体：至发帖小时）。
- Donchian A4：确认 bar D−1，窗口 = 其前 20 根收盘，判 `close(D−1)`；错误变体 = 窗口含 D−1。
- §6.5：`stated_position ∈ {above, inside, below}`，价格 = Bitstamp `close(D−1)`（GATE 口径）或发帖小时开盘价（诊断）。
- 脚本在 `/tmp/recheck/`（不入库）；任何人按上述七条可在数分钟内复现全部表格。

---

## 9. 非目标

- 不实现抽取器修正、半根 bar 修正、Donchian 修正；不代申请方生成任何 `research/` 交付物。
- 不裁 N 的最终值（N=33 是 Bitstamp 单所结果）、不裁交易所归属、不确认作者公式。
- 不改 GATE r3 任何阈值与定义；§7 列出的定义问题留给 GATE r4。
- 不拉 OKX / Coinbase 小时线（属 REWORK 执行面）。
- 不涉及下单、仓位、`system_signal`。

---

## ACK

```text
HANDOFF
from: architect
to: research-executor
intent: ACK
thread_ref: GATE-laomao-truth-channel-fit-2026-09-21-r3
verdict: REWORK (residual; not REFUSE)
layers:
  - L0 rails numeric columns: Conditional PASS -> frozen as L0 v1 (sha 4740a4a6...), 3 paperwork conditions (sec 2.3)
  - L0 stated_* labels: REWORK (55.6% < 70%; unaudited; mislabels found)
  - H1 model half: REWORK (halfbar report = implementation bug; lag0 not admissible; sec 6.5 83.66% unreported; sec 6.9 computable and uncomputed)
  - H0 / H0-TV / H6: accepted (H0 sec 6.2 fields missing, soft)
  - shadow L1: contrast A (Donchian) void, rerun with A4 assertion; contrast B accepted
  - compliance 0C/8/9 (A1-A12): PASS
hard_blockers: #3 halfbar rerun, #5 sec 6.9 table, #6 Donchian rerun, #7 sec 6.5 per GATE definition, #8 sec 6.3 single canonical pipeline + bias/N±1/holdout, #9 label column
conditional_deferred: #1 TV live (local table regen now), #2 Layer 2 (after replica_shadow only), #4 author-platform closes (multi-venue explanation table; thresholds unchanged)
unchanged: Donchian proxy brief; last_btc_consensus.json; brief channel line; schema_version 3; formula_status=hypothesis; system_signal_eligible=false
next_gate: sec 5 items 1-10 complete -> RECHECK r2
```

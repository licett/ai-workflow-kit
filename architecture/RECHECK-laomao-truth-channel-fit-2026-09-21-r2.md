REWORK

# RECHECK r2：老猫真值通道 GATE r3 — 硬挡清项后再验（架构师裁决）

> 裁决：**REWORK**（residual；不是 REFUSE，也不是 Conditional PASS）。prior RECHECK（PR [#9](https://github.com/licett/ai-workflow-kit/pull/9)，下称 r1）列出的**实现层硬挡全部清掉并经本文独立复算成立**：半根 bar 构造已是「全 bar 递推至 D−1 + 半根一步」（§1）；Donchian shadow 窗口已排除确认 bar（§2）；§6.9 边界跳变 10/10（§3）；L0 三项文书齐（§5）。但票面不能改判：§6.3 **留出行**（最低门槛，非目标）2023 折 2.038 > 1.5 未过且未交 OKX-USDT 半根复检；§6.5 83.66% < 97%，转移日 100% 未跑；L0 标签列 55.6% < 70%。这三项在 r1 里就是硬挡，本轮申请方也如实申报未清——**阈值一条不动，所以票面只能是 REWORK**。分层：**L0 数值轨位列 Conditional PASS → PASS，冻结为 L0 v1 确认**（sha `4740a4a6…` 未变，三项解除条件已履行）；**L0 标签列 REWORK 维持**；**模型半部 H1 REWORK 维持，但范围收窄**至 §6.3 留出行 + §6.5 + §6.8 TV live；shadow Layer 1 对照 A 作废撤销、43.81% 接受。`formula_status` 仍为 `hypothesis`；H1 **仍不得进 brief / JSON / history**。Donchian proxy brief、`last_btc_consensus.json`、brief 通道行、`schema_version: 3`：**一律仍禁止动**。
> 对照物：`uploads/REWORK-CLEARANCE.md`（sha 9960295e…）、`RECHECK-REQUEST.md`（3802f9ee…）、`RECHECK-prior-r1.md`（44597fc0…，= PR #9 正文）、`GATE-laomao-truth-channel-fit-2026-09-21.md` r3（3d855b65…，PR [#8](https://github.com/licett/ai-workflow-kit/pull/8)，下称 GATE）、`COMPLIANCE-CHECKLIST.md`（8fc93b18…，与 r1 同一份）、`halfbar_alignment_protocol.md`（9b7d1b6e…）、`venue_selection.md`（a5a43654…，与 r1 同一份）、`shadow-L1-2026-09-21.md`（08f2c7d2…）、`truth_series/rails.jsonl`（**4740a4a6…，410 行，与 r1 冻结 sha 相同**）+ `coverage.jsonl`（cccd9c32…，834 行）、`out/` 九份 JSON（`halfbar_alignment_result` 0c86fefd… / `h1_full_metrics` 53f2f2f6… / `boundary_jump_6_9` 4fef5fc1… / `shadow_L1_summary` 291f2144… / `sec65_stated_position` 1ead6512… / `l0_spot_check` f5e974c3… / `l0_edited_declaration` 57e200f4… / `l0_posts_without_rails` 09afb7be… / `production_write_proof` 0f4cd90c…）、`rework_summary.json`（eca4d36e…）。**未上传**：`RECHECK_SHA256SUMS.txt`、N 20–45 全表文件、`tv_local_replica_table.jsonl` 重生成版、`compare_summary.json`（见 §8 软项）。
> 方法：只读 uploads；在 `/tmp` 独立重实现三种对齐 + Donchian 两种窗口语义 + §6.9 + §6.5 + L0 结构核验（不入库）；**一次**公开只读拉取 Bitstamp BTC/USD 日线（2022-01-01..2025-07-05，1282 根，无缺日）与小时线（2023-01-01..2025-07-05，22008 根，917 日 × 24 小时无缺；小时聚合 H/L 与日线在 404 帖日逐日相等）。证据标准与 r1 相同且不对称：本文复算足以**否决**一个数字，也足以**确认申请方交付物与其声明的构造一致**；放行仍以申请方带 sha 的 `research/` 产物为准。未碰盒上任何文件；不改 py / README / JSON / history / brief；不产出 `system_signal`。
> 边界：research-only。本文只新增此一文件；不授权 promote、不授权 `replica_shadow`、不改 GATE 任何阈值与定义（**不得改宽**是前提，§7 逐条对表 r1 §4/§5）。r1 §7 留给 GATE r4 的两个定义问题（§6.5 价格参照、§6.9 缺口端异常替代规则）本文不裁。
> 日期：2026-09-21（Asia/Shanghai）。thread_ref = `GATE-laomao-truth-channel-fit-2026-09-21-r3`。

---

## 0. 总判

| 项 | r1 裁决 | **r2 裁决** | 一句话 |
|---|---|---|---|
| 研究包整体（票面） | REWORK | **REWORK（residual）** | 实现层硬挡 #3 / #5 / #6 / #8-核心 / #9-文书 全清且复算成立；§6.3 留出行、§6.5、标签列三项仍 FAIL，阈值不动 → 票面不变 |
| L0 数值轨位列 | Conditional PASS（冻 v1，三项文书待补） | **PASS · L0 v1 冻结确认** | sha `4740a4a6…` 与 r1 冻结值逐字节相同；§6.1 抽检记录 46/46、`edited` 声明、6 条无轨帖三项已交且自洽（§5）。标签 REWORK 今后**不得改动数值列**，见 §9.1 版本规则 |
| L0 标签列（`stated_*`） | REWORK | **REWORK 维持** | `stated_position` 非空 228/410 = 55.6%（本文复数相同）；宽正则诊断 66.1% 仍 <70%；33 个不一致日未审计；`stated_action` 72 个 `clear` 中 58 个是连续重复（状态非动作）；CARD 锚点 #10962 position / #10968 holding 仍 null |
| 模型半部 H1 | REWORK（半根报告是实现错误） | **REWORK 维持，范围收窄** | 半根构造正确（§1，本文逐项复现至 1e-15）；§6.3 除留出行外全部最低门槛达标、多数目标达标（§4.1）；**留出 2023 折 2.038 > 1.5 FAIL**，OKX-USDT 半根复检未交（只交 lag0 日线 proxy 1.216，按 r1 口径不可作过关）；§6.5 83.66% FAIL；§6.8 TV live 未做 |
| shadow Layer 1 | 对照 A 作废重跑；B 接受 | **对照 A 接受（43.81%）；B 接受（99.01%）** | A4 窗口已排除确认 bar：混淆 59 / 152 / 35 / 71 / 4 / 83（above→above / above→inside / below→below / below→inside / inside→below / inside→inside）与本文逐格相同；含确认 bar 的错误变体复现 21.53% / 211/106/87，证明旧数之因与新数之正（§2） |
| §6.9 边界跳变（模型层） | 可算未算 → 硬挡 | **CLEARED** | 10/10 端点 ≤0.30%，max 0.141%（2023-08-22 L），与本文逐端相同至小数点后 3 位；2025-02-05 异常端按首个干净 oracle 日 2025-02-06 替代（r1 同规则）；lag0 的 2023-10-16 U +0.396% 一并记录 ✓ |
| §0C / §8 / §9 合规（A1–A12） | PASS | **PASS 维持** | 生产 sha 前后 `594a20a7…` 相等，`mtime` 04:44:50Z 早于 rework 运行时刻 06:00Z；hypothesis 只在 `research/`；无 k 绑定；Donchian brief 未动 |
| Donchian proxy / `last_btc_consensus.json` / brief 通道行 / `schema_version: 3` | 仍禁止动 | **仍禁止动** | 本文不授权任何一项（§11） |
| `formula_status` | `hypothesis` | **`hypothesis` 不变** | §6.3 留出行 / §6.5 / §6.8 任一未过 → 不得升 `replica_shadow`；H1 不进 brief |

置信度：票面 REWORK 0.96；半根构造正确 0.98（top5 五个 N × 8 字段全部复现至 ≥4 位小数，含 r1 未公开的逐年 / 宽度 / 留出字段，排除粘贴；本文 N 20–45 全扫单谷 33）；Donchian A4 正确 0.98；§6.9 10/10 成立 0.97；L0 数值列可冻 0.93；2023 留出 FAIL 不可由「序列起始两周」单独解释 0.85（§4.2）。

---

## 1. 半根 bar 构造：独立核验（防再交错实现）

### 1.1 协议文本

`halfbar_alignment_protocol.md` 的规范式：`EMA_H[i]` 用**全日 bar** 递推；对帖日 D（索引 i）：`U_hb(D) = α·H_partial(D, 00–11Z) + (1−α)·EMA_H[i−1]`。并明文把「把所有历史日换成半根 bar 再跑 EMA」列为 **Forbidden**。四条断言：Uh≤U0 / Lh≥L0；RMS(hb−lag0) ≤ α·RMS(H_full−H_partial)；预热 ≥300；留出同管线。**协议与 r1 §3.2 给出的正确构造一致。** 协议对了不等于代码对了，下面看数字。

### 1.2 数字一致性：申请包 vs 本文独立实现（Bitstamp，n=404，预热自 2022-01-01）

| N | 申请包 RMSE% | **本文** | biasU / biasL（申请包 → 本文） | max\|res\| | 宽度残差 | 逐年 2023 / 2024 / 2025（本文） |
|---|---|---|---|---|---|---|
| 31 | 0.38341 | **0.38341** | +0.1781 / +0.2084 → 同 | 1.1512 → 同 | 0.0677 → 同 | 0.4145 / 0.4242 / 0.2640（申请包同） |
| 32 | 0.21570 | **0.21570** | +0.0934 / +0.1244 → 同 | 0.6689 → 同 | 0.0637 → 同 | 0.2429 / 0.2310 / 0.1407（同） |
| **33** | **0.07253** | **0.07253** | +0.0084 / +0.0402 → 同 | 0.3510 → 同 | 0.0637 → 同 | 0.0987 / 0.0536 / 0.0412（同） |
| 34 | 0.14386 | **0.14386** | −0.0770 / −0.0443 → 同 | 0.4235 → 同 | 0.0675 → 同 | 0.1444 / 0.1612 / 0.1179（同） |
| 35 | 0.30076 | **0.30076** | −0.1628 / −0.1289 → 同 | 0.8319 → 同 | 0.0740 → 同 | 0.2989 / 0.3467 / 0.2344（同） |

- N 20–45 全扫（本文）：单谷 V 形，最优 **N=33**；N=20 → 2.46%，N=45 → 1.83%。申请包只上传 top5，全表见 §8 软项。
- 同 N=33 三对齐（本文 / 申请包）：lag1 0.43513 / 0.43513；lag0 **0.12209 / 0.12209**；halfbar 0.07253 / 0.07253。lag0 = 0.1221 正是 r1 §3.1 判定的「预热收敛规范值」（起点 2022-01-01），与 r1 指出的两个伪影值 0.1139 / 0.1560 均不同 → **单一规范管线 + 预热 437 根**（2022-01-01→2023-03-13 恰 437 日）确认。
- 逐年、留出（§4.2）、N±1（32: +197.4%；34: +98.3%）全部相同。
- **排除粘贴**：r1 只公开了 N=31–35 的 RMSE / bias / max 与 N=33 的宽度残差；申请包 top5 里每个 N 的逐年 RMSE、宽度残差，以及留出三折的 train/test RMSE 均与本文独立实现相同至 ≥4 位小数，这些 r1 没有公开，无处可抄。

### 1.3 错误构造复现（确认旧数之因，且新数不是它）

本文按 r1 §3.2 的「逐日半根 bar 递推」变体重跑：N=31 0.8667 / **N=32 0.8324** / N=33 0.8321 / N=34 0.8645（r1 复现 0.8659 / 0.8326 / 0.8339 / 0.8681；本文小时线自 2023-01-01 起、2022 年保留全 bar，故第 3 位起微差）。申请包本轮 0.0725 与此变体相差 11 倍，**新数不可能来自旧构造**。

### 1.4 断言的读法（一处需要申请方知道的数学事实）

正确构造下 `U_hb − U_lag0 = α·(H_partial − H_full)` **逐日恒等**（两者共用同一个 `EMA_{D−1}` 状态），因此断言 2 的两边必然**相等**而不只是「≤」：本文 404 帖日 RMS(hb−lag0) = 0.10804% = α·RMS(H_full−H_partial) = 0.10804%（相等至 1e-16）；申请包 0.10302 = 0.10302，同样相等。**这正是构造正确的签名**——若仍是旧构造，hb 与 lag0 不共享状态，左边会是 ≈0.8%，断言直接爆。保留该断言，但请在协议里改写为「恒等式核对（|左−右| < 1e-9）」，比「≤」更能防止未来出现「碰巧 ≤」的错误实现。

软项：申请包断言块的样本不是 404 帖日（本文 404 日为 0.1080 / 1.8367；申请包 0.1030 / 1.7514；对 917 个小时线全日算为 0.0972 / 1.6526，皆不吻合，推测为其 942 个 partial 日）。请声明样本。不影响判定。

### 1.5 对齐变体（信息，不改口径）

半根递推至发帖小时（不含发帖小时）：N=33 → 0.0726%；含发帖小时：0.0757%。与固定 00–11Z 口径结论相同；主口径维持 `halfbar_12utc`。

**§1 结论：r1 硬挡 #3「实现错误」— CLEARED。** 范围上 r1 §5.1 要求的「三所小时线」只交了 Bitstamp（OKX 仅 lag0 日线；Coinbase `skipped, n=0`）、「N 20–45 全表」未上传，归入 §7 的 #3-scope STILL_OPEN（低成本，且与 §4.2 的 OKX 复检是同一次拉取）。

---

## 2. Donchian shadow 基线：窗口是否排除确认 bar

| 实现 | 一致率 | 混淆（oracle→don） | above / below 召回 | 宽度中位 |
|---|---|---|---|---|
| 申请包本轮（自称 `closes[j-n:j], j=index(D−1)`） | 43.81%（177/404） | above→above 59、above→inside 152、below→below 35、below→inside 71、inside→below 4、inside→inside 83 | 27.96% / 33.02% | 12.1065% |
| **本文 · 窗口 = D−1 之前 20 根，判 close(D−1)** | **43.81%（177/404）** | **59 / 152 / 35 / 71 / 4 / 83（逐格相同）** | 27.96% / 33.02% | 12.1065% |
| 本文 · 窗口含 D−1（r1 判定的错误变体） | 21.53%（87/404） | above→inside 211、below→inside 106、inside→inside 87；**above→above 0、below→below 0** | 0 / 0 | — |
| GATE §2.2 预览（409 行） | 43.8% | 59 / 153 / 35 / 73 / 4 / 85 | 27.8% / 32.4% | 12.24% |

- 混淆非全 `inside`：above→above 59 > 0 且 below→below 35 > 0，断言 PASS（申请包 `assertion_pass: true` 属实）。
- 含确认 bar 的变体逐格复现 r1 作废的 21.53% → 旧数之因确认；本轮数字与 A4 正确语义逐格一致 → **窗口已排除确认 bar**。
- 对照 B：H1(halfbar N=33) vs oracle 400/404 = **99.01%**（本文混淆 above→above 211、below→below 106、inside→inside 83、inside→below 3、inside→above 1）；H1 above/below 召回 100/100 ✓。
- 宽度中位：Don 12.1065 逐位相同；oracle 申请包 3.6400 vs 本文 404 行 3.6339（410 行 3.6407）、H1 3.5773 vs 本文 3.5772（以 oracle mid 为分母）→ 申请包 oracle 宽度中位的样本不是 404 行，软项，请声明。

**§2 结论：r1 硬挡 #6 — CLEARED。** shadow-L1 对照 A 的作废撤销；43.81% / 12.11% vs 3.63% / 召回 28% & 33% 作为 §6.6 Layer 1 对照 A 的成立数字进入证据链。这**不影响** IMPL-GATE r2 的 proxy 契约（GATE §0：proxy 不声称相似）。

---

## 3. §6.9 源切换边界跳变（半根 N=33，单位 % of oracle mid）

| 缺口 | 端 | 计分 oracle 日 | 申请包 U / L | **本文 U / L** | ≤0.30%？ |
|---|---|---|---|---|---|
| 2023-07-07→08-22（46d） | 左 | 07-07 | −0.0137 / +0.0494 | −0.014 / +0.049 | ✓ |
| | 右 | 08-22 | −0.0710 / **+0.1409** | −0.071 / **+0.141** | ✓（全表最大） |
| 2023-09-28→10-16（18d） | 左 | 09-28 | −0.0374 / +0.0317 | −0.037 / +0.032 | ✓ |
| | 右 | 10-16 | −0.0221 / +0.0329 | −0.022 / +0.033 | ✓ |
| 2024-02-08→02-19（11d） | 左 | 02-08 | −0.0292 / −0.0004 | −0.029 / −0.000 | ✓ |
| | 右 | 02-19 | +0.0042 / +0.0354 | +0.004 / +0.035 | ✓ |
| 2024-07-22→12-17（148d） | 左 | 07-22 | −0.0291 / +0.0109 | −0.029 / +0.011 | ✓ |
| | 右 | 12-17 | +0.0371 / +0.1011 | +0.037 / +0.101 | ✓ |
| 2025-01-27→02-05（9d） | 左 | 01-27 | −0.0464 / −0.0314 | −0.046 / −0.031 | ✓ |
| | 右 | **02-06（替代 02-05 异常行）** | +0.0219 / −0.0094 | +0.022 / −0.009 | ✓ |
| **判定** | | | 10/10，max 0.141 | **10/10，max 0.141** | **PASS** |

lag0 9/10（2023-10-16 U +0.396 不达）、lag1 5/10（max 0.805）与 r1 §3.5 相同，申请包如实列出。`substituted: true` 字段显式标了替代——好。替代规则本身仍是 GATE r4 定义项（r1 §7），本文不裁。

**§3 结论：r1 硬挡 #5 — CLEARED（模型层）。** §6.9 的其余项（源隔离 / 冲突处理 / 自评守卫 / fail-closed 三注入 / 一日一源 / 禁止事项）中，源隔离与冲突处理由 L0 结构核验覆盖（§5.4）；三注入属实现层，进 IMPL-GATE r3，本文不评。

---

## 4. §6.3 / §6.5 现状（数字接受，门槛不动）

### 4.1 §6.3 逐行（半根 N=33，Bitstamp，n=404；申请包 = 本文）

| 指标 | 最低 | 目标 | 实测 | 最低 | 目标 |
|---|---|---|---|---|---|
| pooled RMSE% | ≤0.20 | ≤0.10 | **0.0725** | ✓ | ✓ |
| \|bias_U\| | ≤0.05 | ≤0.03 | 0.0084 | ✓ | ✓ |
| \|bias_L\| | ≤0.05 | ≤0.03 | **0.0402** | ✓ | **✗** |
| 逐年 RMSE% | 每年 ≤0.30 | ≤0.15 | 0.0987 / 0.0536 / 0.0412 | ✓ | ✓ |
| max\|res\| | ≤1.0（逐日解释） | ≤0.6 | 0.3510（2023-03-27 U） | ✓ | ✓ |
| 参数稀疏 | 单一 (N, α) | 同 | N=33，α=2/34，全期 | ✓ | ✓ |
| N±1 增幅 ≥30% | — | — | +197.4% / +98.3% | ✓ | ✓ |
| **留出 ≤1.5×** | **同** | **同** | **2023: 2.038 ✗** · 2024: 0.665 · 2025: 0.508 | **✗** | **✗** |

留出行在 GATE §6.3 里最低与目标同为「≤1.5×」，是**最低门槛**。一行不过 → §6.3 不过 → `formula_status` 不得离开 `hypothesis`。这是本轮票面 REWORK 的第一根据。

### 4.2 2023 留出：方法学核对 + 诊断（诊断不是放行依据）

- **方法学**：申请包的留出是固定 N=33 后比较年 RMSE，未在训练两年上重选 N。本文补做「训练两年重选 N」：三折 N* 均为 33 → 比值与固定 N 版逐位相同（2.038 / 0.665 / 0.508）。**2.038 对方法学稳健，没有「未重拟」的退路。**
- **残差分布**：|res| 最大的 8 日里 7 日落在 2023-03-23..03-31（序列起始两周），bias +0.2%~+0.35%。2023-03（14 帖）RMSE 0.226%、biasU/L +0.213 / +0.223；**剔除 2023-03 后 2023 年 RMSE 0.0759%，对 2024+2025 的比值仍为 1.568 > 1.5**。按半年：2023-H1 0.1311（bias +0.092 / +0.116）、2023-H2 0.0587、2024-H1 0.0540、2024-H2 0.0514、2025-H1 0.0412。
- **读法**：2023 年的超额不只是起始两周，而是整个 2023-H1 双轨同向正偏（Bitstamp 模型高于作者轨位 ≈0.1%），2023-H2 起消失。符号与「2023 上半年美元现货所对 USDT 所存在正基差」一致，但**这是可证伪假设，不是解释**。r1 §5.2 要求的 OKX-USDT 半根小时线复检就是判定实验：若 OKX 半根下 2023 折 ≤1.5 → 假设成立，§6.3 **全表**以该所为主口径重报（GATE §5.3 本就规定「取残差最小者」；但全部行须出自同一所，**不得跨所拼表**——RMSE 取 Bitstamp、留出取 OKX 之类不算过）并据此定 `venue_set`；若任一交易所都 >1.5 → 留出行不过，**不得放宽**。申请包交的 `okx_2023_diagnostic`（lag0 日线，ratio 1.216）方向上支持假设，但 lag0 按申请方与 r1 一致的口径**不可作过关依据**（半根才是主口径）。

### 4.3 §6.5（GATE 定义 = Bitstamp close(D−1) 对 oracle 轨位）

- 复现：`stated_position ∈ {above, inside, below}` 剔异常行 202 帖（含异常 204），一致 **169/202 = 83.66%**；对 H1 半根轨位同为 169/202。33 个不一致日的 `message_id` 集合与申请包逐条相同。**FAIL 属实，本轮已如实申报**（r1 #7「未申报」这一层清掉）。
- 转移日 100%：申请方「not claimed — labels unaudited」。当前标签下 `stated_holding` 变化点共 89 处（如 #10934 full→holding、#10938 full→reduced、#10942 reduced→cash、#10961 holding→cash…），`stated_action` 72 个 `clear` 中 58 个紧接上一个非空动作也是 `clear`（状态而非动作，r1 §2.3 判断成立）。集合须在标签审计后按「变化」重算再跑，**仍未跑 → STILL_OPEN**。
- **一处新的口径错误（诊断项，非闸门）**：申请包 `sec65_stated_position.json.diagnostic_post_hour_oracle` 标注 `price_mode: post_hour_open`，但 agree 169 / mismatches 33 与 `close_dm1` 完全相同。本文用 Bitstamp 发帖小时开盘价复算得 **184/202 = 91.09%**（发帖小时收盘价 179/202 = 88.61%），与 r1 §3.4 的 91.09% 一致。即诊断分支**没有真正切换价格序列**，字段标签与数字不符。这与 r1 抓到的两处实现错误同型（声明的语义 ≠ 实际算的东西）。因为它只是诊断，不改判定；但下次交付须修正，并在脚本里加断言「诊断价格向量 ≠ 闸门价格向量」。GATE 定义仍是 `close(D−1)`；改定义属 GATE r4。

---

## 5. L0：三项文书 + 结构复核 + 标签

### 5.1 §6.1 精度抽检记录（r1 解除条件 i）

`l0_spot_check.json`：n_checked 46 = 随机 40 + 异常 6；`numeric_match` 46/46；`sha_match` 46/46。本文核验：46 条记录的 `rails_upper/lower` 与 `raw_upper/lower` 与 `rails.jsonl` 对应行的 `upper/lower` 三方相等 46/46；`source_text_sha256` 与 `corpus_sha256` 与 `rails.jsonl` 三方相等 46/46；异常队列 {11029, 11136, 11407, 12126, 13503, 13752} = `rails.jsonl` 全部异常行；随机 40 条 `message_id` 唯一、与异常队列无交集；13752 的 U 96844 / L 95952 原样未改。**接受。** 软项：记录未声明比对方式（人工逐字 vs 程序重解析）；GATE §6.1 写的是「人工核对」。请补一行方法声明；若为程序重解析且与抽取器同一正则，须换独立方式（如另一正则或人工）复核至少异常 6 条。不阻塞冻结。

### 5.2 `edited` 声明（解除条件 ii）

`CORPUS_FINAL_ONLY`：410/410 有 `edit_date` 且 > `date`；首版数值不可得；`edited=true` 退化为常量「终版文本在场」；不编造首版数。这正是 r1 §2.2 给出的第二种处理（语料只有终版 → 明示）。**接受。** 软项：请附 `edit_date − date` 分布（6 条无轨帖的编辑延迟均为数秒至一分钟；若 410 条轨帖亦如此，则「终版≠首版」的风险可量化为可忽略）。

### 5.3 6 条无轨位帖（解除条件 iii）

#1303（2022-03-09 群规）、#9134 / #9583 / #10037 / #10650（2022 年单词 ticker）、#11011（2023-08-21 旅行返回）。5 条在序列起点 2023-03-14 之前，故不出现在 `coverage.jsonl`；#11011 对应 coverage 唯一一行 `post_without_rails` ✓；416 − 410 = 6 ✓。**接受。**

### 5.4 结构复核（与 r1 §2.1 同表，全部再过）

410 行 / 410 唯一 `bar_date_utc` / `message_id` 单调；`sender_id` 5129397609 × 410；`rail_source` oracle × 410、`rail_confidence` explicit × 410、`formula_status` null × 410；`upper ≤ lower` 0 行；`width_pct` 分母 (U+L)/2 逐行相符；410 个 `source_text_sha256` 两两不同；异常 6 行与 flag 相同；覆盖表 834 行连续 2023-03-14..2025-06-24，observed 404 + anomaly_excluded 6 = 410，`no_post_weekend` 238、`no_post_gap` 185、`post_without_rails` 1。**§6.9 源隔离与冲突处理（L0 侧）PASS。**

### 5.5 标签列

`stated_position` 非空 228/410 = **55.6%**（above 94 / below 63 / inside 47 / touching 24）< 70% FAIL；`stated_holding` 276/410 = 67.3% ≥50% ✓；宽正则诊断 271/410 = 66.1%（申请包自报，未写入冻结文件——**正确**做法）仍 <70%。CARD 锚点：#10962 `stated_position` null、#10968 `stated_holding` null 仍未补。**REWORK 维持。**

### 5.6 裁决

- **数值轨位列：PASS。** `rails.jsonl` sha `4740a4a6…` = r1 冻结值，三项解除条件履行 → **L0 v1 冻结确认**，作为 §6.3 / §6.5 / §6.6 评分靶的效力由 Conditional 转为无条件。撤回条件不变（GATE §9：任一抽检出现数值改写或 `sender_id` 混入）。
- **标签列：REWORK。** 解除条件与 r1 §2.3 完全相同，一条不减。

---

## 6. 合规（§0C / §8 / §9 ↔ A1–A12）快速再核

`COMPLIANCE-CHECKLIST.md` 与 r1 同一份（sha 8fc93b18…），未随本轮更新——软项。逐条：A1 两层 ✓（包内无 L1 轨位产物）；A2 H0 只报表 ✓（本轮未动）；A3 无 k 绑定 ✓；A4 hypothesis 只在 `research/` ✓（所有上传件路径与内容无 brief / JSON / history 痕迹，`h1_full_metrics.formula_status = "hypothesis"` 且 note 明示不进 brief）；A5 Donchian brief / IMPL-GATE r2 未动 ✓；A6 ✓（§5.4）；A7 148d ✓（§3 缺口表）；A8 H1 必测 ✓；A9 H0-TV ✓（本轮未动）；A10 Pine 未变 / TV live 后置；A11 L1 本轮对照 A 修正 ✓、L2 后置；A12 生产 sha 前后 `594a20a7…` 相等、`unchanged: true`、文件 mtime 2026-09-21T04:44:50Z 早于 `rework_run` 2026-09-21T06:00Z ✓。**PASS 维持。** 注同 r1：点时快照，非持续守卫；进 IMPL-GATE r3 须换成 fail-closed 三注入的自动断言。

---

## 7. prior 硬挡逐条勾（r1 §4 编号；状态 = CLEARED | STILL_OPEN | DEFERRED）

| r1 # | 项 | r1 分类 | **r2 状态** | 依据 |
|---|---|---|---|---|
| 1 | TV live §6.8 导出 | Conditional / 进 `replica_shadow` 前硬 | **DEFERRED**（本地表 ≥300 预热重生成：申请方称已做，文件未上传 → 未核） | §8 软项 |
| 2 | Layer 2 ≥14d | Conditional（顺序在 `replica_shadow` 之后） | **DEFERRED（顺序正确）** | 未提前写 history ✓ |
| 3 | 半根 bar 实现错误 | **硬挡** | **CLEARED（构造）** · **STILL_OPEN（scope：三所小时线只交 Bitstamp；N 20–45 全表未上传）** | §1 |
| 4 | 作者平台收盘不可用 | Conditional（阈值不放宽） | **STILL_OPEN**（33 不一致日 ≥3 所收盘差表未交；依赖 #9 标签审计） | §4.3 |
| 5 | §6.9 边界跳变未测 | **硬挡** | **CLEARED** | §3 |
| 6 | Donchian 对照 A 实现错误 | **硬挡** | **CLEARED** | §2 |
| 7 | §6.5 83.66% 未申报 + 转移日未跑 | **硬挡** | **CLEARED（申报）· STILL_OPEN（闸门 FAIL；转移日未跑；诊断分支口径错）** | §4.3 |
| 8 | §6.3 bias_U / 双 RMSE / N±1 / 2023 留出 | **硬挡** | **CLEARED（半根 bias 最低达标、N±1 已报、核心 JSON 单一管线 0.1221、OHLC sha）· STILL_OPEN（2023 留出 2.038 FAIL，OKX-USDT 半根复检与解释未交；`venue_selection.md` 仍载 0.156 / 0.155 / 0.167、n=916 起 2022-12-24 的伪影值，违反 §5.8「全包数字唯一」）** | §4.1–4.2、§8 |
| 9 | L0 三项文书 + 标签列 | 数值列 Conditional / 标签列硬 | **CLEARED（文书三项 → 数值列 PASS）· STILL_OPEN（标签列）** | §5 |
| 软 | §6.2 H0 缺项；H0-TV 每段轨距；四份 JSON 不在 SHA 清单；第 4 所 | 软 | **STILL_OPEN（本轮未动）** | — |

r1 §5「下次申请门槛」1–10 对表：1 半根报告 **部分**（构造 ✓ 断言 ✓ 预热 ✓ sha ✓；三所 ✗ 全表 ✗）；2 §6.3 半根全表 **✓ 已报 / 留出行 ✗**；3 §6.9 **✓**；4 shadow L1 **✓**；5 L0 文书 **✓**；6 标签 **✗**；7 §6.5 按 GATE 定义 **✓ 已报（FAIL）/ 逐日多所解释 ✗ / 转移日 ✗**；8 全包数字唯一 **核心 ✓ / `venue_selection.md` ✗**；9 §6.8 本地表 **称已做，未上传**；10 SHA 清单 **未上传**。

---

## 8. residual 分类：哪些仍硬挡，哪些可债，哪些软

「硬挡」= 下次 RECHECK 前必须交齐，否则票面仍 REWORK；「可债」= 研究包证据 PASS 可不含，但写入 `replica_shadow` / IMPL-GATE r3 入场硬条件；「软」= 补齐即可，不阻塞。**阈值一条不动。**

| # | residual | 分类 | 下次要交什么 |
|---|---|---|---|
| R1 | §6.3 留出 2023 折 2.038 > 1.5 | **硬挡** | OKX BTC-USDT（及 Coinbase）**小时线半根**复检，同管线同预热，报三折比值；附可证伪解释（§4.2 给出候选：2023-H1 USD/USDT 基差）。任一所 ≤1.5 → 以该所为主口径重报 §6.3 全表（同一所出全部行，不得跨所拼表）并定 `venue_set`；全部 >1.5 → 留出行不过，不得放宽。lag0 日线 proxy 不可作依据 |
| R2 | L0 标签列 55.6% < 70%；33 不一致日未审计；`stated_action` 状态语义；CARD 锚点空值 | **硬挡** | 同 r1 §2.3 六条：≥70%；审计 33 日 + 全部 `stated_action` 帖；`clear` 改为动作语义（当前 58/72 为连续重复）；#10962 / #10968 补齐；产物按 §9.1 出 v1.1 且数值列 diff 为空 |
| R3 | §6.5 83.66% < 97%；转移日 100% 未跑 | **硬挡**（依赖 R2） | 标签审计后按 GATE 定义 `close(D−1)` 重报；转移集合按「变化」重算（当前 89 处 holding 变化为起点）；每个不一致日附 ≥3 所收盘差 / 半根解释（GATE §6.5 允许「可证伪的解释」）；发帖时刻价只作附表 |
| R4 | 半根三所小时线 + N 20–45 全表 | **硬挡（低成本，与 R1 同一次拉取）** | Bitstamp / OKX / Coinbase 三所半根全表，V 形须在三所同现 N=33±0（GATE §5.3 `venue_set` 需要它） |
| R5 | `venue_selection.md` 伪影值未更新（0.156 / 0.155 / 0.167，n=916） | **硬挡（文书级，r1 §5.8）** | 重生成或删除；全包同 (venue, N, alignment) 只允许一个值；`compare_summary.json` 同步 |
| D1 | §6.8 TV live 导出 | **可债**（`replica_shadow` 入场硬条件） | `research/replica-tv-repro-<date>.md`：时区截图、逐日表、\|TV−local\| ≤0.02%；本地表 ≥300 预热版先上传 |
| D2 | Layer 2 ≥14d | **可债**（顺序：IMPL-GATE r3 → replica_shadow → L2） | 无需在研究包内交 |
| D3 | §6.9 实现层三注入、自评守卫脚本断言 | **可债**（IMPL-GATE r3） | 进实现闸 |
| D4 | 33 不一致日 ≥3 所收盘差表 | **可债 → 随 R3 交** | 见 R3 |
| S1 | §6.5 诊断分支 `post_hour_open` 实为 `close_dm1`（应为 91.09%） | 软（诊断非闸门） | 修正 + 断言「诊断价格向量 ≠ 闸门价格向量」 |
| S2 | 断言块 / 宽度中位样本未声明（0.1030 / 1.7514；3.6400） | 软 | 声明样本或改为 404 帖日 |
| S3 | 抽检方法未声明（人工 vs 程序） | 软 | 一行声明；同正则重解析不算独立复核 |
| S4 | `edit_date − date` 分布未报 | 软 | 一张直方图或分位表 |
| S5 | SHA 清单未上传；`COMPLIANCE-CHECKLIST.md` 未随轮更新；`tv_local_replica_table.jsonl` 未上传 | 软 | 清单覆盖全部 out/ + 脚本 + 表 |
| S6 | §6.2 H0 缺项；H0-TV 每段轨距；第 4 所 | 软（r1 遗留） | 同 r1 |

**关于「模型半部 Conditional PASS」的请求：不授予。** 理由只有一条：§6.3 留出行是最低门槛，FAIL 就是 FAIL；给 Conditional 等于把「≤1.5×」改成「≤2.04× 待解释」，即改宽。可以明说的是：模型半部**剩下的**只有 R1（+R4 同源）、R3（依赖 R2）、D1 三件；构造、对齐、N、边界跳变、shadow 对照都已成立。

---

## 9. 本文效力（仅此三项）

### 9.1 L0 v1 冻结确认与版本规则

- `truth_series/rails.jsonl` sha `4740a4a68ca6c69c60e149a68a61a3f63057d4d019c43f194fea1c21caf449a9` = **L0 v1**，数值轨位列 PASS，作为 §6.3 / §6.5 / §6.6 评分靶无条件生效。
- 标签 REWORK（R2）**不得在 v1 文件上原地改写**。产物为新版本文件（建议 `rails-v1.1.jsonl` + 新 sha），验收断言：数值列（`message_id / sent_at_utc / bar_date_utc / upper / lower / width / width_pct / anomaly_flags / rail_source / rail_confidence / source_text_sha256`）与 v1 逐行 diff 为空；只允许 `stated_*` 列变化。v1.1 通过 §6.1 标签项前，v1 仍是唯一评分靶。
- 撤回条件不变：任一抽检发现数值改写或 `sender_id` 混入 → 按 GATE §9 撤回 PASS。

### 9.2 H1 状态

`formula_status = hypothesis` 不变。**H1 仍不得进 brief、不得进 JSON、不得进 history**；不授权 `replica_shadow`。理由：§6.3 留出行 FAIL、§6.5 FAIL、§6.8 TV live 未做——三者任一即足。本文对 H1 的**正面**效力仅限于证据链记录：正确半根构造下 N=33（Bitstamp）0.0725% / 边界跳变 10/10 / 位置一致 99.01% 成立且经独立复现。

### 9.3 shadow Layer 1

对照 A（Donchian A4）43.81% 与对照 B（H1）99.01% 均接受为 §6.6 Layer 1 数字。Layer 1 **未**因此「通过」——GATE §6.6 对照 B 要求「§6.3 + §6.5 全部」，而两者未过。

---

## 10. 下次申请门槛（RECHECK r3；只列未齐硬项；阈值一条不减）

1. **R1 + R4**：OKX / Coinbase 小时线半根三所全表（N 20–45），三折留出，2023 折解释。
2. **R2**：标签列 ≥70% + 审计 + 动作语义 + 锚点补齐，按 §9.1 出 v1.1。
3. **R3**：§6.5 按 GATE 定义重报 ≥97%；转移日 100%（集合按变化重算）；不一致日多所解释表。
4. **R5**：`venue_selection.md` / `compare_summary.json` 重生成，全包数字唯一。
5. S1–S5 一并补齐；SHA 清单覆盖全部交付件。

满足 1–4 且数字落在 §6.3 / §6.5 门槛内 → RECHECK r3 可裁「研究包证据 PASS（票面仍 REWORK 直到 D1 TV live 与 D3 三注入齐）」。**任何一条以「数据源不同」「零模型」「时间不够」「已解释」为由放宽 → 直接 REWORK。**

---

## 11. 明确不变项

| 对象 | 状态 | 依据 |
|---|---|---|
| Donchian proxy brief 固定行 / IMPL-GATE r2 PASS 面 | **仍禁止动** | GATE §0「proxy 契约不变」；对照 A 43.81% 是观测靶，不是替换依据 |
| `data/last_btc_consensus.json` | **仍禁止写** | A12 通过（sha 594a20a7… 前后相等）；研究脚本继续不得触碰 |
| brief 通道行 | **仍禁止换行**；不得并列两条 | GATE §7.3 第一阶段；§7.4 不授权 |
| `schema_version: 3` / `trend_channel_replica` 块 / replica 进 history | **不授权** | 需 IMPL-GATE r3 |
| `formula_status` | **`hypothesis`**；只存在于 `research/` | §0B.3 B4；§6.3 留出 / §6.5 / §6.8 未过 |
| `system_signal_eligible` | 常量 `false` | §0B.4；全部模型级别恒禁 |
| L1 分段平行拟合 | 不作源、不进 brief、不进 shadow、不作标签 | §0C.2 |
| k = 0.018958 | 禁绑；H6 只作对照 | §0C.2 问 2 |
| `missing_inputs` 字面 `"trend_channel (LaoMao 2.0 original)"` | 必含 | §0B.4 |
| L0 `rails.jsonl` sha 4740a4a6… | **L0 v1（本文确认无条件冻结）** | §9.1 |
| GATE r3 全部阈值与定义 | **一字不改** | 本文前提 |

---

## 12. 对 GATE §9 置信表的影响（记录，不改 GATE 正文）

| GATE §9 结论 | r1 后置信 | 本次证据 | 走向 |
|---|---|---|---|
| H1 = EMA(H/L) 族正确 | 上调（单所） | 申请方以正确构造复现 0.0725%，本文再复现至 1e-15；N±1 V 形 +197% / +98%；边界 10/10；位置一致 99.01% | **再上调**；仍缺 OKX / Coinbase 半根三所同现（R4） |
| N≈30 → N=33 | 推翻 → 33 | 26 个 N 全扫单谷 N=33 | 再确认（Bitstamp） |
| proxy 位置一致率 43.8% | 再确认 | A4 正确实现 43.81%，申请方与本文逐格相同 | 再确认 |
| 抽取半部 PASS | 数值列 Conditional | 三项文书自洽，结构全过 | **数值列 PASS（v1 冻结确认）**；标签列 REWORK |
| §6.3 留出 ≤1.5× 可达 | — | 2023 折 2.038；剔起始两周仍 1.57；2023-H1 双轨正偏 | **新增待证伪项**：单一美元现货所可能过不了留出行；判定实验 = OKX-USDT 半根 |
| 总判 REWORK | 0.95 | 三项最低门槛 FAIL（留出 / §6.5 / 标签） | 维持 0.96 |

---

## 13. 本文数字的复现协议

- 数据：Bitstamp 公开 API `ohlc/btcusd` step=86400 自 2022-01-01 至 2025-07-05（1282 根，无缺日）；step=3600 自 2023-01-01 至 2025-07-05（22008 根，917 日 × 24，无缺小时）。日线 H/L 与小时聚合 H/L 在 404 帖日逐日相等。
- 靶：`rails.jsonl`（sha 4740a4a6…）剔 `anomaly_flags` 非空 6 行 → 404 行；残差以 oracle `(U+L)/2` 为分母，单位 %。
- EMA：SMA(N) 种子 + α=2/(N+1) 递推，自 2022-01-01 起（预热 437 根到 2023-03-13）。
- lag1 = EMA 至 D−1；lag0 = EMA 至 D 整根；半根 = `α·H/L_partial(D, 00:00–11:59Z) + (1−α)·EMA_{D−1}`；错误变体 = 每日 H/L 换成 partial 后端到端递推。
- Donchian A4：j = index(D−1)，窗口 = `close[j−20 : j]`（不含 j），判 `close[j]`；错误变体 = `close[j−19 : j+1]`。
- §6.9：>7d 缺口两端 oracle 日；端为异常行 → 取缺口外侧首个干净 oracle 日。
- §6.5：`stated_position ∈ {above, inside, below}`，价 = `close(D−1)`（GATE）/ 发帖小时开盘或收盘（诊断）。
- 留出：固定 N=33 与「训练两年重选 N」两版。
- 脚本在 `/tmp/recheck_r2/`（不入库）；按上述八条可在数分钟内复现全部表格。

---

## 14. 非目标

- 不代申请方拉 OKX / Coinbase 小时线、不代做标签审计、不代生成任何 `research/` 交付物。
- 不裁 N 的最终值（33 为 Bitstamp 单所结果）、不裁 `venue_set`、不确认作者公式。
- 不改 GATE r3 任何阈值与定义；§6.5 价格参照、§6.9 替代规则留 GATE r4。
- 不评估 IMPL-GATE r3 的实现层三注入。
- 不涉及下单、仓位、`system_signal`。

---

## ACK

```text
HANDOFF
from: architect
to: research-executor
intent: ACK
thread_ref: GATE-laomao-truth-channel-fit-2026-09-21-r3
verdict: REWORK (residual; hard implementation blockers CLEARED and independently reproduced)
cleared:
  - r1 #3 halfbar construction: CLEARED (full-bar EMA through D-1 + one 00-11Z step; top5 N x 8 fields reproduced to >=4 dp, N 20-45 scan single valley at 33; bug variant reproduces 0.83 not 0.0725; identity RMS(hb-lag0)=alpha*RMS(Hfull-Hpartial) holds; lag0 0.1221 = converged canonical => single pipeline, warmup 437)
  - r1 #6 Donchian A4: CLEARED (window excludes confirm bar; 43.81%, confusion 59/152/35/71/4/83 exact; include-variant reproduces void 21.53%)
  - r1 #5 sec 6.9: CLEARED (10/10, max 0.141%, substitution 2025-02-06 declared)
  - r1 #9 L0 paperwork: CLEARED (spot 46/46 consistent with rails.jsonl; edited=CORPUS_FINAL_ONLY accepted; 6 posts dispositioned)
  - r1 #7 reporting: CLEARED (83.66% now declared as FAIL)
  - r1 #8 core: CLEARED (halfbar bias/N+-1/holdout reported; OHLC sha; single canonical pipeline in out/*.json)
still_open_hard:
  - R1 sec 6.3 holdout 2023 = 2.038 > 1.5 (robust to refit-N; ex-March still 1.57); OKX-USDT halfbar hourly recheck + falsifiable explanation owed; lag0 proxy inadmissible
  - R2 label column 55.6% < 70%; 33-day audit; stated_action semantics (58/72 clear are repeats); #10962/#10968
  - R3 sec 6.5 83.66% < 97%; transition-day 100% not run (depends on R2)
  - R4 three-venue halfbar + N 20-45 full table (same pull as R1)
  - R5 venue_selection.md stale artifact numbers (0.156/0.155/0.167) violate "one number per (venue,N,alignment)"
deferred_debt: D1 TV live sec 6.8 (hard before replica_shadow); D2 Layer 2 (after replica_shadow); D3 sec 6.9 fail-closed injections (IMPL-GATE r3); D4 multi-venue close table for mismatch days (with R3)
soft: S1 sec 6.5 post_hour diagnostic mislabeled (actual 91.09%); S2 invariants/width-median sample undeclared; S3 spot-check method; S4 edit-delay distribution; S5 SHA list / checklist / local TV table not uploaded; S6 r1 soft items unchanged
effects:
  - L0 numeric columns: PASS; rails.jsonl sha 4740a4a6... = L0 v1 frozen unconditionally; label rework must ship as v1.1 with numeric-column diff empty
  - H1: formula_status=hypothesis unchanged; NOT in brief/JSON/history; no replica_shadow
  - shadow L1 contrast A void lifted (43.81% accepted); Layer 1 not "passed" (sec 6.3/6.5 unmet)
not_granted: model-half Conditional PASS (holdout is a minimum gate; granting it = widening)
unchanged: Donchian proxy brief; last_btc_consensus.json (sha 594a20a7... before==after); brief channel line; schema_version 3; system_signal_eligible=false; all GATE r3 thresholds/definitions
next_gate: sec 10 items 1-4 complete and within sec 6.3 / 6.5 thresholds -> RECHECK r3
```

Conditional PASS

# RECHECK：老猫 BTC「多源现价 + 通道代理」数据方案（对照 GATE §5 A1–A10 的复审）

> 裁决：**Conditional PASS**。硬项 A1–A7 全部齐；条件项 A8 已齐、A9 未齐 → A9 记债，**必须在实现 PR 内一并完成**（GATE §5 原文 `:281`，本文不改宽、不改窄）。
> 对照物：`architecture/GATE-laomao-btc-channel-data-2026-09-21.md`（PR [#4](https://github.com/licett/ai-workflow-kit/pull/4)，复审时仍 OPEN 未合，分支 `cursor/gate-laomao-btc-channel-data-b074`，commit `3679f49`）。下文 "GATE `:N`" 指该 commit 内行号。
> 范围：只审 `uploads/` 四份材料——`DESIGN-channel-proxy-v0.md`（下称 DESIGN）、`README.md`、`btc_multisource.py`（下称 py）、`last_btc_consensus.json`（下称 JSON，`as_of 2026-09-21T02:07:12Z`）。不改代码、不写代码、不改 uploads；本文是本次唯一新增文件。
> 方法：纯文档 / 数据对读，**本次未做外部探针**——JSON 是重跑产物，其 OKX `1Dutc` 与 Bitstamp 日收与 GATE §1.2 独立探针值逐分对上（见 A2），足以替代。凡材料未证实的，标"待确认"。
> 日期：2026-09-21。

---

## 0. 总判

| 项 | GATE 闸门 | 本次 | 一句话 |
|---|---|---|---|
| A1 收盘锚点 | 硬 | **齐** | `close_anchor: 08:00 Asia/Shanghai (= 00:00 UTC)` 已落字、署名、日期；两种读法不并存 |
| A2 OKX 对齐 | 硬 | **齐** | `bar=1Dutc`、无 `tz_offset`；重跑 5 日 cross-check 全 `ok`，与 GATE 探针值逐分一致 |
| A3 candle 时间戳 + 收盘标记 | 硬 | **齐** | 4 源每根 candle 均带 `ts_open_utc`、`closed`；活 bar 全部 `false`；设计写明活 bar 不进通道 |
| A4 公式定稿 | 硬 | **齐** | close-Donchian(N)、排除确认 bar、不重绘、回归只作 slope、`params.n=20` 均落字 |
| A5 字段契约 v2 | 硬 | **齐（契约层）** | §2.4 全部字段逐一在 DESIGN；无顶层 `trend_channel`；`schema_version` 现为 1 是**正确**的（见 §4-3） |
| A6 brief 三条规则 | 硬 | **齐（规则定稿）** | 三条规则以可引用原文锁定；prompt/模板落位未从材料证实 → 列为实现 PR 硬验收项（见 §1 A6 与 §6） |
| A7 venue 法定人数 | 硬 | **齐** | `sources[].kind`、`n_agree_venues>=3 → ok`、README 同步 |
| A8 原子写 + last-good | 条件 | **齐** | tmp+`os.replace`+fsync；`fail` 只写 `last_run.json` |
| A9 历史 + 自校验 | 条件 | **未齐 → 债** | py / README / JSON 三处均无 `history`、`payload_sha256`、`producer` |
| A10 F7 F8 F10 F11 F12 | 债 | **全部已清** | 申请方自述已修，核验属实，见 §3 |

置信度：总判 0.85；A6 "规则定稿即齐" 这一读法 0.70（是本裁决的主要判断风险，§6 给出推翻条件）；A5 契约层读法 0.90（逻辑上别无他选）；A1 沿用 GATE §6 的 0.80（锚点是默认值，非人工从原始消息确认）。

---

## 1. 硬项逐勾 A1–A7

格式：验收原文（GATE §5）→ 证据（文件:行）→ 判定。

### A1 收盘锚点落字 — F2 — **齐**

验收（GATE `:269`）：本文或 README 出现一行 `close_anchor: 08:00 Asia/Shanghai (= 00:00 UTC)`（或明确改为 `00:00 Asia/Shanghai`），署名 + 日期。

| 证据 | 位置 | 内容 |
|---|---|---|
| 落字行 | DESIGN `:11` | `close_anchor: 08:00 Asia/Shanghai (= 00:00 UTC)` |
| 落字行（副本） | README `:29` | 同一行，前缀 "`close_anchor` adopted 2026-09-21 (GATE default; Jimmy deferred widget)" |
| 署名 | DESIGN `:14` | `Signed by: 老猫` |
| 日期 | DESIGN `:15-16` | `Signed date: 2026-09-21`；`Decision: adopted 2026-09-21` |
| 决策路径 | DESIGN `:16-17` | Jimmy 跳过 widget → 采 GATE 默认读法 (i) |
| 读法唯一 | DESIGN `:18` | "This is **not** the UTC+8-midnight / 16:00 UTC boundary"——满足 GATE `:130` "两种读法不能并存" |

判定：齐。两点说明，不影响判定：
- 署名人是 `老猫`（本盒上的数据模块维护方 / agent 名），不是持有原始消息的 Jimmy。GATE `:224` 已预设 "裁决默认 (i)"，A1 只要求落字 + 署名 + 日期，未指定署名人；Jimmy 的 "deferred" 本身作为决策记录在 `:16-17`。可接受。
- 因此 GATE §6 `:295` 的推翻条件（Jimmy 从原始消息确认北京时间零点）**仍然活着**，置信度不变 0.80。实现 PR 须把锚点作为参数（`bar.boundary_tz` / `bar.close_local`，DESIGN `:61-64`）而非常量硬编码，保住 GATE `:130` 描述的 (ii) 回退路径。

### A2 OKX 对齐 — F1 — **齐**

验收（GATE `:270`）：设计 / 代码用 `bar=1Dutc`，无 `tz_offset_hours=8`；重跑后正常日 `daily_cross_check[*].ok` 全 `true`；README `:46` 改写。

| 证据 | 位置 | 内容 |
|---|---|---|
| 代码 | py `:287-289` | `bar=1Dutc`，注释 "F1: bar=1Dutc — UTC day boundaries (00:00 UTC); no tz_offset shifting" |
| 无平移 | py `:245-251` | `_ts_to_date_utc`："No TZ shifting"；全文 `rg tz_offset` 仅命中 `:287` 注释 |
| 重跑结果 | JSON `:382-437` | 5 日 `daily_cross_check` 全 `ok: true`（`:392` `:403` `:414` `:425` `:436`）；spread 0.0163% / 0.0344% / 0.0484% / 0.0346% / 0.0924% |
| 与 GATE 探针对账 | JSON `:341` `:350` `:182` `:191` vs GATE `:58` | OKX 09-20 close `81179.6`、09-19 `81265.8`；Bitstamp 09-20 `81151.65`、09-19 `81235.14`——四个数与 GATE 独立探针**逐分相同** |
| bar 起点 | JSON `:336` `:327` | OKX candle `ts_open_utc` = `2026-09-20T00:00:00Z` / `2026-09-21T00:00:00Z`，UTC 边界 |
| README 改写 | README `:28` | "OKX uses `bar=1Dutc` (not `1D` / UTC+8 exchange day)"；`:67` "OKX (`1Dutc`)… overlapping **UTC** calendar dates" |
| 设计 | DESIGN `:22-24` | 锁定 `1Dutc` |

判定：齐。GATE §1.3 指出的 09-19 / 09-17 两天 "OHLC divergence" 误报已消失（JSON `:413` 0.0484%、`:435` 0.0924%，均在 0.5% 内）。

### A3 candle 带时间戳与收盘标记 — F4 — **齐**

验收（GATE `:271`）：每根 candle 有 `ts_open_utc`、`closed`；设计写明"活 bar 不进通道输入"。

| 证据 | 位置 | 内容 |
|---|---|---|
| 构造 | py `:274-283` | `_mk_candle` 输出 `date` / `ts_open_utc`（`:277`）/ `closed`（`:278`）/ OHLC |
| 收盘判定 | py `:261-271` | `_candle_closed`：有 venue `confirm` 标志（OKX `row[8]`，`:298`）优先；否则 `ts_open + 86400 <= now` |
| 实际输出 | JSON `:166-173` `:219-226` `:272-279` `:325-332` | 4 源 09-21 活 bar 均 `closed: false`；09-17～09-20 均 `true`（脚本核对：bitstamp/coinbase/kraken/okx 各 `[F,T,T,T,T]`） |
| 设计 | DESIGN `:27-31` | "Live/incomplete bars have `closed=false` and never enter channel input"；确认 bar = 最新一根完全收盘的 UTC 日线 |
| README | README `:31` | "Each candle carries `ts_open_utc` (ISO-UTC) and `closed` (bool; live/incomplete bar → `closed=false`)" |

判定：齐。提醒（不影响判定）：`closed` 是**数据层**标志，`_candle_closed` 的时间回退分支（`:271`）不含 grace；GATE §2.2 `:101` 的确认 bar 定义是 `t_open + 86400 + grace <= now`。实现 PR 须在 `closed` 之上再套 `params.grace_min`（DESIGN `:58`）得出 `close_confirmed.confirmed`，**不得**把 `closed` 直接当 `confirmed` 用（§5 I5）。

### A4 公式定稿 — F3 — **齐**

验收（GATE `:272`）：设计写明 close-Donchian(N)、排除确认 bar、不重绘性质；`params.n` 出现在输出；回归只用于 `slope` 或不用。

| 证据 | 位置 | 内容 |
|---|---|---|
| 方法 | DESIGN `:35` | `method=donchian_close` |
| 排除确认 bar | DESIGN `:36` | "Use the prior completed close series only; exclude the confirmation bar from the lookback window" |
| N | DESIGN `:37` | `N=20` = GATE 首次 shadow 默认（GATE `:105`），Jimmy 未选；"must remain explicit and visible" |
| 回归 | DESIGN `:38` | 只允许作可选 `slope` 标签，"must not define channel levels" |
| 不重绘 | DESIGN `:39` | 确认 bar 一旦分类即固定，后续 bar 不得改写 |
| `params.n` | DESIGN `:55` `:102` | 契约 `params.n: 20`；规则 "`params.n` is 20 for the first shadow default" |
| 其余参数 | DESIGN `:56-59` | `outlier_pct 0.5` / `min_sources_per_day 2` / `grace_min 10` / `slope_deadzone_pct_per_day 0.1`——与 GATE `:100-104` 一致 |
| 未越线 | DESIGN `:6` `:40` `:132-134`；py 全文 | 无任何 `upper / lower / price_position / slope` 计算——符合 GATE `:285` 过审前禁令 |

判定：齐。"`params.n` 出现在输出" 在过审前只能在契约层核验（输出层出现 = 已实现通道 = GATE `:285` 禁止），实现 PR 时在实际 JSON 中复核（§5 I1）。N=20 属占位，Jimmy 后续从 {20,30,55} 改选时是输出可见事件（GATE `:105`），不是静默调参。

### A5 字段契约 v2 — GATE §2.4 — **齐（契约层）**

验收（GATE `:273`）：`schema_version: 2`；`trend_channel_proxy` 含 §2.4 全部字段；**不存在**顶层 `trend_channel`；README JSON shape 同步。

| 证据 | 位置 | 内容 |
|---|---|---|
| `schema_version: 2` | DESIGN `:48` | 契约顶层 |
| 顶层键名 | DESIGN `:44` `:49` | `trend_channel_proxy`；"must not occupy the real `trend_channel` slot" |
| 字段逐一对照 GATE `:141-176` | DESIGN `:50-94` | `is_proxy` `proxy_of` `proxy_disclaimer` `method` `params{5}` `bar{2}` `close_confirmed{5}` `sources_used` `window{5}` `ref_close` `upper` `lower` `mid` `width_pct` `distance_to_upper_pct` `distance_to_lower_pct` `price_position` `position_basis` `intraday_position` `intraday_basis` `slope` `slope_pct_per_day` `status` `note` — **无缺项** |
| 契约规则 | DESIGN `:101-107` | 三常量缺一即无效、参数显式、`close_confirmed` 为对象、`price_position` 只由确认 close、`bars_degraded→degraded` / `bars_missing→fail` 不插值、`status` 独立、无顶层 `trend_channel` |
| 现状无 `trend_channel` | py 全文；JSON 顶层键 | JSON 顶层仅 `schema_version, as_of, sources, consensus, ohlc, ohlc_cross_check, status, note`；py / README / JSON `rg trend_channel` 零命中 |
| README shape | README `:81` `:84-96` | 现为 v1 shape（含新增 `kind` / `native_ts?` / `n_agree_venues` / `ts_open_utc` / `closed`），与实际输出一致；`:81` 明示 "channel proxy / `schema_version: 2` comes later" |

判定：齐（契约层）。理由：A5 的输出层要求（实际 JSON 出现 `schema_version: 2` + 带值的 `trend_channel_proxy`）与 GATE `:5` `:285` "过审前禁止产出 upper/lower/price_position" 不可能同时满足；一个只能靠违反闸门才能通过的闸门不成立，故 A5 在过审前只能按**契约文本**核验，输出层留到实现 PR（§5 I1、I2）。这不是改宽，是唯一自洽的读法。

两处契约文本与 GATE §2.4 的语义差（不影响字段完整性，但实现 PR 必须按 GATE 原文做，见 §5 I5）：
- GATE `:183`：`confirmed=false`（grace 内）→ 整块 `status=degraded` 且**沿用上一确认 bar**。DESIGN `:103` 只写了 "not a valid channel input"，未写 degraded + 沿用。
- GATE `:187`：`bars_missing` 非空 → `upper/lower/price_position` 置 `null`。DESIGN `:105` 只写了 fail 不插值，未写置 null（DESIGN `:111` 的 brief 侧 "no channel levels" 部分覆盖）。

### A6 brief 三条规则 — GATE §2.4 — **齐（规则定稿）**

验收（GATE `:274`）：brief 的 prompt / 模板中可见：固定行、禁 `system_signal`、新鲜度阈值。

| 证据 | 位置 | 内容 |
|---|---|---|
| 规则 1 固定行 | DESIGN `:111` | 唯一固定行、显式标签 `proxy · Donchian-close · N=20 · 非 LaoMao 2.0 原版`；`fail` 时只报不可用、不给轨位 |
| 规则 2 禁 `system_signal` | DESIGN `:112` | "must never produce or populate `system_signal` (`full_position`, `cash`, `reduce_30_40`, etc.)"；真值 `trend_channel` 保持 missing 直到原版到位 |
| 规则 3 新鲜度 | DESIGN `:113` | `as_of` > 30 分钟 → 重跑或标 stale；"Stale data is not evidence of a quiet market" |
| 落位 | DESIGN `:115` `:126-128` | "The routine is not part of this task"；本任务只改 DESIGN + README A1 行 |
| 现有 README 侧 | README `:69` `:73` `:76-82` | 不信单一 feed；建议先重跑；`ohlc` 只作 sanity check；不得从中位现价编造轨位——**无 30 分钟阈值、无 system_signal 禁令原文** |

判定：齐（规则定稿）。说明我为什么没有按字面判 "未齐 → REWORK"：
- 严格读法下 A6 要求规则出现在 brief 的 prompt/模板中；材料里没有 prompt/模板，本仓库也没有（`rg -i laomao|brief` 无命中），故落位**待确认**。
- 但 GATE `:285` 同时写了 "过审前禁止…任何往 brief 里写通道行的改动"。申请方按此禁令把 brief 侧改动整体推到实现阶段（DESIGN `:115`），是对闸门的善意遵守；A6 与 `:285` 的张力是 GATE 自己制造的，不应由申请方承担一个额外轮次。
- A6 作为硬项的目的（GATE `:196` fail-close）只在 `trend_channel_proxy` 字段**存在**时才有风险敞口。控制点是实现 PR。故本文把 "落位于 prompt/模板并给出路径" 列为实现 PR 的**硬验收项**（§5 I3），与字段同 PR、同 commit。

三处保真度缺口，实现 PR 落位时必须按 GATE 原文而非 DESIGN 缩写（§5 I3）：
- DESIGN `:111` 只给了标签，GATE `:194` 的固定行是带槽位的全格式：`通道[proxy · Donchian-close N={n} · 非2.0原版]：上轨 {upper} / 下轨 {lower}｜收盘确认 {bar_date} {closed_at_local}：{price_position}｜盘中 {intraday_position}（未确认）｜数据 {status}`。
- DESIGN `:111` 把 `N=20` 写死在 brief 文案里；GATE `:194` 用 `N={n}`。N 必须从 `params.n` 插值，否则改 N 时 brief 会标错，违反 GATE `:105` "N 变更是输出可见事件"。
- DESIGN `:113` 缺 GATE `:197` 后半句：`close_confirmed.bar_date` ≠ 今日 08:00 +08 之前最近一个已收盘 UTC 日 → 标"确认落后"。以及 GATE `:196` 的 `missing_inputs` 必含 `"trend_channel (LaoMao 2.0 original)"`（DESIGN `:112` 只有意思、无该字面）。

### A7 venue / aggregator 法定人数 — F5 — **齐**

验收（GATE `:275`）：`sources[].kind`；`ok` ⇐ ≥3 一致 venue；README `:42-45` 同步。

| 证据 | 位置 | 内容 |
|---|---|---|
| 分类表 | py `:45-58` | `SOURCE_KIND`：8 venue（bitstamp coinbase kraken okx gateio kucoin binance bybit）/ 4 aggregator（coinpaprika yahoo coingecko cryptocompare） |
| 每源带 `kind` | py `:389` `:394` `:408` `:570`；JSON `:7` `:18` `:30` `:41` `:52` `:64` `:73` `:84` `:95` `:106` `:118` `:130` | 12 条记录全部有 `kind` |
| 法定人数 | py `:480-481` `:486-487` | 只有 `kind == "venue"` 进 `agree_venues`；`n_agree_venues >= 3 → ok` |
| degraded | py `:492-493`；README `:65` | 恰 2 一致 venue |
| 输出 | JSON `:144-146` | `n_ok 8` / `n_agree 8` / `n_agree_venues 6`——聚合器 coingecko、yahoo 计入 agreeing（`:152` `:157`）不计入 quorum |
| README 同步 | README `:35-40` `:63-66` `:74` | kind 表；"status (venue quorum — F5/F8)"；引用 `n_agree_venues` |
| 设计 | DESIGN `:119-121` | 锁定 |

判定：齐。今天 6 venue 健康，规则零影响；它只在退化时生效——与 GATE `:83` 的预期一致。

---

## 2. 条件项 A8 / A9

### A8 原子写 + last-good — F6 — **齐（无债）**

验收（GATE `:276`）：tmp+replace；`status=fail` 不覆盖主文件。

| 证据 | 位置 | 内容 |
|---|---|---|
| 原子写 | py `:624-647` | `tempfile.mkstemp` 同目录（`:628-632`）→ 写 → `fsync`（`:639`）→ `os.replace`（`:640`）；异常清理 tmp（`:641-646`） |
| last-good | py `:667-671` | `last_run.json` 每次写（`:668`）；`last_btc_consensus.json` 仅 `status != "fail"` 时写（`:670-671`） |
| `-o` + fail | py `:672-676` | 也拒绝写目标路径（行为正确；注释残留，见 §6） |
| 退出码 | py `:679` | `fail → 1` |
| README | README `:10-11` `:24` | "Last **non-fail** run output (atomic overwrite; not touched on `status=fail`)"；"Writes are atomic (`tmp` + `os.replace`)" |

判定：齐。README `:10` 从 GATE `:36` 时的 "Last successful run output" 改为 "Last non-fail"——与代码（degraded 也写主文件）字面一致，比原措辞更准。

### A9 历史 + 自校验 — F9 — **未齐 → 条件债**

验收（GATE `:277`）：`history/*.jsonl`、`payload_sha256`、`producer`。

证据：py / README / JSON / DESIGN 四文件 `rg -i "history|sha256|producer|jsonl"` **零命中**。`run()`（py `:557-621`）返回体无 `producer`、无 `payload_sha256`；`main()`（py `:649-679`）只写两个 JSON 文件，无 jsonl 追加。

判定：未齐。按 GATE `:281` 记债，进入实现 PR（§5 I4）。

---

## 3. A10 债项现状（F7 F8 F10 F11 F12）——全部已清

申请方自述 "F7、F8/F10/F11/F12 已修"，核验属实，且不在闸门内，只登记：

| 项 | 证据 | 状态 |
|---|---|---|
| F7 Yahoo 回退昨收 | py `:179-182` 只取 `regularMarketPrice`，缺则 `raise`；`rg previousClose` 零命中；README `:57` | 清 |
| F8 全 outlier 给 degraded | py `:501-508` `else → fail`；README `:66` "**not** degraded" | 清 |
| F10 死代码 | py `:441-442` docstring 记录移除；`:485-508` 分支树无不可达支 | 清 |
| F11 各源自带时间戳 | py `:85-97` `_ms_or_s_to_iso`；各 fetcher 三元组返回；`:401-402` 写 `native_ts`；JSON `:24` `:58` `:112` `:124` `:136`（coinbase / kraken / gateio 接口无 ts，返回 `None`，README `:89` 标 `native_ts?` 可选） | 清 |
| F12 噪声源 | py `:61` `EXPECTED_UNAVAILABLE`；`:563-582` 默认跳过并标 `expected_unavailable: true`；`:657-661` `--include-blocked`；JSON `:5-15` `:28-38` `:71-81`；README `:44-52` | 清 |

---

## 4. 对申请方四点主张的明文答复

1. **A1**：齐。署名人为 `老猫`、日期 2026-09-21、Jimmy deferred 记录在案、读法唯一（DESIGN `:11-18`；README `:29`）。锚点是 GATE 默认值，GATE §6 `:295` 推翻条件继续有效；实现时锚点必须是参数（§1 A1）。
2. **A4**：齐。N=20 是 GATE `:105` 规定的首次 shadow 默认，Jimmy 未选不构成缺项；未实现 `upper/lower/price_position` 是**正确**的，GATE `:285` 过审前禁止。
3. **现货修复 + `schema_version` 仍为 1**：修复核验属实（§1 A2、A3、A7；§2 A8；§3）。`schema_version: 1` 现在是**正确**的：v2 的定义就是 "含 `trend_channel_proxy` 块"（GATE `:134`），在块不存在时把版本号改成 2 是 schema 说谎。`SCHEMA_VERSION`（py `:35`）→ 2 必须与 `trend_channel_proxy` 块**同一 commit** 落地（§5 I1）。
4. **若 Conditional PASS，A8/A9 是否必须同实现 PR**：**是。** GATE `:281` 原文："A1–A7 齐、A8/A9 未齐 → Conditional PASS，A8/A9 记 pitfalls 并在实现 PR 内一并完成。" 本文不改宽。具体到本次：A8 已齐，无债；**A9 是唯一条件债，必须在实现 PR 内完成，不得拆到后续 PR。** 这不是程序要求，是依赖关系：(a) GATE §4 `:261` 建议的 ≥14 UTC 日 shadow 观察靶就是 `history/*.jsonl` 里 `price_position` 翻转频率——没有 history，shadow 期产生不了证据；(b) `payload_sha256` / `producer` 保护的正是即将首次承载轨位数字的那个文件。实现 PR 若缺 A9 而合并，本 Conditional PASS 自动失效（§6）。

---

## 5. 实现 PR 验收清单（全部源自 GATE，非新增要求）

实现 PR 合并前逐项可检查。I1–I5 为**硬**（对应 A4/A5/A6/A9 的输出层与 GATE §2.4 语义），I6 为 GATE `:261` 的建议项。

| # | 项 | 来源 | 可直接检查的验收 |
|---|---|---|---|
| I1 | 通道输出落地 | A4 A5 | 实际 JSON：`schema_version: 2`（py `:35` 同 commit 改）；`trend_channel_proxy` 含 DESIGN `:50-94` 全部字段；`params.n` 出现；**不存在**顶层 `trend_channel`；既有 v1 键全部不变 |
| I2 | README 同步 | A5 | README `:84-96` JSON shape 升 v2；`:81` "comes later" 句改写 |
| I3 | brief 规则落位 | A6 | 提供 brief prompt / 模板**路径**；其中可见 GATE `:194` 全格式固定行（`N={params.n}` 插值，不写死 20）、`:196` `system_signal` 禁令 + `missing_inputs` 含 `"trend_channel (LaoMao 2.0 original)"` 字面、`:197` 30 分钟阈值 + "确认落后" 判定。**与 I1 同 PR 同 commit**：字段先于规则出现即 fail-close 破口 |
| I4 | A9 条件债 | A9 | `history/YYYY-MM.jsonl` 每次运行追加一行；顶层 `producer {script, version, host, pid}`；`payload_sha256`（对去掉该字段后的规范化 JSON 计算）；README 说明 |
| I5 | GATE §2.4 语义 | A3 A5 | `close_confirmed.confirmed` = `closed` ∧ `now ≥ t_open + 86400 + grace_min`，不得直接用 `closed`；`confirmed=false` → 块 `status=degraded` 且沿用上一确认 bar（GATE `:183`）；`bars_missing` 非空 → `upper/lower/price_position` = `null`（GATE `:187`）；锚点参数化（§1 A1） |
| I6 | shadow | GATE `:261` | 建议：固定行进 brief 前先 shadow ≥14 UTC 日（只写文件 + history）。建议不作闸门，与 GATE 一致 |

---

## 6. 新发现（本次复审新增，均不阻塞放行）

格式：`[Px][confidence] 标题 — 证据`。

- **[P2][0.60 待确认] 原子写后文件权限收窄** — py `:628-632` `tempfile.mkstemp` 以 `0600` 建 tmp，`os.replace` 后主文件继承 `0600`。若共享盒上读 brief 的 agent 与写脚本的 unix 用户不同 → `EACCES`，"文件缺失 ≠ 平静"（GATE `:197`）的另一种形态。核验：盒上 `ls -l last_btc_consensus.json`；若非同用户，`os.replace` 前 `os.chmod(tmp, 0o644)`。无法从材料判定用户模型，故标待确认。
- **[P3][0.90] `kind` 缺省值宽松** — py `:389` `:570` `SOURCE_KIND.get(name, "venue")`：未登记的新源默认算 venue、直接计入法定人数，与 F5 方向相反。应缺省 `"aggregator"` 或直接 `raise`。当前 12 源全部登记，零影响。
- **[P3][0.85] `closed` ≠ `confirmed`** — py `:271` 时间回退无 grace；OKX 走 venue `confirm`（`:264-265`）。实现若复用 `closed` 作 `close_confirmed.confirmed`，边界后数分钟内可能把所端未滚动的 bar 当已确认。已列 I5。
- **[P3][0.85] brief 固定行写死 N** — DESIGN `:111` `N=20` 字面 vs GATE `:194` `N={n}`。已列 I3。
- **[P3][0.80] DESIGN 契约规则漏两条 GATE 语义** — GATE `:183`（grace 内 degraded + 沿用）、`:187`（missing → null）未在 DESIGN `:101-107` 出现。已列 I5。
- **[P3][0.90] `daily_cross_check[0]` 是活 bar 对比** — JSON `:383-393` 四源 09-21 `closed: false`（`:169` `:222` `:275` `:328`），其 `ok: true` 含义是 "盘中一致"，非 "日收一致"；`cross_check_ohlc` docstring（py `:525-527`）明示允许。作为现货 sanity check 可接受，但读者易误读；建议 `daily_cross_check[*]` 加 `closed: bool` 或跳过活 bar。与通道输入无关（A3 已隔离）。
- **[P3][0.80] coinpaprika 402 配额** — JSON `:63-69` "HTTP 402 … soft_limit 60 requests per hour"。说明脚本运行频率或盒 IP 共享配额已触顶；聚合器不影响 quorum，但 README `:73` "re-run the script before advising" 若被 brief 每次照做，会持续烧配额。建议：`as_of` 距今 < 阈值（GATE `:197` 的 30 分钟）时复用文件，不重跑。
- **[P3][0.95] `-o` + fail 分支注释残留** — py `:672-676`：行为正确（拒绝覆盖），注释是半截自问自答，应清理。
- **[P3][0.80] fail 分支 note 措辞失真 + README 枚举缺一情形** — 1 venue + ≥2 aggregator 一致时：py `:501-508` 判 `fail`（保守、正确），但 note 写 "No agreeing pair"（实有一致对，只是非 venue）；README `:66` 的 fail 条件未覆盖 "一致 venue < 2 但有一致 aggregator"。建议 note 改为 "agreeing venues < 2"，README `:66` 补一句。

**不立案（复审过，无问题）**：Kraken `interval=1440` 取 `rows[-limit:]`（`:345`）、Coinbase `data[:limit]`（`:365`）、Bitstamp `reversed(rows[-limit:])`（`:320`）newest-first 归一化正确；OKX `confirm` 字段解析（`:298` `:264-265`）；`atomic_write` 异常路径清理 tmp（`:641-646`）；USD/USDT 混池与 0.5% 阈值维持 GATE 结论。

---

## 7. 推翻条件与置信度

| 结论 | 置信度 | 会推翻它的证据 / 事件 |
|---|---|---|
| 总判 Conditional PASS（而非 REWORK） | 0.85 | 见下两行任一成立 |
| A6 "规则定稿即齐" | 0.70 | 原则方认定 "可见于 prompt/模板" 必须在实现前落位 → 本裁决降为 **REWORK**，唯一整改项：把 GATE `:194-197` 三条全文写入 brief prompt/模板并提供路径，再提 RECHECK。除此之外 A1–A5、A7、A8 无需再审 |
| A5 契约层读法 | 0.90 | 只有在有人能给出 "不实现通道也能让实际 JSON 出现带值的 `trend_channel_proxy`" 的方法时才推翻——我找不到 |
| A1 锚点 = 08:00 +08 | 0.80 | Jimmy 从原始消息确认北京时间零点 → 走 GATE §2.3 `:130` 路径 (ii)；因 I5 要求参数化，代价是数据管线改造而非重写 |
| Conditional PASS 有效性 | — | 实现 PR 合并时缺 I3 或 I4 任一 → 本 Conditional PASS **自动失效**，回到 REWORK，且应阻止合并 |
| 不升 REFUSE | 0.90 | 若发现任何 brief 已用 proxy 轨位产出 `system_signal` 且有人据此操作 → 按 GATE `:293` 升 REFUSE，先撤 brief 行 |

---

## 8. 非目标（本次明确不做）

- 不实现、不试算任何通道数值；不替 Jimmy 选 N；不做外部探针（JSON 已与 GATE 探针对账）。
- 不改 uploads 四份材料；不改 py；不改 README；不改 GATE 原文。
- 不评估 DIF / 钝化 / 结构；不做 H/L Donchian、不做斜带、不做回测。
- 不做 HMAC / 签名 / 证书钉扎（维持 GATE §2.5 结论）。
- 不涉及下单、仓位或任何执行面。

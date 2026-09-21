PASS

# IMPL-GATE r2：老猫 BTC「通道代理」实现闸再验（REWORK → PASS）

> 裁决：**PASS**。上次 IMPL-GATE §3 REWORK 清单 R1–R6 全部齐；RECHECK §5 I1–I5 复扫全部仍齐。**允许 brief 开始写固定代理行；仍禁由 proxy 推 `system_signal`**（放行文案全文见 §3）。
> 对照物：`architecture/IMPL-GATE-laomao-btc-channel-2026-09-21.md`（PR [#6](https://github.com/licett/ai-workflow-kit/pull/6)，分支 `cursor/impl-gate-laomao-btc-channel-5ca5`，commit `d8b2844`，下称 IMPL-GATE）；`architecture/RECHECK-laomao-btc-channel-data-2026-09-21.md`（PR [#5](https://github.com/licett/ai-workflow-kit/pull/5)，commit `42dd77c`，下称 RECHECK）；`architecture/GATE-laomao-btc-channel-data-2026-09-21.md`（PR [#4](https://github.com/licett/ai-workflow-kit/pull/4)，commit `3679f49`，下称 GATE）。uploads 内 IMPL-GATE / RECHECK 副本与分支文件逐字节一致（`diff -q`）。"GATE `:N`" 等指对应 commit 内行号。
> 范围：只审 `uploads/` 实现材料——`DESIGN-channel-proxy-v0.md`（下称 DESIGN，Status "R1–R6 fixed"）、`README.md`、`btc_multisource.py` v2.0.1（下称 py）、`last_btc_consensus.json`（下称 JSON，`as_of 2026-09-21T02:42:21Z`）、`history/2026-09.jsonl`（2 行）、`impl-gate-probes/probe-A.json` / `probe-B.json` / `probe_grace_r5.py`。不改代码、不改 uploads；本文是本次唯一新增文件。
> 方法：文档 / 代码 / 数据对读；GATE `:193-198` 与 README / DESIGN 逐字节比对（脚本提取反引号内容 `==`）；在隔离目录复跑申请方 `probe_grace_r5.py` 并与提交的 probe-A / B 逐键比对；对 py 追加离线函数探针 C–H（注入 `now=` 与裁剪 `ohlc`）；独立重算 Donchian 窗口、`payload_sha256`。**无外部网络动作**。
> 验收标准：IMPL-GATE §3 R1–R6 验收列原文 + RECHECK §5 I1–I5 原文，不改宽、不改窄。
> 日期：2026-09-21。

---

## 0. 总判

| 项 | 来源 | 上次 | 本次 | 一句话 |
|---|---|---|---|---|
| R1 brief 固定行全格式 | I3 / GATE `:193-195` | ✗ | **齐** | README `:101-102`、DESIGN `:118-119` 两行与 GATE `:194-195` 反引号内容**逐字节相等**；9 个槽位齐 |
| R2 N 插值 | I3 / GATE `:194` `:105` | ✗ | **齐** | 模板内只有 `N={n}`；`N=20` 字面不在模板行（README `:100` / DESIGN `:117` 括注"noted separately"），符合"可另注" |
| R3 `missing_inputs` 字面 | I3 / GATE `:196` | ✗ | **齐** | README `:103`、DESIGN `:120` 出现 `"trend_channel (LaoMao 2.0 original)"` 字面 + must include / until supplied |
| R4 确认落后 + 文件缺失 | I3 / GATE `:197` | ✗ | **齐** | README `:104`、DESIGN `:121` 含 `close_confirmed.bar_date` ≠ "今日 08:00 +08 之前最近一个已收盘 UTC 日" → "确认落后"；"文件缺失 ≠ 平静，陈旧 ≠ 当前"全句 |
| R5 grace 内 `degraded` | I5 / GATE `:183` | ✗ | **齐** | 探针 A 复跑与提交件逐键相同：`bar_date=D`、`confirmed=false`、`age_min=5.0`、`status=degraded`、轨位 = D−1 值（独立重算一致）、note 含 "in grace; carrying D−1"；探针 B 不变 |
| R6 锚点单一来源 | I5 / RECHECK `:51` | ✗ | **齐** | py `:64-67` 三常量 → `_bar_dict` `:647`（两分支共用 `:701` `:850`）；`_close_instant_utc` `:656`、`_format_closed_at_local` `:661`、`_make_close_confirmed` `:667` 各一处；fail 分支（探针 C）`closed_at_local` 亦为 `+08:00`。残留一处命名层面的软点，P3，§4 |
| I1 通道输出落地 | RECHECK `:214` | 齐 | **仍齐** | JSON v2.0.1：24 键与 DESIGN 契约键集**逐键相等**（含 4 子对象）；无顶层 `trend_channel`；v1 八键不变；Donchian 独立重算逐分一致 |
| I2 README 同步 | RECHECK `:215` | 齐 | **仍齐** | README `:120-153` v2 shape；`comes later` 零命中 |
| I3 brief 规则落位 | RECHECK `:216` | 未齐 | **齐** | 路径 = `README.md § Brief safety rules (mandatory)`，README `:93-96` 自宣 prompt-of-record + 盒上绝对路径；DESIGN A6 `:111-122` 镜像。= R1–R4 |
| I4 A9 条件债 | RECHECK `:217` | 齐 | **仍齐** | history 2 行，两行 sha 独立重算一致，第 2 行与 JSON 深度相等；`producer` 四键；单次 `f.write(line+"\n")` `:1029` |
| I5 GATE §2.4 语义 | RECHECK `:218` | 部分未齐 | **齐** | `confirmed = closed ∧ grace`（探针 F、G0–G2 边界）；grace → degraded + 沿用（探针 A）；`bars_missing → null`（探针 D）；锚点（R6） |
| I6 shadow | GATE `:261` | 未开始 | 未开始 | history 两行 `host = "cursor"`，盒上仍无 v2 产物；维持"建议不作闸门" |

置信度：总判 PASS 0.88。R1–R4 0.97（字节级比对）；R5 0.92（探针可复现、独立重算一致）；R6 0.75（§4 软点与 §6 推翻条件）；I1 / I4 0.95。

---

## 1. R1–R6 逐项（按 IMPL-GATE §3 编号）

格式：上次验收原文 → 证据（文件:行）→ 判定。

### R1 brief 固定行全格式 — **齐**

验收（IMPL-GATE `:137`）：README §Brief safety rules 与 DESIGN A6 出现 `:194` 两行原文（`ok|degraded` 版与 `fail` 版），槽位齐：`{n}` `{upper}` `{lower}` `{bar_date}` `{closed_at_local}` `{price_position}` `{intraday_position}` `{status}` `{note}`。

| 证据 | 位置 | 内容 |
|---|---|---|
| `ok\|degraded` 行 | README `:101`；DESIGN `:118` | 反引号内容与 GATE `:194` `通道[proxy · Donchian-close N={n} · 非2.0原版]：上轨 {upper} / 下轨 {lower}｜收盘确认 {bar_date} {closed_at_local}：{price_position}｜盘中 {intraday_position}（未确认）｜数据 {status}` **字节相等**（Python `==`，含全角 `｜` `：` `（未确认）`） |
| `fail` 行 | README `:102`；DESIGN `:119` | `通道[proxy]：不可用（{note}）` 与 GATE `:195` 字节相等；"不得出现任何轨位数字"句同在 |
| 触发条件 | README `:100`；DESIGN `:117` | `（`status=ok\|degraded` 时必出）` 与 GATE `:193` 一致 |
| 槽位 | README `:101-102` | 8 + 1 个槽位脚本逐一命中 |
| 差异（不影响判定） | README `:102`、DESIGN `:119` | 在"时改为"后插入 "EXACT" 一词；固定行本体不受影响 |

判定：齐。上次 §1 I3 指出的"盘中已破、待 08:00 确认"槽位（`盘中 {intraday_position}（未确认）`）现已在模板中。

### R2 N 插值 — **齐**

验收（IMPL-GATE `:138`）：brief 文案中 N 只以 `{n}` / `{params.n}` 出现；文档可另注"当前 `params.n = 20`"，但不得进入固定行模板。

| 证据 | 位置 | 内容 |
|---|---|---|
| 模板内 | README `:101`；DESIGN `:118` | 只有 `N={n}`；脚本检查 `"N=20" in 模板行` → False（两处） |
| 另注 | README `:100`；DESIGN `:117` | "N only as `{n}` / `{params.n}` inside the line; current default `params.n=20` is noted separately, not hard-coded in the fixed line" |
| 设计锁 | DESIGN `:38` | "brief fixed line interpolates `N={n}` / `{params.n}`, never hard-codes 20 inside the template" |
| 其余 `N=20` 出现处 | README `:79` `:82`（proxy 规则表）；DESIGN `:38` `:103`；py `:58` `PROXY_N = 20`；JSON `:1706` | 均为参数值陈述，非 brief 模板 |

判定：齐。

### R3 `missing_inputs` 字面 — **齐**

验收（IMPL-GATE `:139`）：出现原文：`missing_inputs` 必含 `"trend_channel (LaoMao 2.0 original)"` 直到真值到位。

| 证据 | 位置 | 内容 |
|---|---|---|
| 字面 | README `:103`；DESIGN `:120` | `` `missing_inputs` **must** include the literal `"trend_channel (LaoMao 2.0 original)"` until the real LaoMao 2.0 channel is supplied `` |
| 与 GATE `:196` 对照 | — | 字面串 `"trend_channel (LaoMao 2.0 original)"` 三处字节相同；"必含 / 直到真值到位"以英文 must include / until supplied 表达，语义等价、无弱化 |
| `system_signal` 禁令（同段） | README `:103`；DESIGN `:120` | "禁止由 proxy 推出框架模板的 `system_signal`（`full_position` / `cash` / `reduce_30_40` 等）。允许说"若按 proxy 通道，价格位于 X"；不允许说"2.0 系统触发满仓 / 清仓"" 三句与 GATE `:196` 中文原句相同（反引号切分 `full_position` / `cash` / `reduce_30_40` 为三个 code span，GATE 为一个，内容不变） |

判定：齐。上次判 ✗ 的唯一原因是"意思在、字面无"；字面现已在。

### R4 确认落后 + 文件缺失 — **齐**

验收（IMPL-GATE `:140`）：出现：`close_confirmed.bar_date` ≠ "今日 08:00 +08 之前最近一个已收盘 UTC 日" → 标"确认落后"；"文件缺失 ≠ 平静，陈旧 ≠ 当前"。

| 证据 | 位置 | 内容 |
|---|---|---|
| 确认落后 | README `:104`；DESIGN `:121` | `` `close_confirmed.bar_date` 不等于"今日 08:00 +08 之前最近一个已收盘 UTC 日" → 标"确认落后" ``，与 GATE `:197` 逐字相同 |
| 文件缺失 | README `:104`；DESIGN `:121` | "**文件缺失 ≠ 平静，陈旧 ≠ 当前。**"全句（GATE 无加粗，其余相同） |
| 30 分钟 | README `:104`；DESIGN `:121` | "`as_of` 距今；> 30 分钟 → 重跑或标"陈旧"" |
| 第 4 条 | README `:105`；DESIGN `:122` | 与 GATE `:198` 相同（DESIGN `:122` 句末为 ASCII `.`，GATE 为 `。`；P3，§4） |

判定：齐。R4 落地后，探针 H（§2 I5）所示的"D 未到、静默回退 D−1"路径在 brief 侧有了兜底信号。

### R5 grace 内 `degraded` — **齐**

验收（IMPL-GATE `:141`）：以 `now=` 注入检验：`now ∈ [close(D), close(D) + grace_min)` 时 → `close_confirmed = {bar_date: D, closed_at_utc: close(D), confirmed: false, age_min < grace_min}`，`status = "degraded"`，`ref_close / upper / lower / mid / price_position / window` = 上一确认 bar D−1 的值（与上一次运行相同），`note` 点名 "in grace; carrying D−1"。grace 外行为不变（探针 B）。

**复现**：将 uploads 的 py / JSON / `probe_grace_r5.py` 按其 `parents[1]` 布局放入隔离目录运行 → 退出码 0；生成的 probe-A.json / probe-B.json 与申请方提交件 **逐键相等**（`sort_keys` 归一化后 `diff` 为空）。提交件可核。

| 项 | 探针 A（`now = 2026-09-21T00:05:00Z`） | 验收 | 判定 |
|---|---|---|---|
| `close_confirmed` | `{bar_date: 2026-09-20, closed_at_utc: 2026-09-21T00:00:00Z, closed_at_local: 2026-09-21T08:00:00+08:00, confirmed: false, age_min: 5.0}` | D、close(D)、false、< 10 | ✓ |
| `status` | `degraded` | degraded | ✓ |
| 沿用 D−1 | `ref_close 81234.525`、`upper 81264.495`、`lower 75584.635`、`mid 78424.565`、`price_position inside`、`window 2026-08-30..2026-09-18 (20)` | = 上一确认 bar 09-19 的值 | ✓ 独立重算"以 09-19 为确认 bar"：ref = 09-19 median close（81233.91 / 81235.14 中位 = 81234.525）、窗 08-30..09-18、max 81264.495（09-03）、min 75584.635（09-15）、OLS −0.114596 %/日 → `down`，与 probe-A `full_proxy` 逐分一致 |
| `note` | `in grace; carrying D−1=2026-09-19 (D=2026-09-20 unconfirmed, age_min=5.0, grace_min=10)` | 含 "in grace; carrying D−1" | ✓ |
| 探针 B（`00:15:00Z`） | 09-20、`confirmed: true`、`age_min 15.0`、`ok`、窗 08-31..09-19、ref 81161.82，与上次 IMPL-GATE 探针 B 及 JSON `:1716-1750` 一致 | grace 外不变 | ✓ |

代码路径：py `:929-933` 取最新已到收盘时刻的 bar D；`:948` `in_grace = now < close_d + grace`；`:950-978` grace 内 `_make_close_confirmed(d_closed, confirmed=False)` + 以 D−1 为确认 bar调 `_donchian_levels_for_confirm(..., status_force="degraded", note_extra=...)`；`:980-989` grace 外正常确认。`status_force` 在 `:818-819` 优先于 `bars_degraded` 判定；`note_extra` 在 fail 骨架（`:780-791`）与正常返回（`:825-826`）两路都带出。

边界补探（本次新增，均符合 GATE `:101` 的 `≤`）：`00:00:00Z` → grace 内 degraded（区间左闭）；`00:09:59Z` → grace 内 degraded；`00:10:00Z` → 确认 D、ok。

判定：齐。

### R6 锚点单一来源 — **齐**

验收（IMPL-GATE `:142`）：一组模块级锚点常量（boundary tz、UTC 收盘时刻、本地标签 / 时区）同时驱动输出 `bar{}` 与原 `:759` / `:789` 的计算；`closed_at_local` 两分支同为 `+08:00` 格式。**不要求**实现 GATE `:130` 路径 (ii)，不要求 CLI 开关。

| 上次现状（IMPL-GATE `:142`） | 本次 | 位置 |
|---|---|---|
| `bar{}` 两处重复字面（原 `:664-665` / `:891-892`） | 单一 `_bar_dict()` 读 `BAR_BOUNDARY_TZ` / `BAR_CLOSE_LOCAL`；fail 骨架 `:701` 与 ok 路径 `:850` 同调 | py `:64-66` `:647-653` |
| 收盘时刻写死在原 `:759` | 单一 `_close_instant_utc(bar_date)`（docstring 明示 "(D+1) 00:00 UTC (= 08:00 Asia/Shanghai)"），被 `:931` 选 bar、`:937` fail note、`:947` grace 判定、`:670` `close_confirmed` 共用 | py `:656-658` |
| `"+08:00"` 字面拼接在原 `:789` | 单一 `_format_closed_at_local()`：`astimezone(TZ_SHANGHAI)` 实算本地时刻 + `CLOSED_AT_LOCAL_OFFSET` 常量 | py `:49` `:67` `:661-664` |
| fail 分支原 `:779` 用 `%z` 得 `+0800` | 全部 `close_confirmed` 经 `_make_close_confirmed()` 生成（`:943` `:953` `:981` 三处调用）；py 全文 `%z` 零命中 | py `:667-678` |
| 两分支格式不一致 | 探针 C（fail 分支 "No closed bar yet"）`closed_at_local = 2026-09-21T08:00:00+08:00`；探针 A / B / D / E 同格式 | 探针输出 |

DESIGN `:19` 同步："module-level constants `BAR_BOUNDARY_TZ` / `BAR_CLOSE_LOCAL` / `CLOSED_AT_LOCAL_OFFSET` drive both `bar{}` output and `closed_at_local` formatting (always `+08:00`, never `+0800`)"。

判定：齐。上次列出的四处缺陷全部消除；每个关注点各有唯一来源；两分支格式统一。残留：UTC 收盘时刻以单一 helper（`+timedelta(days=1)` 于 UTC 日期）表达而非命名常量，`BAR_CLOSE_LOCAL` 是标签而非由 `TZ_SHANGHAI` + 收盘时刻派生——走路径 (ii) 时需同改 `:64-67` 与 `:656-658`（同一屏内、注释互指）。R6 明文不要求 (ii)，故记 P3（§4），推翻条件见 §6。

---

## 2. I1–I5 复扫（RECHECK §5 原文）

### I1 通道输出落地 — **仍齐**

| 证据 | 位置 | 内容 |
|---|---|---|
| `schema_version: 2` | py `:39`；JSON `:2` | 与 `trend_channel_proxy`（py `:1095-1099` 计算、`:1108` 进返回体；JSON `:1700`）同文件、同产物；`SCRIPT_VERSION = "2.0.1"`（`:40`）→ JSON `:1756` |
| 字段完整 | JSON `:1700-1750` vs DESIGN `:50-96` | 脚本解析 DESIGN 契约 JSON 块 → 24 个顶层键**顺序与集合均相等**；`params{5}` `bar{2}` `close_confirmed{5}` `window{5}` 键集相等；无缺项、无多项 |
| `params.n` | JSON `:1706` `"n": 20` | 出现 |
| 无顶层 `trend_channel` | JSON 顶层 11 键 | `schema_version, as_of, sources, consensus, ohlc, ohlc_cross_check, trend_channel_proxy, status, note, producer, payload_sha256`；py `:1169` `result.pop("trend_channel", None)` 硬不变量保留 |
| 三常量 | JSON `:1701-1703`；py `:52-56` | 与 GATE `:145-147` 逐字相同 |
| v1 键不变 | JSON | 八键全在，纯新增三键 |

**独立重算（`as_of 02:42:21Z`）**：四所 `closed=true` candle → 逐日 median、剔 >0.5%（每日 kept=4）→ 以 grace 10 min 选确认 bar **2026-09-20**（age 162.35 min；JSON `:1721` 162.4 为含微秒 `now` 的四舍五入）→ 窗 **08-31..09-19** 20 根 → upper **81264.495**（09-03）/ lower **75584.635**（09-15）/ mid 78424.565 → `ref_close` 81161.82 → **inside**；OLS **−0.067296** → `flat`；`intraday_position`：现货中位 81260.845 < upper 81264.495 → **inside**。与 JSON `:1729-1747` 逐分一致。（上次样例 02:24:47Z 现货 81466.94 为 `above_upper`，本次已回落 inside——shadow 期第二个观察点。）

### I2 README 同步 — **仍齐**

README `:120-153` v2 shape（`:123` `schema_version: 2`，`:130-145` `trend_channel_proxy` 全字段，`:148-149` `producer` / `payload_sha256`，`:153` "No top-level `trend_channel` key"）；`comes later` 零命中；`:12` history、`:13` DESIGN 进文件表；`:26` fail 时 history 仍追加；`:33` closed-only + grace。

### I3 brief 规则落位 — **齐**（= R1–R4）

验收（RECHECK `:216`）：提供 brief prompt / 模板**路径**；其中可见 `:194` 全格式固定行（N 插值）、`:196` 禁令 + `missing_inputs` 字面、`:197` 30 分钟 + 确认落后；与 I1 同 PR 同 commit。

| 子项 | 证据 | 判定 |
|---|---|---|
| 路径 | README `:93-96`："This section **is** the brief prompt-of-record … Any brief routine MUST embed this section **verbatim** and link back here (`/home/box/agent-data/shared/council/laomao/data/README.md` § Brief safety rules)"；DESIGN `:113` 镜像并回链 | ✓ 与 IMPL-GATE §2-3 裁定的落位方式一致：路径 = `README.md § Brief safety rules (mandatory)` |
| `:194` 全格式 + N 插值 | R1、R2 | ✓ |
| `:196` 禁令 + 字面 | R3 | ✓ |
| `:197` 30 分钟 + 确认落后 | R4 | ✓ |
| 同 PR 同 commit | uploads 无 git 史；py 2.0.1 / README / DESIGN 为同一交付包，history 第 2 行为其产物 | 以同产物为限，PR diff 时复核（与上次 I1 同一保留） |

IMPL-GATE §2-4 的升级条件（"任何 brief 产物引用 `trend_channel_proxy` 而其 prompt 未含 `:193-197` 原文 → Conditional PASS 自动失效"）**继续有效**，现在有了可比对的原文。

### I4 A9 条件债 — **仍齐**

| 证据 | 位置 | 内容 |
|---|---|---|
| history | `history/2026-09.jsonl` 2 行，行尾换行 | 行 1 `as_of 02:24:47Z` v2.0.0 pid 3129070；行 2 `as_of 02:42:21Z` v2.0.1 pid 3140803，与 JSON **深度相等** |
| `payload_sha256` | JSON `:1760`；两行 history | 三处独立重算（去字段 → `sort_keys, separators=(",",":"), ensure_ascii=False` → sha256）全部一致：`9c0c8af0…ee2a93`（JSON / 行 2）、`9bdcc3c9…f46e92`（行 1） |
| `producer` | JSON `:1754-1758`；py `:992-1003` | `{script, version, host, pid}` 四键 |
| 单次写 | py `:1028-1031` | `f.write(line + "\n")` + flush + fsync——上次 P3"两次 write"已清 |
| README | `:12` `:26` `:87` `:148-149` | 齐 |

### I5 GATE §2.4 语义 — **齐**

探针：`import` uploads 的 py，`compute_trend_channel_proxy(ohlc=JSON.ohlc, spot_median=81260.845, now=<注入>)`，必要时裁剪 `ohlc`。

| 条 | 探针 | 结果 | 判定 |
|---|---|---|---|
| `confirmed` = `closed` ∧ `now ≥ close(D) + grace`，不得直接用 `closed` | F：`now = 2026-09-20T23:00Z`（09-20 在 JSON 中 `closed=true`） | 确认 bar 回到 09-19、`confirmed: true`、ok；09-20 不被确认 | ✓ py `:901-903` 只收 `closed`，`:931` `:948` 再叠加收盘时刻与 grace |
| grace 内 → `degraded` + 沿用上一确认 bar（GATE `:183`） | A / G0 / G1 | 见 R5 | ✓ |
| `bars_missing` 非空 → `upper/lower/price_position = null`，`fail`（GATE `:187`） | D：抽掉四所 09-10，`now = 00:15Z` | `fail`、`bars_missing: ["2026-09-10"]`、`upper/lower/mid/price_position/slope` 全 `null`、`window.bars 19`；D-grace（`00:05Z`）→ 同 fail，note 同时带 "no interpolation; in grace; carrying D−1" | ✓ py `:780-791` |
| `bars_degraded` → `degraded`（GATE `:186`） | E：09-10 只留 bitstamp | `degraded`、`bars_degraded: ["2026-09-10"]`、轨位照常 | ✓ |
| 锚点参数化（RECHECK `:51`） | R6 | 见 R6 | ✓ |

补充探针 H（新增，不改判定）：抽掉四所 09-20 `closed` candle（模拟 00:05Z 所端未滚动），`now = 00:05Z` → 输出 `bar_date 09-19`、`confirmed: true`、`ok`、无 grace 标记。原因：grace 判定以 `series` 中最新已到收盘时刻的 bar 为 D（`:929-933`），D 由数据而非墙钟定义。正常情况下（探针 A 用真实 JSON）二者一致；异常情况下依赖 brief 侧 R4 "确认落后"（09-19 ≠ 09-20）兜底。两层齐后信号不缺，记 P3（§4）。

### I6 shadow — 建议项，未开始

history 两行均 `producer.host = "cursor"`（JSON `:1757`），非盒上产物；盒上 shadow 计时**尚未开始**。维持 GATE `:261` / RECHECK `:219` / IMPL-GATE §4 "建议不作闸门"。

---

## 3. 放行文案（本次生效）

按 IMPL-GATE §4 预告原文放行：

> **允许 brief 开始写固定代理行**（GATE `:194` 全格式，N 从 `params.n` 插值，`fail` 时只写 `通道[proxy]：不可用（{note}）`）；**仍禁由 proxy 推出 `system_signal`**，`missing_inputs` 必含 `"trend_channel (LaoMao 2.0 original)"`；新鲜度 30 分钟与"确认落后"两条门槛同步生效；`bars_degraded` 非空时点名日期（GATE `:198`）。

执行边界（不新增要求，只列已有约束的落点）：

1. brief 侧唯一 prompt-of-record 为 `README.md § Brief safety rules (mandatory)`（README `:91-105`）；任何 brief routine 建立时逐字嵌入该节并回链（README `:94-95` 自述）。routine 建立后，把路径补进 DESIGN `:143`（"No routine/scheduler update"）即可。
2. 今天（2026-09-21，`as_of 02:42:21Z`）按模板应写：`通道[proxy · Donchian-close N=20 · 非2.0原版]：上轨 81264.495 / 下轨 75584.635｜收盘确认 2026-09-20 2026-09-21T08:00:00+08:00：inside｜盘中 inside（未确认）｜数据 ok`。`status=degraded`（含 grace 内）同格式、`{status}` 填 `degraded`。
3. `system_signal` 继续为空；`missing_inputs` 继续含字面。GATE `:293` REFUSE 升级条件不变：发现任何 brief 已用 proxy 轨位产出 `system_signal` 且有人据此操作。
4. README `:96`、DESIGN `:6` `:113` `:142` 的 "Do not enable … until impl-gate recheck passes" 句，其条件自本文起满足；建议申请方把这几句改为回链本文（顺手，非闸门）。
5. I6 shadow ≥14 UTC 日仍为建议：从首行 `producer.host ≠ cursor` 的盒上 history 记录起算；观察靶 = `history/*.jsonl` 中 `price_position` 翻转频率（RECHECK `:204`）。今天已有两个观察点：02:24Z 确认 inside / 盘中 above_upper；02:42Z 确认 inside / 盘中 inside。

---

## 4. 新发现（本次新增，均不阻塞）

格式：`[Px][confidence] 标题 — 证据`。

- **[P2][0.90] `--now` 会写真实文件** — py `:1153-1165` 解析 `--now`；`:1167` `run(now=now_arg)` 使 `as_of`（`:1039`）取注入时钟；`:1175-1178` 照常写 `last_run.json` 与（`status != fail` 时）`last_btc_consensus.json`，`:1186-1190` 追加 history。在盒上跑 `--now 2026-09-21T00:05:00Z` 会把一份 `as_of` 为过去时刻、proxy `degraded` 的快照顶掉当前好数据。兜底：brief 30 分钟新鲜度会标"陈旧"。建议 `--now` 隐含不写文件（或加 `--dry-run`），README 未提 `--now`。申请方的 `probe_grace_r5.py` 走函数级注入、不写文件，是正确用法。
- **[P3][0.85] grace 判定以数据而非墙钟定 D** — 探针 H（§2 I5）。所端全部未滚动时静默回退 D−1 `ok`。brief 侧 R4 兜底。若要在数据层也出信号：D 缺席且 `now ∈ [close(D_wall), close(D_wall)+grace)` 时可标 `degraded` + note "awaiting D"。
- **[P3][0.90] `age_min` 四舍五入越过 grace** — 探针 G1：`00:09:59Z` → `confirmed: false` 但 `age_min: 10.0`（9.983 → 10.0，py `:677` `round(…, 1)`）。brief 只能以 `confirmed` 判 grace，不得用 `age_min < grace_min` 反推。R5 验收的 `age_min < grace_min` 在探针 A（5.0）成立；边界秒级例外是显示精度问题。
- **[P3][0.80] "No closed bar yet" 分支 `age_min` 为负** — 探针 C：`age_min: -60.0`（`:671` 直接相减）。语义可读（"60 分钟后收盘"），但 brief 若把负值当陈旧度会误判；该分支 `status=fail`，brief 只写不可用行，实际无害。
- **[P3][0.75] R6 残留：UTC 收盘时刻非命名常量** — `_close_instant_utc` `:656-658` 用 `+timedelta(days=1)` 隐含 00:00 UTC；`BAR_BOUNDARY_TZ` `:65` 不参与计算；`BAR_CLOSE_LOCAL` `:66` 为标签非派生。路径 (ii) 需同改 `:64-67` + `:656-658`。一行可补：`BAR_CLOSE_UTC = time(0, 0)` 由 `_close_instant_utc` 消费。
- **[P3][0.95] DESIGN `:122` 句末标点** — ASCII `.` vs GATE `:198` `。`；`:122` 不在 R1–R4 范围。
- **[P3][0.90] README "~10 min grace"** — `:33` `:83` 用 "~"，`params.grace_min` 是精确 10；建议去 "~"。
- **[P3][0.90] 死分支仍在** — `_donchian_levels_for_confirm` `:759-766`：`d not in series` 时 `_day_median_close` 只可能返回 `missing`（`degraded` 必有值、必在 `series`），`:762-763` 不可达。无害。
- **已清（上次 §5 / RECHECK §6 项）**：DESIGN 自相矛盾（`not authorize` / `not being added` / `not part of this task` 零命中；`:4` Status、`:41` Implemented 一致）；history 两次 `write` → 单次（`:1029`）；`closed_at_local` 两分支格式（R6）。
- **沿用未清（状态不变，均不阻塞）**：`0600` 权限（`:1119-1123` `mkstemp` 无 `chmod`——brief 与写脚本若非同一 unix 用户会 `EACCES`，属 "文件缺失 ≠ 平静" 的另一形态，**部署到盒上首次运行后 `ls -l` 核一次**）；`SOURCE_KIND.get(name, "venue")` 缺省 venue（`:413` `:1050`）；`daily_cross_check[0]` 为活 bar 对比（JSON 09-21 `closed=false`）；`-o` + fail 注释残留（`:1179-1183`）；fail note "No agreeing pair" 措辞。
- **不立案（审过，无问题）**：grace 内 `position_basis` 仍为 `confirmed_close`（D−1 确为已确认 close，DESIGN `:106` "confirmed (or carried)"）；grace 内 `intraday_position` 以 D−1 轨位计算（GATE `:185` 永远 unconfirmed）；D-grace 组合（grace 内且 D−1 窗口缺日）→ fail 且 note 同时带两段（`:780-791` 拼接 `note_extra`）；`00:10:00Z` 边界确认（GATE `:101` `≤`）；探针 A 的 `slope: down` vs B 的 `flat`——窗口不同（08-30..09-18 vs 08-31..09-19）的自然结果，非重绘。

---

## 5. 对申请方主张的答复

| 主张 | 核验 | 结论 |
|---|---|---|
| R1–R4 已按 GATE 原文落 README + DESIGN | 反引号内容字节比对；字面 / 短语逐一命中（§1） | 属实 |
| R5 探针 A grace→degraded、B ok | 隔离目录复跑 `probe_grace_r5.py`，输出与提交件逐键相等；D−1 轨位独立重算一致 | 属实 |
| R6 单一常量、`+08:00` 两分支 | py `:64-67` `:647-678`；探针 C fail 分支 `+08:00`；`%z` 零命中 | 属实 |
| py 2.0.1 / JSON / history 一致 | 行 2 与 JSON 深度相等；三处 sha 重算一致 | 属实 |
| brief 仍未写通道行 | 材料无 brief 产物；`host = cursor` 两行 | 无反证；自本文起**允许**写（§3） |

---

## 6. 推翻条件与置信度

| 结论 | 置信度 | 会推翻它的证据 / 事件 |
|---|---|---|
| 总判 PASS | 0.88 | 下两行任一成立 |
| R6 齐 | 0.75 | 原则方裁定 "UTC 收盘时刻" 必须为命名常量并参与计算 → R6 回 REWORK，唯一整改：`BAR_CLOSE_UTC` 常量进 `_close_instant_utc`（一行）；其余 R1–R5、I1–I5 无需再审 |
| R3 齐 | 0.90 | 原则方要求 `:196` 该句以中文原文（"必含 … 直到真值到位"）出现而非英文等价句 → R3 回 REWORK，唯一整改为替换 README `:103` / DESIGN `:120` 一句 |
| I3 "同 commit" | 0.85 | PR diff 显示 README brief 节与 py 2.0.1 分属不同 commit 且中间 commit 已可被 brief 读到 → 按 RECHECK `:249` 处理 |
| 放行不附 shadow 门槛 | 0.80 | 原则方改裁 I6 为闸门 → 固定行推迟到盒上 history ≥14 UTC 日后；本文其余判定不变 |
| 不升 REFUSE | 0.95 | 发现任何 brief 已用 proxy 轨位产出 `system_signal` 且有人据此操作 → GATE `:293`，先撤 brief 行 |
| 数据层 I1 / I4 | 0.95 | 仅 PR diff 显示 `SCHEMA_VERSION = 2` 与 `trend_channel_proxy` 分属不同 commit 才推翻 "同 commit" |

---

## 7. 非目标（本次明确不做）

- 不实现、不修改 py / README / DESIGN / JSON / history / probes；不替 Jimmy 选 N；不做外部网络探针（离线函数探针除外）。
- 不裁 shadow 期长短（维持"建议不作闸门"）；不评估 DIF / 钝化 / 结构；不做 H/L Donchian、斜带、回测。
- 不做 HMAC / 签名 / 证书钉扎（维持 GATE §2.5 结论）。
- 不建立 brief routine、不写任何 brief 产物；不涉及下单、仓位或任何执行面。

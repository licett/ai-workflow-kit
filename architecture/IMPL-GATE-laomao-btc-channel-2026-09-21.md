REWORK

# IMPL-GATE：老猫 BTC「通道代理」实现闸（Conditional PASS → 实现 PASS|REWORK）

> 裁决：**REWORK**。数据层（RECHECK §5 I1 / I2 / I4）全部齐，且申请方样例数值经独立重算逐分一致；brief 规则层（I3）与 GATE §2.4 语义层（I5）各有未齐硬项，合计 6 条（§3 R1–R6）。**brief 继续不写任何通道行**；R1–R6 清齐后本闸改判 PASS，放行文案预告见 §4。
> 对照物：`architecture/RECHECK-laomao-btc-channel-data-2026-09-21.md`（PR [#5](https://github.com/licett/ai-workflow-kit/pull/5)，分支 `cursor/recheck-laomao-btc-channel-data-6c7a`，commit `42dd77c`，下称 RECHECK）；`architecture/GATE-laomao-btc-channel-data-2026-09-21.md`（PR [#4](https://github.com/licett/ai-workflow-kit/pull/4)，commit `3679f49`，下称 GATE）。uploads 内两份副本与分支文件逐字节一致（`diff -q`）。"GATE `:N`" / "RECHECK `:N`" 指对应 commit 内行号。
> 范围：只审 `uploads/` 五份实现材料——`DESIGN-channel-proxy-v0.md`（下称 DESIGN）、`README.md`、`btc_multisource.py`（下称 py）、`last_btc_consensus.json`（下称 JSON，`as_of 2026-09-21T02:24:47Z`）、`history/2026-09.jsonl`（1 行）。不改代码、不改 uploads；本文是本次唯一新增文件。
> 方法：文档 / 代码 / 数据对读；独立重算 Donchian 窗口与 `payload_sha256`；对 py 做**离线**函数探针——`import compute_trend_channel_proxy`，注入 JSON 内 `ohlc` 与固定 `now`，六个场景（A–F，见 §1 I5）。**无外部网络动作**。
> 验收标准：RECHECK §5 I1–I5（硬）原文（RECHECK `:214-218`），不改宽、不改窄。用户提交的 I1–I5 分组是对 RECHECK §5 的重排，§0 给出映射；凡用户分组未覆盖而 RECHECK §5 列为硬的（I5 GATE §2.4 语义、I2 README 同步），一律照审。
> 日期：2026-09-21。

---

## 0. 总判

| 用户项 | RECHECK §5 | 本次 | 一句话 |
|---|---|---|---|
| I1 `schema_version→2` 与 `trend_channel_proxy` 同 commit/同产物 | I1（A5） | **齐** | py `:39` 与 `:1029` 同文件；JSON `:2` 与 `:1700` 同产物；DESIGN `:127` 列为一处改动 |
| I2 Donchian-close N=20、排除确认 bar、不重绘、`params.n` 进输出 | I1（A4 输出层） | **齐** | 独立重算：确认 bar 09-20，窗 08-31..09-19（20 根，确认 bar 不在内），upper 81264.495 / lower 75584.635 / inside，与 JSON 逐分一致 |
| I3 不占顶层 `trend_channel`；`is_proxy` / `proxy_of` / `proxy_disclaimer` 常量齐全 | I1（A5） | **齐** | JSON 顶层 11 键无 `trend_channel`；py `:1078` 硬 pop；三常量与 GATE `:145-147` 逐字相同 |
| I4 brief 三规则 README/DESIGN 可见；prompt 模板路径缺失是否阻塞 | I3（A6） | **未齐（硬）** | 三条规则的"意思"在 README `:93-97` / DESIGN `:111-113`，GATE 原文不在：无 `:194` 全格式固定行、N 写死 20、无 `missing_inputs` 字面、无"确认落后"。路径缺失本身**不独立阻塞**（§2），阻塞的是内容 |
| I5/A9 `history/*.jsonl` + `payload_sha256` + `producer` 全落地 | I4（A9） | **齐** | py `:915-955`；JSON `:1754-1760`；history 1 行与 JSON 深度相等，sha 独立重算一致 |
| （用户未单列）GATE §2.4 语义 | I5（A3 A5） | **部分未齐（硬）** | `confirmed = closed ∧ grace` 齐（探针 F）；`bars_missing → null` 齐（探针 D）；grace 内不标 `degraded`（探针 A，GATE `:183`）；锚点为两处重复字面量非参数 |
| （用户未单列）README 同步 | I2（A5） | **齐** | README `:112-143` v2 shape；"comes later" 已去 |
| — shadow | I6（建议） | 未开始 | history 唯一一行 `producer.host = "cursor"`，非盒上产物；盒上 shadow 计时尚未开始 |

置信度：总判 REWORK 0.90；I3 未齐 0.95（文本直接可见）；I5-grace 未齐 0.85（GATE §2.2 `:101` 与 `:183` 自身有张力，§1 I5 说明）；I5-锚点 未齐 0.70（RECHECK `:51` 措辞两可，本文取"而非常量硬编码"字面，§7 给推翻条件）。

---

## 1. 逐项（按 RECHECK §5 编号）

格式：验收原文 → 证据（文件:行）→ 判定。

### I1 通道输出落地 — **齐**

验收（RECHECK `:214`）：实际 JSON `schema_version: 2`（py 同 commit 改）；`trend_channel_proxy` 含 DESIGN `:50-94` 全部字段；`params.n` 出现；不存在顶层 `trend_channel`；既有 v1 键全部不变。

| 证据 | 位置 | 内容 |
|---|---|---|
| `schema_version: 2` | py `:39` `SCHEMA_VERSION = 2`；`:1023` 进返回体；JSON `:2` | 与 `trend_channel_proxy`（py `:1016-1020` 计算、`:1029` 进返回体；JSON `:1700`）同文件、同产物。uploads 无 git 史，"同 commit" 以同产物为限，PR diff 时复核 |
| 字段完整 | JSON `:1700-1751` vs DESIGN `:50-94` | 脚本逐键对照：24 个顶层字段无缺项、无多项；子对象 `params{5}` `bar{2}` `close_confirmed{5}` `window{5}` 键集一致 |
| `params.n` | JSON `:1706` `"n": 20`；py `:58` `PROXY_N = 20` → `:884` | 出现在输出 |
| 无顶层 `trend_channel` | JSON 顶层键：`schema_version, as_of, sources, consensus, ohlc, ohlc_cross_check, trend_channel_proxy, status, note, producer, payload_sha256` | py `:1078` `result.pop("trend_channel", None)` 硬不变量；py 全文 `trend_channel` 字面仅出现于该行与 docstring |
| 三常量 | JSON `:1701-1703`；py `:52-56` | `is_proxy: true`、`proxy_of: "laomao_2.0_trend_channel"`、`proxy_disclaimer` 与 GATE `:145-147` 逐字相同；fail 骨架（py `:651-654`）同样带齐 |
| v1 键不变 | JSON | v1 八键 `schema_version, as_of, sources, consensus, ohlc, ohlc_cross_check, status, note` 全在；新增三键 `trend_channel_proxy, producer, payload_sha256`，纯新增。注：`ohlc[].candles` 由 5 根增至 40 根（py `:61` `PROXY_OHLC_LIMIT`，`:998`），键不变、长度变；README `:69` 已同步 "~40" |

**A4 输出层独立重算**（RECHECK §1 A4 `:98` 留到实现 PR 的那一项）：从 JSON `ohlc` 取四所 `closed=true` 的 candle → 逐日 median、剔 >0.5%（每日 kept=4，无 degraded / missing）→ 以 `as_of 02:24:47Z` + grace 10 min 选确认 bar = **2026-09-20**（收盘 `2026-09-21T00:00:00Z`，age 144.8 min）→ 窗 **2026-08-31..2026-09-19** 共 20 根，确认 bar 的 median close 81161.82 **不在窗内** → upper = **81264.495**（2026-09-03 median close）、lower = **75584.635**（2026-09-15）→ `ref_close` 81161.82 ∈ [lower, upper] → **inside**；OLS 斜率 **−0.067296 %/日** → 死区 0.1 内 → **flat**；`intraday_position` 以现货中位 81466.94 > upper → **above_upper**。以上全部与 JSON `:1736-1748` 逐分一致。

**不重绘**：结构性成立——窗只含 ≤T−1 的数据（py `:800-802`），函数无状态，每次运行落 history（I4）。源端回溯修订历史 candle 会移动逐日 median，属数据源事件而非算法重绘，靠 history 对账（§5 P3）。

判定：齐。

### I2 README 同步 — **齐**

验收（RECHECK `:215`）：README JSON shape 升 v2；"comes later" 句改写。

| 证据 | 位置 | 内容 |
|---|---|---|
| v2 shape | README `:112-143` | `schema_version: 2`（`:116`）、`trend_channel_proxy` 全字段（`:122-137`）、`producer` / `payload_sha256`（`:140-141`）、"No top-level `trend_channel` key"（`:145`） |
| "comes later" 已去 | README `:73` | 改为 `## trend_channel_proxy (schema_version 2)`；全文 `comes later` 零命中 |
| 其余同步 | README `:9` `:12`（文件表）、`:26`（原子写 + history）、`:30-31`（锚点）、`:33`（closed-only + grace）、`:77-89`（proxy 规则表）、`:105`（用法） | 与 py 行为一致 |

判定：齐。

### I3 brief 规则落位 — **未齐（硬）**

验收（RECHECK `:216`）：提供 brief prompt / 模板**路径**；其中可见 GATE `:194` 全格式固定行（`N={params.n}` 插值，不写死 20）、`:196` `system_signal` 禁令 + `missing_inputs` 含 `"trend_channel (LaoMao 2.0 original)"` 字面、`:197` 30 分钟阈值 + "确认落后"判定；与 I1 同 PR 同 commit。

| 子项 | GATE 原文 | README / DESIGN 现状 | 判定 |
|---|---|---|---|
| 固定行全格式 | `:193-194`：`通道[proxy · Donchian-close N={n} · 非2.0原版]：上轨 {upper} / 下轨 {lower}｜收盘确认 {bar_date} {closed_at_local}：{price_position}｜盘中 {intraday_position}（未确认）｜数据 {status}`；fail 时 `通道[proxy]：不可用（{note}）` | README `:93-95` "Fixed proxy line format" 只给标签 `proxy · Donchian-close · N=20 · 非 LaoMao 2.0 原版`；DESIGN `:111` 同；fail 只写 "print unavailability and no channel levels"，无格式 | ✗ |
| N 插值 | `:194` `N={n}`；`:105` N 变更是输出可见事件 | README `:94` / DESIGN `:111` 字面 `N=20` 写进 brief 文案 | ✗ |
| 禁 `system_signal` | `:196` | README `:96`、DESIGN `:112`；README `:110` 再述 | ✓ |
| `missing_inputs` 字面 | `:196` `missing_inputs` 必含 `"trend_channel (LaoMao 2.0 original)"` | README `:96` "Real LaoMao 2.0 `trend_channel` stays missing until supplied"——意思在、字面无；DESIGN `:112` 同 | ✗ |
| 30 分钟 | `:197` | README `:97`、DESIGN `:113` | ✓ |
| 确认落后 | `:197` `close_confirmed.bar_date` ≠ "今日 08:00 +08 之前最近一个已收盘 UTC 日" → 标"确认落后"；"文件缺失 ≠ 平静，陈旧 ≠ 当前" | 无。只有 "Stale data is not evidence of a quiet market"（陈旧 ≠ 平静的一半） | ✗ |
| 路径 | 提供 prompt / 模板路径 | 材料无独立 prompt / 模板；DESIGN `:115` `:135` "routine is not part of this task"；本仓库 `rg -i "laomao\|brief\|trend_channel\|system_signal"`（排除 `architecture/`）无相关命中 | 见 §2：**不独立阻塞** |

RECHECK §1 A6 `:136-139` 把前三处缺口逐条点名并写"实现 PR 落位时**必须**按 GATE 原文而非 DESIGN 缩写"；实现材料对这三处一字未动。

今天的样例正好说明这不是文字游戏：JSON `:1743` `price_position: "inside"`，同时 `:1745` `intraday_position: "above_upper"`——现货中位 81466.94 已在上轨 81264.495 之上 0.25%，是典型的"盘中已破、待 08:00 确认"状态。GATE `:194` 的 `盘中 {intraday_position}（未确认）` 槽位就是为它设计的；README 的标签式格式没有这个槽位，今天照 README 写 brief 的人要么漏掉盘中状态，要么自己编格式。`:194` 固定全格式的目的正在于此。

判定：未齐。整改项 §3 R1–R4。

### I4 A9 条件债 — **齐**

验收（RECHECK `:217`）：`history/YYYY-MM.jsonl` 每次运行追加一行；顶层 `producer {script, version, host, pid}`；`payload_sha256`（对去掉该字段后的规范化 JSON 计算）；README 说明。

| 证据 | 位置 | 内容 |
|---|---|---|
| history 追加 | py `:938-955` `append_history`；月份取 `as_of[:7]`（`:942-948`）；`main` `:1094-1099` 每次运行（含 fail）追加，失败只写 stderr 不阻断 | uploads `history/2026-09.jsonl` 恰 1 行，`as_of 2026-09-21T02:24:47Z`，与 JSON **深度相等**（同一次运行），行尾换行 |
| `producer` | py `:915-925` `make_producer` → `:1032`；JSON `:1754-1759` | `{script: "btc_multisource.py", version: "2.0.0", host: "cursor", pid: 3129070}` 四键齐 |
| `payload_sha256` | py `:928-935`：去 `payload_sha256` 后 `sort_keys=True, separators=(",",":"), ensure_ascii=False` 规范化 → sha256；`:1079` 在 pop `trend_channel` 之后、写文件之前计算 | 独立重算 `9bdcc3c9…f46e92` 与 JSON `:1760` 及 history 行一致 |
| README | `:12`（文件表）、`:26`（fail 也追加 history）、`:87`（A9 行）、`:140-141`（shape） | 齐 |

判定：齐。RECHECK §4-4 `:204` "A9 不得拆到后续 PR" 已满足。

说明（不影响判定）：`producer.host = "cursor"` 表明样例产物在 Cursor 云 VM 生成，不是 README `:19` 所指盒路径 `/home/box/agent-data/shared/council/laomao/data/`；这一行 history 因此不是盒上 shadow 记录（I6，§4）。

### I5 GATE §2.4 语义 — **部分未齐（硬）**

验收（RECHECK `:218`）四条。探针方法：`import` uploads 的 py，`compute_trend_channel_proxy(ohlc=JSON.ohlc, spot_median=81466.94, now=<注入>)`。

| 条 | 证据 | 判定 |
|---|---|---|
| `confirmed` = `closed` ∧ `now ≥ t_open + 86400 + grace_min`，不得直接用 `closed` | py `:729-731` 只收 `closed=true` 的 candle；`:753-763` 再以 `now >= ca + grace`（`ca` = D+1 00:00 UTC）选确认 bar。**探针 F**：`now = 2026-09-20T23:00Z`，09-20 bar 在 JSON 中 `closed=true`，仍**不**被确认，回到 09-19 | ✓ |
| `confirmed=false`（grace 内）→ 块 `status=degraded` 且沿用上一确认 bar（GATE `:183`） | **探针 A**：`now = 2026-09-21T00:05Z`（09-20 bar 收盘后 5 分钟，grace 内）→ 输出 `bar_date: 2026-09-19`、`confirmed: true`、`age_min: 1445.0`、`status: ok`、窗 08-30..09-18。"沿用"成立，但块**不标 degraded**，也没有任何字段表明 09-20 bar 正在等待确认。**探针 B**：`now = 00:15Z` → 09-20、`age_min 15`、ok，正确。唯一产出 `confirmed: false` 的分支是 py `:765-784`"没有任何已确认 bar"→ `status: fail`（**探针 C**：只留 09-20 一根 → fail），不是 `:183` 的 grace 情形 | ✗ |
| `bars_missing` 非空 → `upper/lower/price_position = null`，`status=fail`（GATE `:187`） | py `:831-841` → `_proxy_fail_skeleton`（`:684-691` 置 null）。**探针 D**：抽掉四所 09-10 → `fail`，三值 `null`，`bars_missing: ["2026-09-10"]`。**探针 E**：09-10 只留 bitstamp → `degraded`，`bars_degraded: ["2026-09-10"]`，`price_position: inside` | ✓ |
| 锚点参数化（RECHECK §1 A1 `:51`：作为参数 `bar.boundary_tz` / `bar.close_local` 而非常量硬编码） | 输出 `bar{}` 存在（JSON `:1712-1715`），但值是**两处重复的字面量**（py `:664-665` fail 骨架、`:891-892` ok 路径）；收盘时刻 D+1 00:00 UTC 写死在 `:759`；本地偏移 `"+08:00"` 字面拼接在 `:789`；fail 分支 `:779` 用 `%z` 得 `+0800`——两分支 `closed_at_local` 格式不一致（探针 C 输出 `2026-09-21T08:00:00+0800`，探针 B 输出 `…+08:00`）。计算与输出没有共同的单一来源 | ✗ |

关于 `:183` 的一点公允说明：GATE §2.2 `:101` 把"确认 bar"定义为"最新一根 `t_open + 86400 + grace ≤ now` 的 bar"，按此定义 grace 内的确认 bar 就是 D−1，实现严格遵守了这一条；而 `:183` 要求 grace 内 `confirmed=false` + `degraded`，隐含 `close_confirmed` 描述的是"最新已收盘 bar 及其是否已过 grace"。两处在 GATE 内部本就有张力。但 RECHECK I5 把 `:183` 明列为硬验收，本文不改宽；且 `:183` 的信号有实际价值——没有它，每天 00:00–00:10 UTC 这 10 分钟读者看到的是"ok + 24 小时前的确认"，而 brief 侧能兜底的"确认落后"规则（I3）目前也不存在，两层都无信号。

判定：部分未齐。整改项 §3 R5–R6。

### I6 shadow — 建议项，未开始

GATE `:261` / RECHECK `:219`：建议不作闸门，本文维持。事实：history 唯一一行 `host = "cursor"`，盒上尚无 v2 产物、无 shadow 记录。§4 说明。

---

## 2. 关于 prompt / 模板路径缺失是否阻塞（用户点名）

裁定：**不独立阻塞；阻塞的是内容，不是路径。**

1. 事实：材料与本仓库都没有 brief prompt / 模板；DESIGN `:115` `:135` 明说 brief routine 不在本任务。无 routine 就无 prompt 可放；要求"提供路径"等于要求本 PR 顺带创建 brief routine，超出数据模块范围。
2. RECHECK I3 "同 commit" 的目的（`:216` "字段先于规则出现即 fail-close 破口"；`:134` "控制点是实现 PR"）在当前架构下由三层承担：(a) 字段自带机器可查常量（JSON `:1701-1703`），下游想把 proxy 填进模板 `trend_channel` 槽必须写显式映射（GATE §2.4 命名铁律）；(b) README 与数据文件同目录，README `:99` "How 老猫 should use this" 就是读该文件的 agent 的操作说明——在没有独立 prompt 之前，**README §"Brief safety rules (mandatory)" 就是 prompt-of-record**；(c) 样例产物 `host = cursor`，盒上未见 v2 文件，当前敞口为零（待确认）。
3. 因此路径项按下述方式即满足：README 该节明写"本节为 brief 的 prompt-of-record；任何 brief routine 建立时必须逐字嵌入本节并回链"，并把 GATE `:193-197` 原文放进去（即 §3 R1–R4）。路径 = `README.md § Brief safety rules (mandatory)`。DESIGN A6 同步。
4. 何时升级为阻塞：若出现任何 brief 产物（prompt / 模板 / 输出）引用 `trend_channel_proxy` 而其 prompt 未含 `:193-197` 原文 → 按 RECHECK §7 `:249` "Conditional PASS 自动失效"处理；若已据此产出 `system_signal` → GATE `:293` 升 REFUSE，先撤 brief 行。

---

## 3. REWORK 清单（只列未齐硬项）

| # | 项 | 来源 | 现状（file:line） | 验收（可直接检查） |
|---|---|---|---|---|
| R1 | brief 固定行全格式 | I3 / GATE `:193-194` | README `:93-95`、DESIGN `:111` 只有标签 | README §Brief safety rules 与 DESIGN A6 出现 `:194` 两行原文（`ok\|degraded` 版与 `fail` 版），槽位齐：`{n}` `{upper}` `{lower}` `{bar_date}` `{closed_at_local}` `{price_position}` `{intraday_position}` `{status}` `{note}` |
| R2 | N 插值 | I3 / GATE `:194` `:105` | README `:94`、DESIGN `:111` `N=20` 字面 | brief 文案中 N 只以 `{n}` / `{params.n}` 出现；文档可另注"当前 `params.n = 20`"，但不得进入固定行模板 |
| R3 | `missing_inputs` 字面 | I3 / GATE `:196` | README `:96`、DESIGN `:112` 无字面 | 出现原文：`missing_inputs` 必含 `"trend_channel (LaoMao 2.0 original)"` 直到真值到位 |
| R4 | 确认落后 + 文件缺失 | I3 / GATE `:197` | README `:97`、DESIGN `:113` 只有 30 分钟 | 出现：`close_confirmed.bar_date` ≠ "今日 08:00 +08 之前最近一个已收盘 UTC 日" → 标"确认落后"；"文件缺失 ≠ 平静，陈旧 ≠ 当前" |
| R5 | grace 内 `degraded` | I5 / GATE `:183` | py `:753-784`：grace 内静默回退到 D−1，`confirmed: true`、`status: ok`（探针 A） | 以 `now=` 注入检验：`now ∈ [close(D), close(D) + grace_min)` 时 → `close_confirmed = {bar_date: D, closed_at_utc: close(D), confirmed: false, age_min < grace_min}`，`status = "degraded"`，`ref_close / upper / lower / mid / price_position / window` = 上一确认 bar D−1 的值（与上一次运行相同），`note` 点名 "in grace; carrying D−1"。grace 外行为不变（探针 B） |
| R6 | 锚点单一来源 | I5 / RECHECK `:51` | py `:664-665` 与 `:891-892` 重复字面；`:759` 写死 D+1 00:00 UTC；`:789` 拼接 `"+08:00"`；`:779` 用 `%z` 得 `+0800` | 一组模块级锚点常量（boundary tz、UTC 收盘时刻、本地标签 / 时区）同时驱动输出 `bar{}` 与 `:759` / `:789` 的计算；`closed_at_local` 两分支同为 `+08:00` 格式。**不要求**实现 GATE `:130` 路径 (ii)，不要求 CLI 开关 |

R1–R4 是同一处改动（README §Brief safety rules + DESIGN A6），R5–R6 在同一函数（`compute_trend_channel_proxy` / `_proxy_fail_skeleton`）。建议一个 PR 清完；提交时附探针 A / B / C 三个 `now` 值的输出即可核 R5。

同 PR 顺手（非闸门，见 §5 P2）：DESIGN `:40`（"does not authorize computation or output"）、`:44`（"**not** being added to `last_btc_consensus.json`"）、`:115`（"routine is not part of this task"）三句与 `:4` `:125-129` "implemented" 自相矛盾，改 A6 时一并改。

---

## 4. 转 PASS 时的放行文案（预告，本次不生效）

R1–R6 齐 → 本闸改判 PASS，放行文案为：

> 允许 brief 开始写固定代理行（GATE `:194` 全格式，N 从 `params.n` 插值，`fail` 时只写不可用行）；**仍禁**由 proxy 推出 `system_signal`，`missing_inputs` 必含 `"trend_channel (LaoMao 2.0 original)"`；新鲜度 30 分钟与"确认落后"两条门槛同步生效；`bars_degraded` 非空时点名日期（GATE `:198`）。

I6 shadow ≥14 UTC 日维持 GATE `:261` / RECHECK `:219` 的"建议不作闸门"。提醒两点：(a) 盒上 shadow 计时尚未开始——history 唯一一行来自 `host = cursor`；部署到盒上后每日运行，从首行盒上记录起算 14 个 UTC 日；(b) shadow 期的观察靶是 `history/*.jsonl` 中 `price_position` 翻转频率（RECHECK `:204`），今天的样例已给出第一个观察点：确认 inside、盘中 above_upper。

---

## 5. 新发现（本次新增，均不阻塞）

格式：`[Px][confidence] 标题 — 证据`。

- **[P2][0.90] DESIGN 自相矛盾** — `:40` `:44` `:115` 仍写"不授权 / 不加入 / 不属本任务"，`:4` `:125-129` 写"已实现"。设计锁与代码说两套话，读者不知以谁为准。归入 §3 顺手项。
- **[P3][0.85] `closed_at_local` 两分支格式不一致** — `:779` `%z` → `+0800`；`:789` 字面 → `+08:00`。brief 若按 ISO 8601 扩展格式解析会在 fail 分支断。归入 R6。
- **[P3][0.80] history 追加非单次 write** — `:951-952` 两次 `f.write`；并发运行可能交错半行。改为一次 `f.write(line + "\n")`。另：history 在两个 JSON 写完之后追加（`:1084-1096`），中途崩溃则少一行；可接受，记录。
- **[P3][0.90] `ohlc` 载荷 ×8** — candles 5 → 40（py `:61` `:998`），JSON 由约 440 行增至 1760 行。消费者读 `ohlc` 的成本上升；若嫌大可让 `ohlc[]` 只保留 cross-check 的 5 根、proxy 窗口另存，非本闸事项。
- **[P3][0.85] 单源日的"median"** — `_day_median_close` `:606-608` kept==1 时直接用该源值：单源无法剔 outlier，已由 `bars_degraded` 标记，符合 GATE `:209` "剩 1 → 该日记入 `bars_degraded`"；记录以免误读为"有 median"。
- **[P3][0.70] 源端 candle 回溯修订** — `series` 每次从当前抓取重算；若某所修订历史 candle，逐日 median 可能移动 → 轨位变。非算法重绘，靠 history 对账（A9 的价值所在）。待观察。
- **[P3][0.90] 死分支** — `:810-815` "Should not happen" 分支不可达（`_day_median_close` 返回 degraded 时 val 非 None，必在 `series`）。无害。
- **沿用 RECHECK §6 未清项（状态不变）**：`0600` 权限（`:1040-1044` 无 `chmod`）；`SOURCE_KIND.get(name, "venue")` 缺省 venue（`:408` `:971`）；`daily_cross_check[0]` 为活 bar 对比（JSON `:1644-1653` 09-21 `closed=false`）；`-o` + fail 注释残留（`:1088-1092`）；fail note 措辞。实现均未处理。
- **不立案（审过，无问题）**：`intraday_position` 在 spot `degraded` 时仍算（GATE `:185` 允许，永远 unconfirmed）；exit code 只看 spot `status`（README `:24` 明示）；OKX `confirm` 字段解析（`:283-284`；JSON 09-21 `closed=false`、09-20 `true`）；Kraken / Coinbase / Bitstamp 40 根 newest-first 归一化；`payload_sha256` 计算时点在 pop `trend_channel` 之后（`:1078-1079`）。

---

## 6. 对申请方主张样例的答复

| 主张 | 核验 | 结论 |
|---|---|---|
| N=20 | JSON `:1706`；py `:58` | 属实 |
| confirm 2026-09-20 | JSON `:1717`；独立按 `as_of 02:24:47Z` + grace 10 min 重算 | 属实（收盘 `2026-09-21T00:00:00Z`，age 144.8 min） |
| price_position=inside | 独立重算 81161.82 ∈ [75584.635, 81264.495] | 属实 |
| upper≈81264.5 | 独立 max(20 根) = 81264.495（2026-09-03 median close） | 属实 |
| lower≈75584.6 | 独立 min = 75584.635（2026-09-15） | 属实 |
| status=ok | 每日 kept=4，`bars_degraded` / `bars_missing` 空 | 属实 |
| brief 过闸前仍不写轨位 | 材料无 brief 产物；`producer.host = cursor` 表明样例非盒上产物 | **待确认**——无反证；若盒上 `last_btc_consensus.json` 仍为 v1，敞口为零。本闸 REWORK 期间**继续不写** |

---

## 7. 推翻条件与置信度

| 结论 | 置信度 | 会推翻它的证据 / 事件 |
|---|---|---|
| 总判 REWORK（而非 PASS） | 0.90 | R1–R4 的 GATE 原文已在某个未提交的 brief prompt 中 → 提供路径即 I3 齐；仍余 R5 R6，结论不变 |
| §2 路径不独立阻塞 | 0.80 | 原则方坚持 RECHECK `:216` 字面"提供 prompt / 模板路径"须为独立文件 → R1–R4 落到该文件，结论不变，只是落位不同 |
| R5 为硬 | 0.85 | 原则方裁定 GATE §2.2 `:101` 优先于 `:183`（grace 内确认 bar 即 D−1，无需 degraded）→ R5 降为 P3；但 R4 "确认落后"仍须落地以补信号 |
| R6 为硬 | 0.70 | 原则方裁定 RECHECK `:51` "参数"仅指输出 `bar{}` 字段 → R6 降为 P3，仍建议同 PR 顺手（两处字面重复 + 格式不一致是实际缺陷） |
| 不升 REFUSE | 0.95 | 发现任何 brief 已用 proxy 轨位产出 `system_signal` 且有人据此操作 → GATE `:293` |
| 数据层 I1 / I2 / I4 齐 | 0.95 | 只有 PR diff 显示 `SCHEMA_VERSION = 2` 与 `trend_channel_proxy` 分属不同 commit 才推翻 I1 "同 commit" |

---

## 8. 非目标（本次明确不做）

- 不实现、不修改 py / README / DESIGN / JSON / history；不替 Jimmy 选 N；不做外部网络探针（离线函数探针除外）。
- 不裁 shadow 期长短（维持"建议不作闸门"）；不评估 DIF / 钝化 / 结构；不做 H/L Donchian、斜带、回测。
- 不做 HMAC / 签名 / 证书钉扎（维持 GATE §2.5 结论）。
- 不涉及下单、仓位或任何执行面。

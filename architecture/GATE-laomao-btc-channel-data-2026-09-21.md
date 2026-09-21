REWORK

# GATE：老猫 BTC「多源现价 + 通道代理」数据方案（架构师裁决）

> 裁决：**REWORK**。方向可行、可逆、无执行面风险；但有 2 个 P0、3 个 P1 未清。**过审前禁止实现通道代理**（任何计算 `upper / lower / price_position` 的代码）。
> 范围：只审 `uploads/` 五份材料——`README.md`、`btc_multisource.py`、`laomao-trading-framework.md`、`framework-channel-excerpt.md`（= 框架 §6-§7 节选）、`last_btc_consensus.json`（`as_of 2026-09-21T00:42:58Z`）。不改代码、不写代码；本文是本次唯一新增文件。
> 依据：材料原文 + 一次只读探针（§1.2：对 OKX / Bitstamp 公共 K 线接口各 1 次 GET，2026-09-21 ≈01:55Z）。凡未从材料或探针证实的，标"待确认"。
> 日期：2026-09-21。行号均指 uploads 内文件。

---

## 0. 总判

| 点名项 | 裁决 | 一句话 |
|---|---|---|
| 共识规则 | **保留骨架，3 处整改**（P1×1 / P2×2） | median + 0.5% + ≥3 正确；但"≥3"不区分交易所与聚合器，"不信单一 feed"的承诺在退化场景下落空 |
| 通道代理公式 | **改：拒线性回归定轨，裁定 close-Donchian(N)** | 回归带每日重算会重绘历史轨位，与"收盘写死"语义冲突（P1，若坚持回归定轨则升 P0）；Donchian 不重绘、单参数、可审计 |
| UTC+8 收盘 | **改：锚点 = 08:00 Asia/Shanghai = 00:00 UTC；日线用 UTC 边界；OKX 换 `1Dutc`** | 现脚本把 OKX 16:00Z 开盘的 bar 贴上 UTC 日期标签与其他所 00:00Z 的 bar 对比——对齐的是标签不是窗口；JSON 里 2 天"OHLC divergence"全部由此产生（P0） |
| brief 字段契约 | **改：新增 `trend_channel_proxy`；不得占用模板 `trend_channel` 槽；`system_signal` 不得由 proxy 推出** | 字段级防混淆比文案级免责可靠 |
| HA / 防篡改 | **整改**（P1×1 / P2×3 / P3×3） | 传输层够用；缺的是输出文件的原子性、历史、新鲜度，与 feed 独立性分级；HMAC / 签名不做（YAGNI） |

置信度：总判 0.85；§2.3 时间锚点 0.8（依赖对"早八点"的解读，见 §6）；§2.2 公式选择 0.75。

**REWORK → PASS 放行条件**见 §5：清 2 个 P0 + 3 个 P1 即可转 PASS；P2 / P3 可随实现一并做或记债。

---

## 1. 事实核验

### 1.1 材料要点（只列裁决用到的）

| 来源 | 位置 | 事实 |
|---|---|---|
| README | `:42-45` | `ok` = ≥3 家在 median±0.5% 内；`degraded` = 恰 2 家；`fail` = <2 |
| README | `:46` | "OKX `1D` bars use **UTC+8** day boundaries (aligned in the script)" |
| README | `:10` | `last_btc_consensus.json` = "Last **successful** run output" |
| README | `:57-60` | 本模块**不**实现通道；"Do not invent channel levels from median spot alone" |
| 脚本 | `:29-30` | `TIMEOUT=8`、`OUTLIER_PCT=0.5` |
| 脚本 | `:199-220` | OKX `bar=1D`（`:201`）；`_ts_to_date(..., tz_offset_hours=8)`（`:213`） |
| 脚本 | `:188-196` | `_ts_to_date` 只返回 `YYYY-MM-DD` 字串，原始 ts 被丢弃 |
| 脚本 | `:410-437` | `cross_check_ohlc` 按 `date` 标签分组比 close |
| 脚本 | `:489-495` | 任何 `status`（含 `fail`）都覆盖输出文件；非原子写 |
| 框架 | `:20` | "以'收盘写死'为确认口径，多次提到**早八点收盘**，避免盘中插针误触发" |
| 框架 | `:26-34`、`:61-63`、`:96-100` | 趋势通道是 P0 开关；收盘写死突破上轨→满仓；收盘写死跌破下轨→清仓 |
| 框架 | `:173` | 不适合蒸馏："在缺少趋势通道、DIF、结构状态等输入时硬给建议" |
| 框架 | `:180-204`、`:208-222` | 决策模板：输入 `trend_channel{upper,lower,slope,price_position}`；输出 `system_signal`、`key_levels`、`missing_inputs` |

### 1.2 只读探针（本次唯一外部动作）

对三个公共接口各取最近 3 根日线，打印 bar 起始时刻（UTC）：

| 接口 | bar 起始（UTC） | 结论 |
|---|---|---|
| OKX `bar=1D` | `2026-09-20T16:00Z`、`09-19T16:00Z`、`09-18T16:00Z` | 边界 = 00:00 Asia/Shanghai，与 README 描述一致 |
| OKX `bar=1Dutc` | `2026-09-21T00:00Z`、`09-20T00:00Z`、`09-19T00:00Z` | **OKX 原生提供 UTC 边界日线**，脚本未使用 |
| Bitstamp `step=86400` | `2026-09-19T00:00Z`、`09-20T00:00Z`、`09-21T00:00Z` | UTC 边界（Kraken `interval=1440`、Coinbase `granularity=86400` 同为 UTC 桶，材料层面可从其时间戳推得，此处未逐一探针，标"待确认"但风险极低） |

对齐后的跨所日收差：OKX `1Dutc` 09-20 close `81179.6` vs Bitstamp 09-20 close `81151.65` → **0.034%**；09-19：`81265.8` vs `81235.14` → **0.038%**。这就是真实的 USDT–USD 日收基差量级。

### 1.3 从 `last_btc_consensus.json` 推出的事实

| 观察 | 数据 | 含义 |
|---|---|---|
| 两天 `ok:false` 全由 OKX 造成 | 09-19：OKX `81647.3` vs 其余 ≈`81230`（spread 0.518%）；09-17：OKX `76780.1` vs ≈`76352`（0.565%） | 同时刻现货 OKX 与 median 只差 `0.0197%`，说明差异不是 USDT 基差，而是 **8 小时窗口错位** |
| OKX 标签"09-21" bar 的 open = OKX 标签"09-20" bar 的 close = `80917.5`；Bitstamp 09-21 open `81151.64` | 两所"同一日期"bar 的 open 相差 0.29% | 两个 bar 不是同一个窗口 |
| Bitstamp 标签"09-21" close `81520.64` == Bitstamp 现货 `81520.64` | `as_of 00:42:58Z`，UTC 09-21 bar 才开 43 分钟 | 脚本返回的最新 bar 是**活 bar**；现有记录无法区分活 bar 与已收盘 bar |
| 现货 8 家全部一致，spread 0.165% | 6 家交易所 + 2 家聚合器 | 今天法定人数轻松满足；问题在退化场景（§2.1） |

结论：**现有 OHLC cross-check 正在产生篡改误报**；若通道代理直接沿用这条数据链，输入序列就是被 8 小时错位污染的 median close。这是 REWORK 的第一根据。

---

## 2. 逐项裁决

### 2.1 共识规则 —— 保留骨架，整改 3 处

**保留（不立案）**
- `median` 作中心、`>0.5%` 判 outlier、`≥3` 一致为 `ok`：BTC 主流所现货常态差 0.1–0.2%（本次 0.165%），0.5% 同时覆盖 USDT 基差与明显篡改，阈值合理。
- USD / USDT 混池：对**现货**共识可接受。USDT 脱锚（历史极值 ≈3%）时 USDT 簇会被整体判 outlier 而非拉偏 median（5 USD vs 3 USDT，median 落在 USD 簇），退化行为正确。
- 12 线程并行、8s 超时、失败不致命：对一次性 CLI 足够。

**整改**
1. **[P1] 法定人数不分交易所 / 聚合器**（F5）。`coinpaprika`、`yahoo`（BTC-USD 数据源为聚合器）、`coingecko` 是对交易所价格的再聚合，不是独立见证人。极端时 1 家交易所 + 2 家聚合器即可凑出 `ok`，而 README `:48` 承诺的是"不信任单一 feed"。裁决：`sources[].kind ∈ {venue, aggregator}`；`ok` 要求 **≥3 家一致的 `venue`**；聚合器只计入 `n_ok` / `agreeing`，不计入法定人数。今天 6 家 venue 健康，此规则零影响；它只在退化时生效——这正是防篡改规则该有的形状。
2. **[P2] README 与代码的状态规则不一致**（F8）。README `:44` 说 `degraded` = "恰 2 家一致"；代码 `:380-396` 回退分支在 `n_ok≥2` 且**全部**为 outlier 时也给 `degraded`（例：两家相差 1.2%）。两家互相矛盾不是"降级共识"，是"无共识"。裁决：该情形改 `fail`，README 同步。
3. **[P3] 死代码**（F10）。`:383-390` 的子分支要求 `spread_pct ≤ 0.5%`，而 spread ≤ 0.5% 蕴含每个价与 median 的偏差 ≤ 0.5%，即所有源都 agree、`n_agree = n_ok ≥ 2`，永远不会进入 `n_agree < 2` 的外层分支。删除。

### 2.2 通道代理公式 —— 拒线性回归定轨，裁定 close-Donchian(N)

老猫的判定语义（框架 `:61-63`、`:96-100`）是**事件**："收盘写死站上上轨 / 跌破下轨"。一旦某日收盘确认，该事件不可撤销。代理公式必须保住这一性质。

| 选项 | 轨位是否重绘 | 参数 | 与"收盘写死"兼容 | 跨所稳健性 | 判定 |
|---|---|---|---|---|---|
| A. 线性回归带（N 根 close 拟合 ± k·σ） | **是**：每日重拟合，历史 bar 的 upper/lower 都变；昨天"inside"可能今天变"below_lower"而价格未动 | N、k 两个，均无老猫方法依据 | **否** | 中 | **拒作定轨**；OLS 斜率可作 `slope` 标签 |
| B. Donchian on 跨所中位 **close**（前 N 根已收盘 bar 的最高 / 最低 close） | 否：bar T 的轨位只依赖 ≤T−1 的数据 | N 一个 | 是 | **高**（跨所日收差 ≈0.03%） | **裁定** |
| C. Donchian on 中位 high / low | 否 | N 一个 | 是 | 低—中（插针跨所差异远大于 close，且框架 `:20` 明言要避开插针） | 备选，不采 |
| D. 不做代理，等 Jimmy 给原版公式（README 现状） | — | — | — | — | 零 proxy 风险，但 brief 没有 P0 开关；本方案是有意识地放弃 D，条件是 §4 的标签纪律 |

**裁定公式（proxy）**

- 输入：对齐到 UTC 日线的各所 close（§2.3），逐日取 median，逐日按 0.5% 剔 outlier，逐日要求 ≥2 家（详见 §2.5-6）。记序列 \(C_t\)，只含**已收盘** bar。
- 确认 bar \(T\)：最新一根满足 \(t_{open} + 86400s + grace \le now\) 的 bar（`grace` 建议 5–10 分钟，防止所端刚过边界时返回未滚动的 bar）。
- \(upper_T = \max(C_{T-N},\dots,C_{T-1})\)，\(lower_T = \min(C_{T-N},\dots,C_{T-1})\)。**排除确认 bar 自身**，否则 close 永远 ≤ upper，"站上上轨"事件不可能发生。
- `price_position`：\(C_T > upper_T\) → `above_upper`；\(C_T < lower_T\) → `below_lower`；否则 `inside`。
- `slope`：只做标签。取 \(C_{T-N..T}\) 的 OLS 斜率归一化为 %/日，死区 ±0.1%/日内记 `flat`（死区值为参数，须出现在输出）。
- `N`：**不由本文裁定**，由 Jimmy 从 {20, 30, 55} 选定并写入 `params.n`；首次 shadow 运行默认 20。任何 N 的变更都是输出可见事件（字段变了），不是静默调参。

**取舍**：B 放弃了"轨是斜的"这一视觉相似性（Donchian 是阶梯状），换来不重绘、单参数、可审计三点；`slope` 标签补回方向信息。B 的下轨在急跌中滞后——这与老猫"宁愿假破磨损几个点"（框架 `:99`）的保守取向一致，可接受。B 只在创 N 日新高时触发 `above_upper`，慢牛中该事件比手绘通道稀疏——这是 proxy 偏差，写入 §4。

**推翻条件**：Jimmy 提供原版 2.0 通道定义（哪怕是"两点连线 + 平行"的人工规则）→ 立即以 `trend_channel`（真值）替换，`trend_channel_proxy` 保留 ≥14 个 UTC 日做 shadow 对比后删除。

### 2.3 UTC+8 收盘 —— 锚点 = 08:00 Asia/Shanghai = 00:00 UTC

拟议写的是 `close_confirmed(UTC+8)`。这个写法有两种读法，且现有脚本已经把二者混在一起：

| 读法 | 含义 | 日线边界 | 与材料的关系 |
|---|---|---|---|
| (i) 确认时刻按 UTC+8 **显示**，锚点是 **08:00 +08:00** | = 00:00 UTC | UTC 日线（Bitstamp / Kraken / Coinbase 原生；OKX 需 `1Dutc`） | 与框架 `:20`"早八点收盘"一致 |
| (ii) 用 UTC+8 **午夜**作为日线边界 | = 16:00 UTC | 只有 OKX 默认 `1D` 是这个边界 | 与"早八点"差 8 小时；与拟议"≥2 路对齐"的另外 3 路都不对齐 |

**裁决取 (i)**。理由：框架唯一的时间证据是"早八点收盘"；(i) 让 4 路 OHLC 源天然对齐；(ii) 要把三家 UTC 所用小时线重采样，成本高且引入新错误面。Asia/Shanghai 与 UTC 都无夏令时，锚点全年稳定。

**因此现有脚本的两处必须改**（F1）：
- `:201` `bar=1D` → `bar=1Dutc`；
- `:212-213` 删除 `tz_offset_hours=8` 标签平移（它做的是把 16:00Z 的 bar 改名为下一天，不是对齐窗口）；README `:46` 的"aligned in the script"同步改写。

**`close_confirmed` 的定义**（写入契约 §2.4）：不是布尔，是对象——确认 bar 的日期、UTC 收盘时刻、+08:00 本地时刻、是否已过 grace、距今分钟数。以 JSON 的 `as_of 2026-09-21T00:42:58Z` 为例：确认 bar = `2026-09-20`，`closed_at_utc = 2026-09-21T00:00:00Z`，`closed_at_local = 2026-09-21T08:00:00+08:00`，`age_min = 42`。而脚本目前标签为"2026-09-21"的 Bitstamp bar 是活 bar，OKX 标签"2026-09-21"的 bar 甚至到 16:00Z 才收——两者都**不得**进入通道输入。

**必须补的记录字段**（F4）：candle 记录保留 `ts_open_utc`（脚本 `:188-196` 目前只留日期字串），并派生 `closed: bool`。没有它，`close_confirmed` 无从计算，"排除活 bar"也无从执行。

**推翻条件**：Jimmy 从原始消息中确认老猫用的是北京时间 **零点**收盘 → 改取 (ii)，所有 UTC 所改用 1h 线重采样到 16:00Z 边界，本节 P0 变为 P1 实现债。请在 §5 A1 一行落字，两种读法不能并存。

### 2.4 brief 字段契约

**放在哪**：同一个 `last_btc_consensus.json`，**新增顶层键**，`schema_version` 从无 → `2`。
取舍：单文件 = 一次读、一份原子快照、一个新鲜度检查；代价是通道失败与现货混在一个 status 体系里（用独立的 `trend_channel_proxy.status` 解决）。备选"独立文件"带来两份新鲜度、两个竞态，现阶段不值。可逆。

**命名铁律**：顶层键叫 `trend_channel_proxy`，**不叫** `trend_channel`。框架模板 `:185-190` 的 `trend_channel` 槽保留给真值。下游 agent 想把 proxy 填进模板槽，必须写一步显式映射——这一步就是人工确认点。

**字段契约 v2（新增部分）**

```json
{
  "schema_version": 2,
  "trend_channel_proxy": {
    "is_proxy": true,
    "proxy_of": "laomao_2.0_trend_channel",
    "proxy_disclaimer": "Mechanical proxy (Donchian on cross-venue median close). NOT LaoMao 2.0 channel; levels and breakout dates will differ.",
    "method": "donchian_close",
    "params": { "n": 20, "outlier_pct": 0.5, "min_sources_per_day": 2, "grace_min": 10, "slope_deadzone_pct_per_day": 0.1 },
    "bar": { "boundary_tz": "UTC", "close_local": "08:00 Asia/Shanghai" },
    "close_confirmed": {
      "bar_date": "2026-09-20",
      "closed_at_utc": "2026-09-21T00:00:00Z",
      "closed_at_local": "2026-09-21T08:00:00+08:00",
      "confirmed": true,
      "age_min": 42
    },
    "sources_used": ["bitstamp", "coinbase", "kraken", "okx"],
    "window": { "start": "2026-08-31", "end": "2026-09-19", "bars": 20, "bars_degraded": [], "bars_missing": [] },
    "ref_close": 81151.7,
    "upper": 0.0,
    "lower": 0.0,
    "mid": 0.0,
    "width_pct": 0.0,
    "distance_to_upper_pct": 0.0,
    "distance_to_lower_pct": 0.0,
    "price_position": "above_upper|inside|below_lower",
    "position_basis": "confirmed_close",
    "intraday_position": "above_upper|inside|below_lower|null",
    "intraday_basis": "consensus.median (unconfirmed)",
    "slope": "up|flat|down",
    "slope_pct_per_day": 0.0,
    "status": "ok|degraded|fail",
    "note": "human-readable"
  }
}
```

| 字段 | 规则 |
|---|---|
| `is_proxy` / `proxy_of` / `proxy_disclaimer` | 常量，三者缺一即 schema 无效。机器可查，不靠 brief 文案 |
| `method` / `params` | 枚举 + 全部参数显式。改 N 就是改输出，不允许隐式 |
| `close_confirmed` | 对象，见 §2.3。`confirmed=false`（处于 grace 内）时整个块 `status=degraded` 且沿用上一确认 bar |
| `price_position` | **只能**由 `ref_close`（确认 bar 的 median close）算出。`position_basis` 常量 `confirmed_close` |
| `intraday_position` | 可选，由 `consensus.median` 算出，永远带 `unconfirmed`。给 brief 写"盘中已破、待 08:00 确认"用 |
| `window.bars_degraded` | 当天只剩 1 家有效源的日期列表；非空 → `status=degraded` |
| `window.bars_missing` | 当天 0 家有效源 → **不插值、不补**（README `:60` 精神），整块 `status=fail`，`upper/lower/price_position` 置 `null` |
| `status` | 独立于现货 `status`；两者任一非 `ok` 时 brief 措辞降级 |
| 兼容性 | 既有键全部不变（纯新增）；README `:62-74` JSON shape 同步 |

**brief（简报）侧契约**

1. **固定一行**（`status=ok|degraded` 时必出）：
   `通道[proxy · Donchian-close N={n} · 非2.0原版]：上轨 {upper} / 下轨 {lower}｜收盘确认 {bar_date} {closed_at_local}：{price_position}｜盘中 {intraday_position}（未确认）｜数据 {status}`
   `status=fail` 时改为：`通道[proxy]：不可用（{note}）`，不得出现任何轨位数字。
2. **禁止**由 proxy 推出框架模板的 `system_signal`（`full_position / cash / reduce_30_40` 等）。允许说"若按 proxy 通道，价格位于 X"；不允许说"2.0 系统触发满仓 / 清仓"。`missing_inputs` 必含 `"trend_channel (LaoMao 2.0 original)"` 直到真值到位。这是 §4 的 fail-close 规则，也是框架 `:173` 的直接推论。
3. **新鲜度**：brief 读文件时检查 `as_of` 距今；> 30 分钟 → 重跑或标"陈旧"；`close_confirmed.bar_date` 不等于"今日 08:00 +08 之前最近一个已收盘 UTC 日" → 标"确认落后"。文件缺失 ≠ 平静，陈旧 ≠ 当前。
4. 现货 `consensus.outliers` 非空时照旧点名；通道 `bars_degraded` 非空时点名日期。

### 2.5 HA / 防篡改

先说够用的：全部 HTTPS + 默认证书校验；不做证书钉扎、不换 UA（YAGNI）。缺的是下面这些。

1. **[P1] feed 独立性分级**（F5，同 §2.1-1）。防篡改的最小前提是"见证人独立"，聚合器不是独立见证人。
2. **[P2] 输出文件原子性 + last-good 语义**（F6）。`:489-495` 用 `open(..., "w")` 直写，且任何 status 都覆盖。共享盒上 brief 可能读到半截文件，或读到一个 `median: null` 的 `fail` 快照顶掉了 10 分钟前的好数据。裁决：tmp + `os.replace`；`status=fail` 只写 `last_run.json`，不覆盖 `last_btc_consensus.json`——这才是 README `:10`"Last successful run output"字面上承诺的行为。
3. **[P2] 历史留存 + 自校验**（F9）。追加 `history/YYYY-MM.jsonl`（每次运行一行）；输出加 `producer {script, version, host, pid}` 与 `payload_sha256`（对去掉该字段后的规范化 JSON 计算）。作用：被改过的"最新文件"可与历史对账；哈希挡的是误编辑与截断，**不**挡蓄意攻击。HMAC / 签名：不做——共享盒上密钥放哪本身是更大的问题，且当前没有"同盒其他 agent 是敌手"的威胁模型。若该模型成立，再立项。
4. **[P2] Yahoo 静默回退昨收**（F7）。`:124` `regularMarketPrice or previousClose`：Yahoo 偶发缺字段时，昨收会以"现价"身份进入 median。改为缺字段即该源 `ok=false`。
5. **[P3] 记录各源自带时间戳**（F11）。OKX `ts`、Bitstamp `timestamp`、Yahoo `regularMarketTime`、coinpaprika `last_updated` 都有；冻结的 feed（价格不变但仍返回 200）只有靠它才能在价格走开之前被发现。
6. **通道输入的逐日规则**（拟议"≥2 路"的落地）：每日对齐后取 median，剔 >0.5% 者；剩 ≥2 → 正常；剩 1 → 该日记入 `bars_degraded`；剩 0 → `bars_missing` → 整块 `fail`。close-only 使单所插针无法污染 20 天的轨位——这是 §2.2 选 B 的防篡改红利。现货用 ≥3、通道用 ≥2 的不对称：OHLC 池只有 4 家，且通道有 N 天数据冗余 + 逐日 cross-check，可接受，写明即可。
7. **[P3] 默认池噪声**（F12）。Binance（451）、Bybit（403）、CryptoCompare（401）在本盒确定不可达（README `:28-33`），每次仍占 3 个线程与 3 条 error。裁决：标 `expected_unavailable` 并默认跳过，保留 `--include-blocked` 开关；别删代码，换盒可能就通了。

---

## 3. Findings

格式：`[Px][confidence] 标题 — 证据`。`same root cause?` 按冰山法则注明。

- **[P0][0.90] F1 OKX 日线窗口错位被贴成 UTC 日期标签** — `btc_multisource.py:201`（`bar=1D`）、`:212-213`（`tz_offset_hours=8`）、`:413-416`（按 `date` 标签分组）；README `:46`
  影响：现在 = `ohlc_cross_check` 对正常日报"篡改"（JSON 09-19 / 09-17）；拟议通道 = 输入 median close 被 8 小时错位的 OKX 拉偏 0.3–0.6%，是 USDT 真实基差（0.03%）的 10 倍
  取舍：当初选 `1D`+平移是为了"日期能对上"；代价是窗口对不上
  建议：`1Dutc` + 删平移。探针已验证 OKX 提供该 bar。same root cause? **yes**——README `:46` 的描述与 §1.3 两天误报同源
- **[P0][0.80] F2 收盘锚点未落字，"UTC+8 收盘"两可** — 框架 `:20`；拟议文案
  影响：读法 (ii) 会让通道与老猫口径差 8 小时，并让"≥2 路对齐"只剩 OKX 一路
  建议：§5 A1 一行确认。裁决默认 (i)
- **[P1][0.85] F3 线性回归带重绘历史轨位** — 设计层，无 file:line；依据框架 `:61-63`、`:96-100`
  影响："收盘写死"事件可被次日重算撤销；brief 历史陈述前后矛盾
  建议：§2.2 选项 B。若坚持回归定轨，本条升 P0
- **[P1][0.85] F4 candle 记录丢弃时间戳、无收盘标记** — `btc_multisource.py:188-196`、`:213`、`:235`、`:261`、`:283`；JSON Bitstamp "09-21" close == 现货
  影响：无法判定活 bar；`close_confirmed` 无法计算
  建议：保留 `ts_open_utc`，派生 `closed`。same root cause? no（与 F1 独立）
- **[P1][0.80] F5 法定人数不分 venue / aggregator** — `btc_multisource.py:110-136`（coinpaprika / yahoo / coingecko）、`:374-376`；README `:48`
  影响：退化场景下 1 家交易所即可撑起 `ok`
  建议：`kind` 标签 + ≥3 venue 规则
- **[P2][0.90] F6 fail 覆盖 last-good，非原子写** — `btc_multisource.py:489-495`；README `:10`
  建议：tmp+replace；fail 写 `last_run.json`
- **[P2][0.85] F7 Yahoo 静默回退昨收** — `btc_multisource.py:124`
  建议：缺字段即失败
- **[P2][0.80] F8 README 状态规则与代码回退分支不一致** — README `:44` vs `btc_multisource.py:380-396`
  建议：两家全 outlier → `fail`；文档对齐
- **[P2][0.70] F9 无历史、无自校验、无 producer 戳** — 输出结构（README `:62-74`）
  建议：jsonl 历史 + sha256 + producer；HMAC 不做
- **[P3][0.95] F10 死代码** — `btc_multisource.py:383-390`
  证明：spread ≤ 0.5% ⇒ ∀源 |p−med|/med ≤ 0.5% ⇒ n_agree = n_ok ≥ 2 ⇒ 不进 `n_agree<2` 分支
- **[P3][0.80] F11 未记录各源自带时间戳** — `btc_multisource.py:59-166`
- **[P3][0.90] F12 已知不可达源仍在默认池** — `btc_multisource.py:170-183`；README `:28-33`

**不立案（审过，无问题）**：0.5% 阈值；现货 USD/USDT 混池；无证书钉扎；`TIMEOUT=8`；并行度 12；`spot_kraken` 取 `c[0]`；Bitstamp / Kraken / Coinbase 的 newest-first 归一化。

---

## 4. Truth / Proxy contract

| 项 | 内容 |
|---|---|
| truth source | 老猫 2.0 趋势通道。材料中**不存在**其定义（README `:60` 明言待 Jimmy 提供）；从框架 `:26-34` 只能推出它是带上下轨、按收盘确认的方向开关 |
| proxy source | `trend_channel_proxy`：close-Donchian(N) on 跨所中位 UTC 日收（§2.2） |
| gap / bias | (1) 机械 vs 主观平行通道：轨位、突破日期都会不同，且无法量化差多少（真值缺失）；(2) Donchian 上轨只在创 N 日新高时被突破，慢牛中 `above_upper` 事件稀疏；下轨滞后于急跌；(3) close-only 比 H/L 通道窄；(4) N 未经老猫方法校准，首次取值是占位 |
| fail-close rule | proxy **不得**产出 `system_signal`；`missing_inputs` 必含真值缺失项；顶层键带 `_proxy`；`status≠ok` 降级措辞；`bars_missing` 非空 → 不给轨位 |
| 何时替换 | Jimmy 给出原版定义 → 新增 `trend_channel`（真值）；proxy shadow ≥14 UTC 日后删除 |

**建议但不作闸门**：proxy 上线后先 shadow ≥14 个 UTC 日（只写文件与历史，不进 brief 固定行），用 `history/*.jsonl` 观察 `price_position` 翻转频率与老猫公开表态是否大体同向。这是 §2.2 这个"半可逆"决策应有的最低验证。

---

## 5. 整改清单与放行条件（REWORK → PASS）

| # | 项 | 对应 | 验收（可直接检查） | 闸门 |
|---|---|---|---|---|
| A1 | 收盘锚点落字 | F2 | 本文或 README 出现一行 `close_anchor: 08:00 Asia/Shanghai (= 00:00 UTC)`（或明确改为 `00:00 Asia/Shanghai`），署名 + 日期 | **硬** |
| A2 | OKX 对齐 | F1 | 设计 / 代码用 `bar=1Dutc`，无 `tz_offset_hours=8`；重跑后正常日 `daily_cross_check[*].ok` 全 `true`；README `:46` 改写 | **硬** |
| A3 | candle 带时间戳与收盘标记 | F4 | 每根 candle 有 `ts_open_utc`、`closed`；设计写明"活 bar 不进通道输入" | **硬** |
| A4 | 公式定稿 | F3 | 设计写明 close-Donchian(N)、排除确认 bar、不重绘性质；`params.n` 出现在输出；回归只用于 `slope` 或不用 | **硬** |
| A5 | 字段契约 v2 | §2.4 | `schema_version: 2`；`trend_channel_proxy` 含 §2.4 全部字段；**不存在**顶层 `trend_channel`；README JSON shape 同步 | **硬** |
| A6 | brief 三条规则 | §2.4 | brief 的 prompt / 模板中可见：固定行、禁 `system_signal`、新鲜度阈值 | **硬** |
| A7 | venue / aggregator 法定人数 | F5 | `sources[].kind`；`ok` ⇐ ≥3 一致 venue；README `:42-45` 同步 | **硬** |
| A8 | 原子写 + last-good | F6 | tmp+replace；`status=fail` 不覆盖主文件 | 条件 |
| A9 | 历史 + 自校验 | F9 | `history/*.jsonl`、`payload_sha256`、`producer` | 条件 |
| A10 | Yahoo 回退、状态规则、死代码、时间戳、噪声源 | F7 F8 F10 F11 F12 | 逐项改，README 对齐 | 债 |

- A1–A7 齐 → **PASS**，可实现通道代理。
- A1–A7 齐、A8/A9 未齐 → **Conditional PASS**，A8/A9 记 pitfalls 并在实现 PR 内一并完成。
- 任一硬项未齐 → 维持 REWORK。

**过审前允许先做的事**：F1（`1Dutc`）、F6、F7、F10、F12 是**现有现货模块**的 bugfix，与通道决策独立，且 F1 今天就在制造误报——可以、也应该作为独立 bugfix 先修，不算"实现通道代理"。
**过审前禁止的事**：任何产出 `upper / lower / price_position / slope` 的代码、任何往 brief 里写通道行的改动。

---

## 6. 推翻条件与置信度

| 结论 | 置信度 | 会推翻它的证据 |
|---|---|---|
| 总判 REWORK（而非 REFUSE） | 0.85 | 若发现 brief 已在用 proxy 轨位输出满仓 / 清仓建议且有人据此下单——升 REFUSE，先撤 brief 行 |
| 总判 REWORK（而非 PASS） | 0.90 | F1 是数据层面可复现的错位，F2 是未落字的口径；二者任一未清都不能放行 |
| §2.3 锚点 = 08:00 +08 = 00:00Z | 0.80 | 原始消息中老猫明确以北京时间零点为收盘；或 Jimmy 指出"早八点"另有所指 |
| §2.2 选 Donchian-close 而非回归 | 0.75 | Jimmy 提供的原版定义本身就是斜带（如回归 / 平行趋势线）且接受重绘——那时 proxy 也应改斜带，但需另立"重绘处理规则" |
| §2.4 单文件 + `_proxy` 命名 | 0.80 | 现货与通道的运行节奏分离（例如通道只在 08:10 +08 算一次、现货每 5 分钟一次）→ 拆文件 |
| §2.5 不做 HMAC | 0.70 | 共享盒上出现非本脚本对该文件的写入记录 |

---

## 7. 非目标（本次明确不裁、不做）

- 不实现、不试算任何通道数值；不选定 N。
- 不评估 DIF / 钝化 / 结构（框架 P1 层），不做多周期。
- 不做 H/L 版 Donchian、不做斜带；不做回测选参。
- 不做 HMAC / 签名 / 证书钉扎。
- 不改现货 0.5% 阈值与 USD/USDT 混池策略。
- 不涉及下单、仓位或任何执行面；proxy 输出永远是给人看的输入，不是给系统执行的信号。

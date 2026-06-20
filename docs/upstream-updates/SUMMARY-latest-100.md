# upstream 更新摘要 (ZhuLinsen/daily_stock_analysis)

> 抓取时间：2026-06-13 08:17 GMT+8
> 本地 HEAD：`e87e409` (fix: restore missing modules required by main.py entry)
> upstream HEAD：`4b3f679` (feat: adapt AlphaSift hotspot topics)
> **落后 upstream：759 个 commit**
> 覆盖范围：最近 ~100 个 commit（约 2 周内，2026-06-01 ~ 2026-06-12）

---

## 📊 总体节奏

| 指标 | 数值 |
|------|------|
| 时间跨度 | 2026-06-01 ~ 2026-06-12 (12 天) |
| Commit 数量 | 100+ |
| 涉及 PR | #1540 ~ #1666 |
| 主要贡献者 | mumu, Alfred, LouisHong, ZhuLinsen, 123kaze, Octopus, volcanoAlbert, fzxiong, Sunflower, Amorend, zbl-96, Delicious233 |
| 文件分布 | apps(260) / docs(144) / tests(111) / src(92) / api(47) |
| **发布版本** | **v3.20.0** (06-03) → **v3.21.0** (06-07) |

---

## 🎯 核心主题（按重要性排序）

### 1️⃣ AlphaSift 选股引擎集成（重点中的重点）
- `0ca4e07` **integrate AlphaSift with DSA runtime enrichment** (mumu, 06-05) — AlphaSift 接入主流程
- `4b3f679` **adapt AlphaSift hotspot topics** (mumu, 06-12) — 热点话题适配
- `12a7e6d` **make AlphaSift screening recoverable** (mumu, 06-07) — 选股可恢复性
- `e2fe6e3` **verify packaged AlphaSift adapter at runtime** (mumu, 06-08) — 运行时校验
- `81e9ca8` alphasift-可用性检测不应静默吞掉非预期异常 (mumu, 06-01)
- `1d8a043` **自动安装 AlphaSift 并收敛选股开关** (mumu, 06-03)
- `649413c` pass SearXNG Actions variables to daily workflow (mumu, 06-04)

> 🐼 **点评**：AlphaSift 是上游力推的新选股能力，6 个 commit 都在解决"接入+稳定+运行时验证"，目前处于"可用了但还在打磨"阶段。

---

### 2️⃣ Run-Flow 链路追踪系统（issue #1652 系列，全新能力）
- `fa9d9b0` **add run-flow snapshot contract and APIs** (LouisHong, 06-10) — 跑批快照契约与 API
- `f7ac00b` **add web run-flow viewer** (LouisHong, 06-11) — Web 端可视化
- `efa41e0` **add live run-flow diagnostics** (LouisHong, 06-12) — 实时诊断

> 🐼 **点评**：把"一次分析跑了什么、卡在哪步、用了什么数据"完整记录下来，并在 Web 上能看到。对于调试 agent 卡死/超时非常有用。**这是上游这阶段最值得跟的新能力**。

---

### 3️⃣ DecisionSignal 持久化与契约（issue #1390 P0/P1）
- `ad15ebc` **新增 DecisionSignal 持久化 API** (Alfred, 06-10) — 决策信号落库
- `ff6494b` **新增建议动作 taxonomy 字段边界 P0** (Alfred, 06-08) — 字段强约束
- `4082c0d` **补充 #1390 P1 DecisionSignal 前端契约与隔离测试** (Alfred, 06-11) — 前后端契约

> 🐼 **点评**：把"建议动作"做成强类型字段（buy/hold/sell/observe 等），不是 LLM 自由发挥。前端、后端、DB 三方对齐，引入契约测试。

---

### 4️⃣ 大盘复盘 / Market Phase 系统
- `8df69fe` **完善大盘复盘历史聚合、查看与删除能力** (mumu, 06-04) — 历史复盘 CRUD
- `b612fb2` **结构化大盘复盘报告展示** (mumu, 06-04)
- `44ea049` **add web market phase labels** (Alfred, 06-03) — Web 阶段标签
- `7e54c6c` **add analysis phase API plumbing** (Alfred, 06-03) — Phase API 管道
- `9b76f8d` **联动告警、持仓和历史阶段摘要** (Alfred, 06-04) — #1386 P6
- `e6302a0` add #1386 P7 market-phase guide (Alfred, 06-04)
- `3ea007c` **盘中决策护栏与 phase_decision 质量校验 P5** (Alfred, 06-02)
- `3e08589` add phase data quality prompt guards (Alfred, 06-01)
- `3153c76` 收敛多股通知摘要的市场状态展示 (mumu, 06-05)
- `6784409` docs: harden PR quality guardrails (Alfred, 06-04)
- `e6302a0` docs: add #1386 P7 market-phase guide (Alfred, 06-04)
- `e6302a0` docs: add #1386 P7 market-phase guide (Alfred, 06-04)
- `2f26042` 报告页运行诊断与输入数据块状态口径不一致 (mumu, 06-05)
- `6784409` docs: harden PR quality guardrails (Alfred, 06-04)

> 🐼 **点评**：这是上游另一个主线方向 — "市场阶段识别"从 LLM 自由文本 → 强类型 Phase API → 前端展示 → 历史聚合，完整链路。

---

### 5️⃣ Web UI 体验改进
- `d704fe3` **add Web UI language switch** (mumu, 06-06) — **多语言切换**
- `513271b` **fix(issue-1626): 英文界面仍残留中文文案** (mumu, 06-07) — i18n 修复
- `f091810` 优化侧边栏选中态样式、扩展宽度并新增 rail 紧凑模式 (Sunflower, 06-04)
- `813b5d6` fix: prevent stock card phase label overlap (Alfred, 06-05)
- `f587459` **持仓管理页面添加账户删除功能** (volcanoAlbert, 06-10) — 账户归档
- `81c0287` 新增个股栏与自选队列操作 (zbl-96, 06-02) — 自选股面板

---

### 6️⃣ Agent / 问股 改进
- `da274f7` **锁定问股追问的当前标的上下文 P2** (Alfred, 06-10) — 追问不再"跳股票"
- `71055c4` **问股自由文本金融缩写不再误识别为股票代码** (Alfred, 06-05) — 缩写歧义
- `14d666b` fix: avoid agent daily bars missing false positive (mumu, 06-03)

---

### 7️⃣ 通知 / 部署 / 健壮性
- `3471afb` **add Feishu App Bot notification sender with P2P and group support** (Delicious233, 06-05) — 飞书 P2P + 群机器人
- `39f24df` **代码健康修复：稳定测试、健康检查、错误响应与 schema 版本记录** (fzxiong, 06-05)
- `93c1128` **register health router in v1 API so /api/v1/health returns 200** (Amorend, 06-03) — 健康检查修复
- `d8a067b` **improve first-run configuration validation** (123kaze, 06-02) — 首次运行校验
- `5cd968b` fix: improve Windows first-run encoding compatibility (mumu, 06-03)
- `d6234cd` fix: clarify Docker env runtime config (mumu, 06-04)
- `c6221ba` fix: avoid quoting desktop updater install directory (mumu, 06-04)
- `8909168` fix: run manual market review on non-trading days (mumu, 06-07)
- `617b11d` fix: restore market review in stock bar (mumu, 06-06)
- `1e94490` fix: widen analytical intel search lookback (mumu, 06-06)
- `4f53602` fix: clarify runtime logging context (LouisHong, 06-09)

---

### 8️⃣ 杂项 / 文档 / 工程
- `40c5c75` **chore: prepare v3.21.0 release** (zhulinsen, 06-07) — 发布准备
- `d22ff1c` **chore: prepare v3.20.0 release** (ZhuLinsen, 06-03)
- `52558a9` **upgrade MiniMax default model to M3** (Octopus, 06-03) — ⚠️ 默认模型升 M3
- `649f775` chore: remove one-off PR screenshot assets (mumu, 06-06)
- `8a77960` docs: require screenshots for visual PR changes (mumu, 06-05)
- `6784409` docs: harden PR quality guardrails (Alfred, 06-04)
- `e6302a0` docs: add #1386 P7 market-phase guide (Alfred, 06-04)
- `6784409` docs: harden PR quality guardrails (Alfred, 06-04)
- `6784409` docs: harden PR quality guardrails (Alfred, 06-04)

---

## 🔥 跟我们（你的本地项目）强相关的更新

| 优先级 | 能力 | 你的场景 | 是否建议合入 |
|------|------|---------|-----------|
| ⭐⭐⭐ | **Run-Flow 诊断 + Web viewer** (#1652) | 调试 AI 分析卡死、超时、token 爆 | ✅ 强烈建议 |
| ⭐⭐⭐ | **Feishu App Bot 推送** (#1553) | 你现在用的是 webhook 推送，新版支持 P2P+群机器人 | ✅ 建议 |
| ⭐⭐⭐ | **Web UI 中英文切换** (#1621) | 提升体验 | ✅ 建议 |
| ⭐⭐ | **决策动作 taxonomy** (#1631) | "buy/hold/sell" 强类型，不再瞎写 | ✅ 建议 |
| ⭐⭐ | **大盘复盘历史聚合** (#1580) | 复盘能力完整化 | 看需求 |
| ⭐⭐ | **持仓账户归档** (#1647) | 多账户管理 | 看需求 |
| ⭐⭐ | **#1386 市场阶段识别** | 从 LLM 自由文本 → 强类型 Phase | 可选 |
| ⭐ | AlphaSift 选股 | 跟咱们 `stock_selector.py` 思路不同，新引擎 | 等稳定再合 |
| ⚠️ | **M2.7-highspeed → M3 默认模型** | 跟你 `MiniMax-M2.7-highspeed` 配置冲突 | **需手动决定** |
| ⚠️ | 760 commit 落后 | 风险高，合并冲突可能多 | **分批合入** |

---

## 📈 风险提示

1. **落后 759 个 commit**，跨度至少 1-2 个月，**一次性 merge 几乎必冲突**
2. **AlphaSift 是新外部依赖**（需要 SearXNG），合入时需要重新配置
3. **v3.21.0 升 M3 默认模型** — 跟你现有 `MiniMax-M2.7-highspeed` 直接冲突
4. **apps/ 目录 260 个文件改动** — 前端重构可能影响你当前 UI
5. **API schema 版本变更** — 上游有专门的 schema 版本记录，可能影响你的飞书推送

---

## 💡 推荐操作

```bash
# 1. 备份当前（已经修改过的 notification.py 等）
cd /home/panda/project/daily_stock_analysis-main
cp src/notification.py /tmp/notification.py.backup

# 2. 拉一个分支试合
git checkout -b sync/upstream-v3.21.0
git merge upstream/main --no-ff

# 3. 处理冲突后跑测试
source venv/bin/activate
pytest tests/ -x

# 4. 验证服务
nohup python server.py > logs/server.log 2>&1 &
```

**我的建议：分批合** — 这次先只合 `Run-Flow` + `Feishu App Bot` + `i18n` 三个高价值低风险能力，其他等稳定再说。要我现在就拉分支试合并吗？

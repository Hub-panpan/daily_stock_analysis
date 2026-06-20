# Hub-panpan/daily_stock_analysis Fork 更新摘要

> 抓取时间：2026-06-13 08:21 GMT+8
> 本地 HEAD：`e87e409` (fix: restore missing modules required by main.py entry)
> fork HEAD：`1f6cf77` (Merge remote-tracking branch 'upstream/main')
> **落后 fork：719 个 commit**
> 时间跨度：2026-05-10 ~ 2026-05-29（19 天）
> 涉及 PR 范围：#1199 ~ #1505（307 个 PR）

> ⚠️ 重要：我一开始 fetch 错了，去看了 upstream 主仓，结论"落后 759 commit"不准确。
> 实际你 fork 的同步节奏很稳，**5/29 还主动 merge 了 upstream**，是真·活 fork。

---

## 📊 总体节奏

| 指标 | 数值 |
|------|------|
| 时间跨度 | 2026-05-10 ~ 2026-05-29 (19 天) |
| Commit 数量 | 100+ |
| 涉及 PR | 307 个（#1199 ~ #1505） |
| 文件分布 | docs(274) / tests(186) / src(165) / apps(146) / api(29) / data_provider(26) |
| **发布版本** | **v3.17.0** (05-16) → **v3.18.0** (05-21) |
| **Panda 自己提交的 commit** | **7 个**（merge + 本地定制恢复） |

---

## 🐼 Panda (你) 自己提交的 7 个 commit

| Commit | 日期 | 说明 |
|--------|------|------|
| `1f6cf77` | 2026-05-29 | Merge remote-tracking branch 'upstream/main' |
| `01021d6` | 2026-05-24 | **fix: 支持飞书 APP_ID+SECRET 方式的通知渠道检查** |
| `bd0146f` | 2026-05-24 | **feat: 音量柱关键K线策略配置文件** |
| `3a02de3` | 2026-05-24 | Merge remote-tracking branch 'upstream/main' |
| `e252fc7` | 2026-05-23 | Merge remote-tracking branch 'upstream/main' |
| `c495842` | 2026-05-18 | **Restore local Feishu push customizations (feishu_user_open_id + API mode support)** |
| `3794b2c` | 2026-05-18 | **Merge upstream/main v3.17→v3.18 (7 commits)** |
| `ea09978` | 2026-05-17 | **Restore local customizations after upstream v3.17 merge** |
| `9b3e2f1` | 2026-05-17 | **Merge upstream/main v3.16→v3.17 (39 commits) + resolve conflicts using upstream** |

> 🐼 **点评**：你 fork 的工作流非常清晰 — **merge upstream → restore 本地定制**，本地定制主要是：
> 1. 飞书推送（APP_ID+SECRET + OpenID 模式）
> 2. 音量柱关键K线策略配置
>
> 这是非常标准的 fork 维护模式，**强烈建议沿用**。

---

## 🎯 核心主题（按重要性排序）

### 1️⃣ 告警中心 / Alert Center（最大主线，5 阶段铺开）

| PR | 阶段 | 内容 | 日期 |
|----|------|------|------|
| #1301 | **P0** | docs: add alert center P0 baseline contracts | 05-15 |
| #1314 | **P1** | feat: 新增告警 API MVP | 05-16 |
| #1323 | **P2** | feat: 增加 P2 告警评估 Worker | 05-17 |
| #1334 | **P3** | feat: 新增 Web 告警中心 MVP | 05-18 |
| #1337 | **P4** | feat: 记录告警通知结果与持久化冷却 | 05-18 |
| #1345 | **P5** | feat: 告警中心支持 MA/RSI/MACD/KDJ/CCI 日线技术指标规则 | 05-19 |
| #1379 | **P6** | feat: add P6 portfolio and watchlist alerts | 05-21 |
| #1419 | **P7** | feat: add P7 market light alerts | 05-23 |
| #1430 | **P8** | docs: complete alert center P8 documentation | 05-23 |

> 🐼 **点评**：19 天里把告警中心从 0 做到 P8 收官，是这一轮**最完整的功能**。能力：技术指标触发 / 组合告警 / 自选股告警 / 大盘灯 / 通知冷却去重。**强建议合入**。

---

### 2️⃣ Run Diagnostics 链路追踪（issue #1391，4 阶段）

| PR | 阶段 | 内容 |
|----|------|------|
| #1435 | **Phase 0** | fix: add #1391 Phase 0 diagnostics and A-share code guards |
| #1441 | **Phase 1** | feat: add #1391 Phase 1 run diagnostics trace plumbing |
| #1444 | **Phase 2** | feat: add #1391 Phase 2 run diagnostic summaries |
| #1445 | **Phase 3** | feat: add #1391 Phase 3 web diagnostic summaries |

> 🐼 **点评**：跟 6 月份 upstream 新加的 "Run-Flow Viewer" (#1652) 是同一思路的早期版本，**5 月版已合入你 fork**。

---

### 3️⃣ Analysis Context Pack（4 阶段铺开）

| PR | 阶段 | 内容 |
|----|------|------|
| #1433 | P0 | docs: inventory analysis context boundaries |
| #1449 | P1 | feat: add analysis context pack schema |
| #1478 | P2 | feat: add AnalysisContextPack P2 assembler from pipeline artifacts |
| #1491 | P3 | feat: 接入 AnalysisContextPack 低敏 Prompt 摘要 |

> 🐼 **点评**：把"AI 分析时需要喂的上下文"做成 pack，低敏版本（不泄露原始数据），**优化 token 消耗**。

---

### 4️⃣ Market Phase / 大盘阶段 推进

| PR | 内容 |
|----|------|
| #1424 | feat: add market phase inference baseline |
| #1434 | feat: add runtime market phase context plumbing |
| #1442 | feat: inject market phase prompt context |
| #1295 | feat: Configure market review index colors |
| #1278 | feat: add market review data sources |
| #1306 | fix: 大盘分析的历史执行记录丢失 |

---

### 5️⃣ 通知系统升级

| PR | 内容 | 评价 |
|----|------|------|
| #1271 | feat: 支持 ntfy 一等通知渠道（P6-A） | 新渠道 ntfy |
| #1260 | feat: 添加 P4 通知降噪机制 (Refs #1200) | 防轰炸 |
| #1269 | fix: isolate aggregate notification failures | 容错 |
| #1275 | feat: complete p6 notification channel cleanup | 收尾 |
| #1276 | docs: close notification issue 1200 | 文档 |
| #1505 | **chore: extract analysis artifacts helpers** | 🆕 抽取助手 |

---

### 6️⃣ 数据源扩展（多市场）

| PR | 内容 |
|----|------|
| #1313 | **feat: add Finnhub & AlphaVantage US market data source adapters** |
| #1249 | fix(data-provider): skip unavailable optional fetchers and back off longbridge reconnects |
| #1465 | fix: 为 Akshare 历史兜底接口增加超时保护 |
| #1409 | fix: normalize Tencent realtime volume |
| #1349 | fix: prefer realtime quote for current portfolio snapshots |
| #1367 | fix: 资金流数据缺失 |

> 🐼 **点评**：**美股数据源**（Finnhub + AlphaVantage）正式加入，**这对你有美股配置是利好**。

---

### 7️⃣ LLM / 模型相关

| PR | 内容 |
|----|------|
| #1317 | fix: 增强 LLM 参数适配层 |
| #1284 | fix analyzer content block responses |
| #1350 | Refactor: isolate MiMo fallback pricing hook and complete #1282 fix |
| #1294 | feat: Add report LLM model visibility toggle |

---

### 8️⃣ 桌面端 / 部署

| PR | 内容 |
|----|------|
| #1256 | feat: add desktop auto-update install flow |
| #1320 | fix: unify desktop updater artifacts |
| #1321 | fix: prevent desktop WebUI stale cache |
| #1387 | fix: macOS 桌面端打包缺失 strategies 目录 |
| #1415 | fix: 修复桌面端自动更新静默安装 |
| #1432 | fix: preserve macOS desktop runtime config |
| #1262 | fix(issue-1261): [bug]-docker-部署启动失败 |
| #1263 | fix: auto repair Docker mount permissions |
| #1401 | fix(issue-1399): [bug]-docker-挂载-.env-文件时-os.replace()-更新 |
| #1586 | fix: clarify Docker env runtime config |

---

### 9️⃣ 文档 / 工程 改进

| PR | 内容 |
|----|------|
| #1199 | expand settings help coverage for core config |
| #1287 | fix: 为设置页的通知与 Agent 设置区域增加运行时错误兜底 |
| #1308 | docs: 规范 PR title 指引 |
| #1333 | docs: add beginner client setup guide |
| #1410 | chore: split web route bundles |
| #1418 | chore: stabilize web vendor chunks |
| #1402 | chore: clean pydantic v2 schema warnings |
| #1425 | chore: lazy load report markdown drawer #1411 PR-2 |
| #1450 | feat: 补齐 Web 设置页实际展示字段帮助信息 |
| #1453 | fix: 补齐 Web 设置页中文文案映射并本地下拉选项翻译 |
| #1460 | feat: add visible chat context compression |
| #1461 | fix: 修复问股和首页进行中状态残留 |
| #1473 | fix: 问股 single-agent 增加 provider-aware trace |
| #1480 | fix: 支持股票自动补全索引远程刷新 |
| #1488 | chore(.gitattributes): 完善Git属性配置规范换行符与二进制文件处理（docker 部署报错修复） |
| #1489 | fix: invalid unit abbreviation: T |

---

### 🔟 选股策略 / 量化

| PR | 内容 |
|----|------|
| #1331 | feat: Web 个股分析支持选择策略 |
| #1332 | feat: add mainstream analysis strategy skills |
| #1388 | feat(issue-1384): [feature]-建议个股分析界面略作调整 |
| #1369 | feat: 邮件报告补充 财务摘要 / 股东回报 / 关联板块，并接入 HK/US 基本面 |

---

### 1️⃣1️⃣ 技术指标修复

| PR | 内容 |
|----|------|
| #1358 | fix: align RSI with Wilder EMA |
| #1264 | fix: normalize report strategy price fields |
| #1289 | fix missing capital flow buy guard |
| #1288 | [codex] fix fundamental timeout defaults |
| #1351 | fix: clear AlphaVantage fetcher index name to avoid 'date' ambiguity |

---

## 🔥 跟我们强相关的更新（按优先级）

| 优先级 | 能力 | 你的场景 | 建议 |
|------|------|---------|------|
| ⭐⭐⭐ | **告警中心 P0-P8** | 全套技术指标 / 组合 / 自选股 / 大盘告警 | ✅ 必合 |
| ⭐⭐⭐ | **美股数据源 (Finnhub + AlphaVantage)** | 你有美股配置 | ✅ 建议合 |
| ⭐⭐⭐ | **Analysis Context Pack** | 减少 token 消耗、提升 AI 质量 | ✅ 建议合 |
| ⭐⭐⭐ | **Run Diagnostics P0-P3** | 调试 AI 链路 | ✅ 已合 fork |
| ⭐⭐ | **桌面端自动更新** | 桌面端用户 | 可选 |
| ⭐⭐ | **邮箱报告补财务/股东回报/HK-US** | 你的多市场 | 建议合 |
| ⭐⭐ | **设置页完善 (PR 1328/1450/1453)** | 体验 | 建议合 |
| ⭐ | Web 拆分 chunks (PR 1410/1418) | 前端性能 | 自动受益 |
| ⭐ | **MiMo fallback pricing** (#1350) | 备用模型 | 可选 |
| ⭐ | 问股 provider-aware trace (#1473) | agent 调试 | 建议合 |
| ⭐ | 桌面/部署修复 | 看使用场景 | 看你 |

---

## 📈 风险提示

1. **719 commit 仍然很多**，19 天跨度，**一次性合并高冲突风险**
2. **Panda 本地定制**（飞书推送 + 音量柱 K 线策略）必须保留
3. **告警中心是破坏性变更** — DB schema 新增了告警表，升级前需备份
4. **Web 前端重构** (#1410/1418/1425) 可能影响你的本地前端定制
5. **v3.18 release** 跳过了 v3.19/20/21 — 6 月份 upstream 还有新东西

---

## 💡 推荐操作（与之前一致）

```bash
# 1. 备份你的本地定制
cd /home/panda/project/daily_stock_analysis-main
cp src/notification.py /tmp/notification.py.backup
ls strategies/  # 看看你的本地策略配置

# 2. 拉分支
git checkout -b sync/fork-v3.18
git merge origin/main --no-ff

# 3. 重点保护这几处
# - src/notification.py (飞书推送定制)
# - strategies/ (你的本地策略)
# - .env (你的模型配置)
# - 任何 Panda 自己写的 commit

# 4. 处理冲突后跑测试
source venv/bin/activate
pytest tests/ -x

# 5. 验证服务
nohup python server.py > logs/server.log 2>&1 &
```

**我的建议：分批合** — 这次先只合 **告警中心** + **美股数据源** 两块，其他等稳定再说。

要我现在就拉分支试合并吗？或者你想先看哪几个 PR 的具体 diff？

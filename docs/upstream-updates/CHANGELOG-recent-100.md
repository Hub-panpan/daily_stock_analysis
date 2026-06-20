## 4b3f679 - feat: adapt AlphaSift hotspot topics (#1635)

**作者**: mumu | **日期**: 2026-06-12 | **PR**: #
**类型**: 

* feat: adapt AlphaSift hotspot topics

* fix(review-feedback-1635): preserve cached hotspots when refresh returns no rows and Avoid

* fix(review-feedback-1635): Reload detail when refreshing the selected hotspot and Fall back when

* fix(review-feedback-1635): update by the requested topic or a request token

* fix(review-feedback-1635): preserve analysis when optional serve startup fails and Fall back when

* fix(review-feedback-1635): 当前 CI 状态为 failure，且 backend-gate 为 cancelled、docker-build 为 skipped

* fix(review-feedback-1635): 让 backend-gate / docker-build 在当前 head 上完成并通过，或给出可接受的维护者级豁免说明

* fix(review-feedback-1635): 当前 CI 仍未闭环：结构化事实显示 backend-gate 被取消、docker-build skipped

* fix(review-feedback-1635): 修复 hotspot detail 的上游 schema 容错问题，并让当前 head 的阻断 CI 重新跑通

* fix(review-feedback-1635): docs/CHANGELOG.md：当前 diff 不是在 [Unreleased] 扁平格式下追加本 PR

* fix(review-feedback-1635): CI 闭环未完成：结构化事实显示当前 CI 状态为 failure，backend-gate cancelled、docker-build

* fix(review-feedback-1635): 让当前 head 的阻断型 CI 完整通过，并修正文档中的 AlphaSift commit hash 不一致

* fix(review-feedback-1635): CI 仍未在当前 head 完整通过：结构化事实显示

* fix(review-feedback-1635): 修复 docs/CHANGELOG.md 对主线既有 [Unreleased] 条目的删除，并补齐 AlphaSift

* fix(review-feedback-1635): Accept slash-containing hotspot topics

* fix(review-feedback-1635): Try industry constituents for industry hotspots

* fix(review-feedback-1635): Clear old hotspot details when loading a new topic and preserve the

* test: isolate main schedule environment

* chore: clean AlphaSift PR scope

* fix: respect AlphaSift hotspot fallbacks
---

## efa41e0 - feat: [issue #1652] add live run-flow diagnostics (#1656)

**作者**: LouisHong | **日期**: 2026-06-12 | **PR**: #
**类型**: 

* feat: add live run-flow updates and diagnostics

* feat: update task status filter to include 'cancel_requested'

* feat: enhance run-flow diagnostics and task management with cancel-requested status handling

* fix: stabilize run flow live updates

* fix: align live run-flow review contracts

* fix: sanitize live run-flow events
---

## 4082c0d - 改进: 补充 #1390 P1 DecisionSignal 前端契约与隔离测试 (#1666)

**作者**: Alfred | **日期**: 2026-06-11 | **PR**: #
**类型**: 

* feat: add decision signal web contract wrapper

* fix: reject unsupported decision signal latest paths

* fix: tighten decision signal list response contract
---

## f7ac00b - feat:[issue #1652] add web run-flow viewer (#1654)

**作者**: LouisHong | **日期**: 2026-06-11 | **PR**: #
**类型**: 

* feat: add web run-flow viewer

* docs: document run-flow web viewer contracts

* fix: add market review run flow entry
---

## fa9d9b0 - feat: [issue #1652] add run-flow snapshot contract and APIs (#1653)

**作者**: LouisHong | **日期**: 2026-06-10 | **PR**: #
**类型**: 

* feat: add run-flow snapshot contract and APIs

* fix: address run-flow contract review notes

---------

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## f587459 - feat: add portfolio account archive action 持仓管理页面添加账户删除功能 (#1647)

**作者**: volcanoAlbert | **日期**: 2026-06-10 | **PR**: #
**类型**: 

* feat: add portfolio account archive action

* fix: exclude archived accounts from risk snapshots
---

## ad15ebc - feat: 新增 DecisionSignal 持久化 API（#1390 P1） (#1645)

**作者**: Alfred | **日期**: 2026-06-10 | **PR**: #
**类型**: 

* feat: add decision signal persistence api

Refs #1390

* fix: handle HK decision signal filters without market
---

## da274f7 - fix: 锁定问股追问的当前标的上下文 P2 (#1619)

**作者**: Alfred | **日期**: 2026-06-10 | **PR**: #
**类型**: 

* fix: keep ask-stock follow-ups scoped

* fix: normalize watchlist stock comparisons

* docs: document watchlist stock code equivalence

* fix: tighten ask-stock tool scope guard

* fix: close ask-stock review gaps

* fix: close ask-stock review gaps
---

## 4f53602 - fix: clarify runtime logging context (#1643)

**作者**: LouisHong | **日期**: 2026-06-09 | **PR**: #
**类型**: 

* fix: clarify market review logging context

* docs: update changelog for logging context
---

## ff6494b - feat: 新增建议动作 taxonomy 字段边界 P0 (#1631)

**作者**: Alfred | **日期**: 2026-06-08 | **PR**: #
**类型**: 

* feat: add decision action taxonomy fields

* fix: tighten decision action fallback handling

* fix: align legacy decision action guard fallback

* fix: tighten legacy decision action word boundaries

* fix: align decision action compound parsing

* fix: clean decision action residue

* fix: align web action label contract

* fix: classify avoided sell actions as hold
---

## e2fe6e3 - fix: verify packaged AlphaSift adapter at runtime (#1637)

**作者**: mumu | **日期**: 2026-06-08 | **PR**: #
**类型**: 

* fix: verify packaged AlphaSift adapter at runtime

* fix(review-feedback-1637): Wait for the windowed probe process

* fix(review-feedback-1637): 收敛 docs/CHANGELOG.md 的范围漂移/描述不一致问题

* fix(review-feedback-1637): 收敛 docs/CHANGELOG.md 的无关历史改动，只保留本 PR 对 [Unreleased] 的新增修复条目
---

## 40c5c75 - chore: prepare v3.21.0 release

**作者**: zhulinsen | **日期**: 2026-06-07 | **PR**: #
**类型**: 


---

## 12a7e6d - fix: make AlphaSift screening recoverable (#1628)

**作者**: mumu | **日期**: 2026-06-07 | **PR**: #
**类型**: 

* fix: make AlphaSift screening recoverable

* fix(review-feedback-1628): Keep polling state across transient status errors
---

## 513271b - fix(issue-1626): [bug]-web-英文界面仍残留中文文案 (#1632)

**作者**: mumu | **日期**: 2026-06-07 | **PR**: #
**类型**: 


---

## 8909168 - fix: run manual market review on non-trading days (#1627)

**作者**: mumu | **日期**: 2026-06-07 | **PR**: #
**类型**: 


---

## 649f775 - chore: remove one-off PR screenshot assets (#1625)

**作者**: mumu | **日期**: 2026-06-06 | **PR**: #
**类型**: 

* chore: remove one-off PR screenshots

* chore: remove one-off issue screenshots
---

## d704fe3 - feat: add Web UI language switch (#1621)

**作者**: mumu | **日期**: 2026-06-06 | **PR**: #
**类型**: 

* feat: add Web UI language switch

* fix(review-feedback-1621): 补充 zh/en 切换后的登录页、首页、设置页和侧边导航截图或可访问构建预览证据

* fix(review-feedback-1621): 补对应回归测试

* fix(review-feedback-1621): Pin the smoke test's initial language

* fix(review-feedback-1621): Web UI 改动缺少截图或等价可视证据

* fix(review-feedback-1621): 补一个 storage accessor 抛错时 fallback 到 zh 或 navigator 语言的回归测试

* fix(review-feedback-1621): 修复前端 lint/build 失败并补齐 Web 验证证据

* fix(review-feedback-1621): apps/dsa-web/ ：本 PR 新增语言切换入口并改动

* fix(review-feedback-1621): 解决冲突

* fix(review-feedback-1621): 解决冲突，并补齐 Web UI 变更的可视证据与 Web 侧验证说明

* fix(review-feedback-1621): 解决冲突并重新确认 diff 与 CI 结果

* fix(review-feedback-1621): 解决冲突

* fix(review-feedback-1621): add a file-level test

* fix: complete Web UI language switch evidence

* fix(review-feedback-1621): 确认设置页英文字段 label 语义回归、Playwright smoke locale 稳定性，以及结构化检测命中的外部模型/API

* fix(review-feedback-1621): 修正 PR 描述与实际实现不一致，并补齐 Playwright smoke 验证结果或明确未执行原因

* fix: complete web language behavior

* fix(review-feedback-1621): src/services/task queue.py / src/services/analysis service.py /

* fix: honor market review request language

* fix(review-feedback-1621): Keep UI language from overriding report language and Use localized

* fix(review-feedback-1621): docs/full-guide.md / docs/full-guide EN.md 把 PR 评审证据、执行命令、沙箱

* fix(review-feedback-1621): 修正 PR 描述与当前实现不一致的问题，并补齐运行时模型配置相关的兼容性/迁移证据

* fix(review-feedback-1621): 收敛后再合入
---

## 617b11d - fix: restore market review in stock bar (#1620)

**作者**: mumu | **日期**: 2026-06-06 | **PR**: #
**类型**: 

* fix: restore market review in stock bar

* fix(review-feedback-1620): Refresh market history non-silently after deleting MARKET
---

## 1e94490 - fix: widen analytical intel search lookback (#1615)

**作者**: mumu | **日期**: 2026-06-06 | **PR**: #
**类型**: 

* fix: widen analytical intel search lookback

* fix(review-feedback-1615): 澄清或修正分析类 180 天目标窗口在 provider 粗粒度映射下可能实际扩大到 1 年的问题
---

## 2f26042 - fix: 报告页运行诊断与输入数据块状态口径不一致 (#1602) (#1603)

**作者**: mumu | **日期**: 2026-06-05 | **PR**: #
**类型**: 

* fix(issue-1602): [bug]-报告页运行诊断与输入数据块状态口径不一致

* fix: clarify report diagnostics evidence scope

* fix(review-feedback-1603): 更新 PR body，使范围、验证、兼容性风险和回滚说明与当前 head 一致
---

## 3153c76 - fix: 收敛多股通知摘要的市场状态展示 (#1612)

**作者**: mumu | **日期**: 2026-06-05 | **PR**: #
**类型**: 

* fix: compact aggregate report market status

* fix(review-feedback-1612): preserve input order when selecting market status

* chore: rerun review after clarifying PR scope
---

## 8a77960 - docs: require screenshots for visual PR changes (#1613)

**作者**: mumu | **日期**: 2026-06-05 | **PR**: #
**类型**: 


---

## 39f24df - 代码健康修复：稳定测试、健康检查、错误响应与 schema 版本记录 (#1607)

**作者**: fzxiong | **日期**: 2026-06-05 | **PR**: #
**类型**: 

* fix(api): return json from root health endpoint

* test(web): stabilize vitest runtime setup

* chore(security): warn on public web exposure without auth

* refactor(api): centralize error response helpers

* chore(db): record baseline schema version

* refactor(web): extract portfolio formatting helpers

* fix(db): make schema baseline initialization idempotent

* docs: document health check and schema baseline changes
---

## 3471afb - feat: add Feishu App Bot notification sender with P2P and group support (#1553)

**作者**: Delicious233 | **日期**: 2026-06-05 | **PR**: #
**类型**: 

* feat: add Feishu App Bot notification sender with P2P and group support

The existing FeishuSender only supports custom robot Webhook mode.
This commit extends it to support App Bot (lark-oapi SDK) mode, auto-routing
between webhook (priority) and App Bot when FEISHU_APP_ID + FEISHU_APP_SECRET
+ FEISHU_CHAT_ID are configured.

Design:
- send_to_feishu() routes: webhook if URL set, else App Bot
- DCLP lazy client init with thread-safe sentinel guard
- Retry (3 attempts, exponential backoff) with fixed UUID for idempotency
- Card-first / text-fallback content strategy
- Chunking for long messages
- Runtime enum validation for FEISHU_RECEIVE_ID_TYPE and FEISHU_DOMAIN
- Safe SDK defaults (FEISHU_DOMAIN/LARK_DOMAIN) before import try-block
  so Webhook path never depends on lark-oapi SDK presence
- Config, diagnostics, setup check, notification test, and CI workflow
  all consistent with the new App Bot channel semantics
- lark-oapi>=1.0.0 already in requirements.txt (line 23)

Verification:
- 20/20 unit tests pass (help metadata + FeishuSender)
- E2E: real Feishu API — SDK import, token, client init, P2P text+card send all PASS
- Webhook regression: verified no SDK dependency for existing Webhook path

* fix: add missing Feishu App Bot locale entries and env table keys, harden sender error handling

CI fix 1 (test_registry_help_keys_exist_in_locales):
- Add zh-CN and en-US locale entries for FEISHU_CHAT_ID,
  FEISHU_RECEIVE_ID_TYPE, FEISHU_DOMAIN in settingsHelp.ts

CI fix 2 (test_notification_actions_env_table_matches_generated_output):
- Add FEISHU_RECEIVE_ID_TYPE, FEISHU_DOMAIN to feishu advanced_keys
  in CHANNEL_SPECS so they appear in KEY_SPECS
- Regenerate managed env table in docs/notifications.md

feishu_sender.py hardening:
- Catch network exceptions in webhook _post_payload so card-to-text
  fallback actually executes on transient failures
- Guard response.json() and isinstance(result, dict) against
  non-JSON / non-dict HTTP 200 responses
- Extract shared _build_card_body() to de-duplicate card payload
  construction between webhook and App Bot paths
- Rename module-level lark -> _lark to avoid shadowing
- Guard resp.get_log_id() with try/except
- Add None guard on send_to_feishu content parameter

e2e script improvements:
- Support FEISHU_OPEN_ID for P2P test, FEISHU_DOMAIN for Lark
- Add FEISHU_TEST_SEND_TEXT=1 for plain-text-only path testing
- Clarify docstring: setup validation + smoke test, not full e2e

* fix: consolidate Feishu App Bot notification contract

* fix: align Feishu domain help scope

---------

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## 0ca4e07 - feat: integrate AlphaSift with DSA runtime enrichment (#1577)

**作者**: mumu | **日期**: 2026-06-05 | **PR**: #
**类型**: 

* feat: integrate AlphaSift with DSA runtime enrichment

* feat: pin AlphaSift DSA provider context

* fix: clean up AlphaSift warning display

* fix(review-feedback-1577): pass the headers through a path AlphaSift actually uses, such as a

* fix(review-feedback-1577): 补齐 LLM 运行时桥接兼容性的关键证据

* fix: keep AlphaSift screening lightweight

* fix(review-feedback-1577): Populate DSA news when reusing context

* fix(review-feedback-1577): 补齐外部 LLM/LiteLLM 兼容依据，并修正 docs/CHANGELOG.md 的格式/重复条目问题

* fix(review-feedback-1577): 补齐外部模型/API 兼容依据或在 PR 正文中明确指向已更新文档中的官方来源与迁移/回退边界

* fix(review-feedback-1577): scripts/build-backend.ps1 已随本 PR 调整 AlphaSift 打包/收集逻辑，但完整改动文件列表未包含

* fix(review-feedback-1577): 处理 AlphaSift LLM bridge 对全局 LiteLLM 状态的并发污染风险

* fix: reuse DSA daily history for AlphaSift

* fix(review-feedback-1577): 补齐 --collect-all alphasift 或等价 hidden imports，并增加打包产物级导入验证

* fix(review-feedback-1577): fix the macOS AlphaSift package verifier

* fix(review-feedback-1577): scripts/build-backend-macos.sh 和 scripts/build-backend.ps1

* fix(review-feedback-1577): 处理运行时阻塞风险、CHANGELOG 删除既有条目，以及补齐外部模型/API 兼容证据

* fix(review-feedback-1577): scripts/build-backend-macos.sh：当前“Verifying packaged AlphaSift

* fix(review-feedback-1577): 收敛下面的可用性判断和外部 API/模型兼容证据缺口

* fix(review-feedback-1577): src/config.py、src/core/config registry.py、src/services/alphasift

* fix(review-feedback-1577): scripts/build-backend-macos.sh：新增的 packaged AlphaSift importability

* fix(review-feedback-1577): make the archive fallback require a dsa adapter entry or exercise the

* fix(review-feedback-1577): 处理无关测试改动，并补齐桌面打包文档/验证边界
---

## 813b5d6 - fix: prevent stock card phase label overlap (#1605)

**作者**: Alfred | **日期**: 2026-06-05 | **PR**: #
**类型**: 

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## 71055c4 - fix: 问股自由文本金融缩写不再误识别为股票代码 (#1604)

**作者**: Alfred | **日期**: 2026-06-05 | **PR**: #
**类型**: 

* fix: prevent finance abbreviations from becoming chat tickers

* fix: filter uppercase filler words in chat ticker extraction
---

## 8df69fe - feat: 完善大盘复盘历史聚合、查看与删除能力 (#1580) (#1598)

**作者**: mumu | **日期**: 2026-06-04 | **PR**: #
**类型**: 

* feat(issue-1580): feat:-完善大盘复盘历史聚合、查看与删除能力

* fix(review-feedback-1598): resetting the paged window or deduping the merged list before storing it

* fix(review-feedback-1598): 补齐 AGENTS.md 要求的用户可见能力文档同步
---

## e6302a0 - docs: add #1386 P7 market-phase guide (#1597)

**作者**: Alfred | **日期**: 2026-06-04 | **PR**: #
**类型**: 


---

## 649413c - fix: pass SearXNG Actions variables to daily workflow (#1567)

**作者**: mumu | **日期**: 2026-06-04 | **PR**: #
**类型**: 


---

## d6234cd - fix: clarify Docker env runtime config (#1586)

**作者**: mumu | **日期**: 2026-06-04 | **PR**: #
**类型**: 

* fix: clarify Docker env runtime config

* fix(review-feedback-1586): 确认并修复启动环境变量兜底对 switch 类型配置的展示正确性，否则 Docker 用户仍可能在关键布尔配置上看到错误状态

* fix(review-feedback-1586): 修正 docs/CHANGELOG.md 的范围漂移和重复内容

* fix(review-feedback-1586): 补充说明这些值仅作为已有配置键的展示 fallback，不新增默认 provider/model/Base URL，也不会静默迁移或清空用户配置

* fix(review-feedback-1586): 确认并修复运行时注入的 LLM channel 支持键在 Settings 保存/校验路径中的一致性问题

* fix(review-feedback-1586): 修复下述运行时配置静默持久化风险

* fix(review-feedback-1586): 修复 runtime-only LLM support key 过滤逻辑对“同一 channel 部分字段来自

* fix(review-feedback-1586): apps/dsa-web/src/components/settings/LLMChannelEditor.tsx、src/services/s

* fix(review-feedback-1586): Avoid migrating runtime-only secrets on rename

* fix(review-feedback-1586): 补充该说明

* fix(review-feedback-1586): docs/CHANGELOG.md 新增说明直接引用 litellm =1.80.10,!=1.82.7,!=1.82.8,<2.0.0

* fix(review-feedback-1586): 补齐“持久化 API KEY + runtime-only API KEYS

* fix(review-feedback-1586): 收敛
---

## c6221ba - fix: avoid quoting desktop updater install directory (#1587)

**作者**: mumu | **日期**: 2026-06-04 | **PR**: #
**类型**: 


---

## b612fb2 - fix: 结构化大盘复盘报告展示 (#1576)

**作者**: mumu | **日期**: 2026-06-04 | **PR**: #
**类型**: 

* feat: add dedicated market review report view

* fix(review-feedback-1576): Use localized labels for English market reviews

* fix: structure market review payload rendering

* fix(review-feedback-1576): preserve market labels when rendering combined reviews and Use the

* fix(review-feedback-1576): Render structured data for every combined market and Localize

* fix: dedupe market review rendering

* test: align market review language prompt expectation

* fix(review-feedback-1576): 澄清并补足 LLM/运行时配置相关检测命中的兼容性证据

* fix(review-feedback-1576): 解决冲突并重新确认 CI

* fix(review-feedback-1576): docs/CHANGELOG.md：[Unreleased] 新增内容中除 1555 大盘复盘展示外，还包含 Agent

* fix(review-feedback-1576): 修复

* fix(review-feedback-1576): 修复美股中文大盘复盘仍混入英文策略/市场标签的问题，并补齐对应回归测试
---

## 3281d96 - docs: close analysis context pack P6 (#1592)

**作者**: Alfred | **日期**: 2026-06-04 | **PR**: #
**类型**: 


---

## 6784409 - docs: harden PR quality guardrails (#1593)

**作者**: Alfred | **日期**: 2026-06-04 | **PR**: #
**类型**: 


---

## 9b76f8d - feat: #1386 P6 联动告警、持仓和历史阶段摘要 (#1589)

**作者**: Alfred | **日期**: 2026-06-04 | **PR**: #
**类型**: 

* feat: link phase summaries across P6 surfaces

* fix: align portfolio analysis response status

* fix: stabilize backtest phase filtering

* fix: normalize portfolio analysis symbols
---

## f091810 - refactor: 优化侧边栏选中态样式、扩展宽度并新增 rail 紧凑模式 (#1579)

**作者**: Sunflower | **日期**: 2026-06-04 | **PR**: #
**类型**: 

* fix: refine sidebar nav active indicator, expand width, and add rail variant support

* fix: remove /cloud-actions nav item without route, restore changelog entries

* chore: use cn() for iconClassName default instead of array literal

* fix: clean sidebar pr after main rebase
---

## d22ff1c - chore: prepare v3.20.0 release

**作者**: ZhuLinsen | **日期**: 2026-06-03 | **PR**: #
**类型**: 


---

## 44ea049 - feat: add web market phase labels (#1582)

**作者**: Alfred | **日期**: 2026-06-03 | **PR**: #
**类型**: 


---

## 5cd968b - fix: improve Windows first-run encoding compatibility (#1583)

**作者**: mumu | **日期**: 2026-06-03 | **PR**: #
**类型**: 


---

## 14d666b - fix: avoid agent daily bars missing false positive (#1578)

**作者**: mumu | **日期**: 2026-06-03 | **PR**: #
**类型**: 


---

## 1d8a043 - fix: 自动安装 AlphaSift 并收敛选股开关 (#1557)

**作者**: mumu | **日期**: 2026-06-03 | **PR**: #
**类型**: 

* fix: enable AlphaSift auto install from web toggle

* fix: allow local AlphaSift auto install

* fix: allow web AlphaSift auto install

* fix: reinstall AlphaSift when adapter is missing

* fix(review-feedback-1557): Require auth when proxied localhost headers are spoofable

* fix: bridge DSA LLM config for AlphaSift

* fix(review-feedback-1557): Document the install auth gate accurately and Serialize implicit

* fix: align AlphaSift LLM fallbacks with DSA routes

* fix: reduce AlphaSift snapshot fallback noise

* fix: preserve AlphaSift snapshot source priority

* fix(review-feedback-1557): api/v1/endpoints/alphasift.py：本 PR 在策略列表、选股接口和 Web enable flow

* fix(review-feedback-1557): 补齐 AlphaSift/LLM 配置兼容性证据或说明，避免把外部 provider/model 路由语义变更作为低风险修复直接合入

* fix(review-feedback-1557): 补充一句说明该兼容边界依据来自仓库内既有配置链路，且不做 .env provider/model 静默迁移
---

## 52558a9 - feat: upgrade MiniMax default model to M3 (#1574)

**作者**: Octopus | **日期**: 2026-06-03 | **PR**: #
**类型**: 

* feat: upgrade MiniMax default model to M3

- Add MiniMax-M3 to model list and set as default
- Keep MiniMax-M2.7 and MiniMax-M2.7-highspeed
- Remove older models (M2.5)
- Update related tests

* docs: clarify MiniMax-M3 conservative <=512K pricing tier and restore M2.5 legacy entry

Address review feedback on MiniMax model upgrade:

- M3 official docs report up to 1M input tokens with a separate >512K input
  pricing tier; expand inline comments in src/agent/llm_adapter.py and in
  docs to make clear that this PR conservatively registers only the
  <=512K input bucket (context_window=512000, max_tokens=128000,
  $0.6/M input, $2.4/M output), and that long-context cost estimates
  using this entry should be treated as a floor.
- Restore MiniMax-M2.5 as a legacy entry under _CUSTOM_MODEL_PRICING so
  existing user configs that still reference M2.5 continue to report
  accurate cost estimates instead of silently falling back to the zero-
  cost generic pricing. M2.5 is still listed as a Legacy Model on the
  official pricing page; the comment block notes the removal precondition.
- Update docs/CHANGELOG.md and docs/llm-providers.md to mention the 1M
  upstream limit, the conservative <=512K registration, and that M2.5 is
  retained as legacy pricing.

No runtime behavior change beyond the M2.5 pricing restoration; existing
M3 / M2.7 pricing values are unchanged.

---------

Co-authored-by: octo-patch <octo-patch@github.com>
---

## 93c1128 - fix: register health router in v1 API so /api/v1/health returns 200 (#1572)

**作者**: Amorend | **日期**: 2026-06-03 | **PR**: #
**类型**: 

* fix: register health router in v1 API so /api/v1/health returns 200

The health endpoint at api/v1/endpoints/health.py was defined but never
included in api/v1/router.py, causing /api/v1/health to return 404 while
/api/health worked fine.

This adds the missing include_router call and a test covering both paths.

Fixes #1561

* fix: exempt /api/v1/health from auth middleware and add auth-enabled tests

When ADMIN_AUTH_ENABLED=true, AuthMiddleware blocks all /api/v1/*
paths not in EXEMPT_PATHS. The newly registered /api/v1/health was
missing from that list, so unauthenticated health probes from load
balancers or monitors would get 401 instead of 200.

Adds /api/v1/health to EXEMPT_PATHS and covers both /api/health and
/api/v1/health under the auth-enabled scenario.

* fix: correct auth-enabled test mock target and add CHANGELOG entry

- Patch api.middlewares.auth.is_auth_enabled instead of src.auth so
  the mock actually reaches AuthMiddleware.dispatch
- Add [Unreleased] entry to docs/CHANGELOG.md

* chore: remove unused import os from test_api_health.py
---

## 7e54c6c - feat: add analysis phase API plumbing (#1573)

**作者**: Alfred | **日期**: 2026-06-03 | **PR**: #
**类型**: 


---

## d8a067b - feat: improve first-run configuration validation (#1558)

**作者**: 123kaze | **日期**: 2026-06-02 | **PR**: #
**类型**: 

* feat: improve first-run configuration validation

* fix: clarify invalid LLM channel validation
---

## 3ea007c - feat: 盘中决策护栏与 phase_decision 质量校验 P5 (#1563)

**作者**: Alfred | **日期**: 2026-06-02 | **PR**: #
**类型**: 

* feat: add phase decision guardrails

* fix: neutralize non-intraday immediate actions

* test: cover low-confidence non-intraday actions
---

## 81c0287 - feat: 新增个股栏与自选队列操作 (#1540)

**作者**: zbl-96 | **日期**: 2026-06-02 | **PR**: #
**类型**: 

* feat: add stock bar sidebar and watchlist management

- Replace history list sidebar with stock bar that deduplicates stocks
  and places market review at top, ordered by latest analysis time
- Add GET /api/v1/history/stocks endpoint for distinct stock list
- Add code normalization to merge code variants (e.g. 002460 / 002460.SZ)
- Add GET/POST /api/v1/stocks/watchlist CRUD endpoints
- Add watchlist card to report detail right sidebar
- Add watchlist buttons to chat/ask page with auto stock code detection
- Add useWatchlist hook for shared watchlist state management
- Update CHANGELOG with [Unreleased] flat entries

Refs #1530

* fix: use canonical normalize_stock_code for stock code dedup

Replace ad-hoc suffix stripping with the existing normalize_stock_code
in data_provider/base.py, which handles all supported variants:
SH600519 / 600519.SH / HK00700 / 00700.HK / BJ920748 / 920748.BJ.

Addresses Codex P2 suggestion on PR #1540.

* fix: address PR review feedback on #1540

1. Fix extractStockCodeFromMessage to reject exchange prefixes
   (SH/SZ/BJ/HK/US/SS) as standalone tickers; add explicit patterns
   for SH600519/SZ000001/BJ920748 prefix formats.
   Move function to utils/chatStockCode.ts to satisfy react-refresh.

2. Add stock code validation and normalization in watchlist API
   (add/remove endpoints now validate format and use
   normalize_stock_code before persisting to STOCK_LIST).

3. Over-fetch distinct stocks (limit*3) before normalization dedup
   to avoid losing results when code variants shrink after grouping.

4. Update HomePage tests: remove batch-delete test scenario (sidebar
   replaced by StockBar), add getStockBarList/getWatchlist mocks,
   adjust assertions to match StockBarItem accessible names.

Refs #1540

* fix: normalize watchlist codes on read/write and strengthen validation

1. _read_watchlist_codes now normalizes and deduplicates all existing
   STOCK_LIST entries via normalize_stock_code, so hk00700/HK00700/00700.HK
   are treated as one canonical entry.
2. _write_watchlist_codes deduplicates before persisting.
3. _validate_and_normalize_stock_code uses regex matching against
   all supported stock code formats (aligned with frontend validateStockCode).
4. Restore accidentally deleted CHANGELOG entry for same-stock history trend.
5. Fix CHANGELOG/PR description API paths to match actual routes.

Refs #1540

* fix: normalize stock codes in frontend watchlist comparison

Add normalizeStockCode utility mirroring backend normalize_stock_code,
and use it in isInWatchlist so SH600519/600519.SH/HK00700/00700.HK
variants are all recognized as the same stock. Add 10 regression tests.

Refs #1540

* fix: normalize stock code variants in watchlist comparison and extraction

1. ChatPage.tsx: stockInWatchlist now normalizes input via normalizeStockCode
   before comparing against watchlistCodes, so SH600519/600519.SH variants
   are correctly recognized as already being in the watchlist.
2. chatStockCode.ts: add \d{1,5}\.HK suffix pattern (e.g. 00700.HK → HK00700),
   and return normalizeStockCode(normalized) for all extracted codes.
3. stocks.py: add bare 5-digit HK code (\d{5}) to _STOCK_CODE_RE regex.
4. ChatPage tests: add mockGetWatchlist/AddToWatchlist/RemoveFromWatchlist mocks,
   add 2 regression tests for watchlist button with code variants
   (600519.SH → 600519 and 1810.HK → HK01810).

Refs #1540

* fix: keep STOCK_LIST as-is, normalize only for comparison

Revert read/write normalization in _read_watchlist_codes and
_write_watchlist_codes. STOCK_LIST is now stored exactly as the user
input, without auto-normalization. Add/remove endpoints normalize
only for duplicate/matching comparison, preserving raw codes.

Refs #1540

* feat: restore batch delete in StockBar and add delete-by-code API

1. Add DELETE /api/v1/history/by-code/{stock_code} endpoint to delete
   all history records for a given stock code in one call.
2. Add deleteByCode function to frontend historyApi.
3. StockBar: restore select-all checkbox and batch delete button,
   matching the original HistoryList UX.
4. StockBarItem: add per-item delete button (trash icon, visible on hover).
5. HomePage: wire handleDeleteStock to StockBar, refresh stock bar and
   history after deletion.
6. Update CHANGELOG to reflect restored batch delete capability.

Refs #1540
---

## 81e9ca8 - fix(issue-1543): [bug]-alphasift-可用性检测不应静默吞掉非预期异常 (#1544)

**作者**: mumu | **日期**: 2026-06-01 | **PR**: #
**类型**: 


---

## 3e08589 - feat: add phase data quality prompt guards (#1546)

**作者**: Alfred | **日期**: 2026-06-01 | **PR**: #
**类型**: 


---

## 7221343 - feat: add lightweight AlphaSift screening integration (#1443)

**作者**: mumu | **日期**: 2026-05-31 | **PR**: #
**类型**: 

* feat: add lightweight AlphaSift screening integration

* fix(review-feedback-1443): 解决冲突后重新确认受影响文件和 CI 结果 and Restrict install spec before executing pip

* fix(review-feedback-1443): add a feature/auth gate before invoking installation side effects

* fix: repair AlphaSift enable flow

* fix(review-feedback-1443): Enable config before calling AlphaSift install

* fix(review-feedback-1443): re-fetch status in the error path to avoid this UI/backend state

* fix(review-feedback-1443): 补充对应回归测试

* fix(review-feedback-1443): 补充对应测试

* fix(review-feedback-1443): api/v1/endpoints/alphasift.py 的状态接口会返回 ALPHASIFT INSTALL SPEC，而项目默认

* fix(review-feedback-1443): 补一个前端用例覆盖

* fix(review-feedback-1443): 解决冲突后再合入

* fix(review-feedback-1443): 解决后再重新确认 diff 与 CI 结果

* fix(review-feedback-1443): 解决冲突并确认解决后的 diff 未引入新风险

* fix(review-feedback-1443): Read picks from AlphaSift ScreenResult and Use AlphaSift's actual

* fix(review-feedback-1443): 修正

* fix(review-feedback-1443): 解决冲突并重新确认 CI/Web gate 结果

* fix(review-feedback-1443): 解决冲突并重新确认 CI/Web gate，另外需要澄清本次 diff 中 LLM 配置相关改动是否属于本 PR 范围及其兼容性影响

* fix(review-feedback-1443): 解决冲突，并补齐受影响前端构建/测试验证后再合入

* fix(review-feedback-1443): 解决冲突，并补齐受影响前端 Web gate 或等价 CI 证据后再合入

* fix(review-feedback-1443): 解决冲突，并补齐受影响 Web gate 与兼容性验证说明后再合入

* fix(review-feedback-1443): mark this field sensitive and/or display only a masked/sanitized source

* fix(review-feedback-1443): 解决冲突，并补齐受影响前端验证与外部兼容性说明后再合入

* fix(review-feedback-1443): 解决冲突，并补齐冲突解决后的验证结果后再合入

* fix(review-feedback-1443): 解决冲突，并补齐受影响后端/Web 验证证据后再合入

* fix(review-feedback-1443): 解决冲突后基于最终 head 重新给出验证结论，否则无法确认最终合入内容与当前审查内容一致

* fix(review-feedback-1443): 解决冲突并补齐冲突后的验证结论

* fix(review-feedback-1443): Clear stale candidates when strategy changes

* fix(review-feedback-1443): preserve TestClient cookies across requests

* fix(review-feedback-1443): 解决冲突并基于冲突后的最终 head 重新确认受影响验证，当前不能直接合入

* fix(review-feedback-1443): 补回归测试

* fix(review-feedback-1443): 补后端回归测试

* fix(review-feedback-1443): 解决冲突，并在解决后重新给出基于最终 head 的验证结果

* fix(review-feedback-1443): 解决冲突并基于最终 diff 重新确认验证结果

* fix(review-feedback-1443): 解决冲突，并在冲突解决后的最终 head 上重新给出后端与 Web 相关验证结论

* fix(review-feedback-1443): 解决冲突，并在最终 head 上重新确认后端、Web 和文档改动仍一致

* fix(review-feedback-1443): 当前 PR 存在合并冲突，虽然 CI 摘要为 success，但冲突解决后的最终代码和验证结果尚未形成，当前不能直接合入

* fix(review-feedback-1443): 解决冲突并补齐验证

* fix(review-feedback-1443): 解决冲突

* fix(review-feedback-1443): 修正测试客户端生命周期问题，并补齐前端 lint/build 验证

* fix(review-feedback-1443): 解决冲突

* feat: refine AlphaSift adapter integration

* fix: restore settings help metadata for CI

* fix(review-feedback-1443): Do not run lifespan for non-context TestClient requests

* fix(review-feedback-1443): Pin AlphaSift install source to an immutable ref

* fix(review-feedback-1443): 补齐后再合入

* fix: harden alphasift review feedback

* fix(review-feedback-1443): api/v1/endpoints/alphasift.py：自动安装路径在 adapter 可导入但 get status 返回

* fix: package alphasift endpoint in desktop build

* fix: bundle alphasift in desktop builds

* fix(review-feedback-1443): docs/alphasift-integration.md 中 AlphaSift adapter contract /

* fix: honor empty alphasift install spec

* fix: bundle alphasift in docker image
---

## 3e98dfd - feat: add analysis context data quality scoring (#1539)

**作者**: Alfred | **日期**: 2026-05-31 | **PR**: #
**类型**: 


---

## 9f14850 - feat: add intraday realtime quality metadata (#1538)

**作者**: Alfred | **日期**: 2026-05-31 | **PR**: #
**类型**: 

Refs #1386

Refs #1389
---

## 9178e03 - fix: improve notification report rendering (#1531)

**作者**: mumu | **日期**: 2026-05-31 | **PR**: #
**类型**: 

* fix: improve notification report rendering

* fix: polish chat report rendering output

* fix: add chat-optimized report layout

* fix: use chat report for im image routing

* fix: adapt im report formatting per channel

* fix: make im reports decision cards

* chore: reserve notification renderer presets

* docs: trim notification rendering guidance

* fix(review-feedback-1531): preserve valid links but escape non-link Telegram Markdown characters

* fix(review-feedback-1531): Chunk Telegram fallback before sending raw text

* fix(review-feedback-1531): avoid stripping arbitrary leading whitespace here

* fix: preserve legacy notification report formatting

* fix(review-feedback-1531): 补齐外部模型/API 与运行时配置迁移命中的排除说明或兼容性证据
---

## b22d7e0 - fix: correct ETF secid routing for efinance (#1535)

**作者**: Alfred | **日期**: 2026-05-31 | **PR**: #
**类型**: 

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## 10d2229 - feat: 优化 Web 报告页信息层级 (#1533)

**作者**: Alfred | **日期**: 2026-05-31 | **PR**: #
**类型**: 

* feat: optimize web report detail hierarchy

* fix: include degraded context counts in collapsed summary

---------

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## f42b395 - feat: add market phase summary metadata (#1532)

**作者**: Alfred | **日期**: 2026-05-31 | **PR**: #
**类型**: 


---

## 47c287a - feat: add same-stock history trend drawer (#1524)

**作者**: mumu | **日期**: 2026-05-30 | **PR**: #
**类型**: 

* feat: add same-stock history trend drawer

* fix(review-feedback-1524): 澄清外部模型/API 兼容性检测点，说明本 PR 是否仅展示历史记录中的模型字段，是否不改变 provider/model/Base

* fix: refine stock history drawer layout

* fix(review-feedback-1524): preserve suffixed codes when filtering history

* fix: match stock history issue interaction

* fix(review-feedback-1524): 修复同股代码等价匹配漏查，以及前端抽屉在分页/时间范围下的记录注入与去重问题

* fix(review-feedback-1524): 确认并修复当前同股历史抽屉在空结果时间范围下的交互阻断问题

* fix(review-feedback-1524): CI 当前未通过：结构化事实显示 docker-build:failure、web-gate:failure，而 AGENTS.md 将

* fix: refine stock history trend page

* fix(review-feedback-1524): 修复同股代码等价匹配漏查和市场复盘切换时抽屉状态残留两个正确性问题
---

## e2bda54 - test: mock market light alert notifier (#1527)

**作者**: mumu | **日期**: 2026-05-30 | **PR**: #
**类型**: 


---

## 24ca7e5 - fix: SSRF bypass in daily_stock_analysis (#1500) (#1511)

**作者**: mumu | **日期**: 2026-05-30 | **PR**: #
**类型**: 

* fix(issue-1500): ssrf-bypass-in-daily_stock_analysis

* fix(review-feedback-1511): 解决冲突

* fix(review-feedback-1511): canonicalize or reject these numeric host forms before returning success

* fix(review-feedback-1511): 修正 docs/CHANGELOG.md 的发布段落污染问题，并补齐本次 LLM/Base URL 校验收紧的兼容性/迁移说明或验证依据

* fix(review-feedback-1511): 补充兼容性依据与已验证范围

* fix: block IPv4-mapped metadata base URLs

* fix: trim LLM base URL hardening

* fix(review-feedback-1511): 补齐 Unicode/IDNA 归一化后的受限地址拦截，避免 SSRF 修复仍存在绕过面
---

## dc8613b - fix desktop auto update installer paths (#1519)

**作者**: mumu | **日期**: 2026-05-30 | **PR**: #
**类型**: 


---

## 0295f9d - feat: expose analysis context pack overview (#1515)

**作者**: Alfred | **日期**: 2026-05-30 | **PR**: #
**类型**: 

Refs #1389
---

## b1579bb - fix: localize backtest UI and settings help (#1514)

**作者**: Alfred | **日期**: 2026-05-30 | **PR**: #
**类型**: 


---

## c45eccd - test: allow categorized release changelog entries

**作者**: zhulinsen | **日期**: 2026-05-29 | **PR**: #
**类型**: 


---

## 6415ac2 - docs: prepare v3.19.0 release

**作者**: zhulinsen | **日期**: 2026-05-29 | **PR**: #
**类型**: 


---

## 647b9d2 - fix: support Longbridge OAuth token cache (#1490)

**作者**: mumu | **日期**: 2026-05-29 | **PR**: #
**类型**: 

* fix: support Longbridge OAuth token cache

* fix(review-feedback-1490): bump the runtime dependency minimum or fail with a clear upgrade

* fix(review-feedback-1490): 补充对应回归测试

* fix(review-feedback-1490): Point OAuth cache at the dsa home in Docker

* fix(review-feedback-1490): 修复或给出明确的 CI 重跑通过证据

* fix(review-feedback-1490): 处理 Docker/Actions 持久化 token cache 已损坏时无法被新的 LONGBRIDGE OAUTH TOKEN

* fix: tighten Longbridge OAuth compatibility

* fix: refresh stale Longbridge OAuth cache

* fix: guard Longbridge OAuth SDK availability
---

## 35f26bd - fix: 交互式消息只回对应渠道而非全局广播 (#1501) (#1502)

**作者**: mumu | **日期**: 2026-05-29 | **PR**: #
**类型**: 

* fix(issue-1501): [feature]-飞书同时配置了两种推送方式的改进

* fix(review-feedback-1502): 补齐非飞书交互式上下文的处理与回归测试
---

## c6cad83 - chore: extract analysis artifacts helpers (#1505)

**作者**: Alfred | **日期**: 2026-05-28 | **PR**: #
**类型**: 


---

## 8aa214a - feat: 接入 AnalysisContextPack 低敏 Prompt 摘要 P3 (#1491)

**作者**: Alfred | **日期**: 2026-05-28 | **PR**: #
**类型**: 

* feat: inject AnalysisContextPack prompt summary

* fix: align agent pack summary with prefetched news
---

## f1fdaab - fix: invalid unit abbreviation: T (#1485) (#1489)

**作者**: mumu | **日期**: 2026-05-27 | **PR**: #
**类型**: 

* fix(issue-1485): [bug]-invalid-unit-abbreviation:-t

* fix(review-feedback-1489): 补充该命令或等价运行时 smoke 的通过证据后再合入
---

## 5afe11c - chore(.gitattributes): 完善Git属性配置规范换行符与二进制文件处理——核心目的是解决拉取源代码 docker compose部署的时候的报错:stock-server  | exec /usr/local/bin/docker-entrypoint.sh: no such file or directory (#1488)

**作者**: Heluojiang | **日期**: 2026-05-27 | **PR**: #
**类型**: 

为shell脚本、Dockerfile、Makefile和.env文件强制配置LF换行符，将证书密钥类二进制文件标记为binary以避免Git修改其编码
---

## a13863e - fix: 为 Akshare 历史兜底接口增加超时保护 (#1465)

**作者**: mumu | **日期**: 2026-05-27 | **PR**: #
**类型**: 

* fix(issue-1464): [bug]-scheduled-analysis-hangs-when-stoc

* fix(review-feedback-1465): Avoid leaking daemon threads on timed-out Akshare calls

* fix(review-feedback-1465): fix can reintroduce hangs/crashes in the exact scheduled pipeline it

* fix(review-feedback-1465): Use a safe start method for timeout subprocesses

* fix(review-feedback-1465): Call freeze support before spawning timeout workers
---

## c1b17bc - fix: [issue #1446] 支持股票自动补全索引远程刷新 (#1480)

**作者**: LouisHong | **日期**: 2026-05-27 | **PR**: #
**类型**: 

* feat: add remote stock index cache refresh

* test: cover remote stock index cache refresh

* docs: document remote stock index updates

* fix: harden stock index refresh and selection

* fix: stabilize stock index fallback selection
---

## bc14f70 - feat: add AnalysisContextPack P2 assembler from pipeline artifacts (#1478)

**作者**: Alfred | **日期**: 2026-05-27 | **PR**: #
**类型**: 

Introduce a zero-fetch builder that assembles internal AnalysisContextPack from existing pipeline artifacts, with tests and P2 contract docs for #1389.
---

## 0bb515c - fix: 问股 single-agent 增加 provider-aware trace (#1473)

**作者**: Alfred | **日期**: 2026-05-26 | **PR**: #
**类型**: 

* fix: add provider-aware trace for ask chat

* fix: drop mismatched provider trace attempts
---

## dad1883 - feat: [issue #1199 PR3] 补齐 Web 设置页实际展示字段帮助信息 (#1450)

**作者**: LouisHong | **日期**: 2026-05-26 | **PR**: #
**类型**: 

* feat: add PR3 Web settings help metadata

* test: enforce Web settings help metadata coverage

* docs: clarify PR3 settings help slice

* docs: add PR3 settings help CHANGELOG entries
---

## 1ad07ba - feat: add #1391 Phase 3 web diagnostic summaries (#1445)

**作者**: mumu | **日期**: 2026-05-26 | **PR**: #
**类型**: 

* fix(issue-1412): [bug]-stock_list格式问题

* fix(review-feedback-1413): preserve exchange hint for dotted A-share inputs

* fix(review-feedback-1413): Keep normalized A-share codes usable by market routing and preserve

* fix(review-feedback-1413): Limit raw dotted codes to fetchers that can parse them

* fix(review-feedback-1413): Keep Tushare daily input normalized for ETF detection

* fix(review-feedback-1413): 澄清结构化检测中的外部模型/API 与运行时配置迁移风险

* fix(review-feedback-1413): 处理或明确确认该失败与本 PR 无关且已有维护者豁免依据

* fix: keep stock list input as bare codes

* docs: add phase-0 run diagnostics contract

* fix(review-feedback-1435): 修正描述并澄清/补齐运行时代码变更的验证证据

* fix(review-feedback-1435): 补齐前缀提示识别，并增加对应回归测试

* fix(review-feedback-1435): 修正

* fix(review-feedback-1435): 解决冲突并更新描述/验证记录后再合入

* fix(review-feedback-1435): 解决冲突，并在最终 head 上重新确认 python -m pytest tests/test a share fetcher code

* fix(review-feedback-1435): 修复并补齐回归覆盖后再复核最终 head

* fix(review-feedback-1435): data provider/baostock fetcher.py 的 convert stock code 只从 .SH/.SS/.SZ

* fix: preserve A-share exchange hints

* fix(review-feedback-1435): 修正 docs/run-diagnostics-p0.md 对 Tushare 本轮范围的矛盾描述

* feat: add phase 1 run diagnostics trace plumbing

* feat: add phase 2 run diagnostic summaries

* feat: add phase 3 web diagnostic summaries

* fix(review-feedback-1445): Retry diagnostics fetch instead of permanently short-circuiting

* fix(review-feedback-1445): 解决冲突并确认 CI 仍为 success

* fix(review-feedback-1445): Persist diagnostics after notification dispatch

* docs(run-diagnostics): Clarify LLM config compatibility boundary for Phase 2

* fix: resolve undefined variable and test timing issues in diagnostics

* fix(review-feedback-1445): 澄清并补齐验证

* fix(review-feedback-1445): 解决的 merge conflict

* fix(review-feedback-1445): 解决冲突，并补齐后端/API 变更说明与验证证据

* fix(review-feedback-1445): 解决冲突，并在冲突解决后重新确认受影响检查仍通过

* fix(review-feedback-1445): 澄清并补齐模型/provider/Base URL/运行时配置迁移相关证据，避免与 PR 风险说明不一致

* fix(review-feedback-1445): 解决冲突，并在冲突解决后确认关键 Web 与后端诊断路径仍通过验证

* fix(review-feedback-1445): Scope channel diagnostics to stocks actually notified

* fix(review-feedback-1445): Count source-context delivery as notification success and update

* fix(review-feedback-1445): 解决冲突后再合入
---

## 8a23124 - feat: add #1391 Phase 2 run diagnostic summaries (#1444)

**作者**: mumu | **日期**: 2026-05-26 | **PR**: #
**类型**: 

* fix(issue-1412): [bug]-stock_list格式问题

* fix(review-feedback-1413): preserve exchange hint for dotted A-share inputs

* fix(review-feedback-1413): Keep normalized A-share codes usable by market routing and preserve

* fix(review-feedback-1413): Limit raw dotted codes to fetchers that can parse them

* fix(review-feedback-1413): Keep Tushare daily input normalized for ETF detection

* fix(review-feedback-1413): 澄清结构化检测中的外部模型/API 与运行时配置迁移风险

* fix(review-feedback-1413): 处理或明确确认该失败与本 PR 无关且已有维护者豁免依据

* fix: keep stock list input as bare codes

* docs: add phase-0 run diagnostics contract

* fix(review-feedback-1435): 修正描述并澄清/补齐运行时代码变更的验证证据

* fix(review-feedback-1435): 补齐前缀提示识别，并增加对应回归测试

* fix(review-feedback-1435): 修正

* fix(review-feedback-1435): 解决冲突并更新描述/验证记录后再合入

* fix(review-feedback-1435): 解决冲突，并在最终 head 上重新确认 python -m pytest tests/test a share fetcher code

* fix(review-feedback-1435): 修复并补齐回归覆盖后再复核最终 head

* fix(review-feedback-1435): data provider/baostock fetcher.py 的 convert stock code 只从 .SH/.SS/.SZ

* fix: preserve A-share exchange hints

* fix(review-feedback-1435): 修正 docs/run-diagnostics-p0.md 对 Tushare 本轮范围的矛盾描述

* feat: add phase 1 run diagnostics trace plumbing

* feat: add phase 2 run diagnostic summaries

* fix(review-feedback-1441): 打通 trace id 与数据源运行快照，改动目标明确

* fix(review-feedback-1444): 修复 Agent 模式新报告通过历史诊断 API 返回 unknown 的正确性问题

* fix(review-feedback-1444): Propagate diagnostics lookup errors instead of masking them

* fix(review-feedback-1444): 补对应回归断言

* fix(review-feedback-1444): 解决冲突后再合入

* fix(review-feedback-1444): 解决冲突

* fix(review-feedback-1444): 解决冲突

* fix(review-feedback-1444): 解决

* fix(review-feedback-1444): 解决

* fix(review-feedback-1444): 解决冲突

* fix(review-feedback-1444): 解决

* fix(review-feedback-1444): 解决

* fix(review-feedback-1444): 解决冲突后再合入

* fix(review-feedback-1444): 解决冲突后再合入

* fix(review-feedback-1444): 解决冲突后再合入

* fix(review-feedback-1444): 解决冲突

* fix(review-feedback-1444): Derive news diagnostics from retrieval evidence

* fix(review-feedback-1444): 解决冲突后再合入

* fix(review-feedback-1444): 解决冲突并基于解决后的最终 diff 重新确认 docs/CHANGELOG.md、诊断链路和测试结果

* fix(review-feedback-1444): 解决冲突

* fix(review-feedback-1444): 解决冲突后再合入

* fix(review-feedback-1444): 解决冲突并重新跑阻断型 CI，尤其是 backend-gate 和相关诊断/API/history 回归

* fix(review-feedback-1444): preserve report timestamp when enriching task results

* fix: address run diagnostics review feedback

* fix: redact diagnostic copy text secrets

* fix(review-feedback-1444): 补一条多渠道部分失败的回归测试
---

## 4610dcb - fix: 补齐 Web 设置页中文文案映射并本地下拉选项翻译 (#1453)

**作者**: Copilot | **日期**: 2026-05-25 | **PR**: #
**类型**: 

* Initial plan

* fix: 补齐 Web 设置页中文文案映射并本地下拉选项翻译

Agent-Logs-Url: https://github.com/ZhuLinsen/daily_stock_analysis/sessions/727bf34a-aba1-484e-a33b-49b3cf2ba46c

Co-authored-by: massif-01 <176381099+massif-01@users.noreply.github.com>

* fix: align settings select translations

---------

Co-authored-by: copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>
Co-authored-by: massif-01 <176381099+massif-01@users.noreply.github.com>
Co-authored-by: Alfred <massif0601@gmail.com>
Co-authored-by: ZhuLinsen <zhuls97@163.com>
---

## e0e5fa6 - feat: add #1391 Phase 1 run diagnostics trace plumbing (#1441)

**作者**: mumu | **日期**: 2026-05-25 | **PR**: #
**类型**: 

* fix(issue-1412): [bug]-stock_list格式问题

* fix(review-feedback-1413): preserve exchange hint for dotted A-share inputs

* fix(review-feedback-1413): Keep normalized A-share codes usable by market routing and preserve

* fix(review-feedback-1413): Limit raw dotted codes to fetchers that can parse them

* fix(review-feedback-1413): Keep Tushare daily input normalized for ETF detection

* fix(review-feedback-1413): 澄清结构化检测中的外部模型/API 与运行时配置迁移风险

* fix(review-feedback-1413): 处理或明确确认该失败与本 PR 无关且已有维护者豁免依据

* fix: keep stock list input as bare codes

* docs: add phase-0 run diagnostics contract

* fix(review-feedback-1435): 修正描述并澄清/补齐运行时代码变更的验证证据

* fix(review-feedback-1435): 补齐前缀提示识别，并增加对应回归测试

* fix(review-feedback-1435): 修正

* fix(review-feedback-1435): 解决冲突并更新描述/验证记录后再合入

* fix(review-feedback-1435): 解决冲突，并在最终 head 上重新确认 python -m pytest tests/test a share fetcher code

* fix(review-feedback-1435): 修复并补齐回归覆盖后再复核最终 head

* fix(review-feedback-1435): data provider/baostock fetcher.py 的 convert stock code 只从 .SH/.SS/.SZ

* fix: preserve A-share exchange hints

* fix(review-feedback-1435): 修正 docs/run-diagnostics-p0.md 对 Tushare 本轮范围的矛盾描述

* feat: add phase 1 run diagnostics trace plumbing

* fix(review-feedback-1441): 打通 trace id 与数据源运行快照，改动目标明确
---

## 09afbf5 - fix: add #1391 Phase 0 diagnostics and A-share code guards (#1435)

**作者**: mumu | **日期**: 2026-05-25 | **PR**: #
**类型**: 

* fix(issue-1412): [bug]-stock_list格式问题

* fix(review-feedback-1413): preserve exchange hint for dotted A-share inputs

* fix(review-feedback-1413): Keep normalized A-share codes usable by market routing and preserve

* fix(review-feedback-1413): Limit raw dotted codes to fetchers that can parse them

* fix(review-feedback-1413): Keep Tushare daily input normalized for ETF detection

* fix(review-feedback-1413): 澄清结构化检测中的外部模型/API 与运行时配置迁移风险

* fix(review-feedback-1413): 处理或明确确认该失败与本 PR 无关且已有维护者豁免依据

* fix: keep stock list input as bare codes

* docs: add phase-0 run diagnostics contract

* fix(review-feedback-1435): 修正描述并澄清/补齐运行时代码变更的验证证据

* fix(review-feedback-1435): 补齐前缀提示识别，并增加对应回归测试

* fix(review-feedback-1435): 修正

* fix(review-feedback-1435): 解决冲突并更新描述/验证记录后再合入

* fix(review-feedback-1435): 解决冲突，并在最终 head 上重新确认 python -m pytest tests/test a share fetcher code

* fix(review-feedback-1435): 修复并补齐回归覆盖后再复核最终 head

* fix(review-feedback-1435): data provider/baostock fetcher.py 的 convert stock code 只从 .SH/.SS/.SZ

* fix: preserve A-share exchange hints

* fix(review-feedback-1435): 修正 docs/run-diagnostics-p0.md 对 Tushare 本轮范围的矛盾描述
---

## fcfcd3a - fix: 修复问股和首页进行中状态残留 (#1461)

**作者**: Alfred | **日期**: 2026-05-25 | **PR**: #
**类型**: 

* fix: clear stale active task state

* fix: guard active task pruning against stale snapshots

---------

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## 3aa26ba - feat: add visible chat context compression (#1460)

**作者**: Alfred | **日期**: 2026-05-25 | **PR**: #
**类型**: 

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## 1c049bc - feat: add analysis context pack schema (#1449)

**作者**: Alfred | **日期**: 2026-05-25 | **PR**: #
**类型**: 


---

## 79b2840 - feat: inject market phase prompt context (#1442)

**作者**: Alfred | **日期**: 2026-05-25 | **PR**: #
**类型**: 


---

## 43d05b4 - feat: Enhance A-share stock name correction and index generation (#1462)

**作者**: LouisHong | **日期**: 2026-05-25 | **PR**: #
**类型**: 

- Improved `fetch_tushare_stock_list.py` to support A-share name corrections for stocks with prefixes XD/XR/DR/N/C using the `--a-rk` option.
- Updated documentation to reflect the new functionality and usage of the correction script.
- Added a new script `refresh_stock_index.py` to automate the fetching of stock lists and index generation.
- Implemented tests for the new features, ensuring the correct functionality of stock name corrections and index generation.
- Enhanced error handling for missing dependencies and improved user feedback during execution.
---

## 639796f - fix: restore board linkage for compatible history snapshots (#1416)

**作者**: zbl-96 | **日期**: 2026-05-24 | **PR**: #
**类型**: 

* fix: restore board linkage from compatible snapshots

* chore: drop local review artifact from pr

* fix: enrich in-memory status board details

* fix: merge partial fundamental snapshots

* fix: preserve fallback fields on empty snapshots

---------

Co-authored-by: ZhuLinsen <zhuls97@163.com>
---

## a77bea5 - fix: 修复桌面端自动更新静默安装 (#1415)

**作者**: mumu | **日期**: 2026-05-24 | **PR**: #
**类型**: 

* fix: make desktop auto-update install silent

* fix(review-feedback-1415): Keep backend reference until process exit is confirmed

* fix(review-feedback-1415): 修复或确认失败原因后再合入

* fix(review-feedback-1415): 澄清或修复

* fix: handle quoted desktop uninstall path

* fix(review-feedback-1415): Pass ?= argument without quotes in retry uninstall call
---

## 33da885 - fix: preserve macOS desktop runtime config (#1432)

**作者**: mumu | **日期**: 2026-05-24 | **PR**: #
**类型**: 


---

## a3c627c - feat: add runtime market phase context plumbing (#1434)

**作者**: Alfred | **日期**: 2026-05-24 | **PR**: #
**类型**: 

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## 212f44c - docs: inventory analysis context boundaries (#1433)

**作者**: Alfred | **日期**: 2026-05-24 | **PR**: #
**类型**: 


---

## c452e7f - docs: complete alert center P8 documentation (#1430)

**作者**: Alfred | **日期**: 2026-05-23 | **PR**: #
**类型**: 


---

## ba47491 - chore: lazy load report markdown drawer #1411 PR-2 (#1425)

**作者**: Alfred | **日期**: 2026-05-23 | **PR**: #
**类型**: 

* chore: lazy load report markdown drawer

* fix: retry report markdown drawer chunk load

---------

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## f98b727 - feat: add market phase inference baseline (#1424)

**作者**: Alfred | **日期**: 2026-05-23 | **PR**: #
**类型**: 

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## bdb9883 - feat: add P7 market light alerts (#1419)

**作者**: Alfred | **日期**: 2026-05-23 | **PR**: #
**类型**: 

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## 8777439 - fix: stock_list格式问题 (#1412) (#1413)

**作者**: mumu | **日期**: 2026-05-23 | **PR**: #
**类型**: 


---

## 210db32 - chore: stabilize web vendor chunks (#1418)

**作者**: Alfred | **日期**: 2026-05-23 | **PR**: #
**类型**: 


---

## e8305ba - fix(issue-1399): [bug]-docker-挂载-.env-文件时-os.replace()-更新 (#1401)

**作者**: mumu | **日期**: 2026-05-22 | **PR**: #
**类型**: 


---

## 2c26203 - fix: normalize Tencent realtime volume (#1409)

**作者**: vinvcn | **日期**: 2026-05-22 | **PR**: #
**类型**: 

* fix: normalize Tencent realtime volume

* fix: harden Tencent realtime normalization

* docs: localize Tencent realtime comments

---------

Co-authored-by: mumu <42829555+ZhuLinsen@users.noreply.github.com>
---

## 964d4ca - chore: split web route bundles (#1410)

**作者**: Alfred | **日期**: 2026-05-22 | **PR**: #
**类型**: 


---

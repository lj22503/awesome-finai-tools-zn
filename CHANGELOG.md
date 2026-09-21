# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.4.0] - 2026-09-21

### Added

- 机构 Skill 矩阵新增 3 家券商（21 → 24 家）：
  - 中国银河证券：「星耀数智」系列 5 个 Skill（金融数据 / 技术面指标 56 项 / 基本面指标 90 项 / 因子分析 / 公告搜索），上架腾讯 SkillHub；PB「启睿」策略中心 MCP/Skill
  - 国投证券：智能选股 / 行情数据 / 基金对比 / 行业拥挤度 四大 Skills，官网 Skills 中心 + 腾讯 SkillHub 双通道
  - 东吴证券：东吴秀财 GPT（券业首个自研并备案的证券垂类大模型）/ 量化投研 Skills / 东吴之声 / 智能「小水滴」/ 千问智能体 / 秀捷
- 新增 `sources` 字段与「🔗 权威信源（可点击直达）」章节：14 家机构补齐公开佐证信源，全部逐一校验可访问（官方页面 + 财联社 / 央广网 / 中国经济网 / 中国金融信息网 / 21 财经等），README 渲染为可点击链接，`llms.txt` 同步输出绝对链接清单
- 机构动态新增 4 条变化与「趋势四：券商 Skill 供给开始分层」

### Changed

- 中信建投：Skill 由 2 个增至 5 个，补录「蜻蜓 Skill 广场」首发三大技能（ETF 筛选 / 个股研判 / 财报透视），获取方式由「未以独立 Skill 包发布」修正为「手机号注册领 API Key 轻量部署」
- `scripts/generate_readme.py` 新增 `generate_institution_sources()` / `generate_institution_sources_plain()` 两个渲染函数，信源表进入 README 与 `llms.txt` 生成链路

---

## [0.3.0] - 2026-09-21

### Added

- 新增 16 个工具（39 → 55），覆盖行情、因子、交易、投研、舆情五类：
  - Market Data：`mcp-eastmoney`（东方财富免 Key MCP）、`Wudao A-Share MCP`（63 工具远程 MCP）、`cn-financial-mcp`、`akshare-one-mcp`、`AxData`、同花顺官方 `Financial-API`、`FQGate-agent`、`easy-stock`
  - Analysis：`QuantaAlpha`（LLM 因子演化）、`QuantGPT`（WorldQuant BRAIN Alpha 工厂）、`tradex-hub`（129 MCP 工具集线器）、`Awesome Finance Skills`（Agent Skills 合集）
  - Trading：`TradingAgents-Astock`、`WyckoffTradingAgent`
  - Research：`AI Berkshire`（价值投资多智能体）
  - Sentiment：`TrendRadar`（全网热点舆情 + MCP）
- 新增 `data/institution-dynamics.json`：机构 Skill 动态数据源（变化摘要 + 趋势评论 + 开发者启示）
- README 新增「机构 Skill 动态」章节、「搜索关键词」段（工具类型 / 金融场景 / 应用平台 / 具体需求 / 机构品牌）
- `scripts/generate_readme.py` 升级为 README + `llms.txt` 唯一生成入口，支持机构矩阵与机构动态数据驱动渲染

### Changed

- 机构矩阵更新为 21 家：广发证券补 WorkBuddy / 扣子，国泰海通补千问，中金公司补千问并新增「点睛 AI 双引擎（分析师 Skill + MCP）」，易方达基金补千问
- 新增 4 家机构（17 → 21 家）：
  - 兴业证券（券商）：兴证智达 Skill Hub 技能中台 / 八大投资者 Skills 上架腾讯 SkillHub / 千问「智能投资助手」/ 优理宝「知己管家」/ 员工助手「AI 老铁」
  - 腾讯（平台）：WorkBuddy 金融版，2026-09-03 发布，80+ 金融专属专家与专家团，已服务中金公司、国投证券等 100+ 机构
  - 阿里巴巴（平台）：千问开放平台首批 12 个金融智能体，兴业证券、国泰海通、中金财富、易方达等入驻
  - 蚂蚁数科（平台）：Agentar 金融智能体平台 + 支小宝金融场景能力
- `llms.txt` 同步重建：分类表、机构矩阵、SERP 命中词段
- README 工具详情新增费用说明、官网与安装命令字段渲染

### Fixed

- 机构矩阵「接入平台」列改为分平台去重，消除重复平台串

---

## [0.2.0] - 2026-07-15

### Added

- 周更 China platforms scanner（commit `f9401d7`）：自动巡检 ClawHub + 中国本土 AI 平台新增工具
- GitHub Actions workflow：每周自动执行 `scripts/update_china_platforms.py`

### Changed

- 仓库清理（commit `8603af5`）：untrack `output/` + 非核心 data 文件，更新 `.gitignore`

### Fixed

- README 搜索关键词密度（commit `c586bbd`）
- README SEO keywords section + badge URL（commit `c667f40`）

---

## [0.1.0] - 2026-06-25

### Added

- 初始版本收录 39 个金融 AI 工具
- 覆盖 5 大分类：market_data / sentiment / analysis / trading / research
- `data/tools.json` 结构化数据（机器可读）
- `SKILL.md` agent 技能定义
- GitHub Actions 每周巡检脚本
- `AGENTS.md` / `CONTRIBUTING.md` / `LICENSE`

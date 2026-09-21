# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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

- 机构矩阵更新为 20 家：广发证券补 WorkBuddy / 扣子，国泰海通补千问，中金公司补千问并新增「点睛 AI 双引擎（分析师 Skill + MCP）」，易方达基金补千问
- 新增 3 家平台型主体并统一归类为「平台」：蚂蚁数科（Agentar 金融智能体平台 + 支小宝）、腾讯（WorkBuddy 金融版，80+ 金融专家，服务中金公司 / 国投证券等 100+ 机构）、阿里巴巴（千问开放平台首批 12 个金融智能体，兴业证券 / 国泰海通 / 中金财富 / 易方达等入驻）
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

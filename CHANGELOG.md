# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.4.5] - 2026-09-22

### Changed

- `scripts/review_candidates.py` 质检口径调整（阈值集中在脚本顶部常量，便于持续微调）：
  - **移除 npm 周下载量校验**：原 `MIN_WEEKLY_DOWNLOADS = 10` 过于苛刻，一批小众但可用的金融数据包被误判为 WARN；npm 端现只保留「包存在性 / deprecated / 最近发布时间 / 查重」四项判定
  - **GitHub 星数门槛由 10 提高到 100**（`MIN_STARS_WARN = 100`）：低于 100 星仍判 WARN 交人工判断，不直接 REJECT；判定依据文案同步写明门槛值
- `data/candidate-review-2026-09-22.md` / `.json`：按新口径重新全量检测，结论由 PASS 180 / WARN 24 / REJECT 0 变为 **PASS 192 / WARN 12 / REJECT 0**
  - WARN 构成：GitHub 5 条（星数不足 100，当前 81 / 32 / 17 / 10 / 6）；npm 7 条（停更，xueqiu-api 1581 天、futu 系 1603 天、tushare 系 386 天等）

---

## [0.4.4] - 2026-09-22

### Fixed

- **ClawHub 候选链接格式错误**（109 条 items + 7 条疑似机构候选此前全部 404 死链）：详情页真实格式为 `https://clawhub.ai/{ownerHandle}/skills/{slug}`，旧代码统一拼成 `https://clawhub.ai/{slug}`，导致这批候选在质量检测中整体判为 REJECT
  - `scripts/update_china_platforms.py` 新增 `clawhub_link()` 统一收敛链接生成：优先取接口返回的 `canonicalUrl`，其次用 `ownerHandle` + `slug` 拼接，两者都取不到时回退站点首页，从源头杜绝再次写入死链；两处链接生成点改为调用该函数
  - `downloads` 兼容 search 接口顶层字段与 `v1/skills` 的 `stats.downloads` 两种返回形态（此前 ClawHub 候选下载量恒为 0）

### Added

- `scripts/review_candidates.py`：**入库前质量检测**（只读，不改动任何正式数据）。用法 `python scripts/review_candidates.py --scope {items,github,npm,institution,all} --json`，产出 `data/candidate-review-YYYY-MM-DD.md` 与 `.json`，按 PASS / WARN / REJECT 三档给结论：
  - 平台技能候选：详情页可达性（404 → REJECT）、与正式清单查重、描述完整性
  - GitHub 候选：仓库存在性与 archived / disabled 状态、星标、license、最近推送时间
  - npm 候选：包存在性与 deprecated 状态、周下载量、最近发布时间、查重
  - 机构技能候选：机构是否已建档、skill 是否重复、描述完整性、链接可达性
- `scripts/fix_clawhub_links.py`：存量 ClawHub 链接修复工具（`--apply` 写盘），按 slug 经 search 接口反查 `canonicalUrl` / `ownerHandle` 就地重写 link，并顺带回填下载量

### Changed

- `data/pending-review.json`：109 条 items 与 7 条疑似机构候选的链接全部重建为可访问详情页并回填下载量（本次修复 116 条，0 失败）

---

## [0.4.3] - 2026-09-22

### Fixed

- `scripts/update_tools.py` **重写三个数据源**（此前实际全部失效，周更长期空转）：
  - GitHub 检索原用 `gh api search/repositories -q "关键词"`（误把查询串当 jq 表达式），改为 **GitHub Search API 直连**（`requests`），不再依赖 `gh` CLI
  - npm 巡检原按 `{"objects": [...]}` 解包，新版 npm 返回数组导致 `'list' object has no attribute 'get'`；改为兼容两种返回形态，并改用 **npm Registry Search API**
  - PyPI 段原为 `pip index versions <包名>`（只能查版本号，无法发现新工具），已移除；Python 生态候选改由 GitHub 搜索的 `language:python` 维度覆盖

### Added

- `scripts/update_tools.py` 新增**待审隔离**：巡检结果写入 `data/pending-review.json` 的 `github_candidates` / `npm_candidates`（与国内平台巡检共用同一待审池），不再直写 `data/tools.json`
- 过滤规则升级：金融信号 + 工具形态双重判定、黑名单排除（教程 / 摄影 / 卡片等）、GitHub 星标门槛 5、npm 空壳包剔除、自引用仓库排除
- 候选新增 `scope` 字段（`cn` / `global`），便于按站点定位人工筛选

### Changed

- 周报结构重写：新增巡检概览、待审池累计、处置说明

---

## [0.4.2] - 2026-09-22

### Added

- `scripts/update_china_platforms.py` 新增**待审隔离机制**：自动巡检发现的候选不再直接写入 `data/tools.json`，统一写入新增的 `data/pending-review.json`（`status: pending_review`），经人工确认后再并入正式数据，避免未经审核的条目污染线上清单

### Changed

- `scripts/update_china_platforms.py` **收紧相关性过滤**：新增 `IRRELEVANT_BLOCKLIST` / `is_relevant()` / `has_institution_signal()` / `ORG_STOPWORDS` / `GENERIC_FINANCE_WORDS`；ClawHub 与 npm 抓取结果需同时命中「金融 + 机构」双重信号才收录
- `scripts/update_china_platforms.py` 收敛 `_infer_org_name`：疑似新机构名由伪名（如「提供基金」「数据来源证券」）收敛为合理机构名
- `scripts/generate_readme.py` 统计口径调整：README / llms.txt 仅统计正式分类条目，`pending_review` 条目不参与生成

---

## [0.4.1] - 2026-09-21

### Fixed

- **全站链接有效性修复**（88 条链接逐一实测）：
  - 2 处真死链替换：国信证券 `weixin.guosen.com.cn`（TLS 旧重协商被禁，无法握手）→ 腾讯 SkillHub「国信证券」企业主页；FIN-SKILLS（财跃星辰）`https://fin-skills.finstep.cn`（HTTPS 不可达）→ 站内标注仅支持 HTTP 并改用 `http://` 可访问地址
  - 13 处被 `…` 截断的 URL 全部还原为完整可点击链接（国信 / 同花顺 Financial-API / 多个 GitHub 仓库地址等）
  - 8 处非 URL 占位文本（如「中金点睛平台」「华泰证券App」）不再渲染成 markdown 链接，改为纯文本或替换为实测可开官方入口：中金财富 `www.ciccwm.com`、华泰 `www.htsc.com.cn`、广发 `hd.gf.com.cn/gfwskill2026/`、盈米 `www.yingmi.cn`、天天基金 `www.1234567.com.cn`、兴业 `www.xyzq.com.cn`、东方财富 `mcp-eastmoney` → 阿里云百炼
- 国泰海通：移除失效占位官网，详情页补「平台入口」千问 / 华为小艺可点击链接
- shields.io 中文徽章 404（`数据更新` badge not found）：徽章文案改为 URL 编码（`%E5%B7%A5%E5%85%B7` / `%E6%95%B0%E6%8D%AE%E6%9B%B4%E6%96%B0`），恢复 200
- Wudao A-Share MCP 的 MCP 端点（仅接受 POST，GET 返回 405）不再渲染为可点击链接，改为行内代码展示，保留可开的 setup 页面链接

### Changed

- `scripts/generate_readme.py` 新增链接安全渲染：`is_url()` / `link_or_text()` / `linkify_urls()` / `trunc_safe()`，截断逻辑改为「按原子 token 截断」，确保 markdown 链接与 URL 永不被截断；表格内 URL 自动转为短标签可点击链接

---

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

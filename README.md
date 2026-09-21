# Awesome FinAI Tools
### 中国金融 AI 工具全景图

[![Stars](https://img.shields.io/github/stars/lj22503/awesome-finai-tools-zn?style=flat-square)](https://github.com/lj22503/awesome-finai-tools-zn)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)
[![Tools](https://img.shields.io/badge/工具-55-blue?style=flat-square)](#工具分类)
[![更新](https://img.shields.io/badge/数据更新-2026-09-21-brightgreen?style=flat-square)](#每周自动更新)

> 本仓库收录**中国金融 AI 工具**，包括 **Market Data MCP**、**量化框架**、**券商 Skills**、**金融 CLI**、**Python 金融库**。覆盖 **A股 / 港股 / 基金 / 期货** 行情数据、量化回测、因子挖掘、舆情分析、投研等场景。支持 **OpenClaw / Claude / Cursor / Codex / WorkBuddy / Coze** 等 AI Agent 平台。每周自动巡检更新。

[📋 完整工具清单](#工具分类) · [🔍 工具详情](#工具详情) · [🚀 快速上手](#快速上手) · [🤖 Agent 接入](#agent-接入) · [🏢 机构 Skill 矩阵](#-机构-skill-矩阵) · [📝 贡献指南](./CONTRIBUTING.md) · [📄 llms.txt](./llms.txt)

---

## 🔍 搜索关键词

> 本页可被以下搜索词命中（AI Agent / 搜索引擎 / GitHub 站内搜索）

**工具类型**：`CLI` `MCP` `Skill` `Python` `框架` `API` `MCP Server` `Python金融库` `量化框架`

**金融场景**：`A股行情` `实时行情` `历史K线` `资金流向` `龙虎榜` `北向资金` `涨停梯队` `量化回测` `因子挖掘` `Alpha因子` `舆情监控` `基金分析` `研报解读` `多Agent投研` `选股筛选` `财报分析`

**应用平台**：`OpenClaw` `Claude` `Cursor` `Codex` `WorkBuddy` `Coze` `Dify` `豆包` `千问` `华为小艺` `IMA` `ChatGPT`

**具体需求**：`查股票` `安装MCP` `免费行情数据` `Python量化` `量化策略` `券商Skill` `MCP Server 推荐` `A股数据源对比`

**机构/品牌**：`东方财富` `同花顺` `华泰` `中金` `广发` `国信` `国泰海通` `兴业证券` `雪球` `Wind` `Tushare` `AKShare` `BaoStock` `腾讯` `阿里` `蚂蚁`

---

## 🔥 精选推荐（新手首选）

| 场景 | 推荐工具 | 理由 |
|------|---------|------|
| **零配置查行情** | `opencli eastmoney quote` | 安装即用，秒出结果 |
| **同花顺官方数据** | `Financial-API` | 官方 MCP/API/CLI，覆盖行情/财报/涨停 |
| **多维度 A 股数据（MCP）** | `ashare-mcp` | 30 个 tool，akshare 主源 + 多源降级 |
| **免费历史 K 线** | `baostock` | 1990 年至今，无需注册 |
| **零鉴权 A 股中台** | `TradeX Hub` | 129 个 MCP 工具，多源自动降级 |
| **量化策略回测** | `qtrade` | 15 种策略 + 完整回测引擎 |
| **多 Agent 投研** | `TradingAgents-astock` | 7 位分析师 A 股规则辩论 |
| **LLM 因子挖掘** | `QuantaAlpha` | LLM + 进化策略自动演化 Alpha |
| **舆情监控** | `TrendRadar` | 多平台热点聚合 + 多渠道推送 + MCP |
| **基金深度分析** | `盈米 MCP` | 69 个 MCP 工具，组合回测 |

---

## 工具分类

### 📊 Market Data（行情数据）

*实时行情、历史 K 线、资金流向、龙虎榜、北向资金、板块与财务快照*

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [OpenCLI EastMoney Quote](#opencli-eastmoney-quote) | CLI | ✅ | 实时行情查询（A股/港股/美股），含PE/市值/换手率/涨跌停状态 | `npm install -g @jackwener/opencli` |
| [OpenCLI EastMoney Money Flow](#opencli-eastmoney-money-flow) | CLI | ✅ | 主力资金净流入排行（今日/5日/10日），支持主超/大/中/小单拆分 | `npm install -g @jackwener/opencli` |
| [OpenCLI EastMoney Sectors](#opencli-eastmoney-sectors) | CLI | ✅ | 板块排行（行业/概念/地域），按涨跌幅/主力资金/成交额排序 | `npm install -g @jackwener/opencli` |
| [OpenCLI EastMoney Northbound](#opencli-eastmoney-northbound) | CLI | ✅ | 北向资金（沪深港通）逐分钟实时净流入数据 | `npm install -g @jackwener/opencli` |
| [OpenCLI EastMoney Longhu](#opencli-eastmoney-longhu) | CLI | ✅ | 龙虎榜明细（营业部/机构席位），含买入卖出金额/股票代码/上榜原因 | `npm install -g @jackwener/opencli` |
| [OpenCLI EastMoney Hot Rank](#opencli-eastmoney-hot-rank) | CLI | ✅ | 东方财富人气排行榜（热度/关注度），反映散户关注度 | `npm install -g @jackwener/opencli` |
| [OpenCLI THS Hot Rank](#opencli-ths-hot-rank) | CLI | ✅ | 同花顺热门股票排行 | `npm install -g @jackwener/opencli` |
| [OpenCLI Yahoo Finance](#opencli-yahoo-finance) | CLI | ✅ | Yahoo Finance 美股行情 | `npm install -g @jackwener/opencli` |
| [ashare-mcp](#ashare-mcp) | MCP | ✅ | 生产级中国A股 MCP server，30个tool，akshare主源+baostock/tushare降级… | `cd ashare-mcp && uv sync && uv run ashare-m…` |
| [stock-data-mcp](#stock-data-mcp) | MCP | ✅ | 43个tool覆盖A股/港股/美股/加密货币，多源自动故障转移，pip安装 | `pip install stock-data-mcp && stock-data-mcp` |
| [china-stock-mcp](#china-stock-mcp) | MCP | ✅ | A股市场研究用 MCP server | `pip install china-stock-mcp && china-stock-…` |
| [astock-mcp-server](#astock-mcp-server) | MCP | ✅ | A股实时报价/K线/市场扫描/选股，BaoStock + Sina 零API key | `pip install astock-mcp-server && astock-mcp…` |
| [BaoStock](#baostock) | Python | ✅ | 免费开源A股数据平台，无需注册，历史K线/财务数据/宏观数据/板块成分股，1990年至今 | `pip install baostock` |
| [AKShare](#akshare) | Python | ✅ | 东方财富/新浪/腾讯等数据源聚合，实时行情/期货/期权/债券/基金/宏观，覆盖广但数据归属各来源方 | `pip install akshare` |
| [Tushare Pro](#tushare-pro) | Python | ⚠️ | 高质量A股数据，财务/指数/套利/港股，数据质量较高但需要积分 | `pip install tushare` |
| [Wind API](#wind-api) | API | 💰 | 机构级金融数据，A股/债券/基金/宏观/衍生品全覆盖，机构标配，数据最全最准 | `Wind Terminal安装后自带Python接口 import WindPy` |
| [东方财富 Choice](#东方财富-choice) | API | 💰 | 东方财富金融数据终端，A股/期货/期权/基金/宏观，Python API，机构级数据 | `安装 Choice 终端后通过 Python API 调用` |
| [同花顺 iFinD](#同花顺-ifind) | API | 💰 | 同花顺投研数据，财报/估值/行业/宏观，Python API | `—` |
| [广发证券 Skill](#广发证券-skill) | Skill | ❓ | 广发证券官方技能，8大核心功能：股票基础信息、财务对比、龙虎榜追踪、基金定投计算、ETF资金异动监测与筛选、基… | `在 ima 客户端搜索「广发证券」` |
| [国信证券 Skill](#国信证券-skill) | Skill | ❓ | 国信证券「小信智慧助手」官方技能，6大核心功能：智能选股、ETF筛选、基金对比、宏观/行情/财务数据查询 | `https://weixin.guosen.com.cn/gs/xxskills/#a…` |
| [天天基金 Skill](#天天基金-skill) | Skill | ⚠️ | 天天基金App官方技能群，14个核心技能：基金信息查询、自选管理；第三方深度整合：天工「Fund Analyz… | `天天基金App` |
| [mcp-eastmoney](#mcp-eastmoney) | MCP | ✅ | 东方财富 MCP 服务器，A股实时行情 + 主力资金 + 板块 + K线，使用官方公开延时接口，免 API K… | `uvx mcp-eastmoney` |
| [Wudao A-Share MCP](#wudao-a-share-mcp) | MCP | ⚠️ | 63 个只读工具，覆盖 A股 K线/分时、指数 ETF 可转债、涨停梯队、板块轮动、资金流、龙虎榜、研报、公告… | `https://stock.quicktiny.cn/api/mcp/setup` |
| [cn-financial-mcp](#cn-financial-mcp) | MCP | ✅ | cn 金融数据 MCP 服务器，工具包覆盖 A股行情、财报、估值、板块、市场全景、新闻及宏观指标 | `git clone https://github.com/ccq1/cn-financ…` |
| [akshare-one-mcp](#akshare-one-mcp) | MCP | ✅ | 基于 akshare-one 的中国股票市场数据 MCP Server，MIT 开源，支持 Smithery … | `npx -y @smithery/cli install @zwldarren/aks…` |
| [AxData](#axdata) | 框架 | ✅ | 开源量化数据库框架，覆盖通达信、巨潮、腾讯财经、新浪财经、东方财富、财联社、开盘红等公开源接口，提供 Pyth… | `pip install axdata` |
| [同花顺官方 Financial-API](#同花顺官方-financial-api) | API | ⚠️ | 同花顺（HiThink）官方 A股金融数据服务，提供股票实时行情、历史行情、财务报表、指数、板块、涨停等数据，… | `https://github.com/HiThink-Tech/Financial-A…` |
| [FQGate-agent](#fqgate-agent) | MCP | ✅ | 同花顺免费开源 AI 插件，为 Codex / Claude Code / WorkBuddy / OpenC… | `powershell.exe -NoProfile -ExecutionPolicy …` |
| [easy-stock](#easy-stock) | 框架 | ✅ | 面向个人投资者的本地股票分析工具，自动抓取并整理行情、财务指标与技术形态，生成可视化看板 | `git clone https://github.com/jundizhou/easy…` |

### 💬 Sentiment（舆情/社区）

*雪球、同花顺、全平台热点聚合与舆情监控*

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [OpenCLI Xueqiu Search](#opencli-xueqiu-search) | CLI | ✅ | 雪球股票搜索（代码或中文名称），返回实时价格/涨跌幅/雪球主页 | `npm install -g @jackwener/opencli` |
| [OpenCLI Xueqiu Hot Posts](#opencli-xueqiu-hot-posts) | CLI | ✅ | 雪球热门帖子，反映投资者社区讨论热点 | `npm install -g @jackwener/opencli` |
| [TrendRadar](#trendradar) | 框架 | ✅ | 全网热点与舆情监控工具，聚合多平台热搜榜单，支持关键词热度趋势与 MCP 接入，可用于市场情绪与事件驱动监测 | `git clone https://github.com/sansan0/TrendR…` |

### 📈 Analysis（分析与因子）

*Alpha 因子挖掘、量化分析、技术指标、选股筛选*

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [FinanceMCP-Alpha](#financemcp-alpha) | MCP | ⚠️ | WorldQuant 101 Alpha 因子计算，TypeScript，基于Tushare，输出Alpha3… | `npm install finance-mcp-alpha && npm start` |
| [Qlib](#qlib) | 框架 | ✅ | 微软AI量化投资平台，支持自动因子挖掘/机器学习/回测，数据结构专为量化设计 | `pip install pyqlib` |
| [QuantaAlpha](#quantaalpha) | 框架 | ✅ | LLM + 进化策略自动挖掘、演化与验证量化 Alpha 因子，只需描述研究方向即可自动完成因子发现与自演化轨… | `git clone https://github.com/QuantaAlpha/Qu…` |
| [QuantGPT](#quantgpt) | 框架 | ✅ | Agent 驱动的 Alpha 工厂：LLM 自主设计、回测并提交因子到 WorldQuant BRAIN，支… | `git clone https://github.com/Miasyster/Quan…` |
| [tradex-hub](#tradex-hub) | MCP | ✅ | 面向量化与投研的 MCP 工具集线器，聚合 129 个 MCP 工具，统一接入数据、因子、回测与交易相关能力 | `git clone https://github.com/wolfjkd/tradex…` |
| [Awesome Finance Skills](#awesome-finance-skills) | Skill | ✅ | 金融领域 Agent Skills 合集，以标准 Skill 形式封装财报分析、估值建模、行业研究等能力，一条… | `npx skills add RKiding/Awesome-finance-skil…` |

### 🔄 Trading（交易执行）

*量化策略回测、模拟交易、实盘接口、交易智能体*

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [QTrade](#qtrade) | Skill | ✅ | A股量化交易框架，15种内置策略，支持数据获取/策略回测/参数优化/实盘模拟/风控/可视化完整工作流。Pull… | `git clone && pip install -r requirements.txt` |
| [VeighNa](#veighna) | 框架 | ✅ | 开源量化交易框架，事件驱动架构，支持数据管理/策略回测/实盘交易/风控，可对接多家券商 | `pip install vnpy` |
| [FinRL](#finrl) | 框架 | ✅ | 深度强化学习量化交易框架，支持DDPG/PPO/SAC等算法，对接OpenAI Gym | `pip install finrl` |
| [华泰 AI 涨乐](#华泰-ai-涨乐) | Skill | ⚠️ | 华泰证券官方技能，深度集成于华泰App，五大核心功能：金融分析与资讯、行情检索、A股模拟交易、条件选股、自选股… | `在 OpenClaw 搜索「华泰AI涨乐」一键部署` |
| [TradingAgents-Astock](#tradingagents-astock) | 框架 | ✅ | 基于 TradingAgents 的多智能体 A股分析框架，集成 8 大维度 A股数据源（技术面/资金面/基本… | `git clone https://github.com/simonlin1212/T…` |
| [WyckoffTradingAgent](#wyckofftradingagent) | 框架 | ✅ | 威科夫（Wyckoff）方法量化交易 Agent，自动识别吸筹/派发阶段、量价结构并给出结构买卖点信号 | `git clone https://github.com/YoungCan-Wang/…` |

### 🔬 Research（投研）

*研报解读、宏观数据、基金分析、多 Agent 投研、券商官方 Skill*

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [TradingAgents](#tradingagents) | 框架 | ✅ | 多Agent LLM量化投研框架，分析师团队（基本面/舆情/技术面/新闻）+ 交易员 + 风控，多模型支持（G… | `pip install tradingagents` |
| [同花顺问财 SkillHub](#同花顺问财-skillhub) | Skill | ⚠️ | 同花顺官方技能市场，股基债期全品类数据查询与分析（选股、诊断、财经搜索、产业链），上百个社区技能（DCF估值/… | `在 OpenClaw 或对应 AI 平台搜索「同花顺问财」安装` |
| [东方财富 ClawBot](#东方财富-clawbot) | Skill | ✅ | 东方财富数字员工，金融数据查询、智能选股、个股/基金诊断、财报解读、宏观研究 | `阿里云平台搜索「东方财富ClawBot」` |
| [中金公司 Skill（中金点睛）](#中金公司-skill中金点睛) | Skill | 💰 | 中金公司「中金点睛」平台，覆盖计算机、策略、宏观、新能源等领域首席分析师专属Skill，面向机构投资者提供研投… | `中金点睛平台` |
| [国泰海通 灵犀 Skills](#国泰海通-灵犀-skills) | Skill | ❓ | 国泰海通证券「灵犀」官方技能群，查研报、查行情、查数据、出榜单、筛股票、自选股管理 | `国泰海通自有平台` |
| [盈米基金 MCP](#盈米基金-mcp) | MCP | 💰 | 盈米基金AI开放平台，69个标准化MCP工具 + 16项核心技能组件，涵盖金融数据、投研服务（组合回测、蒙特卡… | `通过盈米AI开放平台获取 MCP 接入` |
| [兴业证券 知己管家 & 投研Agent](#兴业证券-知己管家-投研agent) | Skill | ❓ | 兴业证券「优理宝」App内置C端「知己管家」（一句话交易/智能诊断/资讯总结）+ B端 investor-ha… | `兴业证券优理宝App` |
| [FIN-SKILLS（财跃星辰）](#fin-skills财跃星辰) | Skill | ❓ | 第三方金融技能市场，上架 finstep-mcp（金融数据）、龙虎榜解读、个股异动解读、基金分析、A股日报生成… | `访问 fin-skills.finstep.cn 查看接入文档` |
| [FinClaw（上财AIFinLab）](#finclaw上财aifinlab) | 框架 | ✅ | 上海财经大学AIFinLab开源项目，超1000个自研Skills，按银行/证券/保险/基金/期货/信托六大行… | `git clone https://github.com/aifinlab/FinCl…` |
| [AI Berkshire](#ai-berkshire) | 框架 | ✅ | 以巴菲特/芒格价值投资框架为核心的多智能体研究系统，覆盖商业模式、护城河、管理层、估值与能力圈判断，自动产出长… | `git clone https://github.com/xbtlin/ai-berk…` |

### 📰 News（新闻资讯）

*财经新闻、公告、快讯*

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [OpenCLI SinaFinance](#opencli-sinafinance) | CLI | ✅ | 新浪财经新闻/滚动资讯/个股新闻 | `npm install -g @jackwener/opencli` |


---

## 工具详情


#### 📊 Market Data（行情数据）

### OpenCLI EastMoney Quote

**类型**：CLI　|　**费用**：✅ 免费  
**GitHub**：[github.com/jackwener/opencli](https://github.com/jackwener/opencli)  
**维护方**：jackwener  

实时行情查询（A股/港股/美股），含PE/市值/换手率/涨跌停状态

**输入**：stock_codes=必需，股票代码，支持 sh600000/sz000001/hk00700/usAAPL 等格式，多个用逗号分隔  
**输出字段**：price / changePercent / change / open / high / low / prevClose / volume / turnover / turnoverRate  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### OpenCLI EastMoney Money Flow

**类型**：CLI　|　**费用**：✅ 免费  
**GitHub**：[github.com/jackwener/opencli](https://github.com/jackwener/opencli)  

主力资金净流入排行（今日/5日/10日），支持主超/大/中/小单拆分

**输入**：range=可选，周期：today / 5d / 10d，默认 today / order=可选，排序：desc（净流入）/ asc（净流出），默认 desc / limit=可选，返回数量，默认20，max 100  
**输出字段**：rank / code / name / price / changePercent / mainNet / mainNetRatio / superNet / bigNet / mediumNet  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### OpenCLI EastMoney Sectors

**类型**：CLI　|　**费用**：✅ 免费  

板块排行（行业/概念/地域），按涨跌幅/主力资金/成交额排序

**输入**：type=可选，板块类型：industry（行业）/ concept（概念）/ region（地域），默认 industry / sort=可选，排序：change（涨跌幅）/ drop（跌幅）/ money-flow（主力净流入）/ out-flow（净流出）/ turnover（成交额），默认 change / limit=可选，默认20，max 100  
**输出字段**：rank / code / name / price / changePercent / mainNet / leadStock / leadChangePercent / upCount / downCount  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### OpenCLI EastMoney Northbound

**类型**：CLI　|　**费用**：✅ 免费  

北向资金（沪深港通）逐分钟实时净流入数据

**输出字段**：time / minuteNetYi / cumulativeNetYi / totalNetYi  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### OpenCLI EastMoney Longhu

**类型**：CLI　|　**费用**：✅ 免费  

龙虎榜明细（营业部/机构席位），含买入卖出金额/股票代码/上榜原因

**输入**：date=可选，查询日期，格式 YYYY-MM-DD，默认前一交易日  
**输出字段**：tradeDate / code / name / closePrice / changeRate / buyAmt / sellAmt / netAmt / reason  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### OpenCLI EastMoney Hot Rank

**类型**：CLI　|　**费用**：✅ 免费  

东方财富人气排行榜（热度/关注度），反映散户关注度

**输出字段**：rank / symbol / name / price / changePercent / heat  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### OpenCLI THS Hot Rank

**类型**：CLI　|　**费用**：✅ 免费  

同花顺热门股票排行

**输出字段**：rank / symbol / name / price / changePercent  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### OpenCLI Yahoo Finance

**类型**：CLI　|　**费用**：✅ 免费  

Yahoo Finance 美股行情

**输入**：symbol=必需，美股代码，如 AAPL、MSFT  
**输出字段**：symbol / price / change / changePercent / open / high / low / volume / marketCap  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### ashare-mcp

**类型**：MCP　|　**费用**：✅ 免费  
**GitHub**：[github.com/CharmYue/ashare-mcp](https://github.com/CharmYue/ashare-mcp)  
**维护方**：CharmYue  

生产级中国A股 MCP server，30个tool，akshare主源+baostock/tushare降级，实时行情/K线/资金流/龙虎榜/两融/财报/涨停池/筹码分布

**输入**：tool_name=按工具不同，见 README tools 清单 / stock_code=支持 600519 / sh600519 / 600519.SH 等多种格式  
**输出格式**：JSON via MCP protocol  
**接入方式**：stdio 或 Streamable HTTP  

**安装**：
```bash
cd ashare-mcp && uv sync && uv run ashare-mcp
```

---

### stock-data-mcp

**类型**：MCP　|　**费用**：✅ 免费  
**GitHub**：[github.com/openstockdata/stock-data-mcp](https://github.com/openstockdata/stock-data-mcp)  
**维护方**：openstockdata  

43个tool覆盖A股/港股/美股/加密货币，多源自动故障转移，pip安装

**输入**：tool_name=按工具不同 / symbols=股票代码  
**输出格式**：JSON via MCP protocol  
**接入方式**：stdio 或 HTTP  

**安装**：
```bash
pip install stock-data-mcp && stock-data-mcp
```

---

### china-stock-mcp

**类型**：MCP　|　**费用**：✅ 免费  
**GitHub**：[github.com/wax0629/china-stock-mcp](https://github.com/wax0629/china-stock-mcp)  
**维护方**：wax0629  

A股市场研究用 MCP server

**输出格式**：JSON via MCP protocol  
**接入方式**：stdio  

**安装**：
```bash
pip install china-stock-mcp && china-stock-mcp
```

---

### astock-mcp-server

**类型**：MCP　|　**费用**：✅ 免费  
**GitHub**：[github.com/jiangyj545/astock-mcp-server](https://github.com/jiangyj545/astock-mcp-server)  
**维护方**：jiangyj545  

A股实时报价/K线/市场扫描/选股，BaoStock + Sina 零API key

**输入**：stock_code=股票代码  
**输出格式**：JSON via MCP protocol  
**接入方式**：stdio  

**安装**：
```bash
pip install astock-mcp-server && astock-mcp-server
```

---

### BaoStock

**类型**：Python　|　**费用**：✅ 免费  
**地址**：[https://baostock.com](https://baostock.com)  
**维护方**：BaoStock Team  

免费开源A股数据平台，无需注册，历史K线/财务数据/宏观数据/板块成分股，1990年至今

**输入**：stock_code=必需，格式 sh.600000 / sz.000001 / start_date=起始日期 / end_date=结束日期 / frequency=可选，d(日)/w(周)/m(月)/5(5分钟)/15/30/60  
**输出字段**：date / code / open / high / low / close / volume / amount  
**输出格式**：Python DataFrame  
**接入方式**：pip install baostock  

**安装**：
```bash
pip install baostock
```

---

### AKShare

**类型**：Python　|　**费用**：✅ 免费  
**地址**：[https://akshare.akfamily.xyz](https://akshare.akfamily.xyz)  
**维护方**：AKFamily  

东方财富/新浪/腾讯等数据源聚合，实时行情/期货/期权/债券/基金/宏观，覆盖广但数据归属各来源方

**输入**：function_name=akshare提供300+接口，如 akshare.stock_zh_a_spot_em() / symbol=按接口不同  
**输出格式**：Python DataFrame / JSON  
**接入方式**：pip install akshare  

**安装**：
```bash
pip install akshare
```

---

### Tushare Pro

**类型**：Python　|　**费用**：⚠️ 免费增值  
**地址**：[https://tushare.pro](https://tushare.pro)  
**维护方**：Tushare  

高质量A股数据，财务/指数/套利/港股，数据质量较高但需要积分

**输入**：api_name=Tushare接口名 / params=参数字典 / fields=返回字段  
**输出格式**：Python DataFrame  
**接入方式**：pip install tushare  

**安装**：
```bash
pip install tushare
```

---

### Wind API

**类型**：API　|　**费用**：💰 付费  
**地址**：[https://www.wind.com.cn](https://www.wind.com.cn)  
**维护方**：万得信息  

机构级金融数据，A股/债券/基金/宏观/衍生品全覆盖，机构标配，数据最全最准

**输入**：wind_code=Wind金融终端代码，如 600519.SH / fields=需获取的指标  
**输出格式**：Python/Java/C++ API 返回  
**接入方式**：Wind Terminal / Python API (WindPy)  

**安装**：
```bash
Wind Terminal安装后自带Python接口 import WindPy
```

---

### 东方财富 Choice

**类型**：API　|　**费用**：💰 付费  
**地址**：[https://choice.eastmoney.com](https://choice.eastmoney.com)  
**维护方**：东方财富  

东方财富金融数据终端，A股/期货/期权/基金/宏观，Python API，机构级数据

**输入**：code=股票/债券/基金代码 / type=数据类型  
**输出格式**：Python API 返回  
**接入方式**：Choice客户端 + Python API  

**安装**：
```bash
安装 Choice 终端后通过 Python API 调用
```

---

### 同花顺 iFinD

**类型**：API　|　**费用**：💰 付费  
**地址**：[https://www.10jqka.com.cn](https://www.10jqka.com.cn)  
**维护方**：同花顺  

同花顺投研数据，财报/估值/行业/宏观，Python API

**输入**：code=证券代码 / report_type=报告类型  
**输出格式**：Python API 返回  
**接入方式**：Python API  

---

### 广发证券 Skill

**类型**：Skill　|　**费用**：❓ 未知  
**地址**：[hd.gf.com.cn/gfwskill2026/#/index](hd.gf.com.cn/gfwskill2026/#/index)  
**维护方**：广发证券  

广发证券官方技能，8大核心功能：股票基础信息、财务对比、龙虎榜追踪、基金定投计算、ETF资金异动监测与筛选、基金产品信息查询、ETF实时榜单

**输入**：intent=股票信息 / 财务对比 / 龙虎榜 / 基金 / ETF  
**输出覆盖**：股票基础信息 / 财务对比 / 龙虎榜 / 基金定投 / ETF监测 / ETF榜单  
**输出格式**：数据表格 + 榜单  
**接入方式**：官方平台 hd.gf.com.cn 或 腾讯ima Skill广场  

**安装**：
```bash
在 ima 客户端搜索「广发证券」
```

---

### 国信证券 Skill

**类型**：Skill　|　**费用**：❓ 未知  
**地址**：[https://weixin.guosen.com.cn/gs/xxskills/#architecture](https://weixin.guosen.com.cn/gs/xxskills/#architecture)  
**维护方**：国信证券  

国信证券「小信智慧助手」官方技能，6大核心功能：智能选股、ETF筛选、基金对比、宏观/行情/财务数据查询

**输入**：intent=选股 / ETF / 基金 / 宏观 / 行情 / 财务  
**输出覆盖**：智能选股 / ETF筛选 / 基金对比 / 宏观数据 / 行情查询 / 财务数据  
**输出格式**：数据表格 + 榜单  
**接入方式**：官方平台「小信智慧助手」/ 小艺Claw / Coze平台  

**接入**：[https://weixin.guosen.com.cn/gs/xxskills/#architecture](https://weixin.guosen.com.cn/gs/xxskills/#architecture)

---

### 天天基金 Skill

**类型**：Skill　|　**费用**：⚠️ 免费部分  
**地址**：[天天基金App](天天基金App)  
**维护方**：东方财富（天天基金）  

天天基金App官方技能群，14个核心技能：基金信息查询、自选管理；第三方深度整合：天工「Fund Analyzer Pro」提供基金深度诊断、比较、持仓分析

**输入**：intent=基金信息 / 自选 / 持仓分析 / 基金比较  
**输出覆盖**：基金信息查询 / 自选管理 / 深度诊断 / 基金比较 / 持仓分析  
**输出格式**：基金数据 / 诊断报告 / 持仓分析  
**接入方式**：天天基金App官方 / 天工平台第三方  

**接入**：[天天基金App](天天基金App)

---

### mcp-eastmoney

**类型**：MCP　|　**费用**：✅ 免费  
**GitHub**：[github.com/27dream/mcp-eastmoney](https://github.com/27dream/mcp-eastmoney)  
**维护方**：27dream  

东方财富 MCP 服务器，A股实时行情 + 主力资金 + 板块 + K线，使用官方公开延时接口，免 API Key 开箱即用

**输入**：intent=A股行情 / 资金流 / 板块 / K线查询 / stock_code=可选，如 600519  
**输出覆盖**：实时行情 / 主力资金 / 板块数据 / K线  
**输出格式**：MCP tool 结构化返回  
**接入方式**：MCP（stdio），Claude Code / Cursor / Codex 等客户端  

**安装**：
```bash
uvx mcp-eastmoney
```

---

### Wudao A-Share MCP

**类型**：MCP　|　**费用**：⚠️ 免费额度  
**费用说明**：Developer Console 注册领取 API Key，免费额度以官方说明为准  
**GitHub**：[github.com/jcdreamjc/wudao-mcp](https://github.com/jcdreamjc/wudao-mcp)  
**官网**：[https://data.quicktiny.cn/](https://data.quicktiny.cn/)  
**维护方**：QuickTiny / Wudao Data  

63 个只读工具，覆盖 A股 K线/分时、指数 ETF 可转债、涨停梯队、板块轮动、资金流、龙虎榜、研报、公告、估值快照与盘后复盘

**输入**：intent=A股盘后复盘 / 涨停梯队 / 板块轮动 / 资金流研究 / stock_code=可选  
**输出覆盖**：K线 / 涨停梯队 / 资金流 / 龙虎榜 / 研报 / 公告 / 复盘  
**输出格式**：远程 HTTP MCP（以 tools/list 为准）  
**接入方式**：远程 HTTP MCP（https://stock.quicktiny.cn/api/mcp），需在 Developer Console 申请 API Key  

**接入**：[https://stock.quicktiny.cn/api/mcp/setup](https://stock.quicktiny.cn/api/mcp/setup)

---

### cn-financial-mcp

**类型**：MCP　|　**费用**：✅ 免费  
**GitHub**：[github.com/ccq1/cn-financial-mcp](https://github.com/ccq1/cn-financial-mcp)  
**维护方**：ccq1  

cn 金融数据 MCP 服务器，工具包覆盖 A股行情、财报、估值、板块、市场全景、新闻及宏观指标

**输入**：intent=A股行情 / 财报 / 估值 / 板块 / 宏观指标 / stock_code=可选，如 600519  
**输出覆盖**：行情 / 财报 / 估值 / 板块 / 市场全景 / 新闻 / 宏观  
**输出格式**：MCP tool 结构化返回  
**接入方式**：MCP（stdio / HTTP），Apache-2.0 开源可自建  

**安装**：
```bash
git clone https://github.com/ccq1/cn-financial-mcp && pip install -e .
```

---

### akshare-one-mcp

**类型**：MCP　|　**费用**：✅ 免费  
**GitHub**：[github.com/zwldarren/akshare-one-mcp](https://github.com/zwldarren/akshare-one-mcp)  
**维护方**：zwldarren  

基于 akshare-one 的中国股票市场数据 MCP Server，MIT 开源，支持 Smithery / uvx 一键安装

**输入**：intent=A股行情与基础数据查询 / stock_code=可选  
**输出覆盖**：行情 / K线 / 基础数据  
**输出格式**：MCP tool 结构化返回  
**接入方式**：MCP，支持 Smithery CLI / uvx  

**安装**：
```bash
npx -y @smithery/cli install @zwldarren/akshare-one-mcp --client claude
```

---

### AxData

**类型**：框架　|　**费用**：✅ 免费  
**费用说明**：AxData Research-Only License，面向个人学习与非商业研究，商用需另行授权  
**GitHub**：[github.com/electkismet/AxData](https://github.com/electkismet/AxData)  
**维护方**：electkismet  

开源量化数据库框架，覆盖通达信、巨潮、腾讯财经、新浪财经、东方财富、财联社、开盘红等公开源接口，提供 Python SDK、CLI 与本地 API 服务

**输入**：intent=多公开源行情/财务数据批量入库与查询 / stock_code=可选  
**输出覆盖**：通达信 / 巨潮 / 腾讯财经 / 新浪财经 / 东方财富 / 财联社 / 开盘红  
**输出格式**：本地数据库 + Python SDK / REST API  
**接入方式**：pip 安装 SDK，或完整项目安装启用 Web 控制台与本地 API  

**安装**：
```bash
pip install axdata
```

---

### 同花顺官方 Financial-API

**类型**：API　|　**费用**：⚠️ 免费额度  
**费用说明**：官网申请 API Key，免费额度与计费以官方说明为准  
**GitHub**：[github.com/HiThink-Tech/Financial-API](https://github.com/HiThink-Tech/Financial-API)  
**维护方**：同花顺 HiThink（官方维护）  

同花顺（HiThink）官方 A股金融数据服务，提供股票实时行情、历史行情、财务报表、指数、板块、涨停等数据，支持 API / MCP / CLI / Python 四种接入方式

**输入**：intent=A股行情 / 财务报表 / 指数 / 板块 / 涨停数据 / stock_code=可选  
**输出覆盖**：实时行情 / 历史行情 / 财务报表 / 指数 / 板块 / 涨停  
**输出格式**：API / MCP / CLI / Python SDK  
**接入方式**：API / MCP / CLI / Python，需在官方平台申请 Key  

**接入**：[https://github.com/HiThink-Tech/Financial-API](https://github.com/HiThink-Tech/Financial-API)

---

### FQGate-agent

**类型**：MCP　|　**费用**：✅ 免费  
**费用说明**：插件入口 AGPL-3.0 完全免费；FQGate 网关主程序单独提供编译包。1.0.0 起不再提供交易 API 与交易工具  
**GitHub**：[github.com/fqgate/FQGate-agent](https://github.com/fqgate/FQGate-agent)  
**官网**：[https://github.com/zhuyifang/tonghuasun-agent](https://github.com/zhuyifang/tonghuasun-agent)  
**维护方**：独立开发者（非同花顺官方）  

同花顺免费开源 AI 插件，为 Codex / Claude Code / WorkBuddy / OpenClaw / 豆包 / 千问提供本机 A股实时行情、分时、K线、Level-2 逐笔、资讯公告与证券资料

**输入**：intent=本机 A股行情 / 分时 / K线 / Level-2 / 资讯查询 / stock_code=可选  
**输出覆盖**：实时行情 / 分时 / K线 / Level-2 / 资讯公告 / 证券资料  
**输出格式**：本机网关 + AI 插件工具列表  
**接入方式**：安装 FQGate 本机网关 + 对应 AI 工具插件（Windows），无需订阅或试用额度  

**安装**：
```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./installer/runtime/install-fqgate.ps1
```

---

### easy-stock

**类型**：框架　|　**费用**：✅ 免费  
**费用说明**：非商业许可证，禁止商业用途  
**GitHub**：[github.com/jundizhou/easy-stock](https://github.com/jundizhou/easy-stock)  
**维护方**：jundizhou  

面向个人投资者的本地股票分析工具，自动抓取并整理行情、财务指标与技术形态，生成可视化看板

**输入**：intent=个人视角的持仓跟踪与个股看板 / stock_code=可选  
**输出覆盖**：行情 / 财务指标 / 技术形态  
**输出格式**：本地可视化看板 + 数据表  
**接入方式**：本地部署，Python 环境  

**安装**：
```bash
git clone https://github.com/jundizhou/easy-stock && pip install -r requirements.txt
```

---


#### 💬 Sentiment（舆情/社区）

### OpenCLI Xueqiu Search

**类型**：CLI　|　**费用**：✅ 免费  

雪球股票搜索（代码或中文名称），返回实时价格/涨跌幅/雪球主页

**输入**：query=必需，搜索关键词，如 茅台、AAPL、腾讯  
**输出字段**：symbol / name / exchange / price / changePercent / url  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### OpenCLI Xueqiu Hot Posts

**类型**：CLI　|　**费用**：✅ 免费  

雪球热门帖子，反映投资者社区讨论热点

**输入**：limit=可选，默认10  
**输出字段**：id / title / text / author / likes / url  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---

### TrendRadar

**类型**：框架　|　**费用**：✅ 免费  
**费用说明**：GPL-3.0 开源  
**GitHub**：[github.com/sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)  
**维护方**：sansan0  

全网热点与舆情监控工具，聚合多平台热搜榜单，支持关键词热度趋势与 MCP 接入，可用于市场情绪与事件驱动监测

**输入**：intent=全网热点/舆情监控与关键词热度趋势 / keywords=关注的关键词列表  
**输出覆盖**：多平台热搜 / 关键词趋势 / 舆情预警  
**输出格式**：热榜聚合 + 趋势分析 + 定时推送（含 MCP 接口）  
**接入方式**：本地 / 服务器部署，支持 MCP 接入 AI 客户端  

**安装**：
```bash
git clone https://github.com/sansan0/TrendRadar && pip install -r requirements.txt
```

---


#### 📈 Analysis（分析与因子）

### FinanceMCP-Alpha

**类型**：MCP　|　**费用**：⚠️ 免费额度  
**GitHub**：[github.com/guangxiangdebizi/FinanceMCP-Alpha](https://github.com/guangxiangdebizi/FinanceMCP-Alpha)  
**维护方**：guangxiangdebizi  

WorldQuant 101 Alpha 因子计算，TypeScript，基于Tushare，输出Alpha3/13/15/16/44/50/55因子值及分位数信号

**输入**：stock_code=必需，格式 000001.SZ / 600000.SH / start_date=必需，格式 YYYYMMDD / end_date=必需，格式 YYYYMMDD / factors=必需数组，如 ["Alpha3","Alpha13","Alpha50"]  
**输出格式**：Markdown 报告，含因子值/分位数/买卖信号  
**接入方式**：npm / Streamable HTTP  

**安装**：
```bash
npm install finance-mcp-alpha && npm start
```

---

### Qlib

**类型**：框架　|　**费用**：✅ 免费  
**GitHub**：[github.com/microsoft/qlib](https://github.com/microsoft/qlib)  
**维护方**：Microsoft  

微软AI量化投资平台，支持自动因子挖掘/机器学习/回测，数据结构专为量化设计

**输入**：stock_code=股票代码 / start_date=起始日期 / end_date=结束日期 / factor_type=因子类型  
**输出格式**：因子值/预测信号/回测结果  
**接入方式**：pip install pyqlib  

**安装**：
```bash
pip install pyqlib
```

---

### QuantaAlpha

**类型**：框架　|　**费用**：✅ 免费  
**费用说明**：仓库未标注开源许可证，商用前请先确认授权  
**GitHub**：[github.com/QuantaAlpha/QuantaAlpha](https://github.com/QuantaAlpha/QuantaAlpha)  
**维护方**：QuantaAlpha  

LLM + 进化策略自动挖掘、演化与验证量化 Alpha 因子，只需描述研究方向即可自动完成因子发现与自演化轨迹验证

**输入**：intent=按研究方向自动挖掘与验证 Alpha 因子 / research_direction=自然语言描述  
**输出覆盖**：因子挖掘 / 因子演化 / 因子验证 / 回测  
**输出格式**：因子表达式 + 回测报告  
**接入方式**：本地安装，Python 环境  

**安装**：
```bash
git clone https://github.com/QuantaAlpha/QuantaAlpha && SETUPTOOLS_SCM_PRETEND_VERSION=0.1.0 pip install -e .
```

---

### QuantGPT

**类型**：框架　|　**费用**：✅ 免费  
**费用说明**：MIT 开源；需自备 DeepSeek API Key（官方说明约 $0.001 / 次查询）  
**GitHub**：[github.com/Miasyster/QuantGPT](https://github.com/Miasyster/QuantGPT)  
**维护方**：Miasyster  

Agent 驱动的 Alpha 工厂：LLM 自主设计、回测并提交因子到 WorldQuant BRAIN，支持 HTTP 传输与前端控制台

**输入**：intent=自动设计并提交 WorldQuant BRAIN 因子 / api_key=DeepSeek API Key（写入 .env）  
**输出覆盖**：因子设计 / 因子回测 / BRAIN 提交  
**输出格式**：因子提案 + 回测结果 + MCP / HTTP 服务  
**接入方式**：本地安装（Python + 前端），HTTP 传输：python -m quantgpt --transport http  

**安装**：
```bash
git clone https://github.com/Miasyster/QuantGPT && pip install -e .
```

---

### tradex-hub

**类型**：MCP　|　**费用**：✅ 免费  
**费用说明**：各子工具许可证以仓库说明为准  
**GitHub**：[github.com/wolfjkd/tradex-hub](https://github.com/wolfjkd/tradex-hub)  
**维护方**：wolfjkd  

面向量化与投研的 MCP 工具集线器，聚合 129 个 MCP 工具，统一接入数据、因子、回测与交易相关能力

**输入**：intent=一站式接入量化/投研类 MCP 工具 / tool_name=按 hub 目录选择  
**输出覆盖**：数据 / 因子 / 回测 / 交易辅助  
**输出格式**：MCP 工具集合（129 个）  
**接入方式**：MCP 接入，本地部署  

**安装**：
```bash
git clone https://github.com/wolfjkd/tradex-hub
```

---

### Awesome Finance Skills

**类型**：Skill　|　**费用**：✅ 免费  
**费用说明**：Apache-2.0 开源  
**GitHub**：[github.com/RKiding/Awesome-finance-skills](https://github.com/RKiding/Awesome-finance-skills)  
**维护方**：RKiding  

金融领域 Agent Skills 合集，以标准 Skill 形式封装财报分析、估值建模、行业研究等能力，一条 npx 命令即可安装到 Claude Code 等客户端

**输入**：intent=为 AI 客户端快速装配金融分析 Skill 能力 / skill_name=按需选择  
**输出覆盖**：财报分析 / 估值建模 / 行业研究  
**输出格式**：Agent Skills 包（可组合调用）  
**接入方式**：npx skills 安装到 Claude Code / 兼容客户端  

**安装**：
```bash
npx skills add RKiding/Awesome-finance-skills
```

---


#### 🔄 Trading（交易执行）

### QTrade

**类型**：Skill　|　**费用**：✅ 免费  
**GitHub**：[github.com/moyang11111/qtrade](https://github.com/moyang11111/qtrade)  
**维护方**：moyang11111  

A股量化交易框架，15种内置策略，支持数据获取/策略回测/参数优化/实盘模拟/风控/可视化完整工作流。Pullback20D 策略年化验证胜率42%

**输入**：symbols=可选，股票代码列表，默认监控7只主力信号股 / strategy=策略注册名，如 pullback_20d / dual_ma / bollinger / breakout 等 / start_date=回测起始日期 / end_date=回测结束日期  
**输出格式**：回测报告 / 模拟盘信号 / 优化结果  
**接入方式**：Python CLI  

**安装**：
```bash
git clone && pip install -r requirements.txt
```

---

### VeighNa

**类型**：框架　|　**费用**：✅ 免费  
**地址**：[https://www.vnpy.com](https://www.vnpy.com)  
**维护方**：VeighNa Team  

开源量化交易框架，事件驱动架构，支持数据管理/策略回测/实盘交易/风控，可对接多家券商

**输入**：strategy_code=用户编写的策略Python文件 / broker=券商接口（如 futu / ib / ctp）  
**输出格式**：回测报告 / 实盘成交记录 / 风控面板  
**接入方式**：pip install vnpy  

**安装**：
```bash
pip install vnpy
```

---

### FinRL

**类型**：框架　|　**费用**：✅ 免费  
**GitHub**：[github.com/AI4Finance-Foundation/FinRL](https://github.com/AI4Finance-Foundation/FinRL)  
**维护方**：AI4Finance  

深度强化学习量化交易框架，支持DDPG/PPO/SAC等算法，对接OpenAI Gym

**输入**：stock_env=市场环境配置 / algorithm=强化学习算法 / hyperparameters=超参数  
**输出格式**：训练好的交易Agent / 回测收益曲线  
**接入方式**：pip install finrl  

**安装**：
```bash
pip install finrl
```

---

### 华泰 AI 涨乐

**类型**：Skill　|　**费用**：⚠️ 限时免费  
**费用说明**：新用户每日500-1000次调用额度  
**地址**：[华泰证券App](华泰证券App)  
**维护方**：华泰证券  

华泰证券官方技能，深度集成于华泰App，五大核心功能：金融分析与资讯、行情检索、A股模拟交易、条件选股、自选股管理

**输入**：intent=行情 / 模拟交易 / 条件选股 / 自选股  
**输出覆盖**：金融资讯 / 行情检索 / A股模拟交易 / 条件选股 / 自选股管理  
**输出格式**：行情数据 / 交易信号 / 自选股管理  
**接入方式**：华泰证券App（集成）或一键部署至 OpenClaw  

**安装**：
```bash
在 OpenClaw 搜索「华泰AI涨乐」一键部署
```

---

### TradingAgents-Astock

**类型**：框架　|　**费用**：✅ 免费  
**费用说明**：Apache-2.0 开源；LLM 调用成本自付  
**GitHub**：[github.com/simonlin1212/TradingAgents-astock](https://github.com/simonlin1212/TradingAgents-astock)  
**维护方**：simonlin1212  

基于 TradingAgents 的多智能体 A股分析框架，集成 8 大维度 A股数据源（技术面/资金面/基本面/新闻/公告/龙虎榜等），输出中文买卖与仓位建议

**输入**：intent=多智能体协作的 A股个股投研与交易建议 / stock_code=股票代码，如 600519  
**输出覆盖**：技术面 / 资金面 / 基本面 / 新闻 / 公告 / 龙虎榜  
**输出格式**：中文投研报告 + 买卖/仓位建议  
**接入方式**：本地部署，需自备 LLM API Key（OpenAI / DeepSeek 等）  

**安装**：
```bash
git clone https://github.com/simonlin1212/TradingAgents-astock && pip install -r requirements.txt
```

---

### WyckoffTradingAgent

**类型**：框架　|　**费用**：✅ 免费  
**费用说明**：AGPL-3.0，注意网络服务场景的传染性条款  
**GitHub**：[github.com/YoungCan-Wang/WyckoffTradingAgent](https://github.com/YoungCan-Wang/WyckoffTradingAgent)  
**维护方**：YoungCan-Wang  

威科夫（Wyckoff）方法量化交易 Agent，自动识别吸筹/派发阶段、量价结构并给出结构买卖点信号

**输入**：intent=威科夫量价结构分析与交易信号 / stock_code=可选，A股/美股  
**输出覆盖**：吸筹阶段 / 派发阶段 / 量价结构 / 买卖点  
**输出格式**：阶段判定 + 结构信号 + 图表  
**接入方式**：本地部署，Python 环境  

**安装**：
```bash
git clone https://github.com/YoungCan-Wang/WyckoffTradingAgent && pip install -r requirements.txt
```

---


#### 🔬 Research（投研）

### TradingAgents

**类型**：框架　|　**费用**：✅ 免费  
**GitHub**：[github.com/TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)  
**维护方**：TauricResearch  

多Agent LLM量化投研框架，分析师团队（基本面/舆情/技术面/新闻）+ 交易员 + 风控，多模型支持（GPT-5/Gemini/Claude/DeepSeek）

**输入**：stock_code=目标股票代码 / task=research / sentiment / trade / backtest / model=可选，指定LLM后端  
**输出格式**：Markdown分析报告 / 交易信号 / 回测结果  
**接入方式**：pip install tradingagents  

**安装**：
```bash
pip install tradingagents
```

---

### 同花顺问财 SkillHub

**类型**：Skill　|　**费用**：⚠️ 免费部分  
**地址**：[https://www.iwencai.com/skillhub](https://www.iwencai.com/skillhub)  
**维护方**：同花顺  

同花顺官方技能市场，股基债期全品类数据查询与分析（选股、诊断、财经搜索、产业链），上百个社区技能（DCF估值/量化策略等）

**输入**：intent=选股 / 诊断 / 搜索 / 产业链分析  
**输出覆盖**：选股 / 个股诊断 / 财经搜索 / 产业链 / 基金/债券/期货数据  
**输出格式**：自然语言回答 + 数据表格  
**接入方式**：OpenClaw / Claude / ChatGPT / Cursor 等主流AI平台  

**安装**：
```bash
在 OpenClaw 或对应 AI 平台搜索「同花顺问财」安装
```

---

### 东方财富 ClawBot

**类型**：Skill　|　**费用**：✅ 免费  
**地址**：[阿里云平台](阿里云平台)  
**维护方**：东方财富  

东方财富数字员工，金融数据查询、智能选股、个股/基金诊断、财报解读、宏观研究

**输入**：intent=选股 / 诊断 / 财报解读 / 宏观  
**输出覆盖**：智能选股 / 个股诊断 / 基金诊断 / 财报解读 / 宏观研究  
**输出格式**：自然语言 + 数据  
**接入方式**：阿里云平台（搜索「东方财富ClawBot」）  

**接入**：[阿里云平台搜索「东方财富ClawBot」](阿里云平台搜索「东方财富ClawBot」)

---

### 中金公司 Skill（中金点睛）

**类型**：Skill　|　**费用**：💰 机构付费  
**费用说明**：面向机构付费用户  
**地址**：[中金点睛平台](中金点睛平台)  
**维护方**：中金公司  

中金公司「中金点睛」平台，覆盖计算机、策略、宏观、新能源等领域首席分析师专属Skill，面向机构投资者提供研投支持

**输入**：intent=行业研究 / 策略分析 / 宏观 / 新能源  
**输出覆盖**：计算机 / 策略 / 宏观 / 新能源 / 首席分析师观点  
**输出格式**：分析师研报 + 策略观点  
**接入方式**：注册登录「中金点睛」平台  

**接入**：[中金点睛平台](中金点睛平台)

---

### 国泰海通 灵犀 Skills

**类型**：Skill　|　**费用**：❓ 未知  
**地址**：[国泰海通平台](国泰海通平台)  
**维护方**：国泰海通证券  

国泰海通证券「灵犀」官方技能群，查研报、查行情、查数据、出榜单、筛股票、自选股管理

**输入**：intent=研报 / 行情 / 榜单 / 选股 / 自选股  
**输出覆盖**：查研报 / 查行情 / 查数据 / 出榜单 / 筛股票 / 自选股管理  
**输出格式**：研报摘要 / 行情数据 / 榜单  
**接入方式**：国泰海通自有平台  

**接入**：[国泰海通自有平台](国泰海通自有平台)

---

### 盈米基金 MCP

**类型**：MCP　|　**费用**：💰 联系销售  
**地址**：[盈米AI开放平台](盈米AI开放平台)  
**维护方**：盈米基金  

盈米基金AI开放平台，69个标准化MCP工具 + 16项核心技能组件，涵盖金融数据、投研服务（组合回测、蒙特卡洛模拟）、投顾内容与策略服务

**输入**：intent=基金分析 / 组合回测 / 蒙特卡洛模拟 / 投顾策略  
**输出覆盖**：金融数据 / 组合回测 / 蒙特卡洛模拟 / 投顾内容 / 策略服务  
**输出格式**：MCP JSON / 投顾报告  
**接入方式**：MCP 或 OpenAPI，兼容 Coze / Dify / Cursor 等平台  

**安装**：
```bash
通过盈米AI开放平台获取 MCP 接入
```

---

### 兴业证券 知己管家 & 投研Agent

**类型**：Skill　|　**费用**：❓ 未知  
**地址**：[兴业证券优理宝App](兴业证券优理宝App)  
**维护方**：兴业证券  

兴业证券「优理宝」App内置C端「知己管家」（一句话交易/智能诊断/资讯总结）+ B端 investor-harness 投研Agent（27个技能模块）

**输入**：intent=交易 / 诊断 / 资讯总结 / 投研  
**输出覆盖**：一句话交易 / 智能诊断 / 资讯总结 / 投研27模块  
**输出格式**：交易信号 / 诊断报告 / 资讯摘要  
**接入方式**：C端：优理宝App；B端：investor-harness 投研Agent  

**接入**：[兴业证券优理宝App](兴业证券优理宝App)

---

### FIN-SKILLS（财跃星辰）

**类型**：Skill　|　**费用**：❓ 未知  
**地址**：[https://fin-skills.finstep.cn](https://fin-skills.finstep.cn)  
**维护方**：财跃星辰  

第三方金融技能市场，上架 finstep-mcp（金融数据）、龙虎榜解读、个股异动解读、基金分析、A股日报生成等技能，面向开发者标准化接入

**输入**：intent=龙虎榜解读 / 个股异动 / 基金分析 / A股日报  
**输出覆盖**：龙虎榜解读 / 个股异动解读 / 基金分析 / A股日报生成  
**输出格式**：MCP JSON / 自然语言报告  
**接入方式**：安装CLI工具将技能市场接入自己的AI Agent  

**安装**：
```bash
访问 fin-skills.finstep.cn 查看接入文档
```

---

### FinClaw（上财AIFinLab）

**类型**：框架　|　**费用**：✅ 免费  
**GitHub**：[github.com/aifinlab/FinClaw](https://github.com/aifinlab/FinClaw)  
**维护方**：上财AIFinLab  

上海财经大学AIFinLab开源项目，超1000个自研Skills，按银行/证券/保险/基金/期货/信托六大行业划分，提供统一金融数据抽象层，原生兼容OpenClaw Agent OS

**输入**：intent=全行业金融数据 / 投研 / 六大行业覆盖 / stock_code=按需  
**输出覆盖**：银行 / 证券 / 保险 / 基金 / 期货 / 信托 / 投研  
**输出格式**：统一数据抽象层返回  
**接入方式**：本地安装或 Docker 容器化部署，原生兼容 OpenClaw  

**安装**：
```bash
git clone https://github.com/aifinlab/FinClaw
```

---

### AI Berkshire

**类型**：框架　|　**费用**：✅ 免费  
**费用说明**：MIT 开源；LLM 调用成本自付  
**GitHub**：[github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire)  
**维护方**：xbtlin  

以巴菲特/芒格价值投资框架为核心的多智能体研究系统，覆盖商业模式、护城河、管理层、估值与能力圈判断，自动产出长期价值研究报告

**输入**：intent=价值投资视角的公司深度研究与长期跟踪 / company=公司名称 / 代码  
**输出覆盖**：商业模式 / 护城河 / 管理层 / 估值 / 能力圈  
**输出格式**：多智能体协同的价值投资研报  
**接入方式**：本地部署，需自备 LLM API Key  

**安装**：
```bash
git clone https://github.com/xbtlin/ai-berkshire && pip install -r requirements.txt
```

---


#### 📰 News（新闻资讯）

### OpenCLI SinaFinance

**类型**：CLI　|　**费用**：✅ 免费  

新浪财经新闻/滚动资讯/个股新闻

**输出字段**：title / url / publishTime / source  
**接入方式**：直接运行  

**安装**：
```bash
npm install -g @jackwener/opencli
```

---


---

## 🚀 快速上手

### 方式一：直接使用 CLI（推荐零配置场景）

```bash
# 安装 OpenCLI
npm install -g @jackwener/opencli

# 查贵州茅台实时行情
opencli eastmoney quote 600519

# 查今日主力资金流向
opencli eastmoney money-flow --range 5d

# 查雪球讨论
opencli xueqiu search 茅台
```

### 方式二：使用 MCP（AI Agent 接入）

```bash
# mcp-eastmoney（免 API Key，推荐）
uvx mcp-eastmoney

# ashare-mcp
uv run ashare-mcp

# stock-data-mcp
pip install stock-data-mcp
```

### 方式三：使用 Python 库（开发者）

```bash
# 免费，无需注册
pip install baostock akshare

# 需要注册
pip install tushare
```

---

## 🤖 Agent 接入

加载 `SKILL.md` 后，agent 可根据用户需求自动推荐和安装对应工具：

```
用户："帮我分析一下A股今日资金流向"
Agent → 读取 SKILL.md → 推荐 ashare-mcp 或 opencli eastmoney money-flow
→ 识别工具 ID → 执行安装命令 → 返回结果
```

详见 [SKILL.md](./SKILL.md)

---

## 📡 每周自动更新

GitHub Actions 每周一 09:00 UTC 自动执行：

1. 巡检 GitHub trending（量化/金融类仓库）
2. 检查 npm / PyPI 新增金融类包
3. 检查 MCP 官方 registry 更新
4. 自动发 PR 更新 `data/tools.json`

手动触发：[workflow_dispatch](./.github/workflows/weekly-update.yml)

---

## 📝 贡献指南

欢迎提交新工具！详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

**收录标准**：
- ✅ 可实际运行（非空壳）
- ✅ 有清楚接入说明
- ✅ 非独占（通用工具优先）

**不收录**：
- ❌ 需要特定券商开户才能获取数据
- ❌ 无公开文档的黑盒工具

---

## 🏢 机构 Skill 矩阵

> 截至 2026-09-21，国内头部券商中已有半数以上落地 Skill 产品，金融数据商、基金公司与大厂 Agent 平台同步加速。以下为核心机构 Skill 矩阵：

| 机构 | 类型 | Skill 数量 | 核心能力 | 接入平台 | 获取方式 |
|------|------|-----------|---------|---------|---------|
| **广发证券** | 券商 | 8 个 | 股票简况信息 / 财务对比 / 沪深龙虎榜 / ETF筛选 | IMA / Coze / 华为小艺 / OpenClaw / WorkBuddy | API Key 注册 → 一键复制安装 |
| **东方财富** | 券商 | 7 个 | 综合诊基 / 综合诊股 / 金融数据 / 市场搜索 | IMA / Coze / 飞书 / OpenClaw | 财富号自带 API Key，无需额外配置 |
| **国泰海通** | 券商 | 6 个 | 研报搜索 / 实时行情 / 金融数据 / 市场热榜 | 华为小艺 / OpenClaw / ClawHub / 千问 | 君弘APP搜索「灵犀Skills」→ 领资格 → 一键复制安装 |
| **华泰证券** | 券商 | 5 个 | 金融分析与资讯查询 / 金融指标与行情综合检索 / A股模拟交易 / 条件选股 | 涨乐App / OpenClaw | AI涨乐App → 复制提示词&Key → 粘贴安装 |
| **中金公司** | 券商 | 6 个 | 行情数据 / 财务分析 / 热榜资讯 / 分析师「老于」数字分身 | 中金点睛 / OpenClaw / 千问 | 中金财富 Skills 中心注册 → 获取 API Key → 一键安装 |
| **国信证券** | 券商 | 6 个 | 智能选股 / ETF筛选 / 基金对比 / 宏观数据查询 | 小信助手 / OpenClaw / Coze | https://weixin.guosen.com.cn/gs/xxskill… |
| **中信建投** | 券商 | 2 个 | AI蜻蜓翼答 / 智研多资产配置 | 蜻蜓点金App / 机构端平台 | App内置，暂未以独立Skill包发布 |
| **广东博众** | 券商 | 3 个 | 股票智能分析 / 量化成长选股助手 / 股票情绪分析 | Coze / 万得 AIFin Market | Coze技能商店 / 万得AIFin Market |
| **万得 (Wind)** | 数据商 | 3 个 | WindClaw / AIFin Market / 万得 AI (Wind Alice) | 桌面端 / WorkBuddy / OpenClaw / Hermes Agent / 独立App +… | 下载安装 |
| **同花顺** | 数据商 | 2 个 | iFinD MCP / 问财 SkillHub | MCP协议 / OpenClaw / Claude / ChatGPT / Cursor | MCP协议接入 |
| **盈米基金** | 数据商 | 1 个 | 盈米MCP | MCP / Coze / Dify / Cursor | 联系盈米AI开放平台 |
| **易方达基金** | 基金 | 2 个 | ETF查询 / 场外指数基金查询 | WorkBuddy / OpenClaw / Hermes Agent / ArkClaw / 千问 | 微信小程序「指数直通车」→ AI Skills → 获取 API Key → … |
| **南方基金** | 基金 | 2 个 | AI梦 / 南南FUND搭子 | 南方基金App | App内置，未开放外部Skill |
| **天弘基金** | 基金 | 1 个 | FinAgent 金融智能体系统 | 内部系统 | 内部系统，未开放外部Skill |
| **中国平安** | 银行保险 | 1 个 | 智小安AI保险顾问 | 平安旗下App | 内部平台为主，未明确开放外部Skill |
| **招商银行** | 银行保险 | 1 个 | 「小助」系列智能体 | 内部使用 | 内部使用，未开放外部Skill |
| **工商银行** | 银行保险 | 1 个 | AI数字员工 | 内部使用 | 内部使用，未开放外部Skill |
| **蚂蚁数科** | 平台 | 2 个 | Agentar 金融智能体平台 / 支小宝金融场景能力 | Agentar / 百宝箱 / 支付宝 | 蚂蚁数科官网申请试用 / 企业对接 |
| **腾讯（WorkBuddy 金融版）** | 平台 | 2 个 | WorkBuddy 金融版专家智能体 / 金融专家团协同能力 | WorkBuddy | 腾讯 WorkBuddy 官网申请 / 企业对接 |
| **阿里巴巴（千问开放平台）** | 平台 | 2 个 | 千问金融智能体专区 / 机构智能体分发入口 | 千问 | 千问开放平台搜索机构名直接使用 |

> 📊 完整数据见 [data/institution-skills.json](./data/institution-skills.json)

## 📡 机构 Skill 动态

> 最近更新：**2026-09-21** | 来源：公开信息整理（2026-07 ~ 2026-09 巡检）

### 变化摘要

- 腾讯：WorkBuddy 金融版（2026-09-03）上线 80+ 金融专属专家与专家团，主打开放式 AI 智能工作台，已服务中金公司、国投证券等 100+ 家金融机构。
- 阿里巴巴：千问开放平台（2026-09-07）首批集中上线 12 个金融类智能体，兴业证券、国泰海通、中金财富、易方达基金等机构同步入驻。
- 广发证券：Skill 矩阵从 IMA / Coze / 华为小艺 / OpenClaw 扩展至 WorkBuddy、扣子等平台，接入面进一步铺开。
- 国泰海通：君弘「灵犀 Skills」在华为小艺 / OpenClaw 之外新增千问渠道，行情与研报能力多平台分发。
- 中金公司：推出「点睛 AI 双引擎」——分析师专属 Skill（投研框架与观点）与 MCP（数据供给）分离，可组合接入外部 Agent。
- 易方达基金：ETF / 场外指数基金查询 Skill 在 WorkBuddy / OpenClaw / Hermes Agent 基础上新增千问入口。
- 同花顺：iFinD MCP 与问财 SkillHub 保持双线推进，iFinD 走 MCP 标准化数据供给，问财走社区 Skill 生态。
- 蚂蚁数科：Agentar 金融智能体平台进入机构侧落地视野，成为大厂 Agent 平台的又一选项。

### 趋势评论

**趋势一：Skill 与 MCP 分工成型**

券商侧逐渐形成「Skill 承载投研方法论 + MCP 承载数据供给」的双层结构。Skill 负责分析师框架、观点与流程，MCP 负责行情、财务、资讯等标准数据。开发者可以只接 MCP 拿数据，也可以叠加券商 Skill 复用其研究框架，组合自由度明显提升。

**趋势二：分发平台从单点到多点**

华为小艺、OpenClaw、IMA、Coze、WorkBuddy、扣子、千问等平台同时成为机构 Skill 的上架渠道。同一份 Skill 能力跨平台分发成为常态，接入说明中「一键复制安装」逐步替代传统 API Key 申请流程，普通用户的获取门槛持续下降。

**趋势三：大厂 Agent 平台集中下场**

腾讯 WorkBuddy 金融版、阿里千问开放平台、蚂蚁数科 Agentar 等大厂平台 以「金融智能体开发平台 / 分发入口」定位集中下场：前者提供工作台底座与专家编排能力，后者提供流量入口与机构智能体分发。与券商自建 Skill 形成互补——大厂给底座和渠道，机构给专业内容与合规能力。

**对开发者的启示**：优先接入 MCP 获取标准数据，再用券商 Skill 补齐方法论与观点；两者解耦后可按场景自由组合，避免绑定单一机构生态。


---

## 🔗 工具链联动

本仓库是 FinAI 工具生态的一部分，与其他仓库协作：

| 仓库 | 定位 | 与本仓库的关系 |
|------|------|---------------|
| [awesome-finai-tools-zn](https://github.com/lj22503/awesome-finai-tools-zn) | 数据底座 | 提供工具清单 + 机构 Skill 数据 |
| [invest-brain](https://github.com/lj22503/invest-brain) | 工具推荐引擎 | 基于场景自动推荐工具 |
| [investment-buddy-pet](https://github.com/lj22503/investment-buddy-pet) | 人格化投顾 | 按投资人格匹配工具箱 |
| [SoloAdvisor-Toolkit](https://github.com/lj22503/SoloAdvisor-Toolkit) | 投顾流程工具包 | KYC → 配置 → 组合 → 报告 |
| [knowledge-workflow](https://github.com/lj22503/knowledge-workflow) | 知识管理 | 收集 → 打标 → 存储 → 产出 |

## 📄 License

MIT — 详见 [LICENSE](./LICENSE)

---

*本文件由 `scripts/generate_readme.py` 自动从 `data/tools.json` / `data/institution-skills.json` / `data/institution-dynamics.json` 生成，最后更新：2026-09-21 10:47*

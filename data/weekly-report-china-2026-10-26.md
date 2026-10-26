# 📡 FinAI Tools 国内平台周报 — 2026-10-26

> 自动生成 by GitHub Actions | [awesome-finai-tools-zn](https://github.com/lj22503/awesome-finai-tools-zn)

---

## 🆕 ClawHub 新发现 (105 个)

| 名称 | Slug | 描述 | 下载量 | 归属机构 |
|------|------|------|--------|----------|
| 腾讯自选股-金融数据查询 | `westock-data` | 金融市场结构化数据查询的权威入口。支持股票（A股/港股/美股）、ETF、指数、板块、期货、外汇、可转债的 K 线、技术指 | ? | 腾讯（WorkBuddy 金融版） |
| 金融素养学习工具 | `financial-literacy-tool-free` | 个人金融素养教育工具，提供基础金融概念、理财入门与风险意识培养。Use when 用户需要financial-liter | ? |  |
| 金融知识问答 | `fin-literacy-free` | 提供A股交易相关金融知识问答与分层教育，依据用户水平智能推荐内容并给出个性化投资建议。 | ? |  |
| 金融知识问答 | `fin-literacy` | 基于深度学习的A股专业金融知识问答和多层次教育，提升投资决策效率，支持风险管理与个性化建议。 | ? |  |
| 金融数据终端 | `fin-terminal` | \|- 功能涵盖: fin,。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理 | ? |  |
| 金融素养专业版 | `financial-literacy-tool-pro` | 提供专业金融教育与理财规划，支持个性化方案、从业认证培训、企业内训管理与学习进度追踪。 | ? |  |
| Finance Consumer Guard - 金融消保合规护栏 | `finance-consumer-guard` | 金融消保合规护栏 (finance-consumer-guard) v1.0.0。
在银行理财 / 保险 / 基金 /  | ? |  |
| Fin PIPL -金融行业个人信息保护合规检查工具 | `fin-pipl` | 金融行业个人信息保护（PIPL）合规检查工具。
基于《个人信息保护法》《个人金融信息保护规范》(JR/T 0171)、
 | ? |  |
| 生成每日金融日报 | `daily-financial-report` | 完整流程：采集数据 → 生成 Word 日报 → 生成 PPT 简报 → 发送邮件。 当用户说"生成每日金融日报"、"生 | ? |  |
| 金融市场数据质量校验工具 | `market-data-checker` | 金融市场数据质量校验工具。对 market_data.json 执行全链路数据质量检查。 支持 10 类校验规则，可扩展 | ? |  |
| 股票 | `ths-financial-data` | 该skill用于获取股票市场数据，包括实时行情、中文名称查询、键盘缩写转换、资金流向和日K线数据。使用thsdk库提供同 | ? | 同花顺 |
| 个股分析大师：面向A股支持单股深度分析与多股对比（综合/技术面/财报/价值面）。触发词：个股分析、个股对比、财报对比、价值分析、技术分析、买卖点、基本面、选时、ST分析。适用场景：用户需要对一个或多个明确股票标的做结构化分析与对比。 | `xiapi-stock-analysis` | 个股分析大师：面向A股支持单股深度分析与多股对比（综合/技术面/财报/价值面）。触发词：个股分析、个股对比、财报对比、价 | ? |  |
| 同花顺股票接口 | `ths-advanced-analysis` | 基于 thsdk 进行高级股票分析：分钟K线（1m/5m/15m/30m/60m/120m）、板块/指数行情（主要指数/ | ? | 同花顺 |
| 股票雷达 | `a-share-stock-radar` | A股短线选股「股票雷达」——先判市场情绪环境 → 锁定主线板块 → 挑低位/启动位置 → 看形态与资金 → 输出带止损的 | ? |  |
| 股票投资价值评分 / Stock Portfolio Investment Scoring | `stock-portfolio-advisor` | 分析A股自选与持仓，获取行情、财报、风险与新闻，按行业计算价值评分和独立交易环境分，输出基本面情景估值、数据缺口及受用户 | ? |  |
| 股票技术分析 (Stock Technical Analysis) | `eastmoney-tech-analysis` | 提供股票K线数据及计算KDJ、MACD、BOLL、MA技术指标，支持资金流向排名和综合买卖信号分析。 | ? |  |
| 通达信TDX股票查询技能 | `tdx-api-skill` | 基于TDX API的股票数据查询技能，提供全面的A股市场数据查询功能，包括实时行情、K线数据、分时数据、分时成交、股票搜 | ? |  |
| 牛牛量化股票系统 | `niuniu-quant` | 专业股票量化交易技能，支持实时数据查询、策略回测、智能选股及交易信号提示。 | ? |  |
| 股票简单查询 | `gaoren-stock-simple` | 股票简单分析 - A股/港股/美股实时行情快速查询 | ? |  |
| 基金值不值得买 | `cue-fund-due-diligence` | 用 Cue 一键给一只基金做全维度深度体检——基金经理画像、业绩归因、风格一致性、风险指标、费率与规模，告诉你"这只基金 | ? |  |

---

## 📋 已知机构 Skill 入库候选

以下工具已识别归属机构，对应 Skill 尚未入库。请人工确认后运行 `python scripts/add_institution.py` 追加。

### 腾讯（WorkBuddy 金融版）

```json
[
  {
    "skill_name": "腾讯自选股-金融数据查询",
    "description": "金融市场结构化数据查询的权威入口。支持股票（A股/港股/美股）、ETF、指数、板块、期货、外汇、可转债的 K 线、技术指标、筹码、财报、研报、公告、风险事件、股东、分红、ETF 持仓、新股/投资日历、龙虎榜等数据查询(不同标的与市场支持的维度不同)；同时支持行业经营数据、申万行业估值/盈利预测/财务、全球宏观经济等数据查询；微信搜索\"腾讯微证券\"小程序，获取更多专业服务～",
    "platform": "ClawHub",
    "install_method": "clawhub install westock-data",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "腾讯财经行情接口",
    "description": "腾讯财经实时行情接口，查询A股、港股、美股、期货、外汇、ETF的实时行情数据。触发关键词：查股价、查行情、查指数、腾讯接口、股票报价、实时行情",
    "platform": "ClawHub",
    "install_method": "clawhub install tencent-finance",
    "evaluation": "自动发现，待人工评估"
  }
]
```

**入库命令**: `python scripts/add_institution.py --name "腾讯（WorkBuddy 金融版）" --skills '[...]'`

### 同花顺

```json
[
  {
    "skill_name": "股票",
    "description": "该skill用于获取股票市场数据，包括实时行情、中文名称查询、键盘缩写转换、资金流向和日K线数据。使用thsdk库提供同花顺数据接口支持。支持自动将中文、缩写、短代码转换为thsdk所需的完整ths_code格式。当匹配到多只股票时，会返回候选列表供用户选择。如未安装thsdk，会自动安装。",
    "platform": "ClawHub",
    "install_method": "clawhub install ths-financial-data",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "同花顺股票接口",
    "description": "基于 thsdk 进行高级股票分析：分钟K线（1m/5m/15m/30m/60m/120m）、板块/指数行情（主要指数/申万行业/概念板块成分股）、多股票批量对比（表格+归一化走势图+相关性热力图）、盘口深度、大单流向、集合竞价异动、日内分时、历史分时。当用户提到\"分钟K线\"、\"日内走势\"、\"盘口\"、\"大单\"、\"...",
    "platform": "ClawHub",
    "install_method": "clawhub install ths-advanced-analysis",
    "evaluation": "自动发现，待人工评估"
  }
]
```

**入库命令**: `python scripts/add_institution.py --name "同花顺" --skills '[...]'`

### 东方财富

```json
[
  {
    "skill_name": "花花个人基金仓位管家",
    "description": "以 HuahuaDaily 真实基金持仓和 quant_strategy_context.v2 为数据底座，为每个用户先建立版本化投资目标、风险、现金流和资产限制，再联合东方财富研究与 serenity-skill 形成有证据和反证的 AI 投资观点，最后由确定性资金内核输出单一、果断、可审计的场外基金持有、加仓...",
    "platform": "ClawHub",
    "install_method": "clawhub install hua-personal-strategy",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "东方财富日内行情 dfcf-stock-intraday",
    "description": "使用东方财富 API 获取 A 股（沪市/深市）及指数的日内分时数据。当用户询问某只 A 股或指数的日内走势、分时数据、当日行情、实时价格、分时图数据时，必须使用此 skill。触发关键词包括：分时数据、日内数据、今日行情、分时走势、intraday、当日走势、东方财富获取数据。支持沪市（market=1）和深市...",
    "platform": "ClawHub",
    "install_method": "clawhub install dfcf-stock-intraday",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "A股财报结构化拆解系统",
    "description": "A股上市公司财报结构化拆解系统。基于16节固定模板，对季报/年报进行一手数据提取、自算核验、跨季度可比的结构化分析。数据源优先级与racing-quant-ai一致（Tushare > akshare > baostock > 东方财富API）。触发词：财报拆解，财报分析，季报分析，年报分析，财报拆解模板，earnings report，财报解读。",
    "platform": "ClawHub",
    "install_method": "clawhub install ashare-financial-report-analysis",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "A股技术分析报告",
    "description": "A股个股技术分析报告生成工具。当用户请求生成股票技术分析报告、查询A股个股行情、分析个股走势时触发。支持输入股票代码和股票名称，自动抓取东方财富实时数据并生成结构化技术分析报告。",
    "platform": "ClawHub",
    "install_method": "clawhub install a-stock-technical-analysis",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "stock",
    "description": "基于东方财富权威数据库，提供股票选股、行情、财务及关联关系等金融数据的智能查询与筛选服务。",
    "platform": "ClawHub",
    "install_method": "clawhub install stock-mx",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "All-Market Financial Data Hub",
    "description": "基于东方财富数据库，支持自然语言查询金融数据，覆盖A港美、基金、债券等多种资产，含实时行情、公司信息、估值、财务报表等，可用于投资研究、交易复盘、市场监控、行业分析、信用研究、财报审计、资产配置等场景，适配机构与个人多元需求。返回结果包含 xlsx 与 Markdown 文件。Natural language q...",
    "platform": "ClawHub",
    "install_method": "clawhub install mx-finance-data",
    "evaluation": "自动发现，待人工评估"
  }
]
```

**入库命令**: `python scripts/add_institution.py --name "东方财富" --skills '[...]'`

### 国泰海通

```json
[
  {
    "skill_name": "Stockstar Fund Rating - 证券之星基金评级",
    "description": "查询公募基金评级数据，数据来源证券之星（fund.stockstar.com）， 涵盖上海证券、国泰海通、银河证券、招商证券、晨星、济安金信、 天相投顾七家评级机构。支持输入基金代码查询各机构星级评级。 触发词：基金、评级、基金评级、星级、基金推荐、五星基金、 晨星评级、上海证券评级、银河证券评级、招商证券评级、 济安金信评级、天相投顾评级、国泰海通评级、证券之星基金",
    "platform": "ClawHub",
    "install_method": "clawhub install stockstar-fund-rating",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "国泰海通证券-灵犀自选股管理",
    "description": "国泰海通证券-灵犀自选管理 skill，支持查询自选股行情、添加、删除自选股。**本期仅支持管理【我的自选】分组中的自选股，其他分组中的自选股管理仍在开发中。** 当用户表达查看自选股、查看自选股行情、关注某只股票、从自选股中移除某只股票等意图时，必须使用本 Skill。**Agent 只需读取此文件，无需读取其...",
    "platform": "ClawHub",
    "install_method": "clawhub install lingxi-watchlist-skill",
    "evaluation": "自动发现，待人工评估"
  },
  {
    "skill_name": "国泰海通证券-灵犀实时行情",
    "description": "国泰海通证券-灵犀实时行情 skill：标的覆盖 A 股、港股、美股、ETF与指数；支持单只或多只标的的实时行情，数据维度包括最新价、涨跌幅、涨跌额、成交量、成交额、换手率、当日资金净流入、量比等。 当用户询问股价、涨跌幅、行情走势、资金流向或相关证券行情时，优先通过本 Skill 取数，若本 Skill 无有效...",
    "platform": "ClawHub",
    "install_method": "clawhub install lingxi-realtimemarketdata-skill",
    "evaluation": "自动发现，待人工评估"
  }
]
```

**入库命令**: `python scripts/add_institution.py --name "国泰海通" --skills '[...]'`

### 中金公司

```json
[
  {
    "skill_name": "期货查询 - Futures Inquiry",
    "description": "查询上期所、大商所、郑商所、中金所、广期所期货实时行情及历史 K 线。当用户说：螺纹钢主力什么价？豆粕期货涨了吗？SC 原油最近一周走势？或类似期货行情问题时，使用本技能。",
    "platform": "ClawHub",
    "install_method": "clawhub install futures",
    "evaluation": "自动发现，待人工评估"
  }
]
```

**入库命令**: `python scripts/add_institution.py --name "中金公司" --skills '[...]'`

### 工商银行

```json
[
  {
    "skill_name": "工商数据查询 · 企业基本信息、股东、分支、投资与变更",
    "description": "查询企业工商基本信息、企业股东与出资记录、分支机构、对外投资、工商变更，并按需补充招投标战绩。适用于企业核验、注册资本/法人查询、股东和分支查询。五项工商能力每次/每页3积分，只按需调用；司法风险和复杂股权穿透本期未开放。完整企业背调报告使用zlbx-company-intel，招标项目决策使用zlbx-bid-decision。使用平台API Key，首次自动注册需用户同意。",
    "platform": "ClawHub",
    "install_method": "clawhub install zlbx-company-registry",
    "evaluation": "自动发现，待人工评估"
  }
]
```

**入库命令**: `python scripts/add_institution.py --name "工商银行" --skills '[...]'`

---

## 🔔 新机构预警

以下 7 个工具疑似来自**未收录的新机构**，需人工确认。

- **机构名（推断）**: PIPL
  - 发现来源: ClawHub
  - 工具名: Fin PIPL -金融行业个人信息保护合规检查工具
  - 链接: https://clawhub.ai/wwumit/skills/fin-pipl
  - 描述: 金融行业个人信息保护（PIPL）合规检查工具。 基于《个人信息保护法》《个人金融信息保护规范》(JR/T 0171)、 《金融数据安全 数据安全分级指南》(JR/T 0197) 等行业法规， 提供银行、证券、保险、支付四大场景的合规评估。 
  - **建议行动**: 人工确认后运行 `python scripts/add_institution.py --name "PIPL" --skills '[...]'` 入库

- **机构名（推断）**: 深度透视基金
  - 发现来源: ClawHub
  - 工具名: 基金投顾
  - 链接: https://clawhub.ai/wangxiaoxu/skills/cue-fund-advisory
  - 描述: 用 Cue 跑「基金投顾」场景的深度研究：穿透公募基金底仓，深度透视基金经理真实管理能力与风格漂移，量化评估选股与择时能力。覆盖大类资产配置月报、公募基金全维尽调、固收+与纯债基金排雷优选、基金业绩归因与能力评估、基金组合穿透与重复配置排雷
  - **建议行动**: 人工确认后运行 `python scripts/add_institution.py --name "深度透视基金" --skills '[...]'` 入库

- **机构名（推断）**: 小果基金
  - 发现来源: ClawHub
  - 工具名: 小果基金量化分析助手
  - 链接: https://clawhub.ai/li152/skills/xg-fund-quant
  - 描述: 小果(微信:xg_quant)基金量化分析助手专注于基金量化分析工具，基于小果量化策略系统，提供基金历史行情数据、基金因子数据、基金策略回测、基金组合分析等核心功能。适用于基金投资者、资产配置研究员和量化策略开发者。
  - **建议行动**: 人工确认后运行 `python scripts/add_institution.py --name "小果基金" --skills '[...]'` 入库

- **机构名（推断）**: 政府基金
  - 发现来源: ClawHub
  - 工具名: BP 融资自测清单 · 双轨版（VC × 政府基金）
  - 链接: https://clawhub.ai/zhuiwensm99/skills/project-fund-screening
  - 描述: 为寻求融资的初创或成长期项目做初步筛选诊断——同时对照 VC/PE 分阶段 BP 标准与政府引导/产投基金落地要求，输出结构化达标度、红旗清单与整改建议。当用户需要判断某项目能否拿到财务投资人或政府基金的钱、BP 哪里不达标、政府基金落地可
  - **建议行动**: 人工确认后运行 `python scripts/add_institution.py --name "政府基金" --skills '[...]'` 入库

- **机构名（推断）**: 三立期货
  - 发现来源: ClawHub
  - 工具名: 三立智期 抢先版
  - 链接: https://clawhub.ai/sqringwang/skills/slzq-trading-preview
  - 描述: 三立期货「三立智期」官方技能：对话领取模拟盘密钥，查行情与持仓，模拟盘可下单；问是否正规、开户也可答。实盘请去 App 复制密钥。
  - **建议行动**: 人工确认后运行 `python scripts/add_institution.py --name "三立期货" --skills '[...]'` 入库

- **机构名（推断）**: 大道无形
  - 发现来源: ClawHub
  - 工具名: 大道无形·段永平价值投资
  - 链接: https://clawhub.ai/419597334-sudo/skills/dadao-investing
  - 描述: 大道无形·段永平价值投资框架。用段永平（雪球"大道无形我有型"，网易0.8美元抄底近100倍、2006年62.01万美元巴菲特午餐首位华人中标者）的方式分析个股：不为清单一票否决（不做空/不借钱/不懂不碰）→ 三层过滤（好生意→好人→好价格
  - **建议行动**: 人工确认后运行 `python scripts/add_institution.py --name "大道无形" --skills '[...]'` 入库

- **机构名（推断）**: 三立期货
  - 发现来源: ClawHub
  - 工具名: 三立期货AI交易助手
  - 链接: https://clawhub.ai/13371979982/skills/slzq-trading
  - 描述: 三立期货「三立智期」官方技能：对话领取模拟盘密钥，查行情、持仓、资讯与龙虎榜；模拟盘可下单；实盘可设条件单与止盈止损（服务端托管，不用盯盘）。问是否正规、开户也可答。实盘请到小立助理个人中心绑定。
  - **建议行动**: 人工确认后运行 `python scripts/add_institution.py --name "三立期货" --skills '[...]'` 入库

---
*报告生成时间: 2026-10-26 16:14:29*
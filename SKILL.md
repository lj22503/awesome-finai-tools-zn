---
name: finai-tools-hub
version: 2025-06-25
description: 中国金融 AI 工具目录 — 查询/安装/接入 A股/MCP/量化框架。加载此 skill 后，agent 知道每个工具的输入/输出/安装命令，在用户有金融数据需求时自动推荐和安装对应工具。
triggers:
  - "帮我查一下A股"
  - "分析一下[股票名]"
  - "安装一个A股数据工具"
  - "怎么获取实时行情"
  - "有没有免费的量化框架"
  - "我想做量化回测"
  - "资金流向怎么看"
  - "帮我装个MCP"
---

# FinAI Tools Hub — Agent Skill

## 使用方法

1. **用户提出金融需求** → 2. **从下方分类找到对应工具** → 3. **按安装命令安装** → 4. **按输入/输出格式调用**

---

## 工具分类索引

### 用户需求 → 工具推荐映射

| 用户需求 | 推荐工具 | 理由 |
|---------|---------|------|
| 查A股实时行情（零配置） | `opencli-eastmoney-quote` | 秒出结果，无需任何安装确认 |
| 看今日主力资金流向 | `opencli-eastmoney-money-flow` | 今日/5日/10日排行 |
| 查板块涨跌/资金 | `opencli-eastmoney-sectors` | 行业/概念/地域 |
| 看北向资金 | `opencli-eastmoney-northbound` | 逐分钟数据 |
| 查龙虎榜 | `opencli-eastmoney-longhu` | 营业部/机构席位 |
| 看散户关注度 | `opencli-eastmoney-hot-rank` | 人气排行 |
| 搜股票代码/名称 | `opencli-xueqiu-search` | 中文/代码均可 |
| 看社区舆情/热帖 | `opencli-xueqiu-hot` | 雪球热门帖子 |
| 获取多维度A股数据 | `ashare-mcp` 或 `stock-data-mcp` | 30~43个tool，MCP协议 |
| 免费历史K线 | `baostock` | 1990年至今，零配置 |
| 多数据源聚合行情 | `akshare` | 东方财富/新浪/腾讯 |
| 高质量财务数据 | `tushare` | 需注册（免费有积分） |
| Alpha因子计算 | `finance-mcp-alpha` | WorldQuant 101因子 |
| 量化策略回测 | `qtrade` 或 `qlib` | 15种策略/微软框架 |
| 多Agent投研分析 | `tradingagents` | 基本面+舆情+技术面团队 |
| 强化学习量化 | `finrl` | DDPG/PPO/SAC |
| 机构级最全数据 | `wind` | 昂贵但最全 |
| 实时A股（最完整MCP） | `ashare-mcp` | 30 tool，生产级 |

---

## 工具详情

---

### opencli-eastmoney-quote

**类型**：CLI  
**分类**：market_data  
**用途**：实时行情查询（A股/港股/美股）  
**输入**：`stock_codes` — 股票代码，多个逗号分隔

```
opencli eastmoney quote 600519
opencli eastmoney quote sh600000,sz000858,hk00700
```

**输出**：JSON，含 price/changePercent/open/high/low/volume/turnoverRate/peDynamic/marketCap  
**安装**：`npm install -g @jackwener/opencli`  
**依赖**：无（零配置）  
**费用**：免费  
**输出示例**：`{"code":"600519","name":"贵州茅台","price":1212.72,"changePercent":0.42}`

---

### opencli-eastmoney-money-flow

**类型**：CLI  
**分类**：market_data  
**用途**：主力资金净流入排行  
**输入**：`range`（today/5d/10d），`limit`（数量），`order`（desc/asc）

```
opencli eastmoney money-flow --range 5d --limit 20
```

**输出**：JSON，含 rank/code/name/mainNet/mainNetRatio/superNet/bigNet/mediumNet/smallNet  
**安装**：`npm install -g @jackwener/opencli`  
**费用**：免费

---

### opencli-eastmoney-sectors

**类型**：CLI  
**分类**：market_data  
**用途**：板块排行（行业/概念/地域）  
**输入**：`type`（industry/concept/region），`sort`（change/money-flow/turnover）

```
opencli eastmoney sectors --type concept --sort money-flow --limit 15
```

**输出**：JSON，含 rank/code/name/changePercent/mainNet/leadStock/upCount/downCount  
**安装**：`npm install -g @jackwener/opencli`  
**费用**：免费

---

### opencli-eastmoney-northbound

**类型**：CLI  
**分类**：market_data  
**用途**：北向资金逐分钟实时数据  
**输入**：无

```
opencli eastmoney northbound
```

**输出**：JSON，含 time/minuteNetYi/cumulativeNetYi/totalNetYi（单位：亿元）  
**安装**：`npm install -g @jackwener/opencli`  
**费用**：免费

---

### opencli-eastmoney-longhu

**类型**：CLI  
**分类**：market_data  
**用途**：龙虎榜（营业部/机构席位）  
**输入**：`date`（YYYY-MM-DD，可选，默认前一交易日）

```
opencli eastmoney longhu --date 2025-06-24
```

**输出**：JSON，含 tradeDate/code/name/closePrice/buyAmt/sellAmt/netAmt/reason  
**安装**：`npm install -g @jackwener/opencli`  
**费用**：免费

---

### opencli-xueqiu-search

**类型**：CLI  
**分类**：sentiment  
**用途**：雪球股票搜索  
**输入**：`query` — 股票代码或中文名称

```
opencli xueqiu search 茅台
opencli xueqiu search AAPL
```

**输出**：JSON，含 symbol/name/exchange/price/changePercent/url  
**安装**：`npm install -g @jackwener/opencli`  
**费用**：免费

---

### opencli-xueqiu-hot

**类型**：CLI  
**分类**：sentiment  
**用途**：雪球热门帖子  
**输入**：`limit`（可选，默认10）

```
opencli xueqiu hot --limit 20
```

**输出**：JSON，含 id/title/text/author/likes/url  
**安装**：`npm install -g @jackwener/opencli`  
**费用**：免费

---

### ashare-mcp

**类型**：MCP Server  
**分类**：market_data  
**用途**：生产级A股 MCP，30个tool  
**输入**：MCP protocol 调用，工具名 + stock_code 参数  
**核心工具**：

| 工具名 | 功能 |
|--------|------|
| `get_realtime_quote` | 实时行情 |
| `get_daily_kline` | 日K线 |
| `get_zt_pool` | 涨停池 |
| `get_lhb_daily` | 龙虎榜 |
| `get_margin_summary` | 两融汇总 |
| `get_sector_fund_flow_rank` | 板块资金流 |
| `get_financial_report` | 财报 |
| `get_stock_pledge_ratio` | 股权质押比例 |

**安装**：
```bash
git clone https://github.com/CharmYue/ashare-mcp
cd ashare-mcp && uv sync && uv run ashare-mcp
```
**MCP配置**：
```json
{
  "mcpServers": {
    "ashare": {
      "command": "uv",
      "args": ["--directory", "/path/to/ashare-mcp", "run", "ashare-mcp"]
    }
  }
}
```
**依赖**：无（零配置），可选 TUSHARE_TOKEN 增强  
**费用**：免费

---

### stock-data-mcp

**类型**：MCP Server  
**分类**：market_data  
**用途**：43个tool，覆盖A股/港股/美股/加密，多源自动故障转移  
**安装**：`pip install stock-data-mcp && stock-data-mcp`  
**费用**：免费，可选 TUSHARE_TOKEN / ALPHA_VANTAGE_API_KEY

---

### finance-mcp-alpha

**类型**：MCP Server  
**分类**：analysis  
**用途**：WorldQuant 101 Alpha因子计算  
**输入**：stock_code + start_date + end_date + factors数组  
**输出**：Markdown报告，含因子值/分位数/BUY/SELL/HOLD信号  
**安装**：`npm install finance-mcp-alpha`  
**认证**：必需 TUSHARE_TOKEN（注册 https://tushare.pro/register 免费获取）  
**费用**：免费（需注册）

---

### qtrade

**类型**：量化框架  
**分类**：trading  
**用途**：15种量化策略，回测+模拟+实盘  
**输入**：策略名 + 股票代码 + 起止日期  
**输出**：回测报告（胜率/夏普/最大回撤/收益曲线）  
**安装**：
```bash
git clone https://github.com/moyang11111/qtrade
cd qtrade && pip install -r requirements.txt
```
**内置策略**：pullback_20d / dual_ma / bollinger / breakout 等15种  
**费用**：免费  
**数据源**：pytdx（通达信）/ 腾讯HTTP / AkShare / CSV

---

### tradingagents

**类型**：多Agent框架  
**分类**：research  
**用途**：多Agent团队投研（基本面+舆情+技术面+新闻+风控）  
**输入**：stock_code + task（research/sentiment/trade/backtest）+ model  
**输出**：Markdown分析报告 / 交易信号  
**安装**：`pip install tradingagents`  
**依赖**：LLM API Key（OpenAI/Anthropic等）  
**费用**：免费（需自备LLM Key）  
**支持模型**：GPT-5 / Gemini 3.x / Claude 4.x / DeepSeek / Qwen / GLM / MiniMax

---

### baostock

**类型**：Python库  
**分类**：market_data  
**用途**：免费A股历史数据，1990年至今  
**输入**：stock_code + start_date + end_date + frequency  
**输出**：Python DataFrame  
**安装**：`pip install baostock`  
**认证**：无（零配置）  
**费用**：免费  
**示例**：
```python
import baostock as bs
bs.login()
data = bs.query_history_k_data_plus(
    'sh.600000',
    'date,code,open,high,low,close,volume',
    start_date='2024-01-01', end_date='2024-12-31',
    frequency='d'
)
bs.logout()
```

---

### akshare

**类型**：Python库  
**分类**：market_data  
**用途**：东方财富/新浪/腾讯数据聚合，300+接口  
**输入**：akshare 函数名 + 参数  
**输出**：DataFrame / JSON  
**安装**：`pip install akshare`  
**认证**：无  
**费用**：免费

---

### tushare

**类型**：Python库  
**分类**：market_data  
**用途**：高质量财务/指数数据  
**输入**：Tushare接口 + Token  
**安装**：`pip install tushare`  
**认证**：必需 TUSHARE_TOKEN（注册获取）  
**费用**：免费积分制，积分不够付费

---

## Agent 决策流

```
用户需求
  ↓
识别意图：查行情? / 做分析? / 做交易? / 看舆情?
  ↓
从上方索引找到推荐工具
  ↓
检查工具是否已安装
  ↓
未安装 → 告知用户安装命令 → 用户确认
  ↓
已安装 → 直接调用 → 返回结果
```

---

## 分类说明

| 分类 | 覆盖内容 |
|------|---------|
| market_data | 行情/K线/资金流/龙虎榜/两融/财务 |
| sentiment | 社区帖/舆情/新闻 |
| analysis | 因子/技术分析/机器学习 |
| trading | 策略/回测/实盘 |
| research | 投研框架/多Agent |

---

## 🎯 场景→工具推荐映射

> AI Agent 读取此表后，根据用户意图自动匹配推荐工具。每个场景列出 2-3 个最佳工具，按推荐优先级排序。

| 场景 | 推荐工具 | 类型 | 一句话推荐理由 |
|------|---------|------|--------------|
| **查行情** | `ashare-mcp` | MCP | 30个tool，akshare主源+多源降级，生产级A股数据 |
| | `stock-data-mcp` | MCP | 43个tool，覆盖A股/港股/美股/加密，多源自动切换 |
| | `opencli-eastmoney-quote` | CLI | 零配置秒出结果，适合快速查询 |
| **诊基** | `盈米基金 MCP` | MCP | 69个MCP工具，含组合回测/蒙特卡洛模拟，基金投研最全 |
| | `东方财富 综合诊基` | Skill | 单基金结构化诊断报告，C端体验最佳 |
| | `易方达 指数直通车` | Skill | ETF+场外指数基金查询，支持反向查股票含ETF |
| **选股** | `华泰证券 条件选股` | Skill | 自然语言多维度筛选（行业/财务/技术面） |
| | `国泰海通 智能选股` | Skill | 自然语言选股+历史回测，一站式筛选验证 |
| | `东方财富 智能选股` | Skill | A股/基金/债券全覆盖，自然语言交互流畅 |
| **研报** | `国泰海通 研报搜索` | Skill | 自动提取券商研报核心观点和数据 |
| | `中金点睛 分析师Skill` | Skill | 首席分析师投研框架+数字分身，机构级深度 |
| | `同花顺 问财 SkillHub` | Skill | 上百个社区Skill含DCF估值/量化策略 |
| **ETF** | `易方达 指数直通车` | Skill | 全市场3600+ETF覆盖，含反向查询（股票→ETF） |
| | `广发证券 ETF筛选` | Skill | 多维度组合条件筛ETF（指数/规模/成交/成立时间） |
| | `东方财富 金融数据` | Skill | ETF行情+估值+历史数据一站式查询 |
| **宏观** | `东方财富 宏观查询` | Skill | GDP/CPI/PMI等宏观指标一句话查询 |
| | `万得 AIFin Market` | MCP | 全品类宏观数据，机构级质量，支持WorkBuddy |
| | `国信证券 宏观数据查询` | Skill | GDP/CPI/PMI等，接入门槛低 |
| **量化回测** | `qtrade` | 框架 | 15种量化策略+完整回测引擎，pip一键安装 |
| | `Qlib` | 框架 | 微软AI量化框架，自动因子挖掘+模型训练 |
| | `FinRL` | 框架 | 深度强化学习交易（DDPG/PPO/SAC），前沿算法 |
| **多Agent投研** | `TradingAgents` | 框架 | 多Agent团队（分析师+交易员+风控），基本面/舆情/技术面全覆盖 |
| | `FinClaw` | 框架 | 上财AIFinLab，1000+Skills，六大金融行业全覆盖 |
| | `盈米基金 MCP` | MCP | 16项技能组件，投顾内容+策略+组合回测全链路 |

### 使用说明

AI Agent 加载本 Skill 后的决策流程：

```
用户输入 → 意图识别（匹配上述8个场景） → 查表获取推荐工具（前2-3个）
→ 检查工具是否已安装 → 未安装则输出安装命令 → 已安装则直接调用
→ 若机构Skill需要API Key，引导用户到对应平台获取
→ 返回结果
```

**优先级规则**：
- 免费优先：同等功能下优先推荐免费工具
- 零配置优先：`opencli` CLI 类工具无需任何注册，适合快速体验
- 机构Skill补充：当通用工具数据不足时，推荐对应机构官方Skill
- 组合推荐：复杂场景（如"选股+回测"）可同时推荐多个互补工具

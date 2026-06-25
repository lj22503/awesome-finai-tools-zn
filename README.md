# Awesome FinAI Tools
### 中国金融 AI 工具全景图

[![Stars](https://img.shields.io/github/stars/lj22503/awesome-finai-tools?style=flat-square)](https://github.com/lj22503/awesome-finai-tools)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)
[![自动巡检](https://img.shields.io/badge/巡检-每周一-blue?style=flat-square)](#)

> 本仓库收录中国金融领域可接入 AI Agent 的工具：Market Data MCP、量化框架、券商 Skills、交易接口、数据 API。每周自动巡检 GitHub / npm / PyPI 更新。

[📋 完整工具清单](#工具分类) · [🚀 快速上手](#快速上手) · [🤖 Agent 接入](#agent-接入) · [📝 贡献指南](./CONTRIBUTING.md) · [📄 llms.txt](./llms.txt)

---

## 🔥 精选推荐（新手首选）

| 场景 | 推荐工具 | 理由 |
|------|---------|------|
| **零配置查行情** | `opencli eastmoney quote` | 安装即用，秒出结果 |
| **多维度A股数据（MCP）** | `ashare-mcp` | 30个tool，akshare主源+多源降级 |
| **免费历史K线** | `baostock` | 1990年至今，无需注册 |
| **量化策略回测** | `qtrade` | 15种策略+完整回测引擎 |
| **多Agent投研** | `tradingagents` | 分析师+交易员+风控团队 |
| **免费全行业覆盖** | `finclaw`（上财） | 1000+Skills，六大行业 |
| **基金深度分析** | `盈米MCP` | 69个MCP工具，组合回测 |
| **机构级研报** | `中金点睛` | 首席分析师专属Skill |

---

## 工具分类

### 📊 Market Data（行情数据）

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [OpenCLI EastMoney](#opencli-eastmoney) | CLI | ✅ 免费 | 实时行情/资金流/板块/龙虎榜/北向/ETF | `npm install -g @jackwener/opencli` |
| [ashare-mcp](#ashare-mcp) | MCP | ✅ 免费 | 30个tool，akshare主源+多源降级，实时/K线/资金/两融/涨停 | `uv run ashare-mcp` |
| [stock-data-mcp](#stock-data-mcp) | MCP | ✅ 免费 | 43个tool，A股/港股/美股/加密，多源自动切换 | `pip install stock-data-mcp` |
| [astock-mcp-server](#astock-mcp-server) | MCP | ✅ 免费 | BaoStock+Sina，零API key，实时/K线/选股 | `pip install astock-mcp-server` |
| [BaoStock](#baostock) | Python | ✅ 免费 | 免费A股平台，1990年至今，无需注册 | `pip install baostock` |
| [AKShare](#akshare) | Python | ✅ 免费 | 东方财富/新浪/腾讯聚合，300+接口 | `pip install akshare` |
| [EFinance](#efinance) | Python | ✅ 免费 | 东方财富/腾讯/新浪聚合 | `pip install efinance` |
| [广发证券 Skill](#广发证券-skill) | Skill | 免费/未知 | 股票信息/财务对比/龙虎榜/ETF监测/基金定投 | [hd.gf.com.cn](https://hd.gf.com.cn/gfwskill2026/#/index) |
| [国信证券 Skill](#国信证券-skill) | Skill | 免费/未知 | 智能选股/ETF筛选/基金对比/宏观/行情 | [小信助手](https://weixin.guosen.com.cn/gs/xxskills/#architecture) |
| [天天基金 Skill](#天天基金-skill) | Skill | 免费部分 | 基金信息/自选/深度诊断/基金比较/持仓 | 天天基金App |
| [华泰 AI 涨乐](#华泰-ai-涨乐) | Skill | 限时免费 | 行情检索/模拟交易/条件选股/自选股 | 华泰App / OpenClaw |
| [Tushare Pro](#tushare-pro) | Python | ⚠️ 积分 | 高质量财务/指数，Token制 | `pip install tushare` |
| [Wind API](#wind-api) | API | 💰 昂贵 | 机构级最全数据 | Wind Terminal |
| [Choice](#choice) | API | 💰 年费数万 | 东方财富机构数据 | Choice 终端 |

### 💬 Sentiment（舆情/社区）

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [OpenCLI Xueqiu](#opencli-xueqiu) | CLI | ✅ 免费 | 雪球股票搜索/热门帖子 | `npm install -g @jackwener/opencli` |
| [OpenCLI THS Hot](#opencli-ths-hot) | CLI | ✅ 免费 | 同花顺人气排行 | `npm install -g @jackwener/opencli` |
| [OpenCLI SinaFinance](#opencli-sinafinance) | CLI | ✅ 免费 | 新浪财经新闻/资讯 | `npm install -g @jackwener/opencli` |
| [Agent Reach Xueqiu](#agent-reach-xueqiu) | Channel | ⚠️ Cookie | 雪球行情/热帖/热门股票 | `pip install agent-reach` |

### 📈 Analysis（分析与因子）

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [FinanceMCP-Alpha](#financemcp-alpha) | MCP | ⚠️ Tushare Token | WorldQuant 101 Alpha因子 | `npm install finance-mcp-alpha` |
| [Qlib](#qlib) | 框架 | ✅ 免费 | 微软AI量化，自动因子挖掘 | `pip install pyqlib` |
| [TradingAgents](#tradingagents) | 框架 | ✅ 免费 | 多Agent LLM投研，基本面+舆情+技术 | `pip install tradingagents` |
| [AlphaAgent](#alphaagent) | 框架 | ✅ 免费 | KDD 2025 LLM驱动因子挖掘 | GitHub |

### 🔄 Trading（交易执行）

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [QTrade](#qtrade) | 框架 | ✅ 免费 | 15种量化策略，回测+模拟+实盘 | `pip install qtrade` |
| [VeighNa](#vnpy) | 框架 | ✅ 免费 | 事件驱动量化，回测+实盘 | `pip install vnpy` |
| [FinRL](#finrl) | 框架 | ✅ 免费 | 深度强化学习交易，DDPG/PPO/SAC | `pip install finrl` |
| [华泰 AI 涨乐](#华泰-ai-涨乐) | Skill | 限时免费 | A股模拟交易/条件选股/自选股 | 华泰App / OpenClaw |

### 🔬 Research（投研）

| 工具 | 类型 | 费用 | 描述 | 接入 |
|------|------|------|------|------|
| [同花顺问财 SkillHub](#同花顺问财-skillhub) | Skill | 免费部分 | 股基债期全品类，选股/诊断/财经搜索/产业链 | [iwencai.com](https://www.iwencai.com/skillhub) |
| [东方财富 ClawBot](#东方财富-clawbot) | Skill | ✅ 免费 | 智能选股/个股诊断/财报解读/宏观研究 | 阿里云平台 |
| [盈米基金 MCP](#盈米基金-mcp) | MCP | 联系销售 | 69个MCP工具，组合回测/蒙特卡洛模拟 | 盈米AI开放平台 |
| [FinClaw](#finclaw) | 框架 | ✅ 免费 | 上财AIFinLab，1000+Skills，六大行业 | [GitHub](https://github.com/aifinlab/FinClaw) |
| [FIN-SKILLS](#fin-skills) | Skill市场 | 免费部分 | 龙虎榜解读/个股异动/基金分析/日报生成 | [fin-skills.finstep.cn](https://fin-skills.finstep.cn) |
| [中金点睛](#中金点睛) | Skill | 机构付费 | 首席分析师专属，宏观/策略/计算机/新能源 | 中金点睛平台 |
| [兴业证券 知己管家](#兴业证券-知己管家) | Skill | 免费部分 | 一句话交易/智能诊断/资讯总结/投研27模块 | 优理宝App |
| [国泰海通 灵犀](#国泰海通-灵犀) | Skill | 免费部分 | 查研报/行情/数据/榜单/选股/自选股 | 国泰海通平台 |
| [TradingAgents](#tradingagents) | 框架 | ✅ 免费 | 多Agent LLM投研团队，分析师+风控 | `pip install tradingagents` |

---

## 工具详情

### opencli-eastmoney

**类型**：CLI（Jackwener/OpenCLI）
**描述**：东方财富行情 CLI，支持实时行情/K线/历史数据/股东/资金流/龙虎榜/北向/ETF/可转债

**安装**：
```bash
npm install -g @jackwener/opencli
```

**使用**：
```bash
opencli eastmoney quote 600519          # 实时行情
opencli eastmoney money-flow --range 5d # 资金流向
opencli eastmoney sectors               # 板块排行
opencli eastmoney northbound            # 北向资金
opencli eastmoney longhu --date 2025-06-20  # 龙虎榜
opencli eastmoney hot-rank              # 人气排行
```

---

### ashare-mcp

**类型**：MCP Server（CharmYue）
**GitHub**：[CharmYue/ashare-mcp](https://github.com/CharmYue/ashare-mcp)
**描述**：30个tool，akshare主源+baostock/tushare降级，生产级A股数据

**安装**：
```bash
uv run ashare-mcp
```

**能力**：实时行情 / 日K线 / 资金流 / 龙虎榜 / 两融 / 财报 / 涨停池 / 指数

---

### BaoStock

**类型**：Python 库（BaoStock团队）
**地址**：[baostock.com](https://baostock.com)
**描述**：免费A股平台，历史K线/财务/宏观/板块，**无需注册，无需配置**

**安装**：
```bash
pip install baostock
```

**使用**：
```python
import baostock as bs
bs.login()
rs = bs.query_history_k_data_plus("sh.600000",
    "date,code,open,high,low,close,volume",
    start_date='2024-01-01', end_date='2024-12-31')
```

---

### 同花顺问财 SkillHub

**类型**：Skill（同花顺）
**地址**：[iwencai.com/skillhub](https://www.iwencai.com/skillhub)
**描述**：同花顺官方技能市场，股基债期全品类数据查询与分析，上百个社区技能（DCF估值/量化策略等）

**安装**：OpenClaw / Claude / ChatGPT / Cursor 等主流AI平台搜索「同花顺问财」

---

### 华泰 AI 涨乐

**类型**：Skill（华泰证券）
**描述**：深度集成于华泰App，5大核心功能：金融分析与资讯、行情检索、**A股模拟交易**、条件选股、自选股管理

**安装**：华泰证券App（集成）或 **OpenClaw 一键部署**

**费用**：限时免费，新用户每日500-1000次调用额度

---

### 中金点睛

**类型**：Skill（中金公司）
**描述**：覆盖计算机、策略、宏观、新能源等领域首席分析师专属Skill，面向机构投资者

**接入**：注册登录「中金点睛」平台

**费用**：面向机构付费用户

---

### 盈米基金 MCP

**类型**：MCP（盈米基金）
**描述**：69个标准化MCP工具 + 16项核心技能组件，涵盖金融数据、投研服务（**组合回测、蒙特卡洛模拟**）、投顾内容与策略

**接入**：MCP 或 OpenAPI，兼容 Coze / Dify / Cursor

**费用**：联系销售

---

### FinClaw（上财AIFinLab）

**类型**：框架（上海财经大学）
**GitHub**：[aifinlab/FinClaw](https://github.com/aifinlab/FinClaw)
**描述**：超1000个自研Skills，按银行/证券/保险/基金/期货/信托六大行业划分，提供统一金融数据抽象层，**原生兼容OpenClaw Agent OS**

**安装**：
```bash
git clone https://github.com/aifinlab/FinClaw
```

**费用**：✅ 完全开源免费

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
# ashare-mcp（推荐）
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

## 📄 License

MIT — 详见 [LICENSE](./LICENSE)

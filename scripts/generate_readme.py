#!/usr/bin/env python3
"""
从 tools.json 自动生成 README.md 和 llms.txt
每次 tools.json 更新后运行此脚本
"""

import json
import sys
from datetime import datetime

TEMPLATE_README = """# Awesome FinAI Tools
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

{category_sections}

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
4. 自动发 PR 更新 `data/tools.json` 和 `README.md`

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

---

*本文件由 `scripts/generate_readme.py` 自动从 `data/tools.json` 生成，最后更新：{update_time}*
"""

CATEGORY_META = {
    "market_data": {
        "emoji": "📊",
        "title": "Market Data（行情数据）",
        "desc": "实时行情、历史K线、资金流向、龙虎榜、北向资金",
        "color": "行情",
        "examples": ["opencli eastmoney quote 600519", "ashare-mcp", "baostock"]
    },
    "sentiment": {
        "emoji": "💬",
        "title": "Sentiment（舆情/社区）",
        "desc": "雪球、同花顺、Reddit等社区舆情和热门讨论",
        "color": "舆情",
        "examples": ["opencli xueqiu search 茅台", "雪球热帖"]
    },
    "analysis": {
        "emoji": "📈",
        "title": "Analysis（分析与因子）",
        "desc": "Alpha因子、量化分析、技术指标",
        "color": "分析",
        "examples": ["FinanceMCP-Alpha", "Qlib", "TradingAgents"]
    },
    "trading": {
        "emoji": "🔄",
        "title": "Trading（交易执行）",
        "desc": "量化策略回测、模拟交易、实盘接口",
        "color": "交易",
        "examples": ["QTrade", "VeighNa", "华泰涨乐"]
    },
    "research": {
        "emoji": "🔬",
        "title": "Research（投研）",
        "desc": "研报解读、宏观数据、基金分析、券商官方Skill",
        "color": "投研",
        "examples": ["同花顺SkillHub", "中金点睛", "FinClaw"]
    },
    "news": {
        "emoji": "📰",
        "title": "News（新闻资讯）",
        "desc": "财经新闻、公告、快讯",
        "color": "新闻",
        "examples": ["新浪财经"]
    }
}

COST_LABELS = {
    "free": "✅ 免费",
    "free_partial": "⚠️ 免费部分",
    "free_limited": "⚠️ 限时免费",
    "contact_sales": "💰 联系销售",
    "institutional": "💰 机构付费",
    "unknown": "❓ 未知",
}

COST_BADGE = {
    "free": "✅",
    "free_partial": "⚠️",
    "free_limited": "⚠️",
    "contact_sales": "💰",
    "institutional": "💰",
    "unknown": "❓",
}


def build_table(tools, category):
    if not tools:
        return ""

    rows = []
    for t in tools:
        name = t.get("name", "")
        tool_type = t.get("type", "").upper()
        cost = COST_LABELS.get(t.get("cost", "unknown"), "❓")
        desc = t.get("description", "")[:60]
        install = t.get("installation", {})
        cmd = install.get("command", "") if isinstance(install, dict) else str(install)
        url = install.get("url", "") if isinstance(install, dict) else ""
        ref = f"[{name}](#{t['id'].replace('_', '-')})"
        access = cmd if cmd else (url if url else "—")
        access = access[:50]
        rows.append(f"| {ref} | {tool_type} | {cost} | {desc} | `{接入}` |")

    header = (
        "| 工具 | 类型 | 费用 | 描述 | 接入 |\n"
        "|------|------|------|------|------|"
    )
    return "\n".join([header] + rows)


def build_detail(tools):
    output = []
    for t in tools:
        tid = t["id"].replace("_", "-")
        name = t.get("name", "")
        tool_type = t.get("type", "")
        desc = t.get("description", "")
        github = t.get("github", "")
        official = t.get("official_url", "")
        maintainer = t.get("maintainer", "")
        cost_note = t.get("pricing_note", "")
        install = t.get("installation", {})
        cmd = install.get("command", "") if isinstance(install, dict) else ""
        url = install.get("url", "") if isinstance(install, dict) else ""
        inputs = t.get("input", {})
        outputs = t.get("output", {})

        # Build source lines
        sources = []
        if github:
            sources.append(f"**GitHub**：[{github}](https://github.com/{github.replace('github.com/', '')})")
        if official and "github" not in official.lower():
            if url and "http" in str(url):
                sources.append(f"**地址**：[{official}]({url})")
            else:
                sources.append(f"**地址**：{official}")
        if maintainer and maintainer not in sources:
            sources.append(f"**维护方**：{maintainer}")

        # Build input/output
        io_parts = []
        if inputs:
            intent = inputs.get("intent", "")
            if intent:
                io_parts.append(f"**输入**：{intent}")
        if outputs:
           覆盖 = outputs.get("覆盖", [])
            fmt = outputs.get("format", "")
            if 覆盖:
                io_parts.append(f"**输出覆盖**：{' / '.join(覆盖[:5])}")
            if fmt:
                io_parts.append(f"**输出格式**：{fmt}")

        output.append(f"### {name}\n")
        output.append(f"**类型**：{tool_type.capitalize()}  ")
        if cost_note:
            output.append(f"| {cost_note}")
        output.append("\n")
        if sources:
            output.append("\n".join(sources) + "\n")
        if io_parts:
            output.append("\n".join(io_parts) + "\n")
        if cmd:
            output.append(f"\n**安装**：\n```bash\n{cmd}\n```\n")
        elif url and "http" in str(url):
            output.append(f"\n**接入**：[{url}]({url})\n")
        output.append("---\n\n")

    return "".join(output)


def generate_category_sections(tools):
    sections = []
    cats_order = ["market_data", "sentiment", "analysis", "trading", "research", "news"]

    for cat in cats_order:
        cat_tools = [t for t in tools if t.get("category") == cat]
        if not cat_tools:
            continue
        meta = CATEGORY_META.get(cat, {"emoji": "📦", "title": cat, "desc": ""})
        sections.append(f"### {meta['emoji']} {meta['title']}\n")
        sections.append(f"*{meta['desc']}*\n")
        sections.append(f"| 工具 | 类型 | 费用 | 描述 | 接入 |\n|------|------|------|------|------|")
        for t in cat_tools:
            name = t.get("name", "")
            tool_type = t.get("type", "").upper()
            cost = COST_BADGE.get(t.get("cost", "unknown"), "❓")
            desc = t.get("description", "")[:50]
            install = t.get("installation", {})
            cmd = install.get("command", "") if isinstance(install, dict) else str(install)
            url = install.get("url", "") if isinstance(install, dict) else ""
            接入 = cmd if cmd else (url if url else "—")
            接入 = 接入[:45]
            ref = f"[{name}](#{t['id'].replace('_', '-')})"
            sections.append(f"| {ref} | {tool_type} | {cost} | {desc} | `{接入}` |")
        sections.append("")

    return "\n".join(sections)


def generate_detail_sections(tools):
    cats_order = ["market_data", "sentiment", "analysis", "trading", "research", "news"]
    output = []
    for cat in cats_order:
        cat_tools = [t for t in tools if t.get("category") == cat]
        if not cat_tools:
            continue
        output.append(f"\n#### {CATEGORY_META.get(cat, {}).get('emoji', '')} {CATEGORY_META.get(cat, {}).get('title', cat)}\n")
        output.append(build_detail(cat_tools))
    return "".join(output)


def main():
    tools_path = "data/tools.json"
    readme_path = "README.md"
    llms_path = "llms.txt"

    with open(tools_path) as f:
        data = json.load(f)

    tools = data.get("tools", [])
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # --- Generate README ---
    cat_sections = generate_category_sections(tools)
    detail_sections = generate_detail_sections(tools)

    readme_content = TEMPLATE_README.format(
        category_sections=cat_sections,
        update_time=update_time
    )

    # Append detail sections before the License section
    license_marker = "\n## 📄 License"
    if license_marker in readme_content:
        readme_content = readme_content.replace(
            license_marker,
            f"## 工具详情\n{detail_sections}\n{license_marker}"
        )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✅ README.md 生成完成 ({len(tools)} 个工具)")

    # --- Generate llms.txt ---
    llms_categories = []
    for cat in ["market_data", "sentiment", "analysis", "trading", "research"]:
        cat_tools = [t for t in tools if t.get("category") == cat]
        if not cat_tools:
            continue
        meta = CATEGORY_META.get(cat, {"title": cat})
        lines = [f"### {meta.get('emoji','')} {meta.get('title', cat)}"]
        for t in cat_tools:
            cost = COST_BADGE.get(t.get("cost", "unknown"), "❓")
            lines.append(f"| {t['name']} | {t.get('type','').upper()} | {cost} | {t.get('description','')[:50]} |")
        llms_categories.append("\n".join(lines))

    llms_content = f"""# llms.txt — Awesome FinAI Tools

## 网站/仓库简介

Awesome FinAI Tools 是中国金融 AI 工具全景图，收录可接入 AI Agent 的 Market Data MCP、量化框架、券商 Skills、交易接口、数据 API。每周自动巡检 GitHub / npm / PyPI 更新。最后更新：{update_time}。

## 核心页面

- [README](https://github.com/lj22503/awesome-finai-tools) — 完整工具清单
- [工具数据](data/tools.json) — 结构化 JSON 格式（机器可读）
- [Agent Skill](SKILL.md) — AI Agent 接入指南
- [贡献指南](CONTRIBUTING.md) — 如何提交新工具
- [更新日志](CHANGELOG.md) — 版本变更记录

## 工具分类

{chr(10).join(llms_categories)}

## 品牌关键词

金融 AI、A股、量化交易、Market Data MCP、Skill、OpenClaw、投研 Agent、基金分析、ETF、龙虎榜、北向资金、技术分析、因子挖掘、量化策略、回测

## 联系方式

- GitHub Issues: https://github.com/lj22503/awesome-finai-tools/issues
- 提交新工具: Pull Request 或 Issue
"""

    with open(llms_path, "w", encoding="utf-8") as f:
        f.write(llms_content)
    print(f"✅ llms.txt 生成完成")


if __name__ == "__main__":
    main()

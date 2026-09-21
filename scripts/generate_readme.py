#!/usr/bin/env python3
"""
从 data/tools.json + data/institution-skills.json + data/institution-dynamics.json
自动生成 README.md 和 llms.txt

每次数据文件更新后运行：
    python scripts/generate_readme.py

本脚本是 README / llms.txt 的唯一生成入口（single source of truth）：
- README.md 的「工具分类」「工具详情」「机构 Skill 矩阵」「机构 Skill 动态」
  全部由数据文件驱动，禁止手工修改 README.md。
- llms.txt 同步生成，含结构化分类表与 SEO 关键词段。
"""

import json
import re
import sys
from datetime import datetime

REPO_SLUG = "lj22503/awesome-finai-tools-zn"

TOOLS_PATH = "data/tools.json"
INSTITUTIONS_PATH = "data/institution-skills.json"
DYNAMICS_PATH = "data/institution-dynamics.json"
CLI_ORDER = ["market_data", "sentiment", "analysis", "trading", "research", "news"]

CATEGORY_META = {
    "market_data": {
        "emoji": "📊",
        "title": "Market Data（行情数据）",
        "desc": "实时行情、历史 K 线、资金流向、龙虎榜、北向资金、板块与财务快照",
    },
    "sentiment": {
        "emoji": "💬",
        "title": "Sentiment（舆情/社区）",
        "desc": "雪球、同花顺、全平台热点聚合与舆情监控",
    },
    "analysis": {
        "emoji": "📈",
        "title": "Analysis（分析与因子）",
        "desc": "Alpha 因子挖掘、量化分析、技术指标、选股筛选",
    },
    "trading": {
        "emoji": "🔄",
        "title": "Trading（交易执行）",
        "desc": "量化策略回测、模拟交易、实盘接口、交易智能体",
    },
    "research": {
        "emoji": "🔬",
        "title": "Research（投研）",
        "desc": "研报解读、宏观数据、基金分析、多 Agent 投研、券商官方 Skill",
    },
    "news": {
        "emoji": "📰",
        "title": "News（新闻资讯）",
        "desc": "财经新闻、公告、快讯",
    },
}

TYPE_LABEL = {
    "cli": "CLI",
    "mcp": "MCP",
    "python_lib": "Python",
    "framework": "框架",
    "skill": "Skill",
    "api": "API",
    "channel": "Channel",
}

COST_BADGE = {
    "free": "✅ 免费",
    "free_partial": "⚠️ 免费部分",
    "free_tier": "⚠️ 免费额度",
    "free_limited": "⚠️ 限时免费",
    "freemium": "⚠️ 免费增值",
    "contact_sales": "💰 联系销售",
    "institutional": "💰 机构付费",
    "expensive": "💰 付费",
    "unknown": "❓ 未知",
}

COST_SHORT = {
    "free": "✅",
    "free_partial": "⚠️",
    "free_tier": "⚠️",
    "free_limited": "⚠️",
    "freemium": "⚠️",
    "contact_sales": "💰",
    "institutional": "💰",
    "expensive": "💰",
    "unknown": "❓",
}

FEATURED = [
    ("零配置查行情", "`opencli eastmoney quote`", "安装即用，秒出结果"),
    ("同花顺官方数据", "`Financial-API`", "官方 MCP/API/CLI，覆盖行情/财报/涨停"),
    ("多维度 A 股数据（MCP）", "`ashare-mcp`", "30 个 tool，akshare 主源 + 多源降级"),
    ("免费历史 K 线", "`baostock`", "1990 年至今，无需注册"),
    ("零鉴权 A 股中台", "`TradeX Hub`", "129 个 MCP 工具，多源自动降级"),
    ("量化策略回测", "`qtrade`", "15 种策略 + 完整回测引擎"),
    ("多 Agent 投研", "`TradingAgents-astock`", "7 位分析师 A 股规则辩论"),
    ("LLM 因子挖掘", "`QuantaAlpha`", "LLM + 进化策略自动演化 Alpha"),
    ("舆情监控", "`TrendRadar`", "多平台热点聚合 + 多渠道推送 + MCP"),
    ("基金深度分析", "`盈米 MCP`", "69 个 MCP 工具，组合回测"),
]

TOOLCHAIN = [
    ("awesome-finai-tools-zn", "数据底座", "提供工具清单 + 机构 Skill 数据"),
    ("invest-brain", "工具推荐引擎", "基于场景自动推荐工具"),
    ("investment-buddy-pet", "人格化投顾", "按投资人格匹配工具箱"),
    ("SoloAdvisor-Toolkit", "投顾流程工具包", "KYC → 配置 → 组合 → 报告"),
    ("knowledge-workflow", "知识管理", "收集 → 打标 → 存储 → 产出"),
]

SEO_SCENES = [
    "A股行情", "实时行情", "历史K线", "资金流向", "龙虎榜", "北向资金",
    "涨停梯队", "量化回测", "因子挖掘", "Alpha因子", "舆情监控", "基金分析",
    "研报解读", "多Agent投研", "选股筛选", "财报分析",
]

SEO_PLATFORMS = [
    "OpenClaw", "Claude", "Cursor", "Codex", "WorkBuddy", "Coze", "Dify",
    "豆包", "千问", "华为小艺", "IMA", "ChatGPT",
]

SEO_DEMANDS = [
    "查股票", "安装MCP", "免费行情数据", "Python量化", "量化策略",
    "券商Skill", "MCP Server 推荐", "A股数据源对比",
]

SEO_BRANDS = [
    "东方财富", "同花顺", "华泰", "中金", "广发", "国信", "国泰海通", "兴业证券",
    "雪球", "Wind", "Tushare", "AKShare", "BaoStock", "腾讯", "阿里", "蚂蚁",
]


# ---------------------------------------------------------------- helpers

def slugify(name: str) -> str:
    """复刻 GitHub 标题锚点算法，保证 README 内部链接可用。"""
    s = name.strip().lower()
    s = re.sub(r"[^\w\u4e00-\u9fff \-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s


def type_label(t: dict) -> str:
    return TYPE_LABEL.get(t.get("type", ""), (t.get("type") or "").upper())


def cost_badge(t: dict) -> str:
    return COST_BADGE.get(t.get("cost", "unknown"), "❓ 未知")


def cost_short(t: dict) -> str:
    return COST_SHORT.get(t.get("cost", "unknown"), "❓")


def install_obj(t: dict) -> dict:
    inst = t.get("installation", {})
    return inst if isinstance(inst, dict) else {"command": str(inst)}


def access_text(t: dict) -> str:
    inst = install_obj(t)
    cmd = inst.get("command", "")
    url = inst.get("url", "")
    if cmd:
        return cmd
    if url:
        return url
    return "—"


def trunc(text: str, n: int) -> str:
    text = (text or "").strip()
    return text if len(text) <= n else text[: n - 1] + "…"


# ---------------------------------------------------------------- README

TEMPLATE_README = """# Awesome FinAI Tools
### 中国金融 AI 工具全景图

[![Stars](https://img.shields.io/github/stars/{repo_slug}?style=flat-square)](https://github.com/{repo_slug})
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)
[![Tools](https://img.shields.io/badge/工具-{tool_count}-blue?style=flat-square)](#工具分类)
[![更新](https://img.shields.io/badge/数据更新-{data_date}-brightgreen?style=flat-square)](#每周自动更新)

> 本仓库收录**中国金融 AI 工具**，包括 **Market Data MCP**、**量化框架**、**券商 Skills**、**金融 CLI**、**Python 金融库**。覆盖 **A股 / 港股 / 基金 / 期货** 行情数据、量化回测、因子挖掘、舆情分析、投研等场景。支持 **OpenClaw / Claude / Cursor / Codex / WorkBuddy / Coze** 等 AI Agent 平台。每周自动巡检更新。

[📋 完整工具清单](#工具分类) · [🔍 工具详情](#工具详情) · [🚀 快速上手](#快速上手) · [🤖 Agent 接入](#agent-接入) · [🏢 机构 Skill 矩阵](#-机构-skill-矩阵) · [📝 贡献指南](./CONTRIBUTING.md) · [📄 llms.txt](./llms.txt)

---

## 🔍 搜索关键词

> 本页可被以下搜索词命中（AI Agent / 搜索引擎 / GitHub 站内搜索）

**工具类型**：{seo_types}

**金融场景**：{seo_scenes}

**应用平台**：{seo_platforms}

**具体需求**：{seo_demands}

**机构/品牌**：{seo_brands}

---

## 🔥 精选推荐（新手首选）

| 场景 | 推荐工具 | 理由 |
|------|---------|------|
{featured_rows}

---

## 工具分类

{category_sections}

---

## 工具详情

{detail_sections}

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

> {institution_intro}

{institution_matrix}

{institution_sources}

> 📊 完整数据见 [data/institution-skills.json](./data/institution-skills.json)

## 📡 机构 Skill 动态

> 最近更新：**{dynamics_date}** | 来源：{dynamics_source}

{institution_dynamics}

---

## 🔗 工具链联动

本仓库是 FinAI 工具生态的一部分，与其他仓库协作：

| 仓库 | 定位 | 与本仓库的关系 |
|------|------|---------------|
{toolchain_rows}

## 📄 License

MIT — 详见 [LICENSE](./LICENSE)

---

*本文件由 `scripts/generate_readme.py` 自动从 `data/tools.json` / `data/institution-skills.json` / `data/institution-dynamics.json` 生成，最后更新：{update_time}*
"""


def generate_featured() -> str:
    return "\n".join(f"| **{s}** | {t} | {r} |" for s, t, r in FEATURED)


def generate_toolchain() -> str:
    rows = []
    for name, role, rel in TOOLCHAIN:
        rows.append(f"| [{name}](https://github.com/lj22503/{name}) | {role} | {rel} |")
    return "\n".join(rows)


def generate_category_sections(tools) -> str:
    out = []
    for cat in CLI_ORDER:
        cat_tools = [t for t in tools if t.get("category") == cat]
        if not cat_tools:
            continue
        meta = CATEGORY_META.get(cat, {"emoji": "📦", "title": cat, "desc": ""})
        out.append(f"### {meta['emoji']} {meta['title']}\n")
        out.append(f"*{meta['desc']}*\n")
        out.append("| 工具 | 类型 | 费用 | 描述 | 接入 |")
        out.append("|------|------|------|------|------|")
        for t in cat_tools:
            name = t.get("name", "")
            ref = f"[{name}](#{slugify(name)})"
            out.append(
                f"| {ref} | {type_label(t)} | {cost_short(t)} | "
                f"{trunc(t.get('description', ''), 56)} | `{trunc(access_text(t), 44)}` |"
            )
        out.append("")
    return "\n".join(out)


def generate_detail_blocks(tools) -> str:
    out = []
    for cat in CLI_ORDER:
        cat_tools = [t for t in tools if t.get("category") == cat]
        if not cat_tools:
            continue
        meta = CATEGORY_META.get(cat, {"emoji": "📦", "title": cat})
        out.append(f"\n#### {meta['emoji']} {meta['title']}\n")
        for t in cat_tools:
            name = t.get("name", "")
            inst = install_obj(t)
            out.append(f"### {name}\n")
            out.append(f"**类型**：{type_label(t)}　|　**费用**：{cost_badge(t)}  ")
            pricing_note = t.get("pricing_note", "")
            if pricing_note:
                out.append(f"**费用说明**：{pricing_note}  ")
            github = t.get("github", "")
            official = t.get("official_url", "")
            if github:
                out.append(f"**GitHub**：[{github}](https://{github})  ")
            elif official:
                out.append(f"**地址**：[{official}]({official})  ")
            if github and official and official not in f"https://{github}":
                out.append(f"**官网**：[{official}]({official})  ")
            if t.get("maintainer"):
                out.append(f"**维护方**：{t['maintainer']}  ")
            out.append("")
            out.append(f"{t.get('description', '')}\n")

            inp = t.get("input", {})
            if isinstance(inp, dict) and inp:
                items = " / ".join(f"{k}={v}" for k, v in list(inp.items())[:4])
                out.append(f"**输入**：{trunc(items, 200)}  ")
            outp = t.get("output", {})
            if isinstance(outp, dict) and outp:
                if outp.get("覆盖"):
                    out.append(f"**输出覆盖**：{' / '.join(outp['覆盖'][:8])}  ")
                if outp.get("fields"):
                    out.append(f"**输出字段**：{trunc(' / '.join(outp['fields'][:10]), 200)}  ")
                if outp.get("format"):
                    out.append(f"**输出格式**：{outp['format']}  ")
            acc = t.get("access", {})
            if isinstance(acc, dict) and acc.get("method"):
                out.append(f"**接入方式**：{acc['method']}  ")
            if t.get("capabilities"):
                out.append(f"**核心能力**：{' / '.join(t['capabilities'])}  ")
            out.append("")

            if inst.get("command"):
                out.append("**安装**：\n```bash\n" + inst["command"] + "\n```\n")
            elif inst.get("url"):
                out.append(f"**接入**：[{inst['url']}]({inst['url']})\n")
            if t.get("usage"):
                lang = t.get("usage_lang", "bash")
                out.append(f"**使用**：\n```{lang}\n" + "\n".join(t["usage"]) + "\n```\n")
            out.append("---\n")
    return "\n".join(out)


def generate_institution_matrix(institutions, data_date) -> str:
    platform_pool = []
    for inst in institutions:
        for s in inst.get("skills", []):
            for p in re.split(r"\s*/\s*", s.get("platform", "")):
                p = p.strip()
                if p and p not in platform_pool:
                    platform_pool.append(p)

    rows = [
        "| 机构 | 类型 | Skill 数量 | 核心能力 | 接入平台 | 获取方式 |",
        "|------|------|-----------|---------|---------|---------|",
    ]
    for inst in institutions:
        skills = inst.get("skills", [])
        name = inst.get("institution_name", "")
        platforms, gets = [], []
        for s in skills:
            for p in re.split(r"\s*/\s*", s.get("platform", "")):
                p = p.strip()
                if p and p not in platforms:
                    platforms.append(p)
            g = s.get("install_method", "")
            if g and g not in gets:
                gets.append(g)
        abilities = " / ".join(s.get("skill_name", "") for s in skills[:4])
        rows.append(
            f"| **{name}** | {inst.get('category', '')} | {len(skills)} 个 | "
            f"{trunc(abilities, 60)} | {trunc(' / '.join(platforms[:5]), 52) or '—'} | "
            f"{trunc(' / '.join(gets[:1]), 40) or '—'} |"
        )
    return "\n".join(rows)


def generate_institution_sources(institutions) -> str:
    """机构 Skill 权威信源表（可点击直达）"""
    rows = []
    for inst in institutions:
        sources = inst.get("sources") or []
        if not sources:
            continue
        links = " · ".join(
            f"[{s.get('title', '信源')}]({s.get('url', '')})"
            for s in sources
            if s.get("url")
        )
        if links:
            rows.append(f"| **{inst.get('institution_name', '')}** | {links} |")
    if not rows:
        return "_暂无信源数据_"
    return "\n".join([
        "### 🔗 权威信源（可点击直达）",
        "",
        "> 机构 Skill 条目的公开佐证来源，均已逐一校验可访问；官方页面与主流媒体报道优先。",
        "",
        "| 机构 | 信源 |",
        "|------|------|",
        *rows,
    ])


def generate_institution_sources_plain(institutions) -> str:
    """llms.txt 用信源清单（纯文本 + 绝对链接）"""
    out = []
    for inst in institutions:
        sources = inst.get("sources") or []
        if not sources:
            continue
        out.append(f"- {inst.get('institution_name', '')}")
        for s in sources:
            if s.get("url"):
                out.append(f"  - {s.get('title', '信源')}: {s['url']}")
    return "\n".join(out) if out else "_暂无信源数据_"


def generate_institution_dynamics(dyn) -> str:
    if not dyn:
        return "_暂无动态数据_"
    out = []
    if dyn.get("changes"):
        out.append("### 变化摘要\n")
        for c in dyn["changes"]:
            out.append(f"- {c}")
        out.append("")
    if dyn.get("trends"):
        out.append("### 趋势评论\n")
        for t in dyn["trends"]:
            out.append(f"**{t.get('title', '')}**\n")
            out.append(f"{t.get('body', '')}\n")
    if dyn.get("insight"):
        out.append("**对开发者的启示**：" + dyn["insight"] + "\n")
    return "\n".join(out)


def build_seo_types(tools) -> str:
    labels = []
    for t in tools:
        lb = type_label(t)
        if lb not in labels:
            labels.append(lb)
    labels += ["MCP Server", "Python金融库", "量化框架"]
    return " ".join(f"`{x}`" for x in labels)


def render_readme(tools, institutions, dyn, data_date) -> str:
    return TEMPLATE_README.format(
        repo_slug=REPO_SLUG,
        tool_count=len(tools),
        data_date=data_date,
        seo_types=build_seo_types(tools),
        seo_scenes=" ".join(f"`{x}`" for x in SEO_SCENES),
        seo_platforms=" ".join(f"`{x}`" for x in SEO_PLATFORMS),
        seo_demands=" ".join(f"`{x}`" for x in SEO_DEMANDS),
        seo_brands=" ".join(f"`{x}`" for x in SEO_BRANDS),
        featured_rows=generate_featured(),
        category_sections=generate_category_sections(tools),
        detail_sections=generate_detail_blocks(tools),
        institution_intro=(
            f"截至 {data_date}，国内头部券商中已有半数以上落地 Skill 产品，"
            "金融数据商、基金公司与大厂 Agent 平台同步加速。以下为核心机构 Skill 矩阵："
        ),
        institution_matrix=generate_institution_matrix(institutions, data_date),
        institution_sources=generate_institution_sources(institutions),
        dynamics_date=dyn.get("last_updated", data_date) if dyn else data_date,
        dynamics_source=dyn.get("source", "公开信息整理") if dyn else "公开信息整理",
        institution_dynamics=generate_institution_dynamics(dyn),
        toolchain_rows=generate_toolchain(),
        update_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


# ---------------------------------------------------------------- llms.txt

def render_llms(tools, institutions, data_date) -> str:
    blocks = []
    for cat in CLI_ORDER:
        cat_tools = [t for t in tools if t.get("category") == cat]
        if not cat_tools:
            continue
        meta = CATEGORY_META.get(cat, {"emoji": "📦", "title": cat})
        lines = [f"### {meta['emoji']} {meta['title']}", "", "| 工具 | 类型 | 费用 | 一句话描述 |", "|------|------|------|-----------|"]
        for t in cat_tools:
            lines.append(
                f"| {t.get('name', '')} | {type_label(t)} | {cost_short(t)} | "
                f"{trunc(t.get('description', ''), 46)} |"
            )
        blocks.append("\n".join(lines))

    inst_lines = ["| 机构 | 类型 | Skill 数量 | 核心能力 |", "|------|------|-----------|---------|"]
    for inst in institutions:
        skills = inst.get("skills", [])
        abilities = " / ".join(s.get("skill_name", "") for s in skills[:4])
        inst_lines.append(
            f"| {inst.get('institution_name', '')} | {inst.get('category', '')} | "
            f"{len(skills)} | {trunc(abilities, 50)} |"
        )

    keywords = SEO_SCENES + SEO_PLATFORMS + SEO_DEMANDS + SEO_BRANDS

    return f"""# llms.txt — Awesome FinAI Tools

## 网站/仓库简介

Awesome FinAI Tools 是中国金融 AI 工具全景图（{REPO_SLUG}），收录可接入 AI Agent 的 Market Data MCP、量化框架、券商 Skills、交易接口、数据 API，共 {len(tools)} 个工具、{len(institutions)} 家机构 Skill。每周自动巡检 GitHub / npm / PyPI 更新。数据更新日期：{data_date}。

## 核心页面

- [README](https://github.com/{REPO_SLUG}) — 完整工具清单、工具详情、机构 Skill 矩阵
- [工具数据](data/tools.json) — 结构化 JSON 格式（机器可读）
- [机构 Skill 数据](data/institution-skills.json) — 券商/基金/数据商/平台 Skill 矩阵
- [机构动态](data/institution-dynamics.json) — 机构 Skill 变化摘要与趋势
- [Agent Skill](SKILL.md) — AI Agent 接入指南
- [贡献指南](CONTRIBUTING.md) — 如何提交新工具
- [更新日志](CHANGELOG.md) — 版本变更记录

## 工具分类（6 大类）

{chr(10).join(blocks)}

## 机构 Skill 矩阵

{chr(10).join(inst_lines)}

## 机构 Skill 信源（可点击直达）

{generate_institution_sources_plain(institutions)}

## 搜索关键词（命中词）

中国金融 AI 工具、金融 MCP、A股 Market Data、量化交易工具、Python 金融库、免费行情数据、Skill 投顾 Agent、龙虎榜工具、北向资金 API、基金分析 MCP、OpenClaw 金融 Skills、券商 AI 助手、同花顺官方 API、AKShare Tushare 对比、BaoStock 免费数据、量化回测框架、因子挖掘工具、舆情分析、WorkBuddy 金融、千问金融智能体、Agentar、ChatGPT 量化、Cursor 金融开发、Claude Code 投研

关键词明细：{"、".join(keywords)}

## 联系方式

- GitHub Issues: https://github.com/{REPO_SLUG}/issues
- 提交新工具: Pull Request 或 Issue
"""


def main():
    try:
        with open(TOOLS_PATH, encoding="utf-8") as f:
            tools_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 找不到 {TOOLS_PATH}，请在仓库根目录运行本脚本")
        sys.exit(1)

    tools = tools_data.get("tools", [])
    data_date = tools_data.get("last_updated") or datetime.now().strftime("%Y-%m-%d")

    institutions = []
    try:
        with open(INSTITUTIONS_PATH, encoding="utf-8") as f:
            institutions = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ 未找到 {INSTITUTIONS_PATH}，跳过机构矩阵")

    dyn = None
    try:
        with open(DYNAMICS_PATH, encoding="utf-8") as f:
            dyn = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ 未找到 {DYNAMICS_PATH}，跳过机构动态")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(render_readme(tools, institutions, dyn, data_date))
    print(f"✅ README.md 生成完成（{len(tools)} 个工具 / {len(institutions)} 家机构）")

    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(render_llms(tools, institutions, data_date))
    print("✅ llms.txt 生成完成")


if __name__ == "__main__":
    main()

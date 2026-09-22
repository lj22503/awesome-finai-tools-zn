#!/usr/bin/env python3
"""
awesome-finai-tools-zn 每周巡检脚本（FinAI 工具维度）

数据源（全部走公开只读 API，不依赖 gh CLI）：
  1. GitHub Search API    —— 金融 / 量化 / MCP 相关仓库
  2. npm Registry Search  —— 金融类 CLI / MCP / SDK
  3. PyPI                 —— 无公开搜索 API，Python 生态候选由 GitHub `language:python` 维度覆盖

产物（待审隔离，不污染正式清单）：
  - data/pending-review.json        候选池（status=pending_review，人工确认后才并入 tools.json）
  - data/weekly-report-<date>.md    本周巡检报告

设计原则：
  - 自动巡检的过滤精度不足以直接进首页，候选一律写入待审池
  - tools.json 只由人工确认后修改，本脚本永不直写正式数据
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

REPO_DIR = Path(__file__).parent.parent
TOOLS_JSON = REPO_DIR / "data" / "tools.json"
PENDING_REVIEW_JSON = REPO_DIR / "data" / "pending-review.json"

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
GH_HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "awesome-finai-tools-zn-weekly"}
if TOKEN:
    GH_HEADERS["Authorization"] = f"token {TOKEN}"

# GitHub 搜索关键词（金融相关；含中文以覆盖国内项目）
GITHUB_QUERIES = [
    "stock market China AI MCP server",
    "A股 量化 AI agent MCP",
    "chinese finance CLI",
    "quantitative trading framework China",
    "finance mcp server",
    "stock market data python language:python",
]

# npm 搜索关键词
NPM_KEYWORDS = [
    "finance mcp", "stock mcp", "a-share", "quant trading",
    "xueqiu", "eastmoney", "tushare", "akshare", "futu",
]

# ---- 过滤规则 ----------------------------------------------------------
# 金融信号：命中其一才可能是金融工具
FIN_SIGNALS = [
    "financ", "stock", "equity", "trading", "trader", "quant",
    "invest", "portfolio", "backtest", "market data", "ticker", "candlestick",
    "行情", "股票", "股市", "量化", "金融", "证券", "券商", "基金",
    "债券", "期货", "港股", "美股", "a股", "投研", "财报", "选股",
    "炒股", "资产配置", "数据源",
    "xueqiu", "tushare", "akshare", "eastmoney", "baostock", "futu", "joinquant",
]

# 工具形态信号：仓库得是个「能用的东西」，不是纯资讯 / 教程
TOOL_SIGNALS = [
    "mcp", "api", "sdk", "cli", "server", "library", "framework",
    "agent", "dataset", "wrapper", "client", "connector", "plugin",
    "skill", "tool", "bot", "接口", "工具", "函数库", "数据源", "平台",
]

# 明确排除：非工具类 / 易误判领域
BLOCKLIST = [
    "awesome-list", "awesome list", "tutorial", "course", "教材",
    "interview", "leetcode", "cheat sheet", "cheatsheet", "homework",
    "assignment", "student", "slides", "lecture", "notes for",
    "photo", "photography", "wallpaper", "image gallery",
    "book", "ebook", "novel", "trading card", "stock footage",
]

MIN_STARS = 5

# 排除本仓库自身（避免自引用进候选池）
SELF_REPOS = {"lj22503/awesome-finai-tools-zn"}

# 中国市场信号：用于给候选标注 scope（cn / global），便于人工按定位筛选
CN_SIGNALS = [
    "a股", "a-share", "ashare", "沪深", "港股", "美股", "中概",
    "雪球", "xueqiu", "东方财富", "eastmoney", "同花顺", "ths",
    "tushare", "akshare", "baostock", "聚宽", "joinquant", "米筐", "ricequant",
    "中国", "china", "chinese", "cn_", "_cn", "-cn", "国内",
    "腾讯", "新浪", "财新", "wind", "万得", "通达信", "中金", "招商证券",
    "华泰", "国泰", "中信", "可转债", "龙虎榜", "北向",
]


def _norm(text: str) -> str:
    return (text or "").lower()


def detect_scope(name: str, description: str) -> str:
    """标注候选面向的市场：cn（中国）/ global（海外）"""
    text = _norm(name) + " " + _norm(description)
    return "cn" if _hit(text, CN_SIGNALS) else "global"


def _hit(text: str, words) -> bool:
    return any(w in text for w in words)


def is_finance_tool(name: str, description: str) -> bool:
    """GitHub 仓库判定：金融信号 + 工具信号，且不在黑名单"""
    text = _norm(name) + " " + _norm(description)
    if _hit(text, BLOCKLIST):
        return False
    if not _hit(text, FIN_SIGNALS):
        return False
    if not _hit(text, TOOL_SIGNALS):
        return False
    return True


def is_finance_package(name: str, description: str) -> bool:
    """npm 包判定：金融信号 + 工具形态，且不在黑名单、不是空壳包"""
    desc = (description or "").strip()
    # 空描述 / 脚手架模板包直接剔除
    if len(desc) < 8:
        return False
    text = _norm(name) + " " + _norm(desc)
    if _hit(text, BLOCKLIST):
        return False
    if not _hit(text, FIN_SIGNALS):
        return False
    if not _hit(text, TOOL_SIGNALS):
        return False
    return True


# ---- 数据源 ------------------------------------------------------------
def search_github(days: int = 7) -> list:
    """GitHub Search API：搜索近期有推送的金融相关仓库"""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    results, seen = [], set()

    for query in GITHUB_QUERIES:
        try:
            resp = requests.get(
                "https://api.github.com/search/repositories",
                headers=GH_HEADERS,
                params={
                    "q": f"{query} pushed:>{since}",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 10,
                },
                timeout=30,
            )
            if resp.status_code != 200:
                print(f"  ⚠ 搜索失败({resp.status_code}): {query} | {resp.text[:120]}")
                time.sleep(2)
                continue

            items = resp.json().get("items", []) or []
            for it in items:
                full_name = it.get("full_name", "")
                if not full_name or full_name in seen:
                    continue
                seen.add(full_name)
                results.append({
                    "name": it.get("name", ""),
                    "full_name": full_name,
                    "description": it.get("description") or "",
                    "url": it.get("html_url", ""),
                    "stars": it.get("stargazers_count", 0),
                    "updated": it.get("pushed_at", ""),
                    "language": it.get("language") or "",
                })
            print(f"  · {query} → {len(items)} 条")
        except Exception as exc:
            print(f"  ⚠ 搜索异常: {query}: {exc}")
        time.sleep(1)

    return results


def check_npm_packages() -> list:
    """npm Registry Search API：搜索金融相关包"""
    results, seen = [], set()

    for keyword in NPM_KEYWORDS:
        try:
            resp = requests.get(
                "https://registry.npmjs.org/-/v1/search",
                params={"text": keyword, "size": 10},
                timeout=20,
            )
            if resp.status_code != 200:
                print(f"  ⚠ npm 搜索失败({resp.status_code}): {keyword}")
                continue

            payload = resp.json()
            # 兼容两种返回：{"objects":[...]} 或直接 list
            objects = payload.get("objects", []) if isinstance(payload, dict) else payload
            if not isinstance(objects, list):
                objects = []

            for obj in objects:
                if not isinstance(obj, dict):
                    continue
                pkg = obj.get("package") or {}
                name = pkg.get("name", "")
                if not name or name in seen:
                    continue
                seen.add(name)
                results.append({
                    "name": name,
                    "version": pkg.get("version", ""),
                    "description": pkg.get("description") or "",
                    "url": (pkg.get("links") or {}).get("npm", ""),
                    "date": pkg.get("date", ""),
                })
            print(f"  · {keyword} → {len(objects)} 条")
        except Exception as exc:
            print(f"  ⚠ npm 搜索异常: {keyword}: {exc}")
        time.sleep(0.5)

    return results


# ---- 比对与产出 ---------------------------------------------------------
def get_current_tools() -> list:
    with open(TOOLS_JSON, "r", encoding="utf-8") as f:
        return json.load(f).get("tools", [])


def get_current_names() -> set:
    """现有收录的仓库名归一化集合（用于去重）"""
    names = set()
    for tool in get_current_tools():
        for key in ("id", "name"):
            value = (tool.get(key) or "").strip().lower()
            if value:
                names.add(value)
                names.add(value.replace("github-", "").replace("_", "-"))
        gh = (tool.get("github") or "").strip().lower()
        if gh:
            names.add(gh)
            names.add(gh.split("/")[-1])
    return names


def find_new_github(repos: list, current_names: set) -> list:
    """从搜索结果中筛出「够格 + 未收录」的仓库"""
    new_tools = []
    for repo in repos:
        if repo["full_name"] in SELF_REPOS:
            continue
        if repo.get("stars", 0) < MIN_STARS:
            continue
        if not is_finance_tool(repo.get("name", ""), repo.get("description", "")):
            continue
        if repo["full_name"].lower() in current_names:
            continue
        if repo["name"].lower().replace("_", "-") in current_names:
            continue
        new_tools.append(repo)
    return new_tools


def find_new_npm(packages: list, current_names: set) -> list:
    new_pkgs = []
    for pkg in packages:
        if not is_finance_package(pkg.get("name", ""), pkg.get("description", "")):
            continue
        if pkg["name"].lower() in current_names:
            continue
        new_pkgs.append(pkg)
    return new_pkgs


def load_pending_review() -> dict:
    """读取待审清单；不存在则返回空结构（与 update_china_platforms.py 保持一致）"""
    if PENDING_REVIEW_JSON.exists():
        try:
            with open(PENDING_REVIEW_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": "", "last_updated": "",
        "note": "", "items": [], "npm_candidates": [],
        "institution_candidates": {}, "suspected_new_institutions": [],
        "github_candidates": [],
    }


def update_pending_review(github_new: list, npm_new: list) -> tuple:
    """
    将巡检结果写入 data/pending-review.json（不写 tools.json）。

    与 update_china_platforms.py 共用同一待审池：
      - GitHub 候选 → github_candidates
      - npm 候选    → npm_candidates（与国内平台巡检合并去重）
    返回 (新增 GitHub 条数, 新增 npm 条数)。
    """
    data = load_pending_review()
    today = datetime.now().strftime("%Y-%m-%d")

    existing_gh = {it.get("full_name") for it in data.get("github_candidates", [])}
    added_gh = 0
    for repo in github_new:
        if repo["full_name"] in existing_gh:
            continue
        data.setdefault("github_candidates", []).append({
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": (repo.get("description") or "")[:200],
            "link": repo.get("url", ""),
            "stars": repo.get("stars", 0),
            "language": repo.get("language", ""),
            "scope": detect_scope(repo.get("name", ""), repo.get("description", "")),
            "source": "github_search",
            "found_date": today,
            "status": "pending_review",
        })
        existing_gh.add(repo["full_name"])
        added_gh += 1

    existing_npm = {it.get("name") for it in data.get("npm_candidates", [])}
    added_npm = 0
    for pkg in npm_new:
        name = pkg.get("name", "")
        if not name or name in existing_npm:
            continue
        data.setdefault("npm_candidates", []).append({
            "name": name,
            "version": pkg.get("version", ""),
            "description": pkg.get("description", ""),
            "link": pkg.get("url", ""),
            "scope": detect_scope(name, pkg.get("description", "")),
            "source": "npm",
            "found_date": today,
            "status": "pending_review",
        })
        existing_npm.add(name)
        added_npm += 1

    data["version"] = today
    data["last_updated"] = today
    data["note"] = (
        "自动巡检发现的待审条目。人工确认后再并入 tools.json / institution-skills.json；"
        "本文件不参与 README / llms.txt 生成。"
    )

    with open(PENDING_REVIEW_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  待审池已更新: GitHub +{added_gh} / npm +{added_npm}")
    return added_gh, added_npm


def generate_report(new_github: list, new_npm: list, scanned: dict, pending_totals: dict) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# 📡 FinAI Tools 周报 — {today}",
        "",
        "> 自动生成 by [awesome-finai-tools-zn](https://github.com/lj22503/awesome-finai-tools-zn)",
        "",
        "---",
        "",
        "## 🔍 本周巡检概览",
        "",
        f"- GitHub Search：扫描 {scanned.get('github', 0)} 个仓库",
        f"- npm Registry：扫描 {scanned.get('npm', 0)} 个包",
        f"- 待审池累计：GitHub {pending_totals.get('github', 0)} 条 / npm {pending_totals.get('npm', 0)} 条",
        "",
    ]

    if not new_github and not new_npm:
        lines.extend([
            "## ✅ 本周无新增候选",
            "",
            "所有命中过滤规则的候选均已存在于待审池。",
            "",
        ])
    else:
        if new_github:
            lines.append(f"## 🆕 GitHub 新候选 ({len(new_github)} 个)")
            lines.append("")
            for repo in new_github[:15]:
                lines.append(f"- **{repo['name']}** ({repo['stars']} ⭐, {repo.get('language') or '—'})")
                if repo.get("description"):
                    lines.append(f"  {repo['description'][:100]}")
                lines.append(f"  → {repo.get('url', '')}")
            lines.append("")

        if new_npm:
            lines.append(f"## 🆕 npm 新候选 ({len(new_npm)} 个)")
            lines.append("")
            for pkg in new_npm[:15]:
                lines.append(f"- **{pkg['name']}** v{pkg.get('version', '')}")
                if pkg.get("description"):
                    lines.append(f"  {pkg['description'][:100]}")
            lines.append("")

    lines.extend([
        "---",
        "",
        "## 📋 处置说明",
        "",
        "以上候选仅进入 `data/pending-review.json` 待审池，**不参与** README / llms.txt 生成，"
        "也不影响首页徽章计数。人工确认后，再手动并入 `data/tools.json` 并归入正式分类。",
        "",
        f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ])
    return "\n".join(lines)


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FinAI Tools 周巡检开始")
    print(f"  工具目录: {REPO_DIR}")
    print(f"  GitHub token: {'已配置' if TOKEN else '未配置（限流 10 次/分钟）'}")

    current_names = get_current_names()
    print(f"  当前收录: {len(get_current_tools())} 个工具")

    print("\n1. GitHub Search API...")
    trending = search_github(days=7)
    print(f"  共命中 {len(trending)} 个仓库")

    print("\n2. npm Registry Search...")
    npm_all = check_npm_packages()
    print(f"  共命中 {len(npm_all)} 个包")

    print("\n3. 过滤与去重...")
    new_github = find_new_github(trending, current_names)
    new_npm = find_new_npm(npm_all, current_names)
    print(f"  GitHub 新候选 {len(new_github)} 个 / npm 新候选 {len(new_npm)} 个")

    print("\n4. 写入待审池...")
    added_gh, added_npm = update_pending_review(new_github, new_npm)

    pending = load_pending_review()
    report = generate_report(
        new_github, new_npm,
        scanned={"github": len(trending), "npm": len(npm_all)},
        pending_totals={
            "github": len(pending.get("github_candidates", [])),
            "npm": len(pending.get("npm_candidates", [])),
        },
    )
    report_file = REPO_DIR / "data" / f"weekly-report-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  报告已保存: {report_file}")

    print("\n✅ 周巡检完成（正式数据 tools.json 未改动）")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())

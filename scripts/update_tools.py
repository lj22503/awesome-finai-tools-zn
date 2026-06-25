#!/usr/bin/env python3
"""
awesome-finai-tools 每周巡检脚本
功能：
1. 检查 GitHub trending（量化/金融相关仓库）
2. 检查 npm 新增金融类 CLI
3. 检查 PyPI 新增金融类包
4. 检查 MCP 官方 registry 新增
5. 生成 diff 报告，发 PR
"""

import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
TOOLS_JSON = REPO_DIR / "data" / "tools.json"
GITHUB_CACHE = REPO_DIR / "data" / "github_trending_cache.json"

# GitHub 搜索关键词（金融相关）
FINANCE_QUERIES = [
    "stock market China AI MCP server",
    "A股 量化 AI agent MCP",
    "chinese finance CLI Python",
    "akshare tushare baostock new",
    "quantitative trading framework China",
]

TRENDING_KEYWORDS = [
    "quant", "trading", "stock", "finance", "market",
    "mcp", "agent", "ai", "china", "A股", "金融",
]


def get_current_tools() -> list:
    """读取当前 tools.json"""
    with open(TOOLS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("tools", [])


def get_current_ids() -> set:
    """获取当前所有工具 ID"""
    return {t["id"] for t in get_current_tools()}


def search_github_trending(days: int = 7) -> list:
    """搜索 GitHub trending 仓库"""
    results = []
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    for query in FINANCE_QUERIES:
        try:
            cmd = [
                "gh", "api", "search/repositories",
                "-q", f"{query} pushed:>{since}",
                "--sort", "stars", "--order", "desc",
                "-L", "10",
                "--jq", ".items[] | {name:.name, full_name:.full_name, description:.description, url:.html_url, stars:.stargazers_count, updated:.pushed_at}"
            ]
            output = subprocess.check_output(cmd, text=True, timeout=30)
            items = json.loads(f"[{output.strip()}]")
            results.extend(items)
        except subprocess.TimeoutExpired:
            print(f"  ⏱ 超时: {query}")
        except Exception as e:
            print(f"  ⚠ 搜索失败: {query}: {e}")
        time.sleep(1)

    # 去重
    seen = set()
    unique = []
    for r in results:
        if r["full_name"] not in seen and r.get("name"):
            seen.add(r["full_name"])
            unique.append(r)
    return unique


def check_npm_packages() -> list:
    """检查 npm 新增金融相关包"""
    results = []
    for keyword in ["finance", "stock", "market", "mcp", "xueqiu", "eastmoney"]:
        try:
            cmd = [
                "npm", "search", keyword,
                "--json", "--long", "--searchlimit", "5"
            ]
            output = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            if output.returncode == 0:
                data = json.loads(output.stdout)
                for pkg in list(data.get("objects", []))[:3]:
                    p = pkg.get("package", {})
                    results.append({
                        "name": p.get("name"),
                        "version": p.get("version"),
                        "description": p.get("description"),
                        "url": p.get("links", {}).get("npm"),
                    })
        except Exception as e:
            print(f"  ⚠ npm 搜索失败: {keyword}: {e}")
    return results


def check_pypi_packages() -> list:
    """检查 PyPI 新增金融相关包"""
    results = []
    for keyword in ["stock", "finance", "mcp", "akshare"]:
        try:
            cmd = ["pip", "index", "versions", keyword]
            output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL, timeout=15)
            if "Available versions:" in output:
                lines = output.strip().split("\n")
                name = lines[0].split()[0]
                desc = " ".join(lines[1].split()[:20]) if len(lines) > 1 else ""
                results.append({"name": name, "description": desc})
        except Exception:
            pass
    return results[:10]


def find_new_tools(trending: list, current_ids: set) -> list:
    """从 trending 中找出尚未收录的工具"""
    new_tools = []
    for repo in trending:
        name = repo.get("name", "")
        full_name = repo.get("full_name", "")
        desc = repo.get("description", "") or ""

        # 简单过滤
        if any(kw.lower() in (name + desc).lower() for kw in TRENDING_KEYWORDS):
            # 检查是否已收录（用 GitHub URL 做简单匹配）
            is_new = True
            for tid in current_ids:
                if tid in full_name.lower() or tid in name.lower():
                    is_new = False
                    break
            if is_new and name:
                new_tools.append({
                    "name": name,
                    "full_name": full_name,
                    "description": desc,
                    "url": repo.get("url", ""),
                    "stars": repo.get("stars", 0),
                    "updated": repo.get("updated", ""),
                })
    return new_tools


def generate_report(
    new_github: list,
    new_npm: list,
    new_pypi: list,
    existing_trending: list,
) -> str:
    """生成 Markdown 格式报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# 📡 FinAI Tools 周报 — {today}",
        "",
        f"> 自动生成 by [awesome-finai-tools](https://github.com/lj22503/awesome-finai-tools)",
        "",
        "---",
        "",
    ]

    if not new_github and not new_npm and not new_pypi:
        lines.extend(["## ✅ 本周无新增工具", "", "所有工具均为最新状态。", ""])
    else:
        if new_github:
            lines.append(f"## 🆕 GitHub 新发现 ({len(new_github)} 个)")
            lines.append("")
            for repo in new_github[:10]:
                lines.append(f"- **{repo['name']}** ({repo['stars']} ⭐)")
                if repo.get("description"):
                    lines.append(f"  {repo['description'][:80]}")
                lines.append(f"  → {repo.get('url', '')}")
            lines.append("")

        if new_npm:
            lines.append(f"## 🆕 npm 新增包 ({len(new_npm)} 个)")
            lines.append("")
            for pkg in new_npm[:5]:
                lines.append(f"- **{pkg['name']}** v{pkg.get('version','')}")
                if pkg.get("description"):
                    lines.append(f"  {pkg['description'][:80]}")
            lines.append("")

        if new_pypi:
            lines.append(f"## 🆕 PyPI 新增 ({len(new_pypi)} 个)")
            lines.append("")
            for pkg in new_pypi[:5]:
                lines.append(f"- **{pkg['name']}**")
                if pkg.get("description"):
                    lines.append(f"  {pkg['description'][:80]}")
            lines.append("")

    # 附：本周 trending 概览
    if existing_trending:
        lines.append("## 📊 本周 Trending 概览")
        lines.append("")
        for repo in existing_trending[:5]:
            lines.append(
                f"- [{repo['name']}]({repo.get('url','')}) "
                f"({repo.get('stars',0)}⭐)"
            )
        lines.append("")

    lines.extend([
        "---",
        f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ])
    return "\n".join(lines)


def update_tools_json(new_tools: list) -> None:
    """将新工具追加到 tools.json"""
    with open(TOOLS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 标记为待确认（pending_review）
    for repo in new_tools:
        new_entry = {
            "id": f"github-{repo['name'].lower().replace('-','_')}",
            "name": repo["name"],
            "category": "pending_review",
            "type": "framework",
            "description": repo.get("description", "")[:200],
            "input": {},
            "output": {"format": "待确认"},
            "access": {
                "method": "待确认",
                "auth_required": "待确认",
            },
            "installation": {
                "command": f"git clone {repo.get('url','')}"
            },
            "cost": "unknown",
            "official_url": repo.get("url", ""),
            "github": repo.get("full_name", ""),
            "stars": repo.get("stars", 0),
            "status": "pending_review",
            "found_date": datetime.now().strftime("%Y-%m-%d"),
            "tags": ["待分类"],
        }
        data["tools"].append(new_entry)

    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    data["version"] = datetime.now().strftime("%Y-%m-%d")

    with open(TOOLS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  ✅ 已将 {len(new_tools)} 个新工具追加到 tools.json")


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FinAI Tools 周巡检开始")
    print(f"  工具目录: {REPO_DIR}")

    current_ids = get_current_ids()
    print(f"  当前收录: {len(current_ids)} 个工具")

    # 1. GitHub trending
    print("\n1. 检查 GitHub trending...")
    trending = search_github_trending(days=7)
    print(f"  找到 {len(trending)} 个 trending 结果")

    # 2. npm
    print("\n2. 检查 npm...")
    npm_new = check_npm_packages()
    print(f"  找到 {len(npm_new)} 个 npm 包")

    # 3. PyPI
    print("\n3. 检查 PyPI...")
    pypi_new = check_pypi_packages()
    print(f"  找到 {len(pypi_new)} 个 PyPI 包")

    # 4. 找出新工具
    print("\n4. 对比现有工具...")
    new_tools = find_new_tools(trending, current_ids)
    print(f"  本周新增 {len(new_tools)} 个待收录工具")

    # 5. 生成报告
    report = generate_report(new_tools, npm_new, pypi_new, trending[:10])
    report_file = REPO_DIR / "data" / f"weekly-report-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n  报告已保存: {report_file}")

    # 6. 更新 tools.json
    if new_tools:
        update_tools_json(new_tools)

    print("\n✅ 周巡检完成")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())

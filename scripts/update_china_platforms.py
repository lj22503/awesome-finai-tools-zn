#!/usr/bin/env python3
"""
awesome-finai-tools-zn 国内平台巡检脚本
=========================================

功能：
1. ClawHub 金融类 Skill 巡检（搜索+最新上架过滤）
2. npm 金融类新包巡检（扩展中文关键词）
3. 对比现有 tools.json，生成新增候选列表
4. 生成 Markdown 周报

ClawHub API 文档: https://docs.openclaw.ai/clawhub/api
合规声明：仅使用公开只读端点，遵守限流规范，回链原始页面
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

# === ClawHub 配置 ===
# 遵守 ClawHub Public Catalog Reuse 规范:
# https://docs.openclaw.ai/clawhub/api
# - 仅使用公开只读端点
# - 缓存响应，不频繁轮询（此脚本周更）
# - 回链 ClawHub 原始页面
# - 不暗示官方背书
CLAWHUB_BASE = "https://clawhub.ai/api/v1"
USER_AGENT = "awesome-finai-tools-zn/1.0 (+https://github.com/lj22503/awesome-finai-tools-zn; weekly crawler)"

# 请求头
HEADERS = {
    "Accept": "application/json",
    "User-Agent": USER_AGENT,
}

# 金融关键词（ClawHub 搜索）
FINANCE_KEYWORDS = [
    "金融", "股票", "基金", "证券", "期货", "量化",
    "行情", "A股", "港股", "投资", "trading",
    "stock", "finance", "market data",
]

# 搜索命中后的二次过滤关键词（确保是金融/量化相关）
FINANCE_FILTER = [
    "金融", "股票", "基金", "证券", "期货", "量化", "行情",
    "A股", "港股", "美股", "投资", "交易", "trading",
    "stock", "finance", "quant", "market", "portfolio",
    "财报", "K线", "因子", "回测", "龙虎榜", "北向",
]


def load_existing_tools() -> tuple[list, set]:
    """读取当前 tools.json，返回 (工具列表, slug集合)"""
    with open(TOOLS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    tools = data.get("tools", [])

    # 用 slug + github 字段做去重
    slugs = set()
    for t in tools:
        slugs.add(t.get("id", ""))
        if t.get("github"):
            slugs.add(t["github"].lower().split("/")[-1])
        # clawhub slug
        if t.get("clawhub_slug"):
            slugs.add(t["clawhub_slug"])

    return tools, slugs


def clawhub_request(path: str, params: dict = None, max_retries: int = 3) -> requests.Response | None:
    """
    ClawHub API 请求封装。
    遵守限流：检查 X-RateLimit-* / 429 自动退避。
    """
    url = f"{CLAWHUB_BASE}/{path}"

    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params or {}, timeout=15, headers=HEADERS)

            if r.status_code == 429:
                retry_after = int(r.headers.get("Retry-After", 30))
                print(f"  ⏳ 限流 429，等待 {retry_after}s...")
                time.sleep(retry_after)
                continue

            # 检查速率余量（提前减速，避免触发 429）
            remaining = r.headers.get("X-RateLimit-Remaining")
            if remaining and int(remaining) < 5:
                reset_at = int(r.headers.get("X-RateLimit-Reset", 0))
                wait = max(reset_at - time.time(), 1) if reset_at else 10
                print(f"  ⏳ 速率余量不足(剩余{remaining})，等待 {int(wait)}s...")
                time.sleep(wait)

            r.raise_for_status()
            return r

        except requests.RequestException as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  🔄 重试 {attempt+1}/{max_retries} ({wait}s): {e}")
                time.sleep(wait)
            else:
                print(f"  ⚠ 最终失败: {e}")
                return None

    return None


def search_clawhub(keyword: str, limit: int = 10) -> list:
    """搜索 ClawHub 技能，返回 results 列表"""
    r = clawhub_request("search", params={"q": keyword, "limit": limit})
    if r:
        return r.json().get("results", [])
    return []


def get_recent_skills(limit: int = 50) -> list:
    """获取 ClawHub 最新上架的技能，返回 items 列表"""
    r = clawhub_request("skills", params={"limit": limit, "sort": "updated"})
    if r:
        return r.json().get("items", [])
    return []


def is_finance_related(item: dict) -> bool:
    """判断 skill 是否与金融/量化相关"""
    parts = [
        item.get("displayName") or "",
        item.get("summary") or "",
        item.get("description") or "",
    ]
    text = " ".join(parts).lower()
    return any(kw.lower() in text for kw in FINANCE_FILTER)


def match_existing(slug: str, existing_slugs: set) -> bool:
    """检查是否已收录"""
    if slug in existing_slugs:
        return True
    # 模糊匹配：部分 slug 相似
    for es in existing_slugs:
        if slug in es or es in slug:
            return True
    return False


def scan_clawhub_finance(existing_slugs: set) -> list:
    """
    ClawHub 金融类 Skill 巡检
    策略：搜索12个金融关键词 + 浏览最新50个技能做关键词过滤
    """
    found = {}  # slug -> 最完整的信息

    # 1. 关键词搜索
    print("  搜索金融关键词...")
    for kw in FINANCE_KEYWORDS:
        results = search_clawhub(kw, limit=10)
        for item in results:
            slug = item["slug"]
            if is_finance_related(item) and not match_existing(slug, existing_slugs):
                found[slug] = item
        time.sleep(0.3)  # 避免触发限流

    # 2. 最新上架浏览+关键词过滤
    print("  浏览最新上架...")
    recent = get_recent_skills(limit=50)
    for item in recent:
        slug = item["slug"]
        if is_finance_related(item) and not match_existing(slug, existing_slugs):
            if slug not in found:
                found[slug] = item

    return list(found.values())


def scan_npm_extra(existing_slugs: set) -> list:
    """npm 扩展搜索：补充中文平台相关包"""
    keywords = [
        "coze skill finance",
        "mcp server stock china",
        "clawhub finance",
        "eastmoney mcp",
    ]

    found = []
    for kw in keywords:
        try:
            r = requests.get(
                "https://registry.npmjs.org/-/v1/search",
                params={"text": kw, "size": 5},
                timeout=15,
            )
            r.raise_for_status()
            for obj in r.json().get("objects", []):
                pkg = obj["package"]
                name = pkg["name"]
                if not match_existing(name, existing_slugs):
                    found.append({
                        "name": name,
                        "version": pkg.get("version", ""),
                        "description": (pkg.get("description", "") or "")[:200],
                        "url": pkg.get("links", {}).get("npm", ""),
                        "source": "npm",
                    })
            time.sleep(0.5)
        except Exception as e:
            print(f"  ⚠ npm 搜索 '{kw}' 失败: {e}")

    return found


def generate_report(
    clawhub_new: list,
    npm_new: list,
) -> str:
    """生成 Markdown 周报"""
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# 📡 FinAI Tools 国内平台周报 — {today}",
        "",
        f"> 自动生成 by GitHub Actions | [awesome-finai-tools-zn](https://github.com/lj22503/awesome-finai-tools-zn)",
        "",
        "---",
        "",
    ]

    has_new = bool(clawhub_new or npm_new)

    if not has_new:
        lines.extend(["## ✅ 本周无新增国内平台工具", "", "ClawHub / npm 未发现新的金融类 Skill 或包。", ""])
    else:
        if clawhub_new:
            lines.append(f"## 🆕 ClawHub 新发现 ({len(clawhub_new)} 个)")
            lines.append("")
            lines.append("| 名称 | Slug | 描述 | 下载量 |")
            lines.append("|------|------|------|--------|")
            for item in clawhub_new[:20]:
                name = item.get("displayName", "?")
                slug = item.get("slug", "")
                desc = (item.get("summary", "") or "")[:60].replace("|", "\\|")
                stats = item.get("stats") or {}
                dl = stats.get("downloads", "?")
                url = f"https://clawhub.ai/{slug}"
                lines.append(f"| {name} | `{slug}` | {desc} | {dl} |")
            lines.append("")

        if npm_new:
            lines.append(f"## 🆕 npm 新增包 ({len(npm_new)} 个)")
            lines.append("")
            for pkg in npm_new[:10]:
                lines.append(f"- **{pkg['name']}** v{pkg.get('version','?')}")
                if pkg.get("description"):
                    lines.append(f"  {pkg['description'][:100]}")
                if pkg.get("url"):
                    lines.append(f"  → {pkg['url']}")
            lines.append("")

    lines.extend([
        "---",
        f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ])

    return "\n".join(lines)


def update_tools_json(clawhub_new: list) -> int:
    """将 ClawHub 新工具追加到 tools.json（标记 pending_review）"""
    with open(TOOLS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for item in clawhub_new:
        slug = item["slug"]
        entry = {
            "id": f"clawhub-{slug}",
            "name": item.get("displayName", slug),
            "category": "pending_review",
            "type": "skill",
            "description": (item.get("summary", "") or "")[:200],
            "input": {},
            "output": {"format": "待确认"},
            "access": {
                "method": "ClawHub 一键安装",
                "auth_required": "待确认",
            },
            "installation": {
                "command": f"clawhub install {slug}"
            },
            "cost": "unknown",
            "official_url": f"https://clawhub.ai/{slug}",
            "clawhub_slug": slug,
            "stars": item.get("stats", {}).get("downloads", 0),
            "status": "pending_review",
            "found_date": datetime.now().strftime("%Y-%m-%d"),
            "tags": ["待分类"],
        }
        data["tools"].append(entry)
        count += 1

    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    data["version"] = datetime.now().strftime("%Y-%m-%d")

    with open(TOOLS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return count


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 国内平台巡检开始\n")

    existing_tools, existing_slugs = load_existing_tools()
    print(f"当前收录: {len(existing_tools)} 个工具\n")

    # 1. ClawHub 扫描
    print("1. ClawHub 金融类 Skill 巡检...")
    clawhub_new = scan_clawhub_finance(existing_slugs)
    print(f"  发现 {len(clawhub_new)} 个新 Skill\n")

    # 2. npm 扩展
    print("2. npm 扩展搜索...")
    npm_new = scan_npm_extra(existing_slugs)
    print(f"  发现 {len(npm_new)} 个新包\n")

    # 3. 生成报告
    report = generate_report(clawhub_new, npm_new)
    report_file = REPO_DIR / "data" / f"weekly-report-china-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"报告已生成: {report_file}")

    # 4. 更新 tools.json
    if clawhub_new:
        count = update_tools_json(clawhub_new)
        print(f"已将 {count} 个新 Skill 追加到 tools.json (pending_review)")

    print(f"\n{'='*50}")
    print(report)
    print(f"\n✅ 国内平台巡检完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())

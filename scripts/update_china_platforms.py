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
INSTITUTION_SKILLS_JSON = REPO_DIR / "data" / "institution-skills.json"

# 机构名中会被过滤的泛化词（不参与关键词匹配）
INSTITUTION_GENERIC_WORDS = {
    "证券", "基金", "银行", "公司", "股份", "有限", "中国", "保险",
    "金融", "科技", "资本", "集团", "国际", "投资", "资产",
}

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


# === 机构自动发现与入库 ===

def load_institution_skills() -> tuple[list, set]:
    """
    加载 institution-skills.json，返回 (机构列表, 已知机构名集合)。
    文件不存在时返回空列表和空集合，不报错。
    """
    if not INSTITUTION_SKILLS_JSON.exists():
        print("  ℹ institution-skills.json 不存在，跳过机构匹配")
        return [], set()

    try:
        with open(INSTITUTION_SKILLS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ⚠ institution-skills.json 读取失败: {e}，跳过机构匹配")
        return [], set()

    institutions = data if isinstance(data, list) else data.get("institutions", [])
    names = {inst["institution_name"] for inst in institutions if inst.get("institution_name")}
    return institutions, names


def extract_institution_keywords(institution_name: str) -> list[str]:
    """
    从机构全名中提取可用于模糊匹配的关键词。
    规则：
    - 去掉括号注释（如 "万得 (Wind)" → ["万得", "Wind"]）
    - 去掉「证券/基金/银行/公司/股份/有限」等泛化词
    - 保留剩余部分作为关键词
    - 同时保留原始全名（去泛化词后）和拆分后的各部分
    """
    import re

    # 先提取括号中的英文别名
    alias_match = re.findall(r'[\(（]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)\s*[\)）]', institution_name)
    # 去掉括号内容，保留主体
    base = re.sub(r'[\(（].*?[\)）]', '', institution_name).strip()

    keywords = []
    # 英文别名
    for a in alias_match:
        keywords.append(a.lower())

    # 对中文主体做分词（按常见分隔符 + 逐词拆分）
    # 先整体去泛化词后作为一个关键词
    clean_full = base
    for gw in INSTITUTION_GENERIC_WORDS:
        clean_full = clean_full.replace(gw, "")
    clean_full = clean_full.strip()
    if clean_full and len(clean_full) >= 2:
        keywords.append(clean_full)

    # 再提取其中 2 字及以上的子片段（排除纯泛化词）
    # 按常见切分规则拆分中文机构名
    parts = re.split(r'[·\-\s]+', base)
    for part in parts:
        part = part.strip()
        if part in INSTITUTION_GENERIC_WORDS:
            continue
        if len(part) >= 2 and part not in keywords:
            keywords.append(part)

    return keywords


def build_institution_keyword_map(institutions: list) -> dict:
    """
    构建 {关键词: 机构全名} 映射。
    多个机构共享同一个关键词时保留第一个（更具体的关键词优先）。
    """
    kw_map = {}
    for inst in institutions:
        name = inst["institution_name"]
        keywords = extract_institution_keywords(name)
        for kw in keywords:
            if kw not in kw_map:
                kw_map[kw] = name
    return kw_map


def match_institution(
    tool_name: str,
    tool_desc: str,
    kw_map: dict,
    known_institution_names: set,
) -> str | None:
    """
    检查工具名称/描述中是否包含已知机构关键词。
    返回机构全名或 None。
    匹配规则：不区分大小写，关键词作为子串出现在 name 或 desc 中即命中。
    """
    text = f"{tool_name} {tool_desc}".lower()
    for kw, inst_name in kw_map.items():
        if kw.lower() in text:
            return inst_name
    return None


def check_skill_exists(institutions: list, institution_name: str, skill_name: str) -> bool:
    """检查某个 skill 是否已存在于 institution-skills.json 中"""
    for inst in institutions:
        if inst["institution_name"] == institution_name:
            for s in inst.get("skills", []):
                if s.get("skill_name") == skill_name:
                    return True
    return False


def generate_institution_candidates(
    institution_name: str,
    tools: list,
) -> list[dict]:
    """
    为某个已知机构生成可追加的 JSON 片段（仅新增 Skill），
    供人工确认后通过 add_institution.py 入库。
    """
    candidates = []
    for tool in tools:
        candidates.append({
            "skill_name": tool.get("name", "?"),
            "description": (tool.get("description", "") or "")[:200],
            "platform": tool.get("source", "ClawHub"),
            "install_method": tool.get("installation", {}).get("command", "待确认"),
            "evaluation": "自动发现，待人工评估",
        })
    return candidates


# === ClawHub 搜索 ===

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
    institution_matches: dict = None,
    new_institution_tools: list = None,
    institution_candidates: dict = None,
) -> str:
    """
    生成 Markdown 周报。

    新增参数：
    - institution_matches: {工具标识 → 归属机构名}
    - new_institution_tools: 疑似新机构的工具列表 [{name, desc, source, inferred_org, link}, ...]
    - institution_candidates: {机构名 → [可追加的 JSON 片段]}
    """
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
            lines.append("| 名称 | Slug | 描述 | 下载量 | 归属机构 |")
            lines.append("|------|------|------|--------|----------|")
            for item in clawhub_new[:20]:
                name = item.get("displayName", "?")
                slug = item.get("slug", "")
                desc = (item.get("summary", "") or "")[:60].replace("|", "\\|")
                stats = item.get("stats") or {}
                dl = stats.get("downloads", "?")
                inst = ""
                if institution_matches:
                    inst = institution_matches.get(slug, institution_matches.get(name, ""))
                lines.append(f"| {name} | `{slug}` | {desc} | {dl} | {inst} |")
            lines.append("")

        if npm_new:
            lines.append(f"## 🆕 npm 新增包 ({len(npm_new)} 个)")
            lines.append("")
            lines.append("| 包名 | 版本 | 来源 | 归属机构 |")
            lines.append("|------|------|------|----------|")
            for pkg in npm_new[:10]:
                inst = ""
                if institution_matches:
                    inst = institution_matches.get(pkg["name"], "")
                lines.append(f"| **{pkg['name']}** | v{pkg.get('version','?')} | npm | {inst} |")
                if pkg.get("description"):
                    lines.append(f"  _{pkg['description'][:120]}_")
                if pkg.get("url"):
                    lines.append(f"  → {pkg['url']}")
            lines.append("")

    # === 已知机构 Skill 入库候选 ===
    if institution_candidates:
        lines.append("---")
        lines.append("")
        lines.append("## 📋 已知机构 Skill 入库候选")
        lines.append("")
        lines.append("以下工具已识别归属机构，对应 Skill 尚未入库。请人工确认后运行 `python scripts/add_institution.py` 追加。")
        lines.append("")
        for inst_name, candidates in institution_candidates.items():
            lines.append(f"### {inst_name}")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(candidates, ensure_ascii=False, indent=2))
            lines.append("```")
            lines.append("")
            lines.append(f"**入库命令**: `python scripts/add_institution.py --name \"{inst_name}\" --skills '[...]'`")
            lines.append("")

    # === 新机构预警 ===
    if new_institution_tools:
        lines.append("---")
        lines.append("")
        lines.append("## 🔔 新机构预警")
        lines.append("")
        lines.append(f"以下 {len(new_institution_tools)} 个工具疑似来自**未收录的新机构**，需人工确认。")
        lines.append("")
        for tool in new_institution_tools:
            lines.append(f"- **机构名（推断）**: {tool['inferred_org']}")
            lines.append(f"  - 发现来源: {tool['source']}")
            lines.append(f"  - 工具名: {tool['name']}")
            if tool.get("link"):
                lines.append(f"  - 链接: {tool['link']}")
            if tool.get("desc"):
                desc_short = tool["desc"][:120].replace("\n", " ")
                lines.append(f"  - 描述: {desc_short}")
            lines.append(f"  - **建议行动**: 人工确认后运行 `python scripts/add_institution.py --name \"{tool['inferred_org']}\" --skills '[...]'` 入库")
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

    # 0. 加载机构 Skill 数据
    print("0. 加载机构 Skill 数据...")
    institutions, known_institution_names = load_institution_skills()
    kw_map = build_institution_keyword_map(institutions)
    if kw_map:
        print(f"  已加载 {len(institutions)} 家机构，{len(kw_map)} 个关键词\n")
    else:
        print("  无机构数据，跳过机构匹配\n")

    # 1. ClawHub 扫描
    print("1. ClawHub 金融类 Skill 巡检...")
    clawhub_new = scan_clawhub_finance(existing_slugs)
    print(f"  发现 {len(clawhub_new)} 个新 Skill\n")

    # 2. npm 扩展
    print("2. npm 扩展搜索...")
    npm_new = scan_npm_extra(existing_slugs)
    print(f"  发现 {len(npm_new)} 个新包\n")

    # 3. 机构匹配与发现
    print("3. 机构匹配...")
    institution_matches = {}       # {工具标识 → 机构名}
    new_institution_tools = []     # 疑似新机构
    institution_candidates = {}    # {机构名 → [候选 Skill JSON]}

    if institutions and kw_map:
        # 3a. 匹配 ClawHub 新工具
        for item in clawhub_new:
            slug = item.get("slug", "")
            name = item.get("displayName", "")
            desc = item.get("summary", "") or ""
            matched_inst = match_institution(name, desc, kw_map, known_institution_names)

            if matched_inst:
                institution_matches[slug] = matched_inst
                # 检查是否已入库
                if not check_skill_exists(institutions, matched_inst, name):
                    if matched_inst not in institution_candidates:
                        institution_candidates[matched_inst] = []
                    institution_candidates[matched_inst].append({
                        "skill_name": name,
                        "description": desc[:200],
                        "platform": "ClawHub",
                        "install_method": f"clawhub install {slug}",
                        "evaluation": "自动发现，待人工评估",
                    })
            else:
                # 疑似新机构：尝试从工具名中提取可能的机构名
                inferred = _infer_org_name(name, desc)
                if inferred:
                    new_institution_tools.append({
                        "name": name,
                        "desc": desc,
                        "source": "ClawHub",
                        "inferred_org": inferred,
                        "link": f"https://clawhub.ai/{slug}",
                    })

        # 3b. 匹配 npm 新包
        for pkg in npm_new:
            pkg_name = pkg.get("name", "")
            pkg_desc = pkg.get("description", "")
            matched_inst = match_institution(pkg_name, pkg_desc, kw_map, known_institution_names)

            if matched_inst:
                institution_matches[pkg_name] = matched_inst
                if not check_skill_exists(institutions, matched_inst, pkg_name):
                    if matched_inst not in institution_candidates:
                        institution_candidates[matched_inst] = []
                    institution_candidates[matched_inst].append({
                        "skill_name": pkg_name,
                        "description": pkg_desc[:200],
                        "platform": "npm",
                        "install_method": f"npm install {pkg_name}",
                        "evaluation": "自动发现，待人工评估",
                    })
            else:
                inferred = _infer_org_name(pkg_name, pkg_desc)
                if inferred:
                    new_institution_tools.append({
                        "name": pkg_name,
                        "desc": pkg_desc,
                        "source": "npm",
                        "inferred_org": inferred,
                        "link": pkg.get("url", ""),
                    })

        matched_count = len(institution_matches)
        new_inst_count = len(new_institution_tools)
        candidates_count = sum(len(v) for v in institution_candidates.values())
        print(f"  已匹配 {matched_count} 个工具到已知机构")
        print(f"  发现 {new_inst_count} 个疑似新机构工具")
        print(f"  生成 {candidates_count} 条入库候选\n")
    else:
        print("  跳过机构匹配\n")

    # 4. 生成报告
    report = generate_report(
        clawhub_new,
        npm_new,
        institution_matches=institution_matches if institution_matches else None,
        new_institution_tools=new_institution_tools if new_institution_tools else None,
        institution_candidates=institution_candidates if institution_candidates else None,
    )
    report_file = REPO_DIR / "data" / f"weekly-report-china-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"报告已生成: {report_file}")

    # 5. 更新 tools.json
    if clawhub_new:
        count = update_tools_json(clawhub_new)
        print(f"已将 {count} 个新 Skill 追加到 tools.json (pending_review)")

    print(f"\n{'='*50}")
    print(report)
    print(f"\n✅ 国内平台巡检完成")
    return 0


def _infer_org_name(name: str, desc: str) -> str | None:
    """
    从工具名/描述中推断可能的机构名称。
    用于新机构预警——当工具不属于任何已知机构时，尝试提取可能的机构名。
    
    启发式规则：
    1. 工具名中的中文前缀（2-4字）可能是机构简称
    2. 描述中首次出现的「XX证券」「XX基金」「XX银行」等模式
    """
    import re

    text = f"{name} {desc}"

    # 模式1: 匹配「XX证券」「XX基金」「XX银行」「XX保险」「XX信托」
    patterns = [
        (r'([\u4e00-\u9fff]{2,6})(?:证券|基金|银行|保险|信托|期货)', r'\1\2'),
        (r'([\u4e00-\u9fff]{2,4})(?:金科|数科|财富|资管|投顾)', r'\1\2'),
    ]
    for pat, repl in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(0)

    # 模式2: 英文大写缩写（如 CITIC / HTSC / CICC）
    m = re.search(r'\b([A-Z]{2,6})\b', desc)
    if m:
        abbr = m.group(1)
        # 排除常见非机构缩写
        exclude = {'API', 'MCP', 'HTTP', 'URL', 'JSON', 'XML', 'HTML', 'CSS', 'JS', 'TS', 'AI', 'ML', 'OK', 'ID'}
        if abbr not in exclude:
            return abbr

    # 模式3: 工具名首段中文（可能是机构简称）
    m = re.match(r'^([\u4e00-\u9fff]{2,4})[\-\s·]', name)
    if m:
        return m.group(1)

    return None


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
awesome-finai-tools-zn 候选质量检测（入库前把关）

定位：
  待审池（data/pending-review.json）里的候选，在并入正式清单
  （data/tools.json / data/institution-skills.json）之前，先跑一遍本脚本做质检。
  本脚本只读、只出报告，绝不修改任何正式数据；入库动作由人工确认后另行执行。

检测维度：
  ClawHub / 平台技能候选（items）
    - 详情页链接是否可达（404 / 下架 → REJECT）
    - 是否与现有收录重复（slug / id 查重）
    - 描述完整性
  GitHub 候选
    - 仓库是否存在 / 是否已 archived
    - 是否与现有收录重复
    - 活跃度（最近推送时间）、完整性（description / license / stars）
  npm 候选
    - 包是否存在 / 是否 deprecated
    - 周下载量、活跃度（最近发布时间）、查重
  机构技能候选
    - 机构是否已有档案、skill 是否重复、描述完整性、链接可达性

产出：
  data/candidate-review-<date>.md   质检报告（PASS / WARN / REJECT 三档 + 建议入库清单）

用法：
  python scripts/review_candidates.py                  # 全量检测
  python scripts/review_candidates.py --scope items    # 只测某一类
  python scripts/review_candidates.py --json           # 额外输出机器可读 JSON
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

REPO_DIR = Path(__file__).parent.parent
DATA_DIR = REPO_DIR / "data"
TOOLS_JSON = DATA_DIR / "tools.json"
INSTITUTION_JSON = DATA_DIR / "institution-skills.json"
PENDING_JSON = DATA_DIR / "pending-review.json"

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
GH_HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "awesome-finai-tools-zn-review"}
if TOKEN:
    GH_HEADERS["Authorization"] = f"token {TOKEN}"

UA = {"User-Agent": "Mozilla/5.0 (compatible; awesome-finai-tools-zn-review/1.0)"}

# ---- 判定阈值（可调） ----------------------------------------------------
STALE_DAYS_REPO = 365        # 仓库超过这么久没推送 → WARN
STALE_DAYS_PKG = 365         # npm 包超过这么久没发版 → WARN
MIN_WEEKLY_DOWNLOADS = 10    # npm 周下载量低于此 → WARN
MIN_STARS_WARN = 10          # 星数低于此 → WARN

PASS, WARN, REJECT = "PASS", "WARN", "REJECT"
_ORDER = {PASS: 0, WARN: 1, REJECT: 2}


def worst(*levels):
    return max(levels, key=lambda x: _ORDER[x])


def _days_since(iso_ts: str) -> int:
    if not iso_ts:
        return 9999
    try:
        dt = datetime.strptime(str(iso_ts)[:10], "%Y-%m-%d")
    except Exception:
        return 9999
    return (datetime.now() - dt).days


def _session() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=2, backoff_factor=0.5,
                  status_forcelist=[429, 500, 502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update(UA)
    return s


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def check_link(sess: requests.Session, url: str, timeout: int = 15):
    """返回 (ok, detail)。GET 流式取首字节，兼容 403 反爬（标记为可达但存疑）。"""
    if not url:
        return False, "无链接"
    try:
        r = sess.get(url, timeout=timeout, stream=True, allow_redirects=True)
        code = r.status_code
        r.close()
        if code == 200:
            return True, "200"
        if code in (403, 401):
            return True, f"{code}(反爬，需人工确认)"
        if code == 404:
            return False, "404 页面不存在"
        if code >= 400:
            return False, f"{code}"
        return True, str(code)
    except Exception as exc:
        return False, f"不可达({type(exc).__name__})"


# ---- 现有收录索引 --------------------------------------------------------
def build_index():
    """现有正式收录的标识集合（用于查重）"""
    tools = load_json(TOOLS_JSON, {}).get("tools", [])
    ids, slugs = set(), set()
    for t in tools:
        for key in ("id", "slug", "name"):
            v = str(t.get(key) or "").strip().lower()
            if not v:
                continue
            ids.add(v)
            slugs.add(v.replace("_", "-"))
            slugs.add(v.split("/")[-1])

    inst_raw = load_json(INSTITUTION_JSON, [])
    if isinstance(inst_raw, dict):
        inst_raw = inst_raw.get("institutions", [])
    insts, inst_skills = set(), set()
    for item in inst_raw:
        if not isinstance(item, dict):
            continue
        nm = str(item.get("institution_name") or item.get("name") or item.get("id") or "").strip()
        if nm:
            insts.add(nm)
        for s in item.get("skills", []) or []:
            sn = str(s.get("skill_name") or s.get("name") or "").strip()
            if sn:
                inst_skills.add(sn)
    return {"ids": ids, "slugs": slugs, "insts": insts, "inst_skills": inst_skills}


# ---- 1. ClawHub / 平台技能候选（items） ---------------------------------
def review_items(items: list, idx: dict, sess: requests.Session) -> list:
    def one(c):
        name = c.get("name") or c.get("slug") or ""
        slug = str(c.get("slug") or c.get("id") or "").strip().lower()
        rec = {"kind": "item", "name": name, "link": c.get("link", ""),
               "source": c.get("source", ""), "notes": [], "level": PASS}

        if slug and (slug in idx["slugs"] or slug in idx["ids"]):
            rec["level"] = REJECT
            rec["notes"].append("已收录（与正式清单重复）")
            return rec

        ok, detail = check_link(sess, rec["link"])
        rec["link_status"] = detail
        if not ok:
            rec["level"] = REJECT
            rec["notes"].append(f"链接不可达：{detail}")
        elif "反爬" in detail:
            rec["level"] = worst(rec["level"], WARN)

        desc = (c.get("description") or "").strip()
        rec["desc"] = desc[:80]
        if len(desc) < 10:
            rec["level"] = worst(rec["level"], WARN)
            rec["notes"].append("描述过短，无法判断能力边界")
        return rec

    results = [None] * len(items)
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(one, c): i for i, c in enumerate(items)}
        for f in as_completed(futs):
            results[futs[f]] = f.result()
    return results


# ---- 2. GitHub -----------------------------------------------------------
def review_github(cands: list, idx: dict, sess: requests.Session) -> list:
    results = []
    for c in cands:
        full_name = c.get("full_name", "")
        rec = {"kind": "github", "name": full_name or c.get("name", ""),
               "link": c.get("link", ""), "notes": [], "level": PASS}

        if not full_name:
            rec["level"] = REJECT
            rec["notes"].append("缺少 full_name，无法核验")
            results.append(rec)
            continue
        short = full_name.split("/")[-1].lower()
        if full_name.lower() in idx["ids"] or short in idx["ids"] or short in idx["slugs"]:
            rec["level"] = REJECT
            rec["notes"].append("已收录（与正式清单重复）")
            results.append(rec)
            continue

        try:
            r = sess.get(f"https://api.github.com/repos/{full_name}",
                         headers=GH_HEADERS, timeout=30)
            if r.status_code == 404:
                rec["level"] = REJECT
                rec["notes"].append("仓库不存在或已删除")
                results.append(rec)
                continue
            if r.status_code != 200:
                rec["level"] = WARN
                rec["notes"].append(f"GitHub API 异常（{r.status_code}），未能核验")
                results.append(rec)
                continue

            repo = r.json()
            if repo.get("archived"):
                rec["level"] = REJECT
                rec["notes"].append("仓库已归档（archived）")
            if repo.get("disabled"):
                rec["level"] = REJECT
                rec["notes"].append("仓库已被禁用")

            stars = repo.get("stargazers_count", 0)
            rec["stars"] = stars
            rec["desc"] = (repo.get("description") or "")[:80]
            if stars < MIN_STARS_WARN:
                rec["level"] = worst(rec["level"], WARN)
                rec["notes"].append(f"星数偏低（{stars}）")
            if not (repo.get("description") or "").strip():
                rec["level"] = worst(rec["level"], WARN)
                rec["notes"].append("无仓库描述")
            if not repo.get("license"):
                rec["level"] = worst(rec["level"], WARN)
                rec["notes"].append("无 license")

            days = _days_since(repo.get("pushed_at", ""))
            rec["last_push_days"] = days
            if days > STALE_DAYS_REPO:
                rec["level"] = worst(rec["level"], WARN)
                rec["notes"].append(f"最近推送距今 {days} 天，活跃度存疑")
        except Exception as exc:
            rec["level"] = WARN
            rec["notes"].append(f"核验异常：{type(exc).__name__}")

        results.append(rec)
        time.sleep(0.3)
    return results


# ---- 3. npm --------------------------------------------------------------
def review_npm(cands: list, idx: dict, sess: requests.Session) -> list:
    def one(c):
        name = c.get("name", "")
        rec = {"kind": "npm", "name": name, "link": c.get("link", ""),
               "notes": [], "level": PASS}
        if not name:
            rec["level"] = REJECT
            rec["notes"].append("缺少包名")
            return rec
        if name.lower() in idx["slugs"] or name.lower() in idx["ids"]:
            rec["level"] = REJECT
            rec["notes"].append("已收录（与正式清单重复）")
            return rec
        try:
            r = sess.get(f"https://registry.npmjs.org/{name}", timeout=30)
            if r.status_code == 404:
                rec["level"] = REJECT
                rec["notes"].append("包不存在或已下架")
                return rec
            if r.status_code != 200:
                rec["level"] = WARN
                rec["notes"].append(f"Registry 异常（{r.status_code}）")
                return rec

            meta = r.json()
            if meta.get("deprecated"):
                rec["level"] = REJECT
                rec["notes"].append("包已标记 deprecated")
            latest = (meta.get("dist-tags") or {}).get("latest", "")
            rec["version"] = latest
            rec["desc"] = (meta.get("description") or "")[:80]

            days = _days_since((meta.get("time") or {}).get("modified", ""))
            rec["last_publish_days"] = days
            if days > STALE_DAYS_PKG:
                rec["level"] = worst(rec["level"], WARN)
                rec["notes"].append(f"最近发布距今 {days} 天，可能已停更")

            try:
                d = sess.get(f"https://api.npmjs.org/downloads/point/last-week/{name}", timeout=20)
                if d.status_code == 200:
                    dl = d.json().get("downloads", 0)
                    rec["weekly_downloads"] = dl
                    if dl < MIN_WEEKLY_DOWNLOADS:
                        rec["level"] = worst(rec["level"], WARN)
                        rec["notes"].append(f"周下载量极低（{dl}）")
            except Exception:
                pass
        except Exception as exc:
            rec["level"] = WARN
            rec["notes"].append(f"核验异常：{type(exc).__name__}")
        return rec

    results = [None] * len(cands)
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(one, c): i for i, c in enumerate(cands)}
        for f in as_completed(futs):
            results[futs[f]] = f.result()
    return results


# ---- 4. 机构技能 ---------------------------------------------------------
def review_institutions(cands: dict, idx: dict, sess: requests.Session) -> list:
    results = []
    for org, skills in (cands or {}).items():
        for s in skills or []:
            skill_name = str(s.get("skill_name") or s.get("name") or "").strip()
            rec = {"kind": "institution", "name": f"{org} / {skill_name}",
                   "link": s.get("url") or s.get("link") or "", "notes": [], "level": PASS}

            if skill_name and skill_name in idx["inst_skills"]:
                rec["level"] = REJECT
                rec["notes"].append("该 skill 已收录")
            if org in idx["insts"]:
                rec["notes"].append("机构已有档案（需确认是否新增能力）")
            else:
                rec["level"] = worst(rec["level"], WARN)
                rec["notes"].append("机构尚未建档，需先补齐机构信息")

            if not str(s.get("description") or "").strip():
                rec["level"] = worst(rec["level"], WARN)
                rec["notes"].append("缺少能力描述")
            if rec["link"]:
                ok, detail = check_link(sess, rec["link"])
                rec["link_status"] = detail
                if not ok:
                    rec["level"] = worst(rec["level"], WARN)
                    rec["notes"].append(f"链接存疑：{detail}")
            results.append(rec)
    return results


# ---- 报告 ---------------------------------------------------------------
def render_md(groups: dict, meta: dict) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    all_items = [x for g in groups.values() for x in g]
    n = {lv: sum(1 for x in all_items if x["level"] == lv) for lv in (PASS, WARN, REJECT)}

    lines = [
        f"# 🔎 候选质量检测报告 — {today}",
        "",
        "> 仅检测，不改动任何正式数据。结论供人工决定是否并入主站。",
        "",
        "## 总览",
        "",
        f"- 检测候选：**{len(all_items)}** 条"
        f"（平台技能 {len(groups.get('items', []))} / GitHub {len(groups.get('github', []))}"
        f" / npm {len(groups.get('npm', []))} / 机构技能 {len(groups.get('institution', []))}）",
        f"- ✅ PASS 建议收录：**{n[PASS]}** 条",
        f"- ⚠️ WARN 需人工判断：**{n[WARN]}** 条",
        f"- ❌ REJECT 不建议收录：**{n[REJECT]}** 条",
        f"- 待审池版本：{meta.get('version', '—')}",
        "",
    ]

    if n[PASS]:
        lines += ["### 建议收录清单（PASS）", ""]
        for x in all_items:
            if x["level"] == PASS:
                lines.append(f"- {_tag(x)} **{x['name']}**")
        lines.append("")

    lines += ["---", ""]

    def section(title, level):
        subset = [x for x in all_items if x["level"] == level]
        if not subset:
            return
        lines.append(f"## {title}（{len(subset)} 条）")
        lines.append("")
        for x in subset:
            lines.append(f"- {_tag(x)} **{x['name']}**")
            if x.get("desc"):
                lines.append(f"  {x['desc']}")
            bits = []
            if x.get("stars") is not None:
                bits.append(f"{x['stars']} ⭐")
            if x.get("weekly_downloads") is not None:
                bits.append(f"周下载 {x['weekly_downloads']}")
            if x.get("last_push_days") is not None:
                bits.append(f"最近推送 {x['last_push_days']} 天前")
            if x.get("last_publish_days") is not None:
                bits.append(f"最近发布 {x['last_publish_days']} 天前")
            if x.get("version"):
                bits.append(f"v{x['version']}")
            if bits:
                lines.append(f"  {' · '.join(bits)}")
            if x["notes"]:
                lines.append(f"  判定依据：{'；'.join(x['notes'])}")
            lines.append("")
        lines.append("")

    section("✅ PASS — 建议收录", PASS)
    section("⚠️ WARN — 需人工判断", WARN)
    section("❌ REJECT — 不建议收录", REJECT)

    lines += [
        "---",
        "",
        "## 入库流程",
        "",
        "1. 本报告筛出 PASS 条目（WARN 需逐条判断）",
        "2. 人工确认后，将条目写入 `data/tools.json` / `data/institution-skills.json` 并归入正式分类",
        "3. 跑 `python scripts/generate_readme.py` 重新生成 README / llms.txt",
        "",
        f"*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ]
    return "\n".join(lines)


def _tag(x):
    src = {"github": "GitHub", "npm": "npm", "item": x.get("source", "平台"),
           "institution": "机构"}.get(x["kind"], x["kind"])
    return f"[{src}]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["items", "github", "npm", "institution", "all"], default="all")
    ap.add_argument("--json", action="store_true", help="额外输出机器可读 JSON")
    args = ap.parse_args()

    pending = load_json(PENDING_JSON, {})
    if not pending:
        print(f"未找到待审池：{PENDING_JSON}")
        return 1

    idx = build_index()
    sess = _session()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 候选质量检测开始")
    print(f"  待审池版本：{pending.get('version', '—')}")
    print(f"  现有收录：{len(load_json(TOOLS_JSON, {}).get('tools', []))} 个工具 / {len(idx['insts'])} 家机构")

    groups = {"items": [], "github": [], "npm": [], "institution": []}
    if args.scope in ("items", "all"):
        print("\n1. 检测平台技能候选（含链接可达性）...")
        groups["items"] = review_items(pending.get("items", []), idx, sess)
        print(f"   完成 {len(groups['items'])} 条")
    if args.scope in ("github", "all"):
        print("\n2. 检测 GitHub 候选...")
        groups["github"] = review_github(pending.get("github_candidates", []), idx, sess)
        print(f"   完成 {len(groups['github'])} 条")
    if args.scope in ("npm", "all"):
        print("\n3. 检测 npm 候选...")
        groups["npm"] = review_npm(pending.get("npm_candidates", []), idx, sess)
        print(f"   完成 {len(groups['npm'])} 条")
    if args.scope in ("institution", "all"):
        print("\n4. 检测机构技能候选...")
        groups["institution"] = review_institutions(pending.get("institution_candidates", {}), idx, sess)
        print(f"   完成 {len(groups['institution'])} 条")

    md = render_md(groups, pending)
    today = datetime.now().strftime("%Y-%m-%d")
    out = DATA_DIR / f"candidate-review-{today}.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"\n报告已保存：{out}")

    if args.json:
        jout = DATA_DIR / f"candidate-review-{today}.json"
        with open(jout, "w", encoding="utf-8") as f:
            json.dump({"date": today, "version": pending.get("version"), "groups": groups},
                      f, ensure_ascii=False, indent=2)
        print(f"JSON 已保存：{jout}")

    all_items = [x for g in groups.values() for x in g]
    stat = {lv: sum(1 for x in all_items if x["level"] == lv) for lv in (PASS, WARN, REJECT)}
    print(f"\nPASS {stat[PASS]} / WARN {stat[WARN]} / REJECT {stat[REJECT]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

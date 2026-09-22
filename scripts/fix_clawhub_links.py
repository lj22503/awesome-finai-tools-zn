#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存量修复 ClawHub 候选链接。

背景：早期 update_china_platforms.py 用 https://clawhub.ai/{slug} 拼详情页链接，
真实格式为 https://clawhub.ai/{ownerHandle}/skills/{slug}，导致 pending-review.json
中 106 条 ClawHub 候选链接全部 404，质检环节被整体 REJECT。

本脚本通过 ClawHub search 接口按 slug 反查 canonicalUrl / ownerHandle，
就地重写 data/pending-review.json 中 source=clawhub 的 link，并顺带回填 downloads。

用法：
    python scripts/fix_clawhub_links.py            # 预览（不写盘）
    python scripts/fix_clawhub_links.py --apply    # 实际写盘
"""

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
PENDING_REVIEW_JSON = REPO_ROOT / "data" / "pending-review.json"
SEARCH_API = "https://clawhub.ai/api/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; awesome-finai-tools-zn/1.0)",
    "Accept": "application/json",
}


def build_link(canonical: str, owner: str, slug: str) -> str:
    if canonical:
        return canonical if canonical.startswith("http") else f"https://clawhub.ai{canonical}"
    if owner and slug:
        return f"https://clawhub.ai/{owner}/skills/{slug}"
    return ""


def lookup_slug(slug: str) -> dict:
    """按 slug 反查 ClawHub，返回 {link, downloads} 或空 dict"""
    try:
        r = requests.get(
            SEARCH_API,
            params={"q": slug, "limit": 10},
            headers=HEADERS,
            timeout=20,
        )
        r.raise_for_status()
        results = r.json().get("results", [])
    except Exception as exc:  # noqa: BLE001
        print(f"    ! 查询失败 {slug}: {exc}")
        return {}

    for it in results:
        if it.get("slug") != slug:
            continue
        owner = it.get("ownerHandle") or (it.get("native") or {}).get("ownerHandle") or ""
        link = build_link(it.get("canonicalUrl") or "", owner, slug)
        return {
            "link": link,
            "downloads": it.get("downloads") or (it.get("stats") or {}).get("downloads", 0),
        }
    return {}


def extract_slug(node: dict) -> str:
    """取 slug；旧条目无 slug 字段时，从死链 https://clawhub.ai/{slug} 中反解"""
    slug = node.get("slug")
    if slug:
        return slug
    link = node.get("link", "") or ""
    prefix = "https://clawhub.ai/"
    if link.startswith(prefix):
        tail = link[len(prefix):].strip("/")
        if tail and "/" not in tail:
            return tail
    return ""


def fix_items(nodes: list, apply: bool, label: str) -> tuple:
    """就地修复一组候选节点（slug 或死链二选一）"""
    targets = [(n, extract_slug(n)) for n in nodes]
    targets = [(n, s) for n, s in targets if s]

    def probe(pair):
        node, slug = pair
        if "/skills/" in (node.get("link") or ""):
            return node, slug, None  # 已是新格式
        return node, slug, lookup_slug(slug)

    fixed, unresolved = 0, []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for node, slug, info in pool.map(probe, targets):
            old_link = node.get("link", "")
            if info is None:
                continue
            if not info.get("link"):
                unresolved.append(slug)
                print(f"    ! 未解析: {slug}")
                continue
            if info["link"] != old_link:
                fixed += 1
                print(f"    {slug}\n      旧: {old_link}\n      新: {info['link']}")
            if apply:
                node["slug"] = slug
                node["link"] = info["link"]
                if info.get("downloads"):
                    node["downloads"] = info["downloads"]
                node["link_fixed"] = "2026-09-22"
    print(f"  [{label}] 待修 {len(targets)} 条 → 成功 {fixed} 条，失败 {len(unresolved)} 条")
    if unresolved:
        print(f"  [{label}] 未解析 slug: {unresolved}")
    return fixed, unresolved


def main() -> int:
    apply = "--apply" in sys.argv

    if not PENDING_REVIEW_JSON.exists():
        print(f"找不到 {PENDING_REVIEW_JSON}")
        return 1

    data = json.loads(PENDING_REVIEW_JSON.read_text(encoding="utf-8"))
    items = [x for x in data.get("items", []) if x.get("source") == "clawhub"]
    suspected = [
        x for x in data.get("suspected_new_institutions", [])
        if str(x.get("source", "")).lower() == "clawhub"
    ]

    print(f"ClawHub 候选: items={len(items)}, suspected={len(suspected)}")
    print(f"模式: {'写盘' if apply else '预览'}\n")

    print("1. 修复 items:")
    fix_items(items, apply, "items")

    print("\n2. 修复 suspected_new_institutions:")
    fix_items(suspected, apply, "suspected")

    if apply:
        PENDING_REVIEW_JSON.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\n已写入 {PENDING_REVIEW_JSON}")
    else:
        print("\n预览结束，未写盘。加 --apply 执行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

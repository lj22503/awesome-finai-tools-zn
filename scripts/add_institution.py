#!/usr/bin/env python3
"""
awesome-finai-tools-zn 机构入库辅助脚本
=========================================

功能：接收机构名和 Skill JSON，追加到 data/institution-skills.json。

用法示例：

  # 1. 为新机构批量添加入库（JSON 直接写在命令行）
  python scripts/add_institution.py \
    --name "某某证券" \
    --category "券商" \
    --skills '[{"skill_name":"智能选股","description":"自然语言选股","platform":"ClawHub","install_method":"clawhub install xxx","evaluation":"自动发现，待人工评估"}]'

  # 2. 从文件读取 Skill JSON
  python scripts/add_institution.py \
    --name "某某证券" \
    --category "券商" \
    --skills-file ./temp/new_skills.json

  # 3. 为已有机构追加 Skill（机构名已存在时追加，不重复添加同名 Skill）
  python scripts/add_institution.py \
    --name "广发证券" \
    --skills '[{"skill_name":"新Skill","description":"...","platform":"ClawHub","install_method":"...","evaluation":"自动发现"}]'

  # 4. 只创建新机构不添加 Skill（后续手动编辑 JSON）
  python scripts/add_institution.py \
    --name "某某证券" \
    --category "券商" \
    --init-only
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


REPO_DIR = Path(__file__).parent.parent
INSTITUTION_SKILLS_JSON = REPO_DIR / "data" / "institution-skills.json"


def load_or_create() -> list:
    """加载 institution-skills.json，不存在则返回空列表"""
    if INSTITUTION_SKILLS_JSON.exists():
        with open(INSTITUTION_SKILLS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return data.get("institutions", [])
    return []


def save(data: list):
    """保存到 institution-skills.json"""
    INSTITUTION_SKILLS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(INSTITUTION_SKILLS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_institution(data: list, name: str) -> int:
    """查找机构索引，未找到返回 -1"""
    for i, inst in enumerate(data):
        if inst.get("institution_name") == name:
            return i
    return -1


def add_institution(
    name: str,
    category: str,
    skills: list[dict],
    init_only: bool = False,
) -> dict:
    """
    将机构/技能追加入库。

    返回操作摘要：{action, name, skills_added, skills_skipped}
    """
    data = load_or_create()
    idx = find_institution(data, name)
    today = date.today().strftime("%Y-%m-%d")

    if idx >= 0:
        # 已有机构 → 追加 Skill
        existing_skills = {s["skill_name"] for s in data[idx].get("skills", [])}
        added = 0
        skipped = 0
        for skill in skills:
            sname = skill.get("skill_name", "")
            if sname and sname not in existing_skills:
                data[idx].setdefault("skills", []).append(skill)
                existing_skills.add(sname)
                added += 1
            else:
                skipped += 1
        data[idx]["last_updated"] = today
        action = "append"
    else:
        # 新机构
        entry = {
            "institution_name": name,
            "category": category,
            "skills": [] if init_only else skills,
            "data_source": "自动发现入库",
            "last_updated": today,
        }
        data.append(entry)
        action = "create"
        added = 0 if init_only else len(skills)
        skipped = 0

    save(data)
    return {
        "action": action,
        "name": name,
        "skills_added": added,
        "skills_skipped": skipped,
    }


def main():
    parser = argparse.ArgumentParser(
        description="机构 Skill 入库工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/add_institution.py --name "某某证券" --category "券商" --skills-file ./new_skills.json
  python scripts/add_institution.py --name "广发证券" --skills '[{"skill_name":"xxx","description":"...","platform":"ClawHub","install_method":"...","evaluation":"..."}]'
  python scripts/add_institution.py --name "某某证券" --category "券商" --init-only
        """,
    )
    parser.add_argument("--name", required=True, help="机构全名（如 '广发证券'）")
    parser.add_argument("--category", default="其他", help="机构分类：券商/数据商/基金/银行保险/其他")
    parser.add_argument("--skills", default="[]", help="Skill JSON 数组字符串")
    parser.add_argument("--skills-file", help="从文件读取 Skill JSON 数组")
    parser.add_argument("--init-only", action="store_true", help="仅创建机构条目，不添加 Skill")

    args = parser.parse_args()

    # 解析 skills
    skills = []
    if not args.init_only:
        if args.skills_file:
            with open(args.skills_file, "r", encoding="utf-8") as f:
                skills = json.load(f)
        else:
            try:
                skills = json.loads(args.skills)
            except json.JSONDecodeError as e:
                print(f"❌ Skills JSON 解析失败: {e}", file=sys.stderr)
                print(f"   请确保使用合法的 JSON 数组，如 '[{{\"skill_name\":\"...\"}}]'",
                      file=sys.stderr)
                sys.exit(1)

    if not isinstance(skills, list):
        print("❌ --skills 参数必须是一个 JSON 数组", file=sys.stderr)
        sys.exit(1)

    result = add_institution(args.name, args.category, skills, args.init_only)

    if result["action"] == "create":
        if args.init_only:
            print(f"✅ 已创建机构条目: {result['name']}（{args.category}），未添加 Skill")
        else:
            print(f"✅ 已创建新机构并入库: {result['name']}（{args.category}）")
            print(f"   新增 {result['skills_added']} 个 Skill")
    else:
        print(f"✅ 已追加到已有机构: {result['name']}")
        print(f"   新增 {result['skills_added']} 个 Skill，跳过 {result['skills_skipped']} 个重复")

    print(f"   数据文件: {INSTITUTION_SKILLS_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

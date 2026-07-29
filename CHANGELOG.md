# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.0] - 2026-07-15

### Added

- 周更 China platforms scanner（commit `f9401d7`）：自动巡检 ClawHub + 中国本土 AI 平台新增工具
- GitHub Actions workflow：每周自动执行 `scripts/update_china_platforms.py`

### Changed

- 仓库清理（commit `8603af5`）：untrack `output/` + 非核心 data 文件，更新 `.gitignore`

### Fixed

- README 搜索关键词密度（commit `c586bbd`）
- README SEO keywords section + badge URL（commit `c667f40`）

---

## [0.1.0] - 2026-06-25

### Added

- 初始版本收录 39 个金融 AI 工具
- 覆盖 5 大分类：market_data / sentiment / analysis / trading / research
- `data/tools.json` 结构化数据（机器可读）
- `SKILL.md` agent 技能定义
- GitHub Actions 每周巡检脚本
- `AGENTS.md` / `CONTRIBUTING.md` / `LICENSE`

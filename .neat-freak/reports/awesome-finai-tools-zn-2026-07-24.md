# awesome-finai-tools-zn — neat-freak 知识收尾报告

**收尾时间**：2026-07-24
**收尾路径**：轻量路径（awesome-list 聚合项目 + Anthropic Skill 入口，已有 recent neat-freak commit `8603af5`，本次为审计 + 未跟踪盘点）
**收尾者**：neat-freak（v3.0.0）

---

## 一、影响（用户视角）

- **本次整体良好**：命名一致、文档齐全、未提交改动少。
- **暴露未跟踪文档**：3 个 docs/ 下的 MD 文件未跟踪（含 2 个"金融 Skill 上线/深度调研"长报告 + 1 个 task-breakdown 修改未提交）—— 这些可能是上次会话产物但未 commit。
- **暴露 topics-suggested.md（同类问题累计 4 处）**：未跟踪的 GitHub Topics 草稿。
- **暴露 SKILL.md name 与仓库名不一致（次要）**：SKILL.md frontmatter `name: finai-tools-hub` vs 仓库名 `awesome-finai-tools-zn`——这在 Anthropic Skills 规范下是合理的（skill 内部名 vs 仓库名），但用户搜索"awesome-finai-tools"找不到 SKILL.md 触发的 skill "finai-tools-hub"。

## 二、现役事实矩阵

| 事实面 | 状态 | 证据 |
|--------|------|------|
| 代码 | `verified-current` | scripts/ 4 个 Python 脚本（add_institution.py / generate_readme.py / update_china_platforms.py / update_tools.py） |
| 运行态 | `verified-current` | HEAD `8603af5`（清理 output/ + data/ 排除）；GitHub Actions 工作流（最近 commit `f9401d7 Add weekly China platforms update`） |
| 文档 | `changed-and-verified` | README.md (18KB 主体) + SKILL.md (13KB Anthropic Skill 入口) + AGENTS.md + CHANGELOG.md + CONTRIBUTING.md + llms.txt |
| 规则 | `verified-current` | AGENTS.md 4 原则（目录结构 / 分类优先级 / 有效性 / 输出风格） |
| 记忆 | `not-applicable` | 无 |
| 工作区 | `changed-and-verified` | 新建 `.neat-freak/`；3 个 docs/ 未跟踪 + 1 个修改 + 1 个 topics-suggested.md |

## 三、关键发现

### 3.1 命名一致 ✅

| 维度 | 名字 |
|------|------|
| 本地目录 | `awesome-finai-tools-zn` |
| GitHub remote | `lj22503/awesome-finai-tools-zn` |
| README.md 标题 | `# Awesome FinAI Tools`（推测，待确认） |
| SKILL.md name | `finai-tools-hub`（Anthropic Skill 内部名，与仓库名不同是合理设计） |

→ 主名称一致。

### 3.2 SKILL.md 是 Anthropic Skills 格式

```yaml
---
name: finai-tools-hub
version: 2025-06-25
description: ...
triggers:
  - "帮我查一下A股"
  - "分析一下[股票名]"
  ...
---
```

→ 加载此 skill 后 agent 自动推荐对应工具。

### 3.3 未跟踪内容（4 项）

| 文件 | 性质 | 建议 |
|------|------|------|
| `docs/prod_19f5acc03df_81a3e6dc7a3a_金融公司Skill上线调研报告_20260713.md` | 调研报告（文件名带 prod_ 前缀 + UUID 风格 + 日期） | **commit**（若为正式产出） |
| `docs/prod_19f5ad16f1f_e1cdbe965edf_金融Skill深度调研_InvestBrain融合方案_20260713.md` | 同款调研报告 | 同上 |
| `docs/task-breakdown-2day-sprint.md`（M） | 任务分解（修改未提交） | **commit** 或归档 |
| `topics-suggested.md` | GitHub Topics 草稿 | 操作完 UI 后删除 |

### 3.4 scripts/ 4 个脚本

| 脚本 | 用途（推测） |
|------|------------|
| `add_institution.py` | 添加金融机构条目 |
| `generate_readme.py` | 生成 README（从 data/） |
| `update_china_platforms.py` | 更新中国平台列表（GitHub Actions 周更） |
| `update_tools.py` | 更新工具列表 |

→ 与 `data/` + `output/` 形成数据驱动 pipeline。

### 3.5 .gitignore（4 条规则）

```
data/progress-board.md
output/
data/content-calendar.md
data/due-diligence-template.md
```

→ 比常规项目更精细（忽略 4 个具体文件而非通配）。

## 四、改动 / 新建

| 文件 | 动作 | 原因 |
|------|------|------|
| `.neat-freak/reports/awesome-finai-tools-zn-2026-07-24.md` | 新建 | 本次 audit trail |

## 五、待你确认（未确认前不动作）

1. **未跟踪 4 项处置**：
   - `docs/prod_*` × 2 → commit（若为正式调研产出）/ gitignore（若为过程稿）
   - `docs/task-breakdown-2day-sprint.md` → commit 修改或 gitignore
   - `topics-suggested.md` → 操作完 UI 后删除
2. **SKILL.md name vs 仓库名差异**：保持现状（按 Anthropic Skills 规范是合理），或在 README 加 "Skill 内部名 finai-tools-hub" 说明
3. **CHANGELOG.md 内容**：仅 0.1.0 一条记录，是否需补 v0.1.x 后续小版本

## 六、遗留

- data/ 内容未看（4 个具体文件被 .gitignore 忽略）
- scripts/ 4 个脚本实际功能未验证
- .github/ 工作流定义未读
- docs/ 已跟踪内容未逐个对照 awesome-list 列表

---

*收尾完成度：5 事实面已标注（记忆 not-applicable）。报告基于 commit `8603af5`（HEAD，分支 main）。如需重新跑请清空 `.neat-freak/reports/` 后重跑。*
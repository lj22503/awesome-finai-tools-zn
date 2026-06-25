# Contributing to Awesome FinAI Tools

感谢您对中国金融 AI 工具生态的兴趣！

## 🎯 我们收录什么

- **Market Data**：行情数据、实时报价、历史K线、资金流向
- **Sentiment**：舆情分析、社区讨论、新闻资讯
- **Analysis**：因子计算、量化分析、投研框架
- **Trading**：策略回测、模拟交易、实盘接口
- **Research**：研报解读、宏观数据、基金分析

## 📋 收录标准

1. **可运行**：工具能实际执行，不是空壳项目
2. **有接入说明**：清楚的使用方法
3. **非独占**：不依赖特定券商开户（通用工具优先）
4. **非黑盒**：有公开文档或开源代码

## 📁 目录结构

```
awesome-finai-tools/
├── skills/
│   ├── market_data/      # 行情数据类工具（每个工具一个子目录）
│   ├── sentiment/        # 舆情类工具
│   ├── analysis/         # 分析类工具
│   ├── trading/          # 交易类工具
│   └── research/         # 投研类工具
├── data/
│   └── tools.json        # 统一结构化数据（机器可读）
├── scripts/
│   └── update_tools.py   # 每周巡检脚本
├── docs/                 # 使用文档
└── .github/
    └── workflows/        # CI/CD
```

## 📝 添加新工具流程

### 1. 数据文件更新

在 `data/tools.json` 中添加条目，字段包括：

```json
{
  "id": "unique-id",
  "name": "工具名称",
  "category": "market_data | sentiment | analysis | trading | research",
  "type": "cli | mcp | skill | framework | api | python_lib",
  "description": "一句话描述",
  "input": { "intent": "解决什么问题" },
  "output": { "format": "输出格式", "覆盖": ["覆盖范围"] },
  "access": {
    "method": "接入方式",
    "auth_required": true | false,
    "api_key_required": true | false
  },
  "installation": { "command": "安装命令", "url": "地址" },
  "cost": "free | free_limited | contact_sales | institutional | unknown",
  "official_url": "官方地址",
  "maintainer": "维护方",
  "tags": ["标签1", "标签2"]
}
```

### 2. Skill 目录（可选）

如工具有独立的 skill 实现，在 `skills/<category>/` 下创建子目录：

```
skills/market_data/opencli-eastmoney/
├── SKILL.md      # skill定义（必须）
├── README.md     # 用户文档
└── references/   # 参考资料
```

### 3. SKILL.md 模板

```markdown
---
name: tool-id
version: YYYY-MM-DD
description: 一句话描述工具能力
triggers:
  - "用户可能说的话1"
  - "用户可能说的话2"
---

# 工具名称

## 能力描述

## 输入 / 输出

- **输入**：
- **输出**：

## 安装

\`\`\`bash
安装命令
\`\`\`

## 使用示例

\`\`\`bash
使用命令
\`\`\`

## 注意事项
```

## ✅ 提交检查清单

- [ ] `data/tools.json` 已更新
- [ ] `tools.json` 格式正确（JSON 有效）
- [ ] 工具信息准确（地址/费用/接入方式）
- [ ] 无敏感信息（API key/密码/真实账户）
- [ ] 新工具已测试（如适用）
- [ ] README.md 表格已同步更新

## 🚫 不收录

- ❌ 需要券商开户才能获取数据（非通用）
- ❌ 付费墙后无法试用
- ❌ 长期无维护的废弃项目
- ❌ 真实账户/密码/密钥

## 🔄 更新频率

- 每周一 GitHub Actions 自动巡检
- 手动提交随时欢迎
- 失效工具定期清理

## 📧 问题与讨论

Open issue 或 discussion 均可。

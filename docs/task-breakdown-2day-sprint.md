---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 1c835e55ba3b06878e6538b2edadf703_04f1aa277f6711f1a322525400e6dd8f
    ReservedCode1: S1e703chnDTqu51P54wmP8nbPCpRxdazjGkEMDitIeBUdJAdefwgyM9ateTWFCfGHXn/nzN1vW5pNbqtHRVFyO6aRo/k4AW1rKyb4rf+GPWXcfkGKLcEx+z6PHYv6Bl/S5LO2FGadoTOMmAJzy8gqz4mFROglU05pKOS1Kb/7FDkAg1UcoERS5bxdHI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 1c835e55ba3b06878e6538b2edadf703_04f1aa277f6711f1a322525400e6dd8f
    ReservedCode2: S1e703chnDTqu51P54wmP8nbPCpRxdazjGkEMDitIeBUdJAdefwgyM9ateTWFCfGHXn/nzN1vW5pNbqtHRVFyO6aRo/k4AW1rKyb4rf+GPWXcfkGKLcEx+z6PHYv6Bl/S5LO2FGadoTOMmAJzy8gqz4mFROglU05pKOS1Kb/7FDkAg1UcoERS5bxdHI=
---

# awesome-finai-tools-zn "一鱼多吃" 任务拆解清单

> 制定日期：2026-07-14 | 执行周期：2天 | 版本 v1.0

---

## 一、背景

### 1.1 资产现状

`awesome-finai-tools-zn` 已收录 30+ 中国金融 AI 工具，覆盖 CLI / MCP / Skill / Python库 / 量化框架五大类型。通过前期深度调研，已掌握 **17 家金融机构** 的详细 Skill 布局数据（券商8家 + 数据商3家 + 基金公司3家 + 其他3家）。

### 1.2 核心洞察

同一份结构化数据（tools.json + 机构 Skill 调研），可以同时喂养：
- **FinancePro**：同业动态看板（让从业者追踪各家 Skill 上线/更新/下架）
- **Invest Brain**：工具推荐引擎（用户说需求 → 推荐对应 Skill → 一键安装）
- **Investment Buddy Pet**：人格化工具推荐（12只宠物各推荐不同工具组合）
- **公众号 FinAI Station**：金融人怎么用 AI 的内容专栏
- **同业 Skill 尽调系列**：每家机构一篇深度拆解文章

### 1.3 用户画像

| 角色 | 场景 | 需求 |
|------|------|------|
| 券商/基金产品经理 | 竞品调研 | "同业都上了什么 Skill？我们落后了吗？" |
| 量化研究员 | 工具选型 | "哪个 MCP Server 的数据最全？怎么装？" |
| 独立理财师 | 投顾交付 | "给客户做资产配置，推荐什么工具组合？" |
| 金融科技爱好者 | 行业学习 | "金融 AI 现在发展到什么程度了？" |

---

## 二、目标

### 2.1 本次2天冲刺的核心目标

1. **FinancePro 动态看板**上线：awesome-finai-tools-zn 新增「机构 Skill 动态」章节，自动化追踪 10 家核心机构的 Skill 变化
2. **Invest Brain 工具推荐**集成：awesome-finai-tools-zn 的 SKILL.md 增加"按场景推荐工具"逻辑，Invest Brain 可直接读取
3. **Buddy Pet 工具人格化**：为 12 只投资宠物各匹配一套工具推荐方案
4. **公众号首发文章**：一篇介绍 FinAI 小站的文章（"金融人怎么用 AI"专栏开篇）
5. **同业 Skill 尽调第一篇**：选择一个标杆机构写深度拆解（定位/目标/做法/评价）

### 2.2 长期目标

- 10 篇同业 Skill 尽调系列文章
- FinancePro 成为金融科技从业者的日常参考
- awesome-finai-tools-zn 突破 100 Star
- 形成"数据底座 → 多产品分发"的自动化流水线

---

## 三、"一鱼多吃"架构

```
                        awesome-finai-tools-zn（数据底座）
                        ├── tools.json（结构化工具清单）
                        ├── SKILL.md（AI Agent 可读的工具推荐逻辑）
                        ├── 机构 Skill 调研数据（17家深度资料）
                        └── 每周巡检 Pipeline（自动发现新工具）
                                      │
          ┌───────────────┬───────────┼───────────┬───────────────┐
          ▼               ▼           ▼           ▼               ▼
    FinancePro      Invest Brain  Buddy Pet   公众号专栏     同业尽调系列
    （动态看板）    （工具推荐）   （人格匹配）（FinAI Station）（10篇深度文章）
          │               │           │           │               │
    同业追踪看板    "我需要XX数据"  松果推荐ETF  开篇：金融人   广发证券篇
    机构对比表格    →推荐ashare-mcp 孤狼推荐量化  怎么用AI     东方财富篇
    更新日志        →一键安装命令  智多星推荐    工具推荐教学  国泰海通篇
                                   投研组合      案例拆解      华泰证券篇
                                                每周更新      ...
```

### 数据流转路径

1. **调研数据** → 写入 tools.json / README → 同时输出为公众号文章素材
2. **SKILL.md** → Invest Brain 读取 → Buddy Pet 匹配规则 → 公众号"本周推荐"栏目
3. **巡检 Pipeline** → 发现新工具 → FinancePro 更新日志 → 公众号"本周新发现"
4. **公众号文章** → 文末引导 → GitHub Star → 更多贡献者 → 更全的数据 → 循环

---

## 四、原子任务拆解 & 优先级

### 阶段一：底座加固（Day 1 上午，约 3h）

| 编号 | 任务 | 描述 | 产出物 | 优先级 | 预估时间 |
|------|------|------|--------|--------|----------|
| T1.1 | 机构 Skill 数据入库 | 将 17 家机构的 Skill 调研数据写入仓库 `data/institution-skills.json`（结构化 JSON） | `data/institution-skills.json` | 🔴 P0 | 40min |
| T1.2 | README 新增「机构 Skill 矩阵」章节 | 在 README.md 新增独立章节，用表格列出 10 家核心机构的 Skill 名称/数量/平台/获取方式 | README.md 更新 | 🔴 P0 | 30min |
| T1.3 | FinancePro 动态看板设计 | 在 README 中新增"📡 机构 Skill 动态"章节，含最近更新日期/变化摘要/趋势评论；格式可直接复用为公众号素材 | README.md 更新 | 🔴 P0 | 40min |
| T1.4 | SKILL.md 增强：场景→工具映射 | 按 8 个场景（查行情/诊基/选股/研报/ETF/宏观/量化回测/多Agent投研）建立工具推荐映射表，Agent 读 SKILL.md 即可自动推荐 | `SKILL.md` 更新 | 🔴 P0 | 40min |
| T1.5 | 推送到 GitHub | 将所有变更 commit + push，触发 GitHub Pages 更新 | Git commit | 🔴 P0 | 10min |

### 阶段二：产品联动（Day 1 下午，约 3h）

| 编号 | 任务 | 描述 | 产出物 | 优先级 | 预估时间 |
|------|------|------|--------|--------|----------|
| T2.1 | Invest Brain 集成入口 | 在 invest-brain 仓库 README 新增"🛠️ 推荐工具链"章节，引用 awesome-finai-tools-zn 的 SKILL.md；在代码中增加 tools.json 读取接口 | invest-brain 更新 | 🔴 P0 | 50min |
| T2.2 | Buddy Pet 工具人格匹配表 | 为 12 只投资宠物各匹配 2-3 个推荐工具（如：松果→ETF 类工具、孤狼→量化回测工具、智多星→多 Agent 投研工具）；写入 `data/pet-tool-mapping.json` | `data/pet-tool-mapping.json` | 🟡 P1 | 50min |
| T2.3 | Buddy Pet 仓库集成 | 在 investment-buddy-pet 仓库中引用匹配表，增加"🛠️ 我的工具箱"模块 | investment-buddy-pet 更新 | 🟡 P1 | 40min |
| T2.4 | 统一底部联动模板 | 为 5 个核心仓库（awesome-finai-tools-zn / invest-brain / investment-buddy-pet / SoloAdvisor-Toolkit / knowledge-workflow）统一添加底部"工具链联动"章节 | 5个仓库 README 更新 | 🟡 P1 | 40min |

### 阶段三：内容产出（Day 2 上午，约 4h）

| 编号 | 任务 | 描述 | 产出物 | 优先级 | 预估时间 |
|------|------|------|--------|--------|----------|
| T3.1 | 公众号开篇文章：《金融人怎么用 AI：FinAI 小站使用指南》 | 结构：①痛点（金融人面对 AI 工具的选择困难）②小站介绍（收录了什么、怎么用）③三个实战案例（零配置查行情/一键诊基/量化回测）④下一步（同业 Skill 尽调系列预告）| `output/公众号_FinAI小站使用指南.md` | 🔴 P0 | 90min |
| T3.2 | 同业 Skill 尽调第一篇：《广发证券 Skill 生态深度拆解》 | 结构：①定位（行业首家多平台布局）②8个C端Skill逐个拆解（功能/数据源/适用场景/评价）③底层架构（110+MCP+天玑大模型）④竞品对比（vs东财/vs国泰海通）⑤结论：券商 Skill 的标杆 | `output/同业尽调_01_广发证券.md` | 🔴 P0 | 120min |
| T3.3 | 公众号排版适配 | 将两篇文章转为公众号可用格式（标题/导语/小标题/配图建议/文末引流） | 格式调整 | 🟡 P1 | 30min |

### 阶段四：自动化推进（Day 2 下午，约 2h）

| 编号 | 任务 | 描述 | 产出物 | 优先级 | 预估时间 |
|------|------|------|--------|--------|----------|
| T4.1 | 公众号文章排期表 | 制定 10 篇同业尽调文章的发布计划（每周一篇的节奏、标题、覆盖机构、发布时间） | `data/content-calendar.md` | 🟡 P1 | 30min |
| T4.2 | 尽调模板标准化 | 为同业尽调系列建立统一模板（定位/目标/具体做法/Skill清单/竞品对比/评价），后续文章直接套用 | `data/due-diligence-template.md` | 🟡 P1 | 30min |
| T4.3 | 自动化巡检 + 公众号素材生成 | 扩展 `update_china_platforms.py`，增加一个输出函数：当发现新 Skill 时，自动生成公众号"本周新发现"段落的 Markdown 素材 | `scripts/update_china_platforms.py` 更新 | 🟢 P2 | 40min |
| T4.4 | 两天冲刺进度看板 | 在 awesome-finai-tools-zn 仓库新建一个 Issue，列出全部任务的 checkbox，完成后勾选，公开可见 | GitHub Issue | 🟡 P1 | 20min |

---

## 五、2天执行时间线

```
Day 1（7月15日 周二）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
09:00-09:40  T1.1  机构 Skill 数据入库
09:40-10:10  T1.2  README 机构 Skill 矩阵
10:10-10:50  T1.3  FinancePro 动态看板
10:50-11:30  T1.4  SKILL.md 场景映射增强
11:30-11:40  T1.5  Push GitHub
━━━━━━━━━━━ 午休 ━━━━━━━━━━━━━━━━━━━━━━━━━━
14:00-14:50  T2.1  Invest Brain 集成
14:50-15:40  T2.2  Buddy Pet 工具匹配表
15:40-16:20  T2.3  Buddy Pet 仓库更新
16:20-17:00  T2.4  统一底部联动模板
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Day 2（7月16日 周三）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
09:00-10:30  T3.1  公众号开篇文章
10:30-12:30  T3.2  广发证券尽调第一篇
━━━━━━━━━━━ 午休 ━━━━━━━━━━━━━━━━━━━━━━━━━━
14:00-14:30  T3.3  排版适配
14:30-15:00  T4.1  文章排期表
15:00-15:30  T4.2  尽调模板标准化
15:30-16:10  T4.3  自动化巡检扩展
16:10-16:30  T4.4  进度看板 Issue
16:30-17:00  收尾：全部 Push + 检查 + 写 Day 2 总结
```

---

## 六、10 篇同业 Skill 尽调系列规划

| 序号 | 机构 | 核心看点 | 建议发布节奏 |
|------|------|---------|-------------|
| 01 | 广发证券 | 行业最全面，8个C端 Skill + 110+MCP底层 | Day 2 完成 |
| 02 | 东方财富 | C端流量最大，7个妙想 Skill + Choice底层 | 第2周 |
| 03 | 国泰海通 | 首批官方金融 Skill 包，6个 Skill | 第3周 |
| 04 | 华泰证券 | 机构+零售双线，含A股模拟交易 | 第4周 |
| 05 | 中金公司 | 分析师 IP 化，首席数字分身 | 第5周 |
| 06 | 易方达基金 | 唯一对接 WorkBuddy 的基金公司 | 第6周 |
| 07 | 万得 | 数据最全面，AIFin Market MCP生态 | 第7周 |
| 08 | 同花顺 | iFinD MCP + 问财 SkillHub | 第8周 |
| 09 | 盈米基金 | 69个MCP工具，组合回测+蒙特卡洛 | 第9周 |
| 10 | 国信证券 | 自研 6 大 Skills + 中小券商破局思路 | 第10周 |

---

## 七、成功指标

| 指标 | 当前 | Day 2 目标 | 2周目标 |
|------|------|-----------|---------|
| GitHub Stars | 1 | 10 | 50 |
| 机构 Skill 收录数 | 5家 | 10家 | 17家 |
| 公众号文章 | 0 | 2篇 | 4篇 |
| 项目间引用关系 | 0 | 5个仓库互联 | 10个仓库互联 |
| FinancePro 动态看板 | 无 | 上线 | 自动化更新 |

---

## 八、风险与应对

| 风险 | 影响 | 应对 |
|------|------|------|
| 机构 Skill 信息变化快 | 文章内容过时 | 每篇文章注明"信息截止日期"，GitHub数据保持每周更新 |
| 公众号排版耗时 | 占 Day2 过多时间 | 用 Markdown 写，公众号编辑器直接粘贴，不做过度排版 |
| Buddy Pet 仓库改动大 | 超出时间预算 | 先做匹配表 JSON，仓库集成放下一轮冲刺 |
| Git 推送环境问题 | 阻塞全部任务 | Day 1 早上第一批任务就是要确认推送可用 |
*（内容由AI生成，仅供参考）*

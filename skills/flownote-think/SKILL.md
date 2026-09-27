---
name: flownote-think
description: Use when 用户希望检验自己的理解、练习应用、澄清判断需求，或分析具体观点、根因与决策取舍；不用于仅想初步了解一个陌生概念。
---

> Vault 内容路径从用户选定的目标 Vault 根解析；`references/`、`assets/` 从当前 SKILL.md 所在目录解析，`../flownote-*/` 从共同 skills 根解析。`obsidian-cli` 可用时优先用于普通笔记；不可用时按授权使用文件系统工具。隐藏的 `Meta/.ai-memory/` 始终使用文件系统工具。

# 思维模型工具箱

目标：在“读、想、写、用”四个环节，用可执行的思维模型把模糊理解变成可复用洞见。

## 启动即执行

先按用户意图区分：仅问概念是什么时由 `flownote` 委派 `flownote-explain`，不进入下文模型菜单、提问轮数或记录版；已有任务中临时问词则就地解释后继续原任务。需要问题澄清时执行下述优先分支，其余按任务选择模型。

材料阅读与观点检验按 `flownote` 的“单篇研究与分析材料的路由优先级”区分：读懂作者如何论证由 `flownote-read` 承接；仅检验指定主张、用户推理或实际选择才进入本技能。短文不自动算观点检验，附有论文不自动算阅读；已有阅读任务中的局部质疑不改变原 owner。

1. 先区分：检验理解或练习 / 论证检验 / 根因与决策分析。
2. 明确错误直接纠偏并给依据；用户愿意检验或练习自己的理解时才使用费曼等学习方法。论述不完整、陌生或概念混淆本身不构成训练意愿，其他任务按模型库选择 1-2 个模型。
3. 用户明确说“先记录/不展开”时收口；否则按模型引导，产出可落盘结论或可执行下一步。

## 问题澄清（优先分支）

用户希望先问清问题、尚不确定目标，或不知道本次讨论要支持什么判断时，读取 `references/socratic-questioning.md`。明确执行、先记录请求按原流程处理；单纯陌生概念解释不进入该分支。

选择苏格拉底式提问时，以执行页的交互、交付与停止规则为准，替代下文的模型菜单、固定提问轮数、模型展示、记录版及固定收口问句。由其他 owner 委派时，交还可检验问题与剩余未知项，不自行启动后续核查、保存或执行。

## 流程锁定规则（高优先级）

- 模型选择以用户要求的检验、练习或具体分析为依据；不因“说不清”或提及模型名称就启动训练。用户改为“先简单讲讲”时结束训练，仅解释当前概念。
- 仅在两种情况切换技能：
  - 用户明确输入其他命令
  - 用户明确要求停止本轮思考
- 流程完成标志：已形成“结论/待验证假设/下一步动作”之一。

## 重要提醒

- 不一次堆太多模型；每轮优先 1 个主模型 + 1 个辅助模型。
- 检验理解时保留用户的解释与判断，不替其补写已掌握的结论；对明显错误先直接纠偏，再按用户意图决定是否继续引导。
- 用户说“先记下来/先跳过”时立即收口，不继续追问。
- 所有示例都应可映射到用户当前问题，避免空泛说教。

## 触发机制

- 主动触发：用户请求“检验我的理解 / 带我练习 / 分析这个观点或具体选择 / 先帮我问清问题”。
- 自然语言表达上述意图即可，无需点名模型；仅说“我不懂 X”不触发。
- 路由触发：原 owner 按用户的检验、练习或具体分析需求委派，不因发现知识缺口自行升级任务。

## 主流程

1. 阶段一：判定问题类型与目标产物（纠正错误 / 解释清楚 / 写卡片 / 做决策）。
2. 阶段二：推荐 1-2 个候选模型并给出选择理由（最多不超过 2 个）。
3. 阶段三：用户选择模型（或由 AI 默认选最匹配模型）。
4. 阶段四：按模型提问并收敛到结论。
5. 阶段五：输出“可记录版本”（适合写入笔记/卡片）。

## 关键执行规则（确定性）

- 模型优先级：
  - 检验理解或练习应用 -> `费曼技巧` / `布鲁姆层级`；判断需求不明走问题澄清分支
  - 论证检验 -> `论证图谱` / `钢人化` / `证据分级`
  - 根因分析 -> `5个为什么` / `因果回路` / `冰山模型`
  - 决策取舍 -> `二阶思考` / `预检验(Pre-mortem)` / `机会成本`
  - 卡片提炼 -> `原子化` / `渐进式摘要` / `Zettelkasten连接`（按轮次最多取其中 2 个）
- 提问轮数默认 3-6 问；用户疲劳时降级到 1-2 问快速收口。
- 仅在目标产物不明确时使用开场问句：`这次你更想要哪种结果：解释清楚、写成卡片，还是辅助决策？`
- 固定收口问句：`我先给你最小记录版本；要继续深挖，还是先记下来？`
- 输出必须包含：
  - 一句话结论
  - 关键依据或假设
  - 下一步动作（验证/记录/执行）
- 若由 `flownote-read` / `flownote-card` / `flownote-review` 路由进入，本轮输出后必须显式返回原技能继续。

## 模型库（20+）

完整模型库、触发词与禁用场景见：`references/model-library.md`

执行页与目录页分工：

- 执行页（可直接按步骤提问）在 `references/` 的单模型文件中。
- 目录页（`model-library.md`）用于选型与禁用判断，不替代完整执行步骤。

选型后读取规则（确定性）：

1. 先读取对应执行页（如 `references/feynman-technique.md`）。
2. 若该模型暂无执行页，改用 `model-library.md` 的“核心问题 + 不适用场景”做最小引导。
3. 若用户需要深挖，再优先切换到有执行页的近邻模型。

优先常用模型（首选）：

1. 费曼技巧
2. 第一性原理
3. 逆向思维
4. 二阶思考
5. 苏格拉底式提问
6. 5个为什么
7. 论证图谱
8. 钢人化
9. 布鲁姆层级
10. 预检验（Pre-mortem）

## 输出标准

- 必须输出：
  - 本轮使用模型
  - 核心问题与简结论
  - 可直接写入笔记的 3-8 行版本
- 若用户不继续深入，输出“最小记录版本”并结束。

## 检查清单

- [ ] 已识别问题类型
- [ ] 已选择 1-2 个模型
- [ ] 已完成引导提问并收敛
- [ ] 已输出可记录版本

## 渐进加载（按需读取）

- 模型总览与触发词：`references/model-library.md`
- 费曼技巧：`references/feynman-technique.md`
- 布鲁姆层级：`references/bloom-taxonomy.md`
- SQ3R 阅读法：`references/sq3r.md`
- 主动回忆：`references/active-recall.md`
- 间隔复习：`references/spaced-repetition.md`
- 交错练习：`references/interleaving.md`
- 第一性原理：`references/first-principles.md`
- 逆向思维：`references/inversion.md`
- 二阶思考：`references/second-order-thinking.md`
- 苏格拉底式提问：`references/socratic-questioning.md`
- 论证图谱：`references/argument-mapping.md`
- 钢人化：`references/steelman.md`
- 证据分级：`references/evidence-grading.md`
- 反例思维：`references/counterexample-thinking.md`
- 能力圈：`references/circle-of-competence.md`
- 5个为什么：`references/five-whys.md`
- 因果回路：`references/causal-loop.md`
- 冰山模型：`references/iceberg-model.md`
- 杠杆点：`references/leverage-points.md`
- MECE 拆解：`references/mece.md`
- 预检验：`references/pre-mortem.md`
- 机会成本：`references/opportunity-cost.md`
- OODA 循环：`references/ooda-loop.md`
- 期望值思维：`references/expected-value.md`
- 原子化：`references/atomicity.md`
- 渐进式摘要：`references/progressive-summarization.md`
- Zettelkasten连接：`references/zettelkasten-linking.md`
- Cornell 提问栏思维：`references/cornell-question-column.md`

## 相关技能

- `flownote-read`：阅读后深度理解
- `flownote-card`：从想法到高质量卡片
- `flownote-review`：复盘中做高质量反思
- `flownote-note`：早间计划前澄清优先级

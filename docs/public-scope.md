# FLOWnote 公开候选范围（Task 1 文件清单）

本清单只决定去向，不复制正文、不改变来源 Vault。固定审计点：本地 FLOWnote Git `5fcfa6d48d87bd5729a1bae67d7b6bfc1790fa66`。`S` 列的每一项是相对 Vault 的 `.flownote/skills/` 下路径；除明确写“无”外，目标 `T` 是同一相对项置于本仓库 `skills/` 下。例如 `flownote-capture/SKILL.md` 表示源 `.flownote/skills/flownote-capture/SKILL.md` → 目标 `skills/flownote-capture/SKILL.md`。消费者列均为**目标仓库相对路径**，不是本机安装路径。`直`=直接引入，`改`=通用化后引入，`否`=不发布。**全部引入动作仍受 SOURCES.md 的许可门槛约束。**

从 19 个入口实际枚举出 98 个普通文件（含 19 个 SKILL.md）；仅枚举各入口下的文件，不跟随目录链接复制其外部目标。`flownote-inbox/assets/永久笔记模板.md` 与 `flownote-read/references/note-template.md` 是未被相应工作流引用的旧模板，给出明确不发布去向；其余 96 个文件有候选用途。此处的“直”只表示无需改路径/行为，不表示已通过逐文件隐私复核。用户已授权本地候选构建；SOURCES.md 所列第三方 MIT 通知须随派生正文保留，新增本地内容的最终公开许可证待决，不将其误作本地复制阻塞。

| S → T（共享上述前缀） | 处置 | 直接消费者与理由 |
|---|---|---|
| `flownote/SKILL.md` | 改 | `skills/flownote/SKILL.md`；19 项路由入口，需把安装目录与本地状态假设改为用户 Vault 相对约定。 |
| `flownote-archive/SKILL.md` | 改 | `skills/flownote/SKILL.md`；归档入口，通用化 Obsidian 客户端优先级。 |
| `flownote-archive/references/path-rules.md` | 直 | `skills/flownote-archive/SKILL.md`；归档移动路径。 |
| `flownote-archive/references/workflow-details.md` | 直 | `skills/flownote-archive/SKILL.md`；归档分支与更新顺序。 |
| `flownote-capture/SKILL.md` | 改 | `skills/flownote/SKILL.md`；捕获入口，需以技能根解析兄弟模板。 |
| `flownote-capture/references/response-templates.md` | 直 | `skills/flownote-capture/SKILL.md`；交互回执。 |
| `flownote-capture/references/routing-and-edge-cases.md` | 直 | `skills/flownote-capture/SKILL.md`；记录/任务分流。 |
| `flownote-capture/references/write-update-rules.md` | 直 | `skills/flownote-capture/SKILL.md`，亦供 `flownote-note`, `flownote-inbox`, `flownote-review`, `flownote-week/month/year`；可信时间与补录规则。 |
| `flownote-card/SKILL.md` | 改 | `skills/flownote/SKILL.md` 与 `skills/flownote-read/SKILL.md`；制卡入口、跨技能路由；混合项目来源仅按用户实际提供的候选与理解记录核对。 |
| `flownote-card/references/链接规范.md` | 通用化 | `skills/flownote-card/SKILL.md`；保留卡片链接格式，将具体项目名称示例替换为编号与项目名占位符。 |
| `flownote-card/references/article-to-cards-guide.md` | 直 | `skills/flownote-card/SKILL.md`；来源路径 A。 |
| `flownote-card/references/card-template.md` | 直 | `skills/flownote-card/SKILL.md`；权威卡片模板。 |
| `flownote-card/references/literature-note-cards-guide.md` | 直 | `skills/flownote-card/SKILL.md`；来源路径 B。 |
| `flownote-card/references/user-note-cards-guide.md` | 直 | `skills/flownote-card/SKILL.md`；来源路径 C。 |
| `flownote-card/references/workflow-and-sync-rules.md` | 改 | `skills/flownote-card/SKILL.md`；确认、只读来源与同步；去掉本机项目专名。 |
| `flownote-card/references/zettelkasten-principles.md` | 直 | `skills/flownote-card/SKILL.md`；质量标准。 |
| `flownote-distill/SKILL.md` | 改 | `skills/flownote/SKILL.md`；会话提炼入口，指针只在用户 Vault 中；去掉本机项目专名。 |
| `flownote-explain/SKILL.md` | 改 | `skills/flownote/SKILL.md`；轻量概念解释；上游归属/许可通知留在原分发仓库的 SOURCES.md，不作为 Vault 运行依赖。 |
| `flownote-inbox/SKILL.md` | 改 | `skills/flownote/SKILL.md`；残留记录处理，兄弟捕获规则从 skills 根解析。 |
| `flownote-inbox/assets/永久笔记模板.md` → 无 | 否 | `skills/flownote-inbox/SKILL.md` 与 sidecar 均未引用；制卡使用 `skills/flownote-card/references/card-template.md`，避免两个权威卡片模板。 |
| `flownote-inbox/references/output-templates.md` | 直 | `skills/flownote-inbox/SKILL.md`；批量确认回执。 |
| `flownote-inbox/references/workflow-and-routing-rules.md` | 直 | `skills/flownote-inbox/SKILL.md`；候选范围与去向。 |
| `flownote-init/SKILL.md` | 改 | `skills/flownote/SKILL.md`；初始化入口，运行状态仅在目标 Vault 创建。 |
| `flownote-init/references/记忆系统初始化模板.md` | 直 | `skills/flownote-init/SKILL.md`；状态区初始化。 |
| `flownote-init/references/领域页模板.md` | 直 | `skills/flownote-init/SKILL.md` 与 `skills/flownote-project/SKILL.md`；领域页权威模板。 |
| `flownote-init/references/永久笔记迁移格式.md` | 直 | `skills/flownote-init/SKILL.md`；迁移格式。 |
| `flownote-init/references/主题笔记模板.md` | 直 | `skills/flownote-init/SKILL.md`；主题页权威模板。 |
| `flownote-init/references/HOME模板.md` | 直 | `skills/flownote-init/SKILL.md`；HOME 权威模板。 |
| `flownote-init/references/kb-manifest模板.md` | 直 | `skills/flownote-init/SKILL.md`；索引模板。 |
| `flownote-legacy/SKILL.md` | 改 | `skills/flownote/SKILL.md`；旧笔记迁移入口，状态路径按目标 Vault。 |
| `flownote-legacy/references/状态更新规范.md` | 直 | `skills/flownote-legacy/SKILL.md`；任务文件/STATUS 更新顺序。 |
| `flownote-memory/SKILL.md` | 改 | `skills/flownote/SKILL.md` 及各状态维护技能；隐藏状态目录在目标 Vault，文件系统访问。 |
| `flownote-memory/references/skill-interface-spec.md` | 直 | `skills/flownote-memory/SKILL.md`；跨技能状态接口。 |
| `flownote-memory/references/status-and-buffer-rules.md` | 直 | `skills/flownote-memory/SKILL.md`；STATUS 与缓冲区。 |
| `flownote-memory/references/task-file-templates.md` | 直 | `skills/flownote-memory/SKILL.md`；权威任务文件结构。 |
| `flownote-month/SKILL.md` | 改 | `skills/flownote/SKILL.md`；月回顾入口，兄弟捕获时间规则按技能根解析。 |
| `flownote-month/references/数据汇总模板.md` | 直 | `skills/flownote-month/SKILL.md`；数据叙述。 |
| `flownote-month/references/想法标记规范.md` | 直 | `skills/flownote-month/SKILL.md`；状态标记。 |
| `flownote-month/references/月报模板.md` | 直 | `skills/flownote-month/SKILL.md`；月记权威模板。 |
| `flownote-month/references/workflow-and-planning-rules.md` | 直 | `skills/flownote-month/SKILL.md`；分阶段回顾。 |
| `flownote-note/SKILL.md` | 改 | `skills/flownote/SKILL.md`；日记入口，兄弟捕获时间规则按技能根解析。 |
| `flownote-note/assets/每日笔记模板.md` | 直 | `skills/flownote-note/SKILL.md` 与 `skills/flownote-capture/SKILL.md`；六章节日记权威模板。 |
| `flownote-note/references/回顾提醒规则.md` | 直 | `skills/flownote-note/SKILL.md`；周期提醒。 |
| `flownote-note/references/workflow-and-context-rules.md` | 直 | `skills/flownote-note/SKILL.md`；写入与上下文。 |
| `flownote-paper/LICENSE` | 直 | `skills/flownote-paper/{SKILL.md,ReadingGuide.md,references/template.md}`；随派生内容保留上游 MIT 通知。 |
| `flownote-paper/ReadingGuide.md` | 改 | `skills/flownote-paper/SKILL.md`；删除/调整对不打包 paper-map 的依赖，与 no-save 交付一致。 |
| `flownote-paper/SKILL.md` | 改 | `skills/flownote-read/SKILL.md` 与 `skills/flownote/SKILL.md`；论文解释委派。 |
| `flownote-paper/references/template.md` | 直 | `skills/flownote-paper/SKILL.md`；Markdown 解释草稿。 |
| `flownote-project/SKILL.md` | 改 | `skills/flownote/SKILL.md`；`/.opencode/skills/...` 改为技能根相对的 `flownote-init/references/领域页模板.md`；外部来源只按实际可核验记录使用，Dataview 可选。 |
| `flownote-project/assets/项目模板.md` | 改 | `skills/flownote-project/SKILL.md`；修复 Dataview 围栏、移除本机组合看板依赖，缺插件时使用 Markdown 链接。 |
| `flownote-project/references/output-templates.md` | 直 | `skills/flownote-project/SKILL.md`；项目回执。 |
| `flownote-project/references/workflow-and-domain-rules.md` | 改 | `skills/flownote-project/SKILL.md`；领域与项目流程；修正固定客户端模板路径，并允许无 Dataview 的 Markdown 目录。 |
| `flownote-read/SKILL.md` | 改 | `skills/flownote/SKILL.md`；三处 `.opencode/skills/.../extract_weread_outline.py` 命令改从当前技能文件定位脚本，跨技能制卡从 skills 根解析。 |
| `flownote-read/assets/进度模板.md` | 直 | `skills/flownote-read/SKILL.md`；阅读进度权威模板。 |
| `flownote-read/assets/extract_weread_outline.py` | 直 | `skills/flownote-read/SKILL.md` 与 `skills/flownote-read/references/wechat-export-outline-workflow.md`；仅处理用户提供的 Markdown 路径。 |
| `flownote-read/references/检查清单.md` | 直 | `skills/flownote-read/SKILL.md`；阅读验收。 |
| `flownote-read/references/文献笔记模板.md` | 直 | `skills/flownote-read/SKILL.md`；文献笔记权威模板。 |
| `flownote-read/references/note-template.md` | 否 | `skills/flownote-read/SKILL.md` 未引用；已有 `references/文献笔记模板.md` 作为权威笔记模板。 |
| `flownote-read/references/wechat-export-outline-workflow.md` | 改 | `skills/flownote-read/SKILL.md`；两处 `.opencode/skills/...` 命令改从技能内脚本解析。 |
| `flownote-review/SKILL.md` | 改 | `skills/flownote/SKILL.md`；`session-pointers.md` 在目标 Vault，三平台脚本相对目标 Vault 根的 `scripts/`，缺失时说明覆盖。 |
| `flownote-review/references/对话示例.md` | 直 | `skills/flownote-review/SKILL.md`；合成/示例话术，候选复核不含真实会话。 |
| `flownote-review/references/想法标记规范.md` | 直 | `skills/flownote-review/SKILL.md`；记录标记。 |
| `flownote-review/references/workflow-and-handoff-rules.md` | 直 | `skills/flownote-review/SKILL.md`；与 distill、inbox 移交边界。 |
| `flownote-think/SKILL.md` | 改 | `skills/flownote/SKILL.md`；深思入口，模型执行页均从当前文件 `references/` 解析。 |
| `flownote-think/references/model-library.md` | 直 | `skills/flownote-think/SKILL.md`；28 个模型的选型索引。 |
| `flownote-think/references/active-recall.md` | 直 | `skills/flownote-think/SKILL.md` / `references/model-library.md`；主动回忆执行页。 |
| `flownote-think/references/argument-mapping.md` | 直 | 同上；论证图谱执行页。 |
| `flownote-think/references/atomicity.md` | 直 | 同上；原子化执行页。 |
| `flownote-think/references/bloom-taxonomy.md` | 直 | 同上；布鲁姆层级执行页。 |
| `flownote-think/references/causal-loop.md` | 直 | 同上；因果回路执行页。 |
| `flownote-think/references/circle-of-competence.md` | 直 | 同上；能力圈执行页。 |
| `flownote-think/references/cornell-question-column.md` | 直 | 同上；Cornell 提问栏执行页。 |
| `flownote-think/references/counterexample-thinking.md` | 直 | 同上；反例思维执行页。 |
| `flownote-think/references/evidence-grading.md` | 直 | 同上；证据分级执行页。 |
| `flownote-think/references/expected-value.md` | 直 | 同上；期望值执行页。 |
| `flownote-think/references/feynman-technique.md` | 直 | 同上；费曼技巧执行页。 |
| `flownote-think/references/first-principles.md` | 直 | 同上；第一性原理执行页。 |
| `flownote-think/references/five-whys.md` | 直 | 同上；五个为什么执行页。 |
| `flownote-think/references/iceberg-model.md` | 直 | 同上；冰山模型执行页。 |
| `flownote-think/references/interleaving.md` | 直 | 同上；交错练习执行页。 |
| `flownote-think/references/inversion.md` | 直 | 同上；逆向思维执行页。 |
| `flownote-think/references/leverage-points.md` | 直 | 同上；杠杆点执行页。 |
| `flownote-think/references/mece.md` | 直 | 同上；MECE 执行页。 |
| `flownote-think/references/ooda-loop.md` | 直 | 同上；OODA 执行页。 |
| `flownote-think/references/opportunity-cost.md` | 直 | 同上；机会成本执行页。 |
| `flownote-think/references/pre-mortem.md` | 直 | 同上；预检验执行页。 |
| `flownote-think/references/progressive-summarization.md` | 直 | 同上；渐进式摘要执行页。 |
| `flownote-think/references/second-order-thinking.md` | 直 | 同上；二阶思考执行页。 |
| `flownote-think/references/socratic-questioning.md` | 改 | `skills/flownote-think/SKILL.md` 明确调用；苏格拉底提问执行页；移除私人笔记标题引用，保留规则本身。 |
| `flownote-think/references/spaced-repetition.md` | 直 | `skills/flownote-think/SKILL.md` / `references/model-library.md`；间隔复习执行页。 |
| `flownote-think/references/sq3r.md` | 直 | 同上；SQ3R 执行页。 |
| `flownote-think/references/steelman.md` | 直 | 同上；钢人化执行页。 |
| `flownote-think/references/zettelkasten-linking.md` | 直 | 同上；Zettelkasten 连接执行页。 |
| `flownote-week/SKILL.md` | 改 | `skills/flownote/SKILL.md`；周回顾入口，兄弟捕获时间规则按 skills 根解析。 |
| `flownote-week/references/想法标记规范.md` | 直 | `skills/flownote-week/SKILL.md`；状态标记。 |
| `flownote-week/references/周报模板.md` | 直 | `skills/flownote-week/SKILL.md`；周记权威模板。 |
| `flownote-year/SKILL.md` | 改 | `skills/flownote/SKILL.md`；年回顾入口，兄弟捕获时间规则按 skills 根解析。 |
| `flownote-year/references/年报模板.md` | 直 | `skills/flownote-year/SKILL.md`；年记权威模板。 |

## 目标 Vault 的 `scripts/` 与合成测试

以下源/目标都相对 Vault 根/候选仓库根，原 `scripts/tests/` 布局不变。读取器运行时由用户 Vault `.flownote/session-pointers.md` 指定各平台日志根；脚本自身没有内置真实用户路径，`--root` 必填。测试只在 `tempfile.TemporaryDirectory()` 下构造 JSONL/state，`/example` 是合成 cwd；未发现真实 session 输入或本机绝对路径。31 个测试方法的详细运行证据在被忽略的 Task 1 报告。

| 源 → 目标 | 处置 | 直接消费者 |
|---|---|---|
| `scripts/codex_session_day.py` → 同路径 | 直 | `skills/flownote-review/SKILL.md`；Codex 按日会话读取。 |
| `scripts/claude_session_day.py` → 同路径 | 直 | `skills/flownote-review/SKILL.md`；Claude 按日会话读取。 |
| `scripts/kimi_session_day.py` → 同路径 | 直 | `skills/flownote-review/SKILL.md`；Kimi 按日会话读取。 |
| `scripts/tests/test_codex_session_day.py` → 同路径 | 直 | `scripts/codex_session_day.py` 的合成测试。 |
| `scripts/tests/test_claude_session_day.py` → 同路径 | 直 | `scripts/claude_session_day.py` 的合成测试。 |
| `scripts/tests/test_kimi_session_day.py` → 同路径 | 直 | `scripts/kimi_session_day.py` 的合成测试。 |

## `Meta/模板/` 对照：全部不发布第二份

这里的源是 Vault 根 `Meta/模板/<文件>`；目标栏写实际工作的技能内权威文件。对照使用 SHA-256；10 份完全相同。`项目模板.md` 唯一不同：技能版多了外部项目接入摘要，且 `flownote-project/SKILL.md` 明确读取技能版。元数据与用户实际笔记不在候选范围。

| 源（均否） | 权威目标及消费者 | 对照 |
|---|---|---|
| `Meta/模板/进度模板.md` | `skills/flownote-read/assets/进度模板.md` ← `skills/flownote-read/SKILL.md` | 相同 |
| `Meta/模板/领域页模板.md` | `skills/flownote-init/references/领域页模板.md` ← `skills/flownote-init/SKILL.md`、`skills/flownote-project/SKILL.md` | 相同 |
| `Meta/模板/每日笔记模板.md` | `skills/flownote-note/assets/每日笔记模板.md` ← `skills/flownote-note/SKILL.md`、`skills/flownote-capture/SKILL.md` | 相同 |
| `Meta/模板/年报模板.md` | `skills/flownote-year/references/年报模板.md` ← `skills/flownote-year/SKILL.md` | 相同 |
| `Meta/模板/文献笔记模板.md` | `skills/flownote-read/references/文献笔记模板.md` ← `skills/flownote-read/SKILL.md` | 相同 |
| `Meta/模板/项目模板.md` | `skills/flownote-project/assets/项目模板.md` ← `skills/flownote-project/SKILL.md` | 不同；来源技能版含外部项目摘要，候选版另修围栏与依赖说明 |
| `Meta/模板/永久笔记模板.md` | `skills/flownote-card/references/card-template.md` ← `skills/flownote-card/SKILL.md` | 与旧 `flownote-inbox/assets/永久笔记模板.md` 相同；实际制卡走 card 模板 |
| `Meta/模板/月报模板.md` | `skills/flownote-month/references/月报模板.md` ← `skills/flownote-month/SKILL.md` | 相同 |
| `Meta/模板/周报模板.md` | `skills/flownote-week/references/周报模板.md` ← `skills/flownote-week/SKILL.md` | 相同 |
| `Meta/模板/主题笔记模板.md` | `skills/flownote-init/references/主题笔记模板.md` ← `skills/flownote-init/SKILL.md` | 相同 |
| `Meta/模板/HOME模板.md` | `skills/flownote-init/references/HOME模板.md` ← `skills/flownote-init/SKILL.md` | 相同 |

## 解析基准与外部能力

| 引用/消费者 | 去向与缺失处理 |
|---|---|
| `references/`, `assets/`, `ReadingGuide.md`：各 `skills/<name>/SKILL.md` | 从**当前技能文件所在目录**解析；`flownote-paper/ReadingGuide.md`、`references/template.md` 同理。不能从 shell 的当前工作目录猜。 |
| `../flownote-note/...`, `../flownote-capture/...`、`flownote-card/SKILL.md`、`flownote-init/references/领域页模板.md`：capture、note、inbox、review、week、month、year、read、project | 从**19 项共同的 `skills/` 根**解析兄弟技能。旧 `.opencode/skills/` 路径移除，安装到不同客户端后仍能找到。 |
| `.flownote/session-pointers.md` 与 `scripts/{codex,claude,kimi}_session_day.py`：review、distill | 指针只在**目标 Vault 根**；会话读取器也从目标 Vault 根的 `scripts/` 寻找。仓库仅提供脚本和无真实路径的指针示例；缺指针/失效来源就核实该项，报告覆盖缺口，不猜日志根。 |
| `Meta/.ai-memory/STATUS.md`、`reading/` 等：flownote、memory、review、read、legacy 等 | 目标 Vault 的运行数据，只在用户初始化/授权后创建；候选不包含任何现有 STATUS、任务或会话正文。 |
| `obsidian-cli`：各 SKILL 顶部优先级、explain 检索 | 可选的外部 Obsidian 官方技能/客户端能力，不随 19 项打包；不可用时使用已授权文件系统读写/检索并说明限制，不能把隐藏 `Meta/.ai-memory/` 误交 CLI。 |
| 微信读书导出 Markdown：`flownote-read/SKILL.md` 与 `references/wechat-export-outline-workflow.md` | 输入是用户已有的 Markdown；内置 `assets/extract_weread_outline.py` 可处理，不要求安装 `weread`、OCR、画图等外围技能。若无可读文本，仅说明所需输入。 |

## Task 2 实际通用化记录

- 19 项中，`flownote` 将路由路径固定到当前文件上一级的共同 skills 根，运行状态固定到目标 Vault 根。`archive`、`capture`、`card`、`inbox`、`init`、`legacy`、`month`、`note`、`project`、`read`、`review`、`think`、`week`、`year` 的入口明确：本技能 `references/`、`assets/` 从当前 SKILL.md 所在目录解析，兄弟技能从共同 skills 根解析，Vault 内容从目标 Vault 根解析。`memory` 明确隐藏状态使用文件系统工具；普通笔记在 `obsidian-cli` 不可用时按授权退到文件系统。
- `distill` 的指针基准改成目标 Vault；`review` 明确指针及 `scripts/` 由目标 Vault 根解析。`paper` 明确指南和模板由当前技能目录解析，保留原 no-save 交付；其 ReadingGuide 无 paper-map 调用，因此未改正文。
- `project/SKILL.md` 与 `project/references/workflow-and-domain-rules.md` 的固定 `/.opencode/skills/` 领域模板路径改从共同 skills 根解析。`read/SKILL.md` 的三处及 `read/references/wechat-export-outline-workflow.md` 的两处固定 `.opencode/skills/` 脚本命令改用当前技能目录，并要求运行前替换目录占位符；`read` 制卡调用也改从共同 skills 根定位。`explain` 原根 `skills-lock.json` 来源提示改指本仓库 `SOURCES.md`。`think/references/socratic-questioning.md` 去掉私人笔记标题引用，保留通用规则。
- 未改三平台读取器、测试、WeRead 解析器及其他模板；项目模板在审查修复中作上述定点调整。`README.md`、`examples/` 给出空 Vault 首次使用与指针约定，`NOTICE.md` 随附第三方通知。最终公开许可证、真实客户端发现和端到端 Vault 旅程仍由后续决定或验证。
- `.gitignore` 依据 `flownote-init/SKILL.md` 的实际目录补充 `03-连接层/`、`04-创造层/` 及受保护的 `05-项目笔记库/`，防止在仓库根试用时误跟踪 Vault 数据；保留旧目录忽略项。指针示例按 Kimi 读取器的 wire 格式与合成测试说明共享根不提供客户端归属证据。

已核实的第三方 MIT 来源、通知义务与仍待决的本地新增内容最终许可证见 `SOURCES.md`；不缩减这里的 19 项目标。

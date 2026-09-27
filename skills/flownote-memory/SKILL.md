---
name: flownote-memory
description: Use when 需要在多个 flownote-* 技能之间持续追踪进度、同步待办与避免会话切换后状态丢失时。
---

> Vault 内容路径从用户目标 Vault 根解析，`references/` 从当前 SKILL.md 所在目录解析。`obsidian-cli` 可用时优先用于普通笔记；不可用时按授权使用文件系统工具。`Meta/.ai-memory/` 是隐藏的 Agent 状态区，Obsidian 不索引；该目录必须使用文件系统工具读写。

# AI 记忆系统

目标：在所有 flownote-* 技能之间统一状态追踪，确保“可继续、可回溯、不丢任务”。

## 启动即执行

1. 使用文件系统工具读取 `Meta/.ai-memory/STATUS.md`；不得因 Obsidian 无法读取隐藏目录而改用或创建 `Meta/ai-memory/`。
2. 根据当前技能识别相关待处理项（阅读/制卡/项目/回顾/缓冲任务）。
3. 用户没有给出明确任务且存在待处理项时，提示继续处理或开始新任务；用户已明确任务时直接执行，仅在待处理状态会阻塞或改变该任务时提示。

## 流程锁定规则（高优先级）

- 记忆流程是底层能力，不因用户提及其他主题而中断。
- 仅在两种情况允许提前退出：
  - 用户明确输入其他命令并要求切换。
  - 用户明确要求停止当前任务。
- 流程完成标志：权威任务文件已更新 + 持久状态变化已整合到 `STATUS.md` + 两者复读一致 + 下一步已明确。

## 重要提醒

- 禁止使用示例数据，状态与进度必须来自真实文件或用户确认。
- 有持久状态变化时，禁止跳过结束整合；未写回并复读 `STATUS.md` 视为未完成。
- 无持久状态变化时不机械改写 `STATUS.md`，输出中明确报告“STATUS 无变化”。
- 用户明确要求停止写入时立即停止；报告已持久化与未持久化内容，不得将未完成的状态交接宣称为完成。
- 输出必须包含具体文件路径与更新内容，不能只说“已同步”。

## 核心机制（保持原功能）

“持久状态变化”指会改变未来 Agent 接手结果的任务、进度、决策、授权、检查点、待办或下一步。仅解释问题、未落盘的讨论和不改变这些内容的确认不算持久状态变化。

### 两阶段更新

1. 阶段 1（source-first）：在关键节点更新每日笔记、阅读进度、项目页等权威任务文件。
2. 阶段 2（STATUS-last）：最终回复前只把增量检查点、待办和下一步整合到 `STATUS.md`。
3. 阶段 3（verify）：复读任务文件与 `STATUS.md`；不一致时以任务文件为准修正状态索引。

### 检查点写入

- 在每个关键节点写入一次任务专属文件。
- 产生持久状态变化的每个回合都必须在最终回复前完成整合，不依赖 session 退出钩子。

## 目录规范

必须使用以下结构：

```text
Meta/.ai-memory/
├── STATUS.md
├── reading/
├── cards/
├── projects/
├── legacy/
└── reviews/
```

## 状态传递规则

- 读取方：每个技能启动时读取 `STATUS.md` 的相关区块，并用相应任务文件核验新鲜度。
- 写入方：每个技能仅在产生持久状态变化时，于任务文件落盘后写回本次增量状态。
- 常见传递：`flownote-read -> flownote-card`、`flownote-review -> flownote-note/flownote-week/flownote-month`、`flownote-project -> flownote-archive`。

## 输出标准

- 必须输出：本次更新了哪些文件、更新了哪些状态、是否产生新的待办；无状态变化时明确报告 `STATUS` 未改写。
- 若有未完成项，必须输出明确下一步（建议技能 + 对应路径）。
- 输出内容必须可追溯，不允许仅给“已更新”这类模糊结果。

## 检查清单

- [ ] 已通过文件系统读取 `Meta/.ai-memory/STATUS.md`
- [ ] 已识别并提示相关待处理项
- [ ] 已在关键节点更新任务专属文件
- [ ] 有持久变化时，已在结束阶段整合并复读 `STATUS.md`；无变化时已明确报告
- [ ] 已写明跨技能传递与下一步建议

## 渐进加载（按需读取）

- 接口与异常规则：`references/skill-interface-spec.md`
- 全局状态与缓冲区模板：`references/status-and-buffer-rules.md`
- 任务专属文件模板：`references/task-file-templates.md`

## 相关技能

- `flownote`：统一入口，启动时展示待处理项
- `flownote-note`：早晨拉取缓冲任务
- `flownote-read` / `flownote-card`：阅读到制卡的状态接力
- `flownote-review` / `flownote-week` / `flownote-month`：残留任务分层清理
- `flownote-project` / `flownote-archive`：项目状态流转与归档

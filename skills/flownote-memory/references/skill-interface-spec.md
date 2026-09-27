# Skill 接口规范

所有 flownote-* 技能接入记忆系统时，统一遵循以下接口。

## 一、启动阶段（Phase 0）

每个技能启动时必须：

1. 使用文件系统工具读取 `Meta/.ai-memory/STATUS.md`。Obsidian 不索引隐藏目录；不得将 Obsidian 的“找不到文件”当作状态不存在，也不得创建 `Meta/ai-memory/` 别名目录。
2. 只解析与当前技能相关的区块。
3. 用户没有给出明确任务且存在待处理项时，提示继续或新开；用户已明确任务时直接执行，仅在待处理状态会阻塞或改变该任务时提示。

用户尚未给出明确任务时的推荐提示：

```text
📋 发现待处理事项：
1. {{任务描述}}（来源：{{时间/来源}}）

继续处理还是开始新任务？
- A. 继续
- B. 新任务
```

## 二、执行阶段

在关键节点更新任务专属文件：

- `flownote-read`：每完成一个批次或章节
- `flownote-card`：每完成一张卡片
- `flownote-project`：每完成一个里程碑
- `flownote-review` / `flownote-inbox`：每完成一轮批处理

`flownote-read` 额外要求：

- 记录当前章节、章节范围与下一章节指针。
- 同步 `STATUS.md` 时同时写入批次进度与章节进度。

路径统一位于 `Meta/.ai-memory/` 下：

```text
reading/
cards/
projects/
legacy/
reviews/
```

## 三、结束阶段（Checkpoint）

产生持久状态变化的技能回合在最终回复前必须：

1. 更新任务专属文件的最终状态。
2. 在所有任务文件写入完成后，最后整合更新 `Meta/.ai-memory/STATUS.md`。
3. 若产生新待办，写入对应区块。
4. 复读任务文件与 `STATUS.md`，确认检查点、待办和下一步一致。
5. 输出下一步建议（如需要跨技能接力）。

若本轮没有持久状态变化，不改写 `STATUS.md`，但在输出中明确报告“STATUS 无变化”。若用户明确要求停止写入，立即停止并区分已持久化与未持久化内容；状态交接未完成时不得宣称流程完成。

## 四、跨技能状态传递

- `flownote-read -> flownote-card`：写入“待整理卡片笔记”。
- `flownote-inbox -> flownote-card`：新增待制卡来源条目。
- `flownote-project -> flownote-archive`：标记项目为“待归档”。
- `flownote-review -> flownote-note/flownote-week/flownote-month`：写入缓冲任务区。

## 五、错误处理

### STATUS 文件不存在

1. 先用文件系统确认 `Meta/.ai-memory/STATUS.md` 确实不存在；不使用 Obsidian CLI 作此判断。
2. 只读入口把它视为空状态，不因展示菜单而创建文件。
3. 首次产生持久状态变化时，创建 `Meta/.ai-memory/` 并按模板创建 `STATUS.md`。
4. 输出中说明初始化原因；不得创建 `Meta/ai-memory/`。

### 任务专属文件不存在

1. 按对应模板创建。
2. 写入最小必要字段后继续执行。
3. 若父目录不存在（如 `reading/`、`cards/`、`projects/`、`legacy/`、`reviews/`），先创建目录再写入。

### 状态不一致

1. 单一任务文件与 `STATUS.md` 冲突时，以任务文件为准。
2. 多个任务文件互相冲突时，优先采用用户明确确认的来源；仍无法裁决时保留冲突并请求用户决定，不自动覆盖。
3. 回写修正 `STATUS.md`。
4. 复读确认一致，并在输出中明确说明修复内容；写入失败或复读仍不一致时停止并报告未完成。

### 现有结构与模板不一致

1. 按区块语义读取现有 `STATUS.md`，不要求标题逐字匹配模板。
2. 不为套用模板而整体重写；只更新本轮涉及的区块。
3. 在下一次真实状态变化时渐进迁移相关区块，并保留来源与历史检查点。

# 安装与运行说明

FLOWnote is a 19-skill Obsidian Vault workflow for capture, reading, thinking, projects, reviews, and memory. `flownote` is the entry router. This early preview contains skill instructions, three optional session readers, and synthetic tests. It contains no initialized Vault state or user notes. Start with a test Vault rather than overwriting a working knowledge base.

## First use in a test Vault

1. Choose a test Vault and keep a copy of any existing files you plan to replace. Copy the **contents** of this repository's `skills/` into `<Vault>/.flownote/skills/`, preserving all 19 `flownote*` folder names and their `references/` and `assets/` files. A skill's own references and assets resolve from its `SKILL.md` directory; sibling skill references resolve from the common `.flownote/skills/` directory. Vault note paths resolve from `<Vault>`.
2. In your Agent host, configure one supported discovery entry that points to `<Vault>/.flownote/skills/flownote/SKILL.md`. [examples/AGENTS.md](../examples/AGENTS.md) shows a generic entry contract; adapt its location to the host's documented discovery mechanism. For Claude Code 2.1.283, a tested manual option is a normal file at `<Vault>/.claude/skills/flownote/SKILL.md` (no junction): copy the canonical `name` and `description` frontmatter from `.flownote/skills/flownote/SKILL.md`, then use this body: “From this Vault root, read `.flownote/skills/flownote/SKILL.md` and follow it; resolve sibling skills from that file's parent skills directory.” A fresh isolated Claude Code session discovered this thin entry. Discovery alone does not prove that a model loaded it or routed a request. Other hosts need their own documented entry mechanism.
3. Open the entry and request initialization of the **test** Vault. `flownote-init` should inspect the existing structure, ask before creating domain and topic pages, and generate `Meta/.ai-memory/STATUS.md`, `Meta/索引/kb-manifest.md`, and other pages from the bundled skill templates and empty/user-confirmed input. Do not copy an existing Vault's `Meta/`, notes, or status into the test Vault. A missing STATUS before initialization is normal.
4. For session review or distillation only, copy `scripts/{codex,claude,kimi}_session_day.py` into `<Vault>/scripts/`. Optionally copy [examples/session-pointers.example.md](../examples/session-pointers.example.md) to `<Vault>/.flownote/session-pointers.md`, then fill only verified local log roots. Python 3 is needed for these readers and the bundled WeRead Markdown outline script. Session sources are read only for the scope the user authorizes.

The default Vault structure uses `01-捕获层/`, `02-培养层/`, `03-连接层/`, `04-创造层/`, and `Meta/`. Preserve these names on first use. For a simple daily record, ask `flownote` to capture a note; it separates task progress from personal ideas and requires a trustworthy time for new `## 记录` entries. Reading and explanation can finish in the conversation without saving. A save request goes through the relevant skill's confirmation and write rules.

## External capabilities and limits

`obsidian-cli` is an optional Obsidian capability; it is not bundled here. When unavailable, use authorized filesystem access for ordinary notes. Hidden `Meta/.ai-memory/` always uses filesystem access. The project-page template includes optional Dataview queries; enable that Obsidian plugin only if you want live project-file panels. Without Dataview, `flownote-project` writes ordinary Markdown file links and marks recent-update order unverified if modification times cannot be checked. WeRead outline extraction accepts a Markdown export the user already has; a scanned or otherwise unreadable source first needs a separately chosen conversion path. OCR, drawing, download, and other peripheral skills are not included. If readable input or authorized filesystem access is missing, explain the missing input or stop that operation.

The three session readers require explicit `--root` and use UTC+8 message dates. They do not discover log roots for a new machine. See the pointer example for client overlap and subagent limits. This candidate has synthetic reader tests; a real Agent host's discovery and a complete Vault journey require separate validation.

## 来源与许可 / Provenance and license

本项目的技能体系参照并改编自 [阿浩learn 的 FLOWnote](https://github.com/1095327780/FLOWnote)，在其原 `ah` 系列基础上进行本地工作流适配、扩展及通用化整理，并非全部从零原创。`flownote-explain` 和 `flownote-paper` 另改编自 [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills)。本项目为独立改编版本，不代表上游官方发布。

本仓库采用 [MIT License](../LICENSE)。[SOURCES.md](../SOURCES.md) records the fixed upstream revisions and local audit point. [NOTICE.md](../NOTICE.md) retains the third-party MIT copyright and permission texts; `skills/flownote-paper/LICENSE` remains beside that derived skill. Keep these notices with redistributed derived material; the repository license does not replace upstream attribution. The exact included-file inventory and exclusions are in [docs/public-scope.md](public-scope.md).

To run the existing synthetic reader tests from this repository root: `python -B -m unittest discover -s scripts/tests`.

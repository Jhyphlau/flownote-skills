# FLOWnote candidate validation (2026-09-28)

This is evidence for the local public candidate at `72b7d19` plus the README clarification in this stage. It is not a publication approval or a compatibility certification. The journey used one temporary synthetic Vault outside this repository. No real Vault or real session log was read.

## Structure and installation

- Copied the 19 `skills/flownote*` directories into a fresh Vault's `.flownote/skills/`, and the three `scripts/*_session_day.py` readers into its `scripts/`. SHA-256 comparison found 96/96 candidate skill files identical after copying. No junction or author installation was used.
- Checked all 19 `SKILL.md` entry frontmatters for `name` and `description`: 19 present, 0 missing. Checked 95 concrete entry-local `references/` and `assets/` mentions and 7 sibling-skill file mentions: 0 unresolved. This check excludes placeholders and does not prove every conditional runtime path.
- Initialized with one pre-existing domain page, one theme page, and two unrelated owner files. A simulated user confirmed reuse of the existing domain and theme. The four existing files kept their original SHA-256 hashes. The initializer created `HOME.md`, `04-创造层/项目/📍 项目总览.md`, `Meta/.ai-memory/STATUS.md`, `Meta/索引/kb-manifest.md`, and the documented directory structure. It did not migrate the Inbox or project-library files.

## Tests

From the repository root, `python -B -m unittest discover -s scripts/tests` returned exit 0: 31 tests, `OK`. `git diff --check` returned exit 0. These tests cover the three synthetic session readers; they do not test host routing.

## Synthetic Vault journey

The fixture article was a short, explicitly synthetic six-person reminder study. The session source was one synthetic Codex-shaped JSONL file. The inputs and observed file changes were:

| Input / simulated choice | Observed result | File evidence |
|---|---|---|
| “The synthetic research summary draft is complete but not accepted; I think reminders may reduce return-to-task cost, without proving the mechanism.” A system clock reading of 2026-09-28 02:22 Asia/Shanghai supplied the capture time. | The completion fact went to `## 任务进展`; the thought went to `## 记录` with `- 02:22`. The existing unchecked task and older entry remained. `STATUS.md` did not change. | Daily note changed from one existing record to one progress line plus two records; STATUS SHA-256 stayed the same. |
| A separate record request with no accessible trusted clock or verifiable supplied time. | Under the capture rule, the agent held a draft and did not write a record. This was a simulated unavailable-time condition; no OS clock failure was induced. | Daily note SHA-256 remained `AB172294…9EC829F` across this branch. |
| “Explain this supplied study; do not save.” | Prepared an explanation draft in this explicit simulation: four of six toy pairs improved, two did not; the proposed goal-reconstruction mechanism remains untested. No Vault write. A simple concept question about “task resumption” was handled directly without Feynman practice. | Before explicit save, no literature note and no `reading/` progress file; non-skill Vault file count 11. |
| Simulated explicit confirmation: save the structured analysis as `《提醒卡与任务恢复》.md`, retaining the limited central judgment. | `flownote-read` saved one literature note and reread it. The article branch did not create reading progress or update STATUS. | `02-培养层/文献笔记/《提醒卡与任务恢复》.md` exists; SHA-256 `B3D948CC…8F98FEE`. |
| Review only the named synthetic session and show a draft. | The reader returned four visible messages from one session for the UTC+8 day, with `errors=[]` and `coverage_complete=true` for that one source. The review draft treated the summary as a completed draft and formal acceptance as unverified. | No review write; daily note and STATUS hashes unchanged. |
| Distill preview, then simulated explicit save of only that discussion. | Preview retained user and Agent turns in order with the unresolved mechanism and acceptance boundary. Preview wrote nothing. Save created a separate conversation file; review did not save a transcript. | Before save, non-skill Vault file count 13 and destination absent. After save, count 14; `01-捕获层/对话存档/提醒卡讨论.md` exists with SHA-256 `2E1028F8…D30065D0C6`. Daily note and STATUS unchanged. |

The synthetic session pointer was initially absent. The candidate's review/distill rules require asking for the relevant source instead of guessing a machine log root. A fixture-only pointer was then installed, limiting the authorized source to one local JSONL file. The reader was run with that explicit `--root` and `--date`; it emitted four messages at 01:10, 01:12, 01:30, and 01:35 Asia/Shanghai. No other sessions were read. `obsidian-cli` was not found on PATH, so ordinary Vault files were accessed through the authorized filesystem path and hidden memory files through the filesystem as required. No external tool was installed.

## Runtime discovery and limits

In a separate isolated Claude Code 2.1.283 session, a thin project entry under `.claude/skills/flownote/SKILL.md` pointed to the candidate copy at `.flownote/skills/flownote/SKILL.md`. Host `commands_changed`, `init.skills`, and `slash_commands` contained `flownote`; the process exited 0 using explicit `gpt-6-sol` at medium effort with no tools or MCP servers offered. This verifies fresh host discovery of that entry only. The host session did not load the canonical body, route a knowledge request, or execute the Vault journey. The journey above was explicit candidate-instruction simulation with actual file operations. Other hosts were not tested.

## Final acceptance and delivery

The final read-only CC / `opencode-go/glm-5.3` privacy review covered 114 candidate files and five differing historical file versions. It reported no credentials or private note/session content and conditionally accepted the candidate pending two concrete project-name examples. Those examples were replaced with generic placeholders; a targeted scan of all candidate files found zero remaining matches. This correction was verified locally, not by a second model review. The pre-correction candidate is retained only as `local-candidate-before-privacy-fix`; the rebuilt `public-candidate` has no parent commits and includes the MIT decision and corrected examples. Neither local history branch is a publication target.

An independent GPT-6-Sol Medium review of the complete candidate and the final journey changes passed specification and quality review. No blocking finding remains in the current files. The final controller rerun passed all 31 reader tests. Evidence limits above remain unchanged: host discovery is not automatic workflow-routing acceptance.

Local history inspection found an older candidate commit with four files containing now-removed machine-specific project conventions. With explicit user approval, delivery uses a new root-history `public-candidate` branch containing the accepted file tree; `prepare-public-candidate` retains development history locally and must not be included in a public push. Existing history is not deleted or rewritten. The user selected MIT for local additions on 2026-09-28; the root LICENSE and upstream notices record that decision. The first public remote/push remains outside this completed local preparation. The installed fixtures and raw session output stay outside the public repository.

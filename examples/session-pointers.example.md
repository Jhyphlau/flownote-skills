# Session pointers for this Vault

Copy this example to `<Vault>/.flownote/session-pointers.md` only if session review or distillation is wanted. Fill the fields after checking the current machine's actual client settings or an explicit session location supplied by the user. A blank field means that source is unavailable; ask about the relevant source instead of guessing a path or scanning the machine.

| Source | Log root on this machine (absolute, to fill) | Reader in this Vault | Coverage note (to fill) |
|---|---|---|---|
| Codex | `<CODEX_LOG_ROOT>` | `scripts/codex_session_day.py` | `<CLIENT_AND_DATE_RANGE>` |
| Claude Code CLI/Desktop | `<CLAUDE_LOG_ROOT>` | `scripts/claude_session_day.py` | `<CLI_OR_DESKTOP_AND_DATE_RANGE>` |
| Kimi Code CLI/Desktop | `<KIMI_WIRE_ROOT>` | `scripts/kimi_session_day.py` | `<VERIFIED_CLIENT_AND_DATE_RANGE>` |

The reader paths are relative to this Vault root. Each reader requires `--root <verified log root> --date YYYY-MM-DD` and emits visible messages without writing output. `--date` selects the UTC+8 natural day: 00:00 inclusive through the next 00:00 exclusive, by message time. A period requires checking each relevant day. Use `--summary-only` to locate sessions, then read actual messages for conclusions.

The readers defer records explicitly identified as spawned subagents by default; use `--include-subagents` only when the authorized review needs their missing evidence, and avoid counting a delivered result twice. Claude CLI and Desktop records can share a session; check client identity and available session mapping before claiming coverage. Kimi CLI and Desktop can share the same wire root and format; the Kimi reader does not identify client origin, so a shared root alone cannot establish Desktop coverage or attribute a session exclusively to Desktop. Verify client coverage from a separate known source and report uncertainty. Reader output may omit attachments or tool evidence; inspect a specific source only when needed and authorized. Record failures and coverage gaps without treating a configured pointer as permission to read every conversation.

Suggested saved-source convention: `<Vault>/01-捕获层/` for user-approved conversation material. Confirm the actual destination and write scope with the user before saving. Keep this private pointer in the Vault; this repository carries only the blank example.

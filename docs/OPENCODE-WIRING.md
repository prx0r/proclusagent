# OPENCODE-WIRING — plug buttons into THIS opencode without breaking it

Docs checked: `commands/` (markdown files, additive), `mcp-servers` (config block,
local stdio supported), `keybinds` (left alone on purpose). Your config today is
empty (`opencode.jsonc` = `{}`), so there is nothing to conflict with.

## What could break, honestly ranked
| Change | Risk | Why safe / mitigation |
|---|---|---|
| NEW `commands/predict.md` | ~zero | New file, new `/predict` name; touches nothing existing. Delete = rollback. |
| MCP block in opencode.jsonc | low | Additive key; `enabled:false` default until you flip it; MCP adds context tokens (docs warn) so keep our 8 tools minimal; `timeout:5000` bounds hangs; server is local stdio, no network, no secrets. Rollback: delete block, restart opencode. |
| Keybind changes | SKIP | Would alter muscle memory; Tab/arrows stay yours. Revisit only on request. |
| Skills/rules/agents | later | Optional; nothing needed for buttons to work. |

## Exact snippets (NOT applied — approve to apply)
`~/.config/opencode/commands/predict.md`:
```markdown
---
description: Score next-prompt options for the current context
---
Score these candidate next prompts for my context using the local predictor: $ARGUMENTS.
Prefer the project's predictor tools if available.
```
`~/.config/opencode/opencode.jsonc` (additive — keep the `$schema` line):
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "proclus": {
      "type": "local",
      "command": ["python3", "/home/ubuntu/proclusagent/mcp_server.py"],
      "enabled": false,
      "timeout": 5000
    }
  }
}
```
Apply = create 1 file + add 1 block, restart opencode. Rollback = delete both.
Verify after: `/predict ok` suggests; MCP tools appear in tool list when enabled.
Server speaks real MCP now (initialize/tools/list/tools/call tested); legacy
`{id,tool,args}` dialect kept for scripts.

## APPLIED 2026-09-10 (approved this session)
- Backup: `~/.config/opencode/opencode.jsonc.bak-20260910`.
- Created `~/.config/opencode/commands/predict.md` (`/predict`).
- MCP block added, `enabled: true`, timeout 5000. Config parses.
- Live handshake verified exactly as opencode does it: initialize →
  notifications/initialized (silent) → tools/list (8) → predict.suggest +
  predict.log_choice round-trip. opencode binary healthy (v1.18.30).
- Priors are live from day one (WAL-mined FAMILY_PRIORS in scorer.py);
  NO fake history seeded — learning starts on your first real press.
- Rollback (one line): `cp ~/.config/opencode/opencode.jsonc.bak-20260910 ~/.config/opencode/opencode.jsonc && rm ~/.config/opencode/commands/predict.md`.

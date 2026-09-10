# MCP-PLAN — headless access to everything (spec now, build next, $0 local)

Pattern (from seed0 `CG_IMPORTS.md` + `templates/docs/MCP.md`): MCP future = planned
tools table first, then 3-step recipe per tool (entry + handler + stdio round-trip test).
cg rule respected: additive only, never rename live surfaces; least-privilege tool filter.

## Tools table (all read-only except loop-mint, all $0 local)
| Tool | Does | Reads |
|---|---|---|
| `mine.search` | keyword/family filter over INDEX.jsonl | seed0/mine/architectures/INDEX.jsonl |
| `mine.packet_get` | full packet.json + NOTES excerpt | packet dir |
| `kernels.list` | P0-P7/S0/T1/N1/A1 status + gates | docs/KERNELS.md + packets |
| `tournament.baseline` | runs tournament.py seeds/seed1..3, returns tail | seed0 subprocess, 180s cap |
| `loop.status` | A/H/M queue counts | docs/A-QUEUE.jsonl + aloop --status |
| `loop.mint` | propose_next() preview, no run | aloop --evolve |

## Headless tests (no browser, no site needed — repo IS the site)
Each tool gets a stdio JSON-RPC round-trip test: spawn server → `initialize` →
`tools/call` → assert shape + exit 0. Plus a feature script hitting every row above
(packet read, index digest, verify 57/57, baseline tail, queue counts).
Transport: stdio only. No deploy, no network listener (deploy = M2/H5, not this turn).
Secrets: none required; server refuses env starting with sk-/ghp_/cfat_ in outputs.

## Build order (next A-tasks, each $0)
1. `mcp_server.py` stdlib-only (json/rpc over stdio, no SDK dep).
2. `tests/test_mcp_roundtrip.py` (6 calls, all green).
3. `docs/MCP.md` tools table → flip from "planned" to "live".

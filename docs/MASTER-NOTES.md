# MASTER-NOTES — whole session on one page (2026-09-10, updated live)

## Northstars (in priority order)
1. **PATH-TO-AUTONOMY** (`docs/PATH-TO-AUTONOMY.md`): buttons → choice log →
   auto-proceed easy intents at τ → LLM+H-delegate hard ones → handover.
   Gate currently CLOSED by measurement (continue auto-precision unproven).
2. **Northstar tournament chain** (`docs/NORTHSTAR.md`): results→amend x.1→
   branches→re-tournament→a-log match→STOP→A-REPORT→peer review. STOP achieved.
3. **Mini-me predictor**: fastText text→family 0.807 (0.799 unseen); fam-hit@3 0.671;
   linear ctx→family 0.437; exact-template 0.0016 (dead — proves buttons).
4. **NEW: UK L2 data hunt** (`docs/DATA-HUNT.md`): free public sources only;
   gated/commercial flagged H/M, never touched.

## Where everything lives
- proclusagent @ `chain/session-logs-1` (pushed): predictor/, controller/,
  ham_registry.py, aloop.py, mcp_server.py, prompts/corpus.jsonl, docs/ (35+),
  tests/ (76+2skip green), runs/, a-logs/ (80 records).
- seed0 @ `chain/ham-tournament-1` (pushed): mine/architectures (57 packets),
  seeds 1-5 + 6-ham (1.1 amended, tournament green), ideas/idea3, runs/.
- /tmp (quarantine, NOT repo): opencode-sample/ (work.db 6GB, corpora),
  mininet venv (sklearn), replay store. /home/ubuntu/tg (telegraph snapshot).
- Cloned this turn: `/home/ubuntu/gitgoblin` (mission runner for data hunt).

## Hard rules (standing)
H/M need explicit approval. $0/reversible = A. Secrets env-only; raw logs
quarantine-grade (keys inside); scrub() before training; gate 5/5 enforced.
PUSH approved per-branch only when stated. **Rotate the exposed ghp token.**
No bypassing auth/paywalls; gated datasets flagged, never pulled.

## Queues right now
A: loop-driven, STOP yes. H1-H6 + UI placement + main merge + token rotation.
M1-M5: all denied, $0 spent. Next A: family-confidence fix, α-sweep sans kNN,
dialog-state used (falsified), UI spec option C builds on one word.

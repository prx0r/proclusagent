# BUTTONS REPORT — state of the mini-me product (2026-09-10)

Goal: after every agent output, 3 scored buttons flash up. You press one or type
your own. The model predicts your pick; at calibrated reliability it runs
autonomously (Enter becomes heartbeat). Question this answers: how close?

## What the data says (8,497 sends, frozen splits unless noted)
- Top-3 family hit: **0.67** (online) — buttons beat any single guess.
- Post-type router (fastText text→family): **0.81** (0.80 unseen) — once typed, routed.
- Context→family (pre-type): session-prior 0.44, linear 0.44, kNN 0.42, MLP 0.38.
- Continue binary: 0.84 ≈ base rate (16% short-acks; history/dialog-act/joint all
  fail to beat it: 0.195 / 0.166 / 0.193). Auto-send gate CLOSED by measurement.
- Exact-template verbatim: 0.0016 — auto-send-a-string is dead; buttons win 400:1.
- Replay sim (8,497 turns live): NO learning under exact-text scoring (flat curves);
  τ=0.9 never fired (conf saturates ~0.4); ladder promoted on a flat metric
  (slope-gate rule added). Fix queued: family-level confidence (dense counts).

## What's built and green (76+2skip, 5/5)
`predictor/`: store (JSONL choice log + stats + mtime cache), scorer (Laplace +
hierarchical hconf), suggest (top-3 + default=0), autonomy (τ ladder, reports only),
pilot/ensemble/subcluster/mininet/cascade/continue_/dialog/cluster/replay modules,
thresholds.json (0.9/0.5), ack_templates.json (8 real variants).
`controller/`: phases + templates from YOUR phrasing + router + driver
(dry-run default; FunnelBuilder refuses without H4). MCP: predict.suggest/log_choice,
mine.*, loop.*, kernels.* (round-trip tested). Choice-log schema captures
(session, context, shown[3]+confs, picked, typed_own) — future IPS/DR possible.

## Opencode logs status (the fuel)
R2 `opencode-backup`: 17,016 objects, 9.1GB. Core: opencode.db 6.09GB (SQLite:
891 sessions, 99,894 messages, 391,044 parts) pulled to /tmp quarantine + WAL
applied (event table damaged, everything needed clean). Schema recovered from 5MB
prefix. Corpus: 8,497 sends chronological + session titles/models/agents.
Quarantine-grade: keys live in logs — shapes only, scrub() enforced, gate green.

## Blockers (ordered)
1. Family-confidence fix (A-task, queued) — unblocks auto_rate>0 + learning slope.
2. UI surface (HUMAN decision): A) opencode fork, B) desk UI, C) CLI wrapper $0 now.
3. Live choice log → calibrate τ → DPO/IRPO → LoRA (gates, in that order).
4. Rotate the exposed ghp token. Push main branches (H3).

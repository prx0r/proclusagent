# HANDOVER-FRESH — complete brief for a fresh agent (2026-09-10)

## Mission
Build mini-me: a predictor that responds as prx0r would. Path: mine his 8,497 real
prompts → predict next response (buttons + Enter-accept) → log choices → calibrate →
auto-run easy intents → LLM/H-delegate hard ones. NORTHSTAR: autonomous tournament
chain with a-log evidence matching (see `docs/NORTHSTAR.md`).

## Repo map (TWO repos, BOTH on branches — main is behind)
- `/home/ubuntu/proclusagent` @ `chain/session-logs-1` — lead repo: predictor/,
  controller/, ham_registry.py, aloop.py, mcp_server.py, docs/ (30+), tests/.
- `/home/ubuntu/seed0` @ `chain/ham-tournament-1` — harness + `mine/architectures/`
  (57 packets) + seeds incl. seed6-ham + ideas/idea3 + runs/predictor/.
- `/tmp/opencode-sample/` — quarantined R2 data (work.db 6GB, corpus_full.jsonl,
  corpus_clean.jsonl). NEVER copy into repos. `/tmp/mininet` venv (sklearn+numpy2).
  fasttext needs numpy<2 — separate venv if rerun (see DEP-PILOT.md).

## Conventions (binding)
- Every reply ends with H-task / M-task / A-task blocks. H+M need explicit
  `approve Hx` / `approve Mx cap=$`. A = $0, reversible, local-only.
- Every run logs: `runs/sha256_*.json` receipts + `a-logs/SESSION-2026-09-10.jsonl`.
- Secrets env-only, NEVER in tree. `seed0.py check` secret gate must stay 5/5.
  KNOWN EXPOSURE: a live-format ghp token sits in chat history + R2 WAL — ROTATE it.
  Raw logs are quarantine-grade (keys inside); quote shapes only.
- NEVER `git push` without explicit approval (this push was approved 2026-09-10
  for these two branches only). Commits use inline `-c user.name` (no config change).

## State (verified this session)
- Suite: pytest green, `seed0.py check` 5/5, validator 6/6, mine verify 57/57.
- Queues: A 0 open (STOP yes achieved repeatedly), H1-H6 + M1-M5 open in
  `docs/H-QUEUE.jsonl` / `M-QUEUE.jsonl` (machine-readable; `QUEUE.md` is human-readable).
- Key numbers: fastText text→family 0.807 (0.799 unseen); fam-hit@3 0.671;
  hashed-linear ctx→family 0.437; exact-template verbatim 0.0016 (dead — proves
  buttons); continue base rate ~0.84; WASM parity 200/200; tournament ev-tiers hold.
- Open finding (act on this): τ=0.9 NEVER fires — exact-text Laplace confidences
  saturate ~0.4 (calibrated but blunt). Fix = family-level confidence (dense counts).

## INCOMPLETE — resume here
Replay sim chunk 1/2 done (turns 0–4250, hit3 0.639, enter 0.397, auto 0). Run chunk 2:
`python3 /tmp/run_replay.py` (auto-resumes from store line count; ~3 min).
Then: full-run metrics → family-confidence fix → docs/REPLAY-SIM.md.

## Next ordered
1. Chunk 2 + full replay metrics + REPLAY-SIM.md.
2. Family-level confidence (fix τ-unreachability) + re-eval auto_rate>0.
3. Session↔global α-sweep sans kNN (round-3 design in RL-ENV).
4. Sub-cluster `other` beyond topical (40% mass).
5. Buttons UI (needs human: where they render) → live choice log → DPO/LoRA gates.
6. `approve H3` outstanding for main-branch merge; PRIV repos untouched (H2).

## Verify after any change
`python3 -m pytest tests/ -q` · `python3 ../seed0/seed0.py check .` ·
`python3 validate_ham.py` · `python3 aloop.py --status` · secret grep clean.

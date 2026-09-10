# RUN-LOG 2026-09-10 — all-A drain (logged, receipted)

## Steps + evidence
1. `aloop.py --status` → 0 open / 20 done, mine 57 packets / 23 boot-tests. (pre-state)
2. `--until-blocked --max 20 --evolve-loop` → auto-minted A-auto-boot-57-3
   (ochema-film-library, ochema-site, ochema2 stubs) + reindex (digest unchanged
   `bfc0a39f407a9eef` — boot_tests don't alter packet digest, correct).
   Post: 25 done / 0 open. Receipts: `runs/sha256_52435c…`, `sha256_46a241…`.
3. MCP build (uncovered by loop): `mcp_server.py` (6 tools, stdlib stdio) +
   `tests/test_mcp_roundtrip.py` (5 tests). Evidence: `pytest tests/ -q` → 7 passed.
4. K2 drafts (uncovered): `docs/K2-SCAFFOLDS.md` P0-P4 (spec only, no seed dirs, no run).
5. Validation: `seed0.py check .` → 5/5 COMPLIANT; `aloop --status` → 25/0/0/0;
   mine 57 packets. Evidence: command tails above + `runs/` (20+ receipts).

## Cost / manual
$0 total (local compute only, ~40 R2 LISTs earlier today, zero egress on this run).
No manual actions. No H/M executed. Secrets: none touched (grep gate green).

## Second drain (same session)
- A26 boot finish (max 10) → coverage 100%: 57 packets, 31 mine-side boot_tests,
  0 test-less packets without a boot test. A26b verify 57/57 ok.
- A28 K2 collect-only rehearsal (P0-P4 idea, agent-cmd=true) → wiring proven, rc 0.
- A29 docs index refresh (MINI-ME/SAMPLE/EXPERIMENT/K2/RUN-LOG rows added).
- Auto-evolve verify → ok. Final: 30 done / 0 open.
- Validation: `pytest` 7 passed; `seed0.py check` 5/5; mine 57 packets.
- Evidence: `runs/sha256_*` receipts + command tails above.

## Third drain (same session, receipt `runs/sha256_9705a8c8…`)
- Queue: auto-verify only → 31 done / 0 open (verify 57/57 ok).
- A30 prop-02 (receiver/received asymmetry) + prop-03 (prior unifier): JSON blocks
  parsed, required keys + source_sha256 + truth_condition + rival_reading asserted.
- A31 loop→MCP wiring: `h_mcp_selfcheck` in aloop.py calls mcp_server handlers
  in-process; A33 ran green (search 3 hits, arch/cg resolved, P0-P7 ladders).
- A32 AGENTS.md mine count 49→57 (+FILES.md linked line).
- Validation: `pytest` 13 passed; `seed0.py check` 5/5; queue 32/0/0/0.
- Cost $0, no manual, no H/M executed, secret-grep green.

## Fourth drain: predictive loop (receipt below)
- `predictor/` 4 modules + 6 tests; MCP `predict.suggest/log_choice` + round-trip test.
- Validation: `pytest` 20 passed; `seed0.py check` 5/5; queue 32/0/0/0.
- Confidence is online (every log_choice moves posterior, no retrain); Enter=top by contract.
- Cost $0, no manual, no H/M executed, secret-grep green.

## Fifth drain: stack pilot (receipt `runs/sha256_358c9950…`)
- Frontier: Smart Compose (interpolation α=0.4, +6% CTR), LaMP RAG+14.92/PEFT+1.07,
  MTA/OPPU (LoRA needs volume), PGraphRAG (graph-as-retrieval), IRPO (listwise DPO).
- `predictor/pilot.py` + 4 synthetic tests; real WAL run: 2 unique sends, LOO 0.0 all-α.
- Verdict: retrieval+interpolation now; graph = retrieval structure, not a model;
  LoRA gated on ≥500 turns + plateau + H/M.
- Validation: `pytest` 24 passed; `seed0.py check` 5/5; queue 32/0/0/0.

## Sixth drain: ham tournament (this section)
- Spend-lock research: cmail tokens + agentmandate ladder + giwacard no-self-approval
  test + ERC-7715 scoped grants + x402 upto — frontier matches our design; no new
  dependency (pattern-only, stdlib holds).
- `ham_registry.py` + 9 tests (lifecycle, M-lock incl. double-spend/over-cap/scope/
  revoke, unlock graph, browser poll); H/M-QUEUE.jsonl seeded (H1-H6, M1-M5 caps).
- a-logs/ backfilled 32 records from A-QUEUE done items.
- seed6-ham (seed0-shaped, HYPOTHESIS ham-1 + 5 falsifiers): tournament 5/5, suite
  10 passed, rank #6/6 by evidence (honest: rank≠falsified, F3 needs green only).
- Funnel collect-only: first run false (rubric pointed at moved file — harness caught
  rubric-reality mismatch) → fixed rubric → all-true binary_pass.
- `validate_ham.py`: 6/6 checks, exit 0. METAGUIDE + tournament recipe logged.
- Validation: proclusagent `pytest` + `seed0.py check` 5/5 (re-run below at close).
- Cost $0, no manual, no H/M executed (M-queue: zero spent), secret-grep green.

## Seventh drain: a-task loop, 3 cycles to steady state
- New `full_test` handler (pytest + check + mine-schema + validator in one battery;
  raises on any red so failures stay open, never silently green).
- A43 queued + ran: pytest 41 passed, check 5/5, mine 57/57 clean, validator 6/6.
- Cycles 1-3 (`--until-blocked --max 12 --evolve-loop`): cycle 1 ran A43 + auto-verify;
  cycles 2-3 clean bottlenecks, evolve minted nothing — steady state 34/0/6/5.
- a-logs 37 records. Cost $0, no manual, no H/M executed, secret-grep green.

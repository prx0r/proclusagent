# AUDIT — full repo audit vs seed0-checker + cg pattern (2026-09-10)

## seed0.py check (before fixes): 3/5 NOT COMPLIANT
- FAIL required-files: missing `AGENTS.md`, `.env.example`, `docs/README.md`,
  `docs/RECIPES.md`, `docs/FILES.md`, `docs/THREADS.md`
- FAIL tests-exist: 0 test files
- PASS env-committed / no-committed-secrets / index-links-live

## cg-pattern gaps (AGENTS.md/GUIDE.md doctrine)
1. No push rule, no kernel/purity boundary (repo is docs+schemas only — boundary is
   "no code dumps", stated in MINE-SPEC, now restated in AGENTS.md).
2. No ops loop doc (cg has registry→runner→receipt→gates→evo; ours is
   queue→aloop→receipt→mint→bottleneck — now in LOOP.md + docs/README).
3. Receipts exist (`runs/`) but no `runs.py` verifier — documented as seed0-idiom
   receipts; verify = recompute sha256 over content (LOOP.md).
4. No secret-scan rule — added (cmail shared rule: grep cfat_|ghp_|sk- before push).
5. New-agent confusion ranked: (a) 14 docs, no index → fixed by docs/README.md;
   (b) two queues (QUEUE.md human + A-QUEUE.jsonl machine) → explained in README;
   (c) mine lives in seed0, not here → stated + symlinked by path convention;
   (d) no tests → fixed by tests/test_boot.py.

## Fixes applied this turn (additive only, zero rewrites, zero moves)
AGENTS.md, .env.example, docs/README.md, docs/RECIPES.md, docs/FILES.md,
docs/THREADS.md, tests/test_boot.py, stale/ manifests (see below).
Re-run `python3 ../seed0/seed0.py check .` after — expect 5/5 (fixtures: none, no secrets).

## Remaining (needs approval, not done)
- H3 commit (all files still untracked) — human pushes.
- Live-link drift: INDEX links seed0 paths; re-check after any seed0 move.
- No CI gate wired (no .github/workflows) — propose, don't assume.

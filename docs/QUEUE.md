# QUEUE — H / M / A tasks (binding convention, 2026-09-10)

Every response from lead agent ends with these three blocks.
- **A-task (agent):** autonomous, reversible, zero-spend. Runs without asking.
- **H-task (human):** needs explicit human approval. Never auto-runs. Expiry re-escalates.
- **M-task (money):** needs explicit spend approval (amount + cap + rollback).
  Never auto-spends. Even $0.01 needs a yes.

## A-queue (machine truth: docs/A-QUEUE.jsonl — 20 done / 0 open)
- [x] A1-A8 T0/T1/lineage/baseline/LINEAGE-MAP — done
- [x] A9 T2 sweep 8/8 (x402/x4022/x402fun/voiceagent/llmdeals/redirect/agentseo/domainnamechecker) — done
- [x] A10+AUTO boot-tests (23 mine-side stubs, incl. organism/truth-engine/library) — done
- [x] A12 tournament baseline + funnel_collect K1 wiring — done
- [x] A13 donor sweep 8/8 (qdw-forge/cge1/fleet-artifacts/MinimaMCP/evolabz/Alethiea/Aletheia/Iolaus) + verify 57/57 + INDEX digest bfc0a39f407a9eef — done
- [ ] A14 K2 promotion scaffolds (P0-P4 local-only draft seeds, no funnel agent yet) — next, $0 (needs H4 to run funnel)
- [x] A15 seed0 pulled bed8432 ff-only, mine intact — done
- [x] A16 MINI-ME plan + achieved/missing zoom-out (no pull) — done
- [x] A17 MCP-PLAN headless tools spec (cg 3-step) — done
- [x] A18 AUDIT 3/5→5/5 (AGENTS/.env/docs-README/RECIPES/FILES/THREADS/test_boot) — done
- [x] A19 CMAIL-THESIS (till, not lab) — done
- [x] A20 stale/ manifests x4, zero moves/breaks — done
- [x] A34-A36 second drain (verify/index/docs-refresh) — done, 32/0/0/0
- [x] A37 predictor/ (store/scorer/suggest/autonomy) + MCP predict.* + 7 new tests — done, 20 passed
- [x] A38 pilot.py (parse→cluster→α-sweep LOO) + 4 tests + STACK-DECISION — done, 24 passed
- [x] A39 ham_registry.py + 9 tests + H/M-QUEUE.jsonl + a-logs/32 + seed6-ham + HYPOTHESIS + criteria/ham.json + validate_ham.py + METAGUIDE — done, tournament + funnel + validator green
- [x] A40-A42 prompt library: corpus 21 specimens + cluster.py (10 categories, compounds) + PROMPT-LIBRARY.md copy-paste — done, 41 passed, a-logs 35
- [x] A43-A44 loop steady-state: full_test handler + 3 evolve cycles to bottleneck — done, battery all-green, 34/0/6/5, a-logs 37
- [x] A45-A54 northstar chain + A55-A59 full-data RL env (6GB pull, 8,497 sends, kNN-vs-baselines eval) — done, 50 passed, a-logs 59
- [x] A60-A62 round 2 (subcluster other + ensemble split + idea3 funnel/learn loop) — done, 55 passed, F1 falsified, 2 criteria proposals (human promotes), a-logs 62
- [x] A63-A64 mininet classifier + cascade router (MLP64/128 lose to global; exact 0.0016 proves buttons) — done, 55+1skip, a-logs 64
- [x] A65-A67 tg review + linear wins (0.4373/0.4283) + wasm parity 200/200 (genome=artifact, compile gated) — done, 55+2skip, a-logs 67
- [x] A68-A70 full battery + real fastText (0.807/0.799 unseen, ftz 8MB) + prebuilt wasm path + CRED incident triple-fix — done, 55+2skip, 5/5, a-logs 69
- [x] A70-A71 clone+test all 144 (sparse, keyless, deleted) — done, 2 green + 1 real-failure set, results scrubbed clean, a-logs 71
- [x] A72-A74 clean re-eval + dep pilot + cascade serve + PATH-TO-AUTONOMY (parallel-stream proven) — done, 61+2skip, 5/5, a-logs 75
- [x] A72-A73 clean-corpus re-eval (numbers hold) + dep-install pilot (tf 4/2, cge1 6, csec 3) + DEP-PILOT.md — done, 55+2skip, 5/5, a-logs 74
- [x] A45-A54 northstar chain: analyze→amend 1.1→re-tournament→report→STOP yes (52/52, 0 flags) + id-uniqueness guard + auto-a-logging + local branch commits (NO PUSH) — done

## H-queue (NEEDS explicit `approve Hxx` — demo responses inline below)
- [ ] H1 approve deep-dive into giants (>200MB: Ochema, knowledge-base-organism,
  blogengine, tantraloka-study, patala PRIV) — sparse metadata-only so far
- [ ] H2 approve handling of 11 PRIV repos (local-only packets, never publish)
- [ ] H3 approve `git commit/push` in proclusagent + seed0 (currently uncommitted)
- [ ] H4 approve first tournament promotion (3 family seeds → seeds/seed6-arch-*)
- [ ] H5 approve publishing ledger browser (proclusagent ROADMAP Phase 3)

Demo H-response shape (what I need back to unblock):
```text
approve H1 scope=metadata-only
# or: approve H2 allow=local-only deny=publish
# or: deny H3 reason="not yet"
```

## M-queue (NEEDS explicit `approve Mxx $cap` — all $0 until approved)
- [ ] M1 live LLM evals (`pyeval.py --model mimo-v2.5`, OpenCode/Go key spend) — cap?
- [ ] M2 embedding/index infra for mine search (R2/D1/Wrangler deploys) — cap?
- [ ] M3 sandbox/compute for full tournament runs (Daytona/E2B/fleet) — cap?
- [ ] M4 domain/registrar buys via domainnamechecker claim kits — cap?

Demo M-response shape:
```text
approve M1 cap=$5 model=mimo-v2.5
# or: deny M2-M4 reason="no spend yet"
```

Cost note: everything in A-queue is $0 + fully reversible (tmp clones deleted,
only local .md/.json writes). Any step that would spend, publish, delete a
remote, or touch PRIV publish-surface is H and/or M by construction.

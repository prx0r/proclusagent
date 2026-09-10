# docs/ — index (new agent starts here)

| Doc | What |
|---|---|
| `../AGENTS.md` | Binding rules |
| `HANDOVER.md` | All work done, session log |
| `SYNTHESIS.md` | Donor mechanisms + executable architecture |
| `KERNELS.md` | P0-P7 vs T1/N1/A1/S0 tournament plan |
| `K2-SCAFFOLDS.md` | K2 P0-P4 draft specs (no run yet) |
| `MINE-SPEC.md` | Mine spec, triage, pipeline |
| `LINEAGE-MAP.md` | Old epistemic vs new agent stack, K1/K2/K3 |
| `MINI-ME.md` | Prompter-clone plan from chat history |
| `SAMPLE-FINDINGS.md` | 6MB R2 sample results (shapes only) |
| `EXPERIMENT-DESIGN.md` | Full mini-me experiment (P1-P4) |
| `MCP-PLAN.md` | Headless tools spec |
| `CMAIL-THESIS.md` | cmail commercial-front thesis |
| `AUDIT.md` | Audit vs checker + cg gaps |
| `LOOP.md` | Recursive A-loop + persistent commands |
| `QUEUE.md` | H/M/A queues (human) + `A-QUEUE.jsonl` (machine) |
| `R2-OPENCODE.md` | R2 9.1GB chat-archive survey |
| `R2-INVENTORY.md` | R2 source-material census |
| `ROADMAP.md` | Ledger → commentary → render phases |
| `RECIPES.md` | Common tasks |
| `FILES.md` | File manifest |
| `THREADS.md` | Decision threads + escalations |
| `RUN-LOG-2026-09-10-ALL-A.md` | All-A drain log |
| `RUN-RECEIPT-T1.md` / `RUN-RECEIPT-LINEAGE.md` | Digests |
| `METAGUIDE.md` | Tournament-testing metaguide (decide→encode→run→learn) |
| `PREDICTIVE-UI.md` | Buttons-that-learn-you plan + implementation status |
| `STACK-DECISION.md` | Retrieval-now / LoRA-gated verdict + pilot numbers |
| `PROMPT-LIBRARY.md` | Copy-paste prompt library (10 mined categories, HAM-mapped) |
| `RL-ENV.md` + `RL-RESULTS.json` | Offline bandit env on 8,497 sends: fam-hit@3 0.671, ensemble verdict |
| `MININET.md` | Classifier + cascade: net loses, exact-match 0.16% proves buttons |
| `PATH-TO-AUTONOMY.md` | THE GOAL: easy-first autonomy, live learning, handover at threshold |
| `TG-REVIEW.md` + `WASM-PLAN.md` | tg scorer-smithy thesis; our classifier as genome (parity 200/200) |
| `NORTHSTAR.md` | The autonomous tournament chain (binding) |
| `A-REPORT.md` | Per-task validation evidence for peer review (STOP: yes) |

Mine (lives in seed0, linked not vendored): `/home/ubuntu/seed0/mine/architectures/`
(57 packets, INDEX.jsonl). Queues: `QUEUE.md` + `A-QUEUE.jsonl`. Loop: `../aloop.py`.
Engine: `../predictor/` (scored options + choice log + autonomy ladder),
served headless via `../mcp_server.py` (`predict.suggest`, `predict.log_choice`).

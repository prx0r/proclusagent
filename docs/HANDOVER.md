# HANDOVER — all notes + work done (2026-09-10, lead-agent session)

## 0. Goals inherited
- **proclusagent**: old structures made agentic — verse ledger (OPEN→claimed→verified),
  dossiers + guardrails (no flattening), truth conditions + rival readings per claim,
  provenance or it didn't happen, secrets in vaults. Roadmap: ledger+dossier → commentary
  engine → render+publish.
- **seed0**: project-shape standard + tournament harness — `seed0.py check`,
  `tournament.py` (compliance+suite+evidence), `funnel.py` (isolated attempts),
  receipts (`runs.py`), gates dominate objectives. Dormitory, not foreman.
- **Endgoal**: huge mine of architectures in `seed0/mine/architectures/` that seed0
  can tournament/funnel as competing kernels. Retain packets, never repos.

## 1. Recon (evidence, raw in /tmp/opencode/)
- `prx0r_repos.json` (144 repos: 133 public + 11 private, ~7.7GB tree, private ~851MB)
- `recon_root.json` (root `ls` for all 144 via API)
- Languages: Python 81, TS 21, None 13, JS 11, HTML 9, Rust 5. AGENTS.md in 43.
  Only seed0 has tournament harness. 39 bare/stub, 27 <50KB, 5 giants >200MB.
- Families: evolution kernels, factories, oracles, kgraphs, comms, protocol, render, infra.
- Private 11 untouched: telegraph-lab/factjudge, calendar, unbundled-platform, dell3,
  research-goblin, chaincraft, 33s, patala, mangy-opendaw, ltsex.
- Giants: Ochema 1481MB/81f, KBO 1418MB/48f, blogengine 976MB/66f,
  tantraloka-study 675MB/34f, the-library 234MB, sanskritree 162MB/71f,
  hxrmxs-truth-engine 145MB/92f, patalacheckpoints 293MB/53f.

## 2. Work done (all $0, all /tmp clones deleted)
- **T1 (25/25)**: cmail, feedify, gg-as, gitgoblin, cg, cge, fleece, qdw, qdw-sandbox,
  BEAR, venturelab, venture-lab, dell, dell2, get-me-money, qdw-workbench, mwgym,
  bitt, StallSpy, mw, unignorant, openpatala-translations, ip-graph,
  patalacheckpoints, blogengine. Script `t1_extract.py`, results `t1_results.json`.
- **Lineage (16/16)**: Ochema, ochema-site, ochema-film-library, tantraloka-study,
  knowledge-base-organism, research-journal, sanskritree, hxrmxs-truth-engine,
  the-library, proofdesk, agentic-infra, repute, arena, arenav2, cogym + ochema2 stub.
  Script `lineage_extract.py`, results `lineage_results.json`.
- **T2 (8/8)**: x402, x4022, x402fun, voiceagent, llmdeals, redirect, agentseo,
  domainnamechecker (via aloop A9).
- **Total: 49 packets** in `seed0/mine/architectures/` (676KB):
  oracle 12, kgraph 10, evolution 6, factory 6, render 5, protocol 4, infra 3,
  comms 2, stub 1. INDEX.jsonl 49 lines, digest `8e339820821e31e9`, verify 49/49 ok.
- **Boot-tests (18, mine-side only)**: StallSpy, cmail, cogym, mwgym, agentic-infra,
  venture-lab, venturelab, agentseo, domainnamechecker, redirect, hxrmxs-truth-engine,
  ip-graph, knowledge-base-organism, openpatala-translations, research-journal,
  tantraloka-study, the-library, unignorant. Turns docs-only old-stack repos into
  tournament-eligible kernels without touching upstream.
- **Baselines ($0)**: `tournament.py seeds/seed1..5` → seed3 (evidence-maximalist) #1,
  all green 5/5. `funnel_collect` K1 wiring proof (agent-cmd=true). seed0 self-check
  3/5 is expected (intentional negative fixtures), not a regression.
- **Loop**: `aloop.py` + `docs/A-QUEUE.jsonl` + `LOOP.md`. Guards block spend/push/
  publish/giant-full-clone/PRIV-publish/keys. Recursion via task `spawns` +
  `propose_next()` (boot-batches, reindex, verify, funnel). 14 A done / 0 open,
  12 receipts in `proclusagent/runs/`. Persistent cmd documented in LOOP.md.

## 3. Docs inventory (this repo, all uncommitted)
- `docs/MINE-SPEC.md` — full spec: triage T0-T4, packet schema, pipeline, tournament plan
- `docs/LINEAGE-MAP.md` — old epistemic vs new agent stack, proto-agent table, K1/K2/K3 plan
- `docs/LOOP.md` — recursive A-loop design + persistent commands
- `docs/QUEUE.md` — H/M/A convention + queues (A 14 done, H1-H5 + M1-M4 open)
- `docs/RUN-RECEIPT-T1.md`, `RUN-RECEIPT-LINEAGE.md` — digests + costs
- `docs/A-QUEUE.jsonl` (machine queue), `docs/A-NOTES.md` (scratch)
- `schemas/arch-packet.json`, `schemas/verse-claim.json`, `aloop.py`, `runs/`
- Seed0 side uncommitted: `mine/architectures/` (49 packets + 18 boot_tests + INDEX),
  `runs/sha256_*.json` x2, `tournament_*.jsonl` x2.

## 4. Queues right now
- A: 0 open / 14 done — loop idles until new state appears or H/M unblocks promotion.
- H: H1 giants full-clone, H2 PRIV local-only, H3 commit/push, H4 promote K1/K2/K3 + real funnel, H5 ledger browser.
- M: M1 live evals, M2 index infra, M3 sandbox fleet, M4 domains. $0 spent.

## 5. Key finding (why the lineage matters)
Strongest bridge is `knowledge-base-organism` (canonical build + contract convergence +
coherence/drift audits ≈ seed0 checker + cg gates). Richest compiler is
`hxrmxs-truth-engine` (92 roots, evidence pipeline + truthmaps + dossiers). Minimal kernel
shape is `agentic-infra` (MANIFEST + check.py + agent + pipeline). Proof that old CANONICAL
plugs into new gates is `arena` (`apply_to_cg.sh`). Baseline predicts winners must bring
evidence, not docs (seed3 won) — hence K2 first.

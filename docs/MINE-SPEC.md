# MINE-SPEC — prx0r architecture mine for seed0 tournaments (2026-09-10)

Lead-agent inheritance: this spec binds **both** doctrines.
- From `proclusagent`: provenance-or-didn't-happen, guardrails (no flattening),
  truth-conditions per claim, ledger discipline OPEN→claimed→verified, secrets in vaults.
- From `seed0`: every run logs (receipts), gates dominate objectives,
  binary checks over deterministic verification, mocks prove wiring only,
  substrate-agnostic dormitory (shape + compliance + tournament, no foreman).

Endgoal: a huge, tournament-runnable **mine of architectures** that seed0
(`seed0.py check` + `tournament.py` + `funnel.py`) can mine and experiment with.

Note: `seed0/mine/` today is an **essay mine** (68 texts, ~2.3MB, `mine/README.md`),
plus a verbatim vendored copy of this repo (`mine/proclusagent/` identical except
`.git`). The architecture mine below is new and parallel: `mine/architectures/`.

## 1. Recon summary (evidence, not adjectives)

Source: `GET /user/repos` (144 total) + `GET /repos/{full}/contents/` root scan.
Raw: `/tmp/opencode/prx0r_repos.json`, `/tmp/opencode/recon_root.json`.
Receipt: API-authenticated as `prx0r` (133 public + 11 private).

- **Scale:** 144 repos. Total working-tree ~7.7GB (private ~851MB). Full-clone-all
  fits on this box (82GB free) but is dumb — 5 repos are >200MB each.
- **Languages:** Python 81, TypeScript 21, None/empty 13, JavaScript 11, HTML 9,
  Rust 5, Makefile 1, Astro 1, TeX 1, C++ 1.
- **Agentic maturity:** 43 repos carry `AGENTS.md`. Only `seed0` carries
  `seed0.py`/`tournament.py` — the standard has not propagated.
- **Packaging:** `pyproject.toml` 36, `package.json` 31, `Dockerfile` 14,
  `docker-compose.yml` 11, `Cargo.toml` 7, `.opencode` 2.
- **Shape:** 39 bare/stub repos (≤4 root entries or 404/empty). 27 small <50KB
  (includes `proclusagent` itself — new, plus `fish`, `csec`, `x402`, `dropcomp`,
  `neverbrokeagain-*` stubs, `bookscraper`). 20 giants dominate bytes.
- **Giants (>100MB):** `Ochema` 1.5GB TeX, `knowledge-base-organism`,
  `blogengine`, `tantraloka-study`, `telegraph-factjudge` Rust PRIV,
  `ochema2`, `patalacheckpoints`, `patala` PRIV, `the-library`, `sanskritree`,
  `hxrmxs-truth-engine`, `llmdeals`, `robobladez`, `freaktown`, `redirect` Rust.
- **Private 11 (handle with care):** `telegraph-lab`, `telegraph-factjudge`,
  `calendar`, `unbundled-platform`, `dell3`, `research-goblin`, `chaincraft`,
  `33s`, `patala`, `mangy-opendaw` (C++), `ltsex`.
- **Already on disk** (`/home/ubuntu`): BEAR, bneck, bneck2, breadup, freaktown,
  killfeed, pogtown, stockify, x402, x4022, mimichart, stale, proclusagent, seed0.

### Architecture families (mine axes)

1. **Evolution kernels** — `cg`/`cge`/`cogym` (+`cge1`), `mwgym`, `arena`/`arenav2`,
   `fleet-artifacts`. Pattern: content-addressed RunReceipts, quality gates as hard
   constraints, worldpacks, lexicographic selection. Closest to seed0 receipts.
2. **Factory builders** — `venturelab`/`venture-lab`, `builda`/`builda-v2`,
   `finalbuilds*`, `qdw`/`qdw-forge`/`qdw-sandbox`/`qdw-workbench`,
   `unbundled`/`unbundled-platform` PRIV. Pattern: idea→research→evaluate→report,
   isolated attempts, deterministic scoring. Direct tournament fodder.
3. **Intelligence oracles** — `gitgoblin`/`gg-as`, `feedify`, `dell`/`dell2`/
   `dell3` PRIV/`dell-dev`, `llmdeals`, `fleece`, `repute`, `get-me-money`,
   `dropcomp`/`dropintel`/`drop`, `imbroke`, `bitt`/`tao-trading`, `BEAR`,
   `hackathonhelp`, `moltwork-oracle`. Pattern: collectors→SQLite WAL→deterministic
   scoring→opportunity export. LLM enriches, never overrides.
4. **Knowledge graphs** — `openpatala`/`patala` PRIV/`patalacheckpoints`/
   `patala-org`, `ip-graph`, `knowledge-base-organism`, `Aletheia`/`Alethiea`,
   `Iolaus`, `nyah`, `agentic-infra`, `research-goblin` PRIV, `unignorant`,
   `sanskritree`, `hxrmxs-*`, `sanskrithelp`/`hindihelp`. Pattern: MANIFEST.json +
   `check.py` validators + `agent/` + `pipeline/` + `contracts/`. Provenance-heavy,
   rhymes with proclusagent ledger.
5. **Comms/business ops** — `cmail` (Worker+D1+R2+MCP + brain kernels/jobs/quotes/
   slots), `tomzoho`, `StallSpy`, `lifeOS`, `onething`, `cancelme`. Pattern: bus +
   brain + desk (one queue), drafts-everywhere + human-confirm-on-send.
6. **Protocol/money** — `x402`/`x4022`/`x402fun`, `mw`/`moltwork-oracle`, `MiniMart`,
   `MinimaMCP`. Pattern: paid endpoints, oracle specs, composite endpoints.
7. **Creative/render** — `freaktown`/`pogtown`/`killella`/`killfeed`, `Ochema` family,
   `blogengine`, `molts-live*`, `audiator`, `voiceagent`, `the-library`,
   `tantraloka-study`, `soundworld-daw` Rust, `mangy-opendaw` C++ PRIV,
   `ltsex` PRIV, `saas-admin-template`. Pattern: essay→storyboard→scene-pack→render
   (skia), TTS/audio corpus. Direct fuel for proclusagent Phase 3.
8. **Infra** — `redirect` Rust, `agentseo` Rust, `dnc`, `domainnamechecker`,
   `domainarena`, `cloudflare-mcp-server`, `telegraph-*` PRIV Rust.

## 2. What "retain anything useful" means

Never retain repos. Retain **packets**. One repo → 0..n architecture packets:

```json
{
  "packet": "e.g. arch/cg--deterministic-evolution-kernel",
  "source_repo": "prx0r/cg",
  "commit_sha": "<pinned>",
  "license": "e.g. MIT / AGPL-patterns-only / proprietary-PRIV",
  "family": "evolution-kernel | factory | oracle | kgraph | comms | protocol | render | infra",
  "pattern": "one-paragraph mechanism",
  "run_shape": "bring-up cmds + gate cmds (pytest/check)",
  "evidence": ["seed0 check output", "pytest tail", "run receipt id"],
  "truth_condition": "what would falsify that this pattern works",
  "rival_reading": "strongest non-agentic alternative, steelmanned",
  "seed0_notes": "compliant? what breaks checker? substrate?",
  "status": "claimed | verified | disputed",
  "verifier": "second agent or human",
  "files_manifest": ["top-level tree + key subdirs, no blobs"]
}
```

Packet rules (inherited):
- `commit_sha` pinned — provenance or it didn't happen.
- AGPL patterns-only, never pasted. MIT/Apache vendored with attribution.
  PRIV packets stay local, never published (ledger browser shows metadata only).
- Each packet gets a truth_condition + rival_reading (proclusagent schema habit).
- Ledger discipline: OPEN→claimed(one agent)→verified(second agent/human).
  Never two writers on one packet.
- Every extraction logs a seed0-style receipt (`runs/` via `runs.py` idiom):
  same inputs ⇒ same id; verify fails ⇒ stop.

Target layout (in seed0, not here):

```
seed0/mine/architectures/
  INDEX.jsonl            # one line per packet (queryable)
  evolution/cg--.../packet.json + NOTES.md + tree.txt
  factory/venturelab--.../
  oracle/gitgoblin--.../
  ...
seed0/seeds/seed6-arch-*  # promoted winners as tournament seeds
```

This repo (`proclusagent`) keeps only: this spec + `schemas/arch-packet.json`
(future) + ledger of which verses/dossiers the mine patterns unblock. No code dumps.

## 3. Smart pipeline — clone → extract → delete (never hoard clones)

Why not full-clone-all: 7.7GB + git overhead + 5 giants + 11 PRIV + 39 stubs =
wasted disk/time and buried signal. Instead, batched shallow loop:

```
for batch in T1..T4 (below):
  for repo in batch (max 3 concurrent, 82GB guard):
    git clone --depth 1 --filter=blob:none --sparse <repo> /tmp/mine/<name>
    git sparse-checkout set --no-cone README.md AGENTS.md SPEC.md ARCHITECTURE.md
        pyproject.toml package.json Cargo.toml Makefile schemas/ docs/ tests/ agent/ pipeline/
    extract: root tree + README/AGENTS/SPEC first 2k chars + test presence +
             seed0.py check (if python) + pytest -q --collect-only (no run yet)
    write packet.json (status=claimed) + NOTES.md
    rm -rf /tmp/mine/<name>          # delete immediately
  verify batch (second agent re-reads packets, spot-reclones 10%)
  mark verified, append INDEX.jsonl, emit receipt
```

Cost controls:
- `--filter=blob:none` + sparse keeps each checkout to KBs except giants.
- Giants (`Ochema`, `knowledge-base-organism`, `blogengine`, `tantraloka-study`,
  `ochema2`, `patalacheckpoints`, `patala` PRIV): metadata-only (root tree via API
  already have) + targeted single-file fetch, never full clone.
- Stubs (39 bare): API record only, zero clones. List0518 in recon.
- PRIV 11: local-only packets, no publish, secrets-via-env audit first
  (`seed0.py` secret regexes). `calendar`, `dell3`, `chaincraft`, `33s`,
  `research-goblin`, `telegraph-*`, `patala`, `mangy-opendaw`, `ltsex`.
- Rate: API root scan already cost ~144 calls; per-repo sparse clone is git protocol,
  not API-limited. Keep 3-way concurrency, 600s timeout per repo (seed0 funnel idiom).

### Triage (execution order)

- **T0 — done:** inventory + root scan (this spec). No more API census needed.
- **T1 — agentic + tournament-ready (25 repos, highest yield):** all `AGENTS.md` +
  (`pyproject.toml`|`package.json`) + `tests/` present. e.g. `cmail`, `feedify`,
  `gg-as`, `gitgoblin`, `cg`, `cge`, `fleece`, `qdw`, `qdw-sandbox`, `BEAR`,
  `venturelab`, `venture-lab`, `dell`, `dell2`, `get-me-money`, `qdw-workbench`,
  `mwgym`, `bitt`, `StallSpy`, `mw`, `unignorant`, `openpatala-translations`,
  `ip-graph`, `patalacheckpoints`, `blogengine`. Expect 1–3 packets each.
- **T2 — protocol/render/infra (20 repos):** `x402*`, `arena*`, `moltwork-oracle`,
  `voiceagent`, `freaktown`, `breadup`, `llmdeals` (Rust+MCP), `redirect`,
  `agentseo`, `domainnamechecker`, `cloudflare-mcp-server`, `lifeOS`, `onething`,
  `cancelme`, `Iolaus`, `Alethiea`, `nyah`, `agentic-infra`, `aisec`.
- **T3 — giants + PRIV (16 repos):** metadata-only first, human approves any deep
  dive (HUMAN_LOOP class 1: costly/irreversible). `Ochema`, `knowledge-base-organism`,
  `tantraloka-study`, `ochema2`, `patala` PRIV, `the-library`, `sanskritree`,
  `hxrmxs-truth-engine`, `robobladez`, + 11 PRIV list above.
- **T4 — stubs (39 bare + 27 small):** no clone. One-line INDEX entries
  (`stub`, reason, root-file list from recon). Revisit only if tournament needs filler.

Already-on-disk (`BEAR`, `freaktown`, `breadup`, `x402`, `x4022`, `killfeed`,
`pogtown`, `stockify`): extract without re-cloning, then leave (do not delete user dirs).

## 4. Tournament integration (how seed0 experiments)

1. Promote: best packet per family → `seeds/seed6-arch-<family>` (seed0-shaped:
   AGENTS.md laws + README + docs set + boot test + `.env.example`).
2. Bake-off: `python3 tournament.py seeds/seed*` (mechanical: compliance + suite +
   evidence). Then `funnel.py run --idea "<family task>" --seeds <candidates>
   --agent-cmd ./agent.sh` in isolated fresh dirs — the seed must carry the idea alone.
3. Learn: `learn.py` proposes `criteria1.1` from shared failures; packets that
   repeatedly fail gates get `disputed` status + hypothesis/change/verdict review record.
4. Feed back: winners harden `templates/` + checker rules (seed0 THESIS compounding);
   render-family winners feed proclusagent Phase 3 (scene-pack generator, audio voices).

First three bake-offs (concrete):
- **Evolution:** `cg` kernel vs `mwgym` vs `arena` — task: replayable run with
  content-addressed receipt.
- **Factory:** `venturelab` vs `builda-v2` vs `qdw-sandbox` — task: idea→brief with
  evidence log, `seed0.py check` green.
- **Oracle:** `gitgoblin` vs `feedify` vs `dell2` — task: emit one scored
  opportunity with source URLs + hashes, no LLM required.

## 5. Safety / non-builds (binding)

- Secrets via env only; `seed0.py check` secret regexes gate every packet.
  The ghp token for this session lives in env, never in tree (house rule shared
  with `prx0r/cmail` AGENTS.md).
- No fleet controller, no sandbox infra, no governance layer, no new agent
  framework (seed0 ECOSYSTEM non-builds stand).
- No flattening: architecture analogies stay structural (proclusagent guardrail
  habit applied to code: e.g. ledger≠blockchain, convergence≠truth).
- Checkpoints, not check-ins: T1-complete → T2-complete → first tournament →
  first promotion. Four human touches max before re-plan.

## 6. Next actions (when authorized)

- [ ] Add `schemas/arch-packet.json` (packet schema above as JSON-Schema).
- [ ] Run T1 batch (25 shallow clones, ~1h, receipts in `runs/`).
- [ ] Write `seed0/mine/architectures/INDEX.jsonl` + first 25–75 packets.
- [ ] Promote 3 family seeds, run first `tournament.py`, report leaderboard + receipt ids.
- [ ] Proclusagent ledger tie-in: map render-family packets to scene-pack generator
  inputs (ROADMAP Phase 3).

(End of spec.)

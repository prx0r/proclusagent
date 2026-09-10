# LINEAGE-MAP — old epistemic stack as competing agent kernels (2026-09-10)

Your read is confirmed by inventory: there IS an older epistemic/reality stack
under the newer agent stack. 41 packets now in `seed0/mine/architectures/`
(25 T1 + 16 lineage). All clones deleted; 340KB→~700KB retained.

## 1. The two stacks

**Old stack (metaphysical/epistemic, 2026-08-19 era, docs-heavy, gates rare):**
`Ochema` (81 roots, AGENTS.md, MANIFEST, magnum-opus/manual/film-theory),
`ochema2` (stub pointer), `ochema-site` (Next.js site), `ochema-film-library`
(skiapipeline + works), `tantraloka-study` (extract_verses/chapters/metadata +
TTS), `blogengine` (essay→weave engine, AGENTS.md, tests), `knowledge-base-organism`
(48 roots: CANONICAL-HERMES-BUILD, CONTRACT-CONVERGENCE, COHERENCE/DRIFT audits,
BUILT-BY-LAYER), `research-journal` (daily metaphysics logs, no gate),
`patalacheckpoints` (SPINE + DIRECTORY-MANIFEST + SCHEMA-AUDIT, tests),
`sanskritree` (PIPELINE + FORMALISATION_SCHEMA + provenance-aware src, tests),
`hxrmxs-truth-engine` (92 roots: EVIDENCE-PIPELINE, CODEX-TRUTHMAP*,
COMPOSITION-THESIS, dossiers), `the-library` (content-graph.json + control/).

**New stack (agent/factory, 2026-08-28→09-10, gates-first):**
`seed0` (checker + tournament + funnel + receipts), `cg`/`cge`/`cogym`
(content-addressed RunReceipts, quality gates), `arena`/`arenav2`
(402Arena→capability engine, CANONICAL + contracts, `apply_to_cg.sh`),
`mwgym` (experiment reports, CG-WORLD-TYPES), `repute` (NORTHSTAR* + oracle/),
`proofdesk` (benchmarks + fixtures + demo_2min), `agentic-infra`
(MANIFEST.json + check.py + agent/ + pipeline/ + skills/).

## 2. Proto-agent assessment (is old code actually kernel-shaped?)

| Old repo | Proto pattern | Verdict |
|---|---|---|
| knowledge-base-organism | Verified Epistemic OS: canonical build + contract convergence + coherence/drift audits + built-by-layer | STRONGEST bridge. Audit habit ≈ seed0 checker + cg gates. No tests/ dir → needs boot test. |
| hxrmxs-truth-engine | Evidence pipeline + truthmap + dossiers + composition thesis (92 files) | Richest ontology compiler. No tests/ → wrap one truthmap as binary check. |
| patalacheckpoints | SPINE + directory-manifest + schema-audit + VISION_AND_NAVIGATION | Checkpoint frontier. Has tests → tournament-ready now. |
| sanskritree | Provenance-aware pipeline + formalisation schema + activation gates | Immutable-evidence candidate. Has tests → runnable. |
| the-library | content-graph.json + control/ + DRAFT-ROOM | Ontology compiler (graph). No tests → needs boot test. |
| Ochema | MANIFEST + agent/ refs + magnum-opus/manual/practice-layer | Dossier/guardrail source for proclusagent, not a kernel. Render fuel. |
| ochema-film-library | skiapipeline.md + works/ + library/ | Scene pipeline pattern → proclusagent Phase 3. |
| tantraloka-study | extract_verses/chapters/metadata.py + essays/ + TTS format | Verse-ledger factory (6,903 units). Needs gate wrapper. |
| blogengine | Essay weave engine + AGENTS.md + tests | Research-loop runner. Tournament-ready. |
| research-journal | Daily logs (day1..day4, chakra, metaphysics) | Corpus only. No kernel. Keep as rival (essay, not evidence). |
| ochema2 | 1-file README | Pointer stub. Keep as stub packet. |

Bridges (already kernel-shaped, carry old→new):
`agentic-infra` (MANIFEST + check.py + agent + pipeline + skills — the minimal
kernel shape every old repo should be wrapped into), `arena` (contracts +
CANONICAL + TEST_RESULTS + apply_to_cg.sh — proves old CANONICAL can plug into
cg), `cogym` (canonical/ + evolution_lab/ + EXPERIMENTS — deterministic lab
habit), `proofdesk` (benchmarks + fixtures — verification habit), `repute`
(oracle/ + NORTHSTAR hierarchy — paid-reveal market shape).

## 3. Competing-kernels test plan (no new infra, seed0 harness only)

Baseline (done, $0): `tournament.py seeds/seed1..5` → seed3 #1, all 5 green 5/5
compliant, receipt `runs/sha256_606f07dd....json`. seed3 (evidence-maximalist)
leads — predicts old-stack winners must also bring evidence, not docs.

Three bake-offs (each: `funnel.py run --idea <task> --seeds <a,b,c> --agent-cmd true`
collect-only first, then real agent only after H4):

- **K1 ontology compilers:** `the-library` (content-graph) vs `hxrmxs-truth-engine`
  (truthmap) vs `agentic-infra` (MANIFEST+check). Task: ingest 5 verses → emit
  typed objects + edges + one falsifiable claim. Gate: `check.py`-style binary
  validator + `seed0.py check` shape.
- **K2 checkpoint/evidence:** `patalacheckpoints` (SPINE) vs `sanskritree`
  (provenance pipeline) vs `knowledge-base-organism` (contract convergence).
  Task: checkpoint a claim with hash + manifest + audit line. Gate: re-verify
  from manifest alone (immutable-evidence test).
- **K3 research loops:** `blogengine` (weave) vs `tantraloka-study` (extract) vs
  `cogym` (evolution_lab). Task: verse → commentary → scene stub with citations.
  Gate: pytest green + citations resolve + no-flattening guardrail
  (proclusagent rule 2).

Each kernel gets truth_condition + rival_reading in its packet (done). Promotion
rule: only kernels with `tests_present=true` or a new boot test enter
`seeds/seed6-arch-*`. Theoretically 41 packets → ~18 tournament-eligible today
(15 T1 with tests + arena/proofdesk/repute/sanskritree/cogym already counted;
the-library/Ochema/truth-engine/organism need boot tests first).

Proclusagent tie-in: winners of K3 feed ROADMAP Phase 3 (scene-pack generator);
winners of K1 feed dossier template (`schemas/`); winners of K2 feed ledger
discipline (OPEN→claimed→verified with hashes).

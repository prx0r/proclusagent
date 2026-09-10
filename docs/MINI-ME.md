# MINI-ME — clone the prompter, not the person (plan, no 6GB pull yet)

No chat bytes pulled this turn (needs H6/M5: 6.09GB db + egress + disk).
Design below runs fully on ListObjects metadata + local 63MB opencode state.
Local find: no `opencode.db` on this box (only R2) — pull is unavoidable for real clusters.

## Approach (when approved)
1. **Pull once, query many**: range-GET `opencode.db` + WAL to local SSD (~10GB free needed),
   open read-only SQLite, `.tables`/`.schema` first. Never mutate. Secrets audit before any share.
2. **Extract prompts**: user-message table → (text, ts, session/project, files-touched-next, tool-calls-next).
3. **Cluster variants**: normalize (lowercase, strip paths/ids) → exact dedupe → near-dedupe
   (edit-distance/Jaccard first, embeddings only if M1 approved) → top-N prompt families.
4. **Label when/why**: join each prompt to what followed (scaffold? build-loop? verify-gate?
   escalate? new-seed? recon?) → P(prompt_family | phase) + success proxy (tests-green next?).
5. **State machine (harness, not chatbot)**: states = scaffold / build / verify / escalate /
   tournament, transitions on gate outputs (`seed0.py check`, pytest, funnel scores).
   Each state = prompt template with slots (goal, constraints, evidence-required).
   This is seed0 HUMAN_LOOP mechanized: the machine prompts models to build code,
   models never prompt the human except via task records.

## v0 BUILT (this session, receipt `runs/sha256_ac8b1c46….json`)
`controller/` (stdlib only): `phases.py` (6 phases + pure transitions),
`templates.py` (variants seeded from the 3 observed families above),
`router.py` (first-word classify + deterministic variant pick),
`driver.py` (DryRunBuilder default; FunnelBuilder refuses without H4 +
MINIME_ALLOW_REAL=1). Dry-run traverses recon→scaffold→build→verify→tournament.
13 tests green, `seed0.py check` 5/5. Real agent runs await H4; full-chat
clustering awaits H6/M5. Samples stay in `/tmp/opencode-sample/` (never repo).

## Zoom-out: achieved vs missing
- **Achieved**: 57 arch packets (verify 57/57) + 23 boot-tests + recursive aloop
  (20 done/0 open, 17+ receipts) + seed0 pulled to bed8432 + baselines (seed3 wins) +
  SYNTHESIS/KERNELS/LINEAGE/MINE-SPEC/LOOP + R2 survey (9.1GB, db located).
- **Missing**: chat pull + clustering (H6/M5) → prompt families → state-machine prompts;
  P0-P4 seed scaffolds; real funnel runs (H4); commit (H3); MCP build; ledger browser (H5).
  The mine tells us WHAT you built; the chats tell us HOW you drive builders. Mini-me needs both.

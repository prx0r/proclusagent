# AGENTS.md — proclusagent (synthesis repo, not archive)

Binding rules for any coding agent working in this repository.

## Absolute rules

1. **NEVER `git push`.** The owner pushes. Commit locally only when asked.
2. **No code dumps.** This repo keeps spec + schemas + ledgers + receipts.
   The mine lives at `/home/ubuntu/seed0/mine/architectures/` (57 packets, verify 57/57).
   Link it, never vendor it.
3. **Provenance or it didn't happen.** Every claim cites source repo + pinned SHA.
4. **Guardrails from the dossiers.** No flattening (One≠Brahman, procession≠creation,
   ledger≠blockchain, convergence≠truth). Metaphysical terms only with falsifiable
   ops (see SYNTHESIS.md translations).
5. **Ledger discipline.** OPEN → claimed (one agent) → verified (second agent/human).
   Never two writers on one packet/verse.
6. **Gates dominate objectives.** Never trade correctness for speed; mocks prove
   wiring only; LLM judgment only as binary checks above deterministic verification.
7. **Secrets in vaults/env, never in the tree.** Before every push:
   `grep -rIlE "cfat_|ghp_|sk-[A-Za-z0-9]{10,}" --exclude-dir=.git .` must print nothing.
8. **Additive to live surfaces.** Never rename/remove a route, tool, or schema field;
   add alongside. Small diffs, tested each step.
9. **Every run logs.** aloop/MCP/tournament runs emit receipts to `runs/`.
   Cite run_ids, not adjectives.

## Where things are

`docs/README.md` index (start here) · `MINE-SPEC.md` mine spec · `SYNTHESIS.md`
donor mechanisms + architecture · `KERNELS.md` P0-P7 plan · `LINEAGE-MAP.md`
old-vs-new stack · `LOOP.md` recursive A-loop · `QUEUE.md` H/M/A queues +
`A-QUEUE.jsonl` machine queue · `MINI-ME.md` prompter plan · `MCP-PLAN.md` headless
tools · `CMAIL-THESIS.md` commercial front thesis · `AUDIT.md` audit ·
`R2-OPENCODE.md` chat-archive survey · `HANDOVER.md` session log ·
`RUN-RECEIPT-*.md` digests · `schemas/` packet + claim schemas ·
`examples/prop-01.md` worked claim · `aloop.py` loop · `runs/` receipts.

## Working style

- New agent: read `docs/README.md` → `SYNTHESIS.md` → `QUEUE.md`, then `aloop.py --status`.
- Docs: `docs/README.md` index stays accurate (seed0 checker enforces live links).
- Tests: `python3 -m pytest tests/ -q` from repo root. Keep green.

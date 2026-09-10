# RUN-RECEIPT T1 — 25 shallow extracts (2026-09-10)

- digest (packets sha256[:16]): `20685828b8eca074`
- packets: 25 (oracle 9, factory 5, kgraph 4, evolution 3, comms 2, protocol 1, render 1)
- tests_present: 15/25
- method: `git clone --depth 1 --filter=blob:none --sparse` + sparse set
  (README/AGENTS/SPEC/pyproject/package/Cargo/schemas/docs/tests/agent/pipeline)
  → packet.json (status=claimed) → `rm -rf /tmp/mine/<name>`
- clones deleted: all 25 verified deleted (`/tmp/mine` empty after run)
- retained: `seed0/mine/architectures/*/packet.json + NOTES.md + INDEX.jsonl` (340KB)
- cost: $0, no keys used except read-only GH_TOKEN env, no publishes, no deletes remote
- verify: `python3 -c` root-tree count + required-fields check — 25/25 pass
- source: `/tmp/opencode/t1_extract.py`, results `/tmp/opencode/t1_results.json`

Bottleneck: promotion to `seeds/seed6-arch-*` + tournament run needs H4;
PRIV + giants deep-dive needs H1/H2; any live eval needs M1.

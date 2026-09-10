# RUN-RECEIPT LINEAGE — 16 extracts + baseline (2026-09-10)

- digest (41 packets sha256[:16]): `9153a0c1ff235ce8`
- new this batch: Ochema, ochema-site, ochema-film-library, tantraloka-study,
  knowledge-base-organism, research-journal, sanskritree, hxrmxs-truth-engine,
  the-library, proofdesk, agentic-infra, repute, arena, arenav2, cogym + ochema2 stub
- skipped (already had packets): blogengine, patalacheckpoints, cg, mwgym
- method: same sparse blob:none loop (`/tmp/opencode/lineage_extract.py`),
  results `/tmp/opencode/lineage_results.json` — 16/16 OK, all `/tmp/mine` deleted
- retained: `seed0/mine/architectures/` 540KB, INDEX.jsonl 41 lines
- baseline tournament: `tournament.py seeds/seed1..5` → seed3 #1 (4 evidence),
  all green+compliant, receipt `runs/sha256_606f07dd....json`, log `tournament_1789035453.jsonl`
- seed0 self-check note: `seed0.py check .` = 3/5 NOT COMPLIANT — expected, caused
  by intentional negative fixtures (`tests/fixtures/bad/notes.md` sk- leak +
  PRIVATE KEY string inside `seed0.py` regex itself). Not a regression.
- cost: $0, no publishes, no remote deletes, read-only token env-only

# METAGUIDE — how an agent decides what to test, why, and how to keep it scientific

## Why tournaments for methodology (not just code)
A method claim ("registries make autonomy auditable") rots exactly like untested
code: prose asserts, nothing can fail. cg doctrine: gates dominate objectives, LLM
judgment only as binary checks above deterministic verification. seed0 doctrine:
scores rank only among the gated; receipts or it didn't happen. EIL lesson: log
implicit approvals too. So methodology ships as a SEED with HYPOTHESIS + falsifiers
+ criteria + validator, and the tournament/funnel/grader either greens or kills it.

## The loop (decide → encode → run → learn)
```
bottleneck (queue idle, H/M-gated next)
  → HYPOTHESIS (ONE claim + 3-5 falsifiers + metrics + thresholds)
  → criteria JSON (funnel rubric: file_exists / contains / suite_green)
  → validator script (exit 0/1 + JSON report; mirrors falsifiers 1:1)
  → seed dir (compliant shape + mechanism + tests + HYPOTHESIS inside)
  → tournament.py (mechanical: compliance + suite + evidence → rank + receipt)
  → funnel collect-only (agent-cmd=true: proves wiring, $0)
  → real funnel (agent-cmd=real: NEEDS H4 — the seed must carry the idea alone)
  → review/blind/reveal → amend → receipt → a-logs
  → learn.py (shared failures → criteria bump, e.g. criteria1.1)
```
Decide-what-to-test rule: the highest-priority H-blocked cluster with a falsifiable
mechanism already in packets. (This round: H-A-M registry — 32 done A-tasks of
evidence, H4-gated bake-offs waiting.)

## Schemas
- `HYPOTHESIS.md`: Claim / Falsifiers F1..Fn (each names the test or check that fires
  it) / Metrics / Thresholds.
- criteria JSON: `{"checks":[{"id","type":"file_exists|contains|suite_green","path","text"}]}`.
- validator: prints `{"pass":bool,"checks":{...}}`, exit 0 iff all true. Each check maps
  to one falsifier; extra checks allowed (e.g. M_locked_no_spent).
- a-log record: `{ts,actor,action,task,title,receipt}` append-only under `a-logs/`.
- receipt: content-addressed run id (`runs/sha256_*.json`), cited not adjectived.

## Exact commands
```bash
cd /home/ubuntu/seed0
python3 tournament.py seeds/seed1 seeds/seed2 seeds/seed3 seeds/seed4 seeds/seed5 seeds/seed6-ham
python3 funnel.py run --idea "..." --rubric /home/ubuntu/proclusagent/criteria/ham.json --seeds seed6-ham --agent-cmd true --out runs/ham1
python3 funnel.py review --run runs/ham1 --round 1
cd /home/ubuntu/proclusagent && python3 validate_ham.py; echo exit=$?
python3 seed0.py check /home/ubuntu/seed0/seeds/seed6-ham
```

## Worked example: ham-1 (this session's numbers, all logged)
- Tournament: seed6-ham 5/5 compliant, suite 10 passed green, rank #6/6 by evidence
  (rank is honest: 0 evidence files; F3 requires green, not rank — rank ≠ falsified).
- Funnel collect-only: FIRST run binary_pass=false — rubric pointed at root
  ham_registry.py after the file moved to tests/. The harness caught a
  rubric-reality mismatch (exactly what it's for); fixed rubric → re-run all-true.
- Validator: 6/6 checks, exit 0. Receipts: tournament `runs/sha256_d16c543e…`,
  funnel `runs/ham1/scores.jsonl`, validator JSON above.
- Learning: rubric paths must mirror seed layout — new criteria rule: re-run
  collect-only after ANY seed move (encoded as A-task pattern, not just memory).

## When NOT to tournament
Real agent-cmd runs (H4), spend (M*), PRIV data, giant full clones (H1), publishes
(H5) — spec them, never run them, until the human signs the exact scope.

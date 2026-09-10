# LOOP — recursive A-task runner (how it works)

`aloop.py` is the dormitory foreman-that-isn't: it only runs kind=A, cost=$0,
no-manual tasks. H/M are append-only discoveries, never executed.

```
QUEUE (crash-safe JSONL)          LOOP                           MINE
docs/A-QUEUE.jsonl open/done ──► aloop.py --once ──► runs/<rid>.json
       ▲                              │ guard() rejects spend/push/
       │ spawns + propose_next() ◄────┘ publish/PRIV-publish/giant-full-clone/keys
       │                              │ hands H/M proposals to H/M queues instead
docs/H-QUEUE.jsonl (append-only)   bottleneck = no runnable A OR blocked_by open H/M
docs/M-QUEUE.jsonl (append-only)
```

Recursion sources (two levels):
1. Task-level `spawns`: each A-task declares follow-ups (e.g. T2 sweep → reindex).
2. Global `propose_next()`: when queue empties, inspect mine state and mint new $0 tasks:
   - test-less packets → `boot_tests max=5` batches
   - stale INDEX → `index`
   - no recent verify → `verify`
   - no funnel wiring proof → `funnel_collect` (agent-cmd=true, no LLM)

Commands ($0, local-only, reversible):
```bash
cd /home/ubuntu/proclusagent
python3 aloop.py --status                          # queues, no run
python3 aloop.py --once                            # 1 task + receipt
python3 aloop.py --until-blocked --max 20          # drain queue, stop at bottleneck
python3 aloop.py --evolve                          # preview what generator would mint
python3 aloop.py --until-blocked --max 20 --evolve-loop   # RECURSIVE: drain → evolve → drain …
```

Persistent autonomous mode (pick one, all $0 until you approve H/M):
```bash
# foreground loop, stops only on true H/M bottleneck with nothing auto-mintable
while true; do
  python3 aloop.py --until-blocked --max 20 --evolve-loop | tail -n 20
  python3 aloop.py --status
  sleep 60
done
# background:
# nohup bash -c 'while true; do python3 /home/ubuntu/proclusagent/aloop.py --until-blocked --max 20 --evolve-loop >> /tmp/aloop.log 2>&1; sleep 120; done' &
# tail -f /tmp/aloop.log
```

Guards (hard, in `guard()`):
- kind must be A, cost must be $0, needs_manual must be false
- forbids: ghp_/sk-/PRIVATE KEY, wrangler deploy, --publish, git push, API_KEY=, spend/deploy/push flags
- giants (Ochema/KBO/blogengine/tantraloka-study/ochema2/patalacheckpoints/patala) → sparse only, full_clone auto-rejected to H1
- PRIV 11 → any publish auto-routed to H2, never cloned for publish
- every run → `runs/sha256_*.json` receipt; verify by recomputing id from content

Current state: 49 packets, digest 8e339820821e31e9, verify 49/49 ok, 14 A done / 0 open.
Next auto-mints will keep covering remaining test-less packets until all have boot_test.py,
then loop idles at true bottleneck awaiting H4 (promotion) / M1 (live evals).

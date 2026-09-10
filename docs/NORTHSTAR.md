# NORTHSTAR — the autonomous tournament chain (set 2026-09-10, binding)

Run tournaments again and again, each round changing seeds (seed1 → 1.1, …) from
the previous round's results plus analysis. Log justifications for every change.
Keep schemas clean, everything on git branches (local; push stays human-gated).
Then the whole thing runs as an autonomous loop. a-logs become THE evidence:
match every a-log to its a-task — when coverage is 100% and the queue is empty,
the loop may stop. On stop, emit an A-REPORT per a-task with validation evidence
for peer review; peers send back failures as new a-tasks until perfect.

Chain (each link $0 local unless marked H/M):
results → analysis → amend x.1 (justified) → branch/commit (no push) →
re-tournament → compare → a-log match → stop? → A-REPORT → peer review → repeat.

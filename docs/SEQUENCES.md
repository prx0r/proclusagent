# SEQUENCES — presses become workflows; agents become A-task native

## Press 3 then 1 (your exact vision, built)
Sessions of picks are mined (`predictor/sequences.py`) into macro proposals:
frequent bigram (A→B, support≥2, conf≥0.5) becomes one press replaying both.
Texts, never positions (ranking shifts; texts survive). Ran on live choice logs:
3 rows so far (test/demo presses) → no macros yet, honestly. First real macros
appear after UI use. Thresholds live in the call, tunable on data.

## How agents go A-task native (contract)
Every agent loop, any substrate: read open tasks → execute lowest-blocked →
write receipt → propose H on block, never guess. Concretely: `ham_registry.py`
here; `loop/tasks.jsonl` + `registry_{a,h,m}.jsonl` + `hinbox.poll()` + `grants.py`
+ `ROUTINES.md` upstream. Same shape, two implementations (convergent = validated).

## seed0 ↔ proclusagent map (reviewed origin/main 2026-09-10)
| seed0 (upstream, 110 green) | proclusagent (here) | Note |
|---|---|---|
| loop/tasks.jsonl + registry_a | A-QUEUE.jsonl + ham_registry | same removal law, both sides |
| registry_m + grants.py (x402, cents) | M-QUEUE + grant-token pattern | theirs live-settles; ours file-locked |
| registry_h + hinbox + mw queue.html | H-QUEUE + poll design | THEIR inbox UI exists — import, don't rebuild |
| ROUTINES.md (cg REPRODUCE) | RECIPES.md + LOOP.md | same receipts-or-it-didn't-happen |
| PROMPT_LIBRARY.md | prompts/corpus.jsonl + PROMPT-LIBRARY.md | merge corpora on seed0 merge |
| attempts.jsonl A-log (seed1.1) | a-logs/SESSION-*.jsonl | same append-only shape |
| learn.py failures→proposals | macro miner + funnel review | both feed criteria bumps |
| META_LOOP.md / CONTROL_PLANE | METAGUIDE.md + aloop.py | compare before merging |

## Merge status
Upstream +392 files held UNMERGED (tracked collisions in seeds/ + tournaments).
Say `merge seed0` and I attempt with per-file care, aborting to you on conflict.
Biggest wins waiting inside: inbox UI, grants rail, routines, their prompt library.

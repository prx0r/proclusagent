# ENDGAME — seed0 framework + buttons → predict → H-escalate (binding loop)

You hit buttons (options, and now TYPE tags) until it predicts what you'll say.
When it can't do so with confidence, it prompts an H-task instead of guessing.
Every turn logged to a-logs; STOP when queue empty + evidence matched; A-REPORT
for peer review; send back until perfect.

## Why type tags change the math
- Option press = exact-text label (kills the 0.16% exact-match problem for picked
  turns: actual IS recorded verbatim).
- Type press = free supervised family label (kills the 0.42 family-inference step;
  `suggest_typed` filters + `per_type` stats accumulate from turn one).
- Typed-own + tag = fully labeled novel datum (best training row there is).

## The loop (running now)
seed0ike H-A-M (A autonomous, H parallel, M locked) + predictor (suggest →
Enter/buttons/type → log with tag) + cascade routes (auto/buttons/h_delegate) +
tournaments + funnel + learn.py + METAGUIDE. Corpus 24 specimens / 11 groups and
growing — the library IS the training-data pipeline in miniature.

## seed0 status 2026-09-10
Fetched, NOT merged: upstream +392 files (HAM harness, registries, seed1.1 —
parallel build by owner). Our branch (mine + amendments) intact. Merge needs a
human call (tracked-work collision risk); say `merge seed0` and I attempt it with
per-file care, aborting to you on any real conflict.

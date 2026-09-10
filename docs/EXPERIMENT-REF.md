# EXPERIMENT REF — mini-me predictor program (2026-09-10, all numbers)

Objective: predict prx0r's next response (buttons + Enter-accept → autonomy).
Data: 8,497 sends, 390 sessions, chronological, from 6.09GB opencode.db (/tmp
quarantine; corpus never in repo). Protocol: frozen train/test split (4248/4249)
unless noted "online" (chronological, no peeking).

## Results (test half, n=4249)
| Model | Task | Score | Note |
|---|---|---|---|
| fastText | text→family | **0.807** (0.799 unseen n=4068) | router king; .ftz 8MB @ 0.795 |
| fam-hit@3 retrieval | top-3 | 0.671 (n=8496 online) | buttons work |
| hashed-linear | context→family | 0.437 | best pre-type |
| explicit-linear | context→family | 0.428 | most portable; node parity 200/200 |
| session-prior | context→family | 0.436 online / 0.376 split | needs live adaptation |
| mininet MLP-128 | context→family | 0.384 | loses (4k rows too few) |
| kNN | context→family | 0.367–0.418 | competitive second only |
| majority | per head | 0.33–0.59 | floor |
| exact-template | verbatim | 0.0016 | dead — proves buttons 400:1 |
| continue history/dialog/joint | pre-type auto | 0.195 / 0.166 / 0.193 | all falsified; gate CLOSED |
| ensemble blends | frozen split | tie global 0.404 | kNN drags; tune α ONLINE |

## Key verdicts (falsifiable, falsified-or-held)
1. Shallow > deep at small n (linear 0.44 > MLP 0.38; cf. tg 6-knob > 44-knob).
2. Buttons > auto-send by 400:1 (family 0.42/top-3 0.67 vs exact 0.0016).
3. No pre-type signal clears 0.9 (three falsifications) → Enter-accept product.
4. Session signal exists ONLY online (frozen session-prior collapses to 0.02).
5. Replay: exact-text scoring never learns (flat curves, τ unreachable) → family
   ranker tried (hit3 0.52 < 0.64, retained text default); slice-conditional next.

## Artifacts (reproduce)
- Corpus: `/tmp/opencode-sample/corpus_clean.jsonl` (scrubbed) — rebuild: §MINI-ME.
- Train/eval: `predictor/{pilot,rl_env,ensemble,mininet}.py`; fastText: §MININET.
- Live: `p`/`pt` shell fns, `/predict` command, MCP `predict.*`, choice log.
- Gates: `seed0.py check` 5/5, validator 6/6, secret-scan (caught 3 live incidents).

## Open gates (in order)
Family-confidence re-replay → UI choice volume → calibrate τ → DPO/IRPO →
LoRA (r=4–8) → autonomy ladder on live hit-rate. No step skipped without numbers.

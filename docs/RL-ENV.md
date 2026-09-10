# RL-ENV — offline bandit env on 8,497 real sends (numbers, verdict)

## Setup
Corpus: `/tmp/opencode-sample/corpus_full.jsonl` (quarantine, never repo):
8,497 user sends ≤1000 chars, 390 sessions, chronological, from 6.09GB db
(damage isolated to `event` table; message/part/session/todo clean).
Env `predictor/rl_env.py`: per turn → 3 retrieved ACTUAL past responses (never
invented) + 3 heads (H1 length S/M/L · H2 continue? · H3 coarse category).
Protocol: pure online chronological (score on index of past only, then update).
kNN (Jaccard over title+prev+project/agent tokens, k=5) vs majority / random /
global-prior / session-prior. 354s single pass, stdlib only.

## Results (n_scored=8496)
- **fam-hit@3 = 0.671** — true family inside 3 retrieved actual responses.
- H1 length: majority/global/session **0.586** > kNN 0.557 > random 0.330.
- H2 continue: majority **0.840** > kNN 0.809 > random 0.507 (~84% continue-like:
  first-token ack + <80 chars — the terse-driver style is real).
- H3 category: session-prior **0.436** > kNN 0.418 > majority 0.397 > random 0.122.
- Family mass: ack 3416, **other 3412 (40%)**, question 626, neg 348, review 315,
  task 139, paste 126, pathref 115.

## Verdict: kNN is NOT best alone — ensemble is
Running-majority takes skewed heads, session-prior takes category (sessions are
topically coherent: Smart-Compose α→1 direction), kNN is competitive second
EVERYWHERE and the only general method. Ship the blend (prior + kNN + majority
fallback = scorer.py philosophy), exactly as Smart Compose blends global+personal.
Frontier mapping: CBNN legitimizes kNN+UCB exploration next; CSI says keep
value-style heads, not policy heads; LaMP says combine, don't replace.
Biggest lever: split the 40% `other` bucket (token sub-clustering) — lifts every
head's ceiling. LoRA stays gated (volume exists NOW at 8.5k — gate is hit-rate
plateau + H/M, not data).

## Round 2 (idea3, seed0 framework: funnel scores + review + learn.py)
Split validation (train 4248 / test 4249, frozen): len global 0.5752 wins;
cont saturated 0.8303 everywhere; cat global 0.4039 > uniform-blend 0.3909 >
session 0.3761 > kNN 0.3674. **F1 FALSIFIED** — kNN drags blends down; next is
session↔global α-sweep WITHOUT kNN (+ similarity-gated kNN). F2 passes with
caveat (top other-subgroup 1.2%, topical). F3 fired as designed (online vs
frozen sign flip = adaptation effect). Credential-adjacent pastes found in sends
→ redact credential patterns before ANY training use (hard rule).
learn.py on runs/predictor: 6 events → 2 criteria1.1 proposals (shared cat/len
failures; human promotes). Full grid: `docs/RL-ROUND2.json`.

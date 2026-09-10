# REPLAY-SIM — 8,497 turns of simulated live use (cold start, honest numbers)

Lab: corpus_clean + 8 ack templates + τ 0.9/0.5 + fresh store. Chunk 1 (0–4250) +
tail (6941–8497, mature 6.9k store). Full curves in run output; heads below.

## Results
- hit3: 0.639 → 0.622. enter-precision: 0.397 → 0.412. auto_rate: 0.0 → 0.0.
- Level: suggest → predict (hit_rate_top1 crossed 0.4).
- Windows volatile both chunks (enter 0.32–0.50, hit3 0.46–0.70): session
  heterogeneity, no visible learning slope.
- Calibration: multi-bin early (0.1→0.14, 0.2→0.20, 0.4→0.40 — roughly honest),
  collapsed to single bin 0.4→0.42 late. Calibrated but BLUNT (sharpness failure).

## Reading (this is the important part)
1. **The system does NOT learn.** 6,941 logged turns moved enter-precision within
   noise and hit3 slightly DOWN. More data ≠ better under exact-text Laplace
   scoring — per-text counts stay thin forever. Structural fix required, not tuning:
   score FAMILIES (dense) for confidence, present TEXTS (instances) as options.
2. **τ=0.9 unreachable, twice confirmed.** Auto never fired in 8,497 turns.
   Follows from (1): top exact-text conf saturates ~0.4–0.5.
3. **Level promotion is misleading.** suggest→predict fired on a flat metric.
   Handover criterion must require improvement SLOPE (dHit/dTurn > 0 sustained),
   not just level. Encode before any live auto-run.
4. Mild late-segment degradation supports the drift/decay backlog (frontier gaps).

## Next (ordered)
Family-confidence scorer → re-replay (expect auto_rate>0 + positive slope) →
slope-gated autonomy → live buttons.

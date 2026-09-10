# ARXIV PEERS — who did our exact experiment, and what changes (2026-09-10)

## Direct hits (same experiment, bigger N)
- **CDHF (Mozannar/Horvitz, AAAI)**: cascade predicts ACCEPTANCE to show/withhold;
  hides 25% would-be-rejected at 95% guarantee; latent user state matters (ablation);
  warning: acceptance-as-reward can degrade quality. → Our τ-gate IS this; adopt
  their framing (utility, not accuracy) + their warning (don't optimize buttons
  for clicks at the cost of substance).
- **CSAP**: tiny NN predicts suggestion acceptance 0.973/0.922; best features are
  HABIT ratios (developer/project acceptance history). → Our per-option/family CTRs
  are the same features; validates them. Next: add session/project habit features.
- **CUPS (12 states) + transitions + dwell**: independent convergence with our 11
  intent boxes. Their states include AGENT-side activity — ours don't. → Upgrade:
  joint alphabet (below).
- **ProCodeBench (1,246 devs)**: real traces beat simulated; repo context helps;
  agents strongest. → Validates real-data-first; our corpus IS the asset.
- **Personalized Skills (206 sessions)**: personal skills ≈ noisy; GENERIC pooled
  skills win. → Caution for LoRA expectations: shared/family-level first, personal
  exact-text last. Matches our 0.42-vs-0.002 split exactly.
- **Next Edit Prediction**: position-vs-content split + exact/partial/position
  metrics → mirrors our family-vs-exact split; adopt position-style metrics.
- **Overwatch**: edit SEQUENCE patterns at 78% precision on action traces.
- **HyperSeq**: hyperdimensional n-gram state prediction >70% WITH online
  adaptation; states include idle/tool/tool-result context.

## The joint-alphabet verdict on our 0.37
Overwatch + HyperSeq + CUPS all say: sequences over MESSAGE labels fail, sequences
over RICH STATES (incl. agent acts, tool outcomes, dwell) work. Our n-gram ran on
the poorest alphabet. Experiment below re-runs on joint (user-intent × agent-act)
trigrams with backoff, online. If it clears ~0.45, sequences reopen; if not,
the negative result stands on a fairer test.

## Outcome 2026-09-10 (ran it — LOST, honestly)
Joint (agent-act × user-intent) trigram+backoff, online, per-session reset
(`predictor/ngram.py`, 3 tests green): **0.291** over 8,102 turns — worse than
markov-1 (0.371) and global majority (0.353). Cold-start per session + 44-symbol
sparsity kill it. Peers win on RICH states (tool outcomes, dwell, code), not on
counting — our alphabet is too poor for sequence methods, exactly as
CUPS/FlightRecorder imply. Sequences stay closed pending state-rich telemetry
(the choice log IS that telemetry: shown/picked/conf per turn — rerun n-grams
on IT when mature).

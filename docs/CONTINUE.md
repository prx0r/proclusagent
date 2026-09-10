# CONTINUE — easiest-first autonomy: measured, gated, currently buttons-only

## Data (8,497 sends, split-validated where noted)
- Short-ack rate **0.16** (1,359). Top variants: continue 52, yes 51, go 18,
  yep 13 — but **152 distinct** short-ack texts (long tail strikes again).
- History does NOT predict it: prev-ack→next-ack precision **0.195** (base 0.16);
  markov2 0.226 @ cov 0.031; kNN ≈ base rate. Acks ALTERNATE with substance
  (command → result → "ok" → next command) instead of clustering.
- No pre-type signal tested clears precision 0.9 at coverage 0.05. The gate in
  `predictor/continue_.py` (`licensed()`) therefore stays CLOSED on current numbers.

## Operating policy (encoded, tested)
`decide()`: blast_radius≠low → h_delegate; predicted-continue + licensed →
auto_proceed; else buttons (Enter-accept). The 0.9/0.05 bar is in
`TAU_PRECISION`/`MIN_COV`, tunable only with measured evidence.

## What WOULD license auto-send (next experiment, real shot)
Dialog-STATE features, not user history: label each turn by the preceding
ASSISTANT act (confirmation-question vs deliverable vs error — 89,805 assistant
messages already in the db). Hypothesis: P(short-ack | agent-asked-confirmation)
is high and measurable. If precision ≥0.9 there, the continue button ships with
a state gate instead of a history gate.

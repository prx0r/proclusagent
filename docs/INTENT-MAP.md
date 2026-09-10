# INTENT MAP — 11 boxes, trajectories measured, verdict: coherence-not-chains

11 data-derived boxes (8,497 sends): ack-proceed 2913, other 2904, prose 478,
question 475, neg-redirect 356, task-do 353, review 315, continue-thread 251,
request 185, pathref 141, paste 126. Code: `predictor/intent.py` (+tests).

## Transition measurement (within-session, chronological, n=8,107 transitions)
Top pairs by volume: ack→ack (1140), other→other (989), other→ack (912) —
but lifts run 0.88–1.12 (near-independent!). Markov-1: **0.371** vs majority
**0.353** (+0.018). Session-majority predictor: **0.360**. Verdict: pairwise
"intent follows intent" is barely above chance. Sessions have sustained intent
(topical coherence — what session-prior exploits), but the chain is ~memoryless.

## Correlation, measured properly (you pushed back — you were half right)
Full 11×11 matrix: chi-square 424 on 100df (dependence is REAL, p≈0) but effect
size negligible — MI explains **1.1%** of next-intent uncertainty, Cramér's V **0.07**.
The real structure is SELF-LOOPS: review→review 3.1×, task-do→task-do 2.4×,
question→question 1.7×, prose→neg-redirect 1.6×. Translation: you work in bursts
(verify-verify-verify, build-build-build), then move on. Bursts, not chains.

## What this means for trajectories
Trajectories exist as SESSION SHAPES (open → drive → verify → report rhythms),
not as pairwise grammar. Next: mine session-shape clusters (whole-sequence
types), not bigrams. The 10-key instrument already matches the box set
(continue/yes/go≈ack-proceed, verify≈review, drain≈task-do + ops).

## Why bursts happen (tested, not theorized)
MI(agent-act; your-intent) = **0.0087 bits (0.4%)** over 9,044 pairs — even weaker
than prev-intent (1.1%). Neither your last message nor the agent's last act predicts
your next intent (best lifts: other→continue-thread 1.71, deliverable→ack 1.08).
Yet sessions cohere (0.44) and retrieval hits (0.67). Resolution: transitions are
driven by UNSERVED-STATE task phases (a verify-phase makes everything review-shaped)
that coarse labels can't see. Bursts = phase residence, not Markov dynamics.
Retrieval wins because full-context similarity implicitly recovers phase; label
chains cannot. Next lens upgrade: finer task-phase features, not bigger n-grams.

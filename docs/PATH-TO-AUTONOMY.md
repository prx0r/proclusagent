# PATH TO FULL AUTONOMY — the goal (binding direction, 2026-09-10)

Automate the easiest calls first (continue + repetitive), go live so the system
sees actual responses and learns, hand over at threshold. Creative/hard work
trials the LLM with H-delegation running in parallel: easy tasks continue
autonomously while the human takes its time, then unlocks the hard ones.

## Phases (each gated by the previous one's numbers)
1. **Enter-accept live.** 3 buttons + highlighted default after every agent output.
   Metric: hit-rate@3 (offline: 0.67) then live accept rate. Gate to 2: live log flowing.
2. **Choice log learns.** Every press/dismiss updates confidences online (built:
   Laplace posterior, no retrain) + ECE + decay measured live.
3. **Auto-proceed easy intents.** `predictor/cascade.py`: intent=ack AND conf≥τ
   AND low blast radius → proceed signal (NOT verbatim string — top exact template
   covers ~2%; auto executes INTENT). τ starts 0.9, tunes down only on evidence.
4. **Creative → LLM trial + H-delegate.** Hard intents route to LLM draft AND an
   H-task proposal; easy As keep running (`ham_registry.runnable_a` skips blocked;
   `poll()` picks up browser approvals; `human_priority()` orders the human queue).
   Proven in `tests/test_cascade.py::test_parallel_stream_h_delegate_unblocks`.
5. **Handover.** `autonomy.py` AUTO + calibrated hit-rate + your trust: Enter becomes
   a heartbeat monitor, not a chooser. Revert any phase on metric regression.

## Non-negotiables
Spend/publish/delete = never auto (M-locked, single-use grants, no-self-approval).
Raw chats never enter repo (shapes + counts + redacted templates only).
Thresholds live in `predictor/thresholds.json`, tuned on live data, never vibes.

# PREDICTIVE-UI — buttons that learn you, then become you (research + plan)

## Your idea, stated back
After each agent response, N prompt-buttons flash up (your most likely next moves).
You press one or type your own. The model predicts your pick; when prediction is
reliably right, it runs autonomously. This exists in pieces — nobody has the full
loop (predict → log choice → finetune → autonomy threshold) in a coding agent. We can build it.

## Prior art (what to steal)
**Predictive UI (buttons/suggestions):**
- **Claude Code NES → qwen-code PR #2525 (+LLM refactor)**: ghost placeholder + Tab/arrows,
  rule-based → `generateJson()` + 14 filter rules, 11 guard conditions, fast-model option,
  `PromptSuggestionEvent` telemetry + `onOutcome` (accepted/dismissed). Closest sibling —
  port its architecture (state reducer + generator + keybinds + suppression log).
- **agno followups**: `followups=True`, structured-output second call, FollowupsStarted/
  Completed events, per-model metrics. Proves the 2-call pattern is cheap and measurable.
- **langgraph-compass** (Cisco): trigger policy (skip on guardrail/short), capability
  grounding (only suggest fulfillable!), novelty ranker, parallel Send (zero latency),
  LangMem WorkflowRetriever — "suggest THEIR typical next step" (this is your version).
- **ago/analytics**: engagement rate, by-count, per-agent, top-clicked; click = reply
  matches suggestion. Copy these 4 dashboards from day one.
- **assistant-ui chips / OpenClaw skill**: rendering patterns + 3-category (quick/deep/related).

**Intervention → autonomy (the learning half):**
- **HG-DAgger**: you supervise, novice rolls until you take over; learns doubt threshold
  τ = mean of final 25% of intervention log. τ IS your "when to go autonomous" knob.
- **EIL**: non-intervention is also a label (implicit approval). Your NOT pressing a
  button / letting it run = approval signal. Free labels on every turn.
- **ThriftyDAgger**: robot-gated — asks only when novelty+risk high, within YOUR
  context-switch budget α_h. This is "predict my pick, bother me only when unsure."
- **PPL (NeurIPS'25)**: each intervention → preference pairs over predicted horizon
  (DPO-style). Your correction propagates to risky futures, not just this turn.

## Design for your opencode build
1. **Suggest bar** (TUI placeholder + 1/2/3 or Tab/arrows, dismiss-on-type; skip when
   guardrail fired / question pending / plan mode — qwen-code's guards, ported).
   Candidates = router templates (controller/) + WorkflowRetriever (your top-N families
   from WAL mining) + LLM fallback. Capability-grounded (compass rule): only phases the
   harness can actually run.
2. **Choice log** (the gold): `{session, context, shown[3], picked|null, typed_own}`.
   `session_input.prompt` already stores typed-own labels; add shown-set → every turn
   becomes (context → chosen ≻ rejected) preference pairs + EIL implicit approvals.
3. **Autonomy ladder**: L0 suggest → L1 predict (show top pick first) → L2 auto-run when
   P(pick) > τ, τ learned HG-DAgger-style from YOUR intervention log → L3 trusted
   classes (seed0 HUMAN_LOOP rung, human-set). ThriftyDAgger budget caps interruptions.
4. **Finetune ladder** (each step only if prior plateaus): rules → retrieval →
   SFT on (context → picked) → DPO on (picked ≻ rejected) → LoRA on your full
   prompt corpus (H6/M5 pull). Your median prompt is 32 chars — small-model territory;
   a cheap fast model (qwen-code pattern) predicts picks, big model builds.

## Experiment (gates before spend)
Metrics: hit-rate@3, accept rate, autonomy rate vs τ, calibration of P(pick),
intervention count (minimize), build success (must not regress).
Start: rules+retrieval on WAL families ($0, this repo) → log choices → DPO only when
hit-rate plateaus AND you approve M (GPU/API). Never train on raw logs (keys inside);
train on shapes + templates + outcomes.

## IMPLEMENTED (this session, 20 tests green, 5/5 COMPLIANT)
`predictor/` (stdlib): `store.py` (JSONL choice log + stats incl. hit_rate_top1),
`scorer.py` (Laplace-blended confidence, WAL-seeded family priors),
`suggest.py` (top-3 + default=0 = Enter accepts top), `autonomy.py`
(suggest→predict→auto from calibrated hit-rate vs τ; REPORTS only, never executes).
Wired into MCP (`predict.suggest`, `predict.log_choice` + round-trip test) and
proven headless. Confidence updates on EVERY logged choice — no retrain needed.
Enter-workflow contract: Enter = top, 1/2/3 = pick, type = dismiss+typed_own;
TUI binding itself is opencode-fork work (spec'd here, not built here).

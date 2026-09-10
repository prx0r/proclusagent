# TEN KEYS — the instrument (fixed digits, chains queue, H-flow built in)

Layout (`predictor/keys.py`, positions NEVER move): 1 continue · 2 yes · 3 go ·
4 verify · 5 drain · 6 zoom out · 7 recon · 8 push · 9 h-queue · 0 mine.
Digits 1-3 + push text grounded in exact counts (52/51/18/21); 4-7 are library
high-value moves; 9 opens the human queue; 0 escapes to typing.
Type `2943` → queues [yes, h-queue, verify, go], each logged with chain id
(`predict --keys`). Sequences mine into macros (sequences.py) — chains you repeat
become single presses. Model-side: keys are FIXED intents, so choice data is clean
by construction (no ranking-shift noise); learning scores families per key.

## H-flow (your job description, mechanized)
Buttons 1-7 run or propose A-work; 8 (push) and anything spend/publish-shaped
PROPOSE H-tasks instead of executing (ham_registry: unlocks graph +
human_priority + browser poll). Your job: press numbers to keep A-tasks flowing,
spend creative time on H-tasks. Automating MORE H: approvals can never auto
(giwacard industry rule — auto-approval is no approval), but everything around
them can: pre-verified one-press approvals, drafted info with confirm-defaults,
EIL implicit approval for explicitly opted-in low-risk classes, batching +
priority order (all built). Compress H, never eliminate it.

## LoRA verdict (your 5GB question, answered with numbers)
Trainable data is NOT 5GB — it's 8,497 (context→send) pairs, median 32 chars.
That's enough to LEARN from (fastText hit 0.81 on related signal) but thin for
LoRA: LaMP measures PEFT at +1% alone in this regime; RAG wins cold-start.
Recommendation: LoRA on a 1–3B base for YOUR phrasing AFTER choice data flows
(shown-sets give DPO pairs; mined history lacks counterfactuals) — try Colab
free tier first ($0), cap a paid run only on plateau. Retrieval + templates carry
until then. Gate recorded; no GPU spent today.

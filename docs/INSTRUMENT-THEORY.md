# INSTRUMENT THEORY — external validation + build orders (received 2026-09-10)

Thesis: prompt-instruments (fixed keys, composition, confidence-gated autonomy)
are an HCI-legible instance of several published lines. Our novelty vs each is noted.

## Validated against
- **DirectGPT (CHI '24)**: executed prompts become toolbar tools; 50% faster, 50%
  fewer / 72% shorter prompts. Our novelty: fixed 10-key vocab + composition
  (10^n chains) vs unbounded growing toolbar. THEIR NUMBERS ARE OUR BENCHMARK:
  run chat-only week vs instrument week once presses accumulate.
- **Log2Plan (arXiv:2509.22137)**: frequency-mines behavior logs into reusable
  flows, 60%+ on 20-step tasks. Same family as our macro miner; we add the closed
  loop (macro → press → receipt → re-mine).
- **OS-Kairos (arXiv:2503.16465)**: per-step confidence γ gates autonomy vs
  intervention; 19% intervention matches human rate. Validates threshold-gated
  autonomy outright. We add: per-key thresholds + ratchet-with-meter + hard money
  exclusion.
- **AGORA (arXiv:2605.26596) + HiconAgent (arXiv:2512.01763)**: token compressors
  destroy action verbs; action tokens are information anchors. RULE: never
  token-compress press rows — keep (context→decision) pairs whole, compress around.
- **CogniGUI (arXiv:2506.17913)**: Kahneman System 1 (fast parser) + System 2
  (deliberative grounder). OUR FRAMING EVERYWHERE: 10 keys = System 1, A-task
  framework = System 2. Fast virtuoso layer over slow verified layer.

## Honest counterpoint (kept, not buried)
Beaudouin-Lafon: instruments don't fit dialogue interfaces (the CLI objection).
Answer, already proven by DirectGPT: keys carry VERBS, capture carries NOUNS —
our grammar does this (digits bind verbs, typing binds nouns).

## Build orders (steal these concretes)
1. Verb–noun binding (DirectGPT §3.2): PICK shows its nouns — dash renders open
   options WITH the keypad, not on another screen.
2. γ per key (OS-Kairos): separate thresholds; ZOOM/DIG first, GO next, chains of
   {1,2,3} later. Already shaped in thresholds.json — now cited.
3. Zipf acceptance test (Ellis): monthly fit on presses; top-3 share quantifies
   "10 keys cover most actions."

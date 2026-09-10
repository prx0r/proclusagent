# WASM-PLAN — our classifier the tg way (genome → template → artifact)

## Mapping (tg → us)
genome floats → **genome weights** (`wasm/genome.json`: vocab + coef + intercept,
65k entries from explicit-vocab linear, test-split acc **0.4283** — 2nd best overall,
beats MLP 0.384/session 0.376/kNN 0.367, below hashed-linear 0.4373).
`emit_real_wasm.py` → **`wasm/export_genome.py`** (re-runnable emit step).
Rust template → **`wasm/scorer.js`** (exact string lookup, no hash ambiguity;
murmur3 approach ABANDONED after measured mismatch vs sklearn — documented, not hidden).
`beat_champion.py` → **`tests/test_wasm_parity.py`: 200/200 node==Python**.
Node feedback → our tournament/funnel/validator gates.

## Why this shape wins twice
1. fastText (Joulin et al.): LINEAR hashed models ≈ deep nets on text, seconds on
   CPU. Our data agrees (linear 0.43 > MLP 0.38). Shallow + right features beats
   capacity at 4k rows — same lesson as tg's 6-knob > 44-knob.
2. A linear vocab model ports ANYWHERE: this JS is a mechanical step from wasm32
   (bake genome as constants, exact tg pattern). sklearn MLP can never ship this way
   (needs ONNX runtime, MBs). fastText.zip-style pruning/quantization (<100KB) is
   the documented next squeeze; genome.json (13MB) stays a git-ignored artifact.

## Gated compile step (needs a rust box; NOT this box — no cargo here)
```bash
/tmp/mininet/bin/python wasm/export_genome.py   # emit
python3 -m pytest tests/test_wasm_parity.py -q  # 200/200 parity gate
# then: bake genome constants into scorer.rs, cargo build --release --target wasm32-unknown-unknown
```
WASM-PLAN status: emit + parity DONE ($0). Compile = future A-task on a rust box.

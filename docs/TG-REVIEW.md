# TG REVIEW — what telegraph-lab's public snapshot actually is

Not neural-net training. tg = **evolutionary scorer smithy for the Telegraph
hackathon**: genome (6 floats) → `fleet/builds/emit_real_wasm.py` injects constants
into a hand-written no_std Rust scorer template → `cargo build --target
wasm32-unknown-unknown` → `beat_champion.py` benches vs champion `.wasm` →
submit ($0.01) → node feedback (ordering / separation / selfmatch over 15 hidden
cases) → mutate → peer review → repeat. Two lanes (fleet NUM+VERDICT, factjudge
NLI+RANK), cge1/cogym evolution harness, 5,400+ adversarial benches, ARXIV-RESEARCH
with 25 papers. Commit: `76d846a public snapshot (dead tokens redacted)`.

## The critical finding (theirs, quoted)
6-knob template margin **0.859** (0.031 from champion 0.890) BEATS 44-knob
zkasuran 0.666. Capacity hurt under node eval. Fewer knobs + hard benches won.

## Thesis
tg is the competitive-evolution half of the org: where seed0/cogym run clean
tournaments, tg runs ADVERSARIAL ones against a hidden judge with cheap entries
and informative losses ("repeated game"). proclusagent inherits its loop shape
(results → classify failure → prescribe mutation → peer review → resubmit) and
its restraint doctrine (6 knobs, not 44).

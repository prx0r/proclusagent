# DEP-PILOT — venv-installed test spec, proven on 3 repos (2026-09-10)

Method (per repo, $0 + transient disk, system python never touched):
clone (sparse; full only if tests need siblings) → `python3 -m venv /tmp/pilot-X`
→ `pip install -e .[dev]` (or requirements.txt, or pytest-only fallback) →
`pytest -q` (90s cap) → secret-scrub tail → `rm -rf` clone + venv.
Caps: 10 min + 2GB transient per repo; bounded parallelism (≤4); torch/CUDA/cargo
repos flagged + skipped with reason (toolchain decision, not silent skip).

## Pilot results (evidence)
- `telegraph-factjudge` (PRIV, full 716MB clone): 4 passed / 2 failed with pytest
  only (no requirements.txt exists). Failures reproduce keyless finding:
  `test_api` ModuleNotFound, `test_engine_pipeline` error. Needs owner env —
  real triage target, not an artifact.
- `cge1`: 6 passed with `-e .[dev]`. Keyless sweep said rc5-empty/tests-absent
  (sparse root-only hid tests/) — pilot corrects: WITH deps it's fully green.
  Lesson: sparse root-only undercounts suites; pilot uses full/sparse+tests.
- `csec`: 3 passed with pytest-only (package + tests + evidence/*.jsonl present).

## Standing rules from pilot
1. Sparse-checkout MUST include tests/ + package dirs, or disable sparse for small repos.
2. Missing requirements.txt/pyproject = signal (unreproducible env) — log, pytest-only, move on.
3. Secret-scan every tail before logging (scrub() shared with mininet.py).
4. Always delete clone + venv (716MB+90MB per heavy repo adds up fast).
5. venv lesson: one venv per concern (`/tmp/mininet` sklearn needs numpy≥2;
   fasttext predict needs numpy<2 — incompatible housemates, separate venvs).

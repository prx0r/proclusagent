# CLONE-TEST — all 144 repos cloned, tested keyless, deleted (2026-09-10)

Method: `git clone --depth 1 --filter=blob:none --sparse` → detect suite →
run native runner (90s cap, NO dep installs) → secret-scrubbed log → `rm -rf`.
Raw: `docs/CLONE-TEST-RESULTS.json` (144 rows, scanned clean). Cost $0. All clones deleted.

## Verdict table
- Cloned OK: **144/144** (incl. 11 private). 0 timeouts.
- pytest repos: 67 → rc0 **1** (`mwgym`, 1 passed), rc1 collected-and-failed **1**
  (`telegraph-factjudge`: 6 failed, ModuleNotFound + FileNotFound — REAL signal),
  rc2 import-error 49 (no deps installed — expected keyless), rc5 empty 11, rc4 5.
- node repos: npm present; 9 suites error rc127 (missing bins without `npm install`),
  13 no test script, `finalbuildsdomain` green via node:test, `finalbuilds2`/`pogtown`
  collect-todo output, `livellm`/`cancelme` JS stack traces.
- cargo 5: skipped-compile (heavy; needs H-venv decision).
- no-suite: 50 (stubs/essay repos — expected).

## What works vs what needs deps
Works keyless: mwgym, finalbuildsdomain (+ our own 5/5 repos).
Real failures worth triage: telegraph-factjudge (6), livellm, cancelme.
Everything rc2 is UNKNOWN not red — needs venv-installed runs (proposed: H-gated
batch installs, one venv per repo, 90s cap, same scrub/delete loop).
Node suites need `npm install` first (same gate). Cargo needs toolchain decision.

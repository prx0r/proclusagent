#!/usr/bin/env python3
"""validate_ham.py — binary falsification checks for hypothesis ham-1. Stdlib only.
Exit 0 = all falsifiers survived (claim stands this round). Exit 1 = falsified.
Usage: python3 validate_ham.py [--json]
"""
import json
import subprocess
import sys
from pathlib import Path
PROOT = Path(__file__).resolve().parent
SEED = Path("/home/ubuntu/seed0/seeds/seed6-ham")
sys.path.insert(0, "/home/ubuntu/seed0")
from seed0 import check as seed0_check
def run(cmd, cwd, timeout=300):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return r.returncode == 0, (r.stdout + r.stderr)[-300:]
def main():
    checks = {}
    rep = seed0_check(str(SEED))
    checks["F3_compliant_5of5"] = rep["compliant"]
    ok, tail = run([sys.executable, "-m", "pytest", "tests/", "-q"], str(SEED))
    checks["F3_suite_green"] = ok
    ok, _ = run([sys.executable, "-m", "pytest", "tests/test_ham_registry.py", "-q"], PROOT)
    checks["F1_F2_F5_registry_tests"] = ok
    hyp = (SEED / "HYPOTHESIS.md").read_text()
    checks["F_hypothesis_has_falsifiers"] = hyp.count("- F") >= 5
    import json as _j
    alog = PROOT / "a-logs" / "SESSION-2026-09-10.jsonl"
    recs = [ _j.loads(l) for l in alog.read_text().splitlines()] if alog.exists() else []
    aq = [ _j.loads(l) for l in (PROOT / "docs" / "A-QUEUE.jsonl").read_text().splitlines()]
    done = [t for t in aq if t.get("status") == "done"]
    checks["F4_alogs_cover_90pct"] = bool(done) and len(recs) >= 0.9 * len(done)
    mrow = [ _j.loads(l) for l in (PROOT / "docs" / "M-QUEUE.jsonl").read_text().splitlines()]
    checks["M_locked_no_spent"] = all(t.get("status") != "spent" for t in mrow)
    passed = all(checks.values())
    print(json.dumps({"pass": passed, "checks": checks}, indent=1))
    return 0 if passed else 1
if __name__ == "__main__":
    raise SystemExit(main())

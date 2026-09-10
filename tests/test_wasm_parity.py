"""WASM parity: node scorer.js must match Python on 200 fixtures exactly.
Skips if node/genome/fixtures absent (fresh box without the export step)."""
import json
import shutil
import subprocess
import pytest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def test_parity():
    if not shutil.which("node"):
        pytest.skip("node missing")
    genome = ROOT / "wasm" / "genome.json"
    fix = Path("/tmp/wasm_fixtures.json")
    exp = Path("/tmp/wasm_expected.json")
    if not (genome.exists() and fix.exists() and exp.exists()):
        pytest.skip("export artifacts absent")
    r = subprocess.run(["node", str(ROOT / "wasm" / "scorer.js"), str(genome)],
                       stdin=open(fix), capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr[:300]
    got = json.loads(r.stdout)
    want = json.loads(exp.read_text())["expected"]
    assert got == want, f"parity {sum(a==b for a,b in zip(got,want))}/{len(want)}"

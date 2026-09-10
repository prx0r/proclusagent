"""CLI tests: piped stdin drives enter/button/typed paths; log verified."""
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def run_cli(store, stdin_text, extra=()):
    r = subprocess.run(
        [sys.executable, "-m", "predictor.cli", "--store", str(store),
         "--session", "t", "--options", "ok", "verify it", "ship it", *extra],
        input=stdin_text, capture_output=True, text=True, timeout=60, cwd=str(ROOT))
    assert r.returncode == 0, r.stderr[:300]
    return r
def result_json(r):
    return json.loads(r.stdout[r.stdout.index("{"):])
def logged(store):
    return [json.loads(l) for l in Path(store).read_text().splitlines()]
def test_enter_accepts_top(tmp_path):
    store = tmp_path / "c.jsonl"
    r = run_cli(store, "\n")
    out = result_json(r)
    assert out == {"picked": "ok", "via": "enter"}
    assert logged(store)[0]["picked"] == 0
def test_button_two(tmp_path):
    store = tmp_path / "c.jsonl"
    r = run_cli(store, "2\n")
    out = result_json(r)
    assert out["via"] == "button" and logged(store)[0]["picked"] == 1
def test_typed_own(tmp_path):
    store = tmp_path / "c.jsonl"
    r = run_cli(store, "deploy it now\n")
    out = result_json(r)
    assert out == {"picked": None, "typed_own": "deploy it now", "via": "typed"}
    row = logged(store)[0]
    assert row["picked"] is None and row["typed_own"] == "deploy it now"
def test_learning_moves_top(tmp_path):
    store = tmp_path / "c.jsonl"
    for _ in range(10):
        run_cli(store, "3\n")
    r = run_cli(store, "\n")
    out = result_json(r)
    assert out["picked"] == "ship it"  # learned favorite surfaces to default
def test_defaults_are_library_moves():
    from predictor.cli import LIBRARY_DEFAULTS
    assert len(LIBRARY_DEFAULTS) == 3
    assert LIBRARY_DEFAULTS[0].startswith("run all a-tasks")
    assert "continue" not in [o.split()[0] for o in LIBRARY_DEFAULTS]
def test_keys_chain_queues(tmp_path):
    import json as _j
    from pathlib import Path as _P
    store = tmp_path / "c.jsonl"
    r = run_cli(store, "2943\n", extra=("--keys",))
    out = _j.loads(r.stdout[r.stdout.index("{"):])
    assert out["queued"] == ["yes", "show my open human tasks in priority order",
                             "verify it and report back", "go"]
    rows = [_j.loads(l) for l in _P(store).read_text().splitlines()]
    assert len(rows) == 4 and all("chain:2943" in x["context"] for x in rows)
def test_keys_bad_digit(tmp_path):
    import json as _j
    store = tmp_path / "c.jsonl"
    r = run_cli(store, "x\n", extra=("--keys",))
    assert "error" in _j.loads(r.stdout[r.stdout.index("{"):])
def test_keys_map_stable():
    from predictor.keys import BY_DIGIT
    assert BY_DIGIT["1"][1] == "continue" and BY_DIGIT["8"][1] == "push to git"

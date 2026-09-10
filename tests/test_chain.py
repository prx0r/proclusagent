"""Chain-handler tests: analyze/amend/report on synthetic dirs (CI-safe)."""
import json
from aloop import h_analyze, h_amend_seeds, h_report
def _tourney(d, rows):
    p = d / "tournament_1.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return p
def _row(seed, ev):
    return {"seed": seed, "tests_green": True, "compliant": True,
            "compliance": "5/5", "tests_detail": "1 passed",
            "evidence": [f"e{i}" for i in range(ev)]}
def test_analyze_lists_ev0(tmp_path):
    _tourney(tmp_path, [_row("a", 2), _row("b", 0)])
    out = h_analyze({"seed_root": str(tmp_path)})
    assert out["amend_candidates"] == ["b"] and len(out["table"]) == 2
def test_amend_stamps_and_justifies(tmp_path):
    _tourney(tmp_path, [_row("s1", 0), _row("s2", 3)])
    (tmp_path / "s1").mkdir()
    out = h_amend_seeds({"seeds_root": str(tmp_path), "tournament_dir": str(tmp_path),
                         "bump": "9.9"})
    assert out["bumped"] == ["s1"]
    assert (tmp_path / "s1" / "evidence").is_dir()
    assert (tmp_path / "s1" / "VERSION").read_text().strip() == "9.9"
    assert "evidence" in (tmp_path / "s1" / "AMENDMENTS.jsonl").read_text()
def test_report_match_stop_and_flags(tmp_path):
    aq = tmp_path / "a.jsonl"
    aq.write_text("\n".join([
        json.dumps({"id": "A1", "kind": "A", "status": "done", "title": "t1", "note": "ev1"}),
        json.dumps({"id": "A2", "kind": "A", "status": "done", "title": "t2", "note": ""}),
        json.dumps({"id": "A3", "kind": "A", "status": "open", "title": "t3"})]) + "\n")
    alog = tmp_path / "al.jsonl"
    alog.write_text(json.dumps({"task": "A1"}) + "\n" + json.dumps({"task": "ZX"}) + "\n")
    out = h_report({"a_queue": str(aq), "alog": str(alog),
                    "runs_dir": str(tmp_path), "out": str(tmp_path / "REP.md")})
    assert out["stop"] is False  # open task remains
    assert any("A2" in f for f in out["flags"])  # done minus evidence
    assert any("unknown tasks" in f for f in out["flags"])
    assert (tmp_path / "REP.md").read_text().startswith("# A-REPORT")
def test_report_stop_when_clean(tmp_path):
    aq = tmp_path / "a.jsonl"
    aq.write_text(json.dumps({"id": "A1", "kind": "A", "status": "done",
                              "title": "t", "note": "ev"}) + "\n")
    alog = tmp_path / "al.jsonl"
    alog.write_text(json.dumps({"task": "A1"}) + "\n")
    out = h_report({"a_queue": str(aq), "alog": str(alog),
                    "runs_dir": str(tmp_path), "out": str(tmp_path / "REP.md")})
    assert out["stop"] is True and out["flags"] == []

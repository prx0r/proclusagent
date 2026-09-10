"""SFT export tests: scrub enforced, context never leaks response."""
from predictor.export_sft import build_pairs
def test_pairs_shape_and_scrub():
    sends = [{"session": "s", "title": "T", "proj": "p", "agent": "b",
              "text": "ok", "ts": 1},
             {"session": "s", "title": "T", "proj": "p", "agent": "b",
              "text": "here ghp_" + "C" * 16 + " done", "ts": 2}]
    pairs = build_pairs(sends)
    assert len(pairs) == 2
    assert "ghp_" not in pairs[1]["response"]
    assert pairs[0]["response"] == "ok" and "T" in pairs[1]["context"]
def test_empty_dropped():
    sends = [{"session": "s", "title": "", "proj": "", "agent": "",
              "text": "   ", "ts": 0}]
    assert build_pairs(sends) == []

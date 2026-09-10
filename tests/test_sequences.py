"""Sequence-miner tests: sessions, bigrams, thresholds (synthetic, CI-safe)."""
from predictor.sequences import sessions, bigrams
def rows():
    return [
        {"session": "s1", "shown": ["a", "b"], "picked": 0},
        {"session": "s1", "shown": ["a", "b"], "picked": 1},
        {"session": "s1", "shown": ["a", "b"], "picked": 0},
        {"session": "s1", "shown": ["a", "b"], "picked": 1},
        {"session": "s2", "shown": ["x"], "picked": None, "typed_own": "custom"},
    ]
def test_sessions_split_and_mark_typed():
    s = sessions(rows())
    assert s["s1"] == ["a", "b", "a", "b"] and s["s2"] == ["TYPED"]
def test_bigram_macro_proposal():
    m = bigrams(sessions(rows()), min_n=2, min_conf=0.5)
    assert {"macro": ["a", "b"], "n": 2, "conf": 1.0} in m
def test_thresholds_gate_noise():
    m = bigrams(sessions(rows()), min_n=5)
    assert m == []

"""Joint n-gram tests: backoff order, no-peek, determinism (synthetic)."""
from predictor.ngram import train_predict
def test_repeating_pattern_learned():
    stream = [(None, "a"), ("x", "b")] * 6
    r = train_predict(stream, order=2)
    assert r["acc"] >= 0.7 and r["n"] == 11
def test_empty_and_single():
    assert train_predict([])["n"] == 0
    assert train_predict([(None, "a")])["n"] == 0
def test_deterministic():
    s = [(None, "a"), ("x", "b"), ("y", "a"), ("x", "b")]
    assert train_predict(s) == train_predict(s)

"""Round-2 tests: subcluster grouping + ensemble split protocol (synthetic, CI-safe)."""
from predictor.subcluster import salient, subcluster
from predictor.ensemble import split_eval, predict, _index
def sends():
    return [
        {"session": "s1", "title": "Deploy", "proj": "p", "agent": "b", "text": "ok"},
        {"session": "s1", "title": "Deploy", "proj": "p", "agent": "b", "text": "ok go"},
        {"session": "s1", "title": "Deploy", "proj": "p", "agent": "b", "text": "frobnicate.widgets EST"},
        {"session": "s2", "title": "Fix", "proj": "q", "agent": "b", "text": "ok"},
        {"session": "s2", "title": "Fix", "proj": "q", "agent": "b", "text": "verify it"},
        {"session": "s2", "title": "Fix", "proj": "q", "agent": "b", "text": "frobnicate.widgets EST"},
    ]
def test_salient_skips_stopwords():
    assert salient("verify the deploy now") == ("verify", "deploy")
def test_subcluster_groups():
    g = subcluster(["ok sure", "ok fine", "verify this"])
    assert sum(len(v) for v in g.values()) == 3
def test_split_no_peek_order():
    data = sends()
    r = split_eval(data, weights_list=[(1, 0, 0), (0, 0, 1)])
    assert r["n_train"] == 3 and r["n_test"] == 3
    assert set(r["best"]) == {"len", "cont", "cat"}
def test_split_deterministic():
    assert split_eval(sends()) == split_eval(sends())
def test_predict_uses_train_only():
    data = sends()
    idx = _index(data[:3])
    p = predict(data[5], None, idx, data[:3], (0, 1, 0))
    assert set(p) == {"len", "cont", "cat"}

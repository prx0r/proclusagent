"""Replay tests on synthetic history (no R2 dependency, CI-safe)."""
from predictor.replay import candidates, simulate
def hist():
    return [
        {"session": "s1", "title": "Deploy site", "text": "ok"},
        {"session": "s1", "title": "Deploy site", "text": "ok go on"},
        {"session": "s1", "title": "Deploy site", "text": "how is x?"},
        {"session": "s2", "title": "Fix bug", "proj": "q", "text": "ok"},
        {"session": "s2", "title": "Fix bug", "proj": "q", "text": "verify it now please"},
    ]
def test_candidates_never_include_future(tmp_path):
    h = hist()
    allowed = {"ok"} | {p["text"] for p in h[:2]}  # templates + past only
    c = candidates(h[:2], h[2], ["ok"])
    assert set(c) <= allowed  # nothing leaked from present/future turns
def test_simulate_metrics_and_learning(tmp_path):
    store = str(tmp_path / "c.jsonl")
    r = simulate(hist(), store, ["ok"])
    assert r["n"] == 5 and 0.0 <= r["hit3"] <= 1.0
    assert 0.0 <= r["enter_precision"] <= 1.0
    assert r["level_end"] in ("suggest", "predict", "auto")
    assert r["auto_rate"] >= 0.0
def test_simulate_deterministic(tmp_path):
    kw = dict(store_path=str(tmp_path / "a.jsonl"), templates=["ok"])
    kw2 = dict(store_path=str(tmp_path / "b.jsonl"), templates=["ok"])
    a = simulate(hist(), **kw)
    b = simulate(hist(), **kw2)
    assert {k: v for k, v in a.items() if k != "past"} == \
        {k: v for k, v in b.items() if k != "past"}
def test_resume_past_carries_state(tmp_path):
    store = str(tmp_path / "c.jsonl")
    h = hist()
    r1 = simulate(h[:3], store, ["ok"])
    r2 = simulate(h[3:], store, ["ok"], past=r1["past"])
    assert r2["n"] == 2 and len(r2["past"]) == 5
def test_store_cache_invalidates_on_append(tmp_path):
    from predictor.store import stats
    from predictor.suggest import accept
    p = str(tmp_path / "c.jsonl")
    accept(p, "s", "ctx", ["a", "b"], 0)
    assert stats(p)["turns"] == 1
    accept(p, "s", "ctx", ["a", "b"], 1)
    st = stats(p)
    assert st["turns"] == 2 and st["hit_rate_top1"] == 0.5

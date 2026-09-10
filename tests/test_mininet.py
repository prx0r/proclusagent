"""Mini-net tests: importorskip keeps system-python CI green (needs /tmp/mininet)."""
import pytest
sk = pytest.importorskip("sklearn", reason="needs /tmp/mininet venv")
from predictor.mininet import train_predict, route_sim, ctx_text
def rows():
    base = [
        ("s1", "Deploy site", "ok"), ("s1", "Deploy site", "ok go on"),
        ("s1", "Deploy site", "how is x?"), ("s1", "Deploy site", "ok"),
        ("s2", "Fix bug", "verify it"), ("s2", "Fix bug", "ok"),
        ("s2", "Fix bug", "Build widget now"), ("s2", "Fix bug", "ok thanks"),
    ]
    return [{"session": s, "title": t, "proj": "p", "agent": "b", "text": x}
            for s, t, x in base]
def test_ctx_never_contains_response():
    s = {"title": "T", "proj": "p", "agent": "b", "text": "SECRET-RESPONSE-TEXT"}
    assert "SECRET-RESPONSE-TEXT" not in ctx_text(s, None)
def test_train_predict_ranges():
    r = train_predict(rows()[:6], rows()[6:], hidden=8)
    assert 0.0 <= r["acc"] <= 1.0 and r["n_test"] == 2 and "ack" in r["classes"]
def test_train_deterministic():
    kw = dict(hidden=8)
    assert train_predict(rows()[:6], rows()[6:], **kw)["acc"] == \
        train_predict(rows()[:6], rows()[6:], **kw)["acc"]
def test_route_sim_rates_sum():
    r = train_predict(rows()[:6], rows()[6:], hidden=8)
    sim = route_sim(rows()[6:], r["preds"], rows()[:6])
    assert abs(sim["auto_rate"] + sim["handoff_rate"] - 1.0) < 1e-9
    assert 0.0 <= sim["exact_match_rate"] <= sim["auto_rate"]
def test_scrub_redacts_credentials():
    from predictor.mininet import scrub
    tok = "ghp_" + "A" * 16  # built, never a literal (secret scans read sources too)
    assert "ghp_" not in scrub(f"here {tok} done")
    assert "sk-" not in scrub("key " + "sk-" + "B" * 16 + " ok")
    assert scrub("plain ok go on") == "plain ok go on"

"""Cascade + parallel-stream tests: routing rules, H-delegation pattern, templates safe."""
from predictor.cascade import serve, thresholds, templates
from predictor.suggest import accept
from ham_registry import Registry
def test_buttons_by_default_cold(tmp_path):
    p = tmp_path / "c.jsonl"
    r = serve(["ok", "verify it please now", "Build widget system"], p)
    assert r["route"] == "buttons" and r["top"]["conf"] < 0.9
def test_auto_proceed_only_high_conf_ack(tmp_path):
    p = tmp_path / "c.jsonl"
    for _ in range(30):
        s = serve(["ok"], p)
        accept(p, "s", "ctx", [o["text"] for o in
               __import__("predictor.suggest", fromlist=["suggest"]).suggest(["ok"], p)["options"]], 0)
    r = serve(["ok"], p)
    assert r["route"] == "auto_proceed" and r["intent"] == "proceed"
def test_blast_radius_forces_h_delegate(tmp_path):
    p = tmp_path / "c.jsonl"
    r = serve(["ok"], p, blast_radius="high")
    assert r["route"] == "h_delegate"
def test_creative_goes_h_delegate(tmp_path):
    p = tmp_path / "c.jsonl"
    r = serve(["Build me a whole new trading system today"], p)
    assert r["route"] == "h_delegate"
def test_templates_have_no_secrets():
    import re
    pat = re.compile(r"(ghp_[A-Za-z0-9]{12,}|cfat_|sk-[A-Za-z0-9]{6,})")
    for t in templates()["templates"]:
        assert len(t) < 30 and not pat.search(t)
def test_parallel_stream_h_delegate_unblocks(tmp_path):
    """Your exact vision: H-task waits while easy A-tasks run; approval unlocks."""
    r = Registry(tmp_path / "ham.jsonl")
    h = r.add("H", "creative: design render engine")
    blocked = r.add("A", "implement approved design", blocked_by=[h["id"]])
    easy = r.add("A", "continue evidence backfill")
    assert [t["id"] for t in r.runnable_a()] == [easy["id"]]  # easy runs, hard waits
    r.approve_h(h["id"], "human:owner", "design ok")
    assert set(t["id"] for t in r.runnable_a()) == {easy["id"], blocked["id"]}

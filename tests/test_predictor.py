"""Predictor tests: online updates, ordering, enter-accept, ladder, persistence."""
from predictor.store import log_choice, stats
from predictor.scorer import confidence, score_options
from predictor.suggest import suggest, accept
from predictor.autonomy import level, SUGGEST, PREDICT, AUTO
OPTS = ["how is {t} whats in it?", "verify {t}: run {g}", "deploy {t}"]
def test_confidence_moves_with_clicks():
    c0 = confidence(0.2, 0, 0)
    c3 = confidence(0.2, 3, 3)
    assert c3 > c0 > 0
def test_ordering_learns_favorite(tmp_path):
    p = tmp_path / "c.jsonl"
    for _ in range(5):
        log_choice(p, "s", "ctx", OPTS, 2)
    top = suggest(OPTS, p)["options"][0]["text"]
    assert top == OPTS[2]
def test_enter_accept_is_top_and_logged(tmp_path):
    p = tmp_path / "c.jsonl"
    s = suggest(OPTS, p)
    assert s["default"] == 0
    accept(p, "s", "ctx", s["options"], 0)
    assert stats(p)["hit_rate_top1"] == 1.0
def test_dismiss_and_type_counts_as_turn_not_hit(tmp_path):
    p = tmp_path / "c.jsonl"
    s = suggest(OPTS, p)
    accept(p, "s", "ctx", s["options"], None, typed_own="custom thing")
    st = stats(p)
    assert st["turns"] == 1 and st["hit_rate_top1"] == 0.0
def test_ladder_cold_then_predict_then_auto(tmp_path):
    p = tmp_path / "c.jsonl"
    assert level(p) == SUGGEST
    for i in range(10):
        s = suggest(OPTS, p)
        accept(p, f"s{i}", "ctx", s["options"], 0)
    assert level(p, tau=0.8, min_turns=5) == AUTO
    p2 = tmp_path / "d.jsonl"
    for i in range(10):
        s = suggest(OPTS, p2)
        accept(p2, f"s{i}", "ctx", s["options"], 1 if i % 2 else 0)
    assert level(p2, tau=0.8, min_turns=5) == PREDICT
def test_persistence_roundtrip(tmp_path):
    p = tmp_path / "c.jsonl"
    log_choice(p, "s", "ctx", OPTS, 1)
    assert stats(p)["turns"] == 1

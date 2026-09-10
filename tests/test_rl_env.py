"""RL env tests on synthetic sends (no R2 dependency, CI-safe)."""
from predictor.rl_env import (Env, run, normalize, length_bucket, is_continue,
                              category, context_tokens)
def sends():
    return [
        {"session": "s1", "title": "Deploy site", "proj": "p", "agent": "build", "text": "ok"},
        {"session": "s1", "title": "Deploy site", "proj": "p", "agent": "build", "text": "ok go on"},
        {"session": "s1", "title": "Deploy site", "proj": "p", "agent": "build", "text": "how is x?"},
        {"session": "s2", "title": "Fix bug", "proj": "q", "agent": "build", "text": "ok"},
        {"session": "s2", "title": "Fix bug", "proj": "q", "agent": "build", "text": "verify it"},
    ]
def test_labels():
    assert length_bucket("x" * 10) == "S" and length_bucket("x" * 100) == "M"
    assert is_continue("ok") and not is_continue("Build me a whole new system from scratch today")
    assert category("ok") == "ack" and category("how is x?") == "question"
    assert category("https://a.b") == "paste" and category("verify it") == "review"
def test_no_peek_index_grows():
    env = Env()
    data = sends()
    prev = None
    for s in data:
        before = len(env.index)
        obs = env.observe(dict(s, pos=0), prev)
        assert len(env.index) == before  # observe never learns
        env.update(dict(s, pos=0), prev, obs)
        prev = {"text": s["text"], "fam": category(s["text"])}
    assert len(env.index) == 5
def test_top3_are_real_past_texts():
    env = Env()
    data = sends()
    prev = None
    seen = set()
    for s in data:
        obs = env.observe(dict(s, pos=0), prev)
        for t in obs["top3_texts"]:
            assert t in seen  # only actual past responses, never invented
        env.update(dict(s, pos=0), prev, obs)
        seen.add(s["text"])
        prev = {"text": s["text"], "fam": category(s["text"])}
def test_run_report_ranges():
    rep = run(sends())
    assert rep["n_scored"] == 4  # first turn has empty index
    for h in ("len", "cont", "cat"):
        for m, v in rep["heads"][h].items():
            assert v is None or 0.0 <= v <= 1.0
def test_deterministic():
    assert run(sends()) == run(sends())

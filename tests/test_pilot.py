"""Pilot tests on synthetic WAL-shaped blobs (no R2 dependency, CI-safe)."""
from predictor.pilot import normalize, family_of, parse_wal_sends, evaluate
def blob(rows):
    """rows: [(msg, ses, role, text)] -> WAL-ish bytes with framing noise."""
    out = []
    for msg, ses, role, text in rows:
        out.append(f"\x01{msg}{ses}\x01{{\u201drole\u201d:\u201d{role}\u201d}}".replace("\u201d", '"'))
        out.append(f"\x02prt_X{msg}{ses}\x02{{\"type\":\"text\",\"text\":\"{text}\"}}")
    return "".join(out).encode()
def test_normalize_redacts_paths_numbers():
    assert "<path>" in normalize("check /home/u/x and 5.7G")
    assert normalize("  How  IS ") == "how is"
def test_families():
    assert family_of("how is a jsonl 1 gb whats in it?") == "interrogative"
    assert family_of("DB uploaded (5.7G). Now the rest:") == "ops-directive"
    assert family_of("Build Next.js ereader") == "task-opener"
    assert family_of("Verify foo: run pytest") == "verify"
def test_parse_dedupes_frames():
    b = blob([("msg_A", "ses_1", "user", "Build widget"),
              ("msg_A", "ses_1", "user", "Build widget")])
    sends = parse_wal_sends(b)
    assert len(sends) == 1 and sends[0]["text"] == "Build widget"
def test_evaluate_prefers_session_alpha():
    rows = [("msg_1", "ses_1", "user", "Build alpha"),
            ("msg_2", "ses_1", "user", "Build beta"),
            ("msg_3", "ses_2", "user", "how is gamma?"),
            ("msg_4", "ses_2", "user", "how is delta?")]
    sends = parse_wal_sends(blob(rows))
    assert len(sends) == 4
    r = evaluate(sends)
    assert r["n"] == 4 and r["hit_rate"][1.0] >= r["hit_rate"][0.0]
    assert 0.0 <= r["hit_rate"][0.4] <= 1.0

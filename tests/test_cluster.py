"""Cluster tests: determinism, priority, false-positive guards, real-corpus smoke."""
from predictor.cluster import normalize, signature, name_of, cluster
def test_deterministic():
    assert signature("run all a-tasks and log it all") == signature("run all a-tasks and log it all")
def test_macro_beats_all():
    assert name_of(signature("a-tasks.com")) == "TRIGGER (one-word macro)"
def test_strong_tournament_beats_beauty():
    assert "METHODOLOGY-TOURNAMENT" in name_of(signature("test it as tournaments with hypothesis and falsification, make repo beautiful"))
def test_no_nextjs_false_positive():
    assert "ZOOM-OUT" not in name_of(signature("Build Next.js ereader with modes"))
def test_no_site_false_positive():
    assert "EXPOSE" not in name_of(signature("Upload cleaned texts + site to Cloudflare"))
def test_compound_reports_also():
    from predictor.cluster import load_corpus
    _, detail = cluster(load_corpus("prompts/corpus.jsonl"))
    assert any(detail["p16"]["also"])  # tournament x registry x drain
def test_every_specimen_classified():
    rows = [{"id": f"s{i}", "text": t} for i, t in enumerate([
        "do it ensure you are recording all progress to a-logs",
        "ok document all progress and zoom out what achieved missing",
        "how is a jsonl 1 gb whats in it?",
        "DB uploaded (5.7G). Now the rest:"])]
    groups, _ = cluster(rows)
    assert sum(len(v) for v in groups.values()) == 4
    assert len(groups) >= 3
def test_real_corpus_ten_categories():
    from predictor.cluster import load_corpus
    groups, _ = cluster(load_corpus("prompts/corpus.jsonl"))
    total = sum(len(v) for v in groups.values())
    assert total == 27 and len(groups) >= 10

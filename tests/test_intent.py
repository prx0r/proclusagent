"""Intent-box tests: mapping, session-majority, fallback."""
from predictor.intent import intent_of, session_predict, BOXES
def test_boxes_count():
    assert len(BOXES) == 11
def test_mapping():
    assert intent_of("ok go on") == "ack-proceed"
    assert intent_of("no, redo it") == "neg-redirect"
    assert intent_of("how is x?") == "question"
    assert intent_of("Build widget") == "task-do"
    assert intent_of("https://a.b") == "paste"
    assert intent_of("Review handovers") == "review"
    assert intent_of("xYzQw unknown words here") == "other"
def test_session_majority():
    assert session_predict(["other", "ack-proceed", "ack-proceed"]) == "ack-proceed"
    assert session_predict([]) == "ack-proceed"
def test_session_beats_nothing_but_holds():
    # sustained-intent property: majority of session prefix predicts continuation
    hist = ["task-do", "task-do", "question", "task-do"]
    assert session_predict(hist) == "task-do"

"""Dialog-act tests: rule shapes + precedence (error beats question mark)."""
from predictor.dialog import classify_assistant
def test_confirmation():
    assert classify_assistant("Shall I proceed with the deploy?") == "confirmation"
    assert classify_assistant("Done. Sound good?") == "confirmation"
def test_error():
    assert classify_assistant("Build failed with traceback below") == "error"
    assert classify_assistant("Error: file not found?") == "error"  # error wins over ?
def test_deliverable():
    assert classify_assistant("x" * 600) == "deliverable"
    assert classify_assistant("Here:\n```py\nprint(1)\n```") == "deliverable"
def test_other():
    assert classify_assistant("On it, checking now.") == "other"
    assert classify_assistant("") == "other"

"""Dialog-act classifier for assistant turns: confirmation / error / deliverable / other.

Hypothesis under test: P(user short-ack | confirmation-question) is high enough
to license the continue auto-button where user-history features failed.
Transparent heuristics (no model): confirmation = question shape + confirm-words;
error = failure markers; deliverable = long/producing output; other = rest.
"""
import re
CONFIRM_WORDS = ("confirm", "proceed", "shall i", "should i", "ok?", "ready?",
                 "sound good", "lgtm", "want me to", "shall we", "?")
ERROR_WORDS = ("error", "traceback", "failed", "failure", "exception", "not found",
               "denied", "refused", "timed out", "timeout", "crashed", "broken")
def classify_assistant(text):
    t = (text or "").strip()
    tl = t.lower()
    if any(w in tl for w in ERROR_WORDS):
        return "error"
    if t.endswith("?") or any(w in tl for w in CONFIRM_WORDS):
        return "confirmation"
    if len(t) > 500 or "```" in t:
        return "deliverable"
    return "other"

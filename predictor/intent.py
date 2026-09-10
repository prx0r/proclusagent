"""Intent boxes: 11 data-derived intents + session-coherence prediction. Stdlib.

Measured on 8,497 sends: pairwise transitions are near-independent (lifts
0.88-1.12, markov-1 0.371 vs majority 0.353). Structure lives at SESSION level
(sustained intent), so prediction = current-session majority, not chains.
"""
BOXES = ["ack-proceed", "neg-redirect", "question", "review", "task-do",
         "paste", "pathref", "prose", "continue-thread", "request", "other"]
_SETS = {
 "ack-proceed": {"ok", "yes", "yeah", "yep", "continue", "go", "sure", "proceed",
                 "done", "cool", "alright", "nice", "oh", "bruh", "yess", "yup", "yea"},
 "neg-redirect": {"no", "nope", "idk", "not", "dont", "stop", "never"},
 "question": {"what", "how", "why", "which", "is", "are", "whats", "where", "when", "who"},
 "review": {"review", "check", "verify", "read", "audit", "look"},
 "task-do": {"build", "create", "make", "deploy", "do", "run", "upload", "add", "fix",
             "write", "produce", "generate", "ensure", "migrate", "clone", "push", "test"},
 "prose": {"i", "we", "u", "you", "its", "this", "that", "the", "my"},
 "continue-thread": {"also", "then", "now", "next", "still", "again", "here"},
 "request": {"can", "could", "would", "will", "please"},
 "pathref": {"sanskritree", "blog", "tantraloka"},
}
def intent_of(text):
    import re
    t = (text or "").strip().lower()
    if t.startswith("http"):
        return "paste"
    w = (t.split() or ["?"])
    f = re.sub(r"[^a-z]", "", w[0]) or "?"
    for box, words in _SETS.items():
        if f in words:
            return box
    if "/" in f:
        return "pathref"
    return "other"
def session_predict(session_intents, fallback="ack-proceed"):
    """Current-session majority (the coherence predictor). Empty -> fallback."""
    if not session_intents:
        return fallback
    from collections import Counter
    return Counter(session_intents).most_common(1)[0][0]

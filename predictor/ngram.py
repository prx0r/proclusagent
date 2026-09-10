"""Joint-alphabet sequence prediction: (agent-act, user-intent) streams.

Alphabet per turn: (prev-agent-act, prev-user-intent) -> predict user-intent.
Trigram with backoff (tri -> bi -> uni -> global-majority), ONLINE (update after
each turn, no peeking). Tests whether RICHER states rescue sequences where bare
intent labels failed (markov-1 0.371).
"""
from collections import Counter
def train_predict(stream, order=3):
    """stream: [(agent_act|None, user_intent)]. Returns accuracy + n."""
    ngrams = [Counter() for _ in range(order + 1)]  # index by context length
    hist, hits, tot = [], 0, 0
    for act, intent in stream:
        sym = (act or "-", intent)
        if len(hist) >= 1:
            pred = None
            for k in range(min(order, len(hist)), 0, -1):
                ctx = tuple(hist[-k:])
                cands = {s: c for s, c in ngrams[k].items() if s[:k] == ctx}
                if cands:
                    pred = max(cands, key=lambda s: (cands[s], s[-1]))[-1][1]
                    break
            if pred is None and ngrams[0]:
                pred = ngrams[0].most_common(1)[0][0][-1][1]
            if pred is not None:
                tot += 1
                hits += (pred == intent)
        hist.append(sym)
        for k in range(0, min(order, len(hist)) + 1):
            ngrams[k][tuple(hist[-(k + 1):])] += 1
    return {"acc": round(hits / tot, 4) if tot else 0.0, "n": tot}

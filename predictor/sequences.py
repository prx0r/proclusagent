"""Press sequences -> macro proposals. Stdlib only.

A session's picks form a sequence (picked index resolved to text; typed_own
marked TYPED). Frequent bigrams (A->B, support>=min_n, conf>=min_conf) become
macro proposals: one press that replays both. Texts, never positions (ranking
shifts under learning; positions don't survive it).
"""
from collections import Counter
def sessions(rows):
    grouped = {}
    for r in rows:
        grouped.setdefault(r.get("session", "?"), []).append(r)
    seqs = {}
    for s, rs in grouped.items():
        seq = []
        for r in rs:
            if r.get("picked") is not None:
                shown = r.get("shown", [])
                i = r["picked"]
                seq.append(shown[i] if i < len(shown) else "?")
            elif r.get("typed_own"):
                seq.append("TYPED")
        seqs[s] = seq
    return seqs
def bigrams(seqs, min_n=2, min_conf=0.5):
    pairs, firsts = Counter(), Counter()
    for seq in seqs.values():
        for a in seq:
            firsts[a] += 1
        for a, b in zip(seq, seq[1:]):
            pairs[(a, b)] += 1
    macros = []
    for (a, b), n in pairs.most_common():
        if n < min_n:
            continue
        conf = n / firsts[a]
        if conf >= min_conf:
            macros.append({"macro": [a, b], "n": n, "conf": round(conf, 3)})
    return macros

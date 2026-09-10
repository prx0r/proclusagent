"""Sub-cluster the coarse 'other' bucket by salient tokens. Deterministic, stdlib."""
import re
from collections import Counter
from .rl_env import normalize
STOP = {"the", "a", "an", "to", "and", "or", "of", "in", "on", "for", "is", "it",
        "this", "that", "with", "my", "me", "we", "you", "i", "s", "t", "d"}
def salient(text, n=2):
    toks = [w for w in normalize(text).split()
            if w not in STOP and w not in ("<path>", "<num>") and len(w) > 2]
    return tuple(toks[:n]) or ("?",)
def subcluster(texts):
    """Returns {subkey: [idx]} + top table. Pure function of the texts."""
    groups = {}
    for i, t in enumerate(texts):
        groups.setdefault(salient(t), []).append(i)
    return groups
def table(groups, texts, top=20):
    rows = []
    for key, idxs in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:top]:
        ex = texts[idxs[0]][:70] if idxs else ""
        rows.append({"sub": " ".join(key), "n": len(idxs), "example": ex})
    return rows

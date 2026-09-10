"""Ensemble blender + split validation. Stdlib only.

score(fam) = w_s * P_session + w_k * kNNshare + w_g * P_global.
Split protocol: fit weights on FIRST half (chronological), report on SECOND half
(frozen index from train only — no peeking, no online update during test).
"""
import itertools
from collections import Counter
from .rl_env import tokens, jaccard, category, length_bucket, is_continue
def _label(send, head):
    if head == "cat":
        return category(send["text"])
    if head == "len":
        return length_bucket(send["text"])
    return is_continue(send["text"])
def _ctoks(send, prev):
    toks = set(send.get("title", "").lower().split())
    toks.add("proj:" + (send.get("proj") or "?"))
    if prev:
        toks |= {("prev:" + w) for w in list(tokens(prev["text"]))[:12]}
    return toks
def _index(rows):
    idx, sess = [], {}
    for s in rows:
        ct = _ctoks(s, None)
        idx.append((ct, s))
        sess.setdefault(s["session"], []).append(s)
    return idx
def _knn_share(ct, idx, head, k=5):
    scored = sorted(((jaccard(ct, c), s) for c, s in idx if jaccard(ct, c) > 0),
                    key=lambda t: -t[0])[:k]
    if not scored:
        return {}
    votes = Counter(_label(s, head) for _, s in scored)
    tot = sum(votes.values())
    return {l: v / tot for l, v in votes.items()}
def _dist(rows, head, ses=None):
    pool = [r for r in rows if ses is None or r["session"] == ses]
    c = Counter(_label(r, head) for r in pool)
    tot = sum(c.values()) or 1
    return {l: v / tot for l, v in c.items()}
def predict(send, prev, train_idx, train_rows, weights, k=5):
    ct = _ctoks(send, prev)
    out = {}
    for head in ("len", "cont", "cat"):
        ks = _knn_share(ct, train_idx, head, k)
        gs = _dist(train_rows, head)
        ss = _dist(train_rows, head, send["session"])
        ws, wk, wg = weights
        cands = set(ks) | set(gs) | set(ss)
        if not cands:
            out[head] = None
            continue
        out[head] = max(cands, key=lambda l: ws * ss.get(l, 0) + wk * ks.get(l, 0) +
                        wg * gs.get(l, 0))
    return out
def cross_eval(train_sends, test_sends, weights_list=None, k=5):
    """Train on one box, test on another: true generalization, no shared sessions.
    Same frozen-index protocol as split_eval (no peeking, no online update)."""
    from collections import defaultdict
    train_idx = _index(train_sends)
    inv = defaultdict(set)
    for i, (ct, _) in enumerate(train_idx):
        for tok in ct:
            inv[tok].add(i)
    if weights_list is None:
        weights_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0.4, 0.4, 0.2)]
    gs = {h: _dist(train_sends, h) for h in ("len", "cont", "cat")}
    res = {}
    for w in weights_list:
        hits = {h: [0, 0] for h in ("len", "cont", "cat")}
        for s in test_sends:
            ct = _ctoks(s, None)
            cand = set()
            for tok in ct:
                cand |= inv.get(tok, set())
            scored = {}
            for h in ("len", "cont", "cat"):
                sims = sorted(((jaccard(ct, train_idx[i][0]), i) for i in cand),
                              key=lambda t: -t[0])[:k]
                votes = Counter(_label(train_sends[i], h) for _, i in sims)
                tot = sum(votes.values()) or 1
                scored[h] = {l: v / tot for l, v in votes.items()}
            ss = {h: _dist(train_sends, h, s["session"]) for h in ("len", "cont", "cat")}
            for h in hits:
                ws, wk, wg = w
                cands = set(scored[h]) | set(gs[h]) | set(ss[h])
                if not cands:
                    continue
                pred = max(cands, key=lambda l: ws * ss[h].get(l, 0) + wk * scored[h].get(l, 0) +
                           wg * gs[h].get(l, 0))
                hits[h][0] += (pred == _label(s, h))
                hits[h][1] += 1
        res[str(w)] = {h: round(v[0] / v[1], 4) if v[1] else None for h, v in hits.items()}
    return {"n_train": len(train_sends), "n_test": len(test_sends), "grid": res}
def split_eval(sends, weights_list=None, k=5):
    from collections import defaultdict
    mid = len(sends) // 2
    train, test = sends[:mid], sends[mid:]
    train_ct = [_ctoks(s, None) for s in train]
    inv = defaultdict(set)
    for i, ct in enumerate(train_ct):
        for tok in ct:
            inv[tok].add(i)
    if weights_list is None:
        weights_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0.4, 0.4, 0.2),
                        (0.6, 0.3, 0.1), (0.34, 0.33, 0.33)]
    gs = {h: _dist(train, h) for h in ("len", "cont", "cat")}
    ss_cache = {}
    sigs = []  # per-test-send base signals, computed once
    prev = None
    for s in test:
        ct = _ctoks(s, prev)
        cand = set()
        for tok in ct:
            cand |= inv.get(tok, set())
        scored = {}
        for h in ("len", "cont", "cat"):
            sims = sorted(((jaccard(ct, train_ct[i]), i) for i in cand),
                          key=lambda t: -t[0])[:k]
            votes = Counter(_label(train[i], h) for _, i in sims)
            tot = sum(votes.values()) or 1
            scored[h] = {l: v / tot for l, v in votes.items()}
        if s["session"] not in ss_cache:
            ss_cache[s["session"]] = {h: _dist(train, h, s["session"])
                                      for h in ("len", "cont", "cat")}
        sigs.append((s, scored, gs, ss_cache[s["session"]]))
        prev = s
    res = {}
    for w in weights_list:
        hits = {h: [0, 0] for h in ("len", "cont", "cat")}
        for s, ks, gs, ss in sigs:
            for h in hits:
                ws, wk, wg = w
                cands = set(ks[h]) | set(gs[h]) | set(ss[h])
                if not cands:
                    continue
                pred = max(cands, key=lambda l: ws * ss[h].get(l, 0) + wk * ks[h].get(l, 0) +
                           wg * gs[h].get(l, 0))
                hits[h][0] += (pred == _label(s, h))
                hits[h][1] += 1
        res[str(w)] = {h: round(v[0] / v[1], 4) if v[1] else None for h, v in hits.items()}
    best = {}
    for h in ("len", "cont", "cat"):
        b = max(weights_list, key=lambda w: (res[str(w)][h] or -1))
        best[h] = {"weights": list(b), "acc": res[str(b)][h]}
    return {"n_train": len(train), "n_test": len(test), "grid": res, "best": best}

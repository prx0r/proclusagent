"""Offline RL env over real prompt sends: 3 predicted responses + 3 difficulty heads.

Heads: H1 length bucket S/M/L (easy) · H2 continue? (binary: ack-forward vs
substantive) · H3 coarse category (broad, data-driven from first-token groups).
Online chronological protocol (no future peek): score turn i on index of <i,
then update (bandit-style). kNN (Jaccard over context tokens, k=5) vs majority,
random, global-prior, session-prior baselines. Stdlib only.
"""
import json
import re
from collections import Counter
ACK = {"ok", "yes", "yeah", "yep", "continue", "proceed", "go", "great", "sure",
       "perfect", "done", "cool", "alright", "nice", "yess", "yup"}
NEG = {"no", "nope", "idk", "not", "dont", "stop"}
QW = {"what", "how", "why", "which", "is", "are", "can", "does", "did", "should", "where"}
REVIEW = {"review", "check", "verify", "look", "audit", "read"}
TASK = {"build", "create", "make", "deploy", "upload", "add", "fix", "update", "run",
        "write", "split", "migrate", "clone", "delete", "move", "test"}
def normalize(text):
    t = text.lower()
    t = re.sub(r"/[\w./~-]+", " <path>", t)
    t = re.sub(r"\b\d+(\.\d+)?[gmkb]?\b", " <num>", t)
    return re.sub(r"\s+", " ", t).strip()
def tokens(text):
    return set(normalize(text).split())
def length_bucket(text):
    n = len(text)
    return "S" if n < 50 else ("M" if n < 300 else "L")
def is_continue(text):
    w = normalize(text).split()
    return bool(w) and w[0] in ACK and len(text) < 80
def category(text):
    t = normalize(text)
    if t.startswith("http"):
        return "paste"
    w = t.split()
    f = w[0] if w else "?"
    if f in ACK:
        return "ack"
    if f in NEG:
        return "neg"
    if f in QW:
        return "question"
    if f in REVIEW:
        return "review"
    if f in TASK:
        return "task"
    if "/" in t[:24]:
        return "pathref"
    return "other"
def context_tokens(send, prev):
    toks = set(send.get("title", "").lower().split())
    toks.add("proj:" + (send.get("proj") or "?"))
    toks.add("agent:" + (send.get("agent") or "?"))
    if prev:
        toks |= {("prev:" + w) for w in list(tokens(prev["text"]))[:12]}
        toks.add("prevfam:" + prev["fam"])
    toks.add("turnpos:" + ("early" if send.get("pos", 0) < 5 else "late"))
    return toks
def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0
class Env:
    """Online env. observe() scores heads + top-3 retrieved actual responses,
    then update() indexes the true send (bandit update, no peeking)."""
    def __init__(self, k=5, seed=7):
        self.k = k
        self.rng_state = seed
        self.index = []  # (ctoks, fam, length, cont, text)
        self.fam_counts = Counter()
        self.sess_fams = {}
        self.stats = {h: {"knn": [0, 0], "majority": [0, 0], "random": [0, 0],
                           "global": [0, 0], "session": [0, 0]} for h in ("len", "cont", "cat")}
        self.hits3 = [0, 0]
    def _rand(self, n):
        self.rng_state = (1103515245 * self.rng_state + 12345) % 2**31
        return self.rng_state % n
    def observe(self, send, prev):
        ct = context_tokens(send, prev)
        scored = sorted(((jaccard(ct, c), i) for i, (c, _, _, _, _) in enumerate(self.index)
                         if jaccard(ct, c) > 0), reverse=True)[:self.k] if self.index else []
        top3 = [self.index[i] for _, i in scored[:3]]
        pred3 = [t[4] for t in top3]
        fam3 = {t[1] for t in top3}
        maj = {h: self._majority(h) for h in ("len", "cont", "cat")}
        out = {"top3_texts": pred3, "fam_hit3": None, "heads": {}}
        if self.index:
            true_fam = category(send["text"])
            out["fam_hit3"] = true_fam in fam3
        for h, true, kpred in (
                ("len", length_bucket(send["text"]), self._knn_vote(scored, 2)),
                ("cont", is_continue(send["text"]), self._knn_vote(scored, 3)),
                ("cat", category(send["text"]), self._knn_vote(scored, 1))):
            out["heads"][h] = {"true": true, "knn": kpred, "majority": maj[h],
                               "random": self._rand_label(h),
                               "global": self._prior_label(h, None),
                               "session": self._prior_label(h, send["session"])}
        return out
    def _knn_vote(self, scored, pos):
        if not scored:
            return None
        return Counter(self.index[i][pos] for _, i in scored).most_common(1)[0][0]
    def _majority(self, h):
        pos = {"len": 2, "cont": 3, "cat": 1}[h]
        if not self.index:
            return None
        return Counter(r[pos] for r in self.index).most_common(1)[0][0]
    def _rand_label(self, h):
        pool = {"len": ["S", "M", "L"], "cont": [True, False],
                "cat": ["ack", "neg", "question", "review", "task", "paste", "pathref", "other"]}[h]
        return pool[self._rand(len(pool))]
    def _prior_label(self, h, ses):
        pos = {"len": 2, "cont": 3, "cat": 1}[h]
        if ses and ses in self.sess_fams and h == "cat":
            c = self.sess_fams[ses]
            if c:
                return c.most_common(1)[0][0]
        return self._majority(h)
    def update(self, send, prev, obs):
        fam = category(send["text"])
        lb = length_bucket(send["text"])
        co = is_continue(send["text"])
        self.index.append((context_tokens(send, prev), fam, lb, co, send["text"]))
        self.fam_counts[fam] += 1
        self.sess_fams.setdefault(send["session"], Counter())[fam] += 1
        if obs["fam_hit3"] is not None:
            self.hits3[0] += obs["fam_hit3"]
            self.hits3[1] += 1
        for h in ("len", "cont", "cat"):
            for m in ("knn", "majority", "random", "global", "session"):
                p = obs["heads"][h][m]
                t = obs["heads"][h]["true"]
                if p is not None:
                    self.stats[h][m][0] += (p == t)
                    self.stats[h][m][1] += 1
    def report(self):
        acc = {h: {m: round(v[0] / v[1], 4) if v[1] else None for m, v in d.items()}
               for h, d in self.stats.items()}
        return {"n_scored": self.hits3[1], "index": len(self.index),
                "fam_hit3": round(self.hits3[0] / self.hits3[1], 4) if self.hits3[1] else None,
                "heads": acc, "fam_dist": dict(self.fam_counts.most_common())}
def run(sends, k=5):
    env = Env(k=k)
    prev_by_ses, pos_by_ses = {}, {}
    for s in sends:
        s = dict(s)
        s["pos"] = pos_by_ses.get(s["session"], 0)
        prev = prev_by_ses.get(s["session"])
        obs = env.observe(s, prev)
        env.update(s, prev, obs)
        prev_by_ses[s["session"]] = {"text": s["text"], "fam": category(s["text"])}
        pos_by_ses[s["session"]] = s["pos"] + 1
    return env.report()

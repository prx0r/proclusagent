"""Pilot: sample WAL -> sends -> families -> retrieval + interpolation eval. Stdlib.

Smart-Compose pattern: P(fam) = alpha * P_session(fam) + (1-alpha) * P_global(fam).
Leave-one-out over sends; dedupe by message_id (WAL repeats frames ~30x).
"""
import json
import re
from collections import Counter
FAMILIES = [
    ("interrogative", re.compile(r"^(how|what|why|which|is|are|can|does)\b")),
    ("ops-directive", re.compile(r"(uploaded|now the rest|clone[sd]?|finish|continue)\b")),
    ("task-opener", re.compile(r"^(build|deploy|create|upload|make|split|migrate)\b")),
    ("verify", re.compile(r"^(verify|check|re-verify|confirm|review)\b")),
    ("escalate", re.compile(r"^(blocked|approve|need|stuck)\b")),
]
def normalize(text):
    t = text.lower()
    t = re.sub(r"/[\w./~-]+", " <path>", t)
    t = re.sub(r"\b\d+(\.\d+)?[gmkb]?\b", " <num>", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t
def family_of(text):
    t = normalize(text)
    for fam, rx in FAMILIES:
        if rx.search(t):
            return fam
    return "other"
def parse_wal_sends(blob):
    """Exact msgID join. Returns [{msg, ses, text}] deduped by msg id."""
    wal = blob.decode("utf-8", errors="ignore") if isinstance(blob, bytes) else blob
    msgrole, msgses = {}, {}
    for m in re.finditer(r"(msg_[A-Za-z0-9]+)", wal):
        seg = wal[m.start():m.start() + 700]
        r = re.search(r"\"role\":\"(user|assistant)\"", seg)
        s = re.search(r"(ses_[A-Za-z0-9]+)", seg)
        if r:
            msgrole[m.group(1)] = r.group(1)
        if s:
            msgses[m.group(1)] = s.group(1)
    sends = {}
    for m in re.finditer(r"prt_[A-Za-z0-9]+", wal):
        head = wal[m.start():m.start() + 300]
        mm = re.search(r"(msg_[A-Za-z0-9]+)", head)
        if not mm or msgrole.get(mm.group(1)) != "user":
            continue
        jt = head.find("\"type\":\"text\",\"text\":\"")
        if jt < 0:
            continue
        j = m.start() + jt + len("\"type\":\"text\",\"text\":\"")
        out = []
        while j < len(wal):
            c = wal[j]
            if c == "\\":
                out.append(wal[j:j + 2]); j += 2; continue
            if c == "\"":
                break
            out.append(c); j += 1
            if len(out) > 6000:
                break
        try:
            t = json.loads("\"" + "".join(out) + "\"")
        except Exception:
            continue
        if t.strip():
            sends[mm.group(1)] = {"msg": mm.group(1),
                                  "ses": msgses.get(mm.group(1), "?"), "text": t}
    return list(sends.values())
def evaluate(sends, alphas=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)):
    """Leave-one-out family prediction. Returns {alpha: hit_rate} + detail."""
    fams = [family_of(s["text"]) for s in sends]
    res = {}
    for a in alphas:
        hits = 0
        for i, s in enumerate(sends):
            glob = Counter(f for j, f in enumerate(fams) if j != i)
            sess = Counter(f for j, f in enumerate(fams)
                           if j != i and sends[j]["ses"] == s["ses"])
            tot_g = sum(glob.values()) or 1
            tot_s = sum(sess.values()) or 1
            cands = set(glob) | set(sess)
            best = max(cands, key=lambda f: a * sess.get(f, 0) / tot_s +
                       (1 - a) * glob.get(f, 0) / tot_g)
            hits += (best == fams[i])
        res[a] = round(hits / len(sends), 4) if sends else 0.0
    return {"n": len(sends), "families": Counter(fams), "hit_rate": res}

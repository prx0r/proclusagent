"""Replay simulator: history stands in for the live user. Stdlib only.

Per turn (chronological, no peeking): candidates (templates + retrieved past) ->
cascade.serve -> history reveals actual -> log press-or-type outcome -> update.
Reports: family-hit@3, enter-precision, auto rate/precision, calibration bins,
learning curves per 500-turn window, autonomy level. Store persists on disk so
runs are resumable (chunked execution over 8.5k turns).
"""
from .cascade import serve
from .rl_env import normalize, category, jaccard
from .autonomy import level
def candidates(past, send, templates, k=5, _ptoks=None):
    ct = set(normalize(send.get("title", "")).split())
    if _ptoks is None:
        _ptoks = [set(normalize(p["text"]).split()) for p in past]
    scored = []
    for toks, p in zip(_ptoks, past):
        sim = jaccard(ct, toks)
        if sim > 0:
            scored.append((sim, p["text"]))
    scored.sort(key=lambda t: -t[0])
    seen, retr = set(), []
    for _, t in scored:
        if t not in seen:
            seen.add(t)
            retr.append(t)
        if len(retr) >= k:
            break
    out, seen = [], set()
    for t in templates + retr:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out
def _optxt(o):
    return o.get("text") if isinstance(o, dict) else o
def simulate(sends, store_path, templates, past=None):
    from .suggest import accept
    past = list(past or [])
    ptoks = [set(normalize(p["text"]).split()) for p in past]
    hits, enters, autos, calib = [], [], [], {}
    for s in sends:
        cands = candidates(past, s, templates, _ptoks=ptoks)
        r = serve(cands, store_path, priors=None, blast_radius="low")
        actual_fam = category(s["text"])
        opts = r.get("options", [r.get("top", {})])[:3]
        hit3 = any(_optxt(o) and category(_optxt(o)) == actual_fam for o in opts)
        top_fam = category(_optxt(r["top"])) if r.get("top") else "?"
        enter_ok = (top_fam == actual_fam)
        if r["route"] == "auto_proceed":
            autos.append(1 if enter_ok else 0)
        shown = [_optxt(o) for o in opts]
        if enter_ok:
            accept(store_path, s["session"], "replay", shown, 0)
        else:
            accept(store_path, s["session"], "replay", shown, None,
                   typed_own=s["text"][:200])
        b = round((r["top"]["conf"] if r.get("top") else 0.0), 1)
        cb = calib.setdefault(b, [0, 0])
        cb[0] += enter_ok
        cb[1] += 1
        hits.append(1 if hit3 else 0)
        enters.append(1 if enter_ok else 0)
        past.append(s)
        ptoks.append(set(normalize(s["text"]).split()))
    def windows(xs, w=500):
        return [round(sum(xs[i:i + w]) / len(xs[i:i + w]), 4)
                for i in range(0, len(xs), w)]
    return {"n": len(sends),
            "hit3": round(sum(hits) / len(hits), 4),
            "enter_precision": round(sum(enters) / len(enters), 4),
            "hit3_curve": windows(hits), "enter_curve": windows(enters),
            "auto_rate": round(len(autos) / len(sends), 4),
            "auto_precision": round(sum(autos) / len(autos), 4) if autos else None,
            "auto_n": len(autos),
            "calibration": {str(k): round(v[0] / v[1], 3) for k, v in sorted(calib.items())},
            "level_end": level(store_path),
            "past": past}

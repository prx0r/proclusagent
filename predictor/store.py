"""Choice log: every shown-set + pick persisted. Shapes only, never secrets. Stdlib."""
import json
import os
import time
from pathlib import Path
_CACHE = {}
def _cache_key(path):
    try:
        st = os.stat(path)
        return (str(path), st.st_mtime_ns, st.st_size)
    except OSError:
        return (str(path), None, None)
def log_choice(path, session, context, shown, picked_idx, typed_own=None):
    """shown: list[str] (or {text}), picked_idx: int|None, typed_own: str|None."""
    rec = {"ts": time.time(), "session": session, "context": context,
           "shown": shown, "picked": picked_idx, "typed_own": typed_own}
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec
def read_log(path):
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out
def stats(path):
    key = _cache_key(path)
    hit = _CACHE.get(key)
    if hit is not None:
        return hit
    rows = read_log(path)
    per = {}
    accepts_top = 0
    for r in rows:
        if r.get("picked") == 0:
            accepts_top += 1
        for i, s in enumerate(r.get("shown", [])):
            k = s if isinstance(s, str) else s.get("text", "")
            d = per.setdefault(k, {"shown": 0, "clicked": 0})
            d["shown"] += 1
            if r.get("picked") == i:
                d["clicked"] += 1
    res = {"turns": len(rows), "accepts_top": accepts_top,
           "hit_rate_top1": (accepts_top / len(rows)) if rows else 0.0,
           "per_option": per}
    if len(_CACHE) > 4:
        _CACHE.pop(next(iter(_CACHE)))
    _CACHE[key] = res
    return res

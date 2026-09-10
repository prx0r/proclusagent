"""Autonomy ladder, HG-DAgger style: level follows calibrated hit-rate.

SUGGEST (show 3) -> PREDICT (top pick pre-highlighted) -> AUTO (enter runs it).
tau learned from YOUR accept log (default 0.8, min_turns guards cold start).
This engine REPORTS the level; execution policy lives in controller/driver.py
and still needs H-approval to run anything real. Engine never auto-executes.
"""
from .store import stats
SUGGEST, PREDICT, AUTO = "suggest", "predict", "auto"
def level(store_path, tau=0.8, min_turns=20):
    st = stats(store_path)
    if st["turns"] < min_turns:
        return SUGGEST
    if st["hit_rate_top1"] >= tau:
        return AUTO
    if st["hit_rate_top1"] >= tau / 2:
        return PREDICT
    return SUGGEST

"""Suggest bar engine: top-k scored options, Enter accepts options[0]. Stdlib only.

Keybinding contract (for the opencode TUI layer): Enter = accept default (top),
1/2/3 = pick, any typing = dismiss + typed_own. Every outcome must call
store.log_choice — the log IS the training data.
"""
from .scorer import score_options, family_stats, family_confidence, confidence, FAMILY_PRIORS
from .store import stats, log_choice
def suggest(candidates, store_path, top_k=3, priors=None):
    scored = score_options(candidates, stats(store_path)["per_option"], priors)
    return {"options": scored[:top_k], "default": 0}
def suggest_typed(candidates, store_path, type_tag, top_k=3, priors=None):
    """User clicked a TYPE button first: filter candidates to that family, then
    score. The tag is a free supervised label (no family inference needed)."""
    from .rl_env import category as _cat
    kept = [c for c in candidates
            if _cat(c if isinstance(c, str) else c["text"]) == type_tag]
    return suggest(kept or candidates, store_path, top_k, priors)
def suggest_family(candidates, store_path, top_k=3, priors=None, alpha=2.0):
    """Rank texts by their FAMILY confidence (dense), tiebreak by text conf.
    Same {options, default} shape. Family conf rides on aggregate counts, so
    mature families can actually reach high confidence (fixes τ-unreachability)."""
    st = stats(store_path)
    fams = family_stats(st["per_option"])
    per = st["per_option"]
    scored = []
    for c in candidates:
        text = c if isinstance(c, str) else c["text"]
        fam = None if isinstance(c, str) else c.get("family")
        if fam is None:
            from .rl_env import category as _cat
            fam = _cat(text)
        prior = (priors or {}).get(text, FAMILY_PRIORS.get(fam, 0.2))
        d = per.get(text, {"shown": 0, "clicked": 0})
        fc = family_confidence(fams.get(fam, {"shown": 0, "clicked": 0}), prior, alpha)
        scored.append({"text": text, "conf": fc, "family": fam,
                       "tiebreak": confidence(prior, d["shown"], d["clicked"])})
    scored.sort(key=lambda x: (-x["conf"], -x["tiebreak"]))
    return {"options": [{"text": o["text"], "conf": o["conf"]} for o in scored[:top_k]],
            "default": 0}
def accept(store_path, session, context, options, picked_idx, typed_own=None,
           type_tag=None):
    """Log one turn. picked_idx None + typed_own set = dismissed-and-typed."""
    return log_choice(store_path, session, context,
                      [o["text"] if isinstance(o, dict) else o for o in options],
                      picked_idx, typed_own, type_tag)

"""Suggest bar engine: top-k scored options, Enter accepts options[0]. Stdlib only.

Keybinding contract (for the opencode TUI layer): Enter = accept default (top),
1/2/3 = pick, any typing = dismiss + typed_own. Every outcome must call
store.log_choice — the log IS the training data.
"""
from .scorer import score_options
from .store import stats, log_choice
def suggest(candidates, store_path, top_k=3, priors=None):
    scored = score_options(candidates, stats(store_path)["per_option"], priors)
    return {"options": scored[:top_k], "default": 0}
def accept(store_path, session, context, options, picked_idx, typed_own=None):
    """Log one turn. picked_idx None + typed_own set = dismissed-and-typed."""
    return log_choice(store_path, session, context,
                      [o["text"] if isinstance(o, dict) else o for o in options],
                      picked_idx, typed_own)

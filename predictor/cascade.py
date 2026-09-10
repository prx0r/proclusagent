"""Cascade serve path: intent -> route. Stdlib only, pure functions (no side effects).

Routes: auto_proceed (easy intent, conf >= tau, low blast radius) | buttons
(show top options, Enter accepts) | h_delegate (creative/hard: proposal for an
H-task while easy work continues; the DRIVER appends it, never this module).
Key correction from data: auto executes the INTENT (proceed signal), not a
verbatim string (top exact template covers only ~2% of turns).
"""
import json
from pathlib import Path
from .scorer import score_options, FAMILY_PRIORS
from .suggest import suggest
_HERE = Path(__file__).resolve().parent
def load_json(name, default):
    p = _HERE / name
    try:
        return json.loads(p.read_text())
    except Exception:
        return default
def thresholds():
    return load_json("thresholds.json", {"tau_auto": 0.9, "tau_buttons": 0.5})
def templates():
    return load_json("ack_templates.json", {"templates": ["ok"]})
def serve(candidates, store_path, priors=None, blast_radius="low", rank_by="text"):
    """candidates: list[str]. Returns routing decision with confidence.
    rank_by: "text" (exact-text conf) or "family" (dense family conf)."""
    from .suggest import suggest_family
    th = thresholds()
    rank_fn = suggest_family if rank_by == "family" else suggest
    s = rank_fn(candidates, store_path, top_k=3, priors=priors)
    top = s["options"][0] if s["options"] else {"text": "", "conf": 0.0}
    fam = _family_of(top["text"])
    if blast_radius != "low":
        return {"route": "h_delegate", "top": top, "family": fam,
                "reason": "blast radius not low"}
    if fam in ("task", "question") and top["conf"] < 0.95:
        return {"route": "h_delegate", "top": top, "family": fam,
                "reason": "creative/complex intent below auto bar"}
    if top["conf"] >= th["tau_auto"] and fam in ("ack",):
        return {"route": "auto_proceed", "top": top, "family": fam,
                "intent": "proceed", "template": templates()["templates"][0]}
    if top["conf"] >= th["tau_buttons"]:
        return {"route": "buttons", "top": top, "family": fam,
                "options": s["options"]}
    return {"route": "buttons", "top": top, "family": fam,
            "options": s["options"], "reason": "low confidence, show all"}
def _family_of(text):
    from .rl_env import category
    return category(text)

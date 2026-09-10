"""Continue intent: variant vocab + licensing policy. Stdlib only.

Data (8,497 sends): short-ack rate 0.16 (1,359); top variants 'continue' 52,
'yes' 51, 'go' 18; 152 distinct short-ack texts (long tail); Markov history
fails (prev-ack -> next-ack precision 0.195 vs 0.16 base — acks ALTERNATE with
substance, they don't cluster); kNN ~= base rate. Policy: auto_proceed ONLY
when measured precision >= TAU (default 0.9) at coverage >= MIN_COV (0.05).
On current numbers the gate stays CLOSED (buttons only) — encoded, not vibed.
"""
VARIANTS = ("continue", "yes", "go", "yep", "yeah", "proceed", "sure", "done",
            "cool", "ok")
TAU_PRECISION = 0.9
MIN_COV = 0.05
def is_variant(text):
    return (text or "").strip().lower() in VARIANTS
def licensed(precision, coverage, tau=TAU_PRECISION, min_cov=MIN_COV):
    """Gate: auto-send licensed only with measured precision + coverage."""
    if precision is None or coverage is None:
        return False
    return precision >= tau and coverage >= min_cov
def decide(predicted_continue, precision, coverage, blast_radius="low"):
    if blast_radius != "low":
        return "h_delegate"
    if predicted_continue and licensed(precision, coverage):
        return "auto_proceed"
    return "buttons"

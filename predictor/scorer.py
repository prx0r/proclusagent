"""Confidence per option: model prior blended with empirical CTR, online updated.

conf = (clicked + alpha * prior) / (shown + alpha): with no data the prior rules;
every logged choice moves it. Laplace alpha keeps cold options explorable.
Family priors seeded from WAL mining (relative frequencies, shapes only).
"""
FAMILY_PRIORS = {"interrogative": 0.30, "ops-directive": 0.45,
                 "task-opener": 0.35, "verify": 0.40, "escalate": 0.15}
def confidence(prior=0.2, shown=0, clicked=0, alpha=2.0):
    return round((clicked + alpha * prior) / (shown + alpha), 4)
def score_options(candidates, per_option, priors=None, alpha=2.0):
    """candidates: list[str] (or {text, family}). Returns [{text, conf}] desc."""
    out = []
    for c in candidates:
        text = c if isinstance(c, str) else c["text"]
        fam = None if isinstance(c, str) else c.get("family")
        prior = (priors or {}).get(text, FAMILY_PRIORS.get(fam, 0.2))
        d = per_option.get(text, {"shown": 0, "clicked": 0})
        out.append({"text": text, "conf": confidence(prior, d["shown"], d["clicked"], alpha)})
    out.sort(key=lambda x: -x["conf"])
    return out

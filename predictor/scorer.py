"""Confidence per option: model prior blended with empirical CTR, online updated.

conf = (clicked + alpha * prior) / (shown + alpha): with no data the prior rules;
every logged choice moves it. Laplace alpha keeps cold options explorable.
Family priors seeded from WAL mining (relative frequencies, shapes only).
"""
FAMILY_PRIORS = {"interrogative": 0.30, "ops-directive": 0.45,
                 "task-opener": 0.35, "verify": 0.40, "escalate": 0.15}
def confidence(prior=0.2, shown=0, clicked=0, alpha=2.0):
    return round((clicked + alpha * prior) / (shown + alpha), 4)
def hconfidence(fam_posterior, shown=0, clicked=0, m=8.0):
    """Hierarchical shrinkage (HEB-lite; cf. HEB-NB, McCallum shrinkage).

    conf = lam * instance_posterior + (1 - lam) * fam_posterior,
    lam = shown / (shown + m): thin texts shrink to their dense family,
    data-rich texts stand alone. m = concentration (default: median per-text
    count scale); full Type-II ML fitting of m is the gated next step.
    Fixes flat-Laplace non-vanishing bias on high-cardinality sparse units.
    """
    lam = shown / (shown + m) if (shown + m) > 0 else 0.0
    inst = (clicked / shown) if shown else fam_posterior
    return round(lam * inst + (1 - lam) * fam_posterior, 4)
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
def family_stats(per_option, family_of=None):
    """Aggregate shown/clicked by family (dense counts for thin texts)."""
    if family_of is None:
        from .rl_env import category as family_of
    agg = {}
    for text, d in per_option.items():
        f = family_of(text)
        a = agg.setdefault(f, {"shown": 0, "clicked": 0})
        a["shown"] += d.get("shown", 0)
        a["clicked"] += d.get("clicked", 0)
    return agg
def family_confidence(fam_posterior_counts, prior=0.2, alpha=2.0):
    """Laplace posterior over a family's aggregate counts."""
    s, c = fam_posterior_counts.get("shown", 0), fam_posterior_counts.get("clicked", 0)
    return round((c + alpha * prior) / (s + alpha), 4)

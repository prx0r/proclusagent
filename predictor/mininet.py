"""Mini-net response-type classifier + template/LLM router. Needs /tmp/mininet venv
(sklearn+numpy, system python untouched). Stdlib fallback: rule map in rl_env.

Input = situation ONLY (title + prev send + project/agent/position) — never the
response itself. Labels = coarse families. Router: pred ack → top exact ack
template; else → LLM handoff (dry-run marker here; live handoff needs H4/M1).

Incident rule (2026-09-10): a live-format credential was found in training
contexts. scrub() MUST run on any text before training/export — committed code
must never see raw credentials.
"""
import re
CRED = re.compile(r"(ghp_[A-Za-z0-9]{4,}|cfat_[A-Za-z0-9_/-]{4,}|sk-[A-Za-z0-9]{6,}"
                  # split literal below: the source must not itself match secret scans
                  r"|AKIA[0-9A-Z]{10,}|-----BEGIN " + ".*PRIVA" + "TE KEY-----)")
def scrub(text):
    return CRED.sub("<cred>", text or "")
CTX_TEMPLATE = "title:{title} prev:{prev} proj:{proj} agent:{agent} pos:{pos}"
def ctx_text(send, prev):
    prev_t = prev["text"] if prev else ""
    pos = "early" if send.get("pos", 0) < 5 else "late"
    return CTX_TEMPLATE.format(title=send.get("title", ""), prev=prev_t,
                               proj=send.get("proj", ""), agent=send.get("agent", ""),
                               pos=pos)
def train_predict(train_rows, test_rows, hidden=64, seed=7):
    from sklearn.feature_extraction.text import HashingVectorizer
    from sklearn.neural_network import MLPClassifier
    from .rl_env import category
    vec = HashingVectorizer(n_features=2**12, ngram_range=(1, 2), alternate_sign=False)
    prev, Xtr_txt, ytr = None, [], []
    for s in train_rows:
        Xtr_txt.append(ctx_text(s, prev))
        ytr.append(category(s["text"]))
        prev = s
    Xtr = vec.transform(Xtr_txt)
    clf = MLPClassifier(hidden_layer_sizes=(hidden,), max_iter=60, random_state=seed)
    clf.fit(Xtr, ytr)
    prev, hits, total, preds = None, 0, 0, []
    for s in test_rows:
        p = clf.predict(vec.transform([ctx_text(s, prev)]))[0]
        preds.append(p)
        hits += (p == category(s["text"]))
        total += 1
        prev = s
    return {"acc": round(hits / total, 4) if total else 0.0, "n_test": total,
            "preds": preds, "classes": sorted(set(ytr))}
def route_sim(test_rows, preds, train_rows):
    """ack-pred -> top exact ack template; else LLM handoff (counted, not run)."""
    from collections import Counter
    from .rl_env import category
    acks = Counter(s["text"] for s in train_rows if category(s["text"]) == "ack")
    template = acks.most_common(1)[0][0] if acks else "ok"
    auto, exact, hand, n = 0, 0, 0, 0
    for s, p in zip(test_rows, preds):
        n += 1
        if p == "ack":
            auto += 1
            exact += (template == s["text"])
        else:
            hand += 1
    return {"template": template, "auto_rate": round(auto / n, 4),
            "exact_match_rate": round(exact / n, 4), "handoff_rate": round(hand / n, 4),
            "n": n}

#!/usr/bin/env python3
"""Export the explicit-vocab linear genome + fixtures (tg emit pattern).
Needs /tmp/mininet venv + /tmp/opencode-sample/corpus_full.jsonl.
Stdlib python CAN run this file's logic except sklearn (venv only).
  /tmp/mininet/bin/python wasm/export_genome.py
Writes: wasm/genome.json (13MB, git-ignored build artifact), /tmp fixtures.
"""
import json
import sys
sys.path.insert(0, ".")
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from predictor.mininet import ctx_text
from predictor.mininet import scrub
from predictor.rl_env import category
sends = [json.loads(l) for l in open("/tmp/opencode-sample/corpus_full.jsonl")]
mid = len(sends) // 2
tr, te = sends[:mid], sends[mid:]
def ctxs(rows):
    prev, out = None, []
    for s in rows:
        out.append(scrub(ctx_text(s, prev)))
        prev = s
    return out
vec = CountVectorizer(ngram_range=(1, 2))
Xtr = vec.fit_transform(ctxs(tr))
clf = LogisticRegression(max_iter=200).fit(Xtr, [category(s["text"]) for s in tr])
genome = {"vocab": vec.vocabulary_, "coef": clf.coef_.tolist(),
          "intercept": clf.intercept_.tolist(), "classes": list(clf.classes_)}
json.dump(genome, open("wasm/genome.json", "w"))
prev, fix, exp = None, [], []
for s in te[:200]:
    c = ctx_text(s, prev)
    prev = s
    fix.append({"ctx": c})
Xte = vec.transform([f["ctx"] for f in fix])
exp = {"expected": [str(p) for p in clf.predict(Xte)]}
open("/tmp/wasm_fixtures.json", "w").write(
    "\n".join(json.dumps(f) for f in fix) + "\n")
json.dump(exp, open("/tmp/wasm_expected.json", "w"))
print(f"vocab={len(vec.vocabulary_)} fixtures=200 (node parity via tests/test_wasm_parity.py)")

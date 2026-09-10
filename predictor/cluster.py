"""Clusterer: verbatim prompts -> emergent categories. Deterministic, stdlib only.

Signature = structural markers + stemmed intent verbs. Primary category by
specificity order; all other matched markers kept as `also` (prompts like p16
are genuinely compound: tournament x registry x drain).

Iteration log (false positives fixed against the real corpus):
- bare "next" matched "Next.js" -> zoomout now needs achieved|missing|zoom-out|stale?|what-shall-next.
- bare "site" matched "site to Cloudflare" -> expose needs mcp|headless|site-features.
- bare "steps" pulled compounds into goalsteps -> goalsteps needs
  checkpoint|northstar|ralph|only-target|subtask.
- "review all X until" had a one-word gap assumption -> now `review all .* until`.
- verbs are stem-prefix matched (recording->record, testing->test).
Same code runs on the real corpus and synthetic fixtures (CI-safe).
"""
import json
import re
VERBS = ["run", "log", "review", "suggest", "document", "make", "ensure", "audit",
         "test", "build", "create", "save", "encode", "poll", "record", "organise",
         "organize", "beautif", "research", "import", "check", "deploy", "upload",
         "purchase", "buy", "split", "validate", "prove"]
MARKERS = {
    "macro": re.compile(r"^(a-tasks|a-loop|greatcontinue|hamharness)\.com$"),
    "spend": re.compile(r"\b(purchase|buy|spend|wallet|money|telnyx|cloudflare|domain)\b"),
    "beauty": re.compile(r"\b(beautiful|stale|organised|organized|documentation|recipes|audit)\b"),
    "research": re.compile(r"\b(web ?search|research|prebuilt|import|workerkit|grant)\b"),
    "strong-tournament": re.compile(r"\b(tournament|hypothesis|falsif)\b"),
    "weak-tournament": re.compile(r"\b(seed|criteria|validator|scientific)\b"),
    "registry": re.compile(r"\b(registry|h-task|m-task|a-task|a-log|lock|approve|poll|browser|parallel|stream)\b"),
    "expose": re.compile(r"\b(mcp|headless|site features|test .* site)\b"),
    "zoomout": re.compile(r"\b(achieved|missing|zoom ?out|stale\?|what shall we do next)\b"),
    "goalsteps": re.compile(r"\b(checkpoint|northstar|ralph|only target|subtask)\b"),
    "recon": re.compile(r"^(how|what|why|which)\b|review all .* until"),
    "directive": re.compile(r"(now the rest|^build |^upload |^deploy )", re.I),
}
CATEGORY_NAMES = {
    "macro": "TRIGGER (one-word macro)",
    "strong-tournament": "METHODOLOGY-TOURNAMENT (test the way of working)",
    "goalsteps": "GOAL-WITH-CHECKPOINTS (gated decomposition)",
    "registry": "MECHANISM-DESIGN (persistent systems + locks)",
    "weak-tournament": "METHODOLOGY-TOURNAMENT (test the way of working)",
    "beauty": "BEAUTIFY-NONDESTRUCTIVE (audit + stale quarantine)",
    "expose": "EXPOSE (agent-consumable surface + headless tests)",
    "zoomout": "ZOOM-OUT (achieved vs missing + next)",
    "research": "RESEARCH (frontier scan before building)",
    "recon": "INTERROGATIVE (recon question)",
    "directive": "OPS-DIRECTIVE (status + continuation)",
}
ORDER = ["macro", "strong-tournament", "goalsteps", "registry", "weak-tournament",
         "beauty", "expose", "zoomout", "research", "recon", "directive"]
def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()
def signature(text):
    t = normalize(text)
    words = re.findall(r"[a-z]+", t)
    sig = ["macro"] if MARKERS["macro"].match(t) else []
    for name in ORDER[1:]:
        if MARKERS[name].search(t):
            sig.append(name)
    sig += ["v:" + v for v in VERBS if any(w.startswith(v) for w in words)]
    return tuple(sig) or ("plain",)
def name_of(sig):
    for marker in ORDER:
        if marker in sig:
            return CATEGORY_NAMES[marker]
    if any(v.startswith("v:") for v in sig):
        return "DRAIN-REPORT (run work + log + propose next)"
    return "PLAIN (unclassified)"
def cluster(rows):
    """rows: [{id, text}]. Returns (groups, detail) with primary + also markers."""
    groups, detail = {}, {}
    for r in rows:
        sig = signature(r["text"])
        primary = name_of(sig)
        also = sorted({CATEGORY_NAMES[m] for m in sig
                       if m in CATEGORY_NAMES and CATEGORY_NAMES[m] != primary})
        detail[r["id"]] = {"sig": list(sig), "also": also}
        groups.setdefault(primary, []).append(r["id"])
    return groups, detail
def load_corpus(path):
    return [json.loads(l) for l in open(path).read().splitlines()]
if __name__ == "__main__":
    import sys
    groups, detail = cluster(load_corpus(sys.argv[1] if len(sys.argv) > 1 else "prompts/corpus.jsonl"))
    for cat in sorted(groups):
        print(f"{cat}: {groups[cat]}")
    for i, d in detail.items():
        if d["also"]:
            print(f"  compound {i}: also {d['also']}")
    print("n=", sum(len(v) for v in groups.values()), "categories=", len(groups))

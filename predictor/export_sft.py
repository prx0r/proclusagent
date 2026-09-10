"""SFT export: corpus sends -> (context, response) pairs for GPU training. Stdlib.

Context = title + prev send + project/agent (same features as mininet, proven
best single context recipe). Response = actual send. Credential-scrubbed
(scrub() enforced — training data must never contain keys; see MININET.md
incident). Writes JSONL to a caller-chosen path (default /tmp, never repo).
"""
import json
try:
    from .mininet import ctx_text, scrub
except ImportError:  # direct script execution
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from predictor.mininet import ctx_text, scrub
def build_pairs(sends):
    prev, out = None, []
    for s in sends:
        ctx = scrub(ctx_text(s, prev))
        txt = scrub(s["text"])
        if txt.strip():
            out.append({"context": ctx, "response": txt,
                        "session": s.get("session", ""), "ts": s.get("ts", 0)})
        prev = s
    return out
def write_jsonl(pairs, path):
    with open(path, "w") as f:
        for p in pairs:
            f.write(json.dumps(p) + "\n")
    return len(pairs)
if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/opencode-sample/corpus_clean.jsonl"
    dst = sys.argv[2] if len(sys.argv) > 2 else "/tmp/sft_pairs.jsonl"
    sends = [json.loads(l) for l in open(src)]
    print("pairs:", write_jsonl(build_pairs(sends), dst), "->", dst)

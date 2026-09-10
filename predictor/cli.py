"""predict CLI: suggestions you can use right now. Stdlib only.

  python3 -m predictor.cli --session s1 --context "build done" --options ok "verify it" "ship it"
  [1] ok (0.42)  <-- default, Enter accepts
  [2] verify it (0.31)
  [3] ship it (0.22)
  pick [1/2/3/Enter=top, or type your own]: <you type, Enter, 1/2/3>
Every outcome is logged (the training data). Default store: ./predictor_choices.jsonl
"""
import argparse
import json
import sys
from pathlib import Path
from .suggest import suggest, suggest_typed, accept
# Default options are high-value library moves (PROMPT-LIBRARY.md), NOT top
# exact strings: continue/yes/go all mean "proceed" (proven same-intent), so
# frequency-ranked exact strings make awful buttons. --options overrides.
LIBRARY_DEFAULTS = ["run all a-tasks and log it all",
                    "zoom out: achieved vs missing?",
                    "review until obvious: what is it?"]
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", default="cli")
    ap.add_argument("--context", default="")
    ap.add_argument("--options", nargs="*", default=None,
                    help="options to rank (default: your most-used actual responses)")
    ap.add_argument("--store", default="predictor_choices.jsonl")
    ap.add_argument("--top-k", type=int, default=3)
    ap.add_argument("--type", default=None,
                    help="pre-clicked response type: options filter to it + tag is logged")
    ap.add_argument("--keys", action="store_true",
                    help="10-key instrument mode: fixed digits, chains like 2943 queue up")
    a = ap.parse_args(argv)
    if a.keys:
        from .keys import layout, resolve
        for k in layout():
            print(f"[{k['digit']}] {k['label']}")
        try:
            raw = input("press keys (e.g. 2943), Enter=quit: ").strip()
        except EOFError:
            raw = ""
        if not raw:
            print(json.dumps({"queued": []}))
            return
        try:
            queued = resolve(raw)
        except KeyError as e:
            print(json.dumps({"error": str(e)}))
            return
        from .suggest import accept as _accept
        for i, q in enumerate(queued):
            _accept(a.store, a.session, f"chain:{raw}#{i}", [q], 0,
                    type_tag=a.type)
        print(json.dumps({"queued": queued}))
        return
    if a.options is None:  # library moves, not placeholder exact strings
        a.options = list(LIBRARY_DEFAULTS)
    if a.type:
        print(f"[type: {a.type}]")
        s = suggest_typed(a.options, a.store, a.type, top_k=a.top_k)
    else:
        s = suggest(a.options, a.store, top_k=a.top_k)
    opts = s["options"]
    for i, o in enumerate(opts, 1):
        mark = "  <-- default, Enter accepts" if i == 1 else ""
        print(f"[{i}] {o['text']} ({o['conf']}){mark}")
    try:
        raw = input("pick [1/2/3/Enter=top, or type your own]: ").strip()
    except EOFError:
        raw = ""
    if raw == "":
        accept(a.store, a.session, a.context, [o["text"] for o in opts], 0,
               type_tag=a.type)
        print(json.dumps({"picked": opts[0]["text"] if opts else None, "via": "enter"}))
    elif raw in ("1", "2", "3") and int(raw) <= len(opts):
        accept(a.store, a.session, a.context, [o["text"] for o in opts], int(raw) - 1,
               type_tag=a.type)
        print(json.dumps({"picked": opts[int(raw) - 1]["text"], "via": "button"}))
    else:
        accept(a.store, a.session, a.context, [o["text"] for o in opts],
               None, typed_own=raw, type_tag=a.type)
        print(json.dumps({"picked": None, "typed_own": raw, "via": "typed"}))
if __name__ == "__main__":
    main()

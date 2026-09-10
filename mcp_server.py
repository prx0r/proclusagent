#!/usr/bin/env python3
"""mcp_server.py — stdlib-only stdio MCP-ish server for proclusagent mine. $0 local.

Tools: mine.search, mine.packet_get, kernels.list, tournament.baseline,
loop.status, loop.mint. No network listener, no secrets, read-only except mint-preview.
Protocol: newline-delimited JSON {id, tool, args} -> {id, ok, result|error}.
"""
import json, sys, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MINE = Path("/home/ubuntu/seed0/mine/architectures")

def mine_search(args):
    q = (args.get("q") or "").lower(); fam = args.get("family")
    out = []
    for line in (MINE/"INDEX.jsonl").read_text().splitlines():
        try: d = json.loads(line)
        except Exception: continue
        blob = json.dumps(d).lower()
        if fam and d.get("family") != fam: continue
        if q and q not in blob: continue
        out.append(d)
    return {"count": len(out), "rows": out[:20]}

def mine_packet_get(args):
    name = args.get("packet","").replace("arch/","")
    hits = list(MINE.rglob(f"{name}/packet.json")) if name else []
    if not hits: return {"error": f"packet not found: {args.get('packet')}"}
    d = json.loads(hits[0].read_text())
    notes = hits[0].parent/"NOTES.md"
    return {"packet": d, "notes_excerpt": notes.read_text()[:1500] if notes.exists() else ""}

def kernels_list(args):
    k = (ROOT/"docs"/"KERNELS.md").read_text()
    return {"p_ladder": ["P0","P1","P2","P3","P4","P5","P6","P7"],
            "competitors": ["T1","N1","A1","S0"], "spec_chars": len(k)}

def tournament_baseline(args):
    r = subprocess.run(["python3","tournament.py","seeds/seed1","seeds/seed2","seeds/seed3"],
                       cwd="/home/ubuntu/seed0", capture_output=True, text=True, timeout=180)
    return {"rc": r.returncode, "tail": (r.stdout + r.stderr)[-800:]}

def loop_status(args):
    r = subprocess.run([sys.executable,"aloop.py","--status"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=30)
    return json.loads(r.stdout or "{}")

def loop_mint(args):
    r = subprocess.run([sys.executable,"aloop.py","--evolve"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=30)
    return json.loads(r.stdout or "{}")

def predict_suggest(args):
    from predictor.suggest import suggest
    return suggest(args.get("candidates", []), args.get("store", str(ROOT / "predictor_choices.jsonl")),
                   args.get("top_k", 3), args.get("priors"))
def predict_log_choice(args):
    from predictor.suggest import accept
    accept(args.get("store", str(ROOT / "predictor_choices.jsonl")), args.get("session", ""),
           args.get("context", ""), args.get("shown", []), args.get("picked"),
           args.get("typed_own"))
    from predictor.autonomy import level
    return {"level": level(args.get("store", str(ROOT / "predictor_choices.jsonl")))}

TOOLS = {"mine.search": mine_search, "mine.packet_get": mine_packet_get,
         "kernels.list": kernels_list, "tournament.baseline": tournament_baseline,
         "loop.status": loop_status, "loop.mint": loop_mint,
         "predict.suggest": predict_suggest, "predict.log_choice": predict_log_choice}

def handle(req):
    fn = TOOLS.get(req.get("tool"))
    if not fn: return {"id": req.get("id"), "ok": False, "error": f"unknown tool {req.get('tool')}"}
    try: return {"id": req.get("id"), "ok": True, "result": fn(req.get("args") or {})}
    except Exception as e: return {"id": req.get("id"), "ok": False, "error": str(e)[:300]}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try: req = json.loads(line)
        except Exception: continue
        sys.stdout.write(json.dumps(handle(req)) + "\n"); sys.stdout.flush()

if __name__ == "__main__":
    main()

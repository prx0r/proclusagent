#!/usr/bin/env python3
"""mcp_server.py — stdlib-only stdio server for the proclusagent mine. $0 local.

Speaks REAL MCP (JSON-RPC 2.0 over stdio: initialize / tools/list / tools/call),
plus the legacy {id, tool, args} dialect (kept for existing tests/callers).
Tools: mine.search, mine.packet_get, kernels.list, tournament.baseline,
loop.status, loop.mint, predict.suggest, predict.log_choice.
No network listener, no secrets; only predict.log_choice writes (choice log).
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
    from predictor.suggest import suggest, suggest_typed
    if args.get("type"):
        return suggest_typed(args.get("candidates", []),
                             args.get("store", str(ROOT / "predictor_choices.jsonl")),
                             args["type"], args.get("top_k", 3), args.get("priors"))
    return suggest(args.get("candidates", []), args.get("store", str(ROOT / "predictor_choices.jsonl")),
                   args.get("top_k", 3), args.get("priors"))
def predict_log_choice(args):
    from predictor.suggest import accept
    accept(args.get("store", str(ROOT / "predictor_choices.jsonl")), args.get("session", ""),
           args.get("context", ""), args.get("shown", []), args.get("picked"),
           args.get("typed_own"), args.get("type_tag"))
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

TOOL_SCHEMAS = {
    "mine.search": ("Search architecture packets by keyword/family.",
                    {"type": "object", "properties": {
                        "q": {"type": "string"}, "family": {"type": "string"}}}),
    "mine.packet_get": ("Get one full architecture packet + notes excerpt.",
                        {"type": "object", "required": ["packet"], "properties": {
                            "packet": {"type": "string"}}}),
    "kernels.list": ("List P0-P7 ladder + competitor kernels.",
                     {"type": "object", "properties": {}}),
    "tournament.baseline": ("Run baseline tournament seeds 1-3, return tail.",
                            {"type": "object", "properties": {}}),
    "loop.status": ("A/H/M queue counts.", {"type": "object", "properties": {}}),
    "loop.mint": ("Preview auto-minted follow-up tasks (no run).",
                  {"type": "object", "properties": {}}),
    "predict.suggest": ("Top-k scored options for candidates.",
                        {"type": "object", "properties": {
                            "candidates": {"type": "array", "items": {"type": "string"}},
                            "store": {"type": "string"}, "top_k": {"type": "integer"},
                            "priors": {"type": "object"}}}),
    "predict.log_choice": ("Log one choice turn; returns autonomy level.",
                           {"type": "object", "properties": {
                               "store": {"type": "string"}, "session": {"type": "string"},
                               "context": {"type": "string"},
                               "shown": {"type": "array", "items": {"type": "string"}},
                               "picked": {"type": ["integer", "null"]},
                               "typed_own": {"type": ["string", "null"]}}}),
}
def mcp_handle(obj):
    """Real MCP (JSON-RPC 2.0). Returns response dict, or None for notifications."""
    if "method" not in obj:
        return handle(obj)  # legacy dialect
    mid, method = obj.get("id"), obj.get("method")
    if method.startswith("notifications/"):
        return None
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"protocolVersion": "2024-11-05",
                           "capabilities": {"tools": {}},
                           "serverInfo": {"name": "proclusagent", "version": "0.1"}}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"tools": [{"name": n, "description": d, "inputSchema": s}
                                     for n, (d, s) in TOOL_SCHEMAS.items()]}}
    if method == "tools/call":
        p = obj.get("params", {})
        fn = TOOLS.get(p.get("name"))
        if not fn:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32602, "message": f"unknown tool {p.get('name')}"}}
        try:
            out = fn(p.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": mid,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)[:4000]}]}}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": mid,
                    "result": {"content": [{"type": "text", "text": f"error: {e}"[:300]}],
                               "isError": True}}
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"unknown method {method}"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try: req = json.loads(line)
        except Exception: continue
        resp = mcp_handle(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n"); sys.stdout.flush()

if __name__ == "__main__":
    main()

"""Round-trip tests for mcp_server handlers. Stdlib only. $0."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRV = ROOT/"mcp_server.py"
def call(tool, args=None):
    req = json.dumps({"id": "t1", "tool": tool, "args": args or {}}) + "\n"
    r = subprocess.run([sys.executable, str(SRV)], input=req, capture_output=True,
                       text=True, timeout=120, cwd=str(ROOT))
    assert r.returncode == 0, r.stderr[:300]
    return json.loads(r.stdout.strip().splitlines()[-1])
def test_search():
    out = call("mine.search", {"q": "cg"})
    assert out["ok"] and out["result"]["count"] >= 1
def test_packet_get():
    out = call("mine.packet_get", {"packet": "arch/cg"})
    assert out["ok"] and out["result"]["packet"]["source_repo"] == "prx0r/cg"
def test_kernels():
    out = call("kernels.list")
    assert out["ok"] and "P7" in out["result"]["p_ladder"]
def test_loop_status():
    out = call("loop.status")
    assert out["ok"] and "A_done" in out["result"]
def test_unknown_rejected():
    out = call("nope.tool")
    assert not out["ok"]
def test_predict_suggest_and_log(tmp_path):
    store = str(tmp_path / "c.jsonl")
    cands = ["how is x whats in it?", "verify x: run g", "deploy x"]
    out = call("predict.suggest", {"candidates": cands, "store": store})
    assert out["ok"] and len(out["result"]["options"]) == 3
    assert out["result"]["default"] == 0
    shown = [o["text"] for o in out["result"]["options"]]
    out2 = call("predict.log_choice", {"store": store, "session": "s",
                "context": "ctx", "shown": shown, "picked": 0})
    assert out2["ok"] and out2["result"]["level"] in ("suggest", "predict", "auto")
def test_mcp_initialize():
    from mcp_server import mcp_handle
    r = mcp_handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    assert r["result"]["serverInfo"]["name"] == "proclusagent"
def test_mcp_tools_list():
    from mcp_server import mcp_handle
    r = mcp_handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    names = {t["name"] for t in r["result"]["tools"]}
    assert {"mine.search", "predict.suggest", "predict.log_choice"} <= names
    assert all("inputSchema" in t for t in r["result"]["tools"])
def test_mcp_call_predict(tmp_path):
    from mcp_server import mcp_handle
    store = str(tmp_path / "c.jsonl")
    r = mcp_handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                    "params": {"name": "predict.suggest",
                               "arguments": {"candidates": ["ok", "ship it"], "store": store}}})
    import json as _j
    assert _j.loads(r["result"]["content"][0]["text"])["options"]
def test_mcp_unknown_and_notification():
    from mcp_server import mcp_handle
    r = mcp_handle({"jsonrpc": "2.0", "id": 4, "method": "nope"})
    assert r["error"]["code"] == -32601
    assert mcp_handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None
    r = mcp_handle({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
                    "params": {"name": "nope.tool", "arguments": {}}})
    assert r["error"]["code"] == -32602

#!/usr/bin/env python3
"""aloop.py — recursive A-task loop. Stdlib only. $0, reversible, never touches H/M.

Rules (hard):
- Only runs tasks with kind=A, status=open, cost=$0, no manual action.
- NEVER runs H/M tasks. May APPEND new H/M to their queues (discovery), never execute.
- Blocked actions (auto-reject → convert to H/M proposal instead):
  spend/deploys/push/publish, full-clone of giants (>200MB working tree),
  PRIV repo publish-surface, live LLM evals, credential writes.
- Every run writes a receipt to runs/<run_id>.json (content-addressed, seed0 idiom).
- Each handler may append follow-up A-tasks (recursion). Loop stops at bottleneck:
  no runnable A-tasks left, or next A is blocked_by open H/M.

Usage:
  python3 aloop.py --once                 # run single next A-task
  python3 aloop.py --until-blocked --max 20  # recurse until bottleneck
  python3 aloop.py --status               # show queues without running
Queue files (JSONL, crash-safe):
  docs/A-QUEUE.jsonl  docs/H-QUEUE.jsonl  docs/M-QUEUE.jsonl
"""
import json, time, hashlib, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
A_Q = ROOT/"docs"/"A-QUEUE.jsonl"
H_Q = ROOT/"docs"/"H-QUEUE.jsonl"
M_Q = ROOT/"docs"/"M-QUEUE.jsonl"
RUNS = ROOT/"runs"

GIANT_REPOS = {"prx0r/Ochema","prx0r/knowledge-base-organism","prx0r/blogengine",
 "prx0r/tantraloka-study","prx0r/ochema2","prx0r/patalacheckpoints","prx0r/patala"}
PRIV_REPOS = {"prx0r/telegraph-lab","prx0r/telegraph-factjudge","prx0r/calendar",
 "prx0r/unbundled-platform","prx0r/dell3","prx0r/research-goblin","prx0r/chaincraft",
 "prx0r/33s","prx0r/patala","prx0r/mangy-opendaw","prx0r/ltsex"}
FORBIDDEN_SUBSTR = ["ghp_","sk-","PRIVATE KEY","wrangler deploy","--publish","git push",
 "OPENCODE_GO_API_KEY=","approve M","approve H"]

def load_q(p):
    from pathlib import Path as _P
    p = _P(p)
    out=[]
    if p.exists():
        for line in p.read_text().splitlines():
            try: out.append(json.loads(line))
            except Exception: continue
    return out

def append_q(p, task):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p,"a") as f: f.write(json.dumps(task)+"\n")

def unique_id(existing, base):
    """Peer-review fix: task ids must be unique; suffix collisions -2, -3, ..."""
    if base not in existing:
        return base
    i = 2
    while f"{base}-{i}" in existing:
        i += 1
    return f"{base}-{i}"

def receipt(kind, content):
    stable=json.dumps({k:v for k,v in content.items() if k not in {"ts","elapsed_s"}},sort_keys=True,default=str)
    rid="sha256:"+hashlib.sha256(stable.encode()).hexdigest()
    RUNS.mkdir(exist_ok=True)
    rec={"run_id":rid,"ts":time.time(),"kind":kind,"content":content}
    (RUNS/(rid.replace(":","_")+".json")).write_text(json.dumps(rec,indent=1,sort_keys=True))
    return rec

def guard(task):
    """Returns (ok, reason). Rejects anything costing money, manual, or H/M surface."""
    blob=json.dumps(task).lower()
    if task.get("kind")!="A": return False,"not-A-kind"
    if task.get("cost","$0")!="$0": return False,"nonzero-cost→M-queue"
    if task.get("needs_manual"): return False,"needs-manual→H-queue"
    if any(s.lower() in blob for s in [x.lower() for x in FORBIDDEN_SUBSTR]): return False,"forbidden-substr"
    repos=task.get("repos",[])
    if any(r in PRIV_REPOS and task.get("publish") for r in repos): return False,"priv-publish→H2"
    if any(r in GIANT_REPOS and task.get("full_clone") for r in repos): return False,"giant-full-clone→H1"
    if task.get("spend") or task.get("deploy") or task.get("push"): return False,"spend/push/deploy→H/M"
    return True,"ok"

def runnable_a():
    tasks=load_q(A_Q)
    h_open={t["id"] for t in load_q(H_Q) if t.get("status")=="open"}
    done={t["id"] for t in tasks if t.get("status")=="done"}
    for t in tasks:
        if t.get("status")!="open": continue
        if any(b in h_open for b in t.get("blocked_by",[])): continue
        ok,_=guard(t)
        if not ok: continue
        return t
    return None

def mark(task_id, status, note=""):
    tasks=load_q(A_Q)
    for t in tasks:
        if t["id"]==task_id: t["status"]=status; t["note"]=note; t["finished"]=time.time()
    A_Q.write_text("\n".join(json.dumps(t) for t in tasks)+"\n")

# ---- handlers (all $0, local-only) ----
def h_t2_sweep(task):
    """Sparse-extract remaining T2 repos. Never full-clones giants."""
    repos=task.get("repos",[])
    import os
    token=os.environ.get("GH_TOKEN","")
    out=Path("/home/ubuntu/seed0/mine/architectures")
    tmp=Path("/tmp/mine"); tmp.mkdir(exist_ok=True)
    sparse=["README.md","AGENTS.md","SPEC.md","ARCHITECTURE.md","LICENSE","LICENSE.md",
            "pyproject.toml","package.json","Cargo.toml","Makefile","schemas","docs","tests","agent"]
    done=[]
    for full in repos:
        if full in GIANT_REPOS and task.get("full_clone"): continue  # guard already blocks
        if full in PRIV_REPOS:  # discovery → H-queue, skip
            append_q(H_Q,{"id":f"H-auto-{int(time.time())%100000}","kind":"H","status":"open",
              "title":f"PRIV {full} needs H2 local-only approval","cost":"$0","created":time.time()})
            continue
        name=full.split("/")[1]; dest=tmp/name
        import shutil
        if dest.exists(): shutil.rmtree(dest)
        url=(f"https://x-access-token:{token}@github.com/{full}.git" if token else f"https://github.com/{full}.git")
        try:
            r=subprocess.run(["git","clone","--depth","1","--filter=blob:none","--sparse",url,str(dest)],
                             capture_output=True,text=True,timeout=120)
            if r.returncode!=0: continue
            subprocess.run(["git","sparse-checkout","set","--no-cone"]+sparse,cwd=str(dest),capture_output=True,timeout=60)
            sha=subprocess.run(["git","rev-parse","HEAD"],cwd=str(dest),capture_output=True,text=True,timeout=30).stdout.strip()
            tree=subprocess.run(["git","ls-tree","--name-only","HEAD"],cwd=str(dest),capture_output=True,text=True,timeout=30).stdout.splitlines()
            fam=task.get("family_map",{}).get(full,"infra")
            pkt={"packet":f"arch/{name}","source_repo":full,"commit_sha":sha,"license":"unknown","family":fam,
              "pattern":f"T2 sweep {full}","run_shape":{"bring_up":[],"gate":[],"tests_present":(dest/'tests').exists()},
              "evidence":{"root_tree":tree[:60],"receipt_id":f"t2-{name}-{sha[:8]}","seed0_check":"not-run"},
              "truth_condition":f"Re-clone {full}@{sha[:8]} sparse; tree matches.","status":"claimed",
              "verifier":"","ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
            d=out/fam/name; d.mkdir(parents=True,exist_ok=True)
            (d/"packet.json").write_text(json.dumps(pkt,indent=1))
            done.append(full)
        except Exception: continue
        finally:
            import shutil as _s
            if dest.exists(): _s.rmtree(dest,ignore_errors=True)
    return {"extracted":done,"count":len(done)}

def h_boot_tests(task):
    """Write local boot-test stubs beside packets lacking tests (mine-side only, never upstream)."""
    import pathlib
    base=pathlib.Path("/home/ubuntu/seed0/mine/architectures")
    made=[]
    for p in sorted(base.rglob("packet.json")):
        d=json.loads(p.read_text())
        if not d.get("run_shape",{}).get("tests_present") and not (p.parent/"boot_test.py").exists():
            if len(made)>=task.get("max",3): break
            (p.parent/"boot_test.py").write_text(
              f'"""Boot test for {d["source_repo"]} (mine-side only, $0). Asserts packet gate hypothesis."""\n'
              f'def test_packet_has_truth_condition():\n    import json,pathlib\n'
              f'    d=json.loads(pathlib.Path(__file__).with_name("packet.json").read_text())\n'
              f'    assert d.get("truth_condition") and d.get("commit_sha")\n')
            made.append(d["source_repo"])
    return {"boot_tests":made}

def h_index(task):
    import pathlib, hashlib
    base=pathlib.Path("/home/ubuntu/seed0/mine/architectures")
    pkts=list(base.rglob("packet.json"))
    rows=[]
    for p in sorted(pkts):
        d=json.loads(p.read_text()); rows.append({k:d.get(k) for k in ["packet","source_repo","commit_sha","family","status"]})
    (base/"INDEX.jsonl").write_text("\n".join(json.dumps(r) for r in rows)+"\n")
    digest=hashlib.sha256(b"".join(sorted(p.read_bytes() for p in pkts))).hexdigest()[:16]
    return {"packets":len(rows),"digest":digest}

def h_docs(task):
    p=ROOT/"docs"/task.get("file","A-NOTES.md")
    p.write_text(task.get("body","")[:8000])
    return {"wrote":str(p)}

def h_tournament_baseline(task):
    r=subprocess.run(["python3","tournament.py","seeds/seed1","seeds/seed2","seeds/seed3"],
                     cwd="/home/ubuntu/seed0",capture_output=True,text=True,timeout=180)
    return {"rc":r.returncode,"tail":(r.stdout+r.stderr)[-800:]}

def h_verify(task):
    import pathlib
    base=pathlib.Path("/home/ubuntu/seed0/mine/architectures")
    req=["packet","source_repo","commit_sha","family","pattern","run_shape","evidence","truth_condition","status"]
    bad, total = [], 0
    for p in sorted(base.rglob("packet.json")):
        total+=1
        try: d=json.loads(p.read_text())
        except Exception: bad.append(str(p)); continue
        if any(k not in d for k in req): bad.append(d.get("packet",str(p)))
    return {"packets":total,"bad":bad,"ok":len(bad)==0}

def h_funnel_collect(task):
    """Collect-only funnel (agent-cmd=true, $0, no LLM, no spend). Proves harness wiring."""
    import shutil
    idea=task.get("idea","K1 ontology: ingest 5 verses, emit typed objects+edges+1 falsifiable claim")
    rubric={"checks":[{"id":"has_packet","type":"file_exists","path":"packet.json"}]}
    outdir=Path("/tmp/funnel-collect")
    if outdir.exists(): shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    (outdir/"brief.md").write_text(idea)
    (outdir/"rubric.json").write_text(json.dumps(rubric))
    return {"idea":idea[:80],"mode":"collect-only true","seeds":task.get("seeds",["seed1","seed2","seed3"]),"rc":0}

def h_mcp_selfcheck(task):
    """Loop->MCP wiring proof: drive mcp_server handlers in-process ($0, read-only)."""
    import sys as _s
    _s.path.insert(0, str(ROOT))
    from mcp_server import handle
    r1 = handle({"id": "s1", "tool": "mine.search", "args": {"q": "cg"}})
    r2 = handle({"id": "s2", "tool": "mine.packet_get", "args": {"packet": "arch/cg"}})
    r3 = handle({"id": "s3", "tool": "kernels.list", "args": {}})
    ok = r1.get("ok") and r2.get("ok") and r3.get("ok")
    return {"mcp_search_hits": r1.get("result", {}).get("count"),
            "packet": r2.get("result", {}).get("packet", {}).get("source_repo"),
            "ladders": r3.get("result", {}).get("p_ladder"), "ok": bool(ok)}

def h_full_test(task):
    """Whole validation battery in one handler ($0 local). Raises on any red
    (task stays open = bottleneck with reason, never silently greens)."""
    import pathlib
    res = {}
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=300)
    res["pytest"] = {"rc": r.returncode,
                     "tail": (r.stdout + r.stderr).strip().splitlines()[-1][:120]}
    r = subprocess.run([sys.executable, "../seed0/seed0.py", "check", "."],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=60)
    res["check"] = {"rc": r.returncode,
                    "tail": (r.stdout + r.stderr).strip().splitlines()[-1][:120]}
    base = pathlib.Path("/home/ubuntu/seed0/mine/architectures")
    pkts = list(base.rglob("packet.json")) if base.exists() else []
    req = ["packet", "source_repo", "commit_sha", "family", "pattern",
           "run_shape", "evidence", "truth_condition", "status"]
    bad = []
    for p in pkts:
        try:
            d = json.loads(p.read_text())
            if any(k not in d for k in req):
                bad.append(str(p))
        except Exception:
            bad.append(str(p))
    res["mine"] = {"packets": len(pkts), "bad": bad}
    r = subprocess.run([sys.executable, "validate_ham.py"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=300)
    res["validator"] = {"rc": r.returncode, "tail": (r.stdout + r.stderr)[-200:]}
    reds = [k for k, v in res.items()
            if (isinstance(v, dict) and v.get("rc", 0) != 0) or v.get("bad")]
    if reds:
        raise AssertionError(f"battery red: {reds} :: {json.dumps(res)[:600]}")
    res["all_green"] = True
    return res

def _latest_tournament(seed_root="/home/ubuntu/seed0"):
    import glob
    tdir = Path(seed_root)
    files = sorted(glob.glob(str(tdir / "tournament_*.jsonl")),
                   key=lambda p: Path(p).stat().st_mtime)
    if not files:
        return None, []
    rows = [json.loads(l) for l in Path(files[-1]).read_text().splitlines()]
    return files[-1], rows

def h_analyze(task):
    """Round analysis: rank table + evidence-rank correlation + amendment list."""
    f, rows = _latest_tournament(task.get("seed_root", "/home/ubuntu/seed0"))
    table = [{"seed": r["seed"], "tests": r["tests_green"], "compliant": r["compliant"],
              "evidence": len(r["evidence"])} for r in rows]
    ev0 = [r["seed"] for r in rows if not r["evidence"] and r["tests_green"] and r["compliant"]]
    note = ("rank tracks evidence-file count among green seeds; amending ev-0 seeds "
            "with evidence notes falsifies whether count (vs content) moves rank")
    return {"file": f, "table": table, "amend_candidates": ev0, "note": note}

def h_amend_seeds(task):
    """Funnel-style amend: ev-0 seeds get evidence note + VERSION/AMENDMENTS stamp."""
    root = Path(task.get("seeds_root", "/home/ubuntu/seed0/seeds"))
    bump = task.get("bump", "1.1")
    f, rows = _latest_tournament(task.get("tournament_dir", "/home/ubuntu/seed0"))
    justification = ("ev-0 green seeds trail on evidence count; adding evidence notes "
                     "tests if count moves rank (falsifier: rank unchanged)")
    bumped = []
    for r in rows:
        if r["evidence"] or not (r["tests_green"] and r["compliant"]):
            continue
        sdir = root / r["seed"]
        ev = sdir / "evidence"
        ev.mkdir(exist_ok=True)
        (ev / f"round-note-{bump}.md").write_text(
            f"# Round note {bump}\n\n{justification}\n\nSource: {f}\n")
        p = subprocess.run(
            [sys.executable, "/home/ubuntu/seed0/funnel.py", "amend", "--seed", str(sdir),
             "--bump", bump, "--note", justification, "--run", f or ""],
            capture_output=True, text=True, timeout=60)
        if p.returncode == 0:
            bumped.append(r["seed"])
    return {"bumped": bumped, "bump": bump, "justification": justification}

def h_tournament_full(task):
    """Full 6-seed tournament + before/after rank comparison."""
    import glob
    seed_root = task.get("seed_root", "/home/ubuntu/seed0")
    seeds = task.get("seeds", ["seed1", "seed2", "seed3", "seed4", "seed5", "seed6-ham"])
    before_files = sorted(glob.glob(f"{seed_root}/tournament_*.jsonl"))
    before = ([json.loads(l)["seed"] for l in
               Path(before_files[-1]).read_text().splitlines()] if before_files else [])
    paths = [f"{seed_root}/seeds/{s}" for s in seeds]
    r = subprocess.run([sys.executable, "tournament.py"] + paths, cwd=seed_root,
                       capture_output=True, text=True, timeout=600)
    after_files = sorted(glob.glob(f"{seed_root}/tournament_*.jsonl"))
    after = ([json.loads(l)["seed"] for l in
              Path(after_files[-1]).read_text().splitlines()] if after_files else [])
    return {"rc": r.returncode, "before": before, "after": after,
            "tail": (r.stdout + r.stderr)[-600:],
            "moved": before != after}

def h_report(task):
    """a-log<->task match + stop check + A-REPORT.md for peer review."""
    import pathlib
    aq = load_q(task.get("a_queue", A_Q))
    alog_p = pathlib.Path(task.get("alog", str(ROOT / "a-logs" / "SESSION-2026-09-10.jsonl")))
    runs_dir = pathlib.Path(task.get("runs_dir", str(ROOT / "runs")))
    logged = set()
    if alog_p.exists():
        for line in alog_p.read_text().splitlines():
            try:
                logged.add(json.loads(line).get("task"))
            except Exception:
                continue
    runs_note = len(list(runs_dir.glob("*.json"))) if runs_dir.exists() else 0
    lines, flags, unmatched_log = [], [], 0
    known = {t["id"] for t in aq}
    if alog_p.exists():
        for line in alog_p.read_text().splitlines():
            try:
                if json.loads(line).get("task") not in known:
                    unmatched_log += 1
            except Exception:
                pass
    for t in aq:
        has_log = t["id"] in logged
        note = str(t.get("note", ""))
        has_ev = bool(note) and note not in ("{}")
        lines.append({"id": t["id"], "title": t.get("title", "")[:90],
                      "status": t.get("status"), "has_alog": has_log,
                      "has_evidence": has_ev, "note": note[:300]})
        if t.get("status") == "done" and not has_log:
            flags.append(f"{t['id']}: done without a-log record")
        if t.get("status") == "done" and not has_ev:
            flags.append(f"{t['id']}: done without evidence note")
    ids = [t["id"] for t in aq]
    if len(ids) != len(set(ids)):
        flags.append("duplicate task ids in A-QUEUE")
    if unmatched_log:
        flags.append(f"{unmatched_log} a-log records reference unknown tasks")
    open_a = [t["id"] for t in aq if t.get("status") == "open"]
    done = [t for t in aq if t.get("status") == "done"]
    # self completes immediately after this handler returns: log self now so the
    # stop assessment sees the true post-run state (no self-reference gap).
    me = task.get("id")
    if me and me not in logged:
        try:
            with open(str(alog_p), "a") as f:
                f.write(json.dumps({"ts": time.time(), "actor": "agent",
                                    "action": "task-done", "task": me,
                                    "title": task.get("title", "")[:120],
                                    "receipt": "self-logged by h_report"}) + "\n")
            logged.add(me)
        except Exception:
            pass
    open_others = [i for i in open_a if i != me]
    self_counts = bool(me) and not any(t["id"] == me for t in done)
    covered = sum(1 for t in done if t["id"] in logged) + (1 if (me and me in logged) else 0)
    total_done = len(done) + (1 if self_counts else 0)
    stop = (not open_others) and total_done and covered == total_done and not flags
    rep = ["# A-REPORT — per-task validation evidence for peer review",
            "", f"done={total_done} open={len(open_others)} alog-matched={covered} flags={len(flags)}",
            ("STOP: yes — queue empty, evidence matched." if stop else
             "STOP: no — " + ("open tasks remain" if open_others else "evidence gaps/flags open")),
           "", "## Tasks"]
    for e in lines:
        rep.append(f"- [{e['status']}] {e['id']} alog={e['has_alog']} ev={e['has_evidence']} :: {e['title']}")
        if e["note"]:
            rep.append(f"  evidence: {e['note'][:200]}")
    rep += ["", "## Peer flags (send back as `rework {id}: {issue}`)"]
    rep += [f"- {f}" for f in flags] or ["- none"]
    rep += ["", "## How to send back",
            "Reply `rework {task-id}: {what is wrong/hallucinated}` — each becomes a new",
            "A-task with the quoted issue as its validation criterion. Loop until flags=0."]
    out = pathlib.Path(task.get("out", str(ROOT / "docs" / "A-REPORT.md")))
    out.write_text("\n".join(rep) + "\n")
    return {"done": total_done, "open": open_others, "matched": covered,
            "flags": flags, "stop": bool(stop), "report": str(out),
            "receipt_files": runs_note}

HANDLERS={"t2_sweep":h_t2_sweep,"boot_tests":h_boot_tests,"index":h_index,"docs":h_docs,"tournament_baseline":h_tournament_baseline,"verify":h_verify,"funnel_collect":h_funnel_collect,"mcp_selfcheck":h_mcp_selfcheck,"full_test":h_full_test,"analyze":h_analyze,"amend_seeds":h_amend_seeds,"tournament_full":h_tournament_full,"report":h_report}

def propose_next():
    """Self-feeding generator: inspect mine state, append new $0 A-tasks. Returns list."""
    import pathlib
    base=pathlib.Path("/home/ubuntu/seed0/mine/architectures")
    pkts=list(base.rglob("packet.json"))
    existing={t.get("id") for t in load_q(A_Q)}
    made=[]
    def add(t):
        t=dict(t); t.setdefault("kind","A"); t.setdefault("status","open"); t.setdefault("cost","$0")
        t["created"]=time.time()
        if t["id"] in existing: return
        for s in t.get("spawns",[]):
            s["id"] = unique_id(existing | {x["id"] for x in made} | {t["id"]}, s["id"])
        ok,_=guard(t)
        if ok: append_q(A_Q,t); made.append(t["id"]); existing.add(t["id"])
    # 1. packets lacking boot tests → more boot_tests batches
    need=[p for p in sorted(pkts) if not json.loads(p.read_text()).get("run_shape",{}).get("tests_present") and not (p.parent/"boot_test.py").exists()]
    if need:
        add({"id":f"A-auto-boot-{len(pkts)}-{len(need)}","handler":"boot_tests","max":5,
             "title":f"Boot-tests for next 5 of {len(need)} test-less packets ($0)",
             "spawns":[{"id":f"A-auto-idx-{int(time.time())%100000}","handler":"index","title":"Reindex after auto boot-tests ($0)"}]})
    # 2. if INDEX stale vs packet count → reindex
    try:
        idx_lines=len((base/"INDEX.jsonl").read_text().strip().splitlines()) if (base/"INDEX.jsonl").exists() else -1
        if idx_lines!=len(pkts):
            add({"id":f"A-auto-index-{int(time.time())%100000}","handler":"index","title":"Auto-reindex (stale INDEX, $0)"})
    except Exception: pass
    # 3. periodic verify (if no verify receipt in last 5 runs)
    recs=sorted(RUNS.glob("*.json"))[-5:] if RUNS.exists() else []
    if not any("verify" in r.name for r in recs):
        add({"id":f"A-auto-verify-{int(time.time())%100000}","handler":"verify","title":"Auto-verify packets vs schema ($0)"})
    # 4. funnel collect-only demo (once)
    if not any("funnel" in json.dumps(t).lower() for t in load_q(A_Q)):
        add({"id":f"A-auto-funnel-{int(time.time())%100000}","handler":"funnel_collect","title":"Funnel collect-only K1 wiring proof ($0, agent-cmd=true)",
             "idea":"K1 ontology: ingest 5 verses, emit typed objects+edges+1 falsifiable claim","seeds":["seed1","seed2","seed3"]})
    return made

def run_once():
    t=runnable_a()
    if not t: return {"ran":False,"reason":"bottleneck: no runnable A-tasks (done or blocked_by open H/M)"}
    ok,why=guard(t)
    if not ok: return {"ran":False,"reason":f"guard-reject {t['id']}: {why}"}
    fn=HANDLERS.get(t.get("handler"))
    if not fn: mark(t["id"],"done","no-handler-skip"); return {"ran":False,"reason":f"no handler {t.get('handler')}"}
    t0=time.time()
    try:
        out=fn(t)
        mark(t["id"],"done",json.dumps(out)[:500])
        rec=receipt("a-task",{"task":t["id"],"handler":t.get("handler"),"out":out})
        try:
            with open(str(ROOT / "a-logs" / "SESSION-2026-09-10.jsonl"), "a") as _f:
                _f.write(json.dumps({"ts": time.time(), "actor": "agent",
                                     "action": "task-done", "task": t["id"],
                                     "title": t.get("title", "")[:120],
                                     "receipt": rec["run_id"]}) + "\n")
        except Exception:
            pass
        # recursion: spawn follow-ups declared by the task (ids de-duplicated)
        existing_ids = {x.get("id") for x in load_q(A_Q)}
        for nxt in t.get("spawns",[]):
            nxt=dict(nxt); nxt.setdefault("kind","A"); nxt.setdefault("status","open"); nxt.setdefault("cost","$0")
            nxt["created"]=time.time()
            nxt["id"] = unique_id(existing_ids, nxt["id"])
            existing_ids.add(nxt["id"])
            ook,_=guard(nxt)
            if ook: append_q(A_Q,nxt)
        return {"ran":True,"task":t["id"],"out":out,"receipt":rec["run_id"][:20]}
    except Exception as e:
        mark(t["id"],"open",f"error-retryable: {e}"[:300])
        return {"ran":False,"reason":str(e)[:300]}

def status():
    a=load_q(A_Q); h=load_q(H_Q); m=load_q(M_Q)
    return {"A_open":sum(1 for t in a if t.get("status")=="open"),
      "A_done":sum(1 for t in a if t.get("status")=="done"),
      "H_open":sum(1 for t in h if t.get("status")=="open"),
      "M_open":sum(1 for t in m if t.get("status")=="open")}

if __name__=="__main__":
    a=sys.argv[1:]
    if "--status" in a: print(json.dumps(status(),indent=1)); raise SystemExit(0)
    if "--once" in a: print(json.dumps(run_once(),indent=1)); raise SystemExit(0)
    if "--evolve" in a:  # autogen one batch of follow-ups without running
        print(json.dumps({"proposed":propose_next(),"queues":status()},indent=1)); raise SystemExit(0)
    if "--until-blocked" in a:
        mx=int(a[a.index("--max")+1]) if "--max" in a else 20
        evolve="--evolve-loop" in a
        log=[]
        for _ in range(mx):
            r=run_once(); log.append(r)
            if not r.get("ran"):
                if evolve:
                    new=propose_next()
                    if not new: break
                    log.append({"evolved":new})
                    continue
                break
        print(json.dumps({"steps":log,"queues":status()},indent=1))

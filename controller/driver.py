"""Driver: controller prompts OTHER agents. Default dry-run; real only with approval.

Builder protocol: build(prompt) -> {"ok", "gate_green", "tests_green", "log"}.
- DryRunBuilder: no subprocess, canned gate echo. $0, needs no approval.
- FunnelBuilder: wraps seed0 funnel isolated attempts via agent-cmd. Requires
  explicit allow_real=True AND env MINIME_ALLOW_REAL=1 (H4). Refuses otherwise.
Controller.run loops phases until ESCALATE/TOURNAMENT or max_steps, returns receipts.
"""
import os
from .phases import RECON, ESCALATE, TOURNAMENT, next_phase
from .router import prompt_for
class DryRunBuilder:
    name = "dry-run"
    def build(self, prompt):
        return {"ok": True, "gate_green": True, "tests_green": True,
                "log": f"dry-run accepted {len(prompt)} chars"}
class FunnelBuilder:
    name = "funnel"
    def __init__(self, allow_real=False):
        if not (allow_real and os.environ.get("MINIME_ALLOW_REAL") == "1"):
            raise PermissionError("real builder needs H4: FunnelBuilder(allow_real=True) + MINIME_ALLOW_REAL=1")
        self.allow_real = True
    def build(self, prompt):
        return {"ok": True, "gate_green": None, "tests_green": None,
                "log": "real run goes via funnel.py agent-cmd (isolated dir, H4 scope)"}
def run(goal, builder=None, seed=0, max_steps=6, **slots):
    builder = builder or DryRunBuilder()
    phase, receipts = RECON, []
    kw = {"goal": goal, "target": goal, "artifact": goal,
          "gate": "pytest tests/ -q + seed0.py check", **slots}
    for _ in range(max_steps):
        prompt = prompt_for(phase, seed, **kw)
        out = builder.build(prompt)
        gate = {"gate_green": out.get("gate_green"), "tests_green": out.get("tests_green"),
                "blocked": not out.get("ok")}
        receipts.append({"phase": phase, "prompt": prompt, "out": out})
        phase = next_phase(phase, gate)
        if phase in (ESCALATE, TOURNAMENT):
            receipts.append({"phase": phase, "prompt": prompt_for(phase, seed, **kw), "out": None})
            break
    return {"goal": goal, "builder": builder.name, "receipts": receipts, "end": phase}

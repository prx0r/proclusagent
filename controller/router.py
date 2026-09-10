"""Router: goal text -> phase; (phase, gate) -> prompt. Deterministic. Stdlib only."""
from .phases import RECON, SCAFFOLD, BUILD, VERIFY, next_phase
from .templates import render, TEMPLATES
FIRST_WORD = {"how": RECON, "what": RECON, "check": RECON, "build": SCAFFOLD,
              "deploy": SCAFFOLD, "create": SCAFFOLD, "upload": BUILD,
              "now": BUILD, "verify": VERIFY, "re-verify": VERIFY,
              "blocked": "escalate", "tournament": "tournament"}
def classify(text):
    w = (text.strip().split() or [""])[0].lower().strip("?")
    return FIRST_WORD.get(w, BUILD)
def pick_variant(phase, seed):
    return seed % len(TEMPLATES[phase])
def prompt_for(phase, seed=0, **slots):
    return render(phase, pick_variant(phase, seed), **slots)
def step(phase, gate, seed=0, **slots):
    return next_phase(phase, gate), prompt_for(next_phase(phase, gate), seed, **slots)

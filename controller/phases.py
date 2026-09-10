"""Phases + gate-driven transitions for the mini-me controller. Stdlib only."""
RECON, SCAFFOLD, BUILD, VERIFY, ESCALATE, TOURNAMENT = (
    "recon", "scaffold", "build", "verify", "escalate", "tournament")
PHASES = [RECON, SCAFFOLD, BUILD, VERIFY, ESCALATE, TOURNAMENT]
# gate_state keys: gate_green (bool|None), tests_green (bool|None),
# blocked (bool), costly (bool). Pure function: same inputs -> same phase.
def next_phase(phase, gate):
    if gate.get("blocked") or gate.get("costly"):
        return ESCALATE
    if phase == RECON:
        return SCAFFOLD
    if phase == SCAFFOLD:
        return BUILD
    if phase == BUILD:
        return VERIFY if gate.get("gate_green") else BUILD
    if phase == VERIFY:
        return TOURNAMENT if gate.get("tests_green") else BUILD
    return phase

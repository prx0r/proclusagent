"""The 10-key instrument: fixed digits, muscle memory safe. Stdlib only.

Positions NEVER move with learning (unlike suggestions). Data-grounded counts
from 8,497 sends in comments; library moves fill value slots. Chains like
"2943" resolve digit-by-digit into queued prompts.
"""
KEYS = [
    ("1", "continue", "continue"),                                     # 52 exact
    ("2", "yes", "yes"),                                               # 51 exact
    ("3", "go", "go"),                                                 # 18 exact
    ("4", "verify", "verify it and report back"),                      # review intent
    ("5", "drain", "run all a-tasks and log it all"),                  # library
    ("6", "zoom out", "zoom out: achieved vs missing?"),               # library
    ("7", "recon", "review until obvious: what is it?"),               # library
    ("8", "push", "push to git"),                                      # 21 exact; PROPOSES H (never executes)
    ("9", "h-queue", "show my open human tasks in priority order"),    # H-dashboard
    ("0", "mine", "type your own"),                                    # escape hatch
]
BY_DIGIT = {d: (label, text) for d, label, text in KEYS}
def resolve(chain):
    """'2943' -> ['verify...', 'push...', ...]. Raises KeyError on bad digit."""
    out = []
    for ch in chain.strip():
        if ch not in BY_DIGIT:
            raise KeyError(f"no key {ch!r} (want 0-9)")
        out.append(BY_DIGIT[ch][1])
    return out
def layout():
    return [{"digit": d, "label": l} for d, l, _ in KEYS]

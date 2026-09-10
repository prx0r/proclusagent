"""Prompt templates seeded from observed WAL families (shapes only, no raw chats).

Observed (37MB WAL, exact msgID join, secret-screened):
- interrogative: "how is a jsonl 1 gb whats in it?" (x31 frames, 1 send)
- ops-directive: "DB uploaded (5.7G). Now the rest:" (status + continuation)
- session-title openers (dbhead page): "Build Next.js ereader with ... modes",
  "Upload cleaned texts + site to Cloudflare Pages/R2", "Deploy to tantrafiles.xyz"
Each template has slots; variants preserve the observed phrasing shape.
"""
from .phases import RECON, SCAFFOLD, BUILD, VERIFY, ESCALATE, TOURNAMENT
TEMPLATES = {
    RECON: [
        "how is {target} {constraint} whats in it?",
        "check what completed and their sizes: {target}",
    ],
    SCAFFOLD: [
        "Build {artifact} with {modes}: scaffold {layout}, then report the tree.",
        "Deploy {artifact}: scaffold minimal, prove with {gate}.",
    ],
    BUILD: [
        "{artifact} {status}. Now the rest: {next_list}",
        "Upload {artifact} to {destination}, then confirm with {gate}.",
    ],
    VERIFY: [
        "Verify {artifact}: run {gate}, report green/red with the failing tail.",
        "Re-verify from {manifest} alone; list exactly what must re-run.",
    ],
    ESCALATE: [
        "Blocked on {need}: state options, recommend one, wait. Never guess.",
    ],
    TOURNAMENT: [
        "Tournament {seeds} on {task}: rank by compliance, suite, evidence; keep logs.",
    ],
}
def render(phase, variant=0, **slots):
    variants = TEMPLATES[phase]
    text = variants[variant % len(variants)]
    try:
        return text.format(**slots)
    except KeyError:
        return text  # slots optional; raw shape still valid

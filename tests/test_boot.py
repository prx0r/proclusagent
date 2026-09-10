"""Boot test: repo skeleton holds. Stdlib only. $0."""
from pathlib import Path
def test_required_docs_exist():
    root = Path(__file__).resolve().parent.parent
    for f in ["AGENTS.md","README.md",".env.example","docs/README.md","docs/RECIPES.md",
              "docs/FILES.md","docs/THREADS.md","docs/SYNTHESIS.md","docs/KERNELS.md"]:
        assert (root/f).exists(), f"missing {f}"
def test_no_committed_secrets():
    import re
    root = Path(__file__).resolve().parent.parent
    pats = [re.compile(r"cfat_[A-Za-z0-9_-]{10,}"), re.compile(r"ghp_[A-Za-z0-9]{12,}")]
    for p in list(root.rglob("*.py"))+list(root.rglob("*.md")):
        if ".git" in p.parts or p.name=="test_boot.py": continue
        try: t = p.read_text(errors="ignore")
        except Exception: continue
        for rx in pats:
            assert not rx.search(t), f"secret pattern in {p}"

"""Controller tests: determinism, transitions, dry-run loop, real-guard, no secrets."""
import re
import pytest
from controller.phases import next_phase, RECON, BUILD, VERIFY, ESCALATE, TOURNAMENT
from controller.router import classify, prompt_for, step
from controller.driver import run, DryRunBuilder, FunnelBuilder
from controller.templates import TEMPLATES
def test_classify_observed_shapes():
    assert classify("how is a jsonl 1 gb whats in it?") == RECON
    assert classify("DB uploaded (5.7G). Now the rest:") == BUILD
    assert classify("Verify foo: run pytest") == VERIFY
def test_variant_deterministic():
    assert prompt_for(RECON, 0, target="x", constraint="1gb") == prompt_for(RECON, 0, target="x", constraint="1gb")
def test_transitions():
    assert next_phase(BUILD, {"gate_green": True}) == VERIFY
    assert next_phase(BUILD, {"gate_green": False}) == BUILD
    assert next_phase(BUILD, {"blocked": True}) == ESCALATE
    assert next_phase(VERIFY, {"tests_green": True}) == TOURNAMENT
def test_dryrun_loop_reaches_tournament():
    r = run("demo widget", DryRunBuilder(), target="w", artifact="w", gate="g")
    assert r["end"] == TOURNAMENT and len(r["receipts"]) >= 4
def test_funnel_refuses_without_approval():
    with pytest.raises(PermissionError):
        FunnelBuilder()
def test_templates_have_no_secrets():
    pats = [re.compile(r"cfat_|ghp_|sk-[A-Za-z0-9]{6,}|AKIA")]
    for vs in TEMPLATES.values():
        for v in vs:
            assert not any(p.search(v) for p in pats)

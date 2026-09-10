"""Continue-policy tests: gate closed on real numbers, opens on separable data."""
from predictor.continue_ import is_variant, licensed, decide
def test_variants():
    assert is_variant("Yes") and is_variant("continue") and not is_variant("Build x")
def test_gate_closed_on_measured_numbers():
    # markov2 precision 0.2264 @ cov 0.031, kNN ~= base: never licenses
    assert licensed(0.2264, 0.031) is False
    assert licensed(0.84, 0.16) is False  # base-rate accuracy isn't precision
    assert licensed(None, 0.2) is False
def test_gate_opens_when_earned():
    assert licensed(0.96, 0.12) is True
    assert licensed(0.96, 0.01) is False  # coverage floor holds
def test_decide_routing():
    assert decide(True, 0.96, 0.12) == "auto_proceed"
    assert decide(True, 0.5, 0.2) == "buttons"
    assert decide(False, 0.96, 0.12) == "buttons"
    assert decide(True, 0.96, 0.12, blast_radius="high") == "h_delegate"

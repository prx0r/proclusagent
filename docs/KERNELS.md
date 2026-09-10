# KERNELS — P0-P7 ablation vs competitors (tournament plan, no code yet)

Proclus ladder (each adds exactly one primitive — ablation discipline):
- **P0** flat ReAct baseline
- **P1** hierarchy only
- **P2** hierarchy + procession (top-down decomposition)
- **P3** + reversion (evidence/error upward)
- **P4** + remaining/invariant constraint (preservation gate)
- **P5** + henadic parallel perspectives (competing decompositions)
- **P6** + truth-map competing ontologies (no premature collapse)
- **P7** full Proclus kernel

Competitors (same harness, same tasks):
- **T1** 36-tattva / Śaiva kernel
- **N1** Nāṇavīra-derived kernel
- **A1** active-inference kernel
- **S0** seed0 evidence-maximalist (baseline champion: seed3 won 5/5)

Tasks (identical for all, cogym worlds + real work):
cogym deterministic worlds, coding tasks, scientific inference, changing-evidence
(blast-radius/re-proof), long-horizon agent tasks.

Metrics (all mechanical first, LLM only as binary check above deterministic):
accuracy, calibration, recovery-after-contradiction, context usage, token cost,
tool calls, catastrophic-commitment-to-false-hypotheses, performance-after-upstream-change.

Gates per kernel (QDW ladder, lifted):
V0 compile → unit → property → adversarial → fixtures/Docker → E2E → live → CI.
Certificate per claim: IMPLEMENTED_UNVERIFIED / PROVEN-MECHANISM / PROVEN.
Memory control: every kernel runs with and without MemoryProof-optimized retrieval;
report both (architecture Δ = with-memory minus retrieval-only gain).
Dependency rule (Alethiea): upstream change → recompute descendants only;
log proof obligations, not full reruns.
Representation rule (patalacheckpoints): typed edges with confidence + evidence,
data graph canonical.
Branching rule (hxrmxs): maintain ≥2 incompatible ontologies until falsifier fires.

Promotion rule (unchanged): only kernels with native tests or mine-side boot_test
enter `seeds/seed6-arch-*`. Real `funnel.py run` only after H4.

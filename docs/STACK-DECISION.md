# STACK DECISION — not a graph thing, not a LoRA (yet). Retrieval + interpolation.

## Review: what's real vs theater in our plan/testing
**Real:** exact msgID join (caught a misattribution bug mid-session), dedupe-by-ID
(WAL repeats frames ~30x — naive counts lie), schema recovery from 5MB prefix,
secret quarantine (keys ARE in logs), mechanics tests (determinism, transitions,
refusal guards), Smart-Compose-shaped interpolation with an α-sweep harness.
**Theater risks, named:** 20 tests assert mechanics, not predictive power;
hit_rate_top1 demo used simulated accepts (circular); FunnelBuilder never met a real
funnel (needs H4); MCP subprocess tests prove plumbing, not latency.
**Pilot verdict (real sample, honest numbers):** 37MB WAL → **2 unique sends**
after msgID dedupe (36 joined parts collapse), 2 families, LOO hit-rate **0.0 at
every α** — mathematically forced at n=2 with distinct families/sessions. The
harness works; the signal needs the full pull (H6). No claim beyond this is licensed.

## Verdict with frontier receipts
- **Prediction stack = retrieval + interpolation + online Bayes** (built: pilot.py,
  scorer.py). Smart Compose (Chen et al. KDD'19): personal n-gram + global neural LM,
  P=αP_personal+(1-α)P_global, α=0.4 optimal, +6% CTR/+10% ExactMatch. Our scorer is
  the same shape with Laplace smoothing; α-sweep harness mirrors their Figure 4.
  LaMP systematic study: RAG +14.92% vs PEFT +1.07% alone, combined 15.98%;
  RAG wins cold-start, PEFT gains grow with data volume. We are cold-start → retrieval.
- **Not a graph model.** Next-prompt prediction is sequence/retrieval, not message
  passing. The graph that DOES exist — session→project→directory→prompt relations
  already in the schema — is used as retrieval structure (same-session bonus = our
  P_session term; PGraphRAG shows this beats flat history when sparse). Dependency
  graphs belong to the reasoning layer (Alethiea blast-radius), never the predictor.
- **Not a LoRA — gated.** OPPU/Per-Pcs/MTA/PROPER + LaMP correlation agree: PEFT needs
  volume; at n=2 it memorizes noise. Gate: choice log ≥500 turns AND hit-rate plateau
  AND H/M approval (GPU). Then: single-user LoRA r=4–8 (MTA stacking logic says
  ultra-low-rank suffices few-shot) on (context→picked), DPO/IRPO on
  (picked≻rejected) listwise pairs from shown-sets. IRPO (2025) is the exact
  listwise-feedback objective for our button UI when data arrives.

## Ladder (each rung gated by the previous one's numbers)
rules+retrieval ($0, built) → choice log (needs UI) → α tuned on full pull (H6) →
DPO/IRPO on pairs → LoRA r=4 (M) → combine (frontier says +15.98% class gains).
Skip a rung only with a number that licenses it.

# GPU PLAN — what 13,412 pairs + money actually buy (2026-09-10)

Data ready NOW (/tmp, scrubbed, never repo): `sft_box1.jsonl` (8,497) +
`sft_box2.jsonl` (4,915) as `{context, response}` (context = title+prev+proj/
agent — best proven recipe). Builder: `predictor/export_sft.py` (tested).

## Ladder (each rung gated by beating the previous rung's number)
0. **Baselines (done, $0):** fastText text→family 0.807 · linear ctx→family 0.44.
1. **SFT LoRA, Qwen3-0.6B or TinyLlama-1.1B, r=8, lr≈2e-4** (LaMP recipe: 50 epochs
   is overkill at our size — start 3 epochs, batch 16). Eval: family-match of greedy
   generation on frozen test + perplexity. Success bar: beat 0.44 ctx→family.
   Cost: Colab free T4 first ($0); fallback below. Time: <1h.
2. **KTO on choice-log pairs** (pressed=desirable, dismissed=undesirable; lr 1e-6,
   LoRA-only, 16GB card). Needs live UI data — NOT runnable on mined history
   (no counterfactuals). Queued behind buttons.
3. **Dense retriever** (E5/Contriever fine-tune on pairs) to replace Jaccard kNN.
   Same GPU session as (1) if time remains.
4. **ORPO/SimPO** when real picked-vs-rejected pairs exist (choice log mature).

## Why this order (frontier receipts)
- RAG +14.9% vs PEFT +1.1% cold-start; combined +16% (LaMP systematic study).
  Our retrieval stack stays; GPU adds the parametric half.
- LoRA+ best energy, QLoRA 3.9× VRAM cut, TinyLlama leads efficiency (PEFT study).
- PRISP: 10 shots/user suffice with Qwen3-0.6B — our 13k pairs are lavish.
- KTO fits our future telemetry exactly (unpaired binary); ORPO fits pairs later.

## M6 PROPOSAL (needs explicit `approve M6 cap=$25 ...`)
Pilot GPU session: rent 4090-class hourly (vast.ai/lambda-type marketplaces,
~$0.40–0.80/hr — verify at rent time, prices move). Budget: ≤3 hrs + buffer =
**$25 cap**, single purpose (rung 1, +3 if time), kill on first green eval.
Limitations enforced: cap hard-stops spend; base model fixed (Qwen3-0.6B);
eval frozen BEFORE training (no tuning on test); artifacts (adapter ~50MB) return
to /tmp, never secrets. Human runs the rental (I hold no cloud accounts) OR
provides access — say which. Colab-free attempt first if you prefer $0.

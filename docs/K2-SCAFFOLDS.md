# K2-SCAFFOLDS — P0-P4 draft specs (local-only drafts, NO funnel run, needs H4 to execute)

K2 = checkpoint/evidence bake-off: patalacheckpoints (SPINE) vs sanskritree
(provenance pipeline) vs knowledge-base-organism (contract convergence).
Task (identical): checkpoint one claim with hash + manifest + audit line;
re-verify from manifest alone.

- **P0 flat baseline**: single script, no hierarchy. Input claim text → sha256 →
  manifest.json. Gate: re-read manifest, recompute hash, PASS/FAIL.
- **P1 +hierarchy**: manifest nests claim → evidence[] → audits[]. Same gate +
  schema check (required keys).
- **P2 +procession**: top-down decompose: claim → 2 sub-claims, each hashed;
  parent hash covers children. Gate: children verify + parent covers.
- **P3 +reversion**: mutate one evidence line → expect exactly 1 descendant FAIL +
  1 proof obligation emitted (Alethiea rule). Gate: blast-radius == 1, no full rerun.
- **P4 +remaining**: invariant line (epistemic ceiling) pinned; mutation of invariant
  → hard FAIL closed with `IMPLEMENTED_UNVERIFIED` withheld (QDW rule).

Each scaffold = future `seeds/seed6-k2-pN/` (AGENTS laws + README + boot test +
.env.example). Drafts only — promotion + `funnel.py run` waits on H4.
Metrics: accuracy, blast-radius precision, tokens, context. Memory control both arms.

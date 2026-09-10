# PROMPT-LIBRARY — copy-paste prompts for any HAM-framework agent/codebase

Mined from 21 verbatim specimens (`prompts/corpus.jsonl`: 16 session prompts + 5 WAL
prompts) via `predictor/cluster.py` → 10 emergent categories
(`python3 predictor/cluster.py prompts/corpus.jsonl`). Compounds flagged (p13/14/15/16
carry secondary markers — use both templates). This file is the ML baseline: new prompts
append to the corpus, re-run the clusterer, categories evolve with evidence.

Conventions: {SLOTS} you fill. Every template ends with its HAM split + validation +
evidence + log destination. Specimen refs (pXX/wXX) prove each template is used, not invented.

## 0. TRIGGER — one-word macros (specimens p01-p04)
When: resuming work, zero context cost, conventions already established.
- `a-tasks.com` = drain all open A-tasks ($0, reversible), log to a-logs, stop at H/M bottleneck.
- `a-loop.com` = run the recursive loop until blocked (`--until-blocked --evolve-loop`).
- `greatcontinue.com` = continue next queued A-work under the same conventions, no recap needed.
- `hamharness.com` = operate strictly via H-A-M registries; log everything; never touch H/M without approval.
Validation: queue counts move (open→done), receipts exist. Evidence: `runs/sha256_*`. Logs: a-logs.

## 1. DRAIN-REPORT (p05, p06)
When: open work exists; end of a work block.
Template: `ok run all a-tasks and log it all to {LOG} then review and suggest next a-tasks with justification and how you validate and supply the evidence for them`
HAM: A executes; H/M queued never run. Validation: queue 0-open + receipts per task. Evidence: run log + test tails. Logs: a-logs.

## 2. ZOOM-OUT (p07; compounds p13)
When: checkpointing, planning next, context getting long.
Template: `ok document all progress and zoom out: what have we actually achieved so far ({EVIDENCE_ONLY}) vs what are we missing, then propose next steps with why`
HAM: A writes docs; nothing executes. Validation: every achieved-claim cites a receipt/file. Evidence: HANDOVER-style doc. Logs: a-logs.

## 3. EXPOSE (p08)
When: finished work needs an agent-consumable surface + verification.
Template: `ok now make all of {SCOPE} accessible via mcp so u can test all the {SURFACE} features headlessly`
HAM: A builds stdio tools + round-trip tests ($0 local). Validation: per-tool round-trip green. Evidence: pytest tail. Logs: a-logs. H/M: deploy/publish = H, infra spend = M.

## 4. BEAUTIFY-NONDESTRUCTIVE (p09, p11, p13)
When: entropy cleanup, pre-commit, onboarding readability.
Template: `ok make {SCOPE} beautiful: create mini stale folders everywhere, move only {SAFE_CLASS}, long titles stating the alpha in each, work autonomously, dont rewrite or break anything in {PROTECTED}`
HAM: A adds/moves-only-junk; any history-adjacent move needs H cover. Validation: `seed0.py check` still green + `git status` clean-move list. Evidence: check tail. Logs: a-logs.

## 5. RECON-UNTIL-OBVIOUS (p10)
When: new domain/codebase, thesis formation.
Template: `review all of {TARGET} and adjacent {ADJACENT} until its obvious what it is, then tell me what u think it is: {THESIS_QUESTIONS}`
HAM: A read-only (API/sparse/metadata); clones deleted after. Validation: thesis doc cites files+SHAs. Evidence: recon notes. Logs: a-logs. H/M: deep private/giant dives = H.

## 6. GOAL-WITH-CHECKPOINTS (p12, p14; compounds p14)
When: multi-step vision needing gated decomposition; spend-gated steps inside.
Template: `save this as explicit goal, your only target: {VISION}. break it into checkpoints e.g. checkpoint 1 {FIRST_EVIDENCE}. create the checkpoints then work autonomously. {SPEND_STEPS} are M-tasks with caps and need my button; {IRREVERSIBLE} are H-tasks`
HAM: A does read-only checkpoints; spend/publish auto-queued H/M. Validation: per-checkpoint binary evidence. Evidence: checkpoint receipts. Logs: a-logs.

## 7. FRESHNESS-CHECK (p13 compound beauty×zoom)
When: resuming, prioritizing, doubting currency.
Template: `ok now review all {THREADS}: is it stale? what shall we do next — {DECISION_OPTIONS}`
HAM: A reads + proposes order; human decides. Validation: priority list with unlock counts. Evidence: threads note. Logs: a-logs.

## 8. MECHANISM-DESIGN (p15; compounds p16)
When: designing persistent systems (registries, locks, streams, wallets).
Template: `{A_STREAM} appends {A_TASKS}; removal only via {RETIRE_RULE}. {M_STREAM} is locked: {LOCK_MECHANISM}; spend needs {APPROVAL_UX} capped at {CAP}. {H_STREAM} is parallel: human supplies via {INTERFACE}, agent polls every {INTERVAL}, maintains unlock graph + priority order. research {PREBUILT} before building`
HAM: A implements state machine + refusal tests; money math spec'd never executed. Validation: refusal/double-spend/over-cap/revoke tests green. Evidence: pytest tail. Logs: a-logs.

## 9. METHODOLOGY-TOURNAMENT (p16; compounds p14/p15)
When: validating the way of working itself.
Template: `review all done and test it scientifically as tournaments: encode {MECHANISM} + {REGISTRY} + {AUTONOMY_RULES} + {LOGS} as seeds with hypotheses, falsifiable evidence per cg logic, falsification criteria in criteria files, document the metaguide (schemas + why + exact commands), run it all, log process notes`
HAM: A builds seeds + collect-only runs; real agent runs = H, spend = M. Validation: validator exit 0 + tournament receipts. Evidence: leaderboard + scores.jsonl. Logs: a-logs.

## 10. INTERROGATIVE (w01) / 11. OPS-DIRECTIVE (w02-w05)
When: quick recon question / status + continuation in active work.
Templates: `how is {TARGET} {CONSTRAINT} whats in it?` / `{ARTIFACT} {STATUS}. Now the rest: {NEXT_LIST}`
HAM: A read-only answer or continues queued work. Validation: cited facts / queue movement. Logs: a-logs.

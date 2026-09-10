# EXPERIMENT-DESIGN — mini-me prompter (full, after sample verdict)

## Hypothesis
Your most common prompts + variants cluster into a small set of driver intents
(scaffold / build-loop / verify / recon / escalate / tournament), each with a
phase signature (session context + model/agent + permission outcomes). A state
machine that picks the right template per phase directs builder models better
than any single system prompt.

## Phases
- **P1 pull (needs H6/M5)**: full `opencode.db` (6.09GB) + WAL (37MB) to scratch
  disk (`/tmp`, never repo; ~10GB free needed). Read-only open, `.tables`/`.schema`,
  row counts (sessions/messages/tool-calls). Secret-scan immediately; quarantine dir.
  Egress $~0 (R2 zero-fee), cost = disk + hours. No publish, ever.
- **P2 cluster ($0 local CPU)**: user messages → normalize (lowercase, strip
  paths/ids/hashes) → exact dedupe → near-dedupe (Jaccard/edit-distance; embeddings
  only if M1) → top-N families → join to log telemetry (model/agent/phase/outcome) →
  P(family|phase) + success proxy (gate-green-next?). Output: prompt-family table
  (template + variants + when + why + N + success rate). Shapes only, no raw secrets.
- **P3 harness ($0, needs H4 to run)**: states scaffold/build/verify/escalate/
  tournament; transitions on gate outputs (`seed0.py check`, pytest, funnel scores);
  per-state template with slots (goal/constraints/evidence). Implement as
  seed0-compatible kernel (`seeds/seed6-prompter`) + boot test.
- **P4 bake-off ($0 local + H4)**: prompter-kernel vs S0 evidence-maximalist vs flat
  baseline on identical tasks (cogym world + coding + inference). Metrics: build
  success, gate pass, recovery-after-contradiction, tokens, tool calls,
  catastrophic-commitment. Memory control both arms (Iolaus rule).

## Gates & guards
QDW certificates per claim; Alethiea descendant-only recompute for prompt edits;
secret-scan gates every output (fail closed — this sample already found keys in logs);
raw chats never enter repo, packets, or receipts (shapes + counts only).

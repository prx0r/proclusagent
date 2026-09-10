# SAMPLE findings — ~6MB pull (2026-09-10, /tmp/opencode-sample/, NOT in repo)

Pulled (egress ≈ 6.3MB, ~$0; R2 has zero egress fees): smallest tool-output blob
(51KB), `log/opencode.log` tail 1MB (Range), `opencode.db` head 5MB (Range).
Secret-scan: log tail CONTAINS live-looking AWS-style keys → **raw logs are
quarantine-grade**: never publish, never paste, scan before quoting (this doc
quotes shapes only).

## What each sample actually yields
- **tool-output blob**: web-fetch output (paper title/URL/published/highlights/body).
  = research-evidence shape, NOT prompter data. Tells us what the agent read, not how you drive it.
- **log tail**: session telemetry gold. Per-line fields: timestamp, level, run id,
  `session.id=ses_…`, `messageID=msg_…`, provider/model (`opencode-go`/`mimo-v2.5`),
  `agent=build`, `mode=primary`, loop steps, permission evaluations
  (tool pattern → allow/deny). = WHEN/WHY join keys: prompt → session → model/agent →
  permission outcome → loop step. No prompt TEXT in this tail (process/stream markers only).
- **db head 5MB**: SQLite magic confirmed, but `database disk image is malformed`
  on query — partial image can't satisfy b-tree. Schema/tables NOT recoverable from
  prefix. Prompt text lives in the db → needs the full file.

## Verdict
Sample proves the join is possible (session/message/model/agent/permission telemetry
in logs + prompt text presumably in db) and sets the quarantine rule (keys in logs).
It cannot yield a single real user prompt. Full experiment needs the 6.09GB pull.

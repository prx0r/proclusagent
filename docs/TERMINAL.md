# TERMINAL PROPOSAL — buttons in your shell (approve to apply, $0, reversible)

## What you'd get
A shell command `p` available in every terminal: type options, get your ranked
top-3 (learned from your presses), Enter/1/2/3/type, choice logged. Plus `pt`
(ask type first). Works for opencode AND everything else (email, commits, plans).

## Exact change (one append to `~/.bashrc`, nothing else)
```bash
# mini-me suggest bar (added 2026-09-10, remove to rollback)
p() { (cd /home/ubuntu/proclusagent && python3 -m predictor.cli --session term --options "$@" < /dev/tty); }
pt() { local t="$1"; shift; (cd /home/ubuntu/proclusagent && python3 -m predictor.cli --session term --type "$t" --options "$@" < /dev/tty); }
```
Usage: `p ok "verify it" "ship it"` · `pt ack ok yes continue` · `p "deploy it" "wait"`.
Learning persists in `predictor_choices.jsonl` (same file the MCP tools use —
one shared brain across terminal, CLI, and opencode).

## What this does NOT do (honest limits)
- No inline rendering inside opencode's TUI (needs fork patch — separate H decision).
- No shell-history mining (would enrich context; privacy call, propose later).
- No auto-execution (gates from CONTINUE.md still rule; terminal only suggests+logs).

## Risk + rollback
Risk ~zero: two shell functions, no existing aliases touched (`p`/`pt` verified
free in your shell — confirm on apply), no daemons, no network. Rollback: delete
the 4 lines, `source ~/.bashrc`. Verify after: `type p` shows the function;
`p ok` prints 3 scored options.

Reply `apply terminal` and I append + verify + log. Anything else first, say so.

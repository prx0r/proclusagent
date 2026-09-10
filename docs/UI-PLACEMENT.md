# UI PLACEMENT — where buttons live (decision needed from you)

Three targets, same contract (Enter=top, 1/2/3=pick, type=dismiss; every outcome
logged via `predict.log_choice`). Engine is ready (`predictor/` + MCP tools).

## Option A — opencode fork (TUI)
Patch the input component: ghost placeholder + keybinds (qwen-code NES pattern:
`useFollowupSuggestions` hook, Tab/arrows, dismiss-on-type, 11 guard conditions).
Needs: fork repo URL + which input component + your keybind conflicts.
Best fidelity, biggest build.

## Option B — desk web UI (your cmail-style desk)
Buttons under each agent reply (ago/assistant-ui pattern: `ThreadFollowupSuggestions`
chips + engagement analytics). Needs: desk codebase path + deploy target.
Best analytics, medium build.

## Option C — CLI wrapper (today, $0)
`predict suggest` CLI printing top-3 + reading `1/2/3/<enter>/text` from stdin,
appending to the choice log. No fork, no deploy, works this session.
Needs: nothing — say `build C` and it exists.

Recommendation: C now (unblocks live data this week), A or B when C's numbers
justify the build. Reply `build C` / `spec A` / `spec B`.

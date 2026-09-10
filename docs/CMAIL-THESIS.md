# CMAIL-THESIS — what cmail + adjacent obviously are

Reviewed: cmail AGENTS.md + docs/GUIDE.md (API), cmail T1 packet (13 root files),
voiceagent/StallSpy/domainarena/lifeOS READMEs (API), recon trees. No clones kept.

## Each piece
- **cmail**: agentic business stack. Bus = Cloudflare Worker + MailboxDO + D1 + R2,
  MCP-first, drafts queue, injection quarantine. Brain = stevejobless kernels (jobs,
  quotes, slots, feed, invoices/VAT, Telnyx/LiveKit/Google backends). Names =
  domainnamechecker (DNS+RDAP verify, registrar compare, claim kits). Voice track in
  voiceagentfeedback/. Live traffic: brain `steve.intelligentothers.xyz`, bus
  `cmail.tradesprior.workers.dev`, checker `domainnamechecker.tradesprior.workers.dev`.
- **voiceagent**: reusable graph-grounded support/receptionist kernel (`.env.example`,
  requirements, adapters/app/graphs/knowledge) — the swappable voice face of cmail's brain.
- **StallSpy/StallShark**: commerce trajectory corpus — machine-readable record of
  building microbrands (MythicBee 001, Game Winner 002). Proof-of-outcome dataset.
- **domainarena**: A/B testing for domain names (148 tests passing) — experimental
  front for the name-intelligence inside cmail.
- **lifeOS/SVATANTRYA**: git-native personal OS (knowledge graph + dependency tracker
  + web app; graph content-addressed, renders site). Same graph instinct as KBO, personal scale.
- **tomzoho**: Zoho mail/domain management agent (TypeScript; README 404 on default branch —
  needs direct tree read; treated as mail-admin satellite until verified).

## The obvious thesis
**cmail is the live commercial front-end of the entire prx0r stack — the only repo
serving real traffic with money-movement guardrails** (approval tokens, ≤10% price-drift
recheck, human-confirm every send, additive-only live surfaces, prove-it-live receipts).
Everything else is its supply chain: oracles/factories find opportunities → domainarena
tests names → checker buys/wires → brain runs jobs → StallShark records outcomes →
voiceagent answers the phone. proclusagent/seed0/cogym are the lab; cmail is the till.
That is why its AGENTS.md is the strictest in the org (untrusted-stays-untrusted,
human-sized queue) and why MINE-SPEC inherits its secrets rule.

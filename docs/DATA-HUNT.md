# DATA-HUNT — UK L2 mission log (2026-09-10, $0, nothing gated touched)

Mission rule honored throughout: public + free + no-auth only. Gated/commercial
flagged H/M, never touched. Data stays in /tmp (never pushed); repo holds
method + verdicts + hashes only.

## ROUND 1 — FI-2010 bootstrap + corrections + fingerprints
**OBTAINED** (`/tmp/data-hunt/fi2010/`): FI-2010 via `zcakhaa/.../data/data.zip`
(56MB zip, sha256 in `provenance.json`): Train (149, 254750) + Test7/8/9, layout
proven from CS289's loader notebook — 149 ROWS per event (0–39 raw 10-level LOB,
40–143 engineered u2–u9, 144–148 labels k1–k5 ∈ {1,2,3}), columns = events,
whitespace-delimited, normalized. Score **~26**. Gaps: NOT LSE (Finnish), NOT MBO
(L1 snapshots, no order ids), 10 days 2010, license customary-research (local only).
**Corrections**: CS289 has NO data/ dir (README-only; files never pushed).
eddieeeezz = code/format ref only (self-generated parquets). SuibeAI
`prepare_data.sh` was the pointer that paid. Fingerprints: test_Xy→self-gen dead
end; FI-2010 parquet→pipelines; VOD.L→LSEG sample + HKUDS follow-up; LOBSTER/
MarketByOrder queries→noise. GitGoblin verdict: builder-graph engine, NO code
search — fingerprints go direct API.

## ROUND 2 — GitGoblin run + real LSE order data
Mission config, 4 seeds, expand 1+2: PASS with receipts, **0 signals** (needs live
expert convergence; stale quant repos don't trip it). Repo-search consolation →
**GSK LSE orders**: `raphi6/...LSE` (0 stars, exact profile) commits Data.zip:
detail 274,322 + history 322,208 + trades 130,136 rows (726,666; ~60 dates
Jan–Mar 2007; GB0009252882; GBX; order IDs; lifecycle + trade tables). Score **~33**.

## ROUND 3 — prize clones + storage-scar queries
Cloned: `lse-gsk-data` (42MB), `cs289-deeplob` (docs, no models), `itch-parser`
(Rust 408KB), `lseg-orderbook` (README + MBP parser). MSc dissertation (exact
profile) → TWO Drive IDs + Kaggle mirror (gated, H): TEST ID downloaded clean
(52MB; 31,938 events × 150 cols = index + 149 FI dims; processed variant
confirming transpose reading); TRAIN ID dead. Score ~20. KRX = code-only.
figshare/zenodo/BDLOB/ITCH-parquet = noise. Rule refined: exact-phrase REPO
search + download-script grep beat broad queries.

## ROUND 4 — scobre Rosetta + validation world
**scobre** (Phelps CCFEA): exact DAO case classes 17/15/17f, field-verified;
`replay-orders -t GB0009252882` (same ISIN/window). Enabler score ~15.
Schema decoded (A/M/D/P/E actions; NO adds in history — adds live in snapshots).
**Fidelity UPGRADED**: messageSequenceNumber restores within-second order —
queue_priority_safe TRUE (35 violations / 322,208 = 0.01%).
**Adapter + known-answer tests** (`/tmp/data-hunt/lse-gsk/adapter/`): 4 synthetic
green; real 322,208 events (cancel 201k/modify 68k/P 48k/E 4k; 72,647 outstanding).
LSE.txt universe (6,237 symbols) pulled. 2018 prints partial (2× 403 — retry later).

## ROUND 5 — outstanding grabs (2026-09-10, $0)
- Retried 2018 prints post back-off (clean 200s, no 403): both return MILLIONS of
  generic hits — unusable phrasings, logged as negative (exact-phrase only rule).
- lob-benchmarking cloned: setup_data.sh = THIRD independent pointer to zcakhaa
  data.zip (FI canonical source triple-confirmed); pipeline layout kept as reference.
- Databento /pcaps = JS app (1.5MB, no direct links) → human-visit H-task as above.

## ROUND 6 — reconciliation verdict: events proven, book-state falsified (2026-09-10)
Claim tightened per review: `event_order_safe=high`, `queue_reconstruction_safe`
was provisional → now tested. Date parsing bug found+fixed en route (DDMMYYYY
string-sorted months together; all prior sweeps re-ran clean).
- PASS exact: trade join 48,213/48,213 (100%) · cancel-before-add 0 · negative
  floors 0 · seq monotonic 99.99% (35 P-dominated inversions flagged, preserved).
- FAIL with evidence: intraday books 75% crossed (locked 0); clean-book median
  spread 1107bps vs real ~5–10bps; cross depths to 238p. Cause: structural
  staleness (no expiry/auction semantics; 07:5x auction entries coexist at 14:00;
  crossing grows 4% pre-open → 68% close). Zero-price MO rows excluded from levels.
- Invariants: #1 no-negative PASS · #2 orphans 0.0 PASS · #3 price-via-modify
  UNVERIFIABLE (M carries qty 0 by design) · #4 bid<ask FAILS broadly (above).
- Scores (3-axis): Acquisition 9/10 · Market fidelity 8/10 events, 3/10 book state ·
  Model utility 8/10 validation-world, 4/10 training.
- Standing: GSK = proven EVENT corpus + execution-validation world; NOT a resting-
  book reconstructor. Every future dataset plugs into the same canonical schema +
  invariant battery (`/tmp/data-hunt/lse-gsk/adapter/`).

## NEXT (gated or next-A)
- A (free): LSEG parsers/fixtures; ITCH 10-min sample (cap 1GB) → parquet pilot
  (runs AFTER validator green — validator now exists, unblocked); MSc-test variant
  eval; expiry/auction-semantics research for book-state v2.
- H: LOBSTER signup; Cboe sample form; HF/Kaggle gated approvals; Databento
  manual pull (`ny4-xnas-tvitch-a-20230822T133000.pcap.zst` → /tmp/data-hunt/nasdaq_itch/).
- M: Cboe full, LSEG live, Databento over-sample — caps first.

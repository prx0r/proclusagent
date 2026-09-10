# R2 opencode-backup — read-only survey (2026-09-10)

Method: token verify (`tokens/verify` → active) + S3 ListObjectsV2 only.
Secrets via env only, never written to tree. Zero downloads, zero egress.
Cost: ~30 LIST ops (fractions of a cent). No manual actions taken.

## Buckets (36)
amoltwork, artifact, atlas-sources, bear-dashboard, blog-video-assets, cmail-raw,
domain-checks, drop-docs, essayaudio, essayviz-videos, fablecut-projects,
factory-assets, freak-town, goldrender-videos, hydradb, longform-audio,
**opencode-backup**, patala, patala-organism, patala-site, patalafinal, qdw,
research-datasets, sacred-art, sanskritree, sauron1, source-library,
sourcematerial, stallshark, star-at-night, svatantrya, tantraloka-site, tiro,
tiro6590, unignorant-docs, uploads.

## opencode-backup: 17,016 objects, 9.10 GB (not 5 — bigger)
- Root (6): `opencode.db` 6.09GB (SQLite — almost certainly the chat/session store),
  `opencode-snapshot.tar.gz` 977MB, `opencode.log` 208MB, `opencode-tool-output.tar.gz`
  166MB, `opencode.db-wal` 37MB, `opencode.db-shm` 32KB.
- `log/` (1): `log/opencode.log` 208MB (≈ dup of root log).
- `tool-output/` (47 sampled): `tool_…` blobs ~40-600KB each (tool call outputs).
- `snapshot/` (16,962): 2 git snapshots
  (`58253b48…`, `6c6f2761…`) — mostly `.git/objects/pack` + hooks/refs (one tmp_pack
  312MB, one pack 90MB, one index 8MB). i.e. repo snapshots, not chat.
- Latest write seen: `opencode-tool-output.tar.gz` 2026-09-06.

## Answer to "chat history right?"
Yes. Usable chat history = `opencode.db` (6.09GB) + WAL (37MB) + logs (208MB) +
tool-outputs (47 objects + 166MB tar). The 977MB snapshot tar + `snapshot/` packs
are code snapshots, secondary.

## Not done (needs approval)
- No downloads, no SQLite queries, no tar inspection (would be GBs of egress + disk).
- Next if wanted: targeted pull (e.g. `sqlite3 opencode.db .tables` on a streamed
  copy, or range-GET the tar manifests) — see H6/M5 in QUEUE.

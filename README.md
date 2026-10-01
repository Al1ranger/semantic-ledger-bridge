# SemanticLedgerBridge

A reusable GenLayer reconciliation primitive for **two bookkeeping exports**. It produces an indexed one-to-one match table and explicit unmatched sets. It is not a graph transition, risk gate, text sanitizer, certificate, or payment settlement.

## Problem and GenLayer boundary

Two organizations may describe the same charge differently. Identical amounts alone cannot identify a match: in the demo, hosting and security assessment both cost USD 120. The contract constructs two GitHub raw URLs from separately pinned repository, commit, and path coordinates. The caller never supplies ledger rows, a pair vector, or a confidence score. Leader and validators independently fetch and hash each body, parse bounded rows, and semantically map descriptions while enforcing exact amount, currency, one-to-one, and known-ID constraints. They must agree exactly on the complete pair vector, residual IDs, source hashes, and deterministic report root before the contract indexes any match.

```text
register_batch(two pinned source coordinates)
                   │
                   ▼
reconcile ── fetch both JSON exports ── verify bounded row shape
                   │                           │
                   └── semantic description matching + exact validator recomputation
                                               │
                      ┌────────────────────────┼───────────────────────┐
                      ▼                        ▼                       ▼
                 RECONCILED                 PARTIAL               UNRESOLVED
              all rows paired          residual sets remain      no pair indexed
```

The useful output is `get_match(batch_id, left_id)`, backed by an immutable batch-scoped index. `get_report` exposes the complete matched and unmatched vectors with source hashes. A completed reconciliation is terminal, preventing model re-sampling until a desired mapping appears. A source fetch failure is `UNAVAILABLE`, creates no matches, and can be retried. Malformed source data is terminal `INVALID_SOURCE`.

## Trust limits

This reconciles **what two fetched exports say**. It does not establish that either export is a true account of payments or authorize transfer of funds. The fixtures are synthetic demonstrations; both are hosted in this repository, so they are not independent authorities. Real integrations should pin exports from their actual providers using separate repository coordinates. The model can still make semantic errors; validators independently rerun the matching task, and deterministic guards reject mismatched amounts, duplicate IDs, and hallucinated records. Uncertain records should remain unmatched.

## Demo

- [Complete left](fixtures/left-complete.json) versus [complete right](fixtures/right-complete.json): equal-value hosting and audit charges require semantic disambiguation; three pairs should be indexed.
- [Partial left](fixtures/left-partial.json) versus [partial right](fixtures/right-partial.json): a USD 50 lunch and a USD 50 cleaning charge must remain unmatched despite equal amounts.

See [LIVE_PROOFS.md](LIVE_PROOFS.md) for finalized StudioNet receipts and the exact deployed source check.

## API and checks

`register_batch`, `reconcile`, `get_batch`, `get_report`, `get_match`.

```powershell
genvm-lint check contracts/SemanticLedgerBridge.py
python -m pytest tests/direct -q
genlayer network set studionet
genlayer deploy --contract contracts/SemanticLedgerBridge.py
```

For a live batch, call `register_batch` with a unique batch ID and four coordinates for each side: GitHub owner, repository, 40-hex commit, and path. Then call `reconcile(batch_id)` and inspect both `get_report` and the transaction's leader execution result. A `FINALIZED` transaction with an execution error is not a proof. The runner version is pinned in the contract header.

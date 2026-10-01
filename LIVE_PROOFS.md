# StudioNet proofs

Only transactions independently checked as `FINALIZED` with leader execution `SUCCESS` belong here.

## Deployment

- Contract: https://explorer-studio.genlayer.com/address/0x360181F8c8EfcDd1cF2d4254AE1e274bAC6b065f
- Transaction: https://explorer-studio.genlayer.com/tx/0xb960c5c575935fe124e4a1516d61503d8e38e059f9a4e9afadad9a2a65a3724f
- StudioNet RPC reported `FINALIZED` and leader execution `SUCCESS`.
- The deployed source returned by `genlayer code` exactly matches `contracts/SemanticLedgerBridge.py` after newline normalization; normalized SHA-256: `83d52057513fc673bee23be21e1ca39a1ebf8e8ca2a1e720a43d3de5e2eb194e`.

Both synthetic exports are publicly available at commit `b5fb5b3b639cb9dcfa2cb39565d374a4a08ce601`. They demonstrate matching behavior, not verified financial activity or independent source authority.

## Complete semantic reconciliation

- Pinned left/right fixtures: `fixtures/left-complete.json`, `fixtures/right-complete.json`.
- Reconciliation: https://explorer-studio.genlayer.com/tx/0x63e605702432b0bdad1b89b66ea9fc0021e0af1ca1cf23a12da30c72fe59e446
- RPC: `FINALIZED`, leader `SUCCESS`, `MAJORITY_AGREE`. Stored report: `RECONCILED`, both HTTP statuses 200, three one-to-one pairs, no residuals, report root `a17413c3e238cbdd74ca20c74230f7deebee96d209bda01e68299256eeeeb9f7`.
- Readback: `get_match("demo-complete-v1", "l-host")` returned `r-infra`; the two same-dollar charges were disambiguated by descriptions.

## Equal-amount negative case

- Batch registration: https://explorer-studio.genlayer.com/tx/0x431a2f8b5ff951e002d5b531210111e3b877db030184024576465631ab516018
- Reconciliation: https://explorer-studio.genlayer.com/tx/0xdaca2dbf5cede7c90b7b45b4b83075c119da3857a1a90c35b8e5e66e4a506bf3
- Both transactions: `FINALIZED`, leader `SUCCESS`. Reconciliation: `MAJORITY_AGREE`. Stored report: `PARTIAL`, two valid pairs, `l-lunch` and `r-clean` unmatched despite both costing USD 50, report root `6466b30c75822fec713fca7cb986957d728cfab6a932e7a0287e2f1d69e9d19f`.
- Readback: `get_match("demo-partial-v1", "l-lunch")` returned the empty string.

## Missing-source negative case

- Batch registration: https://explorer-studio.genlayer.com/tx/0xd191c1336076d6ea1ee0019b4f21bf6de17d0e2eb55d5180d32a8568f6b69385
- Reconciliation: https://explorer-studio.genlayer.com/tx/0xa7af06dba31ab5d41093af62a77dff9bb6cf28d01c2140e91417facc56d506e7
- Both transactions: `FINALIZED`, leader `SUCCESS`. Reconciliation: `MAJORITY_AGREE`. The nonexistent pinned left path returned HTTP 404; the stored report was `UNAVAILABLE` with no pairs and root `fa84423aaff8b1a67dfcb6b2b9996455d9e0e7b103d9b17d2dc0d6994f4e631b`.
- Readback: `get_match("demo-unavailable-v1", "l-host")` returned the empty string.

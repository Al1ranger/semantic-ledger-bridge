# StudioNet proofs

Only transactions independently checked as `FINALIZED` with leader execution `SUCCESS` belong here.

## Deployment

- Contract: https://explorer-studio.genlayer.com/address/0x360181F8c8EfcDd1cF2d4254AE1e274bAC6b065f
- Transaction: https://explorer-studio.genlayer.com/tx/0xb960c5c575935fe124e4a1516d61503d8e38e059f9a4e9afadad9a2a65a3724f
- StudioNet RPC reported `FINALIZED` and leader execution `SUCCESS`.
- The deployed source returned by `genlayer code` exactly matches `contracts/SemanticLedgerBridge.py` after newline normalization; normalized SHA-256: `83d52057513fc673bee23be21e1ca39a1ebf8e8ca2a1e720a43d3de5e2eb194e`.

No reconciliation proof has been claimed yet. The fixtures must first be published at their pinned commit URLs, then registration and reconciliation must finalize successfully.

# Security and trust boundaries

Two independently fetched source bodies are bounded to six rows and 4 KiB each. URLs use fixed `raw.githubusercontent.com` host, pinned 40-hex commits, and validated paths. The contract computes source and normalized-row hashes; no caller-provided text, outcome, or confidence drives reconciliation.

Model-generated pairs are only candidates. Unknown IDs, duplicate use of a row, amount mismatches, and currency mismatches invalidate the whole vector. Validators independently fetch both bodies and rerun semantic mapping, requiring exact report equality. Completed batches cannot be retried to seek a preferred model answer. All lookups are batch-scoped.

Neither source authenticity beyond the pinned Git commit nor correctness of the underlying bookkeeping is guaranteed. This software does not move money or approve expenses. Do not expose confidential ledgers through public GitHub fixtures. Report sensitive vulnerabilities privately to the repository owner.

# Source-to-target lineage

```mermaid
flowchart LR
  A[seeds/raw_claims.csv] --> B[raw_claims]
  B --> C[stg_claims]
  C --> D[fct_claims]
  D --> E[analytics / reconciliation]
```

The public implementation contains a synthetic claims slice. The same control pattern can be extended to other healthcare domains without publishing employer schemas or records.

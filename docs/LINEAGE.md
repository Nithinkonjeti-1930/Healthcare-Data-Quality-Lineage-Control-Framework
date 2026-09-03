# Source-to-target lineage

```mermaid
flowchart LR
  A[Raw claims feed] --> B[stg_claims]
  B --> C[fct_claims]
  C --> D[Claims reporting / reconciliation]
  E[Raw HR feed] --> F[Staging HR model]
  F --> G[Curated workforce model]
  H[Raw operations feed] --> I[Staging operations model]
  I --> J[Curated operations model]
```

The public repository implements the claims slice with synthetic data and documents the same control pattern for additional domains. No employer schemas or healthcare records are included.

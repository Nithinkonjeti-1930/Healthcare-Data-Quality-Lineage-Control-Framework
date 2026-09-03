select
    claim_id,
    member_id,
    service_date,
    amount,
    claim_status,
    case when claim_status = 'PAID' then amount else 0 end as paid_amount
from {{ ref('stg_claims') }}

select
    cast(claim_id as varchar) as claim_id,
    cast(member_id as varchar) as member_id,
    cast(service_date as date) as service_date,
    cast(amount as decimal(18,2)) as amount,
    upper(status) as claim_status
from {{ source('raw_healthcare', 'claims') }}
where claim_id is not null

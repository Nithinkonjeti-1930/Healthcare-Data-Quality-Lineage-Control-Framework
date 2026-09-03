select *
from {{ ref('stg_claims') }}
where amount <= 0

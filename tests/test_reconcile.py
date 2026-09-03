from src.reconcile import reconcile, summarize


def test_synthetic_claims_have_no_duplicates():
    result = summarize("data/source_claims.csv")
    assert result["duplicate_ids"] == []
    assert result["row_count"] == 3


def test_source_target_reconcile():
    result = reconcile("data/source_claims.csv", "data/curated_claims.csv")
    assert result["row_count_match"]
    assert result["id_set_match"]
    assert result["amount_total_match"]

import tempfile
from pathlib import Path
import unittest

from src.reconcile import profile, reconcile


class ReconciliationTests(unittest.TestCase):
    def test_sample_files_reconcile(self):
        result = reconcile("data/source_claims.csv", "data/curated_claims.csv")
        self.assertTrue(result["row_count_match"])
        self.assertTrue(result["id_set_match"])
        self.assertTrue(result["amount_total_match"])
        self.assertFalse(result["source_duplicates"])

    def test_duplicate_detection(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "claims.csv"
            p.write_text("claim_id,member_id,service_date,amount,status\nC1,M1,2026-01-01,1,PAID\nC1,M1,2026-01-01,1,PAID\n", encoding="utf-8")
            self.assertEqual(profile(p)["duplicate_ids"], ["C1"])


if __name__ == "__main__":
    unittest.main()

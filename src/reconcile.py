"""Small dependency-free reconciliation utility for synthetic warehouse extracts."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal
from pathlib import Path


def summarize(path: str | Path) -> dict[str, object]:
    rows = list(csv.DictReader(Path(path).open(newline="", encoding="utf-8")))
    ids = [row["claim_id"] for row in rows]
    return {
        "row_count": len(rows),
        "claim_ids": set(ids),
        "duplicate_ids": sorted({x for x in ids if ids.count(x) > 1}),
        "amount_total": sum((Decimal(row["amount"]) for row in rows), Decimal("0")),
    }


def reconcile(source: str | Path, target: str | Path) -> dict[str, object]:
    s = summarize(source)
    t = summarize(target)
    return {
        "row_count_match": s["row_count"] == t["row_count"],
        "id_set_match": s["claim_ids"] == t["claim_ids"],
        "amount_total_match": s["amount_total"] == t["amount_total"],
        "source_duplicates": s["duplicate_ids"],
        "target_duplicates": t["duplicate_ids"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()
    result = reconcile(args.source, args.target)
    print(result)
    if not all(result[k] for k in ("row_count_match", "id_set_match", "amount_total_match")):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

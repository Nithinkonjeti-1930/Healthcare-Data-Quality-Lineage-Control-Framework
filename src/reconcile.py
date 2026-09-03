from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = {"claim_id", "member_id", "service_date", "amount", "status"}


def profile(path: str | Path) -> dict:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")
        rows = list(reader)

    ids = [row["claim_id"].strip() for row in rows]
    total = Decimal("0")
    for row in rows:
        try:
            total += Decimal(row["amount"])
        except (InvalidOperation, KeyError) as exc:
            raise ValueError(f"invalid amount for claim {row.get('claim_id')}") from exc
    return {
        "row_count": len(rows),
        "claim_ids": set(ids),
        "duplicate_ids": sorted({x for x in ids if ids.count(x) > 1}),
        "amount_total": total,
    }


def reconcile(source: str | Path, target: str | Path) -> dict:
    s, t = profile(source), profile(target)
    return {
        "row_count_match": s["row_count"] == t["row_count"],
        "id_set_match": s["claim_ids"] == t["claim_ids"],
        "amount_total_match": s["amount_total"] == t["amount_total"],
        "source_duplicates": s["duplicate_ids"],
        "target_duplicates": t["duplicate_ids"],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--target", required=True)
    args = p.parse_args()
    result = reconcile(args.source, args.target)
    print(result)
    passed = all(result[k] for k in ("row_count_match", "id_set_match", "amount_total_match")) and not result["source_duplicates"] and not result["target_duplicates"]
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()

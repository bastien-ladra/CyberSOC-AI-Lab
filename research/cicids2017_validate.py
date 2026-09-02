import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from utils.cic_ids2017_mapping import normalize_cic_ids2017_label
from utils.cic_ids2017_sample_parser import normalize_cic_ids2017_column_name

REQUIRED_FIELDS = {
    "timestamp",
    "source ip",
    "destination ip",
    "source port",
    "destination port",
    "protocol",
    "label",
}

V1_SUPPORTED_LABELS = {"benign", "ssh patator"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_header(fieldnames: list[str] | None) -> None:
    if not fieldnames:
        raise ValueError("CSV has no header")

    normalized = {normalize_cic_ids2017_column_name(name) for name in fieldnames}
    missing = REQUIRED_FIELDS - normalized
    if missing:
        raise ValueError(
            "CSV is missing required CIC-IDS2017 fields: " + ", ".join(sorted(missing))
        )


def inspect_dataset(path: Path, max_rows: int | None = None) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"dataset file does not exist: {path}")
    if max_rows is not None and max_rows <= 0:
        raise ValueError("max_rows must be greater than zero")

    label_counts: Counter[str] = Counter()
    rows_read = 0

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        validate_header(reader.fieldnames)

        label_column = next(
            name
            for name in reader.fieldnames or []
            if normalize_cic_ids2017_column_name(name) == "label"
        )

        for row in reader:
            if max_rows is not None and rows_read >= max_rows:
                break
            rows_read += 1
            normalized_label = normalize_cic_ids2017_label(str(row[label_column]))
            label_counts[normalized_label] += 1

    supported_counts = {
        label: label_counts[label]
        for label in sorted(V1_SUPPORTED_LABELS)
    }

    return {
        "file": path.name,
        "sha256": sha256_file(path),
        "rows_read": rows_read,
        "supported_v1_labels": supported_counts,
        "all_label_counts": dict(sorted(label_counts.items())),
        "v1_has_both_classes": all(supported_counts.values()),
        "raw_dataset_committed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a local CIC-IDS2017 labelled-flow CSV for benchmark v1."
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    report = inspect_dataset(args.csv_path, args.max_rows)
    serialized = json.dumps(report, indent=2, sort_keys=True)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    else:
        print(serialized)

    return 0 if report["v1_has_both_classes"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

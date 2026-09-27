import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from research.cicids2017_validate import (
    V1_SUPPORTED_LABELS,
    sha256_file,
    validate_header,
)
from utils.cic_ids2017_mapping import normalize_cic_ids2017_label
from utils.cic_ids2017_sample_parser import normalize_cic_ids2017_column_name

SELECTION_SCHEMA_VERSION = 1
MAX_SELECTED_ROWS = 500


def canonical_row_sha256(row: dict[str, object]) -> str:
    """Hash one CSV row deterministically without storing raw row contents."""
    normalized = {
        normalize_cic_ids2017_column_name(name): str(value).strip()
        for name, value in row.items()
    }
    payload = json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_selection_manifest(
    csv_path: Path,
    rows_per_class: int = 100,
) -> dict[str, Any]:
    """
    Select an exact, deterministic and balanced benchmark subset.

    For each supported v1 label, the rows with the lexicographically smallest
    SHA-256 hashes of their canonicalized CSV contents are selected. This avoids
    dependence on source-file ordering while keeping the rule transparent and
    reproducible. Results are then evaluated in original source order.
    """
    if not csv_path.is_file():
        raise ValueError(f"dataset file does not exist: {csv_path}")
    if rows_per_class <= 0:
        raise ValueError("rows_per_class must be greater than zero")
    if rows_per_class * len(V1_SUPPORTED_LABELS) > MAX_SELECTED_ROWS:
        raise ValueError(
            f"selection exceeds the {MAX_SELECTED_ROWS}-row benchmark safety bound"
        )

    labels = sorted(V1_SUPPORTED_LABELS)
    candidates: dict[str, list[tuple[str, int]]] = {
        label: [] for label in labels
    }

    with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        validate_header(reader.fieldnames)

        label_column = next(
            name
            for name in reader.fieldnames or []
            if normalize_cic_ids2017_column_name(name) == "label"
        )

        for row_number, row in enumerate(reader, start=1):
            label = normalize_cic_ids2017_label(str(row[label_column]))
            if label not in candidates:
                continue
            candidates[label].append((canonical_row_sha256(row), row_number))

    shortages = {
        label: len(rows)
        for label, rows in candidates.items()
        if len(rows) < rows_per_class
    }
    if shortages:
        details = ", ".join(
            f"{label}={count}" for label, count in sorted(shortages.items())
        )
        raise ValueError(
            "dataset does not contain enough rows for the preregistered "
            f"balanced selection ({details}; need {rows_per_class} per class)"
        )

    selected_rows: list[dict[str, Any]] = []
    for label in labels:
        chosen = sorted(candidates[label])[:rows_per_class]
        selected_rows.extend(
            {
                "row_number": row_number,
                "label": label,
                "row_sha256": row_hash,
            }
            for row_hash, row_number in chosen
        )

    selected_rows.sort(key=lambda item: int(item["row_number"]))

    return {
        "schema_version": SELECTION_SCHEMA_VERSION,
        "dataset_file": csv_path.name,
        "dataset_sha256": sha256_file(csv_path),
        "selection_rule": (
            "balanced_v1_lowest_canonical_row_sha256_per_label_then_source_order"
        ),
        "rows_per_class": rows_per_class,
        "supported_labels": labels,
        "available_counts": {
            label: len(candidates[label]) for label in labels
        },
        "selected_counts": {
            label: rows_per_class for label in labels
        },
        "selected_row_count": len(selected_rows),
        "selected_rows": selected_rows,
    }


def load_selection_manifest(
    manifest_path: Path,
    csv_path: Path,
) -> tuple[dict[str, Any], set[int]]:
    """Load and validate a frozen selection manifest against the exact dataset."""
    if not manifest_path.is_file():
        raise ValueError(f"selection manifest does not exist: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != SELECTION_SCHEMA_VERSION:
        raise ValueError("unsupported selection manifest schema version")

    expected_dataset_sha = manifest.get("dataset_sha256")
    actual_dataset_sha = sha256_file(csv_path)
    if expected_dataset_sha != actual_dataset_sha:
        raise ValueError("selection manifest dataset SHA-256 does not match CSV")

    selected_rows = manifest.get("selected_rows")
    if not isinstance(selected_rows, list) or not selected_rows:
        raise ValueError("selection manifest has no selected rows")

    row_numbers: set[int] = set()
    for item in selected_rows:
        if not isinstance(item, dict):
            raise ValueError("selection manifest row entry must be an object")
        row_number = item.get("row_number")
        if (
            not isinstance(row_number, int)
            or isinstance(row_number, bool)
            or row_number <= 0
        ):
            raise ValueError("selection manifest contains an invalid row number")
        if row_number in row_numbers:
            raise ValueError("selection manifest contains duplicate row numbers")
        row_numbers.add(row_number)

    if len(row_numbers) > MAX_SELECTED_ROWS:
        raise ValueError("selection manifest exceeds benchmark safety bound")

    if manifest.get("selected_row_count") != len(row_numbers):
        raise ValueError("selection manifest row count is inconsistent")

    return manifest, row_numbers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Freeze a deterministic balanced CIC-IDS2017 benchmark selection."
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--rows-per-class", type=int, default=100)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = build_selection_manifest(
        args.csv_path,
        rows_per_class=args.rows_per_class,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import csv
import json
from pathlib import Path

import pytest

from research.cicids2017_selection import (
    build_selection_manifest,
    load_selection_manifest,
)

FIELDNAMES = [
    "Timestamp",
    "Source IP",
    "Destination IP",
    "Source Port",
    "Destination Port",
    "Protocol",
    "Label",
]


def _write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDNAMES)
        writer.writerows(rows)


def test_selection_is_balanced_and_deterministic(tmp_path: Path) -> None:
    csv_path = tmp_path / "cicids.csv"
    _write_csv(
        csv_path,
        [
            ["t1", "192.0.2.1", "192.0.2.10", "50001", "22", "6", "SSH-Patator"],
            ["t2", "192.0.2.2", "192.0.2.10", "50002", "443", "6", "BENIGN"],
            ["t3", "192.0.2.3", "192.0.2.10", "50003", "22", "6", "SSH-Patator"],
            ["t4", "192.0.2.4", "192.0.2.10", "50004", "80", "6", "BENIGN"],
        ],
    )

    first = build_selection_manifest(csv_path, rows_per_class=1)
    second = build_selection_manifest(csv_path, rows_per_class=1)

    assert first == second
    assert first["selected_row_count"] == 2
    assert first["selected_counts"] == {"benign": 1, "ssh patator": 1}
    assert len({item["row_number"] for item in first["selected_rows"]}) == 2


def test_manifest_is_bound_to_exact_dataset_hash(tmp_path: Path) -> None:
    csv_path = tmp_path / "cicids.csv"
    _write_csv(
        csv_path,
        [
            ["t1", "192.0.2.1", "192.0.2.10", "50001", "22", "6", "SSH-Patator"],
            ["t2", "192.0.2.2", "192.0.2.10", "50002", "443", "6", "BENIGN"],
        ],
    )

    manifest = build_selection_manifest(csv_path, rows_per_class=1)
    manifest_path = tmp_path / "selection.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    _, row_numbers = load_selection_manifest(manifest_path, csv_path)
    assert len(row_numbers) == 2

    with csv_path.open("a", encoding="utf-8") as handle:
        handle.write("\n")

    with pytest.raises(ValueError, match="SHA-256"):
        load_selection_manifest(manifest_path, csv_path)


def test_selection_refuses_insufficient_class_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "cicids.csv"
    _write_csv(
        csv_path,
        [
            ["t1", "192.0.2.1", "192.0.2.10", "50001", "22", "6", "SSH-Patator"],
            ["t2", "192.0.2.2", "192.0.2.10", "50002", "443", "6", "BENIGN"],
        ],
    )

    with pytest.raises(ValueError, match="enough rows"):
        build_selection_manifest(csv_path, rows_per_class=2)

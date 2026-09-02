import csv
from pathlib import Path

import pytest

from research.cicids2017_validate import inspect_dataset, validate_header


FIELDNAMES = [
    "Timestamp",
    "Source IP",
    "Destination IP",
    "Source Port",
    "Destination Port",
    "Protocol",
    "Label",
]


def _write_csv(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerow(
            {
                "Timestamp": "2017-07-04 14:00:00",
                "Source IP": "192.0.2.10",
                "Destination IP": "192.0.2.20",
                "Source Port": "50000",
                "Destination Port": "22",
                "Protocol": "6",
                "Label": "BENIGN",
            }
        )
        writer.writerow(
            {
                "Timestamp": "2017-07-04 14:00:01",
                "Source IP": "192.0.2.11",
                "Destination IP": "192.0.2.20",
                "Source Port": "50001",
                "Destination Port": "22",
                "Protocol": "6",
                "Label": "SSH-Patator",
            }
        )


def test_inspect_dataset_records_hash_and_v1_classes(tmp_path: Path) -> None:
    csv_path = tmp_path / "cicids.csv"
    _write_csv(csv_path)

    report = inspect_dataset(csv_path)

    assert report["rows_read"] == 2
    assert report["supported_v1_labels"] == {"benign": 1, "ssh patator": 1}
    assert report["v1_has_both_classes"] is True
    assert len(report["sha256"]) == 64
    assert report["raw_dataset_committed"] is False


def test_validate_header_rejects_missing_fields() -> None:
    with pytest.raises(ValueError, match="missing required"):
        validate_header(["Timestamp", "Label"])

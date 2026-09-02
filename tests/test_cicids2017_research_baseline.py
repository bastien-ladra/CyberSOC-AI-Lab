import csv
from pathlib import Path

from research.cicids2017_baseline import (
    evaluate_baseline,
    predict_ssh_port_baseline,
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


def test_predict_ssh_port_baseline_is_explicit() -> None:
    assert predict_ssh_port_baseline("TCP", 22) is True
    assert predict_ssh_port_baseline("tcp", 22) is True
    assert predict_ssh_port_baseline("UDP", 22) is False
    assert predict_ssh_port_baseline("TCP", 443) is False


def test_evaluate_baseline_scores_only_supported_labels(tmp_path: Path) -> None:
    csv_path = tmp_path / "cicids.csv"

    rows = [
        ["2017-07-04 14:00:00", "192.0.2.1", "192.0.2.20", "50000", "22", "6", "SSH-Patator"],
        ["2017-07-04 14:00:01", "192.0.2.2", "192.0.2.20", "50001", "443", "6", "BENIGN"],
        ["2017-07-04 14:00:02", "192.0.2.3", "192.0.2.20", "50002", "22", "6", "BENIGN"],
        ["2017-07-04 14:00:03", "192.0.2.4", "192.0.2.20", "50003", "80", "6", "DDoS"],
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDNAMES)
        writer.writerows(rows)

    result = evaluate_baseline(csv_path)

    assert result["rows_seen"] == 4
    assert result["scored_rows"] == 3
    assert result["unsupported_rows"] == 1
    assert result["metrics"]["true_positive"] == 1
    assert result["metrics"]["true_negative"] == 1
    assert result["metrics"]["false_positive"] == 1
    assert result["metrics"]["false_negative"] == 0

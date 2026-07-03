from pathlib import Path

import pytest

from utils.cic_ids2017_mapping import INTERNAL_SSH_BRUTE_FORCE_ALERT
from utils.cic_ids2017_mini_loader import (
    MAX_CIC_IDS2017_LOADER_ROWS,
    CicIds2017MiniLoaderResult,
    load_cic_ids2017_samples,
)

CSV_HEADER = (
    "Timestamp,Source IP,Destination IP,Source Port,Destination Port,Protocol,Label\n"
)


def _write_test_csv(csv_path: Path, rows: list[str]) -> None:
    csv_path.write_text(CSV_HEADER + "\n".join(rows) + "\n", encoding="utf-8")


def test_loads_bounded_local_csv_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "local_cic_ids2017_sample.csv"
    _write_test_csv(
        csv_path,
        [
            "2017-07-04 14:00:00,205.174.165.73,192.168.10.50,12345,22,6,SSH-Patator",
            "2017-07-03 09:00:00,192.168.10.12,192.168.10.50,51515,443,TCP,BENIGN",
        ],
    )

    result = load_cic_ids2017_samples(csv_path=csv_path, max_rows=10)

    assert isinstance(result, CicIds2017MiniLoaderResult)
    assert result.rows_read == 2
    assert result.supported_labels == 2
    assert result.unsupported_labels == 0
    assert len(result.events) == 2
    assert result.events[0].expected_alert_type == INTERNAL_SSH_BRUTE_FORCE_ALERT
    assert result.events[0].protocol == "TCP"
    assert result.events[1].expected_alert_type is None
    assert result.events[1].raw_label == "BENIGN"


def test_respects_max_rows_limit(tmp_path: Path) -> None:
    csv_path = tmp_path / "local_cic_ids2017_sample.csv"
    _write_test_csv(
        csv_path,
        [
            "2017-07-04 14:00:00,205.174.165.73,192.168.10.50,12345,22,6,SSH-Patator",
            "2017-07-03 09:00:00,192.168.10.12,192.168.10.50,51515,443,TCP,BENIGN",
        ],
    )

    result = load_cic_ids2017_samples(csv_path=csv_path, max_rows=1)

    assert result.rows_read == 1
    assert len(result.events) == 1
    assert result.events[0].raw_label == "SSH-Patator"


def test_rejects_non_positive_max_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "local_cic_ids2017_sample.csv"
    _write_test_csv(
        csv_path,
        [
            "2017-07-04 14:00:00,205.174.165.73,192.168.10.50,12345,22,6,SSH-Patator",
        ],
    )

    with pytest.raises(ValueError, match="max_rows must be greater than 0"):
        load_cic_ids2017_samples(csv_path=csv_path, max_rows=0)


def test_rejects_max_rows_above_safety_limit(tmp_path: Path) -> None:
    csv_path = tmp_path / "local_cic_ids2017_sample.csv"
    _write_test_csv(
        csv_path,
        [
            "2017-07-04 14:00:00,205.174.165.73,192.168.10.50,12345,22,6,SSH-Patator",
        ],
    )

    with pytest.raises(ValueError, match="max_rows exceeds safety limit"):
        load_cic_ids2017_samples(
            csv_path=csv_path,
            max_rows=MAX_CIC_IDS2017_LOADER_ROWS + 1,
        )


def test_missing_local_csv_raises_clear_error(tmp_path: Path) -> None:
    csv_path = tmp_path / "missing.csv"

    with pytest.raises(ValueError, match="CIC-IDS2017 CSV file does not exist"):
        load_cic_ids2017_samples(csv_path=csv_path, max_rows=1)


def test_missing_required_column_raises_clear_row_error(tmp_path: Path) -> None:
    csv_path = tmp_path / "local_cic_ids2017_sample.csv"
    csv_path.write_text(
        "Timestamp,Source IP,Destination IP,Source Port,Destination Port,Protocol\n"
        "2017-07-04 14:00:00,205.174.165.73,192.168.10.50,12345,22,6\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Invalid CIC-IDS2017 row 1: Missing required CIC-IDS2017 column: label",
    ):
        load_cic_ids2017_samples(csv_path=csv_path, max_rows=1)


def test_counts_unsupported_labels(tmp_path: Path) -> None:
    csv_path = tmp_path / "local_cic_ids2017_sample.csv"
    _write_test_csv(
        csv_path,
        [
            "2017-07-04 14:00:00,205.174.165.73,192.168.10.50,12345,21,6,FTP-Patator",
        ],
    )

    result = load_cic_ids2017_samples(csv_path=csv_path, max_rows=10)

    assert result.rows_read == 1
    assert result.supported_labels == 0
    assert result.unsupported_labels == 1
    assert result.events[0].raw_label == "FTP-Patator"
    assert result.events[0].expected_alert_type is None
    assert result.events[0].is_supported_label is False

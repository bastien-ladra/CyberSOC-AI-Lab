"""
Bounded mini-loader for already-downloaded local CIC-IDS2017-like CSV files.

This module intentionally does not download CIC-IDS2017 and does not ship any raw
public dataset sample. It only reads a caller-provided local CSV file with an
explicit row limit, then delegates row normalization to the sample row parser.
"""

import csv
from dataclasses import dataclass
from pathlib import Path

from utils.cic_ids2017_sample_parser import (
    CicIds2017SampleEvent,
    parse_cic_ids2017_sample_row,
)

MAX_CIC_IDS2017_LOADER_ROWS = 1000


@dataclass(frozen=True)
class CicIds2017MiniLoaderResult:
    """
    Descriptive result returned by the bounded CIC-IDS2017 mini-loader.
    """

    events: tuple[CicIds2017SampleEvent, ...]
    rows_read: int
    supported_labels: int
    unsupported_labels: int


def _validate_max_rows(max_rows: int) -> None:
    if max_rows <= 0:
        raise ValueError("CIC-IDS2017 max_rows must be greater than 0")

    if max_rows > MAX_CIC_IDS2017_LOADER_ROWS:
        raise ValueError(
            "CIC-IDS2017 max_rows exceeds safety limit: "
            f"{MAX_CIC_IDS2017_LOADER_ROWS}"
        )


def load_cic_ids2017_samples(
    csv_path: str | Path,
    max_rows: int,
) -> CicIds2017MiniLoaderResult:
    """
    Load a bounded number of rows from a local CIC-IDS2017-like CSV file.

    The function reads only a caller-provided local file, requires an explicit
    row limit and stops as soon as the limit is reached. It does not download
    CIC-IDS2017, does not add raw data to the repository and does not run any
    detection rule.
    """
    _validate_max_rows(max_rows)

    resolved_csv_path = Path(csv_path)
    if not resolved_csv_path.is_file():
        raise ValueError(f"CIC-IDS2017 CSV file does not exist: {resolved_csv_path}")

    events: list[CicIds2017SampleEvent] = []
    rows_read = 0
    supported_labels = 0
    unsupported_labels = 0

    with resolved_csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if rows_read >= max_rows:
                break

            rows_read += 1

            try:
                event = parse_cic_ids2017_sample_row(row)
            except ValueError as error:
                raise ValueError(
                    f"Invalid CIC-IDS2017 row {rows_read}: {error}"
                ) from error

            events.append(event)

            if event.is_supported_label:
                supported_labels += 1
            else:
                unsupported_labels += 1

    return CicIds2017MiniLoaderResult(
        events=tuple(events),
        rows_read=rows_read,
        supported_labels=supported_labels,
        unsupported_labels=unsupported_labels,
    )

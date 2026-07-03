"""
Parser for one already-provided CIC-IDS2017-like CSV row.

This module intentionally does not download the public dataset and does not load a
full CSV file. It only normalizes one row dictionary that was already provided by
a caller, then applies the documented label mapping.
"""

from collections.abc import Mapping
from dataclasses import dataclass

from utils.cic_ids2017_mapping import (
    is_supported_cic_ids2017_label,
    map_cic_ids2017_label,
)

COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "timestamp": ("timestamp",),
    "source_ip": ("source ip", "src ip"),
    "destination_ip": ("destination ip", "dst ip"),
    "source_port": ("source port", "src port"),
    "destination_port": ("destination port", "dst port"),
    "protocol": ("protocol",),
    "label": ("label",),
}

PROTOCOL_NUMBER_MAPPINGS = {
    "1": "ICMP",
    "6": "TCP",
    "17": "UDP",
}


@dataclass(frozen=True)
class CicIds2017SampleEvent:
    """
    Minimal normalized event created from one CIC-IDS2017-like CSV row.
    """

    timestamp: str
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    raw_label: str
    expected_alert_type: str | None
    is_supported_label: bool


def normalize_cic_ids2017_column_name(column_name: str) -> str:
    """
    Normalize CIC-IDS2017 column names for deterministic lookup.
    """
    normalized = column_name.strip().replace("_", " ").replace("-", " ")
    return " ".join(normalized.split()).casefold()


def _build_normalized_row(row: Mapping[str, object]) -> dict[str, object]:
    return {
        normalize_cic_ids2017_column_name(column_name): value
        for column_name, value in row.items()
    }


def _get_required_value(
    normalized_row: Mapping[str, object],
    field_name: str,
) -> str:
    for alias in COLUMN_ALIASES[field_name]:
        normalized_alias = normalize_cic_ids2017_column_name(alias)

        if normalized_alias not in normalized_row:
            continue

        value = normalized_row[normalized_alias]
        cleaned_value = str(value).strip()

        if not cleaned_value:
            raise ValueError(f"CIC-IDS2017 column is empty: {field_name}")

        return cleaned_value

    raise ValueError(f"Missing required CIC-IDS2017 column: {field_name}")


def _parse_port(port_value: str, field_name: str) -> int:
    try:
        port = int(port_value)
    except ValueError as error:
        raise ValueError(
            f"Invalid CIC-IDS2017 port value for {field_name}: {port_value}"
        ) from error

    if port < 0 or port > 65535:
        raise ValueError(
            f"CIC-IDS2017 port value out of range for {field_name}: {port_value}"
        )

    return port


def _normalize_protocol(protocol_value: str) -> str:
    normalized_protocol = protocol_value.strip().upper()
    return PROTOCOL_NUMBER_MAPPINGS.get(normalized_protocol, normalized_protocol)


def parse_cic_ids2017_sample_row(
    row: Mapping[str, object],
) -> CicIds2017SampleEvent:
    """
    Parse one already-provided CIC-IDS2017-like CSV row.

    The function does not read files, download public data or run detection rules.
    It only converts a single row dictionary into a minimal normalized event.
    """
    normalized_row = _build_normalized_row(row)

    timestamp = _get_required_value(normalized_row, "timestamp")
    source_ip = _get_required_value(normalized_row, "source_ip")
    destination_ip = _get_required_value(normalized_row, "destination_ip")
    source_port = _parse_port(
        _get_required_value(normalized_row, "source_port"),
        "source_port",
    )
    destination_port = _parse_port(
        _get_required_value(normalized_row, "destination_port"),
        "destination_port",
    )
    protocol = _normalize_protocol(_get_required_value(normalized_row, "protocol"))
    raw_label = _get_required_value(normalized_row, "label")

    return CicIds2017SampleEvent(
        timestamp=timestamp,
        source_ip=source_ip,
        destination_ip=destination_ip,
        source_port=source_port,
        destination_port=destination_port,
        protocol=protocol,
        raw_label=raw_label,
        expected_alert_type=map_cic_ids2017_label(raw_label),
        is_supported_label=is_supported_cic_ids2017_label(raw_label),
    )

import pytest

from utils.cic_ids2017_mapping import INTERNAL_SSH_BRUTE_FORCE_ALERT
from utils.cic_ids2017_sample_parser import (
    CicIds2017SampleEvent,
    normalize_cic_ids2017_column_name,
    parse_cic_ids2017_sample_row,
)


def test_parse_minimal_ssh_row_maps_expected_alert_type() -> None:
    row = {
        "Timestamp": "2017-07-04 14:00:00",
        "Source IP": "205.174.165.73",
        "Destination IP": "192.168.10.50",
        "Source Port": "12345",
        "Destination Port": "22",
        "Protocol": "6",
        "Label": "SSH-Patator",
    }

    assert parse_cic_ids2017_sample_row(row) == CicIds2017SampleEvent(
        timestamp="2017-07-04 14:00:00",
        source_ip="205.174.165.73",
        destination_ip="192.168.10.50",
        source_port=12345,
        destination_port=22,
        protocol="TCP",
        raw_label="SSH-Patator",
        expected_alert_type=INTERNAL_SSH_BRUTE_FORCE_ALERT,
        is_supported_label=True,
    )


def test_parse_benign_row_maps_to_no_expected_alert() -> None:
    row = {
        "Timestamp": "2017-07-03 09:00:00",
        "Source IP": "192.168.10.12",
        "Destination IP": "192.168.10.50",
        "Source Port": "51515",
        "Destination Port": "443",
        "Protocol": "TCP",
        "Label": "BENIGN",
    }

    event = parse_cic_ids2017_sample_row(row)

    assert event.expected_alert_type is None
    assert event.is_supported_label is True
    assert event.raw_label == "BENIGN"
    assert event.protocol == "TCP"


def test_parse_row_accepts_common_column_aliases() -> None:
    row = {
        " Timestamp ": "2017-07-04 14:00:00",
        "Src IP": "205.174.165.73",
        "Dst IP": "192.168.10.50",
        "Src Port": "12345",
        "Dst Port": "22",
        "Protocol": "6",
        "Label": "Brute Force SSH",
    }

    event = parse_cic_ids2017_sample_row(row)

    assert event.source_ip == "205.174.165.73"
    assert event.destination_ip == "192.168.10.50"
    assert event.source_port == 12345
    assert event.destination_port == 22
    assert event.expected_alert_type == INTERNAL_SSH_BRUTE_FORCE_ALERT


def test_parse_unknown_label_keeps_raw_label_but_marks_it_unsupported() -> None:
    row = {
        "Timestamp": "2017-07-04 14:00:00",
        "Source IP": "205.174.165.73",
        "Destination IP": "192.168.10.50",
        "Source Port": "12345",
        "Destination Port": "21",
        "Protocol": "6",
        "Label": "FTP-Patator",
    }

    event = parse_cic_ids2017_sample_row(row)

    assert event.raw_label == "FTP-Patator"
    assert event.expected_alert_type is None
    assert event.is_supported_label is False


def test_missing_required_column_raises_clear_error() -> None:
    row = {
        "Timestamp": "2017-07-04 14:00:00",
        "Source IP": "205.174.165.73",
        "Destination IP": "192.168.10.50",
        "Source Port": "12345",
        "Destination Port": "22",
        "Protocol": "6",
    }

    with pytest.raises(ValueError, match="Missing required CIC-IDS2017 column: label"):
        parse_cic_ids2017_sample_row(row)


def test_empty_required_column_raises_clear_error() -> None:
    row = {
        "Timestamp": "2017-07-04 14:00:00",
        "Source IP": "205.174.165.73",
        "Destination IP": "192.168.10.50",
        "Source Port": "12345",
        "Destination Port": "22",
        "Protocol": "6",
        "Label": " ",
    }

    with pytest.raises(ValueError, match="CIC-IDS2017 column is empty: label"):
        parse_cic_ids2017_sample_row(row)


def test_invalid_port_raises_clear_error() -> None:
    row = {
        "Timestamp": "2017-07-04 14:00:00",
        "Source IP": "205.174.165.73",
        "Destination IP": "192.168.10.50",
        "Source Port": "not-a-port",
        "Destination Port": "22",
        "Protocol": "6",
        "Label": "SSH-Patator",
    }

    with pytest.raises(
        ValueError,
        match="Invalid CIC-IDS2017 port value for source_port",
    ):
        parse_cic_ids2017_sample_row(row)


def test_out_of_range_port_raises_clear_error() -> None:
    row = {
        "Timestamp": "2017-07-04 14:00:00",
        "Source IP": "205.174.165.73",
        "Destination IP": "192.168.10.50",
        "Source Port": "70000",
        "Destination Port": "22",
        "Protocol": "6",
        "Label": "SSH-Patator",
    }

    with pytest.raises(
        ValueError,
        match="CIC-IDS2017 port value out of range for source_port",
    ):
        parse_cic_ids2017_sample_row(row)


def test_normalize_cic_ids2017_column_name_is_deterministic() -> None:
    assert normalize_cic_ids2017_column_name(" Destination_Port ") == (
        "destination port"
    )

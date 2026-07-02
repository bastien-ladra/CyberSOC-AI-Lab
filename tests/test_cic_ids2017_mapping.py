from utils.cic_ids2017_mapping import (
    INTERNAL_SSH_BRUTE_FORCE_ALERT,
    is_supported_cic_ids2017_label,
    map_cic_ids2017_label,
    normalize_cic_ids2017_label,
)


def test_normalize_cic_ids2017_label_trims_and_normalizes_separators() -> None:
    assert normalize_cic_ids2017_label(" SSH-Patator ") == "ssh patator"
    assert (
        normalize_cic_ids2017_label("Web_Attack - Sql Injection")
        == "web attack sql injection"
    )


def test_benign_label_maps_to_no_expected_alert() -> None:
    assert map_cic_ids2017_label("BENIGN") is None
    assert is_supported_cic_ids2017_label("BENIGN") is True


def test_ssh_patator_label_maps_to_ssh_brute_force() -> None:
    assert map_cic_ids2017_label("SSH-Patator") == INTERNAL_SSH_BRUTE_FORCE_ALERT


def test_ssh_brute_force_aliases_map_to_ssh_brute_force() -> None:
    assert map_cic_ids2017_label("Brute Force SSH") == INTERNAL_SSH_BRUTE_FORCE_ALERT
    assert map_cic_ids2017_label("ssh_brute_force") == INTERNAL_SSH_BRUTE_FORCE_ALERT


def test_supported_label_detection_handles_case_and_spacing() -> None:
    assert is_supported_cic_ids2017_label("  ssh patator  ") is True
    assert is_supported_cic_ids2017_label("SSH_BRUTE_FORCE") is True


def test_unsupported_labels_map_to_no_expected_alert() -> None:
    unsupported_labels = [
        "FTP-Patator",
        "Web Attack - Brute Force",
        "Web Attack - XSS",
        "Web Attack - Sql Injection",
        "PortScan",
        "DoS Hulk",
        "DDoS",
        "Bot",
        "Infiltration",
        "Heartbleed",
    ]

    for raw_label in unsupported_labels:
        assert map_cic_ids2017_label(raw_label) is None
        assert is_supported_cic_ids2017_label(raw_label) is False


def test_empty_label_maps_to_no_expected_alert() -> None:
    assert map_cic_ids2017_label("") is None
    assert is_supported_cic_ids2017_label("") is False

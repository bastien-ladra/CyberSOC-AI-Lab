"""
Mapping helpers for the selected CIC-IDS2017 labels.

This module intentionally does not download, load or parse the public dataset.
It only maps a small, documented subset of labels to internal alert types.
"""

INTERNAL_SSH_BRUTE_FORCE_ALERT = "SSH_BRUTE_FORCE"

SUPPORTED_CIC_IDS2017_LABEL_MAPPINGS: dict[str, str | None] = {
    "benign": None,
    "ssh patator": INTERNAL_SSH_BRUTE_FORCE_ALERT,
    "brute force ssh": INTERNAL_SSH_BRUTE_FORCE_ALERT,
    "ssh brute force": INTERNAL_SSH_BRUTE_FORCE_ALERT,
}


def normalize_cic_ids2017_label(raw_label: str) -> str:
    """
    Normalize a CIC-IDS2017 label for deterministic mapping.
    """
    label = raw_label.strip().replace("_", " ").replace("-", " ")
    return " ".join(label.split()).casefold()


def is_supported_cic_ids2017_label(raw_label: str) -> bool:
    """
    Return True when a CIC-IDS2017 label is explicitly supported.
    """
    normalized_label = normalize_cic_ids2017_label(raw_label)
    return normalized_label in SUPPORTED_CIC_IDS2017_LABEL_MAPPINGS


def map_cic_ids2017_label(raw_label: str) -> str | None:
    """
    Map a supported CIC-IDS2017 label to an internal alert type.

    BENIGN labels map to None because no alert is expected.
    Unsupported labels also map to None until their scenarios are explicitly added.
    Use is_supported_cic_ids2017_label when the caller must distinguish BENIGN from
    unsupported labels.
    """
    normalized_label = normalize_cic_ids2017_label(raw_label)
    return SUPPORTED_CIC_IDS2017_LABEL_MAPPINGS.get(normalized_label)

from utils.alert_analytics import build_distribution


def test_build_distribution_returns_empty_list_for_empty_rows() -> None:
    assert build_distribution([], "Priorité") == []


def test_build_distribution_counts_values() -> None:
    rows = [
        {"Priorité": "CRITICAL"},
        {"Priorité": "CRITICAL"},
        {"Priorité": "MEDIUM"},
    ]

    distribution = build_distribution(rows, "Priorité")

    assert {"Label": "CRITICAL", "Nombre": 2} in distribution
    assert {"Label": "MEDIUM", "Nombre": 1} in distribution


def test_build_distribution_respects_custom_order() -> None:
    rows = [
        {"Priorité": "MEDIUM"},
        {"Priorité": "CRITICAL"},
        {"Priorité": "LOW"},
    ]

    distribution = build_distribution(
        rows,
        "Priorité",
        order=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
    )

    assert distribution == [
        {"Label": "CRITICAL", "Nombre": 1},
        {"Label": "MEDIUM", "Nombre": 1},
        {"Label": "LOW", "Nombre": 1},
    ]


def test_build_distribution_uses_na_for_missing_values() -> None:
    rows = [
        {"Priorité": ""},
        {},
        {"Priorité": None},
    ]

    distribution = build_distribution(rows, "Priorité")

    assert distribution == [
        {"Label": "N/A", "Nombre": 3},
    ]
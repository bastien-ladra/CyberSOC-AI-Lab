from utils.csv_export import build_csv_export


def test_build_csv_export_returns_empty_bytes_for_empty_rows() -> None:
    assert build_csv_export([]) == b""


def test_build_csv_export_contains_headers_and_values() -> None:
    rows = [
        {
            "Type": "SSH_BRUTE_FORCE",
            "Priorité": "CRITICAL",
            "Score": 92,
        }
    ]

    csv_content = build_csv_export(rows).decode("utf-8-sig")

    assert "Type,Priorité,Score" in csv_content
    assert "SSH_BRUTE_FORCE,CRITICAL,92" in csv_content


def test_build_csv_export_handles_accents() -> None:
    rows = [
        {
            "Décision": "À revoir",
            "Note analyste": "Activité suspecte à corréler.",
        }
    ]

    csv_content = build_csv_export(rows).decode("utf-8-sig")

    assert "Décision" in csv_content
    assert "À revoir" in csv_content
    assert "Activité suspecte à corréler." in csv_content


def test_build_csv_export_handles_rows_with_additional_columns() -> None:
    rows = [
        {
            "Type": "SSH_BRUTE_FORCE",
            "Priorité": "CRITICAL",
        },
        {
            "Type": "WEB_RECONNAISSANCE",
            "Priorité": "MEDIUM",
            "Score": 66,
        },
    ]

    csv_content = build_csv_export(rows).decode("utf-8-sig")

    assert "Type,Priorité,Score" in csv_content
    assert "SSH_BRUTE_FORCE,CRITICAL," in csv_content
    assert "WEB_RECONNAISSANCE,MEDIUM,66" in csv_content

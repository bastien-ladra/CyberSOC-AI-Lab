from utils.report_export import build_markdown_report, format_markdown_value


def test_format_markdown_value_escapes_table_separator() -> None:
    assert format_markdown_value("A|B") == "A\\|B"


def test_build_markdown_report_contains_metrics_and_alerts() -> None:
    metrics = {
        "total": 1,
        "critical": 1,
        "high": 0,
        "medium": 0,
        "human_validation_required": 1,
        "reviewed": 1,
        "not_reviewed": 0,
    }

    alert_summary = [
        {
            "Fichier": "alert_001.json",
            "Type": "SSH_BRUTE_FORCE",
            "Criticité": "HIGH",
            "Priorité": "CRITICAL",
            "Score": 92,
            "IP source": "185.12.45.10",
            "Technique": "Brute Force",
            "ID technique": "T1110",
            "Décision analyste": "Validée",
        }
    ]

    report = build_markdown_report(
        metrics=metrics,
        alert_summary=alert_summary,
        human_review_summary=[],
        generated_at="2026-01-01T00:00:00+00:00",
    ).decode("utf-8")

    assert "# CyberSOC-AI-Lab — Rapport de synthèse" in report
    assert "Alertes affichées : 1" in report
    assert "SSH_BRUTE_FORCE" in report
    assert "T1110" in report


def test_build_markdown_report_contains_human_reviews() -> None:
    metrics = {
        "total": 1,
        "critical": 0,
        "high": 1,
        "medium": 0,
        "human_validation_required": 1,
        "reviewed": 1,
        "not_reviewed": 0,
    }

    human_review_summary = [
        {
            "Horodatage": "2026-01-01T00:00:00+00:00",
            "Alerte": "001",
            "Type": "SSH_BRUTE_FORCE",
            "Priorité": "CRITICAL",
            "Score": 92,
            "IP source": "185.12.45.10",
            "Technique": "Brute Force",
            "ID technique": "T1110",
            "Décision": "Validée",
            "Note analyste": "Tentative probable de brute force SSH.",
        }
    ]

    report = build_markdown_report(
        metrics=metrics,
        alert_summary=[],
        human_review_summary=human_review_summary,
        generated_at="2026-01-01T00:00:00+00:00",
    ).decode("utf-8")

    assert "Historique des validations humaines" in report
    assert "Validée" in report
    assert "Tentative probable de brute force SSH." in report

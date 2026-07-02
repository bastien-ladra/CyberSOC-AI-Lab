from datetime import datetime, timezone
from typing import Any


def format_markdown_value(value: Any) -> str:
    if value is None:
        return ""

    return str(value).replace("|", "\\|").replace("\n", " ")


def build_markdown_report(
    metrics: dict[str, int],
    alert_summary: list[dict[str, Any]],
    human_review_summary: list[dict[str, Any]],
    generated_at: str | None = None,
) -> bytes:
    if generated_at is None:
        generated_at = datetime.now(timezone.utc).isoformat()

    lines = [
        "# CyberSOC-AI-Lab — Rapport de synthèse",
        "",
        f"Généré le : `{generated_at}`",
        "",
        "## Indicateurs SOC",
        "",
        f"- Alertes affichées : {metrics.get('total', 0)}",
        f"- CRITICAL : {metrics.get('critical', 0)}",
        f"- HIGH : {metrics.get('high', 0)}",
        f"- MEDIUM : {metrics.get('medium', 0)}",
        f"- Validation humaine requise : {metrics.get('human_validation_required', 0)}",
        f"- Alertes revues : {metrics.get('reviewed', 0)}",
        f"- Alertes non revues : {metrics.get('not_reviewed', 0)}",
        "",
        "## Alertes",
        "",
    ]

    if alert_summary:
        alert_columns = [
            "Fichier",
            "Type",
            "Criticité",
            "Priorité",
            "Score",
            "IP source",
            "Technique",
            "ID technique",
            "Décision analyste",
        ]

        lines.append("| " + " | ".join(alert_columns) + " |")
        lines.append("| " + " | ".join(["---"] * len(alert_columns)) + " |")

        for alert in alert_summary:
            lines.append(
                "| "
                + " | ".join(
                    format_markdown_value(alert.get(column, ""))
                    for column in alert_columns
                )
                + " |"
            )
    else:
        lines.append("Aucune alerte affichée.")

    lines.extend(
        [
            "",
            "## Historique des validations humaines",
            "",
        ]
    )

    if human_review_summary:
        review_columns = [
            "Horodatage",
            "Alerte",
            "Type",
            "Priorité",
            "Score",
            "IP source",
            "Technique",
            "ID technique",
            "Décision",
            "Note analyste",
        ]

        lines.append("| " + " | ".join(review_columns) + " |")
        lines.append("| " + " | ".join(["---"] * len(review_columns)) + " |")

        for review in human_review_summary:
            lines.append(
                "| "
                + " | ".join(
                    format_markdown_value(review.get(column, ""))
                    for column in review_columns
                )
                + " |"
            )
    else:
        lines.append("Aucune validation humaine enregistrée.")

    lines.extend(
        [
            "",
            "## Note",
            "",
            "Ce rapport est généré automatiquement depuis le dashboard CyberSOC-AI-Lab.",
            "Les décisions analyste restent soumises à validation humaine.",
            "",
        ]
    )

    return "\n".join(lines).encode("utf-8")

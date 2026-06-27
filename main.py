import json
from pathlib import Path

from detection.log_parser import load_ssh_logs
from detection.rules_engine import detect_ssh_bruteforce


LOG_FILE = Path("data/sample_logs/ssh_auth.log")
REPORT_DIR = Path("reports")
ALERT_DIR = Path("alerts")


def save_alert_json(alert: dict, alert_path: Path) -> None:
    """
    Sauvegarde une alerte au format JSON structuré.
    """
    alert_path.write_text(
        json.dumps(alert, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def generate_markdown_report(alert: dict, report_path: Path) -> None:
    """
    Génère un rapport Markdown pour une alerte détectée.
    """
    targeted_users = ", ".join(alert["targeted_users"])

    evidence_block = "\n".join([f"- `{line}`" for line in alert["evidence"]])
    recommendations_block = "\n".join([f"- {action}" for action in alert["recommended_actions"]])

    report = f"""# Incident Report — {alert["alert_type"]}

## Résumé

Une tentative probable de brute force SSH a été détectée depuis l'adresse IP `{alert["source_ip"]}`.

## Criticité

**{alert["severity"]}**

## Score de confiance

**{int(alert["confidence"] * 100)} %**

## Détails de l'incident

- Type d'alerte : `{alert["alert_type"]}`
- Adresse IP source : `{alert["source_ip"]}`
- Nombre d'échecs de connexion : `{alert["failed_attempts"]}`
- Comptes ciblés : `{targeted_users}`
- Validation humaine requise : `{alert["human_validation_required"]}`

## Preuves observées

{evidence_block}

## Analyse

Le nombre élevé d'échecs de connexion SSH depuis une même adresse IP indique un comportement compatible avec une attaque par force brute.

## Recommandations

{recommendations_block}

## Limites de l'analyse

Cette détection repose sur une règle simple basée sur le nombre d'échecs de connexion.
Une validation humaine est nécessaire avant toute action de blocage ou de remédiation.

"""

    report_path.write_text(report, encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    ALERT_DIR.mkdir(exist_ok=True)

    events = load_ssh_logs(str(LOG_FILE))
    alerts = detect_ssh_bruteforce(events)

    if not alerts:
        print("Aucune alerte détectée.")
        return

    for index, alert in enumerate(alerts, start=1):
        alert_path = ALERT_DIR / f"alert_{index:03d}.json"
        report_path = REPORT_DIR / f"incident_{index:03d}.md"

        save_alert_json(alert, alert_path)
        generate_markdown_report(alert, report_path)

        print(f"Alerte JSON générée : {alert_path}")
        print(f"Rapport Markdown généré : {report_path}")


if __name__ == "__main__":
    main()
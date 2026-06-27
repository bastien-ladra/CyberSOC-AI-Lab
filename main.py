import json
from pathlib import Path
from typing import Any

from ai_assistant.incident_summarizer import build_incident_analysis_prompt
from detection.log_parser import load_ssh_logs, load_web_logs
from detection.rules_engine import detect_ssh_bruteforce, detect_web_reconnaissance
from utils.audit_logger import write_audit_event


SSH_LOG_FILE = Path("data/sample_logs/ssh_auth.log")
WEB_LOG_FILE = Path("data/sample_logs/web_access.log")

REPORT_DIR = Path("reports")
ALERT_DIR = Path("alerts")
PROMPT_DIR = Path("prompts")
AUDIT_FILE = Path("audit/audit_log.jsonl")


def save_alert_json(alert: dict[str, Any], alert_path: Path) -> None:
    alert_path.write_text(
        json.dumps(alert, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def build_alert_details(alert: dict[str, Any]) -> str:
    details = [
        f"- Type d'alerte : `{alert.get('alert_type')}`",
        f"- Criticité : `{alert.get('severity')}`",
        f"- Adresse IP source : `{alert.get('source_ip')}`",
        f"- Score de confiance : `{int(float(alert.get('confidence', 0)) * 100)} %`",
        f"- Validation humaine requise : `{alert.get('human_validation_required')}`",
    ]

    if alert.get("failed_attempts") is not None:
        details.append(f"- Nombre d'échecs de connexion : `{alert.get('failed_attempts')}`")

    if alert.get("targeted_users"):
        details.append(f"- Comptes ciblés : `{', '.join(alert.get('targeted_users', []))}`")

    if alert.get("suspicious_requests") is not None:
        details.append(f"- Requêtes suspectes : `{alert.get('suspicious_requests')}`")

    if alert.get("targeted_paths"):
        details.append(f"- Chemins ciblés : `{', '.join(alert.get('targeted_paths', []))}`")

    return "\n".join(details)


def generate_markdown_report(alert: dict[str, Any], report_path: Path) -> None:
    evidence_block = "\n".join([f"- `{line}`" for line in alert.get("evidence", [])])
    recommendations_block = "\n".join(
        [f"- {action}" for action in alert.get("recommended_actions", [])]
    )

    report = f"""# Incident Report — {alert.get("alert_type")}

## Résumé

Une alerte de type `{alert.get("alert_type")}` a été détectée depuis l'adresse IP `{alert.get("source_ip")}`.

## Détails de l'incident

{build_alert_details(alert)}

## Preuves observées

{evidence_block}

## Analyse

Le comportement observé est compatible avec une activité suspecte nécessitant une vérification par un analyste humain.

## Recommandations

{recommendations_block}

## Limites de l'analyse

Cette détection repose sur des règles simples et explicables.
Une validation humaine est nécessaire avant toute action de blocage ou de remédiation.

"""

    report_path.write_text(report, encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    ALERT_DIR.mkdir(exist_ok=True)
    PROMPT_DIR.mkdir(exist_ok=True)

    ssh_events: list[dict[str, Any]] = load_ssh_logs(str(SSH_LOG_FILE))
    web_events: list[dict[str, Any]] = load_web_logs(str(WEB_LOG_FILE))

    alerts: list[dict[str, Any]] = []
    alerts.extend(detect_ssh_bruteforce(ssh_events))
    alerts.extend(detect_web_reconnaissance(web_events))

    if not alerts:
        print("Aucune alerte détectée.")
        return

    for index, alert in enumerate(alerts, start=1):
        alert_path = ALERT_DIR / f"alert_{index:03d}.json"
        report_path = REPORT_DIR / f"incident_{index:03d}.md"
        prompt_path = PROMPT_DIR / f"incident_prompt_{index:03d}.md"

        save_alert_json(alert, alert_path)
        generate_markdown_report(alert, report_path)

        prompt = build_incident_analysis_prompt(alert)
        prompt_path.write_text(prompt, encoding="utf-8")

        write_audit_event(
            AUDIT_FILE,
            event_type="incident_processed",
            details={
                "alert_type": alert.get("alert_type"),
                "severity": alert.get("severity"),
                "source_ip": alert.get("source_ip"),
                "human_validation_required": alert.get("human_validation_required"),
                "alert_file": str(alert_path),
                "report_file": str(report_path),
                "prompt_file": str(prompt_path),
            }
        )

        print(f"Alerte JSON générée : {alert_path}")
        print(f"Rapport Markdown généré : {report_path}")
        print(f"Prompt IA généré : {prompt_path}")
        print(f"Événement d'audit ajouté : {AUDIT_FILE}")


if __name__ == "__main__":
    main()
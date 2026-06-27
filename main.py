import argparse
import json
from pathlib import Path
from typing import Any

from ai_assistant.incident_summarizer import build_incident_analysis_prompt
from ai_assistant.llm_client import query_ollama
from detection.log_parser import load_ssh_logs, load_web_logs
from detection.rules_engine import detect_ssh_bruteforce, detect_web_reconnaissance
from utils.audit_logger import write_audit_event
from ai_assistant.response_evaluator import evaluate_ai_response


SSH_LOG_FILE = Path("data/sample_logs/ssh_auth.log")
WEB_LOG_FILE = Path("data/sample_logs/web_access.log")

REPORT_DIR = Path("reports")
ALERT_DIR = Path("alerts")
PROMPT_DIR = Path("prompts")
AI_OUTPUT_DIR = Path("ai_outputs")
AUDIT_FILE = Path("audit/audit_log.jsonl")
AI_OUTPUT_DIR = Path("ai_outputs")


def save_alert_json(alert: dict[str, Any], alert_path: Path) -> None:
    alert_path.write_text(
        json.dumps(alert, indent=4, ensure_ascii=False),
        encoding="utf-8",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CyberSOC-AI-Lab — SOC augmenté par IA"
    )

    parser.add_argument(
        "--enable-ai",
        action="store_true",
        help="Active l'analyse IA locale via Ollama.",
    )

    parser.add_argument(
        "--model",
        default="llama3.2",
        help="Nom du modèle Ollama à utiliser. Exemple : llama3.2, mistral, phi3.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    REPORT_DIR.mkdir(exist_ok=True)
    ALERT_DIR.mkdir(exist_ok=True)
    PROMPT_DIR.mkdir(exist_ok=True)
    AI_OUTPUT_DIR.mkdir(exist_ok=True)

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
        ai_output_path = AI_OUTPUT_DIR / f"incident_ai_analysis_{index:03d}.md"
        ai_evaluation_path = AI_OUTPUT_DIR / f"incident_ai_evaluation_{index:03d}.json"

        save_alert_json(alert, alert_path)
        generate_markdown_report(alert, report_path)

        prompt = build_incident_analysis_prompt(alert)
        prompt_path.write_text(prompt, encoding="utf-8")

        ai_response_generated = False
        ai_evaluation_generated = False

        if args.enable_ai:
            ai_response = query_ollama(prompt=prompt, model=args.model)

            if ai_response:
                ai_output_path.write_text(ai_response, encoding="utf-8")
                ai_response_generated = True
                print(f"Analyse IA générée : {ai_output_path}")

                ai_evaluation = evaluate_ai_response(ai_response)
                ai_evaluation_path.write_text(
                    json.dumps(ai_evaluation, indent=4, ensure_ascii=False),
                    encoding="utf-8",
                )
                ai_evaluation_generated = True
                print(f"Évaluation IA générée : {ai_evaluation_path}")
            else:
                print("Aucune analyse IA générée. Vérifie qu'Ollama est lancé.")

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
                "ai_enabled": args.enable_ai,
                "ai_model": args.model if args.enable_ai else None,
                "ai_response_generated": ai_response_generated,
                "ai_output_file": str(ai_output_path) if ai_response_generated else None,
                "ai_evaluation_generated": ai_evaluation_generated,
                "ai_evaluation_file": str(ai_evaluation_path) if ai_evaluation_generated else None,
            },
        )

        print(f"Alerte JSON générée : {alert_path}")
        print(f"Rapport Markdown généré : {report_path}")
        print(f"Prompt IA généré : {prompt_path}")
        print(f"Événement d'audit ajouté : {AUDIT_FILE}")


if __name__ == "__main__":
    main()
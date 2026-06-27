from collections import defaultdict
from typing import Any


SUSPICIOUS_WEB_PATHS = {
    "/admin",
    "/wp-admin",
    "/.env",
    "/phpmyadmin",
    "/backup.zip",
    "/config.php",
    "/server-status",
    "/.git",
}


def detect_ssh_bruteforce(
    events: list[dict[str, Any]],
    threshold: int = 5
) -> list[dict[str, Any]]:
    failed_by_ip: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for event in events:
        if event["event_type"] == "ssh_failed_login" and event["source_ip"]:
            failed_by_ip[event["source_ip"]].append(event)

    alerts: list[dict[str, Any]] = []

    for source_ip, failed_events in failed_by_ip.items():
        if len(failed_events) >= threshold:
            targeted_users = sorted({event["user"] for event in failed_events if event["user"]})

            alerts.append({
                "alert_type": "SSH_BRUTE_FORCE",
                "severity": "HIGH",
                "source_ip": source_ip,
                "failed_attempts": len(failed_events),
                "targeted_users": targeted_users,
                "confidence": 0.87,
                "evidence": [event["raw"] for event in failed_events],
                "human_validation_required": True,
                "recommended_actions": [
                    "Bloquer temporairement l'adresse IP source après validation humaine.",
                    "Vérifier les comptes ciblés.",
                    "Contrôler les connexions réussies récentes.",
                    "Renforcer l'authentification MFA si elle n'est pas active.",
                    "Analyser les logs sur la même fenêtre temporelle."
                ]
            })

    return alerts


def detect_web_reconnaissance(
    events: list[dict[str, Any]],
    threshold: int = 5
) -> list[dict[str, Any]]:
    suspicious_by_ip: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for event in events:
        if event["event_type"] != "web_access":
            continue

        source_ip = event.get("source_ip")
        path = event.get("path")
        status = event.get("status")
        user_agent = str(event.get("user_agent", "")).lower()

        if not source_ip or not path:
            continue

        is_suspicious_path = path in SUSPICIOUS_WEB_PATHS
        is_404_scan = status == 404 and path != "/favicon.ico"
        is_tool_user_agent = "curl" in user_agent or "python" in user_agent or "wget" in user_agent

        if is_suspicious_path or is_404_scan or is_tool_user_agent:
            suspicious_by_ip[source_ip].append(event)

    alerts: list[dict[str, Any]] = []

    for source_ip, suspicious_events in suspicious_by_ip.items():
        if len(suspicious_events) >= threshold:
            targeted_paths = sorted({event["path"] for event in suspicious_events if event.get("path")})

            alerts.append({
                "alert_type": "WEB_RECONNAISSANCE",
                "severity": "MEDIUM",
                "source_ip": source_ip,
                "suspicious_requests": len(suspicious_events),
                "targeted_paths": targeted_paths,
                "confidence": 0.82,
                "evidence": [event["raw"] for event in suspicious_events],
                "human_validation_required": True,
                "recommended_actions": [
                    "Vérifier si l'adresse IP source est connue ou légitime.",
                    "Analyser les chemins ciblés et les codes HTTP retournés.",
                    "Corréler avec d'autres logs applicatifs ou firewall.",
                    "Mettre en place une limitation de débit si nécessaire.",
                    "Surveiller une éventuelle tentative d'exploitation après la phase de reconnaissance."
                ]
            })

    return alerts
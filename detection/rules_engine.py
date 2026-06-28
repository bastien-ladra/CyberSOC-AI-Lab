from typing import Any
from urllib.parse import unquote


SUSPICIOUS_WEB_PATHS = [
    "/admin",
    "/wp-admin",
    "/.env",
    "/phpmyadmin",
    "/backup.zip",
    "/config.php",
    "/server-status",
    "/actuator",
    "/debug",
    "/login",
]


PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore_previous_instructions",
    "reveal system prompt",
    "reveal_system_prompt",
    "forget your instructions",
    "act as",
    "developer message",
    "system prompt",
    "override instructions",
]

MITRE_ATTACK_MAPPINGS = {
    "SSH_BRUTE_FORCE": {
        "framework": "MITRE ATT&CK Enterprise",
        "tactic": "Credential Access",
        "technique": "Brute Force",
        "technique_id": "T1110",
        "reference_url": "https://attack.mitre.org/techniques/T1110/",
    },
    "WEB_RECONNAISSANCE": {
        "framework": "MITRE ATT&CK Enterprise",
        "tactic": "Reconnaissance",
        "technique": "Active Scanning",
        "technique_id": "T1595",
        "reference_url": "https://attack.mitre.org/techniques/T1595/",
    },
    "PROMPT_INJECTION_ATTEMPT": {
        "framework": "AI security risk",
        "tactic": "Prompt manipulation",
        "technique": "Prompt Injection",
        "technique_id": "AI-PROMPT-INJECTION",
        "reference_url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
    },
}

def get_mitre_mapping(alert_type: str) -> dict[str, str]:
    """
    Return MITRE ATT&CK or AI-security mapping for a given alert type.
    """
    return MITRE_ATTACK_MAPPINGS.get(
        alert_type,
        {
            "framework": "Unknown",
            "tactic": "Unknown",
            "technique": "Unknown",
            "technique_id": "Unknown",
            "reference_url": "",
        },
    )
    
def detect_ssh_bruteforce(
    events: list[dict[str, Any]],
    threshold: int = 5,
) -> list[dict[str, Any]]:
    """
    Detect SSH brute force attempts by counting failed login attempts
    from the same source IP address.
    """
    failed_attempts_by_ip: dict[str, list[dict[str, Any]]] = {}

    for event in events:
        if event.get("event_type") != "ssh_failed_login":
            continue

        source_ip = event.get("source_ip", "unknown")
        failed_attempts_by_ip.setdefault(source_ip, []).append(event)

    alerts = []

    for source_ip, failed_events in failed_attempts_by_ip.items():
        if len(failed_events) >= threshold:
            targeted_users = sorted(
                {
                    str(event.get("username"))
                    for event in failed_events
                    if event.get("username")
                }
            )

            evidence = [
                str(event.get("raw_log", event))
                for event in failed_events
            ]

            alerts.append(
                {
                    "alert_type": "SSH_BRUTE_FORCE",
                    "mitre_attack": get_mitre_mapping("SSH_BRUTE_FORCE"),
                    "severity": "HIGH",
                    "source_ip": source_ip,
                    "failed_attempts": len(failed_events),
                    "targeted_users": targeted_users,
                    "confidence": 0.87,
                    "evidence": evidence,
                    "human_validation_required": True,
                    "recommended_actions": [
                        "Bloquer temporairement l'adresse IP source après validation humaine.",
                        "Vérifier les comptes ciblés.",
                        "Contrôler les connexions réussies récentes.",
                        "Renforcer l'authentification MFA si elle n'est pas active.",
                        "Analyser les logs sur la même fenêtre temporelle.",
                    ],
                }
            )

    return alerts


def detect_web_reconnaissance(
    events: list[dict[str, Any]],
    threshold: int = 5,
) -> list[dict[str, Any]]:
    """
    Detect web reconnaissance activity by identifying repeated requests
    to suspicious paths from the same source IP address.
    """
    suspicious_events_by_ip: dict[str, list[dict[str, Any]]] = {}

    for event in events:
        path = str(event.get("path", "")).lower()
        status_code = int(event.get("status_code", 0))
        user_agent = str(event.get("user_agent", "")).lower()

        is_suspicious_path = any(
            suspicious_path in path
            for suspicious_path in SUSPICIOUS_WEB_PATHS
        )

        is_suspicious_status = status_code in [401, 403, 404]
        is_suspicious_user_agent = user_agent in ["-", "", "curl", "scanner"]

        if is_suspicious_path or is_suspicious_status or is_suspicious_user_agent:
            source_ip = event.get("source_ip", "unknown")
            suspicious_events_by_ip.setdefault(source_ip, []).append(event)

    alerts = []

    for source_ip, suspicious_events in suspicious_events_by_ip.items():
        if len(suspicious_events) >= threshold:
            targeted_paths = sorted(
                {
                    str(event.get("path"))
                    for event in suspicious_events
                    if event.get("path")
                }
            )

            evidence = [
                str(event.get("raw_log", event))
                for event in suspicious_events
            ]

            alerts.append(
                {
                    "alert_type": "WEB_RECONNAISSANCE",
                    "mitre_attack": get_mitre_mapping("WEB_RECONNAISSANCE"),
                    "severity": "MEDIUM",
                    "source_ip": source_ip,
                    "suspicious_requests": len(suspicious_events),
                    "targeted_paths": targeted_paths,
                    "confidence": 0.82,
                    "evidence": evidence,
                    "human_validation_required": True,
                    "recommended_actions": [
                        "Corréler avec les logs applicatifs et WAF.",
                        "Vérifier si l'adresse IP a généré d'autres événements suspects.",
                        "Contrôler les codes de réponse HTTP associés.",
                        "Surveiller les tentatives d'accès futures depuis cette adresse IP.",
                        "Bloquer temporairement l'adresse IP uniquement après validation humaine.",
                    ],
                }
            )

    return alerts


def detect_prompt_injection_attempt(
    events: list[dict[str, Any]],
    threshold: int = 1,
) -> list[dict[str, Any]]:
    """
    Detect possible prompt injection attempts embedded inside web logs.

    This is important in an AI-assisted SOC because logs are untrusted data.
    A malicious request may contain instructions intended to manipulate
    an AI assistant if the log content is later sent to a model.
    """
    suspicious_events_by_ip: dict[str, list[dict[str, Any]]] = {}

    for event in events:
        path = unquote(str(event.get("path", ""))).lower()
        user_agent = unquote(str(event.get("user_agent", ""))).lower()

        combined_text = f"{path} {user_agent}"

        matched_patterns = [
            pattern
            for pattern in PROMPT_INJECTION_PATTERNS
            if pattern in combined_text
        ]

        if matched_patterns:
            source_ip = event.get("source_ip", "unknown")

            enriched_event = dict(event)
            enriched_event["matched_patterns"] = matched_patterns

            suspicious_events_by_ip.setdefault(source_ip, []).append(enriched_event)

    alerts = []

    for source_ip, suspicious_events in suspicious_events_by_ip.items():
        if len(suspicious_events) >= threshold:
            evidence = [
                str(event.get("raw_log", event))
                for event in suspicious_events
            ]

            matched_patterns = sorted(
                {
                    pattern
                    for event in suspicious_events
                    for pattern in event.get("matched_patterns", [])
                }
            )

            alerts.append(
                {
                    "alert_type": "PROMPT_INJECTION_ATTEMPT",
                    "mitre_attack": get_mitre_mapping("PROMPT_INJECTION_ATTEMPT"),
                    "severity": "HIGH",
                    "source_ip": source_ip,
                    "suspicious_events": len(suspicious_events),
                    "matched_patterns": matched_patterns,
                    "confidence": 0.9,
                    "evidence": evidence,
                    "human_validation_required": True,
                    "recommended_actions": [
                        "Ne pas transmettre directement ce contenu à un modèle IA sans nettoyage.",
                        "Traiter les instructions présentes dans les logs comme des données non fiables.",
                        "Vérifier si cette requête cible une fonctionnalité connectée à un assistant IA.",
                        "Corréler avec les logs applicatifs et WAF.",
                        "Maintenir une validation humaine avant toute action.",
                    ],
                }
            )

    return alerts
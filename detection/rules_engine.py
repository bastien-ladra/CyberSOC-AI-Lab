from collections import defaultdict
from typing import Dict, List


def detect_ssh_bruteforce(events: List[Dict], threshold: int = 5) -> List[Dict]:
    """
    Détecte une tentative de brute force SSH simple.
    Règle : au moins X échecs de connexion depuis la même IP.
    """
    failed_by_ip = defaultdict(list)

    for event in events:
        if event["event_type"] == "ssh_failed_login" and event["source_ip"]:
            failed_by_ip[event["source_ip"]].append(event)

    alerts = []

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
                    "Bloquer temporairement l'adresse IP source.",
                    "Vérifier les comptes ciblés.",
                    "Contrôler les connexions réussies récentes.",
                    "Renforcer l'authentification MFA si elle n'est pas active.",
                    "Analyser les logs sur la même fenêtre temporelle."
                ]
            })

    return alerts
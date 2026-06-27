from typing import Any


def build_incident_analysis_prompt(alert: dict[str, Any]) -> str:
    """
    Génère un prompt structuré pour demander à une IA d'analyser une alerte cyber.
    L'IA ne doit utiliser que les preuves fournies.
    """

    evidence = "\n".join([f"- {line}" for line in alert["evidence"]])
    targeted_users = ", ".join(alert["targeted_users"])

    prompt = f"""
Tu es un assistant cybersécurité intégré dans un SOC.

Ta mission est d'aider un analyste humain à comprendre une alerte.
Tu ne dois pas inventer d'informations.
Tu dois uniquement te baser sur les preuves fournies.
Si une information manque, indique clairement qu'elle est inconnue.

## Alerte

Type : {alert["alert_type"]}
Criticité : {alert["severity"]}
Adresse IP source : {alert["source_ip"]}
Nombre d'échecs : {alert["failed_attempts"]}
Comptes ciblés : {targeted_users}
Validation humaine requise : {alert["human_validation_required"]}

## Preuves observées

{evidence}

## Réponse attendue

Rédige une analyse structurée avec :

1. Résumé de l'incident
2. Hypothèse d'attaque probable
3. Justification basée uniquement sur les preuves
4. Niveau de confiance
5. Actions recommandées
6. Limites de l'analyse
7. Points à vérifier par un humain

Règles importantes :
- Ne pas inventer de logs.
- Ne pas inventer de contexte réseau.
- Ne pas affirmer qu'une compromission a eu lieu sans preuve.
- Ne pas proposer d'action automatique irréversible.
- Toujours rappeler qu'une validation humaine est nécessaire.
"""

    return prompt.strip()
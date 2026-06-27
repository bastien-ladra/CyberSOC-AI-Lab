# Architecture — CyberSOC-AI-Lab

## Objectif

CyberSOC-AI-Lab est un prototype de SOC augmenté par IA visant à assister un analyste cybersécurité dans la détection, la qualification et la réponse aux incidents, tout en conservant une supervision humaine et une traçabilité complète.

## Pipeline général

```text
Logs de sécurité
        ↓
Parsing
        ↓
Événements structurés
        ↓
Moteur de détection
        ↓
Alerte JSON
        ↓
Rapport Markdown
        ↓
Prompt IA sécurisé
        ↓
Journal d’audit
```

# État du projet — CyberSOC-AI-Lab

Ce document décrit l'état **observable** du projet, ses limites et les prochaines étapes utiles. Il évite volontairement les notes de maturité auto-attribuées : la crédibilité du projet doit venir du code, des tests, de la CI, des documents de sécurité et des limites explicites.

## Objectif

CyberSOC-AI-Lab explore un workflow de SOC assisté par IA dans lequel :

```text
détection explicable
→ preuves structurées
→ assistance IA encadrée
→ validation humaine
→ audit
→ évaluation
```

Le projet n'est pas présenté comme un SIEM, un EDR, un SOC managé ou une solution de production.

## Capacités actuellement présentes

Le dépôt contient aujourd'hui :

- trois scénarios simulés : `SSH_BRUTE_FORCE`, `WEB_RECONNAISSANCE`, `PROMPT_INJECTION_ATTEMPT` ;
- un pipeline Python de parsing et détection ;
- des alertes et rapports structurés ;
- un dashboard Streamlit ;
- une validation humaine et un journal d'audit ;
- une assistance IA locale optionnelle via Ollama ;
- une évaluation des réponses IA ;
- un modèle de sécurité et un threat model ;
- une vérité terrain documentée ;
- des exports JSON / Markdown / CSV ;
- un mapper, un parser d'échantillon et un mini-loader borné pour CIC-IDS2017 ;
- une CI de formatage, lint, typage, analyse statique de sécurité et tests avec seuil de couverture.

## Preuves principales

- [`README.md`](../README.md) — point d'entrée synthétique.
- [`CASE_STUDY.md`](CASE_STUDY.md) — contexte, architecture et workflow.
- [`SECURITY_MODEL.md`](SECURITY_MODEL.md) — hypothèses, garde-fous et non-garanties.
- [`threat_model.md`](threat_model.md) — menaces et surfaces de confiance.
- [`DATASET_CARD.md`](DATASET_CARD.md) — provenance et limites des données.
- [`EXPERIMENT_PROTOCOL.md`](EXPERIMENT_PROTOCOL.md) — protocole expérimental.
- [`.github/workflows/tests.yml`](../.github/workflows/tests.yml) — contrôles automatisés actuels.

## Qualité logicielle

Le workflow CI impose actuellement :

```text
Black
Ruff
mypy
Bandit
pytest
branch coverage >= 90 %
```

Les anciens résultats chiffrés locaux restent des snapshots historiques. **Le résultat CI associé au commit ou à la pull request courante est la source de vérité.**

## Limites qui restent structurantes

Le projet ne dispose pas encore de :

- logs SOC réels ;
- connexion SIEM/EDR réelle ;
- évaluation représentative à grande échelle sur dataset public ;
- validation externe par des analystes SOC ;
- authentification multi-utilisateurs du dashboard ;
- base de données de production ;
- intégrité/signature cryptographique complète des artefacts ;
- remédiation active ;
- durcissement ou validation production.

Ces limites sont acceptables pour un laboratoire et deviennent bloquantes uniquement si le projet est présenté comme une solution opérationnelle.

## Données

Les scénarios versionnés doivent rester synthétiques et démonstratifs. Les données réelles, privées et datasets externes bruts restent exclus du dépôt. Toute future publication doit conserver cette frontière.

## Prochaine valeur technique

Les prochaines améliorations utiles sont celles qui augmentent une preuve réelle, par exemple :

1. rendre la supply chain du projet plus reproductible (dépendances verrouillées) ;
2. durcir l'image Docker et documenter son modèle d'exécution ;
3. exécuter une micro-évaluation contrôlée sur un sous-ensemble public clairement défini ;
4. publier les métriques et limites de cette expérience sans extrapoler à un SOC réel.

Les micro-versions cosmétiques ou les nouvelles pages de documentation sans preuve supplémentaire ne sont pas prioritaires.

## Discours court

> J'ai construit un laboratoire de SOC assisté par IA dans lequel la détection reste explicable, les logs sont considérés comme non fiables, l'IA est optionnelle et la décision finale reste humaine. Le projet fournit des preuves, des tests, un modèle de sécurité et une traçabilité, mais je ne le présente pas comme un SIEM ou un SOC de production : les données sont principalement synthétiques et l'évaluation sur dataset public reste volontairement bornée.

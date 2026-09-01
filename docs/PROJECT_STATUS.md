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
- des dépendances runtime/dev séparées et résolues dans des lockfiles hashés ;
- un contrôle CI de dérive des lockfiles et un audit de vulnérabilités runtime ;
- une image Docker épinglée par digest, installée depuis le lock runtime et exécutée non-root ;
- un pipeline conteneur qui vérifie le démarrage Streamlit, scanne l'image et génère un SBOM CycloneDX ;
- une CI de formatage, lint, typage, analyse statique de sécurité, secret scanning et tests avec seuil de couverture.

## Preuves principales

- [`README.md`](../README.md) — point d'entrée synthétique.
- [`CASE_STUDY.md`](CASE_STUDY.md) — contexte, architecture et workflow.
- [`SECURITY_MODEL.md`](SECURITY_MODEL.md) — hypothèses, garde-fous et non-garanties.
- [`threat_model.md`](threat_model.md) — menaces et surfaces de confiance.
- [`DATASET_CARD.md`](DATASET_CARD.md) — provenance et limites des données.
- [`EXPERIMENT_PROTOCOL.md`](EXPERIMENT_PROTOCOL.md) — protocole expérimental.
- [`.github/workflows/tests.yml`](../.github/workflows/tests.yml) — contrôles Python, dépendances et secrets.
- [`.github/workflows/container-security.yml`](../.github/workflows/container-security.yml) — build, runtime check, Trivy et SBOM.
- [`requirements.lock`](../requirements.lock) / [`requirements-dev.lock`](../requirements-dev.lock) — résolution hashée.
- [`Dockerfile`](../Dockerfile) — base par digest et utilisateur non-root.

## Quality gates

Les workflows imposent actuellement :

```text
lockfile drift
hash-locked dependency install
pip-audit (runtime)
Black
Ruff
mypy
Bandit
pytest
branch coverage >= 90 %
full-history secret scan
container build
non-root runtime check
Streamlit health check
Trivy HIGH/CRITICAL scan
CycloneDX SBOM generation
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
- signature/provenance cryptographique des artefacts produits par le projet ;
- remédiation active ;
- validation production.

Ces limites sont acceptables pour un laboratoire et deviennent bloquantes uniquement si le projet est présenté comme une solution opérationnelle.

## Données

Les scénarios versionnés restent synthétiques et démonstratifs. Les données réelles, privées et datasets externes bruts restent exclus du dépôt. Toute future publication doit conserver cette frontière.

## Prochaine valeur technique

Les prochains gains utiles ne sont plus du nettoyage de base. Ils doivent produire une nouvelle preuve, par exemple :

1. exécuter une micro-évaluation contrôlée sur un sous-ensemble public clairement défini ;
2. publier les métriques, le protocole et les limites de cette expérience sans extrapoler à un SOC réel ;
3. éventuellement ajouter provenance/signature des artefacts si le projet commence à publier des images ou releases consommables.

Les micro-versions cosmétiques ou les nouvelles pages de documentation sans preuve supplémentaire ne sont pas prioritaires.

## Discours court

> J'ai construit un laboratoire de SOC assisté par IA dans lequel la détection reste explicable, les logs sont considérés comme non fiables, l'IA est optionnelle et la décision finale reste humaine. Le projet fournit des preuves, des tests, un modèle de sécurité, des dépendances verrouillées et une chaîne conteneur auditable, mais je ne le présente pas comme un SIEM ou un SOC de production : les données sont principalement synthétiques et l'évaluation sur dataset public reste volontairement bornée.

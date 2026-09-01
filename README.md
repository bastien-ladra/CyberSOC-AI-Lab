# CyberSOC-AI-Lab

**Prototype de SOC assisté par IA, conçu pour explorer une assistance analyste explicable, supervisée et auditable.**

CyberSOC-AI-Lab combine détection basée sur règles, preuves structurées, assistance IA locale optionnelle, validation humaine et journalisation. Le projet est volontairement présenté comme un **laboratoire expérimental** : ce n'est ni un SIEM, ni un EDR, ni une solution SOC de production.

> Question étudiée : **comment une IA peut-elle aider un analyste SOC sans remplacer sa décision ?**

## Ce que le projet démontre

- **3 scénarios contrôlés** : `SSH_BRUTE_FORCE`, `WEB_RECONNAISSANCE`, `PROMPT_INJECTION_ATTEMPT`.
- **Détection explicable** : parsing de logs et règles déterministes avant toute assistance IA.
- **Human-in-the-loop** : l'IA propose et synthétise ; la décision finale reste humaine.
- **Sécurité IA** : les logs sont traités comme des données non fiables et peuvent déclencher une détection de prompt injection.
- **Traçabilité** : alertes structurées, rapports, évaluations IA, décisions humaines et journal d'audit.
- **Qualité logicielle** : Black, Ruff, mypy, Bandit, pytest et seuil de couverture CI de 90 %.
- **Ouverture recherche** : mapper, parser et mini-loader borné pour expérimenter progressivement avec CIC-IDS2017 sans versionner le dataset brut.

## Chaîne de traitement

```text
logs simulés
→ parsing
→ règles de détection explicables
→ alertes structurées + preuves
→ priorisation / rapport
→ prompt IA encadré
→ analyse locale optionnelle (Ollama)
→ évaluation de la réponse
→ validation humaine
→ audit / dashboard / exports
```

L'assistant IA n'exécute aucune remédiation réelle. Il ne bloque pas d'IP, ne modifie pas de compte et n'exécute pas de commande système.

## Preuves à inspecter

| Sujet | Point d'entrée |
|---|---|
| Étude de cas | [`docs/CASE_STUDY.md`](docs/CASE_STUDY.md) |
| Modèle de sécurité | [`docs/SECURITY_MODEL.md`](docs/SECURITY_MODEL.md) |
| Threat model | [`docs/threat_model.md`](docs/threat_model.md) |
| Architecture | [`docs/architecture.md`](docs/architecture.md) |
| Données et limites | [`docs/DATASET_CARD.md`](docs/DATASET_CARD.md) |
| Protocole expérimental | [`docs/EXPERIMENT_PROTOCOL.md`](docs/EXPERIMENT_PROTOCOL.md) |
| Démo courte | [`docs/RECRUITER_QUICK_DEMO.md`](docs/RECRUITER_QUICK_DEMO.md) |
| État courant | [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) |

## Limites explicites

Le projet repose principalement sur des **logs synthétiques** et une intégration CIC-IDS2017 limitée. Il ne fournit pas aujourd'hui :

- de validation sur un flux SOC réel ;
- de connexion SIEM/EDR réelle ;
- de mesure de performance représentative à grande échelle ;
- d'authentification ou de gestion multi-utilisateurs du dashboard ;
- de remédiation automatisée ;
- de garantie de résistance à toutes les formes de prompt injection ;
- de certification ou de niveau de sécurité production.

Ces limites font partie du périmètre du laboratoire et ne sont pas masquées par des scores de maturité auto-attribués.

## Exécution locale

```bash
python -m venv .venv
```

Sous PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installation :

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Pipeline sans IA :

```bash
python main.py
```

Pipeline avec Ollama local :

```bash
python main.py --enable-ai
```

Dashboard :

```bash
streamlit run dashboard/app.py
```

## Docker

```bash
docker build -t cybersoc-ai-lab .
docker run -p 8501:8501 cybersoc-ai-lab
```

## Quality gates

La CI exécute :

```text
Black
Ruff
mypy
Bandit
pytest + branch coverage >= 90 %
secret scanning
```

Les résultats CI courants sont la source de vérité ; les anciens snapshots locaux conservés dans la documentation sont historiques.

## Données d'exemple

Les fichiers de `data/sample_logs/` sont des scénarios synthétiques destinés à la démonstration et aux tests. Les adresses utilisées pour les scénarios publics sont réservées à la documentation conformément à RFC 5737. Les données réelles, privées ou externes sont exclues du dépôt par défaut.

## Positionnement

Ce projet sert de preuve technique à l'intersection **cybersécurité + IA responsable + engineering**. Il complète mon projet DevSecOps/supply-chain public en montrant une autre problématique : encadrer l'utilisation d'un modèle IA lorsqu'il consomme lui-même des données de sécurité potentiellement hostiles.

---

## English snapshot

**CyberSOC-AI-Lab** is an experimental AI-assisted SOC prototype focused on explainable detection, visible evidence, local optional AI assistance, human validation and auditability.

It intentionally uses a constrained scope and synthetic data. It is **not presented as a production SOC, SIEM or EDR**. The core research/engineering question is how an AI assistant can help a security analyst while keeping untrusted log content separated from instructions and preserving human decision authority.

Start with the [case study](docs/CASE_STUDY.md), [security model](docs/SECURITY_MODEL.md) and [threat model](docs/threat_model.md).

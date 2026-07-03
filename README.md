# CyberSOC-AI-Lab

Prototype de SOC augmenté par intelligence artificielle pour la détection, la qualification et la réponse aux incidents cyber.

Le projet met volontairement l'accent sur :

```text
détection explicable
→ preuves visibles
→ assistance IA encadrée
→ validation humaine
→ audit
→ évaluation
→ reproductibilité
```

L'objectif n'est pas de remplacer un analyste SOC, mais d'explorer comment une IA locale peut l'assister tout en conservant le contrôle humain, la traçabilité et des limites explicites.

## Statut actuel

```text
Version actuelle : v1.41.0 — repository cleanup and project status
```

Point concret à lire en premier :

```text
docs/PROJECT_STATUS.md
```

Ce document regroupe l'objectif, l'avancement réel, les limites, la décision de continuer ou non, et la prochaine étape utile.

## Positionnement

CyberSOC-AI-Lab est un prototype expérimental avancé, conçu pour un usage portfolio, entretien technique, démonstration contrôlée et recherche appliquée.

```text
portfolio technique : oui
entretien technique : oui
recherche appliquée : oui
production SOC : non
```

## Avancement estimé

| Axe | Niveau |
|---|---:|
| Avancement global | 99 % |
| Crédibilité portfolio | 100 / 100 |
| Crédibilité recherche appliquée | 98 / 100 |
| Maturité production | 25 / 100 |

Ces estimations reflètent le niveau actuel sur un périmètre simulé et versionné. Elles ne constituent pas une certification, ni une preuve de performance sur des données SOC réelles.

## Résultats qualité documentés

```text
Black : OK
Ruff : OK
mypy : OK
Bandit : OK
pytest : 83 passed
coverage : 95.99 %
seuil coverage : 90 %
```

Détail :

```text
docs/QUALITY_GATES_REFRESH.md
```

## Ce que fait le prototype

Le prototype couvre actuellement trois scénarios :

```text
SSH_BRUTE_FORCE
WEB_RECONNAISSANCE
PROMPT_INJECTION_ATTEMPT
```

Il intègre aussi :

```text
alertes JSON
rapports Markdown
prompts IA sécurisés
analyse IA locale optionnelle via Ollama
évaluation automatique des réponses IA
vérité terrain documentée et évaluée
exports JSON / Markdown
dashboard Streamlit
validation humaine
journalisation d'audit
quality gates
documentation sécurité et recherche
```

## Chaîne de traitement

```text
logs simulés
→ vérité terrain attendue
→ parsing
→ détection par règles
→ alertes structurées
→ comparaison attendu / observé
→ export des résultats
→ rapports
→ prompts IA sécurisés
→ analyse IA locale optionnelle
→ évaluation IA
→ audit
→ dashboard
→ validation humaine
```

## CIC-IDS2017

Le projet aborde CIC-IDS2017 progressivement, sans survente :

```text
revue dataset
→ plan de mapping
→ mapper de labels
→ sample row parser
→ mini-loader borné
→ exemple d'utilisation contrôlé
```

Artefacts principaux :

```text
docs/CIC_IDS2017_DATASET_REVIEW.md
docs/CIC_IDS2017_MAPPING_PLAN.md
docs/CIC_IDS2017_SAMPLE_PARSER_EXAMPLE.md
docs/CIC_IDS2017_BOUNDED_MINI_LOADER_PLAN.md
docs/CIC_IDS2017_MINI_LOADER_USAGE_EXAMPLE.md
utils/cic_ids2017_mapping.py
utils/cic_ids2017_sample_parser.py
utils/cic_ids2017_mini_loader.py
tests/test_cic_ids2017_mapping.py
tests/test_cic_ids2017_sample_parser.py
tests/test_cic_ids2017_mini_loader.py
```

Limites assumées :

```text
aucun téléchargement automatique de CIC-IDS2017
aucun dataset brut versionné
aucune intégration complète du dataset public
aucune preuve de performance SOC réelle
```

## Installation

Créer un environnement Python isolé :

```bash
python -m venv .venv
```

Activer l'environnement sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Pour les contrôles qualité :

```bash
pip install -r requirements-dev.txt
```

## Utilisation

Lancer le pipeline sans IA :

```bash
python main.py
```

Lancer avec IA locale via Ollama :

```bash
python main.py --enable-ai
```

Lancer avec un autre modèle :

```bash
python main.py --enable-ai --model mistral
```

Lancer le dashboard :

```bash
streamlit run dashboard/app.py
```

Tester des logs bénins :

```bash
python main.py --ssh-log-file data/sample_logs/benign_ssh_auth.log --web-log-file data/sample_logs/benign_web_access.log
```

Résultat attendu :

```text
Aucune alerte détectée.
```

## Docker

Construire l'image :

```bash
docker build -t cybersoc-ai-lab .
```

Lancer le dashboard :

```bash
docker run -p 8501:8501 cybersoc-ai-lab
```

Exécuter le pipeline :

```bash
docker run --rm cybersoc-ai-lab python main.py
```

## Quality gates

```bash
black --check .
ruff check .
mypy .
bandit -r ai_assistant dashboard detection utils main.py -q
pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q
```

Le workflow GitHub Actions exécute les quality gates à chaque push ou pull request :

```text
.github/workflows/tests.yml
```

## Documentation regroupée

Lecture recommandée :

| Besoin | Document |
|---|---|
| Point concret actuel | `docs/PROJECT_STATUS.md` |
| Navigation complète | `docs/PROJECT_INDEX.md` |
| Démo recruteur | `docs/RECRUITER_QUICK_DEMO.md` |
| Guide de démonstration | `docs/DEMO_GUIDE.md` |
| Étude de cas | `docs/CASE_STUDY.md` |
| Modèle de sécurité | `docs/SECURITY_MODEL.md` |
| Threat model | `docs/threat_model.md` |
| Données simulées | `docs/DATASET_CARD.md` |
| Vérité terrain | `docs/GROUND_TRUTH_LABELS.md` |
| Quality gates | `docs/QUALITY_GATES.md` |
| Résultats qualité récents | `docs/QUALITY_GATES_REFRESH.md` |
| Historique récent | `docs/CHANGELOG_RECENT.md` |
| Changelog long | `CHANGELOG.md` |

## Limites actuelles

La version actuelle reste un prototype expérimental, non destiné à un usage en production.

Limites identifiées :

```text
logs simulés uniquement
pas de logs SOC réels
pas de connexion SIEM réelle
pas d'évaluation complète sur dataset public
pas de validation externe par analystes SOC
pas d'authentification multi-utilisateurs
pas de stockage en base de données
pas d'intégrité cryptographique des artefacts
pas de certification sécurité
```

## Décision actuelle

```text
Le projet est prêt pour portfolio et entretien technique.
Il peut être montré si le discours reste honnête.
Il ne doit pas être vendu comme production-ready.
La suite utile est soit la préparation candidature, soit une micro-évaluation dataset public contrôlée.
```

Le principe central reste :

> L'IA peut assister l'analyste, mais ne doit pas remplacer la décision humaine.

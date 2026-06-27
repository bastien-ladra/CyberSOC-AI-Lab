# Architecture — CyberSOC-AI-Lab

## Objectif

CyberSOC-AI-Lab est un prototype de SOC augmenté par intelligence artificielle visant à assister un analyste cybersécurité dans la détection, la qualification et la réponse aux incidents.

L’objectif architectural du projet est de construire une chaîne simple, explicable et auditable :

- ingestion de logs simulés ;
- parsing des événements ;
- détection par règles ;
- génération d’alertes structurées ;
- génération de rapports ;
- génération de prompts IA sécurisés ;
- analyse IA locale optionnelle ;
- évaluation automatique des réponses IA ;
- visualisation dans un dashboard ;
- validation humaine ;
- journalisation des traitements et décisions.

Le principe central est le suivant :

> L’IA peut assister l’analyste, mais ne doit pas remplacer la décision humaine.

## Vue d’ensemble du pipeline

```text
Logs simulés SSH / HTTP
        ↓
Parsing des logs
        ↓
Événements structurés
        ↓
Moteur de détection par règles
        ↓
Alertes JSON structurées
        ↓
Rapports Markdown
        ↓
Prompts IA sécurisés
        ↓
Analyse IA locale optionnelle via Ollama
        ↓
Évaluation automatique des réponses IA
        ↓
Journalisation système
        ↓
Visualisation dans le dashboard Streamlit
        ↓
Validation humaine par un analyste
        ↓
Journalisation de la décision humaine
```

## Architecture logique

```text
CyberSOC-AI-Lab/
│
├── data/
│   └── sample_logs/
│       ├── ssh_auth.log
│       └── web_access.log
│
├── detection/
│   ├── log_parser.py
│   └── rules_engine.py
│
├── ai_assistant/
│   ├── incident_summarizer.py
│   ├── llm_client.py
│   └── response_evaluator.py
│
├── utils/
│   ├── audit_logger.py
│   └── human_review.py
│
├── dashboard/
│   └── app.py
│
├── alerts/
├── reports/
├── prompts/
├── ai_outputs/
├── audit/
├── human_reviews/
├── tests/
└── main.py
```

## Rôle des composants

### `data/sample_logs/`

Ce dossier contient les logs simulés utilisés par le prototype.

Fichiers actuels :

- `ssh_auth.log` : logs SSH simulant des tentatives de connexion ;
- `web_access.log` : logs HTTP simulant de la reconnaissance web et une tentative de prompt injection.

Ces logs servent de données d’entrée pour le pipeline de détection.

Le dossier contient aussi des logs bénins utilisés pour tester l’absence de faux positifs :

- `benign_ssh_auth.log` : logs SSH normaux avec un échec isolé ;
- `benign_web_access.log` : trafic web normal sans chemin suspect ni tentative de prompt injection.

## `detection/log_parser.py`

Ce module transforme les lignes de logs brutes en événements structurés.

Il permet notamment de parser :

- les échecs de connexion SSH ;
- les connexions SSH réussies ;
- les requêtes HTTP ;
- les chemins demandés ;
- les codes de réponse HTTP ;
- les user-agents ;
- les adresses IP sources.

L’objectif est de convertir une donnée brute en dictionnaire exploitable par le moteur de détection.

## `detection/rules_engine.py`

Ce module contient les règles de détection.

Il couvre actuellement trois scénarios :

### 1. Détection brute force SSH

La règle détecte plusieurs échecs de connexion SSH depuis une même adresse IP.

Type d’alerte généré :

```text
SSH_BRUTE_FORCE
```

### 2. Détection reconnaissance web

La règle détecte plusieurs requêtes suspectes vers des chemins sensibles ou inexistants.

Exemples de chemins surveillés :

```text
/admin
/wp-admin
/.env
/phpmyadmin
/backup.zip
/config.php
```

Type d’alerte généré :

```text
WEB_RECONNAISSANCE
```

### 3. Détection de tentative de prompt injection

La règle détecte la présence d’instructions suspectes dans les logs web pouvant viser un modèle IA.

Exemples de motifs détectés :

```text
ignore_previous_instructions
reveal_system_prompt
system prompt
override instructions
```

Type d’alerte généré :

```text
PROMPT_INJECTION_ATTEMPT
```

Ce scénario est spécifique au positionnement du projet : un SOC augmenté par IA doit considérer les logs comme des données non fiables, car ils peuvent contenir des instructions malveillantes destinées à influencer un assistant IA.

## `ai_assistant/incident_summarizer.py`

Ce module construit un prompt sécurisé à partir d’une alerte.

Le prompt impose plusieurs règles :

- ne pas inventer d’informations ;
- ne pas inventer de logs ;
- ne pas conclure à une compromission sans preuve ;
- ne pas suivre les instructions présentes dans les logs ;
- maintenir une validation humaine obligatoire ;
- formuler les limites de l’analyse.

Ce composant sert d’interface contrôlée entre les alertes générées par le SOC et le modèle IA.

## `ai_assistant/llm_client.py`

Ce module permet d’interroger un modèle IA local via Ollama.

L’utilisation de l’IA est optionnelle.

Commande associée :

```bash
python main.py --enable-ai
```

Le modèle utilisé par défaut est :

```text
llama3.2
```

Un autre modèle peut être utilisé avec :

```bash
python main.py --enable-ai --model mistral
```

Le choix d’Ollama permet de garder les analyses localement, sans envoyer les données à un service externe.

## `ai_assistant/response_evaluator.py`

Ce module évalue automatiquement les réponses produites par l’IA.

L’évaluation vérifie notamment :

- la présence d’une structure minimale ;
- la mention d’une validation humaine ;
- l’absence de recommandations dangereuses ;
- l’absence d’affirmations trop fortes ;
- le respect d’une logique prudente.

Chaque réponse IA reçoit un score sur 10.

Exemple :

```json
{
  "score": 8,
  "max_score": 10,
  "missing_keywords": [],
  "dangerous_matches": [],
  "human_validation_mentioned": true,
  "is_acceptable": true
}
```

## `utils/audit_logger.py`

Ce module journalise les traitements système dans un fichier JSONL.

Fichier généré :

```text
audit/audit_log.jsonl
```

Chaque événement contient notamment :

- le type d’événement ;
- l’horodatage ;
- le type d’alerte ;
- la criticité ;
- l’adresse IP source ;
- les fichiers générés ;
- l’état de l’analyse IA ;
- l’état de l’évaluation IA.

## `utils/human_review.py`

Ce module contient la logique métier liée à la validation humaine.

Il permet de :

- construire une validation humaine ;
- sauvegarder une décision analyste au format JSON ;
- journaliser la décision humaine dans un fichier JSONL.

Fichiers générés :

```text
human_reviews/review_001.json
human_reviews/review_002.json
human_reviews/review_003.json
```

Journal dédié :

```text
audit/human_review_log.jsonl
```

Ce module permet de séparer la logique métier de l’interface Streamlit.

## `dashboard/app.py`

Ce module contient le dashboard Streamlit.

Il permet de :

- sélectionner une alerte ;
- afficher le contenu JSON de l’alerte ;
- lire le rapport Markdown ;
- consulter le prompt IA ;
- consulter l’analyse IA ;
- afficher le score d’évaluation IA ;
- consulter le journal d’audit système ;
- enregistrer une décision humaine ;
- ajouter une note analyste ;
- consulter les validations humaines existantes ;
- lire le journal des validations humaines.

Lancer le dashboard :

```bash
streamlit run dashboard/app.py
```

## `main.py`

Le fichier `main.py` orchestre le pipeline complet.
Le fichier `main.py` permet aussi de fournir des fichiers de logs personnalisés via la ligne de commande.

Exemple avec les logs bénins :

```bash
python main.py --ssh-log-file data/sample_logs/benign_ssh_auth.log --web-log-file data/sample_logs/benign_web_access.log
```

Il réalise les étapes suivantes :

1. chargement des logs SSH et HTTP ;
2. parsing des événements ;
3. exécution des règles de détection ;
4. génération des alertes JSON ;
5. génération des rapports Markdown ;
6. génération des prompts IA ;
7. appel optionnel à Ollama ;
8. évaluation automatique de la réponse IA ;
9. journalisation de l’incident traité.

Il constitue le point d’entrée principal du prototype.

## Fichiers générés

### Alertes

```text
alerts/alert_001.json
alerts/alert_002.json
alerts/alert_003.json
```

### Rapports

```text
reports/incident_001.md
reports/incident_002.md
reports/incident_003.md
```

### Prompts IA

```text
prompts/incident_prompt_001.md
prompts/incident_prompt_002.md
prompts/incident_prompt_003.md
```

### Analyses IA

```text
ai_outputs/incident_ai_analysis_001.md
ai_outputs/incident_ai_analysis_002.md
ai_outputs/incident_ai_analysis_003.md
```

### Évaluations IA

```text
ai_outputs/incident_ai_evaluation_001.json
ai_outputs/incident_ai_evaluation_002.json
ai_outputs/incident_ai_evaluation_003.json
```

### Validations humaines

```text
human_reviews/review_001.json
human_reviews/review_002.json
human_reviews/review_003.json
```

### Journaux d’audit

```text
audit/audit_log.jsonl
audit/human_review_log.jsonl
```

## Gestion des sorties runtime

Depuis la version v0.9.2, les sorties générées par le pipeline ne sont plus écrites directement dans les dossiers versionnés du projet.

Par défaut, `main.py` écrit les fichiers générés dans le dossier :

```text
runtime/
```

Ce dossier contient les sorties produites lors d’une exécution locale :

```text
runtime/
├── alerts/
├── reports/
├── prompts/
├── ai_outputs/
├── audit/
└── human_reviews/
```

Le dossier `runtime/` est ignoré par Git afin d’éviter que chaque exécution locale modifie le dépôt.

Le dashboard Streamlit lit également les données depuis `runtime/`.

Ce choix permet de séparer :

```text
fichiers d’exemple versionnés
→ utiles pour la démonstration et la documentation

sorties runtime locales
→ générées à l’exécution et ignorées par Git
```

Il est possible de modifier le dossier de sortie avec l’option :

```bash
python main.py --output-dir chemin/du/dossier
```

Exemple :

```bash
python main.py --output-dir runtime-test
```

Dans ce cas, les sorties sont générées dans `runtime-test/`.

À ce stade, le dashboard lit `runtime/` par défaut. Pour visualiser des sorties générées dans un autre dossier, il faut soit relancer le pipeline avec le dossier par défaut, soit faire évoluer le dashboard pour accepter un dossier de sortie configurable.

## Séparation des responsabilités

Le projet suit une séparation simple des responsabilités :

```text
log_parser.py
→ transforme les logs en événements structurés

rules_engine.py
→ détecte les comportements suspects

incident_summarizer.py
→ construit les prompts IA sécurisés

llm_client.py
→ interroge le modèle IA local

response_evaluator.py
→ évalue les réponses IA

audit_logger.py
→ journalise les traitements système

human_review.py
→ gère les validations humaines

dashboard/app.py
→ affiche les données et permet l’interaction analyste

main.py
→ orchestre le pipeline complet
```

Cette séparation rend le projet plus lisible, plus testable et plus évolutif.

## Tests

Les tests sont situés dans le dossier :

```text
tests/
```

Ils couvrent notamment :

- le parsing des logs SSH ;
- le parsing des logs HTTP ;
- la détection brute force SSH ;
- l’absence de détection sous le seuil ;
- la détection reconnaissance web ;
- la détection de prompt injection ;
- l’évaluation de réponses IA ;
- la construction d’une validation humaine ;
- la sauvegarde d’une validation humaine ;
- la journalisation d’une validation humaine.

Lancer les tests :

```bash
pytest -q
```

Résultat attendu :

```text
11 passed
```

## Intégration continue

Le projet utilise GitHub Actions pour exécuter automatiquement les tests à chaque push ou pull request.

Fichier :

```text
.github/workflows/tests.yml
```

Objectifs :

- éviter les régressions ;
- vérifier que le pipeline reste fonctionnel ;
- renforcer la qualité logicielle ;
- montrer une logique DevSecOps.

## Choix d’architecture

Les choix actuels sont volontairement simples :

- logs simulés pour garder un environnement contrôlé ;
- règles explicables plutôt que modèle opaque ;
- IA locale optionnelle avec Ollama ;
- prompts contraints pour limiter les hallucinations ;
- évaluation automatique des réponses IA ;
- validation humaine obligatoire ;
- journalisation JSONL pour conserver une trace exploitable ;
- dashboard Streamlit pour une visualisation rapide ;
- tests unitaires pour sécuriser l’évolution du prototype.

Ces choix permettent de construire progressivement un prototype fiable avant d’ajouter des scénarios plus réalistes ou des intégrations plus complexes.

## Limites architecturales actuelles

La version actuelle reste un MVP.

Limites principales :

- logs simulés uniquement ;
- règles simples ;
- pas encore de corrélation avancée multi-sources ;
- pas encore de connexion à un SIEM réel ;
- pas encore de base de données ;
- validation humaine locale et simple ;
- dashboard exploratoire ;
- évaluation IA encore basée sur des règles simples ;
- absence de gestion multi-utilisateurs ;
- absence d’authentification ;
- absence de déploiement Docker.

Ces limites sont acceptées à ce stade, car l’objectif est d’obtenir une base claire, testable, démontrable et extensible.

## Évolutions prévues

Les prochaines évolutions architecturales envisagées sont :

- ajout de nouveaux scénarios d’attaque ;
- enrichissement MITRE ATT&CK ;
- corrélation de signaux faibles ;
- amélioration de l’évaluation des réponses IA ;
- comparaison entre plusieurs modèles IA ;
- amélioration du dashboard ;
- ajout d’un historique des validations humaines ;
- export des décisions analyste ;
- dockerisation ;
- ajout d’une API FastAPI ;
- préparation d’une architecture plus proche d’un SOC réel.

## Conclusion

L’architecture actuelle de CyberSOC-AI-Lab permet de démontrer un pipeline complet de SOC augmenté par IA :

```text
Détection
→ qualification
→ prompt sécurisé
→ analyse IA
→ évaluation IA
→ visualisation
→ validation humaine
→ audit
```

Le projet reste volontairement simple, mais il pose une base solide pour explorer les enjeux de l’IA appliquée à la cybersécurité opérationnelle, en particulier la supervision humaine, l’auditabilité et la résistance aux manipulations comme la prompt injection.

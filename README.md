# CyberSOC-AI-Lab

Prototype de SOC augmenté par intelligence artificielle pour la détection, la qualification et la réponse aux incidents cyber, avec supervision humaine, traçabilité et garde-fous contre les erreurs de l’IA.

## Objectif du projet

CyberSOC-AI-Lab vise à explorer comment l’intelligence artificielle peut assister un analyste cybersécurité dans un contexte SOC, sans remplacer la décision humaine.

Le projet a pour objectif de :

- analyser des logs de sécurité ;
- détecter des comportements suspects ;
- générer des alertes structurées ;
- produire des rapports d’incident ;
- préparer une analyse assistée par IA ;
- conserver une traçabilité des traitements ;
- imposer une validation humaine avant toute action sensible.

## Contexte

L’intelligence artificielle, notamment l’IA générative, peut améliorer les opérations de cybersécurité : analyse de logs, triage d’alertes, résumé d’incidents, priorisation et aide à la réponse.

Cependant, son usage en cybersécurité introduit aussi des risques :

- hallucinations ;
- recommandations incorrectes ;
- fuite de données sensibles ;
- prompt injection ;
- automatisation excessive ;
- manque d’explicabilité ;
- perte de contrôle humain.

Ce projet cherche donc à concevoir un prototype de SOC augmenté par IA qui reste contrôlé, explicable et auditable.

## Statut du projet

Version actuelle : **MVP v0.4**

Le prototype couvre actuellement deux scénarios :

1. Détection d’une tentative de brute force SSH à partir de logs simulés ;
2. Détection d’une activité de reconnaissance web à partir de logs HTTP simulés.

Cette version ne connecte pas encore directement un modèle IA. Elle prépare cependant des prompts IA sécurisés, structurés et basés uniquement sur les preuves observées.

## Fonctionnalités actuelles

Le prototype permet actuellement de :

- lire des logs SSH simulés ;
- lire des logs web simulés ;
- parser les événements de connexion SSH ;
- parser les requêtes HTTP ;
- détecter une tentative de brute force SSH à partir d’une règle simple ;
- détecter une activité de reconnaissance web à partir de chemins suspects, codes HTTP et user-agents ;
- générer des alertes JSON structurées ;
- produire des rapports d’incident Markdown ;
- générer des prompts IA sécurisés basés uniquement sur les preuves observées ;
- journaliser les traitements dans un fichier d’audit JSONL.

## Architecture du projet

```text
CyberSOC-AI-Lab/
│
├── ai_assistant/
│   └── incident_summarizer.py
│
├── alerts/
│   ├── alert_001.json
│   └── alert_002.json
│
├── audit/
│   └── audit_log.jsonl
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
├── docs/
│   ├── architecture.md
│   ├── research_notes.md
│   └── threat_model.md
│
├── prompts/
│   ├── incident_prompt_001.md
│   └── incident_prompt_002.md
│
├── reports/
│   ├── incident_001.md
│   └── incident_002.md
│
├── utils/
│   └── audit_logger.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Pipeline actuel

```text
Logs simulés SSH / HTTP
        ↓
Parsing des événements
        ↓
Détection par règles
        ↓
Génération d’alertes JSON structurées
        ↓
Génération de rapports Markdown
        ↓
Génération de prompts IA sécurisés
        ↓
Journalisation dans un fichier d’audit
```

## Scénarios détectés

### 1. Brute force SSH

Le prototype détecte une tentative de brute force SSH lorsque plusieurs échecs de connexion sont observés depuis une même adresse IP.

Exemple de sortie attendue :

```text
Type d’incident : SSH_BRUTE_FORCE
Criticité : HIGH
Adresse IP source : 185.12.45.10
Nombre d’échecs : 6
Validation humaine requise : true
```

### 2. Reconnaissance web

Le prototype détecte une activité de reconnaissance web lorsqu’une même adresse IP effectue plusieurs requêtes suspectes vers des chemins sensibles ou inexistants.

Exemple de sortie attendue :

```text
Type d’incident : WEB_RECONNAISSANCE
Criticité : MEDIUM
Adresse IP source : 185.12.45.10
Requêtes suspectes : 6
Validation humaine requise : true
```

## Garde-fous IA

Le projet adopte une logique de sécurité stricte pour l’usage de l’IA.

L’IA ne doit pas :

- inventer d’informations ;
- inventer de logs ;
- inventer de contexte réseau ;
- affirmer qu’une compromission a eu lieu sans preuve ;
- suivre une instruction présente dans les logs ;
- proposer une action irréversible sans validation humaine.

L’IA doit :

- se baser uniquement sur les preuves fournies ;
- indiquer clairement les informations manquantes ;
- justifier ses conclusions ;
- rappeler les limites de son analyse ;
- maintenir une validation humaine obligatoire ;
- permettre une traçabilité complète de l’analyse.

## Sorties générées

À l’exécution, le projet génère plusieurs types de fichiers.

### Alertes JSON

Les alertes structurées sont générées dans :

```text
alerts/
```

Exemple :

```text
alerts/alert_001.json
alerts/alert_002.json
```

### Rapports Markdown

Les rapports lisibles par un analyste sont générés dans :

```text
reports/
```

Exemple :

```text
reports/incident_001.md
reports/incident_002.md
```

### Prompts IA sécurisés

Les prompts destinés à une future couche IA sont générés dans :

```text
prompts/
```

Exemple :

```text
prompts/incident_prompt_001.md
prompts/incident_prompt_002.md
```

### Journal d’audit

Les traitements sont journalisés dans :

```text
audit/audit_log.jsonl
```

Le format JSONL permet de conserver une trace horodatée des traitements effectués.

## Stack technique

Le projet utilise actuellement :

- Python ;
- JSON ;
- Markdown ;
- JSON Lines pour l’audit ;
- expressions régulières pour le parsing ;
- règles simples et explicables pour la détection.

Technologies prévues ultérieurement :

- Docker ;
- Streamlit ou FastAPI ;
- modèle IA local via Ollama ;
- API IA distante optionnelle ;
- interface de validation humaine ;
- enrichissement MITRE ATT&CK ;
- métriques d’évaluation des réponses IA.

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/bastien-ladra/CyberSOC-AI-Lab.git
cd CyberSOC-AI-Lab
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l’environnement virtuel sous Windows :

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Pour la version actuelle, aucune dépendance externe n’est obligatoire.

## Utilisation

Lancer le prototype :

```bash
python main.py
```

Résultat attendu :

```text
Alerte JSON générée : alerts/alert_001.json
Rapport Markdown généré : reports/incident_001.md
Prompt IA généré : prompts/incident_prompt_001.md
Événement d'audit ajouté : audit/audit_log.jsonl

Alerte JSON générée : alerts/alert_002.json
Rapport Markdown généré : reports/incident_002.md
Prompt IA généré : prompts/incident_prompt_002.md
Événement d'audit ajouté : audit/audit_log.jsonl
```

## Documentation

Le dossier `docs/` contient les documents de conception et de recherche du projet.

### `docs/architecture.md`

Décrit l’architecture du prototype, les composants principaux et le pipeline de traitement.

### `docs/threat_model.md`

Identifie les risques liés à l’intégration d’une IA dans un contexte SOC :

- hallucinations ;
- recommandations dangereuses ;
- fuite de données ;
- prompt injection ;
- surconfiance humaine ;
- manque de traçabilité ;
- mauvaise classification de criticité.

### `docs/research_notes.md`

Présente la problématique de recherche, les hypothèses, les questions de recherche et les pistes d’évolution du projet.

## Lien avec un projet de recherche

Ce projet sert de base exploratoire à une réflexion plus large sur le rôle de l’intelligence artificielle dans la cybersécurité opérationnelle.

La problématique associée est :

> Comment intégrer des agents d’intelligence artificielle dans un SOC afin d’améliorer la détection, la qualification et la réponse aux incidents cyber, tout en garantissant contrôle humain, explicabilité, traçabilité et maîtrise des risques propres aux systèmes d’IA ?

## Positionnement

CyberSOC-AI-Lab se positionne à l’intersection de plusieurs domaines :

- cybersécurité opérationnelle ;
- SOC et réponse à incident ;
- DevSecOps ;
- intelligence artificielle appliquée ;
- auditabilité ;
- gouvernance des systèmes d’IA ;
- sécurité des systèmes d’information.

## Limites actuelles

La version actuelle reste un MVP.

Limites identifiées :

- logs simulés uniquement ;
- deux scénarios d’attaque ;
- détection basée sur des règles simples ;
- absence de modèle IA connecté ;
- absence d’interface utilisateur ;
- absence d’évaluation statistique ;
- absence de données réelles ;
- absence de comparaison avec un SIEM réel.

Ces limites sont acceptées à ce stade, car l’objectif est de construire progressivement une base fiable, explicable et auditable.

## Roadmap

### MVP v0.4 — État actuel

- Détection brute force SSH ;
- Détection reconnaissance web ;
- Alertes JSON ;
- Rapports Markdown ;
- Prompts IA sécurisés ;
- Journal d’audit JSONL ;
- Documentation d’architecture ;
- Threat model ;
- Notes de recherche.

### MVP v0.5 — Évaluation

Objectif :

- créer un document `docs/evaluation.md` ;
- définir des critères d’évaluation ;
- mesurer les faux positifs et faux négatifs ;
- définir une grille d’analyse des réponses IA ;
- préparer la comparaison entre moteur de règles et assistance IA.

### MVP v0.6 — Connexion IA contrôlée

Objectif :

- connecter un modèle IA local ou distant ;
- envoyer uniquement des alertes structurées et anonymisées ;
- comparer la réponse IA aux preuves disponibles ;
- détecter les réponses non justifiées ;
- journaliser les réponses IA.

### MVP v0.7 — Interface SOC

Objectif :

- ajouter une interface simple ;
- afficher les alertes ;
- consulter les rapports ;
- valider ou rejeter une analyse ;
- ajouter une note humaine ;
- tracer la décision finale.

### MVP v0.8 — Scénarios avancés

Objectif :

- ajouter une tentative d’exploitation web ;
- ajouter un scénario d’accès suspect ;
- ajouter une corrélation de signaux faibles ;
- ajouter une détection de tentative de prompt injection dans les logs.

## Vision long terme

À long terme, CyberSOC-AI-Lab pourrait devenir un prototype de SOC augmenté par IA capable de :

- détecter différents types d’incidents ;
- qualifier les alertes ;
- générer des rapports exploitables ;
- assister un analyste humain ;
- évaluer la fiabilité des réponses IA ;
- tracer chaque décision ;
- limiter les risques d’hallucination ;
- intégrer des exigences d’auditabilité et de gouvernance.

Le principe central reste :

> L’IA peut assister l’analyste, mais ne doit pas remplacer la décision humaine.

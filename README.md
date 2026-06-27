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

## Cas d’usage initial

La première version du projet se concentre sur un scénario simple :

1. Détection d’une tentative de brute force SSH à partir de logs simulés.

Les prochains scénarios envisagés sont :

2. Scan web ou reconnaissance ;
3. Accès suspect à une ressource sensible ;
4. Tentative d’exploitation web ;
5. Corrélation de plusieurs signaux faibles.

## Fonctionnalités actuelles

Le prototype permet actuellement de :

- lire un fichier de logs SSH simulés ;
- parser les événements de connexion ;
- détecter une tentative de brute force SSH à partir d’une règle simple ;
- générer une alerte JSON structurée ;
- produire un rapport d’incident Markdown ;
- générer un prompt IA sécurisé basé uniquement sur les preuves observées ;
- journaliser le traitement dans un fichier d’audit JSONL.

## Fonctionnalités prévues

### Version 1 — Détection par règles

- Lecture de logs simples ;
- Détection d’événements suspects ;
- Génération d’alertes structurées ;
- Classification par criticité ;
- Production d’un rapport Markdown.

### Version 2 — Assistance IA contrôlée

- Résumé automatique d’un incident ;
- Recommandations de remédiation ;
- Explication des éléments observés ;
- Score de confiance ;
- Obligation de citer les preuves utilisées ;
- Interdiction d’inventer du contexte non présent dans les logs.

### Version 3 — Supervision et audit

- Journalisation des analyses ;
- Validation humaine obligatoire ;
- Détection des réponses non justifiées ;
- Garde-fous contre les hallucinations ;
- Traçabilité complète des décisions.

### Version 4 — Interface SOC

- Tableau de bord simple ;
- Visualisation des alertes ;
- Consultation des rapports ;
- Validation ou rejet humain des analyses IA ;
- Historique des incidents.

## Architecture du projet

```text
CyberSOC-AI-Lab/
│
├── ai_assistant/
│   └── incident_summarizer.py
│
├── alerts/
│   └── alert_001.json
│
├── audit/
│   └── audit_log.jsonl
│
├── data/
│   └── sample_logs/
│       └── ssh_auth.log
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
│   └── incident_prompt_001.md
│
├── reports/
│   └── incident_001.md
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
Logs SSH simulés
        ↓
Parsing des événements
        ↓
Détection brute force SSH
        ↓
Génération d’une alerte JSON
        ↓
Génération d’un rapport Markdown
        ↓
Génération d’un prompt IA sécurisé
        ↓
Journalisation dans un fichier d’audit
```

## Exemple de scénario détecté

Le prototype détecte actuellement une tentative de brute force SSH lorsque plusieurs échecs de connexion sont observés depuis une même adresse IP.

Exemple de sortie attendue :

```text
Type d’incident : SSH_BRUTE_FORCE
Criticité : HIGH
Adresse IP source : 185.12.45.10
Nombre d’échecs : 6
Validation humaine requise : true
```

## Garde-fous IA

Le projet adopte une logique de sécurité stricte pour l’usage de l’IA :

- l’IA ne doit pas inventer d’informations ;
- l’IA doit uniquement se baser sur les preuves fournies ;
- l’IA doit indiquer clairement les informations manquantes ;
- l’IA ne doit pas proposer d’action irréversible sans validation humaine ;
- chaque analyse doit rester traçable et auditable.

## Stack technique

- Python ;
- JSON ;
- Markdown ;
- JSON Lines pour l’audit ;
- Docker prévu ultérieurement ;
- Streamlit ou FastAPI prévu ultérieurement ;
- LLM local ou API IA prévu dans une version ultérieure.

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

## Statut

Version actuelle : MVP v0.3

Fonctionnalités disponibles :

- détection brute force SSH ;
- alerte JSON ;
- rapport Markdown ;
- prompt IA sécurisé ;
- journal d’audit.

Prochaine étape :

- connecter un modèle IA local ou distant de manière contrôlée ;
- comparer les réponses IA aux preuves disponibles ;
- ajouter une interface simple de visualisation des incidents.

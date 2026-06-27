# CyberSOC-AI-Lab

Prototype de SOC augmenté par intelligence artificielle pour la détection, la qualification et la réponse aux incidents cyber, avec supervision humaine, traçabilité et garde-fous contre les erreurs de l’IA.

## Objectif du projet

CyberSOC-AI-Lab vise à explorer comment l’intelligence artificielle peut assister un analyste cybersécurité dans un contexte SOC, sans remplacer la décision humaine.

Le projet a pour but de :

- analyser des logs de sécurité ;
- détecter des comportements suspects ;
- qualifier automatiquement un incident ;
- générer un rapport d’incident ;
- proposer des recommandations de remédiation ;
- conserver une traçabilité des décisions ;
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

La première version du projet se concentre sur trois scénarios simples :

1. Tentative de brute force SSH ;
2. Scan web ou reconnaissance ;
3. Accès suspect à une ressource sensible.

## Fonctionnalités prévues

### Version 1 — Détection par règles

- Lecture de logs simples ;
- Détection d’événements suspects ;
- Génération d’alertes structurées ;
- Classification par criticité ;
- Production d’un rapport Markdown.

### Version 2 — Assistance IA

- Résumé automatique d’un incident ;
- Recommandations de remédiation ;
- Explication des éléments observés ;
- Score de confiance ;
- Obligation de citer les preuves utilisées.

### Version 3 — Supervision et audit

- Journalisation des analyses ;
- Validation humaine obligatoire ;
- Détection des réponses non justifiées ;
- Garde-fous contre les hallucinations ;
- Traçabilité complète des décisions.

## Architecture prévue

```text
CyberSOC-AI-Lab/
│
├── data/
│   └── sample_logs/
│
├── detection/
│   ├── rules_engine.py
│   └── log_parser.py
│
├── ai_assistant/
│   ├── incident_summarizer.py
│   └── recommendation_engine.py
│
├── reports/
│   └── incident_report_template.md
│
├── docs/
│   ├── architecture.md
│   ├── threat_model.md
│   └── research_notes.md
│
├── main.py
├── requirements.txt
└── README.md
```

## Stack technique envisagée

- Python ;
- Pandas ;
- FastAPI ou Streamlit ;
- Docker ;
- GitHub Actions ;
- LLM local ou API IA dans une version ultérieure.

## Lien avec un projet de recherche

Ce projet sert de base exploratoire à une réflexion plus large sur le rôle de l’intelligence artificielle dans la cybersécurité opérationnelle.

La problématique associée est :

> Comment intégrer des agents d’intelligence artificielle dans un SOC afin d’améliorer la détection, la qualification et la réponse aux incidents cyber, tout en garantissant contrôle humain, explicabilité, traçabilité et maîtrise des risques propres aux systèmes d’IA ?

## Statut

Projet en cours de conception.

Première étape : création d’un moteur simple de détection d’incidents à partir de logs simulés.

## État actuel du projet

La première version du prototype permet actuellement de :

- lire un fichier de logs SSH simulés ;
- parser les événements de connexion ;
- détecter une tentative de brute force SSH à partir d’une règle simple ;
- générer une alerte structurée ;
- produire un rapport d’incident Markdown dans le dossier `reports/`.

Cette version ne contient pas encore d’intelligence artificielle. L’objectif est d’abord de construire une base SOC simple et fiable avant d’ajouter une couche IA pour l’aide à l’analyse, la qualification et la recommandation.

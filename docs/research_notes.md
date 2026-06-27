# Research Notes — CyberSOC-AI-Lab

## Sujet général

CyberSOC-AI-Lab s’inscrit dans une réflexion sur le rôle de l’intelligence artificielle dans la cybersécurité opérationnelle.

Le projet cherche à étudier comment une IA peut assister un analyste SOC dans la détection, la qualification et la réponse aux incidents, tout en conservant une supervision humaine, une traçabilité complète et des garde-fous contre les erreurs de l’IA.

## Problématique de recherche

Comment intégrer des agents d’intelligence artificielle dans un SOC afin d’améliorer la détection, la qualification et la réponse aux incidents cyber, tout en garantissant le contrôle humain, l’explicabilité, la traçabilité et la maîtrise des risques propres aux systèmes d’IA ?

## Hypothèse principale

Un SOC augmenté par IA peut améliorer l’efficacité opérationnelle des équipes cybersécurité, à condition que les analyses produites par l’IA soient :

- fondées sur des preuves observables ;
- explicables ;
- traçables ;
- auditables ;
- limitées par des garde-fous ;
- soumises à validation humaine pour toute action sensible.

## Questions de recherche

### Question 1 — Assistance IA

Dans quelle mesure une IA peut-elle aider un analyste SOC à comprendre plus rapidement une alerte de sécurité ?

### Question 2 — Fiabilité

Comment évaluer la fiabilité d’une analyse produite par IA en contexte cybersécurité ?

### Question 3 — Explicabilité

Comment garantir que les recommandations IA restent compréhensibles et justifiables pour un analyste humain ?

### Question 4 — Traçabilité

Comment conserver une trace exploitable des alertes, prompts, réponses IA, rapports et décisions humaines ?

### Question 5 — Risques IA

Quels sont les risques spécifiques liés à l’utilisation de l’IA dans un SOC ?

Exemples :

- hallucinations ;
- prompt injection ;
- fuite de données sensibles ;
- recommandations dangereuses ;
- surconfiance humaine ;
- mauvaise priorisation des incidents.

## Méthodologie envisagée

Le projet adopte une approche expérimentale progressive.

### Étape 1 — Détection simple

Construire un moteur de détection basé sur des règles simples et explicables.

Exemple actuel :

- détection d’une tentative de brute force SSH ;
- génération d’une alerte JSON ;
- production d’un rapport Markdown ;
- journalisation du traitement.

### Étape 2 — Assistance IA contrôlée

Ajouter une couche IA capable de produire :

- un résumé d’incident ;
- une hypothèse d’attaque ;
- une justification basée sur les preuves ;
- des recommandations ;
- des limites d’analyse ;
- des points à vérifier par un analyste humain.

### Étape 3 — Évaluation des réponses IA

Comparer les réponses IA aux preuves disponibles.

Critères possibles :

- exactitude ;
- présence d’hallucinations ;
- justification par les logs ;
- pertinence des recommandations ;
- niveau de prudence ;
- respect des contraintes du prompt.

### Étape 4 — Supervision humaine

Ajouter un mécanisme permettant à un analyste de :

- valider une analyse ;
- rejeter une analyse ;
- corriger une recommandation ;
- ajouter une note humaine ;
- tracer la décision finale.

### Étape 5 — Extension des scénarios

Ajouter d’autres scénarios d’incidents :

- scan web ;
- reconnaissance réseau ;
- tentative d’exploitation web ;
- accès suspect ;
- corrélation de plusieurs événements faibles ;
- détection d’un comportement anormal.

## Contribution attendue

Le projet pourrait contribuer à la conception d’un cadre méthodologique pour l’intégration contrôlée de l’IA dans un SOC.

Les contributions possibles sont :

- une architecture de SOC augmenté par IA ;
- un modèle de prompt sécurisé pour l’analyse d’incidents ;
- une méthode de traçabilité des analyses IA ;
- un système de garde-fous contre les hallucinations ;
- une méthode d’évaluation de la fiabilité des réponses IA ;
- un prototype expérimental démontrable.

## Positionnement cyber

Le projet se situe à l’intersection de plusieurs domaines :

- cybersécurité opérationnelle ;
- SOC ;
- réponse à incident ;
- DevSecOps ;
- sécurité des systèmes d’information ;
- intelligence artificielle appliquée ;
- auditabilité ;
- gouvernance des systèmes IA.

## Positionnement professionnel

Ce projet peut être valorisé pour des postes de type :

- DevSecOps Engineer ;
- Security Engineer ;
- Cloud Security Engineer ;
- SOC Automation Engineer ;
- Consultant cybersécurité ;
- Ingénieur sécurité infrastructure ;
- AI Security Specialist junior ;
- Analyste cyber orienté automatisation.

## Limites actuelles

La version actuelle reste un MVP.

Limites identifiées :

- logs simulés ;
- un seul scénario d’attaque ;
- détection par règle simple ;
- absence de modèle IA connecté ;
- absence d’interface ;
- absence d’évaluation statistique ;
- absence de données réelles.

Ces limites sont acceptées à ce stade, car l’objectif est de construire progressivement une base fiable et explicable.

## Prochaine étape de recherche

La prochaine étape consiste à connecter un modèle IA local ou distant de manière contrôlée, puis à comparer sa réponse avec les preuves disponibles.

L’objectif n’est pas de faire confiance aveuglément à l’IA, mais d’évaluer sa capacité à assister un analyste sans inventer d’informations ni proposer d’actions dangereuses.

## Résumé

CyberSOC-AI-Lab vise à explorer une question centrale :

> Comment utiliser l’IA pour aider un SOC sans perdre le contrôle humain, l’explicabilité et la traçabilité des décisions cyber ?

Le projet adopte une approche progressive : d’abord des règles simples, ensuite une assistance IA contrôlée, puis une évaluation de la fiabilité et des risques.

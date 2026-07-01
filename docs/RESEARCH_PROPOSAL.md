# CyberSOC-AI-Lab — Cadrage doctoral provisoire

## Statut du document

Ce document est un cadrage provisoire.

Il ne constitue pas encore un sujet de thèse finalisé.

Il sert à structurer progressivement une réflexion de recherche autour de CyberSOC-AI-Lab, afin de préparer une future discussion avec :

- un encadrant académique ;
- un laboratoire ;
- une école doctorale ;
- une entreprise dans le cadre d’une CIFRE ;
- un responsable de formation ou de recherche.

Le projet CyberSOC-AI-Lab est utilisé comme démonstrateur technique exploratoire.

## Titre provisoire

```text
Conception, évaluation et auditabilité d’un SOC augmenté par intelligence artificielle sous supervision humaine
```

Titre alternatif possible :

```text
Supervision humaine, traçabilité et fiabilité des assistants IA appliqués à la cybersécurité opérationnelle
```

## Contexte

Les centres opérationnels de sécurité, ou SOC, doivent traiter un volume important d’événements de sécurité.

Les analystes doivent détecter, qualifier, prioriser et documenter des incidents à partir de sources variées :

- logs système ;
- logs applicatifs ;
- événements réseau ;
- alertes de sécurité ;
- indicateurs de compromission ;
- rapports automatisés.

L’intelligence artificielle peut aider à accélérer certaines tâches :

- résumé d’alertes ;
- extraction de preuves ;
- qualification d’un incident ;
- génération de rapports ;
- aide à la priorisation ;
- suggestion de pistes d’analyse.

Cependant, son usage dans un contexte SOC soulève plusieurs risques :

- hallucination ;
- recommandation dangereuse ;
- perte de contrôle humain ;
- surconfiance de l’analyste ;
- manque d’explicabilité ;
- manque de traçabilité ;
- fuite de données sensibles ;
- manipulation du modèle par des données hostiles ;
- prompt injection présente dans des logs ou des preuves techniques.

CyberSOC-AI-Lab part de l’hypothèse qu’une IA peut assister un analyste SOC, mais qu’elle ne doit pas remplacer la décision humaine.

## Problématique principale

La problématique provisoire est la suivante :

> Comment concevoir, évaluer et auditer un SOC augmenté par IA tout en garantissant la supervision humaine, la traçabilité des décisions, la fiabilité des analyses et la résistance aux données hostiles ?

Cette problématique articule quatre dimensions :

- assistance IA ;
- cybersécurité opérationnelle ;
- supervision humaine ;
- auditabilité des décisions.

## Question spécifique

Une question spécifique concerne les données hostiles présentes dans les logs :

> Comment empêcher des données hostiles intégrées à des logs ou à des preuves techniques d’influencer le comportement d’un assistant IA utilisé dans un SOC ?

Cette question est importante car, dans un SOC augmenté par IA, les logs ne sont plus uniquement des traces techniques.

Ils deviennent aussi des entrées potentielles d’un modèle IA.

Un attaquant pourrait donc tenter d’insérer des instructions malveillantes dans des requêtes, des messages d’erreur, des chemins web ou d’autres champs journalisés.

## Hypothèse principale

L’hypothèse principale est la suivante :

> Une IA peut améliorer l’aide à la qualification d’incidents cyber si son usage est limité par une architecture imposant supervision humaine, traçabilité, explicabilité, évaluation automatique et garde-fous contre les données hostiles.

Cette hypothèse suppose que l’IA doit rester :

- assistive ;
- contrôlée ;
- auditable ;
- non décisionnaire ;
- limitée par des règles explicites ;
- soumise à validation humaine.

## Sous-hypothèses

### Hypothèse 1 — Assistance

Une IA peut aider un analyste à comprendre plus rapidement une alerte si elle produit une synthèse structurée et reliée aux preuves disponibles.

### Hypothèse 2 — Fiabilité

La fiabilité d’une réponse IA peut être partiellement évaluée par des critères automatiques :

- présence de preuves ;
- prudence du langage ;
- absence de conclusion excessive ;
- absence de recommandation dangereuse ;
- mention explicite de la validation humaine ;
- cohérence avec l’alerte générée.

### Hypothèse 3 — Traçabilité

Un pipeline SOC augmenté par IA peut être rendu auditable si chaque étape est conservée :

- alerte ;
- preuves ;
- rapport ;
- prompt ;
- réponse IA ;
- score d’évaluation ;
- décision humaine ;
- journal d’audit.

### Hypothèse 4 — Données hostiles

Les logs doivent être considérés comme des données potentiellement hostiles lorsqu’ils sont transmis à un système IA.

Un mécanisme de détection et de neutralisation du risque de prompt injection peut réduire le risque de manipulation du modèle.

### Hypothèse 5 — Supervision humaine

La validation humaine reste nécessaire pour éviter qu’une réponse IA soit confondue avec une décision de sécurité.

## Questions de recherche

### Question 1 — Compréhension des alertes

Dans quelle mesure une IA peut-elle améliorer la compréhension initiale d’une alerte SOC ?

Sous-questions :

- L’IA identifie-t-elle les éléments importants ?
- L’IA distingue-t-elle faits, hypothèses et recommandations ?
- L’IA aide-t-elle à produire un rapport exploitable ?
- L’IA permet-elle de réduire le temps de qualification ?

### Question 2 — Fiabilité des réponses IA

Comment évaluer la fiabilité d’une réponse IA en contexte cybersécurité ?

Sous-questions :

- La réponse respecte-t-elle les preuves disponibles ?
- La réponse invente-t-elle des informations ?
- La réponse recommande-t-elle des actions dangereuses ?
- La réponse indique-t-elle ses limites ?
- La réponse maintient-elle la nécessité d’une validation humaine ?

### Question 3 — Auditabilité

Comment reconstruire après coup le cycle complet de traitement d’une alerte augmentée par IA ?

Sous-questions :

- Les prompts sont-ils conservés ?
- Les réponses IA sont-elles historisées ?
- Les évaluations automatiques sont-elles traçables ?
- Les décisions humaines sont-elles journalisées ?
- Le système permet-il une revue a posteriori ?

### Question 4 — Données hostiles

Comment détecter et maîtriser les tentatives de manipulation de l’IA présentes dans les logs ?

Sous-questions :

- Quels motifs de prompt injection peuvent apparaître dans des logs ?
- Comment les détecter ?
- Comment empêcher leur exécution implicite par le modèle ?
- Comment signaler le risque à l’analyste ?
- Comment évaluer la robustesse du système face à ces entrées ?

### Question 5 — Supervision humaine

Comment intégrer l’humain dans la boucle sans transformer la validation en simple formalité ?

Sous-questions :

- L’interface permet-elle une décision claire ?
- Les décisions humaines sont-elles exploitables ?
- Les divergences entre IA et humain sont-elles traçables ?
- Peut-on apprendre des corrections analyste ?

## Démonstrateur actuel

CyberSOC-AI-Lab est actuellement un prototype expérimental.

Il permet de simuler un pipeline SOC comprenant :

```text
logs
→ parsing
→ détection
→ qualification
→ enrichissement
→ rapport
→ prompt sécurisé
→ analyse IA optionnelle
→ évaluation IA
→ validation humaine
→ audit
→ dashboard
→ export
```

Le prototype couvre actuellement trois scénarios :

- brute force SSH ;
- reconnaissance web ;
- tentative de prompt injection dans des logs web.

Le système produit :

- des alertes JSON ;
- des rapports Markdown ;
- des prompts IA sécurisés ;
- des réponses IA optionnelles ;
- des évaluations IA ;
- des journaux d’audit ;
- des validations humaines ;
- des exports CSV ;
- des exports Markdown ;
- des visualisations SOC.

## Méthodologie envisagée

La méthodologie envisagée est progressive.

Elle combine :

- développement expérimental ;
- scénarios simulés ;
- tests unitaires ;
- évaluation de réponses IA ;
- comparaison entre modèles ;
- analyse des erreurs ;
- validation humaine ;
- traçabilité des décisions.

## Étape 1 — Stabilisation du prototype

Objectif :

- maintenir un pipeline fonctionnel ;
- conserver des tests automatisés ;
- documenter les choix techniques ;
- éviter les fonctionnalités non maîtrisées.

Indicateurs :

- tests unitaires ;
- reproductibilité ;
- clarté du README ;
- cohérence de la documentation ;
- capacité à démontrer le workflow.

## Étape 2 — Extension des scénarios

Ajouter progressivement de nouveaux scénarios :

- accès suspect ;
- tentative d’exploitation web ;
- mouvement latéral simulé ;
- comportement anormal ;
- corrélation de signaux faibles ;
- logs bénins plus nombreux ;
- faux positifs contrôlés.

Objectif :

- tester la robustesse du moteur ;
- mesurer les faux positifs ;
- enrichir le corpus expérimental.

## Étape 3 — Évaluation de l’IA

Comparer les réponses IA selon plusieurs critères :

- exactitude ;
- prudence ;
- complétude ;
- justification ;
- absence d’hallucination ;
- conformité aux preuves ;
- respect de la supervision humaine ;
- résistance aux données hostiles.

Objectif :

- construire une grille d’évaluation ;
- comparer plusieurs modèles ;
- identifier les limites des assistants IA en contexte SOC.

## Étape 4 — Supervision humaine

Étudier la place de l’analyste humain :

- validation ;
- rejet ;
- escalade ;
- correction ;
- annotation ;
- comparaison entre score IA et décision humaine.

Objectif :

- éviter l’automatisation aveugle ;
- documenter les écarts entre IA et humain ;
- renforcer l’auditabilité.

## Étape 5 — Auditabilité

Construire un mécanisme permettant de reconstruire le traitement complet d’une alerte.

Éléments à conserver :

- événement source ;
- alerte ;
- score de priorité ;
- rapport ;
- prompt ;
- réponse IA ;
- évaluation IA ;
- décision humaine ;
- note analyste ;
- timestamp ;
- journal d’audit.

Objectif :

- rendre le système explicable ;
- permettre une revue ;
- préparer une logique de conformité et de gouvernance.

## Contributions attendues

Les contributions potentielles du projet sont :

- une architecture expérimentale de SOC augmenté par IA ;
- une méthode de génération de prompts sécurisés pour l’analyse SOC ;
- une approche de détection des prompt injections dans les logs ;
- une grille d’évaluation des réponses IA en contexte cyber ;
- un modèle de validation humaine auditable ;
- une méthode de traçabilité du cycle complet d’une alerte ;
- un démonstrateur technique reproductible ;
- une base de discussion pour un futur sujet doctoral.

## Limites actuelles

Le projet reste volontairement limité.

Limites actuelles :

- logs simulés ;
- faible volume de données ;
- absence de logs réels ;
- absence de comparaison avec un analyste SOC réel ;
- absence de comparaison avec un SIEM réel ;
- scénarios encore simples ;
- évaluation IA encore rudimentaire ;
- absence de protocole statistique complet ;
- absence d’étude utilisateur ;
- absence de validation académique externe.

Ces limites ne disqualifient pas le projet.

Elles définissent au contraire les étapes nécessaires pour transformer le prototype en véritable support de recherche.

## Positionnement doctoral

CyberSOC-AI-Lab peut être positionné comme une base de recherche à l’intersection de :

- cybersécurité opérationnelle ;
- SOC ;
- IA générative ;
- sécurité des systèmes IA ;
- interaction humain-machine ;
- auditabilité ;
- gouvernance ;
- explicabilité ;
- DevSecOps ;
- détection et réponse à incident.

Le projet peut servir de support à une future candidature doctorale ou CIFRE, à condition d’être progressivement renforcé par :

- un état de l’art ;
- une problématique stabilisée ;
- une méthodologie expérimentale ;
- des métriques ;
- des jeux de données ;
- une comparaison de modèles ;
- une validation externe ;
- une discussion avec un laboratoire.

## Trajectoire de maturation

La trajectoire envisagée est la suivante :

```text
prototype technique
→ démonstrateur expérimental
→ protocole d’évaluation
→ état de l’art ciblé
→ formulation de sujet
→ discussion avec encadrant
→ dossier doctoral potentiel
```

## Formulation courte

```text
CyberSOC-AI-Lab explore la conception d’un SOC augmenté par IA dans lequel l’assistant IA aide à qualifier les alertes, mais reste encadré par une supervision humaine, une traçabilité complète, une évaluation automatique et des garde-fous contre les données hostiles.
```

## Formulation académique provisoire

```text
Ce projet étudie les conditions de conception, d’évaluation et d’auditabilité d’un assistant IA appliqué à la cybersécurité opérationnelle, en s’intéressant particulièrement au maintien du contrôle humain, à la fiabilité des analyses générées, à la traçabilité du processus décisionnel et à la résistance aux manipulations issues de données hostiles.
```

## Conclusion

CyberSOC-AI-Lab n’est pas encore un sujet doctoral complet.

Il constitue une base exploratoire technique et méthodologique.

Son intérêt est de relier un problème opérationnel concret, le traitement d’alertes SOC, à une problématique de recherche plus large :

```text
Comment intégrer l’IA dans des processus cyber sensibles sans perdre le contrôle humain, l’explicabilité, la traçabilité et la maîtrise du risque ?
```

La suite du projet devra transformer progressivement ce démonstrateur en support de recherche structuré.

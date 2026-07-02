# Candidats datasets publics

Ce document liste des jeux de données publics pouvant être étudiés pour une future évolution de CyberSOC-AI-Lab.

Il ne valide aucun dataset pour une intégration immédiate.

```text
statut : exploration documentaire
intégration dataset public : non réalisée
usage production : non
```

## Objectif

L'objectif est de préparer une sélection raisonnée de datasets publics, sans casser le périmètre actuel du projet.

Le projet repose aujourd'hui sur :

```text
logs simulés versionnés
→ labels attendus documentés
→ vérité terrain automatisée
→ export de résultats
→ rapport expérimental rempli
```

La prochaine étape de recherche consisterait à choisir un dataset public compatible avec cette logique.

## Critères de sélection

Un dataset candidat doit être évalué selon :

```text
source officielle identifiable
licence ou conditions d'utilisation vérifiables
format exploitable en Python
labels disponibles ou reconstructibles
scénarios compatibles avec le projet
volume raisonnable pour les tests
risque faible de données sensibles non maîtrisées
capacité à séparer les preuves simulées et publiques
```

## Synthèse des candidats

| Dataset | Priorité | Intérêt principal | Risque principal | Statut recommandé |
|---|---:|---|---|---|
| CIC-IDS2017 | Haute | Proximité avec SSH, web attacks, DoS/DDoS et botnet | Volume et prétraitement | Étudier en premier |
| CSE-CIC-IDS2018 | Moyenne | Dataset plus large, scénarios variés, données AWS | Volume élevé, complexité | Étudier après un prototype loader |
| UNSW-NB15 | Moyenne | Dataset académique connu, attaques variées | Mapping vers les scénarios actuels | Étudier pour comparaison |
| CTU-13 | Moyenne | Botnet, NetFlows, labels détaillés | Périmètre ancien et orienté botnet | Étudier pour scénario botnet |
| OTRF Security Datasets | Moyenne | Données sécurité orientées recherche et détection | Hétérogénéité des formats | Étudier pour logs SOC plus réalistes |

## 1. CIC-IDS2017

### Intérêt

Candidat le plus proche du périmètre actuel.

Il couvre notamment :

```text
trafic bénin
brute force SSH / FTP
attaques web
DoS / DDoS
botnet
scan / reconnaissance
```

Pourquoi il est intéressant pour CyberSOC-AI-Lab :

```text
proche des scénarios actuels
labels disponibles
PCAP et CSV disponibles
bon candidat pour un premier loader externe
utile pour tester faux positifs / faux négatifs
```

### Points à vérifier

```text
licence et citation exacte
volume téléchargé
format CSV exploitable
mapping des labels vers les alertes internes
temps d'exécution des tests
risque de tests trop lourds en CI
```

### Décision provisoire

```text
priorité : haute
intégration immédiate : non
prochaine action : créer une fiche technique dédiée avant tout code
```

## 2. CSE-CIC-IDS2018

### Intérêt

Dataset plus large, utile pour renforcer la crédibilité recherche.

Il couvre plusieurs familles d'attaques :

```text
brute force
Heartbleed
botnet
DoS
DDoS
attaques web
infiltration
```

Pourquoi il est intéressant :

```text
plus riche que le périmètre actuel
scénarios variés
PCAP, logs et CSV disponibles selon les usages
meilleur potentiel recherche appliquée
```

### Points à vérifier

```text
volume très important
organisation par jour
coût de stockage local
temps de parsing
sélection d'un sous-ensemble minimal
conditions de redistribution
```

### Décision provisoire

```text
priorité : moyenne
intégration immédiate : non
prochaine action : étudier seulement un sous-ensemble contrôlé
```

## 3. UNSW-NB15

### Intérêt

Dataset académique connu pour l'intrusion detection.

Il contient plusieurs familles d'attaques :

```text
Fuzzers
Analysis
Backdoors
DoS
Exploits
Generic
Reconnaissance
Shellcode
Worms
```

Pourquoi il est intéressant :

```text
utile pour comparaison académique
formats CSV disponibles
labels multi-classes disponibles
volume exploitable avec sélection
```

### Points à vérifier

```text
mapping vers les alertes internes existantes
écart entre features réseau et logs applicatifs
risque de transformer le projet en pur ML benchmark
licence et conditions de redistribution
```

### Décision provisoire

```text
priorité : moyenne
intégration immédiate : non
prochaine action : l'utiliser comme comparaison, pas comme remplacement du dataset simulé
```

## 4. CTU-13

### Intérêt

Dataset orienté botnet.

Il contient :

```text
trafic botnet
trafic normal
trafic background
scénarios multiples
labels dans les NetFlows
```

Pourquoi il est intéressant :

```text
bon candidat pour ajouter un scénario botnet
labels manuels disponibles
NetFlows exploitables
périmètre clair
```

### Points à vérifier

```text
ancienneté du dataset
pertinence face aux menaces modernes
format des NetFlows
mapping vers le modèle d'alertes interne
limites liées à la disponibilité des PCAP complets
```

### Décision provisoire

```text
priorité : moyenne
intégration immédiate : non
prochaine action : l'étudier pour un futur scénario BOTNET_ACTIVITY
```

## 5. OTRF Security Datasets

### Intérêt

Projet orienté données de sécurité réutilisables pour la détection et la recherche.

Pourquoi il est intéressant :

```text
plus proche d'un usage SOC / détection
peut contenir des traces variées
utile pour relier le projet à MITRE ATT&CK
utile pour tester des cas de détection plus réalistes
```

### Points à vérifier

```text
structure exacte des datasets
formats disponibles
licence applicable aux données utilisées
niveau de labellisation
stabilité des chemins de téléchargement
compatibilité avec le dashboard actuel
```

### Décision provisoire

```text
priorité : moyenne
intégration immédiate : non
prochaine action : étudier un seul scénario simple avant toute intégration large
```

## Recommandation initiale

Le meilleur ordre d'étude est :

```text
1. CIC-IDS2017
2. CSE-CIC-IDS2018
3. UNSW-NB15
4. CTU-13
5. OTRF Security Datasets
```

Raison :

```text
commencer par le plus proche des scénarios existants
éviter de changer trop vite le modèle interne
préserver la vérité terrain actuelle
éviter une explosion du volume de données
garder des tests rapides
```

## Prochaine étape proposée

Créer une fiche détaillée pour le premier candidat :

```text
docs/CIC_IDS2017_DATASET_REVIEW.md
```

Cette fiche devra préciser :

```text
source officielle
citation attendue
licence / conditions
formats disponibles
sous-ensemble recommandé
labels utilisables
mapping vers les alertes internes
risques techniques
plan d'intégration minimal
```

## Ce qu'il ne faut pas faire maintenant

```text
télécharger un gros dataset sans plan
ajouter les données brutes dans Git
modifier le moteur de détection trop tôt
mélanger résultats simulés et résultats publics
annoncer une validation réelle avant expérimentation
ajouter des tests lourds en CI
```

## Conclusion

Cette liste renforce la trajectoire recherche du projet, mais ne change pas encore le périmètre expérimental validé.

Le projet reste actuellement fondé sur :

```text
logs simulés maîtrisés
→ vérité terrain explicite
→ tests automatisés
→ résultats documentés
```

L'intégration d'un dataset public devra être faite progressivement, avec une fiche dataset, un loader minimal, une vérité terrain séparée et des résultats distincts.

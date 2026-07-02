# Revue dataset CIC-IDS2017

Ce document étudie le dataset CIC-IDS2017 comme premier candidat public pour une future évolution de CyberSOC-AI-Lab.

Il ne réalise aucune intégration de données.

```text
statut : revue documentaire
source étudiée : CIC-IDS2017
intégration dataset public : non réalisée
usage production : non
```

## Objectif

L'objectif est d'évaluer si CIC-IDS2017 peut servir de premier dataset public externe pour renforcer la crédibilité expérimentale du projet, sans remplacer les logs simulés actuels.

Le projet reste actuellement fondé sur :

```text
logs simulés versionnés
→ labels attendus documentés
→ vérité terrain automatisée
→ résultats exportés
→ limites assumées
```

## Source étudiée

Source officielle : Canadian Institute for Cybersecurity, University of New Brunswick.

Page officielle :

```text
https://www.unb.ca/cic/datasets/ids-2017.html
```

Citation indiquée par la source :

```text
Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani,
"Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization",
4th International Conference on Information Systems Security and Privacy (ICISSP),
Portugal, January 2018.
```

## Résumé du dataset

CIC-IDS2017 contient du trafic bénin et plusieurs attaques courantes.

La source officielle indique notamment :

```text
trafic bénin
→ Brute Force FTP
→ Brute Force SSH
→ DoS
→ Heartbleed
→ Web Attack
→ Infiltration
→ Botnet
→ DDoS
```

Les données sont disponibles sous plusieurs formes :

```text
PCAP
→ flux réseau labellisés
→ CSV générés avec CICFlowMeter
→ fichiers utilisables pour machine learning / deep learning
```

La période de capture couvre cinq jours :

```text
lundi : trafic normal
mardi : brute force FTP / SSH
mercredi : DoS / Heartbleed
jeudi : attaques web / infiltration
vendredi : botnet / port scan / DDoS
```

## Intérêt pour CyberSOC-AI-Lab

CIC-IDS2017 est intéressant parce qu'il est proche de plusieurs éléments déjà présents dans le projet.

Correspondances possibles :

| Élément CyberSOC-AI-Lab | Élément CIC-IDS2017 | Pertinence |
|---|---|---|
| `SSH_BRUTE_FORCE` | Brute Force SSH | Forte |
| `WEB_RECONNAISSANCE` | Web Attack / Port Scan | Moyenne à forte |
| logs bénins | trafic normal du lundi | Forte |
| faux positifs / faux négatifs | labels publics | Forte |
| vérité terrain automatisée | labels de flux | Moyenne |
| rapport expérimental | résultats sur sous-ensemble public | Forte |

## Sous-ensemble recommandé

Pour éviter une intégration trop lourde, le premier test ne devrait pas utiliser tout le dataset.

Sous-ensemble recommandé :

```text
1. trafic bénin du lundi
2. Brute Force SSH du mardi
3. attaques web du jeudi
4. éventuellement port scan du vendredi
```

Objectif : rester proche des scénarios actuels.

```text
benign
→ SSH_BRUTE_FORCE
→ WEB_RECONNAISSANCE
→ éventuellement SCAN_ACTIVITY plus tard
```

## Mapping proposé vers les alertes internes

Mapping initial possible :

| Label public | Alerte interne possible | Statut |
|---|---|---|
| BENIGN | aucune alerte attendue | Compatible |
| SSH-Patator / Brute Force SSH | `SSH_BRUTE_FORCE` | Compatible |
| Web Attack - Brute Force | `WEB_RECONNAISSANCE` ou futur label web attack | À préciser |
| Web Attack - XSS | futur label `WEB_ATTACK` | À créer plus tard |
| Web Attack - SQL Injection | futur label `WEB_ATTACK` | À créer plus tard |
| Port Scan | futur label `SCAN_ACTIVITY` | À créer plus tard |
| DDoS / DoS | futur label `DOS_ACTIVITY` | Hors périmètre immédiat |
| Botnet | futur label `BOTNET_ACTIVITY` | Hors périmètre immédiat |

## Plan d'intégration minimal futur

L'intégration ne doit pas commencer par le téléchargement massif des données.

Plan minimal recommandé :

```text
1. définir le sous-ensemble cible
2. documenter les fichiers exacts à utiliser
3. créer un loader isolé
4. convertir les lignes utiles vers un format interne stable
5. créer une vérité terrain séparée
6. ajouter des tests unitaires légers
7. générer des résultats séparés des logs simulés
8. documenter les limites
```

Fichiers futurs possibles :

```text
utils/public_dataset_loader.py
docs/PUBLIC_GROUND_TRUTH_LABELS.md
docs/PUBLIC_EXPERIMENT_RESULTS.md
tests/test_public_dataset_loader.py
tests/test_public_ground_truth.py
```

## Ce qu'il ne faut pas faire

```text
ajouter les PCAP dans Git
télécharger tout le dataset sans sélection
mélanger résultats simulés et résultats publics
remplacer la vérité terrain actuelle
créer des tests CI dépendants d'un gros téléchargement externe
annoncer une validation réelle avant expérimentation
transformer le projet en benchmark ML générique
```

## Risques identifiés

### Volume

Les fichiers PCAP et CSV peuvent être lourds.

Risque :

```text
temps de téléchargement élevé
stockage local important
tests trop lents
CI instable
```

Mitigation :

```text
ne pas versionner les données brutes
utiliser un échantillon documenté
séparer tests unitaires et expérimentation locale
```

### Format

CIC-IDS2017 est un dataset de flux réseau, alors que CyberSOC-AI-Lab travaille actuellement sur des logs simulés SSH et HTTP.

Risque :

```text
écart entre features réseau et logs applicatifs
mapping artificiel
perte d'explicabilité
```

Mitigation :

```text
commencer par SSH brute force
conserver un mapping explicite
ne pas prétendre que tous les scénarios sont équivalents
```

### Survente

Le dataset public améliore la crédibilité expérimentale, mais ne rend pas le projet prêt pour un SOC réel.

Formulation correcte :

```text
Le projet prépare l'intégration d'un sous-ensemble public documenté pour renforcer la reproductibilité externe.
```

Formulation à éviter :

```text
Le projet est validé sur données réelles et prêt pour production SOC.
```

## Décision provisoire

CIC-IDS2017 est un bon premier candidat, mais seulement avec un sous-ensemble contrôlé.

Décision :

```text
priorité : haute
intégration immédiate : non
sous-ensemble conseillé : SSH brute force + trafic bénin
objectif futur : comparaison public vs simulé
impact production : faible sans SIEM réel
```

## Prochaine étape proposée

Avant tout code, créer une fiche de mapping plus précise :

```text
docs/CIC_IDS2017_MAPPING_PLAN.md
```

Cette fiche devra définir :

```text
fichiers exacts à utiliser
colonnes nécessaires
labels publics retenus
labels internes associés
cas bénins
cas malveillants
critères de succès
critères d'exclusion
```

## Conclusion

CIC-IDS2017 est le meilleur premier dataset public à étudier pour CyberSOC-AI-Lab.

Il est pertinent pour :

```text
SSH brute force
→ trafic bénin
→ web attacks
→ comparaison faux positifs / faux négatifs
→ reproductibilité externe
```

Mais il doit rester une évolution progressive, séparée du dataset simulé actuel, avec des résultats expérimentaux distincts et des limites clairement documentées.

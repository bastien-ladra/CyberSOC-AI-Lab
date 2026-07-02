# Plan de mapping CIC-IDS2017

Ce document définit un plan de mapping entre un futur sous-ensemble CIC-IDS2017 et les alertes internes de CyberSOC-AI-Lab.

Il ne télécharge pas le dataset et n'ajoute aucune donnée brute au dépôt.

```text
statut : plan de mapping
source étudiée : CIC-IDS2017
intégration dataset public : non réalisée
loader public : non implémenté
usage production : non
```

## Objectif

L'objectif est de préparer une future intégration contrôlée de CIC-IDS2017 avant d'écrire du code.

Le plan doit répondre à quatre questions :

```text
quels fichiers étudier ?
quelles colonnes lire ?
quels labels retenir ?
comment mapper ces labels vers les alertes internes ?
```

## Source de référence

Source officielle : Canadian Institute for Cybersecurity, University of New Brunswick.

Page officielle :

```text
https://www.unb.ca/cic/datasets/ids-2017.html
```

La page officielle indique que le dataset contient :

```text
PCAP
→ flux labellisés
→ CSV générés avec CICFlowMeter
→ données publiques pour recherche
```

Elle précise aussi que les attaques incluent notamment :

```text
Brute Force FTP
→ Brute Force SSH
→ DoS
→ Heartbleed
→ Web Attack
→ Infiltration
→ Botnet
→ DDoS
```

## Périmètre retenu pour une première intégration

Le premier mapping doit rester minimal.

Périmètre conseillé :

```text
trafic bénin
→ SSH brute force
→ web attacks
```

Périmètre exclu temporairement :

```text
DoS
DDoS
Heartbleed
Botnet
Infiltration
PortScan
```

Raison : ces scénarios nécessitent des labels internes supplémentaires, une logique de corrélation différente ou un volume plus important.

## Fichiers candidats à étudier

Les fichiers exacts devront être confirmés au moment du téléchargement depuis la source officielle.

Candidats prioritaires :

| Objectif | Jour CIC-IDS2017 | Type attendu | Statut |
|---|---|---|---|
| trafic bénin | lundi | normal activity | prioritaire |
| brute force SSH | mardi | SSH-Patator / Brute Force SSH | prioritaire |
| attaques web | jeudi matin | Web Attack - Brute Force / XSS / SQL Injection | secondaire |
| port scan | vendredi après-midi | PortScan | exploratoire |

Nom de fichiers possibles à vérifier localement après téléchargement :

```text
Monday-WorkingHours*.csv
Tuesday-WorkingHours*.csv
Thursday-WorkingHours*WebAttacks*.csv
Friday-WorkingHours*PortScan*.csv
```

Ces noms ne doivent pas être codés en dur avant vérification locale.

## Colonnes minimales à extraire

Colonnes nécessaires pour une première expérimentation :

| Besoin | Colonne CIC-IDS2017 probable | Usage |
|---|---|---|
| timestamp | `Timestamp` | reconstruire l'ordre des événements |
| IP source | `Source IP` ou équivalent | identifier l'origine |
| IP destination | `Destination IP` ou équivalent | identifier la cible |
| port source | `Source Port` ou équivalent | enrichissement |
| port destination | `Destination Port` ou équivalent | déduction protocole/service |
| protocole | `Protocol` | filtrage |
| durée de flux | `Flow Duration` | contexte |
| nombre paquets forward | `Total Fwd Packets` | contexte réseau |
| nombre paquets backward | `Total Backward Packets` | contexte réseau |
| label | `Label` | vérité terrain |

Colonnes optionnelles :

```text
Flow Bytes/s
Flow Packets/s
Fwd Packet Length Mean
Bwd Packet Length Mean
SYN Flag Count
ACK Flag Count
RST Flag Count
```

## Schéma interne cible

Le loader futur ne doit pas exposer directement toutes les colonnes CIC-IDS2017 au moteur.

Format interne minimal proposé :

```json
{
  "timestamp": "2017-07-04T14:00:00",
  "source_ip": "205.174.165.73",
  "destination_ip": "192.168.10.50",
  "source_port": 12345,
  "destination_port": 22,
  "protocol": "TCP",
  "raw_label": "SSH-Patator",
  "expected_alert_type": "SSH_BRUTE_FORCE",
  "dataset": "CIC-IDS2017",
  "source_file": "Tuesday-WorkingHours...csv"
}
```

Le champ `raw_label` doit conserver le label original.

Le champ `expected_alert_type` doit contenir le mapping interne ou `null` pour le trafic bénin.

## Mapping des labels

Mapping prioritaire :

| Label CIC-IDS2017 | Alerte interne | Décision |
|---|---|---|
| `BENIGN` | `null` | aucune alerte attendue |
| `SSH-Patator` / brute force SSH | `SSH_BRUTE_FORCE` | compatible |
| `FTP-Patator` / brute force FTP | hors périmètre immédiat | à ignorer au départ |
| `Web Attack - Brute Force` | `WEB_RECONNAISSANCE` ou futur `WEB_ATTACK` | à arbitrer |
| `Web Attack - XSS` | futur `WEB_ATTACK` | à exclure au départ |
| `Web Attack - Sql Injection` | futur `WEB_ATTACK` | à exclure au départ |
| `PortScan` | futur `SCAN_ACTIVITY` | exploratoire |
| `DoS*` | futur `DOS_ACTIVITY` | à exclure |
| `DDoS` | futur `DOS_ACTIVITY` | à exclure |
| `Bot` / Botnet | futur `BOTNET_ACTIVITY` | à exclure |
| `Infiltration` | futur `INFILTRATION_ACTIVITY` | à exclure |
| `Heartbleed` | futur `EXPLOIT_ATTEMPT` | à exclure |

## Règles de filtrage initiales

Pour un premier prototype loader :

```text
garder BENIGN
→ garder SSH-Patator / Brute Force SSH
→ exclure les autres labels
→ limiter le volume
→ conserver la source et le label brut
```

Critères d'exclusion :

```text
label inconnu
colonnes obligatoires absentes
lignes vides ou non parsables
volumes trop élevés pour les tests unitaires
scénarios non couverts par les alertes internes actuelles
```

## Stratégie de tests

Les tests ne doivent pas télécharger le dataset public.

Tests unitaires recommandés :

```text
utiliser 5 à 20 lignes synthétiques représentatives
vérifier le mapping BENIGN → null
vérifier le mapping SSH-Patator → SSH_BRUTE_FORCE
vérifier l'exclusion des labels hors périmètre
vérifier la conservation du raw_label
vérifier la présence du dataset et du source_file
```

Fichier de test futur possible :

```text
tests/test_cic_ids2017_mapping.py
```

## Artefacts futurs proposés

```text
utils/cic_ids2017_mapping.py
utils/public_dataset_loader.py
docs/PUBLIC_GROUND_TRUTH_LABELS.md
docs/PUBLIC_EXPERIMENT_RESULTS.md
tests/test_cic_ids2017_mapping.py
tests/test_public_dataset_loader.py
```

## Critères de succès

La future intégration minimale sera réussie si :

```text
aucune donnée brute n'est ajoutée au dépôt
le loader accepte un CSV local documenté
les labels originaux sont conservés
les labels internes sont générés explicitement
les résultats publics sont séparés des résultats simulés
les tests restent rapides
la documentation précise les limites
```

## Limites à assumer

Même avec ce mapping, le projet ne sera pas encore une solution SOC de production.

Limites persistantes :

```text
pas de SIEM réel
pas de flux temps réel
pas de validation analyste externe
pas de corrélation multi-sources avancée
pas de déploiement production
mapping partiel du dataset public
```

## Décision provisoire

Le premier mapping doit cibler uniquement :

```text
BENIGN
→ SSH_BRUTE_FORCE
```

Les scénarios web pourront être étudiés ensuite, mais ne doivent pas bloquer le premier loader.

## Prochaine étape proposée

Créer un module de mapping pur, sans téléchargement de dataset :

```text
utils/cic_ids2017_mapping.py
```

Ce module devra exposer une fonction simple :

```text
map_cic_ids2017_label(raw_label: str) -> str | None
```

Puis ajouter des tests unitaires indépendants du dataset complet.

## Conclusion

Ce plan rend l'intégration future plus sûre.

Il prépare :

```text
source publique
→ fichiers candidats
→ colonnes minimales
→ labels retenus
→ mapping explicite
→ tests légers
→ intégration progressive
```

Il évite de sur-vendre le projet et protège la reproductibilité en séparant clairement les logs simulés, la revue documentaire et les futures expérimentations publiques.

# Plan de mini-loader borné CIC-IDS2017

Ce document prépare l'étape suivante de l'intégration contrôlée de CIC-IDS2017.

L'objectif n'est pas d'intégrer le dataset complet, mais de définir un mini-loader borné, testable et honnête avant d'écrire le code correspondant.

## Objectif

Le mini-loader devra charger un nombre limité de lignes depuis un fichier CSV local déjà présent sur la machine de l'utilisateur.

```text
fichier CSV local
→ limite stricte de lignes
→ parsing ligne par ligne
→ sample row parser existant
→ événements normalisés
→ labels supportés ou hors périmètre
→ erreurs explicites
```

## Hors périmètre volontaire

Le mini-loader ne devra pas :

```text
télécharger CIC-IDS2017
ajouter le dataset brut au dépôt
charger tout le dataset en mémoire
promettre une évaluation SOC réelle
mesurer une performance scientifique complète
entraîner un modèle
remplacer le pipeline principal existant
lancer des actions de réponse incident
```

## Entrée attendue

Le mini-loader devra recevoir explicitement un chemin local vers un CSV.

Exemple futur envisagé :

```python
load_cic_ids2017_samples(
    csv_path="/chemin/local/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    max_rows=50,
)
```

Le chemin local ne devra pas être codé en dur dans le dépôt.

Le dépôt ne devra contenir aucun fichier brut CIC-IDS2017.

## Limite de lignes obligatoire

Le mini-loader devra imposer une limite de lignes.

```text
max_rows obligatoire
max_rows > 0
max_rows borné par une constante de sécurité
lecture arrêtée dès la limite atteinte
```

Une constante pourra être définie, par exemple :

```python
MAX_CIC_IDS2017_LOADER_ROWS = 1000
```

Cette limite évite :

```text
chargement accidentel du dataset complet
exécution lente en environnement de démonstration
surconsommation mémoire
survente d'une intégration dataset complète
```

## Colonnes minimales attendues

Le mini-loader devra s'appuyer sur le parser déjà existant :

```text
utils/cic_ids2017_sample_parser.py
```

Les colonnes minimales restent celles déjà supportées par le parser :

```text
Timestamp
Source IP / Src IP
Destination IP / Dst IP
Source Port / Src Port
Destination Port / Dst Port
Protocol
Label
```

Le loader ne doit pas dupliquer la logique de normalisation déjà présente dans le parser.

## Comportement attendu

Pour chaque ligne lue :

```text
lire la ligne CSV sous forme de dict
→ appeler parse_cic_ids2017_sample_row
→ récupérer un CicIds2017SampleEvent
→ conserver l'événement si la ligne est valide
→ produire une erreur claire si la ligne est invalide
```

Le comportement exact à choisir avant codage :

```text
mode strict : arrêter au premier événement invalide
mode tolérant : collecter les erreurs et continuer
```

Le premier code devra probablement commencer par un mode strict, plus simple à tester et plus honnête.

## Résultat attendu

La fonction pourra retourner une structure simple :

```python
@dataclass(frozen=True)
class CicIds2017MiniLoaderResult:
    events: tuple[CicIds2017SampleEvent, ...]
    rows_read: int
    supported_labels: int
    unsupported_labels: int
```

Cette structure devra rester descriptive.

Elle ne devra pas prétendre fournir des métriques SOC avancées.

## Tests à prévoir

Les tests devront utiliser uniquement des CSV temporaires générés pendant les tests.

Aucun fichier brut CIC-IDS2017 ne devra être ajouté au dépôt.

Cas minimaux à tester :

```text
charge une ligne SSH-Patator valide
charge une ligne BENIGN valide
respecte max_rows
rejette max_rows <= 0
rejette max_rows au-dessus de la limite autorisée
remonte une erreur claire si une colonne obligatoire manque
conserve les labels hors périmètre comme unsupported
ne télécharge aucune donnée
```

## Exemple de fichier de test autorisé

Un test pourra créer un fichier CSV temporaire comme ceci :

```text
Timestamp,Source IP,Destination IP,Source Port,Destination Port,Protocol,Label
2017-07-04 14:00:00,192.0.2.10,198.51.100.20,51515,22,6,SSH-Patator
2017-07-03 09:00:00,192.0.2.11,198.51.100.20,51516,443,TCP,BENIGN
```

Ce fichier est fictif, minimal et généré par le test.

Il ne correspond pas à un extrait brut du dataset public.

## Commandes de vérification prévues

Après implémentation future, les commandes minimales à exécuter seront :

```bash
pytest tests/test_cic_ids2017_mini_loader.py -q
pytest -q
black --check .
ruff check .
mypy .
bandit -r ai_assistant dashboard detection utils main.py -q
```

## Critères d'acceptation

Le futur mini-loader sera acceptable seulement si :

```text
aucune donnée brute CIC-IDS2017 n'est ajoutée au dépôt
le nombre de lignes est borné
les tests créent leurs propres CSV temporaires
le parser existant est réutilisé
les erreurs sont explicites
les labels hors périmètre restent identifiés comme tels
la documentation continue de préciser les limites
```

## Limites assumées

Même après ce mini-loader, le projet ne sera toujours pas un SOC de production.

Le mini-loader constituera seulement une étape vers :

```text
expérimentation contrôlée
→ reproductibilité locale
→ meilleure crédibilité recherche
→ future évaluation sur sous-ensemble public documenté
```

Il ne constituera pas :

```text
une validation sur CIC-IDS2017 complet
une preuve de performance IDS
une certification sécurité
une validation externe par analyste SOC
```

## Étape suivante

Une fois ce plan validé, l'étape suivante pourra être :

```text
v1.37.0 — CIC-IDS2017 bounded mini-loader
```

Cette future version devra ajouter le code minimal et ses tests sans ajouter de données brutes au dépôt.

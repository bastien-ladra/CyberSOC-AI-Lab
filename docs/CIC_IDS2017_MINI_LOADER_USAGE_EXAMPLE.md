# Exemple d'utilisation du mini-loader borné CIC-IDS2017

Ce document montre un exemple contrôlé d'utilisation du mini-loader borné CIC-IDS2017.

L'objectif est de rendre le fonctionnement compréhensible en entretien technique, sans intégrer le dataset public complet et sans versionner de données brutes CIC-IDS2017.

## Périmètre

```text
CSV local fourni explicitement
→ nombre de lignes borné par max_rows
→ parser existant réutilisé
→ labels supportés comptés
→ labels hors périmètre comptés
→ aucun téléchargement du dataset
→ aucun dataset brut ajouté au dépôt
→ aucune règle de détection lancée
```

## Exemple minimal

L'exemple ci-dessous crée un CSV temporaire fictif, puis appelle le mini-loader.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from utils.cic_ids2017_mini_loader import load_cic_ids2017_samples

CSV_HEADER = (
    "Timestamp,Source IP,Destination IP,Source Port,"
    "Destination Port,Protocol,Label\n"
)

CSV_ROWS = [
    "2017-07-04 14:00:00,205.174.165.73,192.168.10.50,12345,22,6,SSH-Patator",
    "2017-07-03 09:00:00,192.168.10.12,192.168.10.50,51515,443,TCP,BENIGN",
    "2017-07-04 15:00:00,205.174.165.73,192.168.10.50,12345,21,6,FTP-Patator",
]

with TemporaryDirectory() as temporary_directory:
    csv_path = Path(temporary_directory) / "local_cic_ids2017_sample.csv"
    csv_path.write_text(CSV_HEADER + "\n".join(CSV_ROWS) + "\n", encoding="utf-8")

    result = load_cic_ids2017_samples(csv_path=csv_path, max_rows=3)

    print(result.rows_read)
    print(result.supported_labels)
    print(result.unsupported_labels)
    print([event.raw_label for event in result.events])
```

## Résultat attendu

```text
3
2
1
['SSH-Patator', 'BENIGN', 'FTP-Patator']
```

Interprétation :

```text
SSH-Patator → label supporté, mappé vers SSH_BRUTE_FORCE
BENIGN      → label supporté, aucune alerte attendue
FTP-Patator → label hors périmètre actuel, aucune alerte attendue
```

## Pourquoi max_rows est obligatoire

Le mini-loader impose `max_rows` pour éviter de charger involontairement un fichier volumineux.

```text
max_rows <= 0      → erreur explicite
max_rows > 1000    → erreur explicite
fichier manquant   → erreur explicite
ligne invalide     → erreur avec numéro de ligne
```

## Ce que cet exemple ne fait pas

```text
ne télécharge pas CIC-IDS2017
ne lit pas le dataset complet
ne versionne aucune donnée publique brute
ne lance aucune règle de détection
ne mesure aucun score scientifique sur CIC-IDS2017
ne prouve pas une performance SOC réelle
```

## Commande de test liée

```bash
pytest tests/test_cic_ids2017_mini_loader.py -q
```

## Positionnement honnête

Cet exemple montre une brique d'intégration locale, contrôlée et testable.

Il ne transforme pas le projet en solution SOC de production et ne constitue pas encore une validation complète sur dataset public.

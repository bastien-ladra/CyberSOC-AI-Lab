# Exemple d'utilisation du sample row parser CIC-IDS2017

Ce document montre comment utiliser le parser minimal CIC-IDS2017 sur une seule ligne déjà fournie localement.

L'objectif est de démontrer l'usage du composant sans intégrer le dataset public complet et sans ajouter de données brutes au dépôt.

## Périmètre

Cet exemple utilise une ligne fictive construite à la main.

```text
ligne dict locale
→ parsing minimal
→ normalisation des colonnes
→ validation des ports
→ normalisation du protocole
→ mapping du label
→ événement normalisé
```

Cet exemple ne fait pas :

```text
pas de téléchargement de CIC-IDS2017
pas de lecture d'un CSV complet
pas de stockage de dataset brut
pas de détection réseau réelle
pas de mesure de performance sur dataset public
pas de validation SOC externe
```

## Exemple minimal

```python
from dataclasses import asdict

from utils.cic_ids2017_sample_parser import parse_cic_ids2017_sample_row

row = {
    "Timestamp": "2017-07-04 14:00:00",
    "Source IP": "192.0.2.10",
    "Destination IP": "198.51.100.20",
    "Source Port": "51515",
    "Destination Port": "22",
    "Protocol": "6",
    "Label": "SSH-Patator",
}

event = parse_cic_ids2017_sample_row(row)

print(asdict(event))
```

## Résultat attendu

```python
{
    "timestamp": "2017-07-04 14:00:00",
    "source_ip": "192.0.2.10",
    "destination_ip": "198.51.100.20",
    "source_port": 51515,
    "destination_port": 22,
    "protocol": "TCP",
    "raw_label": "SSH-Patator",
    "expected_alert_type": "SSH_BRUTE_FORCE",
    "is_supported_label": True,
}
```

## Lecture du résultat

Le parser transforme une ligne dict locale en événement normalisé minimal.

```text
Protocol = 6
→ TCP

Label = SSH-Patator
→ SSH_BRUTE_FORCE

Destination Port = 22
→ port valide
```

Le champ `expected_alert_type` indique l'alerte interne attendue après mapping du label.

Le champ `is_supported_label` indique si le label CIC-IDS2017 est dans le périmètre actuellement supporté.

## Exemple avec trafic bénin

```python
row = {
    "Timestamp": "2017-07-03 09:00:00",
    "Source IP": "192.0.2.10",
    "Destination IP": "198.51.100.20",
    "Source Port": "51515",
    "Destination Port": "443",
    "Protocol": "TCP",
    "Label": "BENIGN",
}

event = parse_cic_ids2017_sample_row(row)

assert event.expected_alert_type is None
assert event.is_supported_label is True
```

Dans ce cas, `BENIGN` est supporté mais ne produit aucune alerte attendue.

## Exemple avec label hors périmètre

```python
row = {
    "Timestamp": "2017-07-04 14:00:00",
    "Source IP": "192.0.2.10",
    "Destination IP": "198.51.100.20",
    "Source Port": "51515",
    "Destination Port": "21",
    "Protocol": "6",
    "Label": "FTP-Patator",
}

event = parse_cic_ids2017_sample_row(row)

assert event.expected_alert_type is None
assert event.is_supported_label is False
```

Ce comportement est volontaire : le parser conserve le label brut, mais ne prétend pas supporter les labels qui ne sont pas encore mappés.

## Vérification technique

Les tests dédiés sont disponibles ici :

```text
tests/test_cic_ids2017_sample_parser.py
```

Commande ciblée :

```bash
pytest tests/test_cic_ids2017_sample_parser.py -q
```

Commande complète du projet :

```bash
pytest -q
```

## Limite importante

Ce document est un exemple d'utilisation contrôlé.

Il ne prouve pas encore que le projet est capable d'ingérer CIC-IDS2017 complet, ni qu'il est prêt pour une validation SOC réelle.

Il prépare seulement l'étape suivante : passer d'une ligne locale contrôlée vers un mini-loader borné, documenté et testé.

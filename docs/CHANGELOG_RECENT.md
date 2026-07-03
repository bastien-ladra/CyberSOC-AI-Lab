# Changelog récent — CyberSOC-AI-Lab

Ce document aligne les dernières versions documentaires après `v1.38.0`.

Il sert de complément récent au `CHANGELOG.md` principal pour éviter une réécriture risquée de tout l'historique long du projet.

## v1.40.1 — recent changelog alignment

### Ajouté

- Ajout de `docs/CHANGELOG_RECENT.md`.
- Ajout d'un récapitulatif récent pour `v1.39.0`, `v1.39.1` et `v1.40.0`.
- Alignement documentaire de l'historique récent sans modification du code.
- Conservation des estimations actuelles.

### Estimation

- Avancement global : 99 %
- Note portfolio : 100 / 100
- Note recherche appliquée : 98 / 100
- Note production : 25 / 100

### Objectif

Garder un historique lisible des dernières versions sans prendre le risque d'écraser le changelog principal complet.

```text
v1.39.0
→ v1.39.1
→ v1.40.0
→ historique récent aligné
→ pas de modification code
```

---

## v1.40.0 — CIC-IDS2017 mini-loader usage example

### Ajouté

- Ajout de `docs/CIC_IDS2017_MINI_LOADER_USAGE_EXAMPLE.md`.
- Ajout d'un exemple contrôlé d'utilisation du mini-loader borné CIC-IDS2017.
- Utilisation d'un CSV temporaire fictif.
- Démonstration de `max_rows=3`.
- Démonstration des labels `SSH-Patator`, `BENIGN` et `FTP-Patator`.
- Clarification que l'exemple ne télécharge pas CIC-IDS2017.
- Clarification qu'aucun dataset brut n'est versionné.
- Clarification qu'aucune règle de détection n'est lancée.
- Mise à jour du README.
- Mise à jour de l'index documentaire.

### Estimation

- Avancement global : 99 %
- Note portfolio : 100 / 100
- Note recherche appliquée : 98 / 100
- Note production : 25 / 100

### Objectif

Rendre le mini-loader compréhensible en entretien technique tout en gardant un périmètre honnête.

```text
mini-loader existant
→ exemple temporaire fictif
→ usage compréhensible
→ limites explicites
→ aucun dataset brut
```

---

## v1.39.1 — Bandit local confirmation

### Modifié

- Confirmation locale de la commande Bandit dédiée.
- Mise à jour de `docs/QUALITY_GATES_REFRESH.md`.
- Mise à jour du README pour indiquer `Black`, `Ruff`, `mypy`, `Bandit` et `pytest` comme contrôles locaux OK.
- Aucune modification du code.
- Aucune modification des tests.

### Estimation

- Avancement global : 99 %
- Note portfolio : 100 / 100
- Note recherche appliquée : 98 / 100
- Note production : 25 / 100

### Objectif

Retirer le dernier point de prudence local lié à Bandit non confirmé dans la capture précédente.

```text
quality gates locaux
→ Bandit confirmé
→ documentation qualité alignée
→ verrouillage propre
```

---

## v1.39.0 — quality gates refresh

### Modifié

- Mise à jour du README avec les résultats qualité locaux actualisés.
- Ajout de `docs/QUALITY_GATES_REFRESH.md`.
- Documentation de `83 passed`.
- Documentation de la couverture `95.99 %`.
- Documentation de `Black`, `Ruff`, `mypy` et `pytest` comme OK.
- Conservation du point de prudence initial concernant Bandit local, ensuite levé en `v1.39.1`.
- Aucune modification du code.
- Aucune modification des tests.

### Estimation

- Avancement global : 99 %
- Note portfolio : 100 / 100
- Note recherche appliquée : 98 / 100
- Note production : 25 / 100

### Objectif

Rafraîchir les chiffres qualité visibles après les ajouts CIC-IDS2017 récents.

```text
anciens chiffres README
→ quality gates relancés
→ 83 tests passés
→ couverture 95.99 %
→ documentation alignée
```

# Reproductibilité

Ce document décrit comment reproduire les contrôles techniques et expérimentaux du projet CyberSOC-AI-Lab.

L'objectif est de permettre à une autre personne de relancer les vérifications principales sans dépendre d'une interprétation informelle du projet.

## Principe

Un résultat est considéré comme reproductible lorsqu'une personne peut :

```text
cloner le dépôt
installer les dépendances
relancer les quality gates
exécuter les tests
vérifier automatiquement la vérité terrain
relire le protocole expérimental
appliquer la matrice d'évaluation
renseigner le rapport de résultats
```

## Version de référence

Avant toute reproduction, relever la version courante indiquée dans le README et le CHANGELOG.

```text
README.md
CHANGELOG.md
```

La version testée doit correspondre au tag Git utilisé.

## Installation

Créer un environnement Python isolé :

```bash
python -m venv .venv
```

Activer l'environnement.

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Sous Linux ou macOS :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Contrôles techniques à reproduire

Les contrôles suivants doivent être relancés :

```bash
black --check .
ruff check .
mypy .
bandit -r ai_assistant dashboard detection utils main.py -q
pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q
```

## Résultats techniques attendus

| Contrôle | Attendu |
|---|---|
| Black | Aucun fichier à reformater |
| Ruff | Aucun problème bloquant |
| mypy | Aucun problème de typage |
| Bandit | Aucun problème critique remonté dans le périmètre scanné |
| pytest | Tests passants |
| coverage | Couverture supérieure ou égale au seuil CI |
| Ground truth evaluator | Labels attendus et alertes observées cohérents sur les logs simulés versionnés |

## Vérification automatique de la vérité terrain

La vérité terrain est documentée dans :

```text
docs/GROUND_TRUTH_LABELS.md
```

Elle est vérifiée automatiquement par :

```text
utils/ground_truth_evaluator.py
tests/test_ground_truth_evaluator.py
```

Cette vérification compare :

```text
labels attendus
→ alertes observées
→ labels manquants
→ labels inattendus
→ résultat passant ou échoué
```

La commande `pytest` du bloc de quality gates exécute aussi ces tests.

## Reproduction expérimentale

Les documents suivants doivent être lus dans cet ordre :

```text
docs/DATASET_CARD.md
docs/GROUND_TRUTH_LABELS.md
docs/EXPERIMENT_PROTOCOL.md
docs/EVALUATION_MATRIX.md
docs/EXPERIMENT_RESULTS.md
```

Ordre de reproduction :

1. Identifier le scénario à évaluer.
2. Relire les labels attendus dans `docs/GROUND_TRUTH_LABELS.md`.
3. Relancer le pipeline sur les logs simulés.
4. Vérifier les alertes générées.
5. Relancer les tests de vérité terrain automatique.
6. Vérifier les preuves conservées.
7. Vérifier le prompt IA généré.
8. Vérifier ou simuler la réponse IA.
9. Appliquer la matrice d'évaluation.
10. Renseigner le rapport de résultats expérimentaux.

## Artefacts à vérifier

Selon le scénario et l'exécution locale, vérifier les dossiers suivants :

```text
runtime/alerts/
runtime/reports/
runtime/prompts/
runtime/ai_outputs/
runtime/audit/
runtime/human_reviews/
```

En l'absence de sortie runtime, le dashboard peut utiliser les exemples versionnés :

```text
examples/alerts/
examples/reports/
examples/prompts/
examples/ai_outputs/
examples/audit/
examples/human_reviews/
```

## Critères de reproduction acceptée

La reproduction est considérée comme acceptable si :

```text
les quality gates passent
les tests passent
le seuil de couverture est respecté
l'évaluateur automatique de vérité terrain passe
les scénarios documentés produisent les alertes attendues
les scénarios bénins ne produisent pas d'alerte critique injustifiée
les prompts IA rappellent les limites et la validation humaine
les décisions humaines restent traçables
les limites expérimentales sont conservées dans le rapport
```

## Ce qui n'est pas encore garanti

```text
reproductibilité sur données SOC réelles
reproductibilité avec tous les modèles IA locaux
stabilité parfaite des réponses génératives
performance en environnement de production
validation par un analyste SOC externe
validation académique externe
```

Ces limites sont assumées et doivent rester visibles dans la documentation.

## Intérêt pour l'évaluation du projet

Ce document renforce la crédibilité du projet car il permet de passer de :

```text
le projet fonctionne chez l'auteur
```

à :

```text
le projet peut être relancé, contrôlé et discuté par une autre personne
```

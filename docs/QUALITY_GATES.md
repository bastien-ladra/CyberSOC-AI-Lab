# Quality gates

Ce document décrit les contrôles qualité utilisés pour renforcer la fiabilité du projet.

## Objectif

L'objectif est de rendre le projet plus difficile à casser et plus facile à auditer.

Les contrôles ne prouvent pas qu'un projet est parfait, mais ils réduisent fortement le risque de régression, d'erreur évidente ou de dette technique non détectée.

## Contrôles locaux

Avant de publier une version, les commandes suivantes doivent passer :

```bash
black --check .
ruff check .
mypy .
bandit -r ai_assistant dashboard detection utils main.py -q
pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q
```

## Contrôles CI

La pipeline GitHub Actions exécute les mêmes contrôles automatiquement :

```text
formatage Black
→ lint Ruff
→ typage statique mypy
→ scan sécurité Bandit
→ tests pytest avec couverture
```

## Couverture de tests

Le seuil minimal de couverture est fixé à 90 % pour les modules cœur :

```text
ai_assistant/
detection/
utils/
```

Le dashboard Streamlit n'est pas encore inclus dans le seuil de couverture, car il nécessite une stratégie de test UI ou de test smoke dédiée.

## Limite assumée

Ces quality gates améliorent la qualité du projet, mais ne remplacent pas :

- une revue humaine du code ;
- des tests sur données réelles ;
- une analyse de sécurité complète ;
- une validation scientifique expérimentale.

Ils constituent cependant une base de qualité technique beaucoup plus solide qu'une simple exécution manuelle des tests.

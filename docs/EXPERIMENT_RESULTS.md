# Résultats expérimentaux

Ce document sert à consigner les résultats obtenus en appliquant le protocole expérimental et la matrice d'évaluation.

Il ne remplace pas les tests automatisés. Il complète les tests en documentant les observations, les limites et l'interprétation des résultats.

## Références internes

Ce rapport s'appuie sur :

```text
docs/EXPERIMENT_PROTOCOL.md
docs/EVALUATION_MATRIX.md
docs/evaluation.md
docs/QUALITY_GATES.md
```

## Synthèse exécutive

| Élément | Statut attendu | Observation |
|---|---|---|
| Quality gates | Tous verts | À renseigner à chaque version |
| Couverture de tests | Supérieure ou égale au seuil CI | À renseigner à chaque version |
| Scénarios malveillants | Détectés | À renseigner |
| Scénarios bénins | Pas d'alerte critique injustifiée | À renseigner |
| Prompt injection | Détectée et neutralisée | À renseigner |
| Validation humaine | Présente | À renseigner |
| Traçabilité | Artefacts produits | À renseigner |

## Résultats par scénario

### SSH_BRUTE_FORCE

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Détection | À renseigner | À renseigner |
| Criticité | À renseigner | À renseigner |
| Preuves | À renseigner | À renseigner |
| Comptes ciblés | À renseigner | À renseigner |
| Recommandations | À renseigner | À renseigner |
| Validation humaine | À renseigner | À renseigner |

### WEB_RECONNAISSANCE

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Détection | À renseigner | À renseigner |
| Criticité | À renseigner | À renseigner |
| Preuves | À renseigner | À renseigner |
| Faux positifs | À renseigner | À renseigner |
| Recommandations | À renseigner | À renseigner |
| Validation humaine | À renseigner | À renseigner |

### PROMPT_INJECTION_ATTEMPT

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Détection | À renseigner | À renseigner |
| Motifs suspects | À renseigner | À renseigner |
| Preuves | À renseigner | À renseigner |
| Prompt IA sécurisé | À renseigner | À renseigner |
| Réponse IA prudente | À renseigner | À renseigner |
| Validation humaine | À renseigner | À renseigner |

## Résultats techniques

| Contrôle | Commande | Résultat |
|---|---|---|
| Formatage | `black --check .` | À renseigner |
| Lint | `ruff check .` | À renseigner |
| Typage | `mypy .` | À renseigner |
| Sécurité statique | `bandit -r ai_assistant dashboard detection utils main.py -q` | À renseigner |
| Tests et couverture | `pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q` | À renseigner |

## Analyse des résultats

À compléter après exécution des scénarios.

Points à analyser :

```text
écarts entre résultats attendus et observés
faux positifs éventuels
faux négatifs éventuels
faiblesses de la réponse IA
qualité de la traçabilité
qualité de la supervision humaine
```

## Limites observées

À compléter après expérimentation.

Exemples de limites possibles :

```text
jeu de données trop petit
logs simulés uniquement
absence de données SOC réelles
absence de comparaison multi-modèles
absence de mesure de temps de traitement
absence d'étude utilisateur avec analystes SOC
```

## Conclusion expérimentale

À compléter après analyse.

La conclusion doit rester prudente :

```text
ce qui est validé
ce qui est partiellement validé
ce qui reste non démontré
ce qui doit être amélioré
```

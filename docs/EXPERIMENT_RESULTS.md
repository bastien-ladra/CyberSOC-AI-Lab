# Résultats expérimentaux

Ce document sert à consigner les résultats obtenus en appliquant le protocole expérimental et la matrice d'évaluation.

Il ne remplace pas les tests automatisés. Il complète les tests en documentant les observations, les limites et l'interprétation des résultats.

## Références internes

Ce rapport s'appuie sur :

```text
docs/DATASET_CARD.md
docs/GROUND_TRUTH_LABELS.md
docs/EXPERIMENT_PROTOCOL.md
docs/EVALUATION_MATRIX.md
docs/evaluation.md
docs/QUALITY_GATES.md
docs/REPRODUCIBILITY.md
utils/ground_truth_evaluator.py
utils/ground_truth_results_exporter.py
```

## Artefacts de résultats

Les résultats de vérité terrain peuvent être exportés dans :

```text
runtime/evaluation/ground_truth_results.json
runtime/evaluation/ground_truth_results.md
```

Ces artefacts doivent être utilisés pour renseigner les résultats observés :

```text
labels attendus
→ alertes observées
→ labels manquants
→ labels inattendus
→ statut global
→ résultat auditable
```

## Synthèse exécutive

| Élément | Statut attendu | Observation |
|---|---|---|
| Quality gates | Tous verts | À renseigner à chaque version |
| Couverture de tests | Supérieure ou égale au seuil CI | À renseigner à chaque version |
| Vérification vérité terrain | Passante | À renseigner depuis `tests/test_ground_truth_evaluator.py` |
| Export résultats JSON | Généré | À renseigner depuis `runtime/evaluation/ground_truth_results.json` |
| Export résultats Markdown | Généré | À renseigner depuis `runtime/evaluation/ground_truth_results.md` |
| Scénarios malveillants | Détectés | À renseigner |
| Scénarios bénins | Pas d'alerte critique injustifiée | À renseigner |
| Prompt injection | Détectée et neutralisée | À renseigner |
| Validation humaine | Présente | À renseigner |
| Traçabilité | Artefacts produits | À renseigner |

## Résultats de vérité terrain exportés

| Fichier | Labels attendus | Labels observés | Manquants | Inattendus | Résultat |
|---|---|---|---|---|---|
| `ssh_auth.log` | À renseigner | À renseigner | À renseigner | À renseigner | À renseigner |
| `web_access.log` | À renseigner | À renseigner | À renseigner | À renseigner | À renseigner |
| `benign_ssh_auth.log` | À renseigner | À renseigner | À renseigner | À renseigner | À renseigner |
| `benign_web_access.log` | À renseigner | À renseigner | À renseigner | À renseigner | À renseigner |

Ce tableau doit être rempli à partir des artefacts générés par `utils/ground_truth_results_exporter.py`.

## Résultats par scénario

### SSH_BRUTE_FORCE

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Vérité terrain | À renseigner | À renseigner |
| Vérification automatique | À renseigner | À renseigner |
| Export des résultats | À renseigner | À renseigner |
| Détection | À renseigner | À renseigner |
| Criticité | À renseigner | À renseigner |
| Preuves | À renseigner | À renseigner |
| Comptes ciblés | À renseigner | À renseigner |
| Recommandations | À renseigner | À renseigner |
| Validation humaine | À renseigner | À renseigner |

### WEB_RECONNAISSANCE

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Vérité terrain | À renseigner | À renseigner |
| Vérification automatique | À renseigner | À renseigner |
| Export des résultats | À renseigner | À renseigner |
| Détection | À renseigner | À renseigner |
| Criticité | À renseigner | À renseigner |
| Preuves | À renseigner | À renseigner |
| Faux positifs | À renseigner | À renseigner |
| Recommandations | À renseigner | À renseigner |
| Validation humaine | À renseigner | À renseigner |

### PROMPT_INJECTION_ATTEMPT

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Vérité terrain | À renseigner | À renseigner |
| Vérification automatique | À renseigner | À renseigner |
| Export des résultats | À renseigner | À renseigner |
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
| Export résultats | `utils/ground_truth_results_exporter.py` | À renseigner |

## Analyse des résultats

À compléter après exécution des scénarios.

Points à analyser :

```text
écarts entre résultats attendus et observés
labels manquants éventuels
labels inattendus éventuels
faux positifs éventuels
faux négatifs éventuels
faiblesses de la réponse IA
qualité de la traçabilité
qualité de la supervision humaine
lisibilité des artefacts JSON et Markdown
```

## Limites observées

À compléter après expérimentation.

Exemples de limites possibles :

```text
jeu de données trop petit
logs simulés uniquement
résultats exportés limités au périmètre versionné
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

# Résultats expérimentaux

Ce document consigne les résultats obtenus en appliquant le protocole expérimental et la matrice d'évaluation sur le périmètre simulé de CyberSOC-AI-Lab.

Il ne remplace pas les tests automatisés. Il complète les tests en documentant les observations, les limites et l'interprétation des résultats.

## Version évaluée

```text
version : v1.25.1 — Evaluation documentation alignment
périmètre : logs simulés versionnés
statut : expérimentation contrôlée
production : non
validation externe SOC : non
```

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

Ces artefacts servent à vérifier :

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
| Quality gates | Tous verts | OK sur la dernière exécution locale connue. |
| Couverture de tests | Supérieure ou égale au seuil CI | OK — 94.94 %. |
| Vérification vérité terrain | Passante | OK — les 4 cas de logs simulés sont couverts par les tests. |
| Export résultats JSON | Généré par l'exporter | OK — la génération JSON est couverte par test automatisé. |
| Export résultats Markdown | Généré par l'exporter | OK — la génération Markdown est couverte par test automatisé. |
| Scénarios malveillants | Détectés | OK sur les scénarios simulés versionnés. |
| Scénarios bénins | Pas d'alerte critique injustifiée | OK sur les scénarios bénins versionnés. |
| Prompt injection | Détectée et neutralisée au niveau détection/prompt | OK sur le scénario simulé. |
| Validation humaine | Présente dans le design | OK — mécanisme présent, pas encore validation externe SOC. |
| Traçabilité | Artefacts produits ou exportables | OK sur le périmètre du prototype. |

## Résultats de vérité terrain exportés

| Fichier | Labels attendus | Labels observés | Manquants | Inattendus | Résultat |
|---|---|---|---|---|---|
| `ssh_auth.log` | `SSH_BRUTE_FORCE` | `SSH_BRUTE_FORCE` | Aucun | Aucun | OK |
| `web_access.log` | `WEB_RECONNAISSANCE`, `PROMPT_INJECTION_ATTEMPT` | `WEB_RECONNAISSANCE`, `PROMPT_INJECTION_ATTEMPT` | Aucun | Aucun | OK |
| `benign_ssh_auth.log` | Aucun | Aucun | Aucun | Aucun | OK |
| `benign_web_access.log` | Aucun | Aucun | Aucun | Aucun | OK |

Ces résultats sont limités aux logs simulés versionnés et ne doivent pas être généralisés à des logs SOC réels.

## Résultats par scénario

### SSH_BRUTE_FORCE

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Vérité terrain | 5 | Le label attendu est explicite dans `docs/GROUND_TRUTH_LABELS.md`. |
| Vérification automatique | 5 | Le cas est couvert par l'évaluateur automatique de vérité terrain. |
| Export des résultats | 5 | Le résultat est exportable en JSON et Markdown. |
| Détection | 5 | Le scénario de brute force SSH est détecté sur les logs simulés. |
| Criticité | 5 | La criticité attendue est élevée sur le scénario suspect. |
| Preuves | 5 | Les échecs SSH répétés servent de preuves observables. |
| Comptes ciblés | 4 | Les comptes ciblés sont identifiables depuis les lignes de logs simulées. |
| Recommandations | 4 | Les recommandations restent orientées analyste et non automatiques. |
| Validation humaine | 5 | Le design impose une validation humaine. |

### WEB_RECONNAISSANCE

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Vérité terrain | 5 | Le label attendu est explicite dans `docs/GROUND_TRUTH_LABELS.md`. |
| Vérification automatique | 5 | Le cas est couvert par l'évaluateur automatique de vérité terrain. |
| Export des résultats | 5 | Le résultat est exportable en JSON et Markdown. |
| Détection | 5 | Le scénario de reconnaissance web est détecté sur les chemins suspects simulés. |
| Criticité | 5 | La criticité reste proportionnée au scénario. |
| Preuves | 5 | Les chemins web suspects sont conservés comme preuves. |
| Faux positifs | 5 | Le scénario web bénin ne produit pas de reconnaissance web attendue. |
| Recommandations | 4 | Les recommandations restent prudentes et nécessitent corrélation. |
| Validation humaine | 5 | Le design impose une validation humaine. |

### PROMPT_INJECTION_ATTEMPT

| Critère | Score 0-5 | Observation |
|---|---:|---|
| Vérité terrain | 5 | Le label attendu est explicite dans `docs/GROUND_TRUTH_LABELS.md`. |
| Vérification automatique | 5 | Le cas est couvert par l'évaluateur automatique de vérité terrain. |
| Export des résultats | 5 | Le résultat est exportable en JSON et Markdown. |
| Détection | 5 | La tentative de prompt injection simulée est détectée dans les logs web. |
| Motifs suspects | 5 | Les motifs de type `ignore_previous_instructions` et `reveal_system_prompt` sont identifiables. |
| Preuves | 5 | Le contenu hostile est conservé comme preuve, pas comme instruction. |
| Prompt IA sécurisé | 5 | Le projet traite les logs comme des données non fiables. |
| Réponse IA prudente | 4 | Les garde-fous sont documentés et testés, mais aucune validation multi-modèles n'est encore réalisée. |
| Validation humaine | 5 | Le design impose une validation humaine. |

## Résultats techniques

| Contrôle | Commande | Résultat |
|---|---|---|
| Formatage | `black --check .` | OK |
| Lint | `ruff check .` | OK |
| Typage | `mypy .` | OK |
| Sécurité statique | `bandit -r ai_assistant dashboard detection utils main.py -q` | OK |
| Tests et couverture | `pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q` | OK — 60 passed, 94.94 % coverage |
| Export résultats | `utils/ground_truth_results_exporter.py` | OK — JSON et Markdown couverts par tests |

## Analyse des résultats

Les résultats montrent que le pipeline est cohérent sur son périmètre simulé :

```text
les labels attendus sont explicites
les alertes observées correspondent aux labels attendus
les cas bénins ne déclenchent pas les alertes suspectes attendues absentes
les résultats sont exportables en JSON et Markdown
les quality gates restent verts
```

L'intérêt principal est la traçabilité : le projet ne repose plus seulement sur une démonstration manuelle, mais sur une chaîne documentaire et testée.

```text
dataset
→ vérité terrain
→ évaluation automatique
→ export de résultats
→ rapport expérimental
```

## Limites observées

Les limites restent importantes :

```text
jeu de données très petit
logs simulés uniquement
résultats exportés limités au périmètre versionné
absence de données SOC réelles
absence de comparaison multi-modèles
absence de mesure de temps de traitement
absence d'étude utilisateur avec analystes SOC
absence de validation externe par analyste SOC
```

Ces limites ne remettent pas en cause la cohérence du prototype. Elles empêchent simplement de conclure à une performance en production.

## Conclusion expérimentale

Sur les scénarios simulés versionnés, le projet valide :

```text
la détection des comportements attendus
l'absence d'alertes attendues sur les scénarios bénins
la comparaison automatique labels attendus / alertes observées
l'export des résultats d'évaluation
la traçabilité documentaire et technique
```

Le projet ne démontre pas encore :

```text
une performance sur logs SOC réels
une robustesse multi-environnements
une stabilité multi-modèles IA
une réduction mesurée des faux positifs en production
une validation par analystes SOC externes
```

Conclusion prudente : CyberSOC-AI-Lab est un prototype expérimental cohérent, testé et auditable sur un périmètre simulé limité. Il constitue une base solide pour portfolio, entretien technique et recherche appliquée, mais pas une solution SOC de production.

# Index documentaire du projet

Ce document sert de carte de navigation pour CyberSOC-AI-Lab.

Le point d'entrée principal après nettoyage documentaire est :

```text
docs/PROJECT_STATUS.md
```

Le statut des documents et le tri de lecture sont ici :

```text
docs/DOCUMENTATION_STATUS.md
```

## Lecture rapide

| Besoin | Document |
|---|---|
| Comprendre l'état réel du projet | `docs/PROJECT_STATUS.md` |
| Savoir quels documents sont actifs ou secondaires | `docs/DOCUMENTATION_STATUS.md` |
| Présenter le projet à un recruteur | `docs/RECRUITER_QUICK_DEMO.md` |
| Faire une démonstration complète | `docs/DEMO_GUIDE.md` |
| Lire l'étude de cas | `docs/CASE_STUDY.md` |
| Comprendre le modèle de sécurité | `docs/SECURITY_MODEL.md` |
| Comprendre les menaces IA/SOC | `docs/threat_model.md` |
| Comprendre les données utilisées | `docs/DATASET_CARD.md` |
| Comprendre la vérité terrain | `docs/GROUND_TRUTH_LABELS.md` |
| Reproduire les contrôles qualité | `docs/QUALITY_GATES.md` |
| Lire les résultats qualité récents | `docs/QUALITY_GATES_REFRESH.md` |
| Lire l'historique récent | `docs/CHANGELOG_RECENT.md` |
| Lire l'historique long | `CHANGELOG.md` |

## Chaîne de crédibilité actuelle

CyberSOC-AI-Lab est organisé autour de la chaîne suivante :

```text
prototype technique
→ tests automatisés
→ quality gates
→ sécurité documentée
→ threat model
→ dataset simulé documenté
→ vérité terrain explicitée
→ vérité terrain vérifiée automatiquement
→ résultats exportés
→ protocole expérimental
→ reproductibilité
→ CIC-IDS2017 traité progressivement
→ limites assumées
→ point projet consolidé
→ statut documentaire clarifié
```

## Documents principaux

| Document | Statut | Rôle |
|---|---|---|
| `README.md` | actif | Présentation synthétique du projet, commandes et liens principaux. |
| `docs/PROJECT_STATUS.md` | actif | Point concret : objectif, avancement, limites, décision de continuer ou non. |
| `docs/DOCUMENTATION_STATUS.md` | actif | Tri documentaire : actifs, secondaires, historiques et non prioritaires. |
| `docs/PROJECT_INDEX.md` | actif | Carte de navigation documentaire. |
| `docs/CHANGELOG_RECENT.md` | actif | Historique récent aligné des versions postérieures à `v1.38.0`. |
| `CHANGELOG.md` | historique long | Historique versionné long du projet. |
| `docs/architecture.md` | actif | Architecture du prototype et flux de traitement. |
| `docs/SECURITY_MODEL.md` | actif | Modèle de sécurité, garanties recherchées et limites du prototype. |
| `docs/threat_model.md` | actif | Menaces identifiées autour de l'IA appliquée au SOC. |
| `docs/DATASET_CARD.md` | actif | Description des jeux de logs simulés, de leurs usages et de leurs limites. |
| `docs/GROUND_TRUTH_LABELS.md` | actif | Labels attendus et critères de comparaison pour les logs simulés. |
| `docs/QUALITY_GATES.md` | actif | Contrôles qualité à exécuter avant validation d'une version. |
| `docs/QUALITY_GATES_REFRESH.md` | actif | Rafraîchissement local des résultats qualité documentés. |
| `docs/EXPERIMENT_PROTOCOL.md` | actif | Protocole expérimental. |
| `docs/EVALUATION_MATRIX.md` | actif | Grille d'évaluation des scénarios et des réponses IA. |
| `docs/EXPERIMENT_RESULTS.md` | actif | Rapport de résultats expérimentaux. |
| `docs/REPRODUCIBILITY.md` | actif | Procédure de reproductibilité. |
| `docs/CASE_STUDY.md` | actif | Étude de cas complète. |
| `docs/DEMO_GUIDE.md` | actif | Guide de démonstration. |
| `docs/RECRUITER_QUICK_DEMO.md` | actif | Démonstration courte orientée recruteur. |
| `docs/RESEARCH_PROPOSAL.md` | actif | Cadrage doctoral provisoire. |
| `docs/research_notes.md` | notes historiques nettoyées | Notes de recherche, non source de vérité sur l'état actuel. |
| `docs/evaluation.md` | complément historique | Ancienne méthodologie générale, conservée mais non prioritaire. |

## Documentation CIC-IDS2017

| Document | Statut | Rôle |
|---|---|---|
| `docs/PUBLIC_DATASET_ROADMAP.md` | actif | Roadmap vers un dataset public documenté. |
| `docs/PUBLIC_DATASET_CANDIDATES.md` | actif | Liste de datasets publics candidats. |
| `docs/CIC_IDS2017_DATASET_REVIEW.md` | actif | Revue du dataset CIC-IDS2017, sans intégration complète. |
| `docs/CIC_IDS2017_MAPPING_PLAN.md` | actif | Plan de mapping entre labels CIC-IDS2017 et alertes internes. |
| `docs/CIC_IDS2017_SAMPLE_PARSER_EXAMPLE.md` | actif | Exemple contrôlé du sample row parser. |
| `docs/CIC_IDS2017_BOUNDED_MINI_LOADER_PLAN.md` | actif | Plan du mini-loader borné. |
| `docs/CIC_IDS2017_MINI_LOADER_USAGE_EXAMPLE.md` | actif | Exemple contrôlé du mini-loader avec CSV temporaire fictif. |

## Artefacts techniques principaux

| Artefact | Rôle |
|---|---|
| `utils/ground_truth_evaluator.py` | Compare les alertes observées aux labels attendus. |
| `tests/test_ground_truth_evaluator.py` | Vérifie l'évaluation de vérité terrain. |
| `utils/ground_truth_results_exporter.py` | Génère les résultats de vérité terrain en JSON et Markdown. |
| `tests/test_ground_truth_results_exporter.py` | Vérifie l'export des résultats. |
| `utils/cic_ids2017_mapping.py` | Mappe un sous-ensemble de labels CIC-IDS2017. |
| `tests/test_cic_ids2017_mapping.py` | Vérifie le mapper CIC-IDS2017. |
| `utils/cic_ids2017_sample_parser.py` | Parse une ligne locale CIC-IDS2017-like. |
| `tests/test_cic_ids2017_sample_parser.py` | Vérifie le sample row parser. |
| `utils/cic_ids2017_mini_loader.py` | Charge un nombre borné de lignes depuis un CSV local. |
| `tests/test_cic_ids2017_mini_loader.py` | Vérifie le mini-loader borné. |

## Lecture recommandée selon le profil

### Recruteur technique

```text
README.md
→ docs/PROJECT_STATUS.md
→ docs/DOCUMENTATION_STATUS.md
→ docs/RECRUITER_QUICK_DEMO.md
→ docs/DEMO_GUIDE.md
→ docs/CASE_STUDY.md
→ docs/QUALITY_GATES_REFRESH.md
```

### Évaluateur cybersécurité

```text
README.md
→ docs/PROJECT_STATUS.md
→ docs/DOCUMENTATION_STATUS.md
→ docs/SECURITY_MODEL.md
→ docs/threat_model.md
→ docs/DATASET_CARD.md
→ docs/GROUND_TRUTH_LABELS.md
→ docs/CIC_IDS2017_MINI_LOADER_USAGE_EXAMPLE.md
→ docs/QUALITY_GATES_REFRESH.md
```

### Encadrant académique ou doctoral

```text
README.md
→ docs/PROJECT_STATUS.md
→ docs/DOCUMENTATION_STATUS.md
→ docs/RESEARCH_PROPOSAL.md
→ docs/PUBLIC_DATASET_ROADMAP.md
→ docs/PUBLIC_DATASET_CANDIDATES.md
→ docs/CIC_IDS2017_DATASET_REVIEW.md
→ docs/EXPERIMENT_PROTOCOL.md
→ docs/EVALUATION_MATRIX.md
→ docs/EXPERIMENT_RESULTS.md
```

### Contributeur technique

```text
README.md
→ docs/PROJECT_STATUS.md
→ docs/DOCUMENTATION_STATUS.md
→ docs/architecture.md
→ docs/REPRODUCIBILITY.md
→ docs/QUALITY_GATES.md
→ docs/QUALITY_GATES_REFRESH.md
→ tests/
→ utils/
```

## Ce qui n'est plus prioritaire

Ces documents sont conservés mais ne doivent pas être utilisés comme première source pour l'état actuel :

```text
docs/evaluation.md
docs/research_notes.md
CHANGELOG.md
```

Sources prioritaires à utiliser à la place :

```text
docs/PROJECT_STATUS.md
docs/DOCUMENTATION_STATUS.md
docs/EXPERIMENT_PROTOCOL.md
docs/EVALUATION_MATRIX.md
docs/CHANGELOG_RECENT.md
```

## Ce que cet index ne remplace pas

Cet index ne remplace pas :

```text
le README
les tests
les quality gates
la documentation détaillée
la reproduction des résultats
la validation humaine
```

Il sert uniquement de carte de navigation.

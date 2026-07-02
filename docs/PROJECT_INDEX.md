# Index documentaire du projet

Ce document sert de point d'entrée rapide vers les documents importants de CyberSOC-AI-Lab.

Il évite de dépendre uniquement du README lorsque le projet grandit et permet à un recruteur, un évaluateur technique ou un futur encadrant académique de comprendre rapidement où trouver chaque information.

## Vue d'ensemble

CyberSOC-AI-Lab est organisé autour de plusieurs axes :

```text
prototype technique
→ sécurité IA
→ validation humaine
→ qualité logicielle
→ données documentées
→ vérité terrain explicitée
→ évaluation expérimentale
→ reproductibilité
→ positionnement recherche
```

## Documents principaux

| Document | Rôle |
|---|---|
| `README.md` | Présentation générale du projet, installation, utilisation et positionnement. |
| `CHANGELOG.md` | Historique versionné des évolutions du projet. |
| `docs/PROJECT_INDEX.md` | Carte de navigation documentaire du projet. |
| `docs/architecture.md` | Architecture du prototype et flux de traitement. |
| `docs/threat_model.md` | Menaces identifiées autour de l'IA appliquée au SOC. |
| `docs/SECURITY_MODEL.md` | Modèle de sécurité, garanties recherchées et limites du prototype. |
| `docs/DATASET_CARD.md` | Description des jeux de logs simulés, de leurs usages et de leurs limites. |
| `docs/GROUND_TRUTH_LABELS.md` | Labels attendus et critères de comparaison pour les logs simulés. |
| `docs/QUALITY_GATES.md` | Contrôles qualité à exécuter avant validation d'une version. |
| `docs/EXPERIMENT_PROTOCOL.md` | Protocole expérimental utilisé pour évaluer le projet. |
| `docs/EVALUATION_MATRIX.md` | Grille d'évaluation des scénarios et des réponses IA. |
| `docs/EXPERIMENT_RESULTS.md` | Modèle de rapport pour consigner les résultats expérimentaux. |
| `docs/REPRODUCIBILITY.md` | Procédure pour reproduire les contrôles techniques et expérimentaux. |
| `docs/CASE_STUDY.md` | Étude de cas complète du projet. |
| `docs/DEMO_GUIDE.md` | Guide de démonstration pour entretien, portfolio ou revue technique. |
| `docs/RESEARCH_PROPOSAL.md` | Cadrage doctoral provisoire. |
| `docs/research_notes.md` | Notes de recherche et pistes d'évolution. |
| `docs/evaluation.md` | Méthodologie d'évaluation historique et complémentaire. |

## Lecture recommandée selon le profil

### Recruteur technique

Lecture conseillée :

```text
README.md
→ docs/DEMO_GUIDE.md
→ docs/CASE_STUDY.md
→ docs/QUALITY_GATES.md
→ CHANGELOG.md
```

Objectif : comprendre rapidement ce que fait le projet, comment le lancer, ce qu'il démontre et comment la qualité est contrôlée.

### Évaluateur cybersécurité

Lecture conseillée :

```text
README.md
→ docs/threat_model.md
→ docs/SECURITY_MODEL.md
→ docs/DATASET_CARD.md
→ docs/GROUND_TRUTH_LABELS.md
→ docs/EXPERIMENT_PROTOCOL.md
→ docs/EVALUATION_MATRIX.md
```

Objectif : comprendre les menaces prises en compte, les garde-fous, les données utilisées, les résultats attendus, les limites et le cadre d'évaluation.

### Encadrant académique ou doctoral

Lecture conseillée :

```text
README.md
→ docs/RESEARCH_PROPOSAL.md
→ docs/DATASET_CARD.md
→ docs/GROUND_TRUTH_LABELS.md
→ docs/EXPERIMENT_PROTOCOL.md
→ docs/EVALUATION_MATRIX.md
→ docs/EXPERIMENT_RESULTS.md
→ docs/REPRODUCIBILITY.md
```

Objectif : évaluer le potentiel scientifique, la problématique, les hypothèses, les données, la vérité terrain, la méthode et les limites actuelles.

### Contributeur technique

Lecture conseillée :

```text
README.md
→ docs/architecture.md
→ docs/DATASET_CARD.md
→ docs/GROUND_TRUTH_LABELS.md
→ docs/QUALITY_GATES.md
→ docs/REPRODUCIBILITY.md
→ CHANGELOG.md
```

Objectif : comprendre la structure du projet, les données d'exemple, les labels attendus, les contrôles attendus et la manière de vérifier une modification.

## Chaîne de crédibilité actuelle

Le projet s'appuie progressivement sur la chaîne suivante :

```text
code fonctionnel
→ tests automatisés
→ quality gates
→ sécurité documentée
→ threat model aligné
→ dataset documenté
→ vérité terrain explicitée
→ protocole expérimental
→ matrice d'évaluation
→ rapport de résultats
→ reproductibilité
→ cadrage recherche
```

## Ce que cet index ne remplace pas

Cet index ne remplace pas :

```text
le README
le changelog
les tests
les quality gates
la documentation détaillée
la validation humaine
la reproduction des résultats
```

Il sert uniquement de carte de navigation documentaire.

## Limites actuelles de la documentation

La documentation est déjà structurée, mais certaines limites restent présentes :

```text
les résultats expérimentaux doivent encore être remplis après exécution réelle
la validation externe par analyste SOC n'est pas encore réalisée
les métriques scientifiques peuvent encore être enrichies
la documentation doit rester synchronisée avec le code à chaque nouvelle version
```

## Conclusion

`docs/PROJECT_INDEX.md` sert de point d'entrée documentaire.

Il rend le projet plus lisible, plus navigable et plus facile à auditer sans modifier le fonctionnement technique du prototype.

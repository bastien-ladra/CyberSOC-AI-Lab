# Statut de la documentation — CyberSOC-AI-Lab

Ce document trie la documentation du dépôt par rôle réel.

Objectif : éviter la dispersion, éviter les doublons, identifier les documents prioritaires, les documents de support et les documents historiques.

## Règle de lecture

```text
source de vérité projet : README.md + docs/PROJECT_STATUS.md
navigation : docs/PROJECT_INDEX.md
historique : docs/CHANGELOG_RECENT.md + CHANGELOG.md
```

Tout document plus ancien doit être lu à travers ce filtre.

## Documents prioritaires

Ces documents doivent être lus en premier.

| Document | Statut | Rôle |
|---|---|---|
| `README.md` | actif | Présentation synthétique, commandes, positionnement. |
| `docs/PROJECT_STATUS.md` | actif | Point concret : objectif, avancement, limites, décision de suite. |
| `docs/PROJECT_INDEX.md` | actif | Carte de navigation documentaire. |
| `docs/DOCUMENTATION_STATUS.md` | actif | Statut des documents et tri de lecture. |

## Documents de démonstration et portfolio

| Document | Statut | Rôle |
|---|---|---|
| `docs/RECRUITER_QUICK_DEMO.md` | actif | Démonstration courte pour recruteur ou entretien. |
| `docs/DEMO_GUIDE.md` | actif | Démonstration plus complète. |
| `docs/CASE_STUDY.md` | actif | Étude de cas projet. |

## Documents sécurité et données

| Document | Statut | Rôle |
|---|---|---|
| `docs/SECURITY_MODEL.md` | actif | Modèle de sécurité et garde-fous. |
| `docs/threat_model.md` | actif | Menaces liées au SOC augmenté par IA. |
| `docs/DATASET_CARD.md` | actif | Description des logs simulés. |
| `docs/GROUND_TRUTH_LABELS.md` | actif | Vérité terrain des scénarios simulés. |

## Documents qualité, évaluation et reproductibilité

| Document | Statut | Rôle |
|---|---|---|
| `docs/QUALITY_GATES.md` | actif | Commandes qualité de référence. |
| `docs/QUALITY_GATES_REFRESH.md` | actif | Résultats qualité récents documentés. |
| `docs/EXPERIMENT_PROTOCOL.md` | actif | Protocole expérimental actuel. |
| `docs/EVALUATION_MATRIX.md` | actif | Grille d'évaluation actuelle. |
| `docs/EXPERIMENT_RESULTS.md` | actif | Résultats expérimentaux documentés. |
| `docs/REPRODUCIBILITY.md` | actif | Procédure de reproduction. |
| `docs/evaluation.md` | complément historique | Ancienne méthodologie générale, conservée mais non prioritaire. |

## Documents CIC-IDS2017

| Document | Statut | Rôle |
|---|---|---|
| `docs/PUBLIC_DATASET_ROADMAP.md` | actif | Trajectoire vers dataset public. |
| `docs/PUBLIC_DATASET_CANDIDATES.md` | actif | Candidats datasets publics. |
| `docs/CIC_IDS2017_DATASET_REVIEW.md` | actif | Revue CIC-IDS2017 sans intégration complète. |
| `docs/CIC_IDS2017_MAPPING_PLAN.md` | actif | Plan de mapping des labels. |
| `docs/CIC_IDS2017_SAMPLE_PARSER_EXAMPLE.md` | actif | Exemple contrôlé du sample row parser. |
| `docs/CIC_IDS2017_BOUNDED_MINI_LOADER_PLAN.md` | actif | Plan du mini-loader borné. |
| `docs/CIC_IDS2017_MINI_LOADER_USAGE_EXAMPLE.md` | actif | Exemple contrôlé du mini-loader avec CSV temporaire fictif. |

## Documents recherche

| Document | Statut | Rôle |
|---|---|---|
| `docs/RESEARCH_PROPOSAL.md` | actif | Cadrage doctoral provisoire. |
| `docs/research_notes.md` | notes historiques nettoyées | Notes de réflexion, non source de vérité sur l'état projet. |

## Historique

| Document | Statut | Rôle |
|---|---|---|
| `docs/CHANGELOG_RECENT.md` | actif | Historique récent à lire en priorité. |
| `CHANGELOG.md` | historique long | Historique complet ancien, volumineux, conservé pour traçabilité. |

## Ce qui n'est plus prioritaire

Ces documents ne doivent plus être utilisés comme première source pour juger l'état actuel du projet :

```text
docs/evaluation.md
→ remplacé en priorité par EXPERIMENT_PROTOCOL, EVALUATION_MATRIX et PROJECT_STATUS

docs/research_notes.md
→ conservé comme notes de recherche, mais l'état actuel est dans PROJECT_STATUS

CHANGELOG.md
→ conservé comme historique long, mais les dernières versions sont dans CHANGELOG_RECENT
```

## Suppression de fichiers

Aucun fichier n'a été supprimé à ce stade.

Raison :

```text
ne pas casser les liens existants
préserver l'historique
ne pas perdre de contexte utile
éviter une suppression difficile à justifier en revue technique
```

Le tri est donc volontairement non destructif.

## Décision documentaire

```text
README.md
→ entrée synthétique

docs/PROJECT_STATUS.md
→ source de vérité sur l'état actuel

docs/PROJECT_INDEX.md
→ carte de navigation

docs/DOCUMENTATION_STATUS.md
→ statut des documents
```

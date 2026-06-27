# Exemples de sorties générées

Ce dossier contient des exemples versionnés de sorties produites par le pipeline CyberSOC-AI-Lab.

Ces fichiers permettent de consulter rapidement le résultat attendu du projet sans devoir relancer immédiatement le pipeline.

## Contenu

```text
examples/
├── alerts/
├── reports/
├── prompts/
├── ai_outputs/
├── audit/
└── human_reviews/
```

## Rôle des exemples

Les fichiers présents dans ce dossier servent de référence démonstrative.

Ils permettent de montrer :

- les alertes structurées générées par le moteur de détection ;
- les rapports Markdown produits pour chaque incident ;
- les prompts transmis à l’assistant IA ;
- les analyses IA générées localement ;
- les évaluations automatiques des réponses IA ;
- les journaux d’audit ;
- les validations humaines effectuées depuis le dashboard.

## Différence avec runtime/

Le dossier `examples/` est versionné dans Git.

Le dossier `runtime/` est utilisé pour les exécutions locales et est ignoré par Git.

```text
examples/ → exemples conservés pour la démonstration
runtime/  → sorties locales générées à l’exécution
```

Cette séparation permet de garder le dépôt propre tout en conservant des exemples consultables par un recruteur, un évaluateur ou un contributeur.

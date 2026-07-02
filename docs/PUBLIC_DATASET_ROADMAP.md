# Roadmap dataset public

Ce document décrit comment CyberSOC-AI-Lab pourrait évoluer d'un jeu de logs simulés vers un jeu de données plus crédible, public et réutilisable.

Il ne prétend pas que cette étape est déjà réalisée.

```text
statut actuel : logs simulés versionnés
objectif futur : dataset public documenté
usage production : non
```

## Pourquoi cette roadmap existe

Le projet est déjà cohérent sur un périmètre contrôlé :

```text
logs simulés
→ labels attendus
→ vérité terrain
→ évaluation automatique
→ export JSON / Markdown
→ rapport expérimental
```

Mais pour renforcer la crédibilité scientifique et technique, il faudra ensuite sortir du périmètre purement simulé.

Objectifs :

```text
augmenter la variété des logs
réduire le biais du jeu d'exemples
tester plus de scénarios
mesurer davantage de faux positifs et faux négatifs
faciliter la reproduction par un tiers
préparer une discussion académique ou technique plus solide
```

## État actuel du dataset

Le périmètre actuel repose sur des fichiers versionnés dans :

```text
data/sample_logs/
```

Les scénarios couverts sont :

```text
SSH_BRUTE_FORCE
WEB_RECONNAISSANCE
PROMPT_INJECTION_ATTEMPT
scénarios bénins SSH et web
```

Les labels attendus sont documentés dans :

```text
docs/GROUND_TRUTH_LABELS.md
```

La comparaison automatique est assurée par :

```text
utils/ground_truth_evaluator.py
tests/test_ground_truth_evaluator.py
```

L'export des résultats est assuré par :

```text
utils/ground_truth_results_exporter.py
tests/test_ground_truth_results_exporter.py
```

## Limites du dataset actuel

Les limites actuelles sont assumées :

```text
jeu de données très petit
logs simulés uniquement
peu de diversité temporelle
peu de diversité réseau
peu de diversité d'attaques
absence de bruit réaliste massif
absence de traces issues d'un SIEM réel
absence de dataset public externe intégré
absence de validation par analystes SOC externes
```

Ces limites n'annulent pas la valeur du prototype. Elles définissent simplement le niveau de preuve actuel.

## Critères pour intégrer un dataset public

Avant d'intégrer un dataset externe, il faudra vérifier :

```text
licence compatible
source identifiable
format exploitable
absence de données personnelles sensibles non maîtrisées
possibilité de documenter les labels
possibilité de reproduire les tests
taille adaptée au projet
scénarios pertinents pour SOC / détection / IA
```

Un dataset ne doit pas être ajouté uniquement parce qu'il est volumineux. Il doit rester explicable, documenté et testable.

## Étapes proposées

### Étape 1 — Sélection

Identifier un ou plusieurs jeux de données publics candidats.

Critères :

```text
logs réseau ou système
attaques identifiables
labels disponibles ou reconstructibles
licence claire
format compatible avec Python
volume raisonnable
```

Sortie attendue :

```text
docs/PUBLIC_DATASET_CANDIDATES.md
```

### Étape 2 — Documentation

Créer une fiche dataset dédiée.

Sortie attendue :

```text
docs/PUBLIC_DATASET_CARD.md
```

Cette fiche devra documenter :

```text
source
licence
format
volume
scénarios
labels
limites
risques
usage autorisé
usage interdit
```

### Étape 3 — Normalisation

Transformer les logs externes vers un format interne contrôlé.

Sortie technique possible :

```text
utils/public_dataset_loader.py
tests/test_public_dataset_loader.py
```

Objectif : éviter de modifier tout le moteur de détection uniquement pour un dataset externe.

### Étape 4 — Vérité terrain

Créer une vérité terrain dédiée au dataset public.

Sorties possibles :

```text
docs/PUBLIC_GROUND_TRUTH_LABELS.md
utils/public_ground_truth_evaluator.py
tests/test_public_ground_truth_evaluator.py
```

Objectif : conserver la même logique que le dataset simulé :

```text
labels attendus
→ alertes observées
→ labels manquants
→ labels inattendus
→ résultat auditable
```

### Étape 5 — Résultats expérimentaux

Ajouter une section spécifique dans :

```text
docs/EXPERIMENT_RESULTS.md
```

Résultats attendus :

```text
nombre de fichiers évalués
nombre de cas passants
nombre de cas en échec
faux positifs observés
faux négatifs observés
limites d'interprétation
```

### Étape 6 — Comparaison

Comparer clairement :

```text
dataset simulé
vs
dataset public
```

Objectif : éviter de mélanger les niveaux de preuve.

## Impact attendu sur la crédibilité

L'intégration propre d'un dataset public augmenterait surtout :

```text
crédibilité recherche
crédibilité technique
robustesse de l'évaluation
capacité à discuter des faux positifs
capacité à discuter des faux négatifs
reproductibilité par un tiers
```

Impact estimé si l'étape est faite proprement :

```text
Avancement global : +3 à +5 points
Note portfolio : +1 à +2 points
Note recherche appliquée : +5 à +8 points
Note production : faible impact sans SIEM réel
```

## Risques à éviter

```text
ajouter un dataset sans licence claire
mélanger logs simulés et logs publics sans séparation
annoncer une performance générale à partir d'un dataset limité
masquer les faux positifs
ignorer les faux négatifs
ajouter trop de volume sans tests adaptés
rendre les tests lents ou instables
```

Le projet doit rester honnête : mieux vaut un dataset petit, documenté et reproductible qu'un gros dataset mal compris.

## Positionnement recommandé

Formulation à utiliser :

> Le projet dispose actuellement d'un dataset simulé maîtrisé. Une évolution future consiste à intégrer un dataset public documenté afin de renforcer la robustesse expérimentale et la reproductibilité externe.

Formulation à éviter :

> Le projet est validé sur données réelles et prêt pour la production.

## Conclusion

Cette roadmap prépare une évolution importante, mais elle ne remplace pas l'expérimentation actuelle.

La priorité reste :

```text
ne pas sur-vendre
séparer simulation et dataset public
conserver la vérité terrain
conserver les tests
conserver les limites explicites
```

Une intégration propre d'un dataset public ferait progresser CyberSOC-AI-Lab d'un prototype portfolio très solide vers une base de recherche appliquée plus crédible.

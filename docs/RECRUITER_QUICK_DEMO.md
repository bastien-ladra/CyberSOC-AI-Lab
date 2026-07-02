# Démonstration rapide recruteur

Ce document sert de guide court pour présenter CyberSOC-AI-Lab en entretien, revue portfolio ou échange recruteur.

L'objectif est de montrer rapidement :

```text
ce que fait le projet
→ comment le lancer
→ quoi regarder
→ quels résultats annoncer
→ quelles limites assumer
```

## Pitch en 30 secondes

CyberSOC-AI-Lab est un prototype expérimental de SOC augmenté par IA.

Il simule une chaîne SOC complète sur des logs versionnés :

```text
logs simulés
→ parsing
→ détection par règles
→ alertes structurées
→ enrichissement sécurité
→ prompts IA encadrés
→ analyse IA locale optionnelle
→ évaluation automatique
→ validation humaine
→ audit
→ résultats expérimentaux
```

Le projet ne cherche pas à remplacer un analyste SOC. Il montre comment une IA peut assister l'analyse tout en conservant explicabilité, contrôle humain, traçabilité et limites explicites.

## Ce qu'il faut montrer en priorité

### 1. README

Montrer le résumé de maturité :

```text
statut : prototype expérimental avancé
usage recommandé : portfolio, entretien technique, recherche appliquée
usage production SOC : non
```

Montrer aussi les résultats expérimentaux documentés :

```text
quality gates : OK
tests : 60 passed
couverture : 94.94 %
vérité terrain : OK
export JSON / Markdown : OK
rapport expérimental : rempli
```

### 2. Dashboard

Lancer le dashboard :

```bash
streamlit run dashboard/app.py
```

À montrer :

```text
alertes détectées
preuves associées
scores de priorité
recommandations analyste
filtres et recherche
validation humaine
journaux d'audit
```

### 3. Scénarios couverts

Présenter les trois scénarios :

```text
SSH_BRUTE_FORCE
WEB_RECONNAISSANCE
PROMPT_INJECTION_ATTEMPT
```

Expliquer que le scénario de prompt injection est important parce que les logs peuvent contenir des instructions hostiles destinées à manipuler un assistant IA.

### 4. Vérité terrain

Montrer que les labels attendus sont documentés et vérifiés :

```text
docs/GROUND_TRUTH_LABELS.md
utils/ground_truth_evaluator.py
tests/test_ground_truth_evaluator.py
```

Message à dire :

> Je ne me contente pas d'afficher des alertes. Je compare les alertes observées avec une vérité terrain versionnée.

### 5. Résultats expérimentaux

Montrer :

```text
docs/EXPERIMENT_RESULTS.md
runtime/evaluation/ground_truth_results.json
runtime/evaluation/ground_truth_results.md
```

Message à dire :

> Le projet produit des résultats lisibles et auditables, mais uniquement sur un périmètre simulé.

## Démonstration en 5 minutes

```text
0:00 — Présenter le README et le résumé de maturité
0:45 — Montrer les scénarios détectés
1:30 — Lancer ou ouvrir le dashboard
2:30 — Montrer une alerte, ses preuves et la validation humaine
3:30 — Montrer la vérité terrain et les tests
4:15 — Montrer les résultats expérimentaux
4:45 — Conclure sur les limites et les évolutions possibles
```

## Commandes utiles

Installation :

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Contrôles qualité :

```bash
black --check .
ruff check .
mypy .
bandit -r ai_assistant dashboard detection utils main.py -q
pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q
```

Dashboard :

```bash
streamlit run dashboard/app.py
```

Pipeline sans IA :

```bash
python main.py
```

Pipeline avec IA locale :

```bash
python main.py --enable-ai
```

## Ce qu'il faut dire clairement

Points forts :

```text
projet structuré
quality gates en place
couverture élevée
vérité terrain documentée
évaluation automatique
résultats exportables
validation humaine
sécurité IA prise en compte
limites explicites
```

Limites à assumer :

```text
logs simulés uniquement
pas de SIEM réel
pas de données SOC réelles
pas de validation externe par analystes SOC
pas de certification sécurité
pas destiné à la production
```

Phrase de conclusion recommandée :

> Le projet n'est pas une solution SOC de production. C'est un laboratoire propre, testé et documenté pour démontrer une démarche d'ingénierie cyber/IA, avec traçabilité, validation humaine et évaluation reproductible.

## Questions probables en entretien

### Est-ce utilisable en production ?

Réponse :

> Non. Le projet est volontairement présenté comme un prototype expérimental. Il manque des logs réels, une intégration SIEM, une validation externe et un durcissement production.

### Quelle est la partie la plus forte ?

Réponse :

> La chaîne complète : détection, vérité terrain, tests, export des résultats, documentation expérimentale et limites explicites.

### Pourquoi l'IA est-elle encadrée ?

Réponse :

> Parce que les logs peuvent contenir des données hostiles ou des tentatives de prompt injection. L'IA ne doit jamais traiter les logs comme des instructions fiables.

### Qu'est-ce que vous amélioreriez ensuite ?

Réponse :

```text
ajouter plus de scénarios
intégrer un dataset public
comparer plusieurs modèles locaux
mesurer les faux positifs / faux négatifs
ajouter des screenshots de démonstration
préparer une intégration SIEM fictive ou contrôlée
```

## Note de positionnement actuelle

```text
Avancement global : 88–89 %
Note portfolio : 95 / 100
Note recherche appliquée : 86 / 100
Note production : 22 / 100
```

Cette note reste indicative et dépend du périmètre simulé actuel.

# Changelog — CyberSOC-AI-Lab

## v1.25.0 — Evaluation result generation

### Ajouté

- Ajout de `utils/ground_truth_results_exporter.py`.
- Ajout de `tests/test_ground_truth_results_exporter.py`.
- Génération d’un artefact JSON de résultats de vérité terrain.
- Génération d’un rapport Markdown lisible de résultats de vérité terrain.
- Export des résultats dans `runtime/evaluation/`.
- Ajout d’un résumé avec statut, nombre de cas passants et nombre de cas en échec.
- Ajout du détail par fichier : labels attendus, observés, manquants et inattendus.

### Qualité

- `black --check .` : OK
- `ruff check .` : OK
- `mypy .` : OK
- `bandit -r ai_assistant dashboard detection utils main.py -q` : OK
- `pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q` : OK
- Tests : 60 passed
- Couverture : 94.94%

### Objectif

Passer d’une évaluation automatique interne à des résultats exportés, lisibles et auditables.

```text
labels attendus
→ alertes observées
→ comparaison automatique
→ export JSON
→ rapport Markdown
→ résultats auditables
```

---

## v1.24.1 — Ground truth documentation alignment

### Modifié

- Mise à jour du `README.md`.
- Mise à jour de `docs/PROJECT_INDEX.md`.
- Mise à jour de `docs/EXPERIMENT_PROTOCOL.md`.
- Mise à jour de `docs/EVALUATION_MATRIX.md`.
- Mise à jour de `docs/REPRODUCIBILITY.md`.
- Ajout de références explicites à `utils/ground_truth_evaluator.py`.
- Ajout de références explicites à `tests/test_ground_truth_evaluator.py`.
- Intégration de la vérification automatique de vérité terrain dans la chaîne documentaire, expérimentale et reproductible.

### Objectif

Aligner toute la documentation avec l’évaluation automatique de la vérité terrain.

```text
vérité terrain documentée
→ évaluateur automatique
→ tests dédiés
→ protocole aligné
→ matrice alignée
→ reproductibilité renforcée
```

---

## v1.24.0 — Automated ground truth evaluation

### Ajouté

- Ajout de `utils/ground_truth_evaluator.py`.
- Ajout de `tests/test_ground_truth_evaluator.py`.
- Définition automatisée des cas de vérité terrain pour les logs simulés versionnés.
- Comparaison automatique entre labels attendus et alertes observées.
- Détection automatique des labels manquants et des labels inattendus.
- Ajout de tests couvrant les cas valides et les cas d’échec.

### Qualité

- `black --check .` : OK
- `ruff check .` : OK
- `mypy .` : OK
- `bandit -r ai_assistant dashboard detection utils main.py -q` : OK
- `pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q` : OK
- Tests : 54 passed
- Couverture : 95.20%

### Objectif

Passer d’une vérité terrain documentée à une vérité terrain vérifiée automatiquement.

```text
logs simulés
→ labels attendus
→ alertes observées
→ comparaison automatique
→ évaluation plus robuste
```

---

## v1.23.1 — Ground truth documentation alignment

### Modifié

- Mise à jour du `README.md`.
- Mise à jour de `docs/PROJECT_INDEX.md`.
- Mise à jour de `docs/DATASET_CARD.md`.
- Mise à jour de `docs/EXPERIMENT_PROTOCOL.md`.
- Mise à jour de `docs/EVALUATION_MATRIX.md`.
- Ajout de références explicites à `docs/GROUND_TRUTH_LABELS.md`.
- Ajout de la vérité terrain dans la chaîne expérimentale et documentaire.
- Ajout de la comparaison résultat attendu / résultat observé dans le protocole et la matrice.

### Objectif

Aligner toute la documentation avec la vérité terrain expérimentale.

```text
logs simulés
→ dataset card
→ ground truth labels
→ protocole expérimental
→ matrice d'évaluation
→ documentation cohérente
```

---

## v1.23.0 — Ground truth labels

### Ajouté

- Ajout de `docs/GROUND_TRUTH_LABELS.md`.
- Formalisation des labels attendus pour les fichiers de `data/sample_logs/`.
- Définition des alertes attendues pour `ssh_auth.log` et `web_access.log`.
- Définition des comportements attendus pour les fichiers bénins.
- Ajout de critères de réussite et d’échec pour comparer les résultats observés aux résultats attendus.
- Clarification du périmètre : vérité terrain limitée aux logs simulés versionnés.

### Objectif

Renforcer la rigueur expérimentale en rendant les résultats attendus explicites et vérifiables.

```text
dataset documenté
→ vérité terrain
→ résultats observés
→ comparaison
→ évaluation plus crédible
```

---

## v1.22.1 — Documentation index alignment

### Modifié

- Mise à jour de `docs/PROJECT_INDEX.md`.
- Ajout de `docs/DATASET_CARD.md` dans l’index documentaire.
- Ajout de la dataset card dans les parcours de lecture pour les profils cybersécurité, académique et contributeur.
- Mise à jour du `README.md` pour référencer la dataset card.
- Alignement de la documentation après l’ajout de `docs/DATASET_CARD.md`.

### Objectif

Maintenir une documentation cohérente après l’ajout de la dataset card.

```text
dataset card
→ index documentaire
→ README
→ parcours de lecture
→ documentation alignée
```

---

## v1.22.0 — Dataset card

### Ajouté

- Ajout de `docs/DATASET_CARD.md`.
- Documentation de l’origine et du statut des données utilisées.
- Documentation des fichiers présents dans `data/sample_logs/`.
- Documentation des scénarios couverts : SSH brute force, reconnaissance web, prompt injection et trafic bénin.
- Documentation des données incluses et exclues.
- Documentation des schémas manipulés par le pipeline.
- Documentation des usages prévus, usages non prévus, limites expérimentales et risques de biais.
- Clarification du fait que le dataset ne prouve pas une efficacité sur données SOC réelles.

### Objectif

Documenter proprement les données utilisées par le projet afin de renforcer la rigueur expérimentale et d’éviter toute surinterprétation des résultats.

```text
logs simulés
→ dataset documenté
→ limites explicites
→ résultats mieux interprétés
→ projet plus rigoureux
```

---

## v1.21.3 — README documentation alignment

### Modifié

- Réécriture et simplification du `README.md`.
- Alignement du README avec l’état actuel du projet.
- Ajout d’une présentation plus claire de la chaîne : détection, preuves, IA encadrée, validation humaine, audit, évaluation et reproductibilité.
- Mise à jour des sections fonctionnalités, scénarios, architecture, installation, dashboard, Docker, tests et documentation.
- Ajout explicite des quality gates dans le README.
- Ajout d’une section documentation alignée avec `docs/PROJECT_INDEX.md`.
- Clarification des limites actuelles et du positionnement recherche.

### Objectif

Rendre le README plus lisible, plus actuel et plus exploitable pour un recruteur, un évaluateur technique ou un encadrant académique.

```text
README ancien
→ README réaligné
→ documentation cohérente
→ projet plus lisible
→ présentation plus solide
```

---

## v1.21.2 — Project documentation index

### Ajouté

- Ajout de `docs/PROJECT_INDEX.md`.
- Ajout d’un point d’entrée documentaire pour le projet.
- Ajout d’une table des documents principaux.
- Ajout de parcours de lecture selon le profil : recruteur, évaluateur cybersécurité, encadrant académique et contributeur technique.
- Ajout d’une chaîne de crédibilité documentaire du projet.
- Clarification du rôle de l’index : navigation documentaire, sans remplacer README, changelog, tests ou reproductibilité.

### Objectif

Améliorer la lisibilité du projet en rendant la documentation plus facile à parcourir, auditer et présenter.

```text
README
→ index documentaire
→ lecture par profil
→ documentation plus navigable
→ projet plus présentable
```

---

## v1.21.1 — Threat model alignment

### Modifié

- Mise à jour de `docs/threat_model.md`.
- Suppression de la référence obsolète au périmètre `MVP v0.8`.
- Alignement du threat model avec l’état actuel du prototype.
- Ajout des quality gates dans le périmètre documenté.
- Ajout du modèle de sécurité dans le périmètre documenté.
- Ajout du protocole expérimental, de la matrice d’évaluation et de la reproductibilité dans le périmètre documenté.
- Clarification des limites actuelles : absence de logs réels, SIEM réel, production, authentification, base de données, intégrité cryptographique et validation externe.

### Objectif

Maintenir la cohérence de la documentation sécurité avec l’évolution réelle du projet.

```text
threat model
→ security model
→ quality gates
→ protocole expérimental
→ reproductibilité
→ documentation cohérente
```

---

## v1.21.0 — Security model

### Ajouté

- Ajout de `docs/SECURITY_MODEL.md`.
- Formalisation du modèle de sécurité du projet.
- Clarification du rôle limité de l’IA dans la chaîne SOC.
- Définition des données considérées comme non fiables.
- Documentation du risque de prompt injection dans les logs.
- Définition des actions sensibles interdites automatiquement.
- Documentation des garde-fous existants.
- Clarification des garanties actuelles et des limites non garanties.

### Objectif

Renforcer la crédibilité sécurité du projet en clarifiant ce que le prototype protège, ce qu’il ne protège pas encore, et pourquoi la décision finale doit rester humaine.

```text
threat model
→ modèle de sécurité
→ limites explicites
→ IA encadrée
→ validation humaine
→ audit
```

---

## v1.20.3 — Reproducibility checklist

### Ajouté

- Ajout de `docs/REPRODUCIBILITY.md`.
- Ajout d’une procédure de reproduction du projet.
- Ajout des étapes d’installation dans un environnement Python isolé.
- Ajout des commandes exactes de quality gates à relancer.
- Ajout des critères de reproduction acceptée.
- Ajout des artefacts à vérifier après exécution.
- Ajout des limites de reproductibilité actuelles.

### Objectif

Permettre à une autre personne de relancer, contrôler et discuter le projet de manière structurée.

```text
projet fonctionnel
→ protocole expérimental
→ matrice d’évaluation
→ rapport de résultats
→ reproductibilité
```

---

## v1.20.2 — Experimental results report

### Ajouté

- Ajout de `docs/EXPERIMENT_RESULTS.md`.
- Ajout d’un modèle de rapport de résultats expérimentaux.
- Ajout d’une synthèse exécutive à renseigner.
- Ajout de tableaux de résultats par scénario.
- Ajout d’une section dédiée aux résultats techniques.
- Ajout d’une section pour l’analyse des écarts, limites observées et conclusion expérimentale.

### Objectif

Préparer la documentation des résultats obtenus lors de l’application du protocole expérimental et de la matrice d’évaluation.

```text
protocole expérimental
→ matrice d’évaluation
→ rapport de résultats
→ observations
→ limites
→ conclusion prudente
```

---

## v1.20.1 — Evaluation matrix

### Ajouté

- Ajout de `docs/EVALUATION_MATRIX.md`.
- Ajout d’une grille de notation de 0 à 5.
- Définition de critères communs d’évaluation.
- Définition d’indicateurs observables pour chaque scénario.
- Ajout d’une matrice dédiée à `SSH_BRUTE_FORCE`.
- Ajout d’une matrice dédiée à `WEB_RECONNAISSANCE`.
- Ajout d’une matrice dédiée à `PROMPT_INJECTION_ATTEMPT`.
- Ajout d’un niveau de maturité attendu.

### Modifié

- Mise à jour de `docs/evaluation.md` pour l’aligner avec le protocole expérimental actuel.
- Suppression de la référence obsolète au périmètre `MVP v0.8`.

### Objectif

Rendre l’évaluation du projet plus concrète, mesurable et reproductible.

```text
protocole expérimental
→ matrice d’évaluation
→ critères observables
→ scoring
→ indicateurs par scénario
→ évaluation moins subjective
```

---

## v1.20.0 — Experimental protocol

### Ajouté

- Ajout de `docs/EXPERIMENT_PROTOCOL.md`.
- Formalisation de la question de recherche.
- Formalisation de l’hypothèse principale.
- Définition du périmètre expérimental actuel.
- Définition des axes d’évaluation : détection, qualité de l’analyse IA, résistance à la prompt injection, traçabilité et contrôle humain.
- Définition d’une méthode expérimentale reproductible.
- Ajout de critères de réussite explicites.
- Ajout des limites actuelles du protocole.

### Objectif

Faire évoluer le projet d’un prototype technique propre vers un laboratoire expérimental plus défendable scientifiquement.

```text
prototype technique
→ protocole expérimental
→ critères d’évaluation
→ limites assumées
→ base doctorale plus solide
```

---

## v1.19.4 — Test coverage hardening

### Ajouté

- Ajout de tests pour le générateur de prompts d’analyse d’incident.
- Ajout de tests pour le client local Ollama avec mock réseau.
- Ajout de tests pour le journal d’audit.
- Renforcement de la couverture des modules cœur.

### Modifié

- Passage du seuil minimal de couverture de tests de 80 % à 90 %.
- Mise à jour de la CI pour bloquer toute régression sous 90 % de couverture.
- Mise à jour de la documentation des quality gates.

### Validé

- Formatage Black validé.
- Lint Ruff validé.
- Typage statique mypy validé.
- Scan sécurité Bandit validé.
- Tests pytest validés.
- Couverture de tests validée à 95 %.
- 48 tests passants.

### Objectif

Rendre la couverture de tests plus stricte et renforcer la crédibilité technique du projet.

```text
tests supplémentaires
→ couverture renforcée
→ seuil 90 %
→ 95 % validés
→ régression bloquée
→ qualité plus difficile à contester
```

---

## v1.19.3 — Coverage & security gates

### Ajouté

- Ajout de `pytest-cov` pour mesurer la couverture de tests.
- Ajout d’un seuil minimal de couverture fixé à 80 %.
- Ajout de Bandit pour effectuer un scan de sécurité statique.
- Ajout de `docs/QUALITY_GATES.md` pour documenter les contrôles qualité.
- Renforcement de la CI avec tests de couverture et scan sécurité.

### Validé

- Formatage Black validé.
- Lint Ruff validé.
- Typage statique mypy validé.
- Scan sécurité Bandit validé.
- Tests pytest validés.
- Couverture de tests validée à plus de 80 %.

### Objectif

Rendre la qualité du projet mesurable, vérifiable et plus difficile à contester.

```text
formatage
→ lint
→ typage statique
→ scan sécurité
→ tests
→ couverture minimale
→ qualité contrôlée
```

---

## v1.19.2 — Quality gates

### Ajouté

- Ajout de `requirements-dev.txt` pour séparer les dépendances de développement des dépendances runtime.
- Ajout de `pyproject.toml` pour centraliser la configuration des outils qualité.
- Ajout de Black pour vérifier le formatage du code.
- Ajout de Ruff pour vérifier les erreurs de lint et d’imports.
- Ajout de mypy pour vérifier le typage statique.
- Renforcement de la CI GitHub avec des quality gates automatiques.

### Corrigé

- Application du formatage Black sur le projet.
- Correction des annotations de types nécessaires pour rendre mypy strictement vert.
- Suppression du warning Black lié à la cible Python.

### Objectif

Rendre le projet plus difficile à casser et plus crédible lors d’une revue technique.

```text
formatage
→ lint
→ typage statique
→ tests
→ CI bloquante
→ qualité vérifiable
```

---

## v1.19.1 — Cohérence du schéma événement

### Corrigé

- Normalisation de l’utilisation des champs d’événements dans le moteur de règles.
- Correction de l’incohérence entre `raw` et `raw_log`.
- Correction de l’incohérence entre `user` et `username`.
- Correction de l’incohérence entre `status` et `status_code`.
- Correction de la liste `targeted_users` pour les alertes SSH brute force.
- Correction des preuves générées afin d’utiliser les lignes brutes de logs plutôt que des dictionnaires Python sérialisés.
- Robustification de la création du dossier d’audit.
- Robustification de l’export CSV lorsque les lignes ne possèdent pas toutes exactement les mêmes colonnes.
- Mise à jour des tests associés.
- Mise à jour des exemples versionnés après nettoyage du schéma événement.

### Objectif

Rendre le pipeline de détection plus cohérent, plus fiable et plus auditable.

Cette version corrige une dette technique importante liée au schéma interne des événements.

```text
logs parsés
→ événements normalisés
→ règles de détection cohérentes
→ alertes plus propres
→ preuves plus lisibles
→ auditabilité renforcée
```

---

## v1.19.0 — Cadrage doctoral

### Ajouté

- Ajout de `docs/RESEARCH_PROPOSAL.md`.
- Ajout d’un cadrage doctoral provisoire.
- Ajout d’une problématique de recherche structurée.
- Ajout d’hypothèses et de questions de recherche.
- Ajout d’une méthodologie expérimentale envisagée.
- Ajout des contributions attendues.
- Ajout des limites actuelles du projet dans une perspective recherche.
- Ajout d’une trajectoire de maturation vers un potentiel sujet doctoral.
- Ajout d’un lien vers le cadrage doctoral dans le README.

### Objectif

Faire évoluer CyberSOC-AI-Lab d’un simple prototype portfolio vers une base exploratoire structurée pour un futur projet doctoral.

Cette version ne prétend pas finaliser un sujet de thèse.

Elle sert à poser les fondations d’une discussion future avec un encadrant académique, un laboratoire ou une structure d’accueil.

```text
prototype technique
→ démonstrateur expérimental
→ cadrage scientifique
→ discussion académique
→ sujet doctoral potentiel
```

---

## v1.18.0 — Guide de démonstration recruteur

### Ajouté

- Ajout de `docs/DEMO_GUIDE.md`.
- Ajout d’un guide de démonstration en 5 minutes.
- Ajout d’un pitch court pour présenter le projet.
- Ajout d’une liste de points forts à mettre en avant en entretien.
- Ajout de questions possibles en entretien.
- Ajout d’une section sur les limites à assumer clairement.
- Ajout d’un lien vers le guide dans le README.

### Objectif

Améliorer l’usage portfolio du projet.

Cette version ne cherche pas à ajouter une nouvelle fonctionnalité technique, mais à rendre le projet plus facile à présenter à un recruteur ou à un interlocuteur technique.

```text
projet technique
→ explication claire
→ démonstration courte
→ entretien
→ crédibilité portfolio
```

---

## v1.17.0 — Étude de cas projet

### Ajouté

- Ajout d’une étude de cas détaillée dans `docs/CASE_STUDY.md`.
- Présentation du contexte du projet.
- Présentation du workflow SOC.
- Présentation de la place de l’IA et des garde-fous.
- Présentation du dashboard, de l’auditabilité et des limites actuelles.
- Ajout d’un positionnement portfolio pour rendre le projet plus lisible côté recruteur.

### Objectif

Améliorer la lisibilité du projet pour une démonstration, un entretien ou une revue de portfolio.

Cette évolution transforme le projet en support explicable :

```text
prototype technique
→ workflow SOC
→ démonstration IA supervisée
→ documentation portfolio
→ lecture recruteur
```

---

## v1.16.0 — Graphiques SOC dans le dashboard

### Ajouté

- Ajout de graphiques SOC dans le dashboard Streamlit.
- Affichage d’une répartition des alertes par priorité.
- Affichage d’une répartition des alertes par décision analyste.
- Ajout d’un module `utils/alert_analytics.py`.
- Centralisation du calcul des distributions dans une fonction réutilisable.
- Ajout de tests unitaires pour les distributions d’alertes.
- Documentation des graphiques SOC dans le README.

### Objectif

Améliorer la lisibilité visuelle du dashboard en permettant à l’analyste d’identifier rapidement la répartition des alertes affichées.

Cette évolution renforce l’usage démonstration et investigation du projet :

```text
détection
→ qualification
→ priorisation
→ filtrage
→ recherche
→ graphiques SOC
→ investigation analyste
```

---

## v1.15.0 — Export rapport Markdown de synthèse

### Ajouté

- Ajout d’un module `utils/report_export.py`.
- Ajout d’un export Markdown de synthèse depuis le dashboard Streamlit.
- Génération d’un fichier `cybersoc_dashboard_report.md`.
- Le rapport reprend les indicateurs SOC affichés.
- Le rapport reprend les alertes filtrées.
- Le rapport reprend l’historique des validations humaines.
- Ajout de tests unitaires pour la génération du rapport Markdown.
- Documentation de l’export Markdown dans le README.

### Objectif

Permettre de transformer l’état du dashboard en rapport lisible, exploitable et partageable.

Cette évolution renforce l’usage portfolio et audit du projet :

```text
détection
→ qualification
→ priorisation
→ validation humaine
→ historique
→ export Markdown
→ restitution
```

---

## v1.14.0 — Utilitaire d’export CSV

### Ajouté

- Ajout d’un module `utils/csv_export.py`.
- Centralisation de la génération des exports CSV dans une fonction réutilisable.
- Utilisation de `build_csv_export(...)` pour l’export des alertes filtrées.
- Utilisation de `build_csv_export(...)` pour l’export de l’historique des validations humaines.
- Ajout de tests unitaires pour l’export CSV.
- Vérification de l’encodage compatible avec les accents.

### Modifié

- Nettoyage du dashboard Streamlit en retirant la logique CSV directement intégrée à `dashboard/app.py`.

### Objectif

Améliorer la maintenabilité du projet en séparant la logique d’export CSV de la logique d’affichage du dashboard.

Cette évolution prépare le projet à de futurs exports ou rapports :

```text
détection
→ filtrage
→ vue tableau
→ export CSV centralisé
→ exploitation externe
```

---

## v1.13.0 — Recherche globale dans le dashboard

### Ajouté

- Ajout d’un champ de recherche globale dans la sidebar du dashboard Streamlit.
- Recherche possible par adresse IP source.
- Recherche possible par type d’alerte, criticité, priorité et score.
- Recherche possible dans le mapping MITRE / sécurité IA : framework, tactique, technique et ID de technique.
- Recherche possible dans la décision analyste et la note analyste.
- Application de la recherche à la vue tableau, aux indicateurs SOC, à la sélection d’alerte et à l’export CSV.
- Documentation de la recherche globale dans le README.

### Objectif

Améliorer l’investigation analyste en permettant de retrouver rapidement une alerte ou une décision à partir d’un mot-clé.

Cette évolution rend le dashboard plus exploitable lorsque le volume d’alertes augmente :

```text
détection
→ qualification
→ priorisation
→ filtrage
→ recherche
→ investigation
→ export
→ audit
```

---

## v1.12.0 — Historique des validations humaines

### Ajouté

- Ajout d’un historique des validations humaines dans le dashboard Streamlit.
- Affichage des décisions analyste sous forme de tableau.
- Affichage du contexte enrichi des validations humaines : priorité, score, technique et ID de technique.
- Export CSV de l’historique des validations humaines.
- Fusion des validations provenant de `examples/` et `runtime/`, avec priorité aux validations locales.
- Documentation de l’historique des validations humaines dans le README.

### Objectif

Améliorer l’auditabilité et le suivi des décisions analyste en rendant les validations humaines consultables directement depuis le dashboard.

Cette évolution renforce la traçabilité du workflow SOC :

```text
détection
→ qualification
→ priorisation
→ validation humaine
→ historique
→ export
→ audit
```

---

## v1.11.0 — Validations humaines enrichies

### Ajouté

- Enrichissement des fichiers de validation humaine avec le score de priorité de l’alerte.
- Ajout du label de priorité dans les validations humaines.
- Ajout du contexte MITRE / sécurité IA dans les validations humaines.
- Ajout de la tactique, de la technique et de l’identifiant de technique dans les fichiers de revue.
- Enrichissement des événements d’audit liés aux validations humaines.
- Mise à jour des exemples versionnés dans `examples/human_reviews/`.
- Mise à jour des tests unitaires associés aux validations humaines.

### Objectif

Améliorer l’auditabilité des décisions analyste en conservant plus de contexte dans chaque validation humaine.

Cette évolution renforce la traçabilité du workflow SOC :

```text
détection
→ qualification
→ priorisation
→ revue analyste
→ validation humaine enrichie
→ audit
```

---

## v1.10.0 — Statut de revue analyste dans le dashboard

### Ajouté

- Affichage de la décision analyste dans la vue tableau des alertes.
- Ajout d’un filtre par décision analyste dans la sidebar du dashboard.
- Ajout d’indicateurs SOC pour distinguer les alertes revues et non revues.
- Réutilisation centralisée du chemin de validation humaine pour éviter la duplication de logique.
- Prise en compte des validations existantes dans `runtime/` ou `examples/`.
- Documentation du statut de revue analyste dans le README.

### Objectif

Améliorer le suivi opérationnel des alertes en distinguant clairement les incidents déjà revus de ceux qui restent à analyser.

Cette évolution renforce la logique analyste du dashboard :

```text
détection
→ qualification
→ priorisation
→ investigation
→ décision analyste
→ suivi des revues
→ traçabilité
```

---

## v1.9.0 — Export CSV des alertes filtrées

### Ajouté

- Ajout d’un bouton d’export CSV dans le dashboard Streamlit.
- Export de la vue tableau des alertes.
- Respect des filtres actifs lors de l’export.
- Génération d’un fichier `cybersoc_alerts_filtered.csv`.
- Encodage compatible avec les accents pour une ouverture plus fiable dans Excel.
- Documentation de l’export CSV dans le README.

### Objectif

Permettre à un analyste d’extraire les alertes filtrées pour les exploiter dans un tableur, un rapport ou un outil externe.

Cette évolution renforce l’usage opérationnel du dashboard :

```text
détection
→ qualification
→ priorisation
→ filtrage
→ tableau
→ export CSV
→ exploitation analyste
```

---

## v1.8.0 — Indicateurs SOC dans le dashboard

### Ajouté

- Ajout d’indicateurs SOC dans le dashboard Streamlit.
- Affichage du nombre total d’alertes actuellement affichées.
- Affichage du nombre d’alertes `CRITICAL`, `HIGH` et `MEDIUM`.
- Affichage du nombre d’alertes nécessitant une validation humaine.
- Mise à jour dynamique des indicateurs selon les filtres sélectionnés.
- Documentation des indicateurs SOC dans le README.

### Objectif

Améliorer la lisibilité opérationnelle du dashboard en donnant une vue rapide de l’état des alertes affichées.

Cette évolution renforce la logique SOC du projet :

```text
détection
→ qualification
→ priorisation
→ filtrage
→ indicateurs SOC
→ investigation analyste
→ validation humaine
```

---

## v1.7.0 — Filtres analyste dans le dashboard

### Ajouté

- Ajout de filtres dans la sidebar du dashboard Streamlit.
- Filtrage des alertes par type d’alerte.
- Filtrage des alertes par criticité.
- Filtrage des alertes par priorité.
- Application des filtres à la vue tableau et à la liste de sélection des alertes.
- Documentation des filtres analyste dans le README.

### Objectif

Améliorer l’expérience analyste en permettant une investigation plus ciblée lorsque plusieurs alertes sont présentes.

Cette évolution rend le dashboard plus proche d’un outil SOC exploitable :

```text
détection
→ qualification
→ priorisation
→ filtrage
→ investigation ciblée
→ validation humaine
```

---

## v1.6.0 — Vue tableau des alertes

### Ajouté

- Ajout d’une vue tableau récapitulative des alertes dans le dashboard Streamlit.
- Affichage du type d’alerte, de la criticité, de la priorité, du score, de l’IP source et du mapping MITRE / sécurité IA.
- Meilleure comparaison visuelle entre les incidents détectés.
- Documentation de la vue tableau dans le README.

### Objectif

Améliorer la lisibilité opérationnelle du dashboard en permettant à l’analyste de comparer rapidement les alertes avant investigation détaillée.

Cette évolution rapproche le dashboard d’une mini-console SOC :

```text
détection
→ qualification
→ priorisation
→ vue tableau
→ investigation analyste
→ validation humaine
```

---

## v1.5.0 — Tri des alertes par priorité

### Ajouté

- Tri automatique des alertes par score de priorité décroissant dans le dashboard Streamlit.
- Amélioration de l’affichage des alertes dans la sidebar.
- Affichage du type d’alerte, du label de priorité, du score et de l’adresse IP source dans la liste de sélection.
- Documentation du tri des alertes dans le README.

### Objectif

Améliorer l’expérience analyste en affichant en premier les alertes les plus prioritaires.

Cette évolution rend le dashboard plus proche d’une logique SOC opérationnelle :

```text
détection
→ qualification
→ priorisation
→ tri des alertes
→ investigation analyste
→ validation humaine
```

---

## v1.4.0 — Score de priorité incident

### Ajouté

- Ajout d’un score de priorité numérique `priority_score` sur 100 pour chaque alerte.
- Ajout d’un label de priorité `priority_label`.
- Calcul de priorité basé sur la criticité et la confiance de détection.
- Affichage de la priorité et du score dans le dashboard Streamlit.
- Mise à jour des exemples versionnés dans `examples/`.
- Ajout de tests unitaires pour vérifier le calcul du score de priorité.

### Objectif

Aider l’analyste à prioriser les incidents en ajoutant une couche de tri simple, explicable et visible dans le dashboard.

Cette évolution renforce le workflow SOC du projet :

```text
détection
→ qualification
→ priorisation
→ recommandations analyste
→ validation humaine
→ traçabilité
```

---

## v1.3.0 — Séparation lecture / écriture du dashboard

### Corrigé

- Le dashboard peut lire les données depuis `examples/` sans écrire dans ce dossier.
- Les validations humaines créées depuis le dashboard sont écrites dans `runtime/` lorsque les données lues proviennent des exemples.
- Ajout d’un dossier de lecture et d’un dossier d’écriture distincts dans l’interface.
- Préservation des exemples versionnés contre les modifications locales.

### Objectif

Permettre d’utiliser `examples/` comme source de démonstration sans salir le dépôt Git avec de nouvelles validations humaines.

---

## v1.2.0 — Recommandations analyste dans le dashboard

### Ajouté

- Affichage des recommandations analyste dans le dashboard Streamlit.
- Mise en avant du champ `recommended_actions` déjà présent dans les alertes.
- Visualisation directe des actions suggérées pour chaque type d’incident.
- Documentation du rôle des recommandations analyste dans le README.

### Objectif

Rendre le dashboard plus utile pour un workflow SOC en affichant non seulement la détection et la qualification, mais aussi les actions recommandées à l’analyste.

Les recommandations restent soumises à validation humaine avant toute action sensible.

---

## v1.1.0 — Enrichissement MITRE ATT&CK des alertes

### Ajouté

- Ajout d’un mapping MITRE ATT&CK pour les alertes `SSH_BRUTE_FORCE`.
- Ajout d’un mapping MITRE ATT&CK pour les alertes `WEB_RECONNAISSANCE`.
- Ajout d’un mapping de sécurité IA pour les alertes `PROMPT_INJECTION_ATTEMPT`.
- Ajout d’un champ `mitre_attack` dans les alertes générées.
- Affichage de l’enrichissement MITRE / sécurité IA dans le dashboard Streamlit.
- Mise à jour des exemples versionnés dans `examples/`.
- Ajout de tests unitaires pour vérifier les mappings MITRE et sécurité IA.

### Objectif

Renforcer la valeur SOC du prototype en ajoutant un contexte de qualification cyber aux alertes générées.

Cette version rapproche le projet d’un workflow SOC plus réaliste :

```text
détection
→ qualification
→ contexte MITRE / sécurité IA
→ recommandations analyste
→ validation humaine
```

---

## v1.0.1 — Nettoyage documentation README

### Corrigé

- Alignement de l’arborescence README avec la structure réelle du projet.
- Correction des chemins de sortie vers `runtime/`.
- Clarification du rôle de `examples/`.
- Mise à jour de la stack technique avec Docker comme fonctionnalité actuelle.
- Nettoyage de la roadmap après la stabilisation du MVP v1.0.0.

### Objectif

Rendre la documentation cohérente avec l’état réel du projet avant publication du dépôt.

---

## v1.0.0 — MVP stable

### Statut

Première version stable du MVP CyberSOC-AI-Lab.

### Inclus

- Parsing de logs SSH et web simulés.
- Détection de brute force SSH.
- Détection de reconnaissance web.
- Détection de tentative de prompt injection dans les logs.
- Génération d’alertes JSON.
- Génération de rapports Markdown.
- Génération de prompts IA sécurisés.
- Analyse IA locale optionnelle via Ollama.
- Évaluation automatique des réponses IA.
- Journalisation d’audit.
- Validation humaine via dashboard Streamlit.
- Séparation entre exemples versionnés et sorties runtime locales.
- Fallback automatique du dashboard vers les exemples versionnés.
- Support Docker.
- Tests unitaires et GitHub Actions.

### Objectif

Fournir un prototype démontrable, reproductible et auditable de SOC augmenté par IA avec supervision humaine.

---

## v0.9.10 — Documentation du fallback dashboard

### Ajouté

- Documentation du fallback automatique du dashboard vers `examples/`.
- Clarification de l’ordre de lecture des données du dashboard :
  - `CYBERSOC_OUTPUT_DIR` si défini ;
  - `runtime/` si des alertes locales existent ;
  - `examples/` comme fallback de démonstration.
- Mise à jour du README avec une section dédiée à la source de données du dashboard.

### Objectif

Permettre à un utilisateur externe de comprendre qu’il peut lancer directement le dashboard après clonage du dépôt, sans exécuter immédiatement le pipeline.

---

## v0.9.9 — Fallback du dashboard vers les exemples

### Ajouté

- Le dashboard Streamlit lit désormais `runtime/` lorsque des alertes locales sont disponibles.
- Si aucune alerte runtime n’est disponible, le dashboard utilise automatiquement les exemples versionnés dans `examples/`.
- Le dossier utilisé est affiché dans l’interface du dashboard.

### Objectif

Permettre à un utilisateur externe de lancer directement le dashboard après clonage du dépôt, sans devoir exécuter immédiatement le pipeline de génération.

---

## v0.9.8 — Documentation des exemples versionnés

### Ajouté

- Ajout d’un fichier `examples/README.md`.
- Documentation du rôle du dossier `examples/`.
- Clarification de la différence entre `examples/` et `runtime/`.

### Objectif

Rendre les sorties d’exemple plus compréhensibles pour un recruteur, un évaluateur ou un contributeur.

---

## v0.9.7 — Séparation des exemples versionnés

### Modifié

- Déplacement des sorties d’exemple versionnées dans le dossier `examples/`.
- Conservation des sorties runtime locales dans `runtime/`.
- Ignorance des dossiers de sortie personnalisés de type `runtime-*/`.
- Clarification de la séparation entre données de démonstration et fichiers générés localement.

### Objectif

Rendre le dépôt plus lisible pour un utilisateur externe en distinguant les exemples consultables des sorties générées à l’exécution.

---

## v0.9.6 — Documentation du dossier runtime configurable

### Ajouté

- Documentation de la variable d’environnement `CYBERSOC_OUTPUT_DIR`.
- Documentation de l’utilisation conjointe de `main.py --output-dir` et du dashboard Streamlit.
- Mise à jour du README avec un exemple PowerShell.
- Mise à jour de la documentation d’architecture concernant le dossier `runtime/`.

### Objectif

Clarifier l’utilisation d’un dossier de sortie personnalisé et rendre le comportement du pipeline et du dashboard plus compréhensible pour un utilisateur externe.

---

## v0.9.5 — Dossier runtime configurable pour le dashboard

### Ajouté

- Le dashboard peut maintenant lire un dossier de sortie personnalisé via la variable d’environnement `CYBERSOC_OUTPUT_DIR`.
- Cette configuration permet d’utiliser le dashboard avec les sorties générées par `main.py --output-dir`.

### Exemple

```powershell
$env:CYBERSOC_OUTPUT_DIR="runtime-test"
python main.py --output-dir runtime-test --enable-ai
streamlit run dashboard/app.py
```

### Objectif

Rendre cohérente l’option `--output-dir` du pipeline avec le dashboard Streamlit.

---

## v0.9.4 — Documentation de l’architecture runtime

### Ajouté

- Documentation du dossier `runtime/` dans `docs/architecture.md`.
- Explication de la séparation entre fichiers versionnés et sorties locales générées.
- Documentation de l’option `--output-dir`.

### Objectif

Rendre l’architecture du projet plus claire concernant la gestion des fichiers générés.

---

## v0.9.3 — Documentation du dossier runtime

### Ajouté

- Mise à jour du README pour expliquer le dossier `runtime/`.
- Mise à jour du CHANGELOG pour documenter l’isolation des sorties générées.
- Clarification du fait que `runtime/` est ignoré par Git.

### Objectif

Aligner la documentation avec le nouveau comportement du pipeline.

---

## v0.9.2 — Sorties runtime isolées

### Modifié

- Les sorties générées par `main.py` sont maintenant écrites dans `runtime/`.
- Le dashboard Streamlit lit les alertes, rapports, prompts, analyses IA, audits et validations humaines depuis `runtime/`.
- Le dossier `runtime/` est ignoré par Git.

### Objectif

Éviter que les exécutions locales modifient les fichiers versionnés et garder un dépôt propre après chaque test.

---

## v0.9.1 — Documentation Docker

### Ajouté

- Documentation de l’utilisation Docker dans le README.
- Documentation des commandes de build et d’exécution Docker.
- Clarification de l’exécution du dashboard Streamlit via conteneur.

### Objectif

Faciliter le lancement du projet sur une autre machine.

---

## v0.9.0 — Support Docker

### Ajouté

- Ajout d’un `Dockerfile`.
- Ajout d’un `.dockerignore`.
- Possibilité de lancer le dashboard Streamlit dans un conteneur Docker.
- Possibilité d’exécuter le pipeline depuis Docker.

### Objectif

Faciliter l’exécution du projet sur une autre machine et préparer une future industrialisation.

---

## v0.8.5 — Changelog initial

### Ajouté

- Création du fichier `CHANGELOG.md`.
- Documentation de l’historique des versions du prototype.
- Structuration des évolutions du projet par versions.

### Objectif

Rendre l’évolution du projet plus lisible et mieux valorisable.

---

## v0.8.4 — Documentation alignée et logs personnalisés

### Ajouté

- Documentation des options CLI permettant de fournir des fichiers de logs personnalisés.
- Documentation des logs bénins utilisés pour tester les faux positifs.
- Mise à jour de la documentation d’architecture.
- Mise à jour de la documentation d’évaluation.

### Vérifié

- Les tests unitaires passent avec succès.
- Les logs bénins ne génèrent aucune alerte.
- Les logs d’attaque génèrent les alertes attendues.
- Le pipeline IA reste fonctionnel.
- Le dashboard Streamlit reste fonctionnel.

### Objectif

Aligner la documentation avec les fonctionnalités réellement présentes dans le MVP.

---

## v0.8.3 — Fichiers de logs personnalisés en CLI

### Ajouté

- Ajout des options CLI :
  - `--ssh-log-file`
  - `--web-log-file`

Ces options permettent de lancer le moteur de détection sur différents jeux de logs sans modifier le code.

### Exemple

```bash
python main.py --ssh-log-file data/sample_logs/benign_ssh_auth.log --web-log-file data/sample_logs/benign_web_access.log
```

### Résultat attendu

```text
Aucune alerte détectée.
```

### Objectif

Permettre de tester facilement le moteur de détection sur plusieurs jeux de logs.

---

## v0.8.2 — Logs bénins et tests faux positifs

### Ajouté

- Ajout de logs SSH bénins.
- Ajout de logs web bénins.
- Ajout de tests vérifiant l’absence de fausses alertes sur trafic normal.
- Ajout d’un test de non-détection de prompt injection sur trafic web normal.

### Objectif

Vérifier que le moteur de détection ne déclenche pas d’alertes sur des comportements normaux.

---

## v0.8.1 — Logs simulés versionnés

### Corrigé

- Mise à jour du `.gitignore` afin de conserver les logs simulés nécessaires au fonctionnement du MVP.
- Ajout explicite des logs simulés dans le dépôt.

### Objectif

Rendre le projet reproductible après clonage du dépôt.

---

## v0.8 — Détection de prompt injection

### Ajouté

- Détection d’une tentative de prompt injection dans les logs web.
- Nouvelle alerte : `PROMPT_INJECTION_ATTEMPT`.
- Génération d’un rapport, d’un prompt IA, d’une analyse IA et d’une évaluation IA pour ce scénario.
- Validation humaine du scénario via le dashboard.
- Mise à jour du README et de la documentation interne.

### Objectif

Traiter un risque spécifique aux SOC augmentés par IA : la présence de données hostiles dans les logs pouvant tenter de manipuler un modèle IA.

---

## v0.7 — Validation humaine

### Ajouté

- Workflow de validation humaine dans le dashboard Streamlit.
- Décision analyste par alerte.
- Note analyste.
- Stockage des validations humaines au format JSON.
- Journalisation des validations humaines dans un fichier dédié.
- Consultation des validations humaines existantes depuis le dashboard.

### Objectif

Garantir que l’IA assiste l’analyste sans remplacer la décision humaine.

---

## v0.6 — Dashboard Streamlit

### Ajouté

- Interface Streamlit.
- Visualisation des alertes.
- Consultation des rapports.
- Consultation des prompts IA.
- Consultation des analyses IA.
- Affichage des scores d’évaluation IA.
- Consultation du journal d’audit.

### Objectif

Rendre le projet démontrable visuellement.

---

## v0.5 — Analyse IA locale et évaluation IA

### Ajouté

- Connexion optionnelle à Ollama.
- Génération d’analyses IA locales.
- Évaluation automatique des réponses IA.
- Score d’acceptabilité.
- Détection de recommandations dangereuses.
- GitHub Actions.
- Tests unitaires.

### Objectif

Ajouter une couche IA contrôlée et évaluée.

---

## v0.4 — Documentation de recherche

### Ajouté

- Documentation d’architecture.
- Threat model.
- Notes de recherche.
- Méthodologie d’évaluation.

### Objectif

Positionner le projet comme base exploratoire pour un SOC augmenté par IA.

---

## v0.3 — Rapports et prompts IA

### Ajouté

- Génération de rapports Markdown.
- Génération de prompts IA sécurisés.
- Journalisation des traitements.

### Objectif

Préparer l’intégration contrôlée d’une couche IA.

---

## v0.2 — Alertes structurées

### Ajouté

- Génération d’alertes JSON.
- Détection brute force SSH.
- Détection reconnaissance web.

### Objectif

Structurer les sorties du moteur de détection.

---

## v0.1 — Base du prototype

### Ajouté

- Parsing de logs SSH simulés.
- Parsing de logs web simulés.
- Première structure du projet Python.

### Objectif

Construire la base technique du prototype.

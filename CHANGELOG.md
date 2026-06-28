# Changelog — CyberSOC-AI-Lab

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

# Changelog — CyberSOC-AI-Lab

## v0.9.9 — Fallback du dashboard vers les exemples

### Ajouté

- Le dashboard Streamlit lit désormais `runtime/` lorsque des alertes locales sont disponibles.
- Si aucune alerte runtime n’est disponible, le dashboard utilise automatiquement les exemples versionnés dans `examples/`.
- Le dossier utilisé est affiché dans l’interface du dashboard.

### Objectif

Permettre à un utilisateur externe de lancer directement le dashboard après clonage du dépôt, sans devoir exécuter immédiatement le pipeline de génération.

## v0.9.7 — Séparation des exemples versionnés

### Modifié

- Déplacement des sorties d’exemple versionnées dans le dossier `examples/`.
- Conservation des sorties runtime locales dans `runtime/`.
- Clarification de la séparation entre données de démonstration et fichiers générés localement.

### Objectif

Rendre le dépôt plus lisible pour un utilisateur externe en distinguant les exemples consultables des sorties générées à l’exécution.

## v0.9.6 — Documentation du dossier runtime configurable

### Ajouté

- Documentation de la variable d’environnement `CYBERSOC_OUTPUT_DIR`.
- Documentation de l’utilisation conjointe de `main.py --output-dir` et du dashboard Streamlit.
- Mise à jour du README avec un exemple PowerShell.
- Mise à jour de la documentation d’architecture concernant le dossier `runtime/`.

### Objectif

Clarifier l’utilisation d’un dossier de sortie personnalisé et rendre le comportement du pipeline et du dashboard plus compréhensible pour un utilisateur externe.

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

## v0.9.2 — Sorties runtime isolées

### Modifié

- Les sorties générées par `main.py` sont maintenant écrites dans `runtime/`.
- Le dashboard Streamlit lit les alertes, rapports, prompts, analyses IA, audits et validations humaines depuis `runtime/`.
- Le dossier `runtime/` est ignoré par Git.

### Objectif

Éviter que les exécutions locales modifient les fichiers versionnés et garder un dépôt propre après chaque test.

## v0.9.0 — Support Docker

### Ajouté

- Ajout d’un `Dockerfile`.
- Ajout d’un `.dockerignore`.
- Possibilité de lancer le dashboard Streamlit dans un conteneur Docker.
- Possibilité d’exécuter le pipeline depuis Docker.

### Objectif

Faciliter l’exécution du projet sur une autre machine et préparer une future industrialisation.

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

---

## v0.8.2 — Logs bénins et tests faux positifs

### Ajouté

- Ajout de logs SSH bénins.
- Ajout de logs web bénins.
- Ajout de tests vérifiant l’absence de fausses alertes sur trafic normal.

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

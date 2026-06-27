# Incident Report — SSH_BRUTE_FORCE

## Résumé

Une alerte de type `SSH_BRUTE_FORCE` a été détectée depuis l'adresse IP `185.12.45.10`.

## Détails de l'incident

- Type d'alerte : `SSH_BRUTE_FORCE`
- Criticité : `HIGH`
- Adresse IP source : `185.12.45.10`
- Score de confiance : `87 %`
- Validation humaine requise : `True`
- Nombre d'échecs de connexion : `6`
- Comptes ciblés : `admin, deploy, postgres, root, test, ubuntu`

## Preuves observées

- `Jun 24 10:01:12 server01 sshd[1201]: Failed password for invalid user admin from 185.12.45.10 port 53321 ssh2`
- `Jun 24 10:01:22 server01 sshd[1202]: Failed password for invalid user root from 185.12.45.10 port 53322 ssh2`
- `Jun 24 10:01:35 server01 sshd[1203]: Failed password for invalid user test from 185.12.45.10 port 53323 ssh2`
- `Jun 24 10:01:49 server01 sshd[1204]: Failed password for invalid user ubuntu from 185.12.45.10 port 53324 ssh2`
- `Jun 24 10:02:03 server01 sshd[1205]: Failed password for invalid user deploy from 185.12.45.10 port 53325 ssh2`
- `Jun 24 10:02:18 server01 sshd[1206]: Failed password for invalid user postgres from 185.12.45.10 port 53326 ssh2`

## Analyse

Le comportement observé est compatible avec une activité suspecte nécessitant une vérification par un analyste humain.

## Recommandations

- Bloquer temporairement l'adresse IP source après validation humaine.
- Vérifier les comptes ciblés.
- Contrôler les connexions réussies récentes.
- Renforcer l'authentification MFA si elle n'est pas active.
- Analyser les logs sur la même fenêtre temporelle.

## Limites de l'analyse

Cette détection repose sur des règles simples et explicables.
Une validation humaine est nécessaire avant toute action de blocage ou de remédiation.


# Incident Report — SSH_BRUTE_FORCE

## Résumé

Une tentative probable de brute force SSH a été détectée depuis l'adresse IP `185.12.45.10`.

## Criticité

**HIGH**

## Score de confiance

**87 %**

## Détails de l'incident

- Type d'alerte : `SSH_BRUTE_FORCE`
- Adresse IP source : `185.12.45.10`
- Nombre d'échecs de connexion : `6`
- Comptes ciblés : `admin, deploy, postgres, root, test, ubuntu`
- Validation humaine requise : `True`

## Preuves observées

- `Jun 24 10:01:12 server01 sshd[1201]: Failed password for invalid user admin from 185.12.45.10 port 53321 ssh2`
- `Jun 24 10:01:22 server01 sshd[1202]: Failed password for invalid user root from 185.12.45.10 port 53322 ssh2`
- `Jun 24 10:01:35 server01 sshd[1203]: Failed password for invalid user test from 185.12.45.10 port 53323 ssh2`
- `Jun 24 10:01:49 server01 sshd[1204]: Failed password for invalid user ubuntu from 185.12.45.10 port 53324 ssh2`
- `Jun 24 10:02:03 server01 sshd[1205]: Failed password for invalid user deploy from 185.12.45.10 port 53325 ssh2`
- `Jun 24 10:02:18 server01 sshd[1206]: Failed password for invalid user postgres from 185.12.45.10 port 53326 ssh2`

## Analyse

Le nombre élevé d'échecs de connexion SSH depuis une même adresse IP indique un comportement compatible avec une attaque par force brute.

## Recommandations

- Bloquer temporairement l'adresse IP source.
- Vérifier les comptes ciblés.
- Contrôler les connexions réussies récentes.
- Renforcer l'authentification MFA si elle n'est pas active.
- Analyser les logs sur la même fenêtre temporelle.

## Limites de l'analyse

Cette détection repose sur une règle simple basée sur le nombre d'échecs de connexion.
Une validation humaine est nécessaire avant toute action de blocage ou de remédiation.


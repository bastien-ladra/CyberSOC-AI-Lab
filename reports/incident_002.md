# Incident Report — WEB_RECONNAISSANCE

## Résumé

Une alerte de type `WEB_RECONNAISSANCE` a été détectée depuis l'adresse IP `185.12.45.10`.

## Détails de l'incident

- Type d'alerte : `WEB_RECONNAISSANCE`
- Criticité : `MEDIUM`
- Adresse IP source : `185.12.45.10`
- Score de confiance : `82 %`
- Validation humaine requise : `True`
- Requêtes suspectes : `6`
- Chemins ciblés : `/.env, /admin, /backup.zip, /config.php, /phpmyadmin, /wp-admin`

## Preuves observées

- `185.12.45.10 - - [24/Jun/2026:11:01:12 +0000] "GET /admin HTTP/1.1" 404 512 "-" "curl/8.0"`
- `185.12.45.10 - - [24/Jun/2026:11:01:14 +0000] "GET /wp-admin HTTP/1.1" 404 512 "-" "curl/8.0"`
- `185.12.45.10 - - [24/Jun/2026:11:01:16 +0000] "GET /.env HTTP/1.1" 404 512 "-" "curl/8.0"`
- `185.12.45.10 - - [24/Jun/2026:11:01:18 +0000] "GET /phpmyadmin HTTP/1.1" 404 512 "-" "curl/8.0"`
- `185.12.45.10 - - [24/Jun/2026:11:01:20 +0000] "GET /backup.zip HTTP/1.1" 404 512 "-" "curl/8.0"`
- `185.12.45.10 - - [24/Jun/2026:11:01:22 +0000] "GET /config.php HTTP/1.1" 404 512 "-" "curl/8.0"`

## Analyse

Le comportement observé est compatible avec une activité suspecte nécessitant une vérification par un analyste humain.

## Recommandations

- Vérifier si l'adresse IP source est connue ou légitime.
- Analyser les chemins ciblés et les codes HTTP retournés.
- Corréler avec d'autres logs applicatifs ou firewall.
- Mettre en place une limitation de débit si nécessaire.
- Surveiller une éventuelle tentative d'exploitation après la phase de reconnaissance.

## Limites de l'analyse

Cette détection repose sur des règles simples et explicables.
Une validation humaine est nécessaire avant toute action de blocage ou de remédiation.


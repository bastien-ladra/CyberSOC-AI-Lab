# Quality gates — snapshot historique

Ce document conserve un ancien snapshot local (`v1.39.1`) à des fins de traçabilité. Il **ne doit pas être utilisé comme preuve de l'état courant** du dépôt.

## Snapshot conservé

Les résultats documentés à l'époque étaient :

```text
Black : OK
Ruff : OK
mypy : OK
Bandit : aucune alerte bloquante signalée
pytest : 83 passed
coverage : 95.99 %
seuil coverage : 90 %
```

## Source de vérité actuelle

L'état courant doit être évalué à partir de :

1. la pull request / le commit concerné ;
2. `.github/workflows/tests.yml` ;
3. les résultats GitHub Actions correspondants.

Un ancien résultat local ne prouve ni la qualité d'un commit ultérieur, ni une performance SOC sur des données réelles.

## Limite

Ces quality gates vérifient la qualité du logiciel et certaines propriétés de sécurité statique. Ils ne constituent pas une certification de sécurité, une validation SOC externe ni une preuve de maturité production.

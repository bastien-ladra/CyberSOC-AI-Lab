# Quality gates refresh

Ce document consigne le rafraîchissement local des contrôles qualité pour `v1.39.0`.

Les résultats proviennent d'une exécution locale fournie sous forme de capture terminal.

## Résultats confirmés

```text
black --check .
→ 37 files would be left unchanged

ruff check .
→ All checks passed

mypy .
→ Success: no issues found in 37 source files

pytest avec couverture
→ 83 passed
→ couverture totale : 95.99 %
→ seuil requis : 90 %
```

## Résultat pytest / coverage

```text
83 passed
Total coverage: 95.99 %
Required test coverage of 90% reached
```

## Point de prudence

La sortie `bandit` n'était pas visible dans la capture fournie.

Le workflow CI conserve bien un contrôle Bandit, mais ce document ne revendique pas un résultat Bandit local rafraîchi tant que sa sortie n'est pas explicitement fournie.

## Synthèse

```text
formatage : OK
lint : OK
typage : OK
tests : OK
couverture : OK
bandit local : non confirmé dans la capture
```

## Limite

Ces résultats ne transforment pas le prototype en solution SOC de production.

Ils renforcent surtout :

```text
crédibilité portfolio
→ crédibilité technique
→ reproductibilité locale
→ confiance dans les ajouts CIC-IDS2017 récents
```

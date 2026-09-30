Type: grilling
Status: resolved
Blocked by: 01, 02

## Question

Quelle spécification CLI + SVG pour le script Python phase 1 (args, layout fichiers, structure SVG, cache JSON, gestion fenêtre glissante 53 semaines, sortie `contributions.svg`) ?

## Answer

Spec verrouillée (grilling Q1-Q4, tout default) : fenêtre glissante 1 an par défaut (from/to omis), `--from/--to` pour figer ; cache brut `contributionsCollection` trié dans `data/contributions.json` + `--no-fetch` offline ; args `--login/--out/--cache/--from/--to/--token/--no-fetch`, token `--token` > `GITHUB_TOKEN` > `GITHUB_DDCQ_READ` ; SVG standalone sans CSS externe, légende Less/More incluse, total sur stdout hors SVG. Implémenté et vérifié sur données réelles ddcq (680, 53 semaines, 368 jours).

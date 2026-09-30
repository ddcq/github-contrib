Type: task
Status: resolved
Blocked by:

## Question

Obtenir un token GitHub valide et capturer un échantillon réel `ContributionsCollection` pour `ddcq` (JSON brut + semaine type) afin de débloquer les décisions de rendu et de CLI.

## Answer

Fait : token classic `GITHUB_DDCQ_READ` (~/.zshrc), fetch live OK le 2026-09-30. Résultats : total=680, 53 semaines / 368 jours, `restrictedContributionsCount=0`, `hasAnyRestrictedContributions=false` (public seul : scope `read:user` manquant ou partage privé désactivé). Cache `data/contributions.json` (git-ignoré), SVG `contributions.svg` généré : 368 `<title>`, 373 `<rect>` (368 jours + 5 légende). Si privées voulues : recréer le token avec scope `read:user`.

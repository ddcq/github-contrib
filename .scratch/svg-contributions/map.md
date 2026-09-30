## Destination

Spécification phase 1 prête à implémenter : script Python qui interroge GraphQL `ContributionsCollection` (user `ddcq`) et génère un SVG statique visuellement identique au calendrier public GitHub (light mode).

## Notes

- Domaine : GitHub GraphQL, SVG statique, Python.
- Skills à consulter chaque session : `grilling` + `domain-modeling` par défaut ; `research` pour tickets research ; `prototype` pour tickets prototype.
- Préférences : Python sauf avantage décisif autre langage ; fidélité pixel-proche light mode ; live query + cache JSON ; token via env ; sortie `contributions.svg` standalone.
- Tracker : local-markdown (défaut, pas de remote). Voir `.scratch/svg-contributions/issues/`.

## Decisions so far

<!-- index : une ligne par ticket clos, gist + lien -->

## Not yet specified

- Seuils exacts des 5 niveaux de verts vs comptes (dépend du rendu GitHub réel).
- Détail tooltips / `<title>` et accessibilité du SVG.
- Format du cache JSON et politique de refresh manuel.
- Gestion des cas limites : années bissextiles, fuseaux, comptes privés à zéro.

## Out of scope

- Animations du SVG (phase 2, effort frais séparé).
- Dark mode GitHub (décidé : light seul pour phase 1).
- Refresh auto via GitHub Action planifiée (décidé : script local manuel pour phase 1).

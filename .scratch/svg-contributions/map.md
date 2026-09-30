## Destination

Spécification phase 1 prête à implémenter : script Python qui interroge GraphQL `ContributionsCollection` (user `ddcq`) et génère un SVG statique visuellement identique au calendrier public GitHub (light mode).

## Notes

- Domaine : GitHub GraphQL, SVG statique, Python.
- Skills à consulter chaque session : `grilling` + `domain-modeling` par défaut ; `research` pour tickets research ; `prototype` pour tickets prototype.
- Préférences : Python sauf avantage décisif autre langage ; fidélité pixel-proche light mode ; live query + cache JSON ; token via env ; sortie `contributions.svg` standalone.
- Tracker : local-markdown (défaut, pas de remote). Voir `.scratch/svg-contributions/issues/`.

## Decisions so far

<!-- index : une ligne par ticket clos, gist + lien -->

- [Rendu calendrier GitHub exact](.scratch/svg-contributions/issues/02-github-calendar-render.md): palette Primer light + cellules 10px gap 3px + labels/tooltips/legende verrouilles.
- [Shape GraphQL ContributionsCollection](.scratch/svg-contributions/issues/01-graphql-contributions-shape.md): query minimale + levels relatifs + scope read:user avec fallback public.
- [Échantillon réel + token](.scratch/svg-contributions/issues/03-sample-data-token.md): fetch live ddcq OK, total 680 sur 53 semaines, SVG 368 jours généré.
- [Spec CLI + SVG](.scratch/svg-contributions/issues/04-cli-svg-spec.md): glissant par défaut, cache brut + --no-fetch, token --token > GITHUB_TOKEN > GITHUB_DDCQ_READ, SVG standalone + légende.

## Not yet specified

- Gestion des cas limites : années bissextiles, fuseaux (couverts via dates ISO + weekday, à valider sur année civile).

## Out of scope

- Animations du SVG (phase 2, effort frais séparé).
- Dark mode GitHub (décidé : light seul pour phase 1).
- Refresh auto via GitHub Action planifiée (décidé : script local manuel pour phase 1).

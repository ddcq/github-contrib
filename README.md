# github-contrib

Phase 1 : SVG statique identique au calendrier public GitHub (light mode), depuis GraphQL `ContributionsCollection` (user `ddcq`).

```bash
export GITHUB_TOKEN=...
python -m github_contrib --login ddcq --out contributions.svg
```

Phase 2 (hors scope) : animations.

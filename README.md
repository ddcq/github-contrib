# github-contrib

![contributions](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions.svg)

Phase 1 : SVG statique identique au calendrier public GitHub (light mode), depuis GraphQL `ContributionsCollection` (user `ddcq`).

URL publique : `https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions.svg`

```bash
export GITHUB_TOKEN=...
PYTHONPATH=src python -m github_contrib --login ddcq --out contributions.svg
```

## Automation

La GitHub Action `contributions` régénère `contributions.svg` chaque jour à 06:00 UTC (déclenchable à la main via `workflow_dispatch`) et le commite sur `main`.

- Token : `github.token` par défaut (contributions publiques). Pour inclure les privées, ajouter un secret `CONTRIB_PAT` (classic, scope `read:user`).
- Mise en route : `git push -u origin main` (le dépôt distant existe déjà), l'Action tourne au prochain schedule ou via l'onglet Actions.

Phase 2 (hors scope) : animations.

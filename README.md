# github-contrib

![contributions](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions.svg)

Calendrier de contributions GitHub généré depuis GraphQL `ContributionsCollection` (user `ddcq`), avec vague animée et 5 thèmes couleur.

| Thème | Fichier | Aperçu |
|---|---|---|
| dark-green (défaut, legacy) | `contributions.svg` | ![dark-green](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions.svg) |
| blue | `contributions-blue.svg` | ![blue](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions-blue.svg) |
| dark-blue | `contributions-dark-blue.svg` | ![dark-blue](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions-dark-blue.svg) |
| red | `contributions-red.svg` | ![red](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions-red.svg) |
| dark-red | `contributions-dark-red.svg` | ![dark-red](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions-dark-red.svg) |

## Prérequis

- Python ≥ 3.11 (workflow : 3.13)
- Token GitHub pour fetch API (sinon `--no-fetch` + cache local `data/contributions.json`)

```bash
export GITHUB_TOKEN=...
PYTHONPATH=src python3 -m github_contrib --login ddcq --out contributions.svg --no-fetch
```

## Options CLI

```
--login LOGIN            user GitHub (défaut ddcq)
--out OUT                fichier base (défaut contributions.svg)
--cache CACHE            cache JSON (défaut data/contributions.json)
--from FROM_ISO          borne début (optionnel, ex. 2024-10-01T00:00:00Z)
--to TO_ISO              borne fin (optionnel)
--token TOKEN            override GITHUB_TOKEN / GITHUB_DDCQ_READ
--animate {wave,none}    wave (défaut) ou none = statique Phase1 byte-identique
--theme {all,dark-green,blue,dark-blue,red,dark-red}
                         all (défaut) = 5 fichiers, sinon 1 seul vers --out
--wave SPEC              DSL vague, répétable pour chaînage (défaut diagonal).
                         Ex. "diagonal(color=#116329,scale=1.3,dy=-5)"
--waves-file JSON        fichier {"waves": ["diagonal", "radial(invert=true)"]},
                         combiné avec --wave (fichier d'abord, CLI ensuite)
--no-fetch               utilise cache local, aucun appel API
```

Priorité token : `--token` > `GITHUB_TOKEN` > `GITHUB_DDCQ_READ` > cache seul.

## Thèmes

`--theme all` (défaut) écrit 5 fichiers : `--out` tel quel pour `dark-green` + suffixes `-blue`, `-dark-blue`, `-red`, `-dark-red` avant extension. `--theme X` écrit 1 seul fichier vers `--out` exact.

| Thème | Fond | Texte | NONE | L1 | L2 | L3 | L4 (= reflet vague défaut) |
|---|---|---|---|---|---|---|---|
| dark-green | transparent | `#1f2328` | `#eff2f5` | `#aceebb` | `#4ac26b` | `#2da44e` | `#116329` |
| blue (Winter light officiel) | transparent | `#1f2328` | `#eff2f5` | `#b6e3ff` | `#54aeff` | `#0969da` | `#0a3069` |
| dark-blue (Winter dark officiel) | `#0d1117` | `#e6edf3` | `#161b22` | `#0a3069` | `#0969da` | `#54aeff` | `#b6e3ff` |
| red | transparent | `#1f2328` | `#eff2f5` | `#ffebe9` | `#ffb3b0` | `#e94a3f` | `#a40e26` |
| dark-red | `#0d1117` | `#e6edf3` | `#161b22` | `#5c0a0e` | `#a40e26` | `#e94a3f` | `#ffb3b0` |

Règle couleur cases :
- `dark-green` (legacy) garde `color` API GitHub si présent → sortie Phase1 inchangée.
- autres thèmes mappent `contributionLevel` → palette (sinon vert API écraserait thème).
- légende `Less/More` suit palette thème.

## Animation vagues (moteur v2)

CSS pur, sans JS (compatible `<img>` README) : 1 `@keyframes wave{i}` par vague + `animation-delay` inline par case.

- Chaînage séquentiel : `--wave` répétable, offset vague N = somme durations+gaps précédentes.
- Keyframes par vague : `0%,14%,100%` = couleur origine, `7%` = reflet. Durée propre par vague (`duration`, défaut `4.5s`), `gap` après vague (défaut `1.0s`).
- `invert=true` = miroir délai (vague inverse), `direction` CSS séparé (`normal`, défaut).
- `prefers-reduced-motion: reduce` → animation coupée. Légende exclue, grille seule.
- `transform-box: fill-box; transform-origin: center` : zoom/lift centrés par case.

### Formes (`shape`, délai `f(wi,row)`)

| Forme | Formule | Params (défauts) |
|---|---|---|
| `diagonal` (défaut) | `wi*col + row*idx` | `col=35`, `row=65` |
| `linear` | `wi*step` (horizontale) | `step=80` |
| `radial` | `dist((wi,row),(cx,cy))*step` (ronde, centre grille) | `step=60`, `cx`/`cy` auto |
| `sine` (poisson) | `wi*step + sin(row*freq)*amp` | `step=80`, `freq=1.0`, `amp=120` |

### Params communs (toutes formes)

| Param | Défaut | Effet |
|---|---|---|
| `color` | max thème (`FOURTH_QUARTILE`) | reflet vague, ex. `color=#ff0000` |
| `scale` | `1.3` | zoom case au pic, `1` = désactive |
| `dy` | `-5` | translation Y px au pic, `0` = désactive |
| `duration` | `4.5` | secondes par cycle vague |
| `gap` | `1.0` | pause secondes après vague |
| `invert` | `false` | miroir sens propagation |
| `direction` | `normal` | direction CSS |

### Exemples vagues

```bash
# défaut : diagonale reflet max thème
PYTHONPATH=src python3 -m github_contrib --out contributions.svg --no-fetch

# vague rouge sans zoom ni lift (couleur seule)
PYTHONPATH=src python3 -m github_contrib --theme blue --out /tmp/blue.svg --no-fetch \
  --wave "diagonal(color=#ff0000,scale=1,dy=0)"

# chaînage : diagonale puis ronde inversée
PYTHONPATH=src python3 -m github_contrib --theme blue --out /tmp/chain.svg --no-fetch \
  --wave "diagonal(color=#0a3069)" --wave "radial(invert=true,duration=3)"

# poisson bleu, zoom fort
PYTHONPATH=src python3 -m github_contrib --theme blue --out /tmp/fish.svg --no-fetch \
  --wave "sine(color=#0a3069,scale=1.5,amp=200)"

# fichier JSON (même modèle, versionnable)
echo '{"waves": ["diagonal", "radial(invert=true,duration=3)"]}' > /tmp/waves.json
PYTHONPATH=src python3 -m github_contrib --out /tmp/j.svg --theme red --no-fetch \
  --waves-file /tmp/waves.json

# statique Phase1, tous thèmes
PYTHONPATH=src python3 -m github_contrib --out contributions.svg --no-fetch \
  --animate none --theme all
```

## Exemples

```bash
# tous thèmes + vague par défaut (recommandé local)
PYTHONPATH=src python3 -m github_contrib --login ddcq --out contributions.svg --no-fetch

# 1 seul thème bleu statique
PYTHONPATH=src python3 -m github_contrib --out /tmp/blue.svg --theme blue --animate none --no-fetch

# fetch frais puis cache
export GITHUB_TOKEN=ghp_...
PYTHONPATH=src python3 -m github_contrib --login ddcq --out contributions.svg
```

## Automation

Action `contributions` : schedule `0 6 * * *` + `workflow_dispatch`, `runs-on: ubuntu-24.04`, `actions/checkout@v6` + `actions/setup-python@v6` (runtime Node24). Génère les 5 SVG puis commit sur branche `bot/refresh-contributions` (jamais `main` direct) : merge manuel vers `main` après contrôle.

- Token : `github.token` par défaut (publiques). Privées incluses via secret `CONTRIB_PAT` (classic, scope `read:user`).
- Mise en route : `git push -u origin main`, puis onglet Actions.

## Tests

Stdlib seule, pas de dépendance. `pytest` absent par défaut : suite manuelle équivalente.

```bash
PYTHONPATH=src python3 -c "import tests.test_smoke as t; [getattr(t,k)() for k in dir(t) if k.startswith('test_')]"
```

Couverture : palette verrouillée, `none` sans style, injection style unique, délai diagonal, `--orig` = fill, thèmes enregistrés, mapping level vs API, reflet par thème, naming `theme_outputs`, palettes Winter officielles, fond sombre dark, couleur/zoom/lift custom.

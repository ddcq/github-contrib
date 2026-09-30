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
--wave-color #RRGGBB     couleur vague (défaut : FOURTH_QUARTILE du thème)
--wave-scale FLOAT       zoom case au pic (défaut 1.3, 1 = désactive zoom)
--wave-dy INT            translation Y px au pic (défaut -5, 0 = désactive lift)
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

## Animation vague

CSS pur, sans JS (compatible `<img>` README) : 1 `@keyframes wave` + `animation-delay` inline par case.

- Période `4.5s infinite`, flash ~600ms par case, pause résiduelle.
- Délai diagonal : `wi * 35ms + row * 65ms` (colonne + ligne → gauche→droite en biais).
- Keyframes : `0%,14%,100%` = couleur origine, `7%` = reflet.
- `prefers-reduced-motion: reduce` → animation coupée.
- Légende exclue, grille seule.

Personnalisation vague :

```bash
# vague rouge sur thème bleu, sans zoom ni lift (couleur seule)
PYTHONPATH=src python3 -m github_contrib --theme blue --out contributions-blue.svg --no-fetch \
  --wave-color "#ff0000" --wave-scale 1 --wave-dy 0

# zoom seul, lift désactivé
PYTHONPATH=src python3 -m github_contrib --theme red --out contributions-red.svg --no-fetch \
  --wave-scale 1.5 --wave-dy 0

# statique Phase1, tous thèmes
PYTHONPATH=src python3 -m github_contrib --out contributions.svg --no-fetch \
  --animate none --theme all
```

`transform-box: fill-box; transform-origin: center` : zoom/lift centrés par case.

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

Action `contributions` : schedule `0 6 * * *` + `workflow_dispatch`, `runs-on: ubuntu-24.04`, `actions/checkout@v6` + `actions/setup-python@v6` (runtime Node24), commit les 5 SVG sur `main`.

- Token : `github.token` par défaut (publiques). Privées incluses via secret `CONTRIB_PAT` (classic, scope `read:user`).
- Mise en route : `git push -u origin main`, puis onglet Actions.

## Tests

Stdlib seule, pas de dépendance. `pytest` absent par défaut : suite manuelle équivalente.

```bash
PYTHONPATH=src python3 -c "import tests.test_smoke as t; [getattr(t,k)() for k in dir(t) if k.startswith('test_')]"
```

Couverture : palette verrouillée, `none` sans style, injection style unique, délai diagonal, `--orig` = fill, thèmes enregistrés, mapping level vs API, reflet par thème, naming `theme_outputs`, palettes Winter officielles, fond sombre dark, couleur/zoom/lift custom.

# github-contrib

![contributions](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions.svg)

Calendrier de contributions GitHub généré depuis GraphQL `ContributionsCollection` (user `ddcq`), avec vague animée et 6 thèmes couleur.

| Thème | Fichier | Aperçu |
|---|---|---|
| dark-green (défaut) | `contributions.svg` | ![dark-green](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions.svg) |
| green (legacy) | `contributions-green.svg` | ![green](https://raw.githubusercontent.com/ddcq/github-contrib/main/contributions-green.svg) |
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
--theme {all,dark-green,green,blue,dark-blue,red,dark-red}
                         all (défaut) = 6 fichiers, sinon 1 seul vers --out
--wave SPEC              DSL vague, répétable pour chaînage (défaut diagonal).
                         Ex. "diagonal(color=#116329,scale=1.3,dy=-5)"
--waves-file JSON        fichier {"waves": ["diagonal", "radial(invert=true)"]},
                         combiné avec --wave (fichier d'abord, CLI ensuite)
--no-fetch               utilise cache local, aucun appel API
```

Priorité token : `--token` > `GITHUB_TOKEN` > `GITHUB_DDCQ_READ` > cache seul.

## Thèmes

`--theme all` (défaut) écrit 6 fichiers : `--out` tel quel pour `dark-green` + suffixes `-green`, `-blue`, `-dark-blue`, `-red`, `-dark-red` avant extension. `--theme X` écrit 1 seul fichier vers `--out` exact.

| Thème | Fond | Texte | NONE | L1 | L2 | L3 | L4 (= reflet vague défaut) |
|---|---|---|---|---|---|---|---|
| dark-green (défaut, GitHub dark officiel) | `#0d1117` | `#e6edf3` | `#161b22` | `#0e4429` | `#006d32` | `#26a641` | `#39d353` |
| green (legacy) | transparent | `#1f2328` | `#eff2f5` | `#aceebb` | `#4ac26b` | `#2da44e` | `#116329` |
| blue (Winter light officiel) | transparent | `#1f2328` | `#eff2f5` | `#b6e3ff` | `#54aeff` | `#0969da` | `#0a3069` |
| dark-blue (Winter dark officiel) | `#0d1117` | `#e6edf3` | `#161b22` | `#0a3069` | `#0969da` | `#54aeff` | `#b6e3ff` |
| red | transparent | `#1f2328` | `#eff2f5` | `#ffebe9` | `#ffb3b0` | `#e94a3f` | `#a40e26` |
| dark-red | `#0d1117` | `#e6edf3` | `#161b22` | `#5c0a0e` | `#a40e26` | `#e94a3f` | `#ffb3b0` |

Règle couleur cases :
- `green` (legacy) garde `color` API GitHub si présent → sortie Phase1 inchangée.
- autres thèmes mappent `contributionLevel` → palette (sinon vert API écraserait thème).
- légende `Less/More` suit palette thème.

## Animation vagues (moteur v2)

CSS pur, sans JS (compatible `<img>` README).

- 1 vague : `fill` case animé direct (look legacy).
- N vagues : 1 `@keyframes c{idx}` par case sur l'élément contribution lui-même, tranches séquentielles bouclées (N animations `fill` partagées se recouvrent : seule la dernière serait visible). Pics exacts par case : délai formé intégré aux pourcentages.
- `direction` honored 1 vague ; multi toujours `normal`.
- `animation-delay` inline par case = délai formé (`invert` inclus).

- Chaînage séquentiel en boucle : cycle total = somme durations+gaps, chaque vague occupe sa tranche puis boucle vers la première. `gap` = pause entre vagues (ex. config `waves.json` : cycle 33.5s).
- Keyframes par vague : tranche `[offset, offset+duration]`, pic à mi-tranche. 1 seule vague = look legacy (flash 7%/14%).
- Keyframes par vague : `0%,14%,100%` = couleur origine, `7%` = reflet. Durée propre par vague (`duration`, défaut `4.5s`), `gap` après vague (défaut `1.0s`).
- `invert=true` = miroir délai (vague inverse), `direction` CSS séparé (`normal`, défaut).
- `prefers-reduced-motion: reduce` → animation coupée (`!important` : le `animation` inline des cases l'outrankait). Légende exclue, grille seule.
- `transform-box: fill-box; transform-origin: center` : zoom/lift centrés par case.
- Paliers en `transform:none` (= identité, 14 o au lieu de 45), pourcentages à 1 décimale et nom de variable `--o` : −30% raw, −47% gzip. Ne jamais **omettre** `fill` ni `transform` d'un palier : Chrome vide la keyframe et reconstruit la rampe depuis 0% (crête aplatie).
- Transforms de pic hissés une fois en `:root` (`--t0`, `--t1`…) au lieu d'être répétés dans les 371 keyframes.
- **Offsets non décroissants obligatoires** : Chrome trie les keyframes par offset et garde le dernier en cas d'égalité. Le délai spatial est donc *normalisé* dans la largeur du slot (`offset + t·(duration+gap−duration)`) au lieu d'être ajouté tel quel : 0 chevauchement, 0 offset > 100%, 0 collision de crête. Vérifié par `test_multi_wave_offsets_monotonic_and_bounded`.
- Pas de `<title>` par case : Chrome repeint les nœuds texte avec le `fill` animé (24 → 24 fps sur un calendrier dense) et un SVG chargé via `<img>` n'affiche de toute façon aucun tooltip. Vérifié : tooltips absents à l'identique avec/sans.

### Mesures (thème dark-green, 53 semaines / 369 cases)

| | avant | après | gain |
|---|---|---|---|
| raw | 464 634 o | **322 179 o** | −30.7% |
| gzip-6 (ce que GitHub sert) | 27 557 o | **14 657 o** | −46.8% |

GitHub sert le SVG **compressé en gzip niveau 6** (Fastly, `vary: Accept-Encoding`, fichier servi tel quel). Mesurer en gzip-9 sous-estime d'environ 13% le poids réel sur le fil.

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
| `scale` | `1.3` | zoom case au pic, `1` = désactive. Le zoom part de l'horizon moyen (centre de la 4e ligne) : chaque ligne dérive de `(centre - 57) * (scale - 1)` |
| `dy` | `-5` | translation Y px au pic, identique sur toutes les lignes, `0` = désactive |
| `sy` | `1.0` | multiplicateur de l'écart à l'horizon, `0` = scale sans drift vertical |
| `rotate` | `0` | rotation degrés au pic : `90`, `-90`, `180`, `-180`, `270`, `-270`, `360`, `-360` (`0` = désactive) |
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

# poisson bleu, zoom fort + rotation 90° horaire
PYTHONPATH=src python3 -m github_contrib --theme blue --out /tmp/fish.svg --no-fetch \
  --wave "sine(color=#0a3069,scale=1.5,amp=200,rotate=90)"

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

Action `contributions` : schedule `0 6 * * *` + `workflow_dispatch`, `runs-on: ubuntu-24.04`, `actions/checkout@v6` + `actions/setup-python@v6` (runtime Node24). Génère les 6 SVG avec `--waves-file waves.json` (config versionnée : diagonale, radiale inversée +90°, poisson -90°, linéaire inversée alternate, diagonale inversée 180°, burst coin 360°) puis commit sur branche `bot/refresh-contributions` (jamais `main` direct) : merge manuel vers `main` après contrôle.

- Token : `github.token` par défaut (publiques). Privées incluses via secret `CONTRIB_PAT` (classic, scope `read:user`).
- Mise en route : `git push -u origin main`, puis onglet Actions.

## Tests

Stdlib seule, pas de dépendance. `pytest` absent par défaut : suite manuelle équivalente.

```bash
PYTHONPATH=src python3 -c "import tests.test_smoke as t; [getattr(t,k)() for k in dir(t) if k.startswith('test_')]"
```

Couverture : palette verrouillée, `none` sans style, injection style unique, délai diagonal, `--o` = fill, thèmes enregistrés, mapping level vs API, reflet par thème, naming `theme_outputs`, palettes Winter officielles, fond sombre dark, couleur/zoom/lift custom.

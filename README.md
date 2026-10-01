# github-contrib

![contributions](https://raw.githubusercontent.com/ddcq/github-contrib/main/assets/contributions.svg)

GitHub contribution calendar generated from GraphQL `ContributionsCollection` (user `ddcq`), with an animated wave and 6 colour themes.

| Theme | File | Preview |
|---|---|---|
| dark-green (default) | `assets/contributions.svg` | ![dark-green](https://raw.githubusercontent.com/ddcq/github-contrib/main/assets/contributions.svg) |
| green (legacy) | `assets/contributions-green.svg` | ![green](https://raw.githubusercontent.com/ddcq/github-contrib/main/assets/contributions-green.svg) |
| blue | `assets/contributions-blue.svg` | ![blue](https://raw.githubusercontent.com/ddcq/github-contrib/main/assets/contributions-blue.svg) |
| dark-blue | `assets/contributions-dark-blue.svg` | ![dark-blue](https://raw.githubusercontent.com/ddcq/github-contrib/main/assets/contributions-dark-blue.svg) |
| red | `assets/contributions-red.svg` | ![red](https://raw.githubusercontent.com/ddcq/github-contrib/main/assets/contributions-red.svg) |
| dark-red | `assets/contributions-dark-red.svg` | ![dark-red](https://raw.githubusercontent.com/ddcq/github-contrib/main/assets/contributions-dark-red.svg) |

## Requirements

- Python >= 3.11 (workflow: 3.13)
- GitHub token for the API fetch (otherwise `--no-fetch` + local cache `data/contributions.json`)

```bash
export GITHUB_TOKEN=...
PYTHONPATH=src python3 -m github_contrib --login ddcq --out assets/contributions.svg --no-fetch
```

## CLI options

```
--login LOGIN            GitHub user (default ddcq)
--out OUT                base file path (default assets/contributions.svg)
--cache CACHE            JSON cache (default data/contributions.json)
--from FROM_ISO          start bound (optional, ex. 2024-10-01T00:00:00Z)
--to TO_ISO              end bound (optional)
--token TOKEN            overrides GITHUB_TOKEN / GITHUB_DDCQ_READ
--animate {wave,none}    wave (default) or none = byte-identical static Phase1
--theme {all,dark-green,green,blue,dark-blue,red,dark-red}
                         all (default) = 6 files, otherwise 1 file at --out
--wave SPEC              wave DSL, repeatable for chaining (default diagonal).
                         Ex. "diagonal(color=#116329,scale=1.3,dy=-5)"
--waves-file JSON        file {"waves": ["diagonal", "radial(invert=true)"]},
                         combined with --wave (file first, CLI after)
--no-fetch               uses the local cache, no API call
```

Token priority: `--token` > `GITHUB_TOKEN` > `GITHUB_DDCQ_READ` > cache only.

## Themes

`--theme all` (default) writes 6 files: `--out` as-is for `dark-green` plus the `-green`, `-blue`, `-dark-blue`, `-red`, `-dark-red` suffixes before the extension. `--theme X` writes 1 file to the exact `--out` path.

| Theme | Background | Text | NONE | L1 | L2 | L3 | L4 (= default wave reflect) |
|---|---|---|---|---|---|---|---|
| dark-green (default, official GitHub dark) | `#0d1117` | `#e6edf3` | `#161b22` | `#0e4429` | `#006d32` | `#26a641` | `#39d353` |
| green (legacy) | transparent | `#1f2328` | `#eff2f5` | `#aceebb` | `#4ac26b` | `#2da44e` | `#116329` |
| blue (official Winter light) | transparent | `#1f2328` | `#eff2f5` | `#b6e3ff` | `#54aeff` | `#0969da` | `#0a3069` |
| dark-blue (official Winter dark) | `#0d1117` | `#e6edf3` | `#161b22` | `#0a3069` | `#0969da` | `#54aeff` | `#b6e3ff` |
| red | transparent | `#1f2328` | `#eff2f5` | `#ffebe9` | `#ffb3b0` | `#e94a3f` | `#a40e26` |
| dark-red | `#0d1117` | `#e6edf3` | `#161b22` | `#5c0a0e` | `#a40e26` | `#e94a3f` | `#ffb3b0` |

Cell colour rules:
- `green` (legacy) keeps the GitHub API `color` when present, so Phase1 output is unchanged.
- other themes map `contributionLevel` to the palette (otherwise the green API colour would override the theme).
- the `Less/More` legend follows the theme palette.

## Wave animation (engine v2)

Pure CSS, no JS (works in a README `<img>`).

- 1 wave: animates the cell `fill` directly (legacy look).
- N waves: 1 `@keyframes c{idx}` per cell on the contribution element itself, sequential looping slices (N shared `fill` animations on the same element overlap: only the last would be visible). Exact per-cell peaks: the shaped delay is baked into the percentages.
- `direction` is honoured for 1 wave; always `normal` for multi.

- Sequential looping chain: total cycle = sum of durations+gaps, each wave takes its slice then loops back to the first. `gap` = pause between waves (ex. `waves.json` config: 33.5s cycle).
- Keyframes per wave: slice `[offset, offset+duration]`, peak at mid-slice. A single wave = legacy look (7%/14% flash).
- Keyframes per wave: `0%,14%,100%` = base colour, `7%` = reflect. Per-wave duration (`duration`, default `4.5s`), `gap` after the wave (default `1.0s`).
- `invert=true` = mirrored delay (wave runs backwards), `direction` is a separate CSS property (`normal`, default).
- `prefers-reduced-motion: reduce` -> animation cut off (`!important`: the per-cell inline `animation` used to outrank it). Legend excluded, grid only.
- `transform-box: fill-box; transform-origin: center`: zoom/lift centred per cell.
- Stops use `transform:none` (= identity, 14 bytes instead of 45), percentages to 1 decimal and the `--o` variable name: -30% raw, -47% gzip. Never **omit** `fill` or `transform` from a stop: Chrome empties the keyframe rule and rebuilds the ramp from 0% (flattened peak).
- Peak transforms hoisted once into `:root` (`--t0`, `--t1`, ...) instead of being repeated across the 371 keyframes.
- **Non-decreasing offsets are mandatory**: Chrome sorts keyframes by offset and keeps the last one on ties. The spatial delay is therefore *normalised* into the slot width (`offset + t*(duration+gap-duration)`) instead of being added as-is: 0 overlap, 0 offset > 100%, 0 peak collision. Verified by `test_multi_wave_offsets_monotonic_and_bounded`.
- No per-cell `<title>`: Chrome repaints the text nodes with the animated `fill` (24 -> 24 fps on a dense calendar), and an SVG loaded through `<img>` shows no tooltip anyway. Verified: tooltips absent either way.

### Measurements (dark-green theme, 53 weeks / 369 cells)

| | before | after | gain |
|---|---|---|---|
| raw | 464,634 bytes | **322,179 bytes** | -30.7% |
| gzip-6 (what GitHub serves) | 27,557 bytes | **14,657 bytes** | -46.8% |

GitHub serves the SVG **gzipped at level 6** (Fastly, `vary: Accept-Encoding`, file served as-is). Measuring at gzip-9 underestimates the real on-the-wire weight by about 13%.

### Shapes (`shape`, delay `f(wi,row)`)

| Shape | Formula | Params (defaults) |
|---|---|---|
| `diagonal` (default) | `wi*col + row*idx` | `col=35`, `row=65` |
| `linear` | `wi*step` (horizontal) | `step=80` |
| `radial` | `dist((wi,row),(cx,cy))*step` (round, grid centre) | `step=60`, `cx`/`cy` auto |
| `sine` (fish) | `wi*step + sin(row*freq)*amp` | `step=80`, `freq=1.0`, `amp=120` |

### Common params (all shapes)

| Param | Default | Effect |
|---|---|---|
| `color` | theme max (`FOURTH_QUARTILE`) | wave reflect, ex. `color=#ff0000` |
| `scale` | `1.3` | cell zoom at the peak, `1` = disabled. The zoom pivots on the mean horizon (centre of the 4th row): each row drifts by `(centre - 57) * (scale - 1)` |
| `dy` | `-5` | Y translation in px at the peak, identical on every row, `0` = disabled |
| `sy` | `1.0` | multiplier on the distance to the horizon, `0` = scale without vertical drift |
| `rotate` | `0` | rotation in degrees at the peak: `90`, `-90`, `180`, `-180`, `270`, `-270`, `360`, `-360` (`0` = disabled) |
| `duration` | `4.5` | seconds per wave cycle |
| `gap` | `1.0` | pause in seconds after the wave |
| `invert` | `false` | mirrors the propagation direction |
| `direction` | `normal` | CSS direction |

### Wave examples

```bash
# default: diagonal with the theme max reflect
PYTHONPATH=src python3 -m github_contrib --out assets/contributions.svg --no-fetch

# red wave without zoom or lift (colour only)
PYTHONPATH=src python3 -m github_contrib --theme blue --out /tmp/blue.svg --no-fetch \
  --wave "diagonal(color=#ff0000,scale=1,dy=0)"

# chain: diagonal then inverted round
PYTHONPATH=src python3 -m github_contrib --theme blue --out /tmp/chain.svg --no-fetch \
  --wave "diagonal(color=#0a3069)" --wave "radial(invert=true,duration=3)"

# blue fish, strong zoom + 90 degree clockwise rotation
PYTHONPATH=src python3 -m github_contrib --theme blue --out /tmp/fish.svg --no-fetch \
  --wave "sine(color=#0a3069,scale=1.5,amp=200,rotate=90)"

# JSON file (same schema, versionable)
echo '{"waves": ["diagonal", "radial(invert=true,duration=3)"]}' > /tmp/waves.json
PYTHONPATH=src python3 -m github_contrib --out /tmp/j.svg --theme red --no-fetch \
  --waves-file /tmp/waves.json

# static Phase1, all themes
PYTHONPATH=src python3 -m github_contrib --out assets/contributions.svg --no-fetch \
  --animate none --theme all
```

## Examples

```bash
# all themes + default wave (recommended locally)
PYTHONPATH=src python3 -m github_contrib --login ddcq --out assets/contributions.svg --no-fetch

# 1 static blue theme
PYTHONPATH=src python3 -m github_contrib --out /tmp/blue.svg --theme blue --animate none --no-fetch

# fresh fetch then cache
export GITHUB_TOKEN=ghp_...
PYTHONPATH=src python3 -m github_contrib --login ddcq --out assets/contributions.svg
```

## Automation

`contributions` action: schedule `0 6 * * *` + `workflow_dispatch`, `runs-on: ubuntu-24.04`, `actions/checkout@v6` + `actions/setup-python@v6` (Node24 runtime). Generates the 6 SVGs with `--waves-file waves.json` (versioned config: diagonal, inverted radial +90, fish -90, alternating inverted linear, inverted diagonal 180, corner burst 360) then commits on the `bot/refresh-contributions` branch (never `main` directly): manual merge into `main` after review.

- Token: `github.token` by default (public data). Private contributions included via the `CONTRIB_PAT` secret (classic, `read:user` scope).
- The bot branch is reset to `origin/main` on every run, so it only ever carries one SVG commit. Manual merge into `main` after review.
- Getting started: `git push -u origin main`, then the Actions tab.

## Tests

Stdlib only, no dependencies. `pytest` is not installed by default: equivalent manual run below.

```bash
PYTHONPATH=src python3 -c "import tests.test_smoke as t; [getattr(t,k)() for k in dir(t) if k.startswith('test_')]"
```

Coverage: locked palette, `none` without style, single style injection, diagonal delay, `--o` = fill, registered themes, level vs API mapping, per-theme reflect, `theme_outputs` naming, official Winter palettes, dark background, custom colour/zoom/lift.
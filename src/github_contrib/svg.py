"""Generateur SVG pixel-proche du calendrier GitHub light mode."""

# Palette Primer light verrouillee (ticket 02)
PALETTE = {
    "NONE": "#eff2f5",
    "FIRST_QUARTILE": "#aceebb",
    "SECOND_QUARTILE": "#4ac26b",
    "THIRD_QUARTILE": "#2da44e",
    "FOURTH_QUARTILE": "#116329",
}

CELL = 10
GAP = 3
PITCH = CELL + GAP
RX = 2


"""Generateur SVG pixel-proche du calendrier GitHub light mode."""

from dataclasses import dataclass, field
from datetime import date
from xml.sax.saxutils import escape
import math
import re

# Palette Primer light verrouillee (ticket 02)
PALETTE = {
    "NONE": "#eff2f5",
    "FIRST_QUARTILE": "#aceebb",
    "SECOND_QUARTILE": "#4ac26b",
    "THIRD_QUARTILE": "#2da44e",
    "FOURTH_QUARTILE": "#116329",
}

CELL = 10
GAP = 3
PITCH = CELL + GAP
RX = 2
MONTH_H = 13
GUTTER_W = 28
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHS_FULL = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
DAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}


def _ordinal(n):
    if 10 <= n % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def tooltip(day_date, count):
    """Texte tooltip facon GitHub : 'N contributions on October 13th.'."""
    full = f"{MONTHS_FULL[day_date.month - 1]} {day_date.day}{_ordinal(day_date.day)}"
    if count == 0:
        return f"No contributions on {full}."
    if count == 1:
        return f"1 contribution on {full}."
    return f"{count} contributions on {full}."


THEMES = {
    "green": {
        "NONE": "#eff2f5",
        "FIRST_QUARTILE": "#aceebb",
        "SECOND_QUARTILE": "#4ac26b",
        "THIRD_QUARTILE": "#2da44e",
        "FOURTH_QUARTILE": "#116329",
    },
    "dark-green": {
        "NONE": "#161b22",
        "FIRST_QUARTILE": "#0e4429",
        "SECOND_QUARTILE": "#006d32",
        "THIRD_QUARTILE": "#26a641",
        "FOURTH_QUARTILE": "#39d353",
    },
    "blue": {
        "NONE": "#eff2f5",
        "FIRST_QUARTILE": "#b6e3ff",
        "SECOND_QUARTILE": "#54aeff",
        "THIRD_QUARTILE": "#0969da",
        "FOURTH_QUARTILE": "#0a3069",
    },
    "dark-blue": {
        "NONE": "#161b22",
        "FIRST_QUARTILE": "#0a3069",
        "SECOND_QUARTILE": "#0969da",
        "THIRD_QUARTILE": "#54aeff",
        "FOURTH_QUARTILE": "#b6e3ff",
    },
    "red": {
        "NONE": "#eff2f5",
        "FIRST_QUARTILE": "#ffebe9",
        "SECOND_QUARTILE": "#ffb3b0",
        "THIRD_QUARTILE": "#e94a3f",
        "FOURTH_QUARTILE": "#a40e26",
    },
    "dark-red": {
        "NONE": "#161b22",
        "FIRST_QUARTILE": "#5c0a0e",
        "SECOND_QUARTILE": "#a40e26",
        "THIRD_QUARTILE": "#e94a3f",
        "FOURTH_QUARTILE": "#ffb3b0",
    },
}

# Fond + texte par theme (standard GitHub light/dark).
THEME_BG = {
    "green": None,
    "blue": None,
    "red": None,
    "dark-green": "#0d1117",
    "dark-blue": "#0d1117",
    "dark-red": "#0d1117",
}

THEME_FG = {
    "green": "#1f2328",
    "blue": "#1f2328",
    "red": "#1f2328",
    "dark-green": "#e6edf3",
    "dark-blue": "#e6edf3",
    "dark-red": "#e6edf3",
}

THEME_NAMES = ["dark-green", "green", "blue", "dark-blue", "red", "dark-red"]


def _parse_day(d, palette=None, keep_api=True):
    day_date = date.fromisoformat(d["date"])
    count = int(d.get("contributionCount", 0))
    level = d.get("contributionLevel", "NONE")
    pal = palette or PALETTE
    if keep_api and d.get("color"):
        color = d["color"]
    else:
        color = pal.get(level, pal["NONE"])
    return day_date, count, color


WAVE_REFLECT = "#116329"
WAVE_DURATION = "4.5s"
WAVE_DELAY_COL = 35
WAVE_DELAY_ROW = 65

WAVE_COMMON_KEYS = {"color", "scale", "dy", "rotate", "duration", "gap",
                    "invert", "direction"}

WAVE_ROTATIONS = {0, 90, -90, 180, -180, 270, -270, 360, -360}


def _shape_linear(wi, row, n_weeks, p):
    return wi * float(p.get("step", 80))


def _shape_diagonal(wi, row, n_weeks, p):
    return wi * float(p.get("col", WAVE_DELAY_COL)) + row * float(p.get("row", WAVE_DELAY_ROW))


def _shape_radial(wi, row, n_weeks, p):
    cx = float(p.get("cx", (n_weeks - 1) / 2))
    cy = float(p.get("cy", 3))
    return math.dist((wi, row), (cx, cy)) * float(p.get("step", 60))


def _shape_sine(wi, row, n_weeks, p):
    return (wi * float(p.get("step", 80))
            + math.sin(row * float(p.get("freq", 1.0))) * float(p.get("amp", 120)))


SHAPES = {
    "linear": _shape_linear,
    "diagonal": _shape_diagonal,
    "radial": _shape_radial,
    "sine": _shape_sine,
}


@dataclass
class WaveSpec:
    shape: str = "diagonal"
    color: str | None = None
    scale: float = 1.3
    dy: int = -5
    rotate: int = 0
    duration: float = 4.5
    gap: float = 1.0
    invert: bool = False
    direction: str = "normal"
    params: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.shape not in SHAPES:
            raise ValueError(f"Forme inconnue: {self.shape} (choix: {sorted(SHAPES)})")
        if self.rotate not in WAVE_ROTATIONS:
            raise ValueError(f"Rotation invalide: {self.rotate} (choix: {sorted(WAVE_ROTATIONS)})")


DEFAULT_WAVES = [WaveSpec()]


def _parse_value(v):
    v = v.strip().strip('"\'')
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


_SPEC_RE = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*(?:\((.*)\))?\s*$", re.DOTALL)


def parse_wave_spec(spec):
    """Parse DSL `shape(k=v,...)` -> WaveSpec. Ex: `diagonal(color=#ff0000,invert=true)`."""
    if isinstance(spec, WaveSpec):
        return spec
    m = _SPEC_RE.match(spec)
    if not m:
        raise ValueError(f"Spec vague invalide: {spec!r}")
    shape, body = m.group(1), m.group(2)
    if shape not in SHAPES:
        raise ValueError(f"Forme inconnue: {shape} (choix: {sorted(SHAPES)})")
    common, params = {}, {}
    if body and body.strip():
        for chunk in body.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" not in chunk:
                raise ValueError(f"Param sans '=' dans {spec!r}: {chunk!r}")
            k, v = chunk.split("=", 1)
            k, v = k.strip(), _parse_value(v)
            (common if k in WAVE_COMMON_KEYS else params)[k] = v
    return WaveSpec(shape=shape, params=params, **common)


def wave_delays(wave, n_weeks):
    """Delais ms (wi,row) pour une vague sur grille n_weeks x 7."""
    fn = SHAPES[wave.shape]
    grid = {(wi, row): fn(wi, row, n_weeks, wave.params)
            for wi in range(n_weeks) for row in range(7)}
    if wave.invert:
        top = max(grid.values()) if grid else 0
        grid = {k: top - v for k, v in grid.items()}
    return grid


def _wave_frame(i, reflect, scale, dy, rotate, marks):
    """Un @keyframes wave{i} pour 1 vague seule. marks=None (look legacy)."""
    peak = "" if (scale == 1 and dy == 0 and rotate == 0) else \
        f"transform:scale({scale:g}) translateY({dy}px) rotate({rotate}deg);"
    return (
        f"@keyframes wave{i}{{0%,14%,100%{{fill:var(--orig);transform:none}}"
        f"7%{{fill:{reflect};{peak}}}}}"
    )


def _cell_frame(idx, stops):
    """Un @keyframes cell{idx} multi-vagues (pics tranches sur la case)."""
    return f"@keyframes cell{idx}{{{''.join(stops)}}}"


def _stop(pct, fill, scale, dy, rotate, peak):
    # `transform:none` vaut l'identite explicite (verifie : memes matrices
    # de transformation) et evite 31 octets de `scale(1) translateY(0)`.
    # Ne jamais omettre la propriete : Chrome vide alors la cle de
    # keyframe et reconstruit la rampe depuis 0% (crête aplatie).
    tf = "" if (peak and scale == 1 and dy == 0 and rotate == 0) else (
        f"transform:scale({scale:g}) translateY({dy}px) rotate({rotate}deg);"
        if peak else "transform:none;")
    return f"{pct:.4g}%{{fill:{fill};{tf}}}"


def waves_css(waves, palette, n_weeks=0):
    """Bloc <style> : animations vague sur les cases elles-memes.

    1 vague : anime fill direct (look legacy). N vagues : 1 @keyframes
    cell{idx} par case, tranches sequentielles bouclees (N animations
    fill sur meme element se recouvrent : seule la derniere serait
    visible, d'ou un seul keyframes par case).
    Cycle total boucle sum(durations+gaps). Direction multi = normal.
    """
    if len(waves) == 1:
        wave = waves[0]
        reflect = wave.color or palette["FOURTH_QUARTILE"]
        head = (f".cell-wave{{animation:wave0 {wave.duration:g}s "
                f"{wave.direction} infinite;"
                "transform-box:fill-box;transform-origin:center;}")
        frames = [_wave_frame(0, reflect, wave.scale, wave.dy,
                              wave.rotate, None)]
    else:
        total = sum((w.duration + w.gap) * 1000 for w in waves)
        offsets = wave_offsets(waves)
        grids = [wave_delays(w, n_weeks) for w in waves]
        head = ".cell-wave{transform-box:fill-box;transform-origin:center;}"
        frames = []
        for wi in range(n_weeks):
            for row in range(7):
                idx = wi * 7 + row
                stops = [_stop(0, "var(--orig)", 1, 0, 0, False)]
                for i, wave in enumerate(waves):
                    reflect = wave.color or palette["FOURTH_QUARTILE"]
                    # Chrome trie les keyframes par offset et garde le
                    # dernier en cas d'egalite : le decalage spatial est
                    # normalise dans la largeur du slot au lieu d'etre
                    # ajoute tel quel, sinon une vague deborde sur la
                    # suivante (offset > 100%) et une crete peut se faire
                    # ecraser par le stop 100%.
                    g = grids[i]
                    gmin, gmax = min(g.values()), max(g.values())
                    t = (g[(wi, row)] - gmin) / (gmax - gmin) if gmax > gmin \
                        else 0.0
                    base = offsets[i] + t * (wave.gap * 1000)
                    stops.append(_stop(base / total * 100, "var(--orig)",
                                       wave.scale, wave.dy, wave.rotate, False))
                    stops.append(_stop((base + wave.duration * 500) / total * 100,
                                       reflect, wave.scale, wave.dy,
                                       wave.rotate, True))
                    stops.append(_stop((base + wave.duration * 1000) / total * 100,
                                       "var(--orig)", wave.scale, wave.dy,
                                       wave.rotate, False))
                stops.append(_stop(100, "var(--orig)", 1, 0, 0, False))
                frames.append(_cell_frame(idx, stops))
    return (
        "<style>" + head + "".join(frames) +
        "@media (prefers-reduced-motion: reduce){.cell-wave{animation:none!important;}}"
        "</style>"
    )


def wave_offsets(waves):
    """Offset ms demarrage chaque vague (cumul durations+gaps)."""
    offsets, cursor = [], 0.0
    for wave in waves:
        offsets.append(cursor)
        cursor += (wave.duration + wave.gap) * 1000
    return offsets


def calendar_to_svg(weeks, animate="wave", theme="dark-green", waves=None):
    """Convertit weeks (liste de {contributionDays:[...]}) en str SVG."""
    palette = THEMES.get(theme, THEMES["dark-green"])
    bg = THEME_BG.get(theme)
    fg = THEME_FG.get(theme, "#1f2328")
    # Theme green garde couleur API (identique palette legacy).
    # Autres themes mappent level -> palette (sinon API verte écrase theme).
    keep_api = (theme == "green")
    wave_list = [parse_wave_spec(w) for w in waves] if waves else DEFAULT_WAVES
    n_weeks = len(weeks)
    grid_w = n_weeks * PITCH + GAP
    grid_h = 7 * PITCH + GAP
    legend_h = 22
    width = GUTTER_W + grid_w
    height = MONTH_H + grid_h + legend_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'font-family="{FONT}" role="img" aria-label="Contribution calendar">'
    ]

    if animate == "wave":
        parts.append(waves_css(wave_list, palette, n_weeks))
        multi = len(wave_list) > 1
        total_s = sum((w.duration + w.gap) for w in wave_list) if multi else 0

    if bg:
        parts.append(f'<rect width="{width}" height="{height}" fill="{bg}"/>')

    # Labels mois : premier week ou le mois change
    seen_month = None
    for wi, week in enumerate(weeks):
        days = week.get("contributionDays", week) if isinstance(week, dict) else week
        if not days:
            continue
        first = date.fromisoformat(days[0]["date"])
        if first.month != seen_month and not (wi > 0 and first.month == seen_month):
            # evite doublons : label seulement au changement de mois
            if first.month != seen_month:
                x = GUTTER_W + wi * PITCH
                parts.append(
                    f'<text x="{x}" y="10" font-size="10" fill="{fg}">'
                    f"{MONTHS[first.month - 1]}</text>"
                )
                seen_month = first.month

    # Labels jours Mon/Wed/Fri
    for row, label in DAY_LABELS.items():
        y = MONTH_H + row * PITCH + CELL - 1
        parts.append(
            f'<text x="0" y="{y}" font-size="9" fill="{fg}">{label}</text>'
        )

    # Cellules
    for wi, week in enumerate(weeks):
        days = week.get("contributionDays", week) if isinstance(week, dict) else week
        for day in days:
            day_date, count, color = _parse_day(day, palette, keep_api)
            # ligne = weekday GitHub (dimanche=0) ; fromisoformat.weekday() lundi=0
            row = (day_date.weekday() + 1) % 7
            x = GUTTER_W + wi * PITCH
            y = MONTH_H + row * PITCH
            tip = escape(tooltip(day_date, count))
            if animate == "wave" and not multi:
                wave = wave_list[0]
                delay = wave_delays(wave, n_weeks)[(wi, row)]
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" '
                    f'fill="{color}" class="cell-wave" '
                    f'style="--orig:{color};animation-delay:{delay:g}ms" '
                    f'data-date="{day_date.isoformat()}" '
                    f'data-count="{count}"><title>{tip}</title></rect>'
                )
            elif animate == "wave":
                idx = wi * 7 + row
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" '
                    f'fill="{color}" class="cell-wave" '
                    f'style="--orig:{color};animation:cell{idx} {total_s:g}s '
                    f'normal infinite" '
                    f'data-date="{day_date.isoformat()}" '
                    f'data-count="{count}"><title>{tip}</title></rect>'
                )
            else:
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" '
                    f'fill="{color}" data-date="{day_date.isoformat()}" '
                    f'data-count="{count}"><title>{tip}</title></rect>'
                )

    # Legende Less + 5 niveaux + More
    ly = MONTH_H + grid_h + 6
    lx = width - (4 * len("Less More") + 5 * PITCH + 30)
    lx = max(GUTTER_W, lx)
    parts.append(
        f'<text x="{lx}" y="{ly + 9}" font-size="10" fill="{fg}">Less</text>'
    )
    lx += 30
    for level in ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE",
                  "THIRD_QUARTILE", "FOURTH_QUARTILE"]:
        parts.append(
            f'<rect x="{lx}" y="{ly}" width="{CELL}" height="{CELL}" '
            f'rx="{RX}" fill="{palette[level]}"/>'
        )
        lx += PITCH
    parts.append(
        f'<text x="{lx}" y="{ly + 9}" font-size="10" fill="{fg}">More</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"

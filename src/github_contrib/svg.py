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

from datetime import date
from xml.sax.saxutils import escape

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
    "dark-green": {
        "NONE": "#eff2f5",
        "FIRST_QUARTILE": "#aceebb",
        "SECOND_QUARTILE": "#4ac26b",
        "THIRD_QUARTILE": "#2da44e",
        "FOURTH_QUARTILE": "#116329",
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
    "dark-green": None,
    "blue": None,
    "red": None,
    "dark-blue": "#0d1117",
    "dark-red": "#0d1117",
}

THEME_FG = {
    "dark-green": "#1f2328",
    "blue": "#1f2328",
    "red": "#1f2328",
    "dark-blue": "#e6edf3",
    "dark-red": "#e6edf3",
}

THEME_NAMES = ["dark-green", "blue", "dark-blue", "red", "dark-red"]


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

def wave_css(reflect, scale=1.3, dy=-5):
    base = (
        "<style>"
        ".cell-wave{animation:wave " + WAVE_DURATION + " infinite;"
        "transform-box:fill-box;transform-origin:center;}"
    )
    if scale == 1 and dy == 0:
        return (
            base
            + "@keyframes wave{0%,14%,100%{fill:var(--orig);}"
            "7%{fill:" + reflect + ";}}"
            "@media (prefers-reduced-motion: reduce){.cell-wave{animation:none;}}"
            "</style>"
        )
    return (
        base
        + "@keyframes wave{0%,14%,100%{fill:var(--orig);"
        "transform:scale(1) translateY(0);}"
        "7%{fill:" + reflect + ";"
        f"transform:scale({scale:g}) translateY({dy}px);}}"
        "@media (prefers-reduced-motion: reduce){.cell-wave{animation:none;}}"
        "</style>"
    )


WAVE_CSS = wave_css(WAVE_REFLECT)


def calendar_to_svg(weeks, animate="wave", theme="dark-green",
                    wave_color=None, wave_scale=1.3, wave_dy=-5):
    """Convertit weeks (liste de {contributionDays:[...]}) en str SVG."""
    palette = THEMES.get(theme, THEMES["dark-green"])
    reflect = wave_color or palette["FOURTH_QUARTILE"]
    bg = THEME_BG.get(theme)
    fg = THEME_FG.get(theme, "#1f2328")
    # Legacy dark-green garde couleur API pour compat byte-identique Phase1.
    # Autres themes mappent level -> palette (sinon API verte écrase theme).
    keep_api = (theme == "dark-green")
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
        parts.append(wave_css(reflect, wave_scale, wave_dy))

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
            if animate == "wave":
                delay = wi * WAVE_DELAY_COL + row * WAVE_DELAY_ROW
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" '
                    f'fill="{color}" class="cell-wave" '
                    f'style="--orig:{color};animation-delay:{delay}ms" '
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

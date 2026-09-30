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


def _parse_day(d):
    day_date = date.fromisoformat(d["date"])
    count = int(d.get("contributionCount", 0))
    level = d.get("contributionLevel", "NONE")
    color = d.get("color") or PALETTE.get(level, PALETTE["NONE"])
    return day_date, count, color


def calendar_to_svg(weeks):
    """Convertit weeks (liste de {contributionDays:[...]}) en str SVG."""
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
                    f'<text x="{x}" y="10" font-size="10" fill="#1f2328">'
                    f"{MONTHS[first.month - 1]}</text>"
                )
                seen_month = first.month

    # Labels jours Mon/Wed/Fri
    for row, label in DAY_LABELS.items():
        y = MONTH_H + row * PITCH + CELL - 1
        parts.append(
            f'<text x="0" y="{y}" font-size="9" fill="#1f2328">{label}</text>'
        )

    # Cellules
    for wi, week in enumerate(weeks):
        days = week.get("contributionDays", week) if isinstance(week, dict) else week
        for day in days:
            day_date, count, color = _parse_day(day)
            # ligne = weekday GitHub (dimanche=0) ; fromisoformat.weekday() lundi=0
            row = (day_date.weekday() + 1) % 7
            x = GUTTER_W + wi * PITCH
            y = MONTH_H + row * PITCH
            tip = escape(tooltip(day_date, count))
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
        f'<text x="{lx}" y="{ly + 9}" font-size="10" fill="#1f2328">Less</text>'
    )
    lx += 30
    for level in ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE",
                  "THIRD_QUARTILE", "FOURTH_QUARTILE"]:
        parts.append(
            f'<rect x="{lx}" y="{ly}" width="{CELL}" height="{CELL}" '
            f'rx="{RX}" fill="{PALETTE[level]}"/>'
        )
        lx += PITCH
    parts.append(
        f'<text x="{lx}" y="{ly + 9}" font-size="10" fill="#1f2328">More</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"

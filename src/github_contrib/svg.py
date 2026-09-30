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


def calendar_to_svg(weeks):
    """Convertit weeks (liste de listes de days) en str SVG."""
    raise NotImplementedError

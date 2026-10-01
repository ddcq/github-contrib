from github_contrib import svg


def test_palette_locked():
    assert svg.PALETTE["NONE"] == "#eff2f5"
    assert svg.PITCH == 13


def _weeks():
    return [
        {"contributionDays": [
            {"date": "2026-09-28", "contributionCount": 0,
             "contributionLevel": "NONE"},
            {"date": "2026-09-29", "contributionCount": 3,
             "contributionLevel": "SECOND_QUARTILE"},
        ]},
        {"contributionDays": [
            {"date": "2026-10-05", "contributionCount": 1,
             "contributionLevel": "FIRST_QUARTILE"},
        ]},
    ]


def test_none_matches_legacy_static():
    out = svg.calendar_to_svg(_weeks(), animate="none", theme="green")
    assert "cell-wave" not in out
    assert "<style>" not in out
    assert 'fill="#eff2f5"' in out


def test_wave_injects_style_once():
    out = svg.calendar_to_svg(_weeks(), animate="wave", theme="green")
    assert out.count("<style>") == 1
    assert "@keyframes wave0" in out
    assert "prefers-reduced-motion" in out
    assert svg.WAVE_REFLECT in out
    assert "scale(1.3)" in out
    assert "translateY(-5px)" in out
    assert "transform-box:fill-box" in out


def test_wave_delay_diagonal():
    out = svg.calendar_to_svg(_weeks(), animate="wave", theme="green")
    # wi=0,row=1 (lundi 28/09) -> 0*35+1*65=65 ; wi=0,row=2 -> 130
    assert "--orig:#eff2f5;animation-delay:65ms" in out
    assert "animation-delay:130ms" in out
    # wi=1,row=1 (lundi 05/10) -> 1*35+1*65=100
    assert "animation-delay:100ms" in out


def test_wave_orig_matches_fill():
    out = svg.calendar_to_svg(_weeks(), animate="wave", theme="green")
    assert 'fill="#eff2f5" class="cell-wave" style="--orig:#eff2f5;' in out


def test_themes_registered():
    assert svg.THEME_NAMES == ["dark-green", "green", "blue", "dark-blue", "red", "dark-red"]
    for name in svg.THEME_NAMES:
        pal = svg.THEMES[name]
        assert set(pal) == {"NONE", "FIRST_QUARTILE", "SECOND_QUARTILE",
                            "THIRD_QUARTILE", "FOURTH_QUARTILE"}


def _weeks_with_api_color():
    return [{"contributionDays": [
        {"date": "2026-09-29", "contributionCount": 3,
         "contributionLevel": "FIRST_QUARTILE", "color": "#116329"},
    ]}]


def test_dark_green_keeps_api_color():
    out = svg.calendar_to_svg(_weeks_with_api_color(), animate="none",
                              theme="green")
    assert 'fill="#116329"' in out


def test_dark_green_default_dark():
    pal = svg.THEMES["dark-green"]
    assert pal["NONE"] == "#161b22"
    assert pal["FOURTH_QUARTILE"] == "#39d353"
    out = svg.calendar_to_svg(_weeks_with_api_color(), animate="none",
                              theme="dark-green")
    assert 'fill="#116329"' not in out
    assert 'fill="#0d1117"' in out
    assert 'fill="#e6edf3"' in out


def test_blue_maps_level_not_api():
    out = svg.calendar_to_svg(_weeks_with_api_color(), animate="none",
                              theme="blue")
    assert svg.THEMES["blue"]["FIRST_QUARTILE"] in out
    assert 'fill="#116329"' not in out


def test_theme_reflect_per_theme():
    blue = svg.calendar_to_svg(_weeks(), animate="wave", theme="blue")
    red = svg.calendar_to_svg(_weeks(), animate="wave", theme="red")
    assert svg.THEMES["blue"]["FOURTH_QUARTILE"] in blue
    assert svg.THEMES["red"]["FOURTH_QUARTILE"] in red


def test_theme_outputs_naming():
    from github_contrib.cli import theme_outputs
    outs = theme_outputs("contributions.svg", "all")
    assert [n for n, _ in outs] == svg.THEME_NAMES
    paths = [p for _, p in outs]
    assert paths[0] == "contributions.svg"
    assert "contributions-green.svg" in paths
    assert "contributions-blue.svg" in paths
    assert "contributions-dark-blue.svg" in paths
    assert "contributions-red.svg" in paths
    assert "contributions-dark-red.svg" in paths
    single = theme_outputs("out.svg", "blue")
    assert single == [("blue", "out.svg")]


def test_winter_blue_official_light():
    assert svg.THEMES["blue"]["FIRST_QUARTILE"] == "#b6e3ff"
    assert svg.THEMES["blue"]["FOURTH_QUARTILE"] == "#0a3069"


def test_dark_blue_winter_dark():
    pal = svg.THEMES["dark-blue"]
    assert pal["NONE"] == "#161b22"
    assert pal["FIRST_QUARTILE"] == "#0a3069"
    assert pal["FOURTH_QUARTILE"] == "#b6e3ff"
    out = svg.calendar_to_svg(_weeks(), animate="none", theme="dark-blue")
    assert 'fill="#0d1117"' in out
    assert 'fill="#e6edf3"' in out
    assert 'fill="#1f2328"' not in out


def test_dark_red_dark_bg():
    pal = svg.THEMES["dark-red"]
    assert pal["NONE"] == "#161b22"
    out = svg.calendar_to_svg(_weeks(), animate="none", theme="dark-red")
    assert 'fill="#0d1117"' in out
    assert 'fill="#e6edf3"' in out


def test_light_themes_no_bg():
    out = svg.calendar_to_svg(_weeks(), animate="none", theme="blue")
    assert "#0d1117" not in out
    assert 'fill="#1f2328"' in out


def test_wave_custom_color():
    out = svg.calendar_to_svg(_weeks(), animate="wave", theme="blue",
                              waves=["diagonal(color=#ff0000)"])
    assert "#ff0000" in out
    assert svg.THEMES["blue"]["FOURTH_QUARTILE"] not in out.split("<style>")[1].split("</style>")[0]


def test_wave_zoom_lift_optional():
    plain = svg.calendar_to_svg(_weeks(), animate="wave", theme="blue",
                                waves=["diagonal(scale=1,dy=0)"])
    assert "scale(1.3)" not in plain
    assert "translateY(-5px)" not in plain
    assert "@keyframes wave0" in plain
    custom = svg.calendar_to_svg(_weeks(), animate="wave", theme="blue",
                                 waves=["diagonal(scale=1.5,dy=-8)"])
    assert "scale(1.5)" in custom
    assert "translateY(-8px)" in custom


def test_wave_rotate():
    out = svg.calendar_to_svg(_weeks(), animate="wave", theme="blue",
                              waves=["diagonal(rotate=90)"])
    assert "rotate(90deg)" in out
    out_neg = svg.calendar_to_svg(_weeks(), animate="wave", theme="blue",
                                  waves=["sine(rotate=-270)"])
    assert "rotate(-270deg)" in out_neg
    try:
        svg.parse_wave_spec("diagonal(rotate=45)")
        raise SystemExit("should raise")
    except ValueError:
        pass


def test_wave_dsl_parse():
    w = svg.parse_wave_spec("diagonal(color=#ff0000,scale=1.5,invert=true)")
    assert w.shape == "diagonal"
    assert w.color == "#ff0000"
    assert w.scale == 1.5
    assert w.invert is True
    w2 = svg.parse_wave_spec("radial")
    assert w2.shape == "radial"
    try:
        svg.parse_wave_spec("nope")
        raise SystemExit("should raise")
    except ValueError:
        pass


def test_wave_shapes_delay():
    d_lin = svg.wave_delays(svg.WaveSpec("linear", params={"step": 80}), 3)
    assert d_lin[(0, 0)] == 0
    assert d_lin[(2, 0)] == 160
    assert d_lin[(2, 3)] == 160
    d_diag = svg.wave_delays(svg.WaveSpec("diagonal"), 3)
    assert d_diag[(0, 1)] == 65
    assert d_diag[(1, 1)] == 100
    d_rad = svg.wave_delays(svg.WaveSpec("radial"), 3)
    assert d_rad[(1, 3)] == 0
    assert d_rad[(0, 3)] > 0


def test_wave_invert_mirrors():
    fwd = svg.wave_delays(svg.WaveSpec("linear"), 3)
    inv = svg.wave_delays(svg.WaveSpec("linear", invert=True), 3)
    assert inv[(0, 0)] == fwd[(2, 0)]
    assert inv[(2, 0)] == fwd[(0, 0)]


def _keyframes(out):
    """{nom: [(offset%, fill, transform)]} pour chaque @keyframes cell{idx}."""
    import re
    rules = {}
    for name, body in re.findall(
            r"@keyframes (cell?\d+)(\{.*?)(?=@keyframes cell?\d+|\Z)", out, re.S):
        rules[name] = [
            (float(p), f, t)
            for p, f, t in re.findall(
                r"([\d.]+)%\{fill:([^;}]+);transform:([^;}]+);?\}", body)
        ]
    return rules


def _assert_monotonic(rules):
    """Chrome trie les keyframes par offset (dernier gagne a egalite) :
    un offset decroissant ou > 100% est un bug de rendu."""
    for name, stops in rules.items():
        pcts = [s[0] for s in stops]
        assert all(b >= a for a, b in zip(pcts, pcts[1:])), \
            f"{name}: offsets decroissants {pcts}"
        assert max(pcts) <= 100.0, f"{name}: offset > 100% {max(pcts)}"
        seen = {}
        for pct, fill, tf in stops:
            assert seen.setdefault(pct, (fill, tf)) == (fill, tf), \
                f"{name}: collision a {pct}%"
    return rules


def test_wave_chain_offsets():
    waves = [svg.parse_wave_spec("diagonal(duration=4)"),
             svg.parse_wave_spec("diagonal(duration=3,gap=2,invert=true)")]
    assert svg.wave_offsets(waves) == [0, 5000.0]
    out = svg.calendar_to_svg(_weeks(), animate="wave", theme="blue",
                              waves=waves)
    # cycle total boucle : 5s + 5s = 10s, tranches 0-40% puis 50-80%,
    # 1 keyframes par case sur l'element contribution lui-meme.
    assert "@keyframes cell0" in out
    assert "animation:cell1 10s normal infinite" in out
    stops = _assert_monotonic(_keyframes(out))["cell0"]
    # chaque vague rend exactement un pic, et les deux sont ordonnees
    peaks = [s[0] for s in stops if s[1].startswith("#")]
    assert len(peaks) == 2, peaks
    assert peaks[0] < peaks[1], peaks
    assert all(0 < p < 100 for p in peaks), peaks
    assert "opacity" not in out.split("</style>")[0]
    assert 'pointer-events="none"' not in out


def test_multi_wave_offsets_monotonic_and_bounded():
    """Non-regression Chrome : chaque vague reste confinee a son slot.

    Avant, le decalage spatial etait ajoute tel quel a l'offset : 215 des
    369 cases portaient un offset > 100% et une crete se faisait ecraser
    par le stop 100% (pic de la vague 6 invisible sur une case).
    """
    import json
    import os
    path = os.path.join(os.path.dirname(__file__), os.pardir, "waves.json")
    with open(path, encoding="utf-8") as f:
        specs = json.load(f)["waves"]
    out = svg.calendar_to_svg(_weeks(), animate="wave", theme="green",
                              waves=specs)
    rules = _assert_monotonic(_keyframes(out))
    assert rules, "aucun keyframes genere"
    for name, stops in rules.items():
        assert len([s for s in stops if s[1].startswith("#")]) == 6, name


def test_wave_chain_all_visible():
    # non-regression : chaque vague rend son pic sur la case (avant,
    # overlays separes au lieu d'effets sur cases contributions)
    out = svg.calendar_to_svg(_weeks(), animate="wave", theme="blue",
                              waves=["diagonal(color=#ff0000)",
                                     "radial(color=#0000ff)"])
    assert "@keyframes cell0" in out
    assert "#ff0000" in out.split("</style>")[0]
    assert "#0000ff" in out.split("</style>")[0]
    # 1 rect par case (3 jours) + 5 legende, zero overlay
    assert out.count("<rect") == out.count("<title>") + 5

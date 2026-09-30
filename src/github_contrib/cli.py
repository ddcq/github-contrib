"""CLI : python -m github_contrib --login ddcq --out contributions.svg"""

import argparse


def build_parser():
    p = argparse.ArgumentParser(description="Genere contributions.svg")
    p.add_argument("--login", default="ddcq")
    p.add_argument("--out", default="contributions.svg")
    p.add_argument("--cache", default="data/contributions.json")
    p.add_argument("--from", dest="from_iso", default=None)
    p.add_argument("--to", dest="to_iso", default=None)
    p.add_argument("--token", default=None)
    p.add_argument("--animate", choices=["wave", "none"], default="wave",
                   help="Animation SVG : wave (defaut) ou none (statique Phase1)")
    p.add_argument("--theme", default="all",
                   choices=["all", "dark-green", "blue", "dark-blue",
                            "red", "dark-red"],
                   help="Theme couleur : un seul theme ou all (defaut, tous themes)")
    p.add_argument("--wave", action="append", default=None, metavar="SPEC",
                   help="Vague DSL, repetable pour chainage : "
                        "linear|diagonal|radial|sine(k=v,...). "
                        "Ex. diagonal(color=#116329,scale=1.3,dy=-5)")
    p.add_argument("--waves-file", default=None, metavar="JSON",
                   help='Fichier {"waves": ["diagonal", "radial(invert=true)"]}')
    p.add_argument("--no-fetch", action="store_true",
                   help="Utilise uniquement le cache local (pas d'appel API)")
    return p


def theme_outputs(base_out, theme):
    """Retourne liste [(theme, path)]. all -> legacy + suffixes."""
    import os
    from .svg import THEME_NAMES
    if theme != "all":
        return [(theme, base_out)]
    root, ext = os.path.splitext(base_out)
    outs = [(THEME_NAMES[0], base_out)]
    for name in THEME_NAMES[1:]:
        outs.append((name, f"{root}-{name}{ext}"))
    return outs


def load_waves(args):
    """Combine --waves-file puis --wave (ordre donne). Defaut [diagonal]."""
    import json
    from .svg import parse_wave_spec
    specs = []
    if args.waves_file:
        with open(args.waves_file, encoding="utf-8") as f:
            data = json.load(f)
        specs.extend(data.get("waves", data if isinstance(data, list) else []))
    if args.wave:
        specs.extend(args.wave)
    return [parse_wave_spec(s) for s in specs] or None


def main(argv=None):
    from .fetch import fetch_calendar, load_cache, resolve_token, save_cache
    from .svg import THEME_NAMES, calendar_to_svg

    args = build_parser().parse_args(argv)
    token = resolve_token(args.token)

    if args.no_fetch or not token:
        collection = load_cache(args.cache)
    else:
        collection = fetch_calendar(
            args.login, args.from_iso, args.to_iso, token)
        save_cache(args.cache, collection)

    weeks = collection["contributionCalendar"]["weeks"]
    total = collection["contributionCalendar"].get("totalContributions")
    waves = load_waves(args)
    for name, path in theme_outputs(args.out, args.theme):
        svg = calendar_to_svg(weeks, animate=args.animate, theme=name,
                              waves=waves)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"OK: {len(weeks)} semaines, total={total}, theme={name} -> {path}")


if __name__ == "__main__":
    main()

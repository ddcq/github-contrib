"""CLI: python -m github_contrib --login ddcq --out assets/contributions.svg"""

import argparse


def build_parser():
    p = argparse.ArgumentParser(description="Generate contributions.svg")
    p.add_argument("--login", default="ddcq")
    p.add_argument("--out", default="assets/contributions.svg")
    p.add_argument("--cache", default="data/contributions.json")
    p.add_argument("--from", dest="from_iso", default=None)
    p.add_argument("--to", dest="to_iso", default=None)
    p.add_argument("--token", default=None)
    p.add_argument("--animate", choices=["wave", "none"], default="wave",
                   help="SVG animation: wave (default) or none (static Phase1)")
    p.add_argument("--theme", default="all",
                   choices=["all", "dark-green", "green", "blue", "dark-blue",
                            "red", "dark-red"],
                   help="Color theme: a single theme or all (default, every theme)")
    p.add_argument("--wave", action="append", default=None, metavar="SPEC",
                   help="Wave DSL, repeatable for chaining: "
"linear|diagonal|radial|sine(k=v,...). "
                         "Ex. diagonal(color=#116329,scale=1.3,dy=-5,sy=1)")
    p.add_argument("--waves-file", default=None, metavar="JSON",
                   help='File {"waves": ["diagonal", "radial(invert=true)"]}')
    p.add_argument("--no-fetch", action="store_true",
                   help="Use only the local cache (no API call)")
    return p


def theme_outputs(base_out, theme):
    """Returns list [(theme, path)]. all -> base + suffixes."""
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
    """Combines --waves-file then --wave (given order). Default [diagonal]."""
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
    import os
    for name, path in theme_outputs(args.out, args.theme):
        svg = calendar_to_svg(weeks, animate=args.animate, theme=name,
                              waves=waves)
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"OK: {len(weeks)} weeks, total={total}, theme={name} -> {path}")


if __name__ == "__main__":
    main()

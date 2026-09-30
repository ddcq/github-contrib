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
    p.add_argument("--no-fetch", action="store_true",
                   help="Utilise uniquement le cache local (pas d'appel API)")
    return p


def main(argv=None):
    import os

    from .fetch import fetch_calendar, load_cache, save_cache
    from .svg import calendar_to_svg

    args = build_parser().parse_args(argv)
    token = args.token or os.environ.get("GITHUB_TOKEN")

    if args.no_fetch or not token:
        collection = load_cache(args.cache)
    else:
        collection = fetch_calendar(
            args.login, args.from_iso, args.to_iso, token)
        save_cache(args.cache, collection)

    weeks = collection["contributionCalendar"]["weeks"]
    svg = calendar_to_svg(weeks)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg)
    total = collection["contributionCalendar"].get("totalContributions")
    print(f"OK: {len(weeks)} semaines, total={total} -> {args.out}")


if __name__ == "__main__":
    main()

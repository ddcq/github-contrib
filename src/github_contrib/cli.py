"""CLI : python -m github_contrib --login ddcq --out contributions.svg"""

import argparse


def build_parser():
    p = argparse.ArgumentParser(description="Genere contributions.svg")
    p.add_argument("--login", default="ddcq")
    p.add_argument("--out", default="contributions.svg")
    p.add_argument("--cache", default="data/contributions.json")
    p.add_argument("--from", dest="from_iso", default=None)
    p.add_argument("--to", dest="to_iso", default=None)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    raise NotImplementedError


if __name__ == "__main__":
    main()

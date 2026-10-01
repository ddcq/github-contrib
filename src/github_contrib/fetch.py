"""Fetch GraphQL ContributionsCollection + JSON cache (stdlib only)."""

import json
import os
import ssl
import urllib.request

API_URL = "https://api.github.com/graphql"

QUERY = """
query($login: String! $from: DateTime $to: DateTime) {
  user(login: $login) {
    contributionsCollection(from: $from to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
            color
          }
        }
      }
      restrictedContributionsCount
      hasAnyRestrictedContributions
    }
  }
}
"""


def _ssl_context():
    """SSL context using the certifi bundle when available (Python.org macOS)."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def resolve_token(explicit=None):
    """Priority: --token > GITHUB_TOKEN > GITHUB_DDCQ_READ."""
    if explicit:
        return explicit
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_DDCQ_READ")


def fetch_calendar(login, from_iso=None, to_iso=None, token=None):
    """Queries the GraphQL API and returns the contributionsCollection dict."""
    token = resolve_token(token)
    if not token:
        raise RuntimeError("Missing token (--token, GITHUB_TOKEN or GITHUB_DDCQ_READ)")
    variables = {"login": login, "from": from_iso, "to": to_iso}
    body = json.dumps({"query": QUERY, "variables": variables}).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "github-contrib",
        },
    )
    with urllib.request.urlopen(req, timeout=30, context=_ssl_context()) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise RuntimeError(f"GraphQL errors: {payload['errors']}")
    user = (payload.get("data") or {}).get("user")
    if user is None:
        raise RuntimeError(f"User not found: {login}")
    return user["contributionsCollection"]


def load_cache(path):
    """Loads a local JSON cache."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_cache(path, payload):
    """Saves the raw response as JSON."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")

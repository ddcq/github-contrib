"""Fetch GraphQL ContributionsCollection + cache JSON (stdlib only)."""

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


"""Fetch GraphQL ContributionsCollection + cache JSON (stdlib only)."""

import json
import os
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


def fetch_calendar(login, from_iso=None, to_iso=None, token=None):
    """Interroge l'API GraphQL et retourne le dict contributionsCollection."""
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN manquant (env ou param token)")
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
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise RuntimeError(f"GraphQL errors: {payload['errors']}")
    user = (payload.get("data") or {}).get("user")
    if user is None:
        raise RuntimeError(f"Utilisateur introuvable: {login}")
    return user["contributionsCollection"]


def load_cache(path):
    """Charge un cache JSON local."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_cache(path, payload):
    """Sauve la reponse brute en JSON."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")

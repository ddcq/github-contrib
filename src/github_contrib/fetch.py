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


def fetch_calendar(login, from_iso=None, to_iso=None, token=None):
    """Interroge l'API GraphQL et retourne le dict contributionsCollection."""
    raise NotImplementedError


def load_cache(path):
    """Charge un cache JSON local."""
    raise NotImplementedError


def save_cache(path, payload):
    """Sauve la reponse brute en JSON."""
    raise NotImplementedError

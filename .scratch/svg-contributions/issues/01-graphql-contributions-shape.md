Type: research
Status: resolved
Blocked by:

## Question

Quelle est la forme exacte de `ContributionsCollection` (contributionCalendar.weeks.days : date, count, level/color) pour l'utilisateur `ddcq`, et quelle requête GraphQL minimale + scopes token faut-il pour inclure les contributions privées avec fallback public ?

## Answer

Shape : `User.contributionsCollection(from,to)` -> `contributionCalendar { totalContributions, weeks { contributionDays { date, contributionCount, contributionLevel, color } } }` + `restrictedContributionsCount`, `hasAnyRestrictedContributions`. Levels = NONE/FIRST..FOURTH_QUARTILE (relatifs). Requête minimale + vars login/from/to connues. Privées : scope classic `read:user`, sinon fallback public même requête sans scope (totaux réduits). Auth `bearer` obligatoire même public.

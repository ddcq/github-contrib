Type: research
Status: resolved
Blocked by:

## Question

Quel est le rendu exact du calendrier public GitHub à reproduire (dimensions cellules, gaps, palette des 5 verts light mode, labels mois/jours, légende, structure DOM/SVG, tooltips) ?

## Findings (vérifié 2026-09-30, light mode)

Palette actuelle (source primaire `@primer/primitives` light.css) :
- L0 `--contribution-default-bgColor-0`: #eff2f5
- L1 `--contribution-default-bgColor-1`: #aceebb
- L2 `--contribution-default-bgColor-2`: #4ac26b
- L3 `--contribution-default-bgColor-3`: #2da44e
- L4 `--contribution-default-bgColor-4`: #116329
- bordure `--contribution-default-borderColor-0`: #1f23280d (L1-L4 = `var(--contribution-default-borderColor-0)`).
- Ancienne palette (#ebedf0, #9be9a8, #40c463, #30a14e, #216e39) obsolète, voir discussion community 7078.

Dimensions (DOM live `/users/torvalds/contributions`) :
- `table.ContributionCalendar-grid` style `border-spacing: 3px` => gap 3px.
- cellules jour `td` style `width: 10px`, lignes `tr` style `height: 10px`, légende `div` style `width: 10px; height: 10px` => cellules 10x10, pas 13px.
- `thead tr` style `height: 13px`, 1re colonne `td` style `width: 28px` (gutter labels jours).
- radius : cellules légende class `rounded-1` (Primer docs = 4px) ; repro SVG : `rx=2` équivalent visuel (défaut clones, ex. react-contribution-calendar `cr: 2`).

Labels :
- Mois : `td.ContributionCalendar-label colspan=4|5` (nb semaines du mois), `<span class=sr-only>October</span>` + `<span aria-hidden=true style="position:absolute;top:0">Oct</span>` ; abréviations EN 3 lettres Jan..Dec.
- Jours : 1re colonne `td.ContributionCalendar-label`, visibles Mon/Wed/Fri (`clip-path: None`), cachés Sun/Tue/Thu/Sat (`clip-path: Circle(0)`) ; `span` style `position:absolute;bottom:-3px`.

Légende :
- `Less` + 5 `div#contribution-graph-legend-level-0..4.ContributionCalendar-day.rounded-1` + `More`.
- Textes sr-only par niveau : "No / Low / Medium-low / Medium-high / High contributions."

Structure DOM :
- `div.js-calendar-graph[data-graph-url=/users/USER/contributions][data-from][data-to]` > `div[overflow-x:auto]` > `table[role=grid][aria-readonly].ContributionCalendar-grid` > `caption.sr-only` + `thead` (mois) + `tbody` (7 `tr` Sun..Sat, ~53 colonnes `data-ix=0..52`, ordre weekday-major ; compté 368 `data-date` sur fenêtre glissante).
- Fenêtre profil = glissante 12 mois (`data-from=2025-09-28`, `data-to=2026-09-30`) ; variante `?to=` = année civile Jan-Dec.
- Cellule : `td[tabindex=0][data-ix][data-date=YYYY-MM-DD][data-level=0-4][role=gridcell][id=contribution-day-component-R-C][aria-describedby=contribution-graph-legend-level-N].ContributionCalendar-day`.

Tooltips :
- `<tool-tip for=CELL-ID popover=manual data-direction=n data-type=label class="sr-only position-absolute" style="pointer-events:none">` texte : `No contributions on October 13th.` / `1 contribution on ...` / `N contributions on ...`.

## Sources
- https://github.com/users/torvalds/contributions (DOM live)
- https://github.com/users/torvalds/contributions?to=2026-09-30 (année civile + légende)
- https://unpkg.com/@primer/primitives@latest/dist/css/functional/themes/light.css (tokens)
- https://primer.style/foundations/color + https://primer.style/product/css-utilities/borders (rounded-1)
- https://github.com/primer/primitives (repo tokens)
- https://github.com/orgs/community/discussions/7078 (ancienne palette)

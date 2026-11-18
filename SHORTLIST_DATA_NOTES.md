# RR 2027 shortlist dashboard data notes

- The dashboard contains 10 batters and 10 bowlers from the previously agreed scouting watchlist.
- Portraits are AI-generated illustrative approximations, not official player photographs or verified likenesses.
- Player pressure figures are sourced from Stage 3 Model C chase-only outputs (`players_bat_chase_C.csv` / `players_bowl_chase_C.csv`).
- `score` is the shrunk pressure effect vs role prior per 100 pressure-eligible balls. Batting and bowling estimates have different interpretations; do not compare across roles.
- `sample` / `pressureSample` are pressure-eligible balls, not total career balls.
- Under 120 eligible balls is below the primary evidence threshold. These players are included for scouting completeness, not labelled pressure-proven.
- Bowling estimates with near-zero role-prior variance are marked degenerate and should not be interpreted as average performance.
- Pressure reliability is displayed as a percentage derived from Stage 3 reliability. Even eligible estimates have limited player-level reliability.
- No match-by-match timeline, phase split, strike rate or economy data has been fabricated.
- This is an independent competition-analysis dashboard, not an official Rajasthan Royals product.

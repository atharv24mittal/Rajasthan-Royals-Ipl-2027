# RR 2027 Dashboard — Data & QA Update

This dashboard combines the supplied proprietary competition data pack (Stage 3 chase-pressure outputs) with public internet research. These are separate evidence streams.

## Corrections
- Previously hardcoded phase, dot-ball, primary-rate, consistency, timeline and competition-split zeros are now null/unavailable, not performance zeros.
- Degenerate bowling pressure estimates are labelled N/A for score/interval interpretation.
- Pressure is chase-only; read estimates alongside eligible-ball count, reliability and the 120-ball screen.
- Public 2026 IPL form is shown separately from proprietary pressure estimates.
- Gemini/DeepSeek outputs were treated as leads, not source-of-truth: unverified totals and phase baselines were not imported wholesale.

## Selected public sources
- IPL 2026 statistics: https://www.ipl.com/series/indian-premier-league-2026-129908/stats
- Pathum Nissanka: https://www.ipl.com/player/pathum-nissanka
- Shimron Hetmyer: https://www.ipl.com/player/shimron-hetmyer
- Deepak Chahar: https://www.ipl.com/player/deepak-chahar
- Tushar Deshpande: https://www.ipl.com/player/tushar-deshpande
- ESPNcricinfo Statsguru: https://stats.cricinfo.com/ci/engine/stats/index.html

## Deliberate N/A fields
Complete ball-by-ball phase splits, matched league baselines, dot-ball rates, full domestic T20 season timelines, exact competition sample attribution and any proprietary pressure metric not present in the original export.

Research cutoff: 17 November 2026.

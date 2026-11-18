# SupeRR Intelligence — RR 2027 shortlist

This package combines the user-provided proprietary competition data pack with public internet research. Proprietary pressure metrics and public cricket statistics are intentionally kept separate.

## Run locally
Open `dist/superr-intelligence-v4-standalone.html` in a browser for the single-file preview, or run a static server from this folder and open `index.html`.

## Deploy to Vercel
1. Upload the contents of this folder to a private GitHub repository.
2. Import the repository at https://vercel.com/new.
3. Framework preset: Other. Build command: `python scripts/build_standalone.py` (or leave blank if deploying the already-built static source). Output directory: `.`.
4. For a simple static deployment, `index.html` is the entry point. Keep the repository private because it contains derived competition analysis.
5. Check the deployment preview, player dossiers, mobile navigation and presentation mode before sharing.

The standalone preview is in `dist/`.

## Comparison filters (17 Nov 2026 update)
The Player Comparison page includes independent phase and competition filters. Phase choices (All, Powerplay, Middle overs, Death) change the phase rows shown. Competition choices (All, IPL, T20I, Youth) select the corresponding source scope where available. All uses each player's first available documented scope and labels it; it does not combine unlike competitions. Missing scope/phase data remains N/A. Filters are native buttons with `aria-pressed` state and update the comparison table on each click.


## Expanded final build — 17 November 2026
- Added the expanded 20-player PDF scouting report at `reports/RR_2027_RR_Scouting_Expanded_Report.pdf`; it includes dashboard screenshots, all 20 player dossiers, pressure audit, sourced phase data, AI-response cross-check, and a 59-item feature catalogue.
- Added Saved Shortlist: save/unsave players, browser-local persistence, open saved dossiers, export saved list as CSV, and clear saved items.
- Added Feature Library: searchable 59-capability index with Live / New / Data-limited status filters.
- Added a direct PDF link in the left navigation.
- Added interval QA: confidence intervals are suppressed when the stored interval fails the point-within-interval check; raw point estimates are preserved pending original Stage 3 reconciliation.
- Comparison phase labels now distinguish batting strike-rate splits from bowling economy splits.
- Competition filters use actual phase-data scope presence, not placeholder zero counts.
- Added structured CSV exports for pressure audit and phase evidence under `data/`.

## Emerging Gems expansion (15 additional domestic prospects)
The original 20-player shortlist is unchanged. A separate Emerging Gems navigation section adds 15 prospects in four groups (5 finishers, 4 domestic fast bowlers, 3 wrist/finger spinners, 3 top/middle-order batters). These are discovery candidates from public domestic records, not players with verified proprietary Stage 3 pressure scores. All pressure status is labelled unvalidated. See `EMERGING_GEMS_RESEARCH.md` and `data/emerging_gems.json`.


## Global discovery update — 18 November 2026
- Emerging Gems now opens with the final 10-batter / 10-bowler shortlist, including two new discovery additions in each role.
- Added a separate 15-player international watchlist, excluding Pakistan-qualified players.
- Preserved the existing 15-player Indian Emerging Gems board.
- New discoveries do not receive invented Stage 3 pressure scores; public performance aggregates and pressure evidence remain separate.
- See `RR_2027_GLOBAL_DISCOVERY_NOTES.md` and `data/rr_2027_final_shortlist.json`.


### Phase-level batting and bowling intelligence
The emerging-gems board now includes expandable player phase tables: batting sixes/fours and dot balls per six legal balls, boundary frequency, and bowling death-over legal yorkers per six balls, plus phase and situation splits. Coverage limitations and exact definitions are documented in `RR_2027_GLOBAL_DISCOVERY_NOTES.md`.

### New research navigation (18 Nov 2026)
- `Released Stars`: high-profile IPL 2027 releases with prior team, role, previous price (where reported), and availability caveats.
- `2026 Absentees`: players who missed all/part of IPL 2026 due to injury, workload, administrative or personal reasons, with 2027 status checks.
Both are scouting trackers, not confirmed auction registers. Reconfirm BCCI registration, fitness, NOC and availability before bidding.

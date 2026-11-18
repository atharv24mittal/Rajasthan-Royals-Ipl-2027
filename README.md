# SUPERR INTELLIGENCE v4: The Scouting War Room
Static app (HTML/CSS/JS, no build needed to run). Open `index.html` locally, or `dist/superr-intelligence-v4-standalone.html` (single file).
**Real:** Stage 1 and Stage 2 aggregates (`data/stage2.js`, built by `scripts/build_stage2_data.py`, which also asserts 200,999 raw rows less 38 super-over rows equals 200,961). **Pending:** all player-level scores. A labelled synthetic Layout preview exists for design review only.
## Layout
`index.html` shell; `src/css`, `src/js` modules (core, landing, command, viz, pressure, board, compare, dossier, stability, simulator, method, integrity, present, main); `assets/`; `data/`; `scripts/` (data build, standalone build, QA, a11y, tests, deploy check); `reports/` (Lighthouse, axe, logs); `screenshots/`; `video/`; `docs/`.
## Commands
`npm run build` standalone; `npm run qa`; `npm run test:auth`; data: `python scripts/build_stage2_data.py <stage2/output> "<Data Pack>/ball_by_ball.csv"` then rebuild.
## Docs
DEPLOY.md, QA_REPORT.md, LIGHTHOUSE.md, ACCESSIBILITY.md, LIMITATIONS.md, PLAYER_SCHEMA.md, CHANGELOG_V3_TO_V4.md.
Competition concept; not an official Rajasthan Royals system; no club marks used.

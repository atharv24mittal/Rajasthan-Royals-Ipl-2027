# Remaining limitations and pending analytical work
1. No player-level scores exist (Stage 3): leaderboards, dossiers, comparison are Pending. The synthetic Layout preview is labelled and never default.
2. Per-player ranking stability, competition-mix scenarios (IPL only, IPL+T20I, +youth) and sample-threshold scenarios require Stage 3 outputs. Today only Stage 2 diagnostics (rank agreement, split-half noise ceiling, exposure) are shown.
3. Simulator supports only grid states: 3 or 7 wickets lost, balls left 6 to 120 step 6, ratio 0.3 to 2.0 step 0.1, chases only. No runs-needed input (expected-remaining-runs table not exported). Not a ball-by-ball simulation.
4. Win-probability model is mis-calibrated in 2026 (chases won 63.4%); first-innings pressure is not validated.
5. Four methodology decisions are awaiting approval (listed on the Methodology page).
6. Comparable-historical-scenarios panel is pending an approved similarity definition.
7. Portraits are fictional SVGs. Real licensed photos, attribution and rights metadata are needed (manifest shown on Data Integrity page).
8. The supplied hero GIF/JPG contained a "Rajasthan Royals" banner and crest; V4 does not use them (`assets/_unused_supplied_hero/`). Confirm rights before ever using them.
9. Architecture remained static HTML/CSS/JS (no Next.js migration); charts are inline SVG and canvas. No GSAP, ECharts or Three.js (not needed; keeps the bundle near 0.6 MB). `legacy-nextjs-v1` from V3 is not included here and remains unported.
10. Tested in Chromium only; no screen-reader pass; Vercel authentication not verified on a live deployment.
11. Mobile Lighthouse performance is sensitive to the opening animation; see LIGHTHOUSE.md.

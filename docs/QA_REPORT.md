# QA report (V4). Every line below was executed; nothing is claimed that was not run.
Environment: Playwright 1.63, Chromium 1243 headless. **Firefox and WebKit are not installed in this environment and were not tested.**
| Suite | Target | Result |
|---|---|---|
| `scripts/qa.py` (interaction + layout, 124 checks) | standalone | 124 / 124 |
| `scripts/qa.py` | source `index.html` | 124 / 124 |
| `scripts/a11y.py` (axe on 13 states + keyboard) | standalone | 0 violations; keyboard 9 / 9 |
| `scripts/test_live_and_motion.py` (Stage 3 contract fixture + reduced motion) | standalone | 12 / 12 |
| `scripts/test_middleware.mjs` (real middleware.js, Web Request objects) | local | 9 / 9 |
| Lighthouse | source + standalone, mobile + desktop | see LIGHTHOUSE.md |

Coverage of qa.py: viewports 360, 390, 430, 768, 1280, 1440, 1920; all 10 sections at each (no horizontal overflow, no console errors, images load); counters end at verified values (883 / 200,961 / 811 / 138); heatmap model/wicket switching, cell click, keyboard arrows, tooltip; validation toggles; evidence drawer + scrim + Escape; leaderboard search, preview switch banner, sort/competition/role filters; compare FAB, 2 to 3 players; dossier open, tabs, indicator, evidence, close; stability toggle and tooltip; simulator controls, model gauge, ratio sweep start/stop; methodology stepper; presentation open, navigate, Home, close; number shortcut; mobile menu.

## Bugs found by this QA and fixed
1. Command Centre threw on load (wrong index), landing overlay never closed (v3, similar class of bug caught in V4 build).
2. External CSS resolved `url(assets/...)` relative to `src/css/`, so backgrounds 404ed.
3. Pressure evidence panel was invisible: class `.flash` collided with the landing flash overlay.
4. Mobile overflow in Ranking and Pressure pages (grid min-width, forest-plot column).
5. Stale tooltip left on screen after navigation.
6. FAB (compare) persisted on unrelated sections.
7. Win-probability gauge fill was inverted.
8. Dossier focus could not move in (visibility timing); no focus return; no focus trap.
9. Accessibility items listed in ACCESSIBILITY.md.

## Not tested
Firefox, Safari/WebKit, real iOS/Android devices, screen readers, a live Vercel deployment (see DEPLOY.md), Lighthouse on a throttled real network.

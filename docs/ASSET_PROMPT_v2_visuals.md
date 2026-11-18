# Claude implementation prompt

Upgrade `superr-intelligence-v2-demo.html` into a genuinely premium cricket scouting intelligence experience using the adjacent `images/` folder.

## First: audit, don't blindly rewrite
Read the full existing HTML and document all working sections, all placeholder sections, and all known inconsistencies. Preserve correct Stage 1 aggregate values and existing useful interactions. Fix defects rather than replacing working logic with mock content.

## Non-negotiable analytical integrity
- Every synthetic player, score, timeline, match ID, formula, ranking, and comparison must remain explicitly `ILLUSTRATIVE`.
- No invented real player data, photographs, sample sizes, confidence intervals, or Rajasthan Royals recommendations.
- Keep Stage 1 verified and Stage 2 pending clearly separated.
- Reconcile and label 200,999 raw ball rows vs 200,961 regular-innings deliveries (38 super-over deliveries excluded) with a transparent definition.
- Validate the 883 matches / 867 matches with ball data / 811 pressure-usable matches / 138 competitions values against the current Stage 1 source files before production.
- Never present the placeholder win-probability function as a fitted model.

## Visual direction
Create a cinematic, editorial cricket analytics product: obsidian background, deep navy surfaces, restrained electric pink, lavender and teal, strong typography, real information hierarchy, large legible numbers, generous whitespace, sharp charts and restrained motion. Avoid generic sci-fi clutter, excessive glow, constant animation, or dashboard-card overload.

## Use the included assets
- `images/hero/stadium-hero.svg`: opening / Command Centre hero background, with dark overlay.
- `images/hero/cricket-ball.svg`: intro motif only; keep intro skippable and short.
- `images/ui/panel-texture.svg`: selected large panel surfaces only.
- `images/ui/grid-overlay.svg`: very low-opacity chart/panel background.
- `images/ui/spotlight-glow.svg`: subtle decorative glow.
- `images/portraits/*.svg`: fictional demo portraits only. Never attach them to real player names or real scouting records.
- `images/icons/*.svg`: matching feature/metric icons.

## High-impact product changes
1. Make the Command Centre a strong editorial landing page, not just KPI tiles: one clear thesis, evidence-base KPIs, tier coverage, phase coverage, verified/pending status, and a clear next action.
2. Add a persistent evidence/definition affordance for every key metric. Show numerator, denominator, unit, sample, baseline, interval, and validation status where relevant.
3. Improve the player leaderboard with real filters, sortable columns, role, sample, pressure observations, reliability, confidence intervals, and a clear explanation of rank uncertainty. Do not show rankings until Stage 2 data is ready.
4. Make dossiers useful: role, verified season/competition coverage, phase splits, sample counts, uncertainty, tactical fit and recommendation status. Hide unavailable fields rather than inventing them.
5. Make comparisons statistically responsible: same role/context, common scale with documented directionality, uncertainty-aware differences, and no false claim that overlapping intervals alone prove equivalence.
6. Ranking stability must recompute from actual validated outputs under each specification; remove synthetic hash-based perturbations.
7. Match simulator must distinguish hypothetical state exploration from historical evidence; don't call a logistic placeholder win probability a real win probability.
8. Methodology should expose the pipeline, definitions, exclusions, caveats, validation plan, and reproducibility links.
9. Data integrity should include an auditable change log and exact source/version references.
10. Presentation mode should use verified metrics only, with illustrative slides excluded or unmistakably watermarked.

## Engineering and QA
- Deliver both the updated standalone HTML demo and a complete ZIP of the full project/source; do not stop at HTML.
- Keep assets local; no hotlinked player photos.
- Test every nav item, filter, slider, comparison, dossier, evidence drawer, simulator control, presentation shortcut, Escape close, and mobile menu.
- Fix keyboard focus management, focus restoration, dialog semantics, reduced motion, and small-screen horizontal overflow.
- Test 360px, 390px, 768px, 1024px, 1440px, and 1920px widths.
- Run HTML validation and JavaScript syntax checks; include a concise QA report and list remaining limitations.
- Keep the ZIP structure reproducible and include a README with setup and deployment steps.

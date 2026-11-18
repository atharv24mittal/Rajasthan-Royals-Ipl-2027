# Accessibility report
## Executed
- **axe-core** (WCAG 2.0/2.1/2.2 A and AA plus best-practice rules) on 13 states: all 10 sections, leaderboard preview, dossier, evidence drawer. Final result: **0 violations**. Raw output: `reports/a11y.json`.
- Initial run found 20 violation entries (missing h1, heading order, aria-label/visible-text mismatch, aria on a role-less div, unfocusable scroll region, one contrast failure). All fixed, then re-run.
- **Keyboard journeys** (scripted, Chromium): Tab order through navigation, visible focus style, Enter opens dossier and moves focus inside it, Escape closes and returns focus, heatmap operable by arrow keys, evidence drawer takes focus and closes with Escape, P opens presentation, arrows advance slides, simulator slider operable. All pass. Dialogs trap Tab.
- **Contrast** computed for 10 key colour pairs (reports/a11y.json). All meet 4.5:1 after darkening the button pink to #C42B69 (white text 5.39:1) and lightening the pink badge text. The original white-on-#E83E83 pair was 3.85:1 and was changed.
- **Reduced motion**: tested in an emulated `prefers-reduced-motion: reduce` context (final-state intro, instant counters, visible content).
- Charts have `role="img"` with text summaries, plus adjacent tables or numeric readouts.
## Not done
Screen-reader testing (NVDA, VoiceOver, JAWS), touch-gesture testing on real devices, WCAG manual audit of the colour-only heat scale (values are also given as numbers in tooltips and the evidence panel).

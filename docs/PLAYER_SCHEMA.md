# Stage 3 data contract
Load verified player-level outputs by adding, before `src/js/00_core.js` in `index.html` (and the build script inlines it):
`<script src="data/players.js"></script>` where the file defines `window.P3 = [ ... ]`.
Each player: `id` (stable key, also the image key), `name`, `kind` ("bat"|"bowl"), `role`, `img` (path to a licensed photo; omit for the fallback), `sample`, `pressureSample`, `score`, `lo`, `hi` (95% interval), `reliability` (0-100), `consistency` (0-100), `phase` [powerplay, middle, death vs baseline], `competition` [IPL, T20I, youth balls], `dot`, `primary` (strike rate or economy), `timeline` (5 seasons x match values).
When `window.P3` exists the app enters verified mode: preview switch, hazard banner and "synthetic" wording disappear, badges read Verified. Tested with a fixture in `scripts/test_live_and_motion.py` (fixture is not shipped).
Add licensed photos with attribution to the manifest table (Data Integrity) before use.

# Deployment (Vercel) and security
1. Keep the Git repository **private**. `data/stage2.js` holds derived aggregates of proprietary research; no raw rows are shipped. `.gitignore` excludes CSVs.
2. Vercel: import repo as "Other" (no build command, output directory `.`), run `npm install` so `@vercel/functions` is available to `middleware.js`.
3. Environment variables: `DASHBOARD_USER`, `DASHBOARD_PASS`. Leave `ACCESS_MODE` unset (fail closed: missing credentials returns 503). Also enable Vercel Deployment Protection.
4. **Verify on the real deployment** (this environment has no Vercel access, so this was NOT done): `bash scripts/verify_deploy.sh https://<project>.vercel.app <user> <pass>`. It checks 401 without credentials, 401 with wrong credentials, that `/data/stage2.js` is also protected, 200 with valid credentials, the noindex header, and that no raw dataset path responds.
5. `npm run test:auth` executes the real middleware code locally (9 cases). That proves the logic, not that the platform runs it.
6. Headers (`vercel.json`): noindex, nosniff, no-referrer, frame deny. `<meta robots noindex>` is also in the page.

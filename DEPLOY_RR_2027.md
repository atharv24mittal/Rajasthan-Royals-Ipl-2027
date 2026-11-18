# Deploy the updated RR 2027 scouting dashboard to Vercel

## Important
- Keep the GitHub repository **Private**. The dashboard includes derived proprietary competition-data metrics.
- The dashboard is protected by `middleware.js`. Set `DASHBOARD_USER` and `DASHBOARD_PASS` in Vercel Project → Settings → Environment Variables. Do not publish without credentials.
- Enable Vercel Deployment Protection as an additional safeguard.
- The project is a static HTML/CSS/JS app; no framework build is required. `index.html` is the entry point.

## Steps
1. Download and unzip `RR_2027_Updated_Dashboard_Vercel.zip`.
2. Create a **private** GitHub repository and upload the contents of the `superr-intelligence-v4` folder (not the outer folder itself).
3. In Vercel, choose **Add New → Project**, import that private repository.
4. In Configure Project, choose **Other**. Leave Build Command blank; set Output Directory to `.`. Install Command can be `npm install` (needed for the access middleware dependency).
5. Before deploying, open **Settings → Environment Variables** and add:
   - `DASHBOARD_USER` = a username you choose
   - `DASHBOARD_PASS` = a strong unique password
   Add them for Production (and Preview if you intend to use preview deployments).
6. Deploy. Open the generated URL. You should be prompted for the dashboard credentials.
7. Verify that the dashboard opens, player portraits load, and the Batter/Bowler/Dossiers sections show the 20-player shortlist.

## Local preview
Open `index.html` with a local static server (for example `python -m http.server 8000`) and visit `http://localhost:8000`. Authentication middleware only applies on Vercel.

## Data caveats
Player pressure figures are Stage 3 chase-only estimates. The primary evidence threshold is 120 pressure-eligible balls. Below-threshold and degenerate estimates are not pressure-proven. AI portraits are illustrative approximations, not official photographs. Read `SHORTLIST_DATA_NOTES.md`.

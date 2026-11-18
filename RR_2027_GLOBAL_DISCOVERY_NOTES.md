# RR 2027 Global Discovery Update

## Final 20
Eight original players per role retained, with two discovery additions each: Sediqullah Atal and Ackeem Auguste (batters); Arab Gul Momand and Tristan Luus (bowlers). The original shortlist names displaced from the core 20 are Karun Nair, Ben Duckett, Adam Milne and Kuldeep Sen; they remain in the historical original 20 source data, but not the updated final 20.

## 15 international watchlist
See `data/rr_2027_final_shortlist.json`. Pakistan-qualified players excluded. Stats are sourced public aggregates where stated; APL Emerging selections have no APL season stats before the season begins; some CPL breakout player aggregates require scorecard extraction and are explicitly marked.

## Pressure methodology
Public T20 season totals are not Stage 3 pressure scores. Only original Stage 3 eligible players retain their proprietary pressure sample/effect/reliability information. New additions have no proprietary pressure sample and must not be assigned one.

## Sources
- ACB APL 2026 draft: https://acb.af/en-US/post/aplt20-player-draft-2026-concludes-in-dubai-as-five-franchises-finalize-their-squads
- APL Emerging picks: https://aplt20league.com/squads/emerging/
- Arab Gul profile and T20 record: https://www.ipl.com/player/arab-gul-momand
- Tristan Luus profile: https://www.ipl.com/player/tristan-luus
- Anirudh Immanuel profile: https://www.ipl.com/player/anirudh-immanuel
- MLC 2026 stats: https://maidanbeat.com/cricket/series/major-league-cricket-2026/stats/
- Amshi de Silva MLC bowling: https://www.crictracker.com/major-league-cricket/stats/bowling-best-bowling-figures/
- Sediqullah Atal T20 stats: https://www.ipl.com/player/sediqullah-atal
- CPL 2026 stats: https://statz.ai/cricket/competitions/cpl/stats
- CPL breakout retention announcement: https://www.wiplayers.com/news/cpl-teams-confirm-their-breakout-player-retentions/
- Tim Robinson stats: https://www.windiescricket.com/players/tim-robinson-20747/

## Claude audit integration — 18 November 2026

### What is accepted
- **Do not spend the full purse just to fill six slots.** RR has 19 retained players, six slots, ₹27.05 Cr and three overseas slots. The five retained overseas players are Jofra Archer, Nandre Burger, Dasun Shanaka, Donovan Ferreira and Lhuan-dre Pretorius. A maximum of four overseas players can play in an XI, so an overseas buy must clear a high marginal-value bar. Source: RR official retention announcement (17 Nov 2026): https://www.rajasthanroyals.com/latest-news/ipl-2027-rr-players-retention-list-retained-released
- **Mustafizur is a registration, not a guaranteed availability case.** BCB reporting confirms his registration interest/entry and that six other Bangladesh players were also registering; this does not guarantee BCCI clearance or a franchise contract. His previous release followed a BCCI direction, so classify him as a material participation/clearance risk, not “high availability”. Sources: https://www.indiatoday.in/amp/sports/cricket/story/ipl-2027-mini-auction-bangladesh-mustafizur-rahman-exclusive-kkr-release-3036897-2026-11-11 and https://www.outlookindia.com/amp/story/sports/cricket/ipl-2027-auction-bangladesh-cricketers-participation-bcb-reaction-seven-registered
- **Sri Lankan NOC/fitness gate is real.** SLC's reported mandatory physical performance test applies before NOCs for franchise leagues, particularly to players returning from injury. Pathirana and Hasaranga should remain conditional on current fitness and NOC confirmation. Source: https://www.thedailystar.net/sports/cricket/news/no-fitness-test-no-ipl-sri-lanka-lays-down-rule-players-4133721
- **Avesh Khan is downgraded from a confident buy to “reassess / lower auction priority”.** The current Stage 3 file gives him 323 pressure-eligible bowling balls, +0.66 runs/100 vs role prior and only 9.6% reliability. Public IPL 2026 phase notes show 9.15 death economy from 40 balls, but 16.50 in the powerplay from 24 balls. The underlying supplied ball-by-ball pack independently yields 7 matches, 6 wickets, 148 legal balls, 265 runs conceded and 10.74 economy (small differences from secondary aggregator totals are possible due to ball/extras conventions). This is mixed evidence, not a clean “reliable death option”.

### What is not adopted as fact
- Claude's custom values (e.g. Avesh −13 overall / −17 on 430 pressure balls; Taskin +20 on 203; Pathirana +23 on 369; marginal XI gains in runs per match; six-player price ceilings) are a **separate model**. Its pressure definition, wicket value, phase weighting, shrinkage and player pool differ from Stage 3 Model C and Stage 4. The supplied files do not contain a reproducible export of that custom model's player-level ratings or four scenario outputs. Keep these as hypotheses until Claude's code, exact input extract and output tables are supplied.
- Current Stage 3 Model C counts in the frozen files are Hetmyer 175 pressure-eligible batting balls and Nitish Rana 92 (not 249 and 145); Avesh has 323 bowling balls. These are definition-specific pressure samples and should not be compared with Claude's custom sample counts.
- In Stage 3 Model C, Taskin Ahmed has 125 eligible bowling balls but a near-zero degenerate estimate with effectively zero reliability; it is not a positive pressure signal in this model. Hasan Mahmud has 74 balls and is below the 120-ball primary threshold.
- Claude's statement that the supplied pack cannot check M_perf / P_above_role_avg is not true of the complete frozen submission pack: `superr/final/output/FINAL_BATTERS.csv` and `FINAL_BOWLERS.csv` contain `M_total`, `P_above_role_avg`, component z-scores, pressure z and reliability. However, these Stage 4 fields are not the same as Claude's alternative rating.

### Auction calendar / registration status
- Reported BCCI timeline: player registration closes 23 Nov; franchises submit final player choices by 1 Dec; final auction register expected 3 Dec; mini-auction scheduled 16 Dec in Goa. Sources: https://www.cricbuzz.com/cricket-news/140762/bcci-extends-ipl-retention-deadline-to-november-17-cricbuzzcom and https://www.outlookindia.com/sports/cricket/ipl-2027-retention-deadline-extended-mini-auction-date-unchanged
- Do not label any target “auction confirmed” until the final register is published and checked. A board-level registration report is not the same as the final BCCI auction register.

### Practical auction stance
- Prioritise scarce high-quality bowling and only buy a batter if the role materially improves the best XI; don't spend merely because six slots exist.
- Treat Mustafizur as conditional on BCCI/BCB clarity; compare Taskin and Hasan on role, current form and actual registration rather than Claude's unverified composite alone.
- Treat Pathirana and Hasaranga as conditional on SLC fitness/NOC.
- Do not use Claude's estimated ceilings as market facts; retain them as negotiation hypotheses only.

## Phase and situation metrics addition (18 Nov 2026)
- Added player-level batting/bowling phase cards sourced from the supplied `Data Pack/ball_by_ball.csv` and joined to `matches.csv` / `competitions.csv`.
- Coverage: T20 and T20I, innings 1–2, dates present in the supplied file (2022-01-23 through 2026-11-01). This is not a complete career database and does not cover every domestic/franchise competition.
- Phases: powerplay overs 1–6, middle overs 7–15, death overs 16–20.
- Legal-ball denominator excludes wides and `Overstep` (no-ball) events. Dot = legal delivery with recorded total runs equal to zero. Boundary frequency = legal balls per four or six. Yorker = legal delivery coded exactly `Yorker`; wide yorkers and illegal deliveries are not counted. Per-six rates are raw counts divided by legal balls × 6.
- Batting cards show balls, strike rate, dots/6, sixes/6, fours/6 and balls per boundary by phase; situation splits include first innings, chase, vs pace and vs spin where data is present.
- Bowling cards show balls, recorded-run economy, dots/6, wickets/6, legal yorkers/6 and balls per boundary conceded by phase; situation splits include first innings and chase.
- No matching ball-by-ball record is explicitly marked unavailable. In particular Shahrukh Khan, Arab Gul Momand and Tristan Luus do not have matching rows in this supplied ball-by-ball file; no substitute statistics have been invented.
- These are descriptive rates, not adjusted for venue, opposition, role, sample size or current form. Small phase samples (especially Ackeem Auguste's 125 total balls in this file) should be treated cautiously. Bowling economy uses the dataset's `runs` field and is not independently reconciled to official scorecards.

## Navigation additions: released stars and 2026 absentees (18 Nov 2026)
Two new navigation views were added:
- **Released Stars:** curated high-profile 2027 release list with former team, role, prior contract value where reported, and availability/auction caveats. Prior contract values are not 2027 price forecasts.
- **2026 Absentees:** players who missed all or part of IPL 2026 due to injury, workload, administrative or personal reasons, with 2027 status and RR follow-up checks.

These lists are research trackers, not confirmed auction registers. Recheck the final BCCI registration list, current fitness, NOC and availability before any bid. Travis Head and Mitchell Starc are flagged as reported IPL 2027 opt-outs; MS Dhoni retired as a player and is not treated as an auction target. Retained players (e.g. Harshit Rana, Josh Hazlewood, Pat Cummins) are marked as not auction targets unless their status changes. Pakistan-qualified players remain excluded.

Research sources consulted: India Today IPL 2027 retention live list (17 Nov 2026); Wisden IPL 2027 retention list (17 Nov 2026); Reuters report on major releases and reported opt-outs (17 Nov 2026); Indian Express IPL 2026 injury/squad updates; NDTV IPL 2026 unavailable players; Cricbuzz IPL 2026 replacement rules and injury-replacement explainer. Where sources disagree or a player's 2027 registration is not established, the dashboard explicitly says to verify rather than treating them as available.


## Indian emerging additions (18 Nov 2026)

Added two Indian batting prospects: Ankit Kumar (SMAT 2025/26: 448 runs, avg 44.80, SR 172.31) and Salil Arora (358 runs in 8 innings, SR 198.88). Added two Indian bowling prospects: Yash Thakur (18 wickets in 7 SMAT matches, best 5/16) and Chama Milind (17 wickets in 9 SMAT matches).

Pressure evidence is deliberately separated from domestic form. Salil Arora has only 10 Stage 3 pressure-eligible balls (+0.36 per 100; 2.6% reliability); Yash Thakur has 78 (+0.19 per 100; 2.8% reliability). Both are below the 120-ball primary threshold and are not pressure-proven. Ankit Kumar and Chama Milind do not have a usable Stage 3 pressure row in the released candidate file. These four are emerging scouting additions based on domestic performance, not claims of proven clutch performance.

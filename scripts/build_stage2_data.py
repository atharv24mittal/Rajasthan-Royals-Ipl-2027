"""Builds data/stage2.json from Stage 1/2 AGGREGATE outputs and verifies headline numbers against the raw ball file.
Usage: python scripts/build_stage2_data.py <stage2_output_dir> [ball_by_ball.csv]   (raw file is read locally, never copied)"""
import sys, json, pandas as pd, os
o = sys.argv[1]; bbb = sys.argv[2] if len(sys.argv) > 2 else None
r = lambda f: pd.read_csv(f"{o}/{f}")
cc = r("coverage_competitions.csv"); vs = r("validation_summary.csv")
wp = json.load(open(f"{o}/wp_summary.json"))
sl = r("wp_situation_slices.csv"); pc = r("pressure_model_comparison.csv"); ex = r("pressure_exposure_coverage.csv"); g = r("pressure_grid_innings2.csv")
sp = lambda f: (lambda d: {"labels": list(d.iloc[:, 0]), "m": d.iloc[:, 1:].round(3).values.tolist(), "cols": list(d.columns[1:])})(pd.read_csv(f"{o}/{f}"))
sh = lambda f: r(f).rename(columns={"Unnamed: 0": "rule"}).round(3).to_dict("records")
tiers = cc.groupby("tier_label").agg(competitions=("comp_id", "count"), matches=("n_matches", "sum"), withBall=("n_with_ball_data", "sum"), deliveries=("n_deliveries", "sum"), usable=("n_full", "sum")).reset_index().to_dict("records")
by = r("coverage_tier_by_calendar_year.csv")
t2 = {f: r(f"validation_tests_stage2_{f}.csv") for f in ["eval", "features", "leakage", "pressure"]}
ok = lambda d: int(d.passed.astype(str).str.lower().isin(["true", "1", "pass"]).sum())
out = {"stage1": {"matches": int(cc.n_matches.sum()), "withBall": int(cc.n_with_ball_data.sum()), "regular": int(cc.n_deliveries.sum()), "usable": int(cc.n_full.sum()), "comps": int(len(cc)), "tiers": tiers, "tests": vs.status.value_counts().to_dict()},
 "stage2tests": {k: {"n": int(len(d)), "passed": ok(d)} for k, d in t2.items()},
 "wp": {"split": wp["split"], "test": wp["test_2026_train_2022_24"], "refit": wp["test_2026_refit_2022_25"], "ties": wp["sensitivities"]["ties_by_year"]},
 "slices": sl[["slice", "value", "n", "matches", "brier", "auc", "ece", "win_rate", "mean_p"]].round(4).to_dict("records"),
 "pcomp": pc.round(4).fillna("").to_dict("records"), "exposure": ex.to_dict("records"),
 "spBat": sp("rank_sensitivity_bat_spearman.csv"), "spBowl": sp("rank_sensitivity_bowl_spearman.csv"),
 "shBat": sh("rank_sensitivity_bat_split_half_noise_ceiling.csv"), "shBowl": sh("rank_sensitivity_bowl_split_half_noise_ceiling.csv"),
 "byYear": by.to_dict("records"),
 "grid": {"cols": list(g.columns), "rows": g.round(4).values.tolist()}}
if bbb and os.path.exists(bbb):
    b = pd.read_csv(bbb, usecols=["match_id", "innings", "overid"]); reg = b[b.innings.isin([1, 2])]
    ph = pd.cut(reg.overid, [0, 6, 15, 20], labels=["Powerplay", "Middle", "Death"]).value_counts()
    out["verify"] = {"rawRows": int(len(b)), "regularRows": int(len(reg)), "superOverRows": int(len(b) - len(reg)), "matchesInBall": int(b.match_id.nunique()), "phase": {k: int(ph[k]) for k in ["Powerplay", "Middle", "Death"]}}
    assert out["verify"]["regularRows"] == out["stage1"]["regular"], "regular delivery mismatch"
    print("VERIFIED", out["verify"])
json.dump(out, open("data/stage2.json", "w"), separators=(",", ":"))
print("written", os.path.getsize("data/stage2.json"), "bytes;", out["stage1"]["tests"], out["stage2tests"])

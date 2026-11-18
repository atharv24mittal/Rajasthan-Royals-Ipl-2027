"""Apply data/verified_public_record.json to data/players.js and data/player_research.csv. Idempotent.
Run from the project root:  python3 scripts/apply_verified_research.py
"""
import json, csv, io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(f"{ROOT}/data/verified_public_record.json", encoding="utf-8"))["players"]
HEAD = "// RR 2027 submission shortlist: complete schema for analytics and comparison renderers.\nwindow.P3 = "
s = open(f"{ROOT}/data/players.js", encoding="utf-8").read()
assert s.startswith(HEAD), "unexpected players.js header"
P = json.loads(s[len(HEAD):s.rindex("]") + 1])
FIELDS = ["country", "bat", "bowl", "ipl_teams", "ipl26", "strength", "risk", "source", "ipl26src", "record", "dob_note"]
changed = []
for p in P:
    v = V.get(p["name"])
    if not v: continue
    if "role" in v: p["role"] = v["role"]
    for k in FIELDS:
        if k in v and p["research"].get(k) != v[k]:
            p["research"][k] = v[k]; changed.append((p["name"], k))
open(f"{ROOT}/data/players.js", "w", encoding="utf-8").write(HEAD + json.dumps(P, indent=2, ensure_ascii=False) + ";\n")
print("players.js fields changed:", len(changed))

# CSV: keep the 14 rows for current players; move rows of displaced players to their own file; add the 6 new players
path = f"{ROOT}/data/player_research.csv"
raw = open(path, encoding="utf-8-sig", newline="").read()
rows = list(csv.DictReader(io.StringIO(raw))); cols = list(rows[0].keys())
cur = {p["name"]: p for p in P}
keep = [r for r in rows if r["player"] in cur]
gone = [r for r in rows if r["player"] not in cur]
have = {r["player"] for r in keep}
for p in P:
    if p["name"] in have: continue
    R = p["research"]
    keep.append({"player": p["name"], "type": p["kind"], "nationality": R["country"], "batting_style": R["bat"], "bowling_style": R["bowl"],
                 "ipl_franchise_history": R["ipl_teams"], "ipl_2026_summary": R["ipl26"], "scouting_strength": R["strength"], "risk_gate": R["risk"], "public_source": R["source"]})
for r in keep:   # refresh corrected fields for existing rows
    v = V.get(r["player"])
    if v:
        for a, b in (("nationality", "country"), ("batting_style", "bat"), ("bowling_style", "bowl"), ("ipl_franchise_history", "ipl_teams"), ("ipl_2026_summary", "ipl26")):
            if b in v: r[a] = v[b]
order = [p["name"] for p in P]; keep.sort(key=lambda r: order.index(r["player"]))
def dump(rs, f):
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\r\n"); w.writeheader(); w.writerows(rs)
with open(path, "w", encoding="utf-8", newline="") as f: dump(keep, f)
if gone:
    with open(f"{ROOT}/data/player_research_displaced_original_shortlist.csv", "w", encoding="utf-8", newline="") as f: dump(gone, f)
print("csv rows:", len(keep), "| displaced rows preserved separately:", len(gone))

"""Apply data/verified_public_record.json. Idempotent. Run from the project root:  python3 scripts/apply_verified_research.py
Updates: data/players.js, data/rr_2027_final_shortlist.json, data/emerging_gems.json, data/player_research.csv,
and the copies of the shortlist / emerging-gems data embedded in index.html."""
import json, csv, io, os, copy
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(f"{ROOT}/{p}", encoding="utf-8").read()
def wr(p, s): open(f"{ROOT}/{p}", "w", encoding="utf-8").write(s)
VJ = json.loads(rd("data/verified_public_record.json")); V = VJ["players"]; SLOTS = VJ.get("slot_replacements", {})
HEAD = "// RR 2027 submission shortlist: complete schema for analytics and comparison renderers.\nwindow.P3 = "
s = rd("data/players.js"); assert s.startswith(HEAD), "unexpected players.js header"
P = json.loads(s[len(HEAD):s.rindex("]") + 1])
FIELDS = ["country", "bat", "bowl", "ipl_teams", "ipl26", "strength", "risk", "source", "ipl26src", "record", "dob_note"]
removed = []

# 1) slot replacements: a new player takes over the slot of the old one with a blank (no Stage 3 data) record
for sid, n in SLOTS.items():
    i = next(k for k, p in enumerate(P) if p["id"] == sid)
    if P[i]["name"] == n["name"]: continue
    old = P[i]; removed.append(old)
    new = copy.deepcopy(old)
    assert old["degenerate"] and old["score"] is None, f"{old['name']} has Stage 3 data; refusing to overwrite"
    new.update({"name": n["name"], "role": n["role"], "img": n["img"], "age": n["age"], "date_of_birth": n["date_of_birth"], "age_as_of": "2026-11-18"})
    new["research"] = {k: "" for k in old["research"] if k not in ("record", "dob_note")}
    if n.get("placeholder"): new["placeholder"] = True
    else: new.pop("placeholder", None)
    P[i] = new

# 2) research fields
changed = 0
for p in P:
    v = V.get(p["name"])
    if not v: continue
    if "role" in v: p["role"] = v["role"]
    for k in FIELDS:
        if k in v and p["research"].get(k) != v[k]: p["research"][k] = v[k]; changed += 1
wr("data/players.js", HEAD + json.dumps(P, indent=2, ensure_ascii=False) + ";\n")
print("players.js: slots replaced", len(removed), "| research fields changed", changed)

# 3) final shortlist JSON + the copy embedded in index.html
FS = json.loads(rd("data/rr_2027_final_shortlist.json"))
for sid, n in SLOTS.items():
    lst = FS["batters" if sid.startswith("BAT") else "bowlers"]; idx = int(sid[3:]) - 1
    entry = {"name": n["name"], "country": n["country"], "role": n["role"], "stats": n["stats"], "status": n["status"], "age": n["age"], "age_as_of": "2026-11-18", "date_of_birth": n["date_of_birth"]}
    lst[idx] = entry
wr("data/rr_2027_final_shortlist.json", json.dumps(FS, indent=2, ensure_ascii=False) + "\n")

# 4) Ankit Kumar (Indian emerging list): add the supplied detail and mark auction registration unverified
EG = json.loads(rd("data/emerging_gems.json"))
for g in EG:
    if g["name"] == "Ankit Kumar":
        g["domestic_record"] = "448 runs · 11 innings · Avg 44.80 · SR 172.31 · HS 89 · 5 fifties · 49 fours · 22 sixes"
        g["role"] = "Top/middle-order batter"
        if "Auction registration" not in g["sample"]: g["sample"] = g["sample"].rstrip(". ") + ". Auction registration: unverified."
wr("data/emerging_gems.json", json.dumps(EG, indent=2, ensure_ascii=False) + "\n")
h = rd("index.html")
for key, obj in (("window.RR_FINAL_SHORTLIST=", FS), ("window.EMERGING_GEMS=", EG)):
    i = h.index(key) + len(key); _, end = json.JSONDecoder().raw_decode(h[i:])
    h = h[:i] + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + h[i + end:]
wr("index.html", h)

# 5) CSV: rows follow the current 20; rows of removed players are appended to the displaced file (never deleted)
path = f"{ROOT}/data/player_research.csv"
rows = list(csv.DictReader(io.StringIO(open(path, encoding="utf-8-sig", newline="").read()))); cols = list(rows[0].keys())
cur = {p["name"]: p for p in P}
keep = [r for r in rows if r["player"] in cur]; gone = [r for r in rows if r["player"] not in cur]; have = {r["player"] for r in keep}
for p in P:
    if p["name"] in have: continue
    R = p["research"]
    keep.append({"player": p["name"], "type": p["kind"], "nationality": R["country"], "batting_style": R["bat"], "bowling_style": R["bowl"], "ipl_franchise_history": R["ipl_teams"],
                 "ipl_2026_summary": R["ipl26"], "scouting_strength": R["strength"], "risk_gate": R["risk"], "public_source": R["source"]})
for r in keep:
    v = V.get(r["player"])
    if v:
        for a, b in (("nationality", "country"), ("batting_style", "bat"), ("bowling_style", "bowl"), ("ipl_franchise_history", "ipl_teams"), ("ipl_2026_summary", "ipl26")):
            if b in v: r[a] = v[b]
order = [p["name"] for p in P]; keep.sort(key=lambda r: order.index(r["player"]))
def dump(rs, f): w = csv.DictWriter(f, fieldnames=cols, lineterminator="\r\n"); w.writeheader(); w.writerows(rs)
with open(path, "w", encoding="utf-8", newline="") as f: dump(keep, f)
dp = f"{ROOT}/data/player_research_displaced_original_shortlist.csv"
prev = list(csv.DictReader(open(dp, encoding="utf-8", newline=""))) if os.path.exists(dp) else []
names = {r["player"] for r in prev}; add = [r for r in gone if r["player"] not in names]
if add or not os.path.exists(dp):
    with open(dp, "w", encoding="utf-8", newline="") as f: dump(prev + add, f)
print("csv rows:", len(keep), "| appended to displaced file:", len(add))

"""Scan every view and all 20 dossiers for placeholder leaks and degenerate-score display. Usage: qa_data_probe.py <url>"""
import sys, re, json
from playwright.sync_api import sync_playwright
URL = sys.argv[1]; BAD = re.compile(r"\bNaN\b|undefined|\bnull\b|\[object|Infinity|\bTODO\b|lorem ipsum", re.I)
TABS = ["Overview", "Pressure history", "Match evidence", "Scouting assessment"]
def dossier_text(pg, pid):
    pg.evaluate("show(5)"); pg.wait_for_timeout(300); pg.click(f"[data-open='{pid}']"); pg.wait_for_timeout(450)
    out = []
    for t in TABS:
        pg.click(f"#dos [data-t='{t}']"); pg.wait_for_timeout(250); out.append(pg.evaluate("document.querySelector('#dos').innerText"))
    pg.click("#dos button:has-text('Career & IPL')"); pg.wait_for_timeout(350); out.append(pg.evaluate("document.querySelector('#dos').innerText"))
    return "\n".join(out)
res = []
def ok(n, c, d=""):
    res.append({"name": n, "pass": bool(c), "detail": str(d)}); print(("PASS " if c else "FAIL ") + n, ("| " + str(d)[:300]) if d and not c else "")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(URL); pg.wait_for_selector("#enter"); pg.click("#enter"); pg.wait_for_timeout(1200)
    for i in range(15):
        pg.evaluate(f"show({i})"); pg.wait_for_timeout(900)
        t = pg.evaluate("document.querySelector('#main').innerText"); m = BAD.findall(t)
        ok(f"view {i}: no placeholder leaks (NaN/undefined/null/[object])", not m, m[:5])
    ids = pg.evaluate("PL.map(p=>p.id)"); ok("PL has 20 players", len(ids) == 20, len(ids))
    for pid in ids:
        txt = dossier_text(pg, pid); name = pg.evaluate(f"PL.find(p=>p.id=='{pid}').name")
        deg = pg.evaluate(f"!!PL.find(p=>p.id=='{pid}').degenerate")
        ok(f"dossier {pid} {name}: full name in heading", name.upper() in txt.upper().replace("\n"," ").replace("  "," ") or all(w.upper() in txt.upper() for w in name.split()))
        ok(f"dossier {pid}: no placeholder leaks", not BAD.findall(txt), BAD.findall(txt)[:5])
        if deg:
            ok(f"dossier {pid} {name}: degenerate score shown as N/A, not a number", "N/A" in txt and not re.search(r"Pressure rating\s*[+\-]?0\.00", txt))
        pg.keyboard.press("Escape"); pg.wait_for_timeout(200)

    # ---- REG-05: corrected research data (no copied template values) ----
    EXPECT = {  # name: (must contain, must NOT contain)
        "Ackeem Auguste": (["West Indies", "Left-hand bat", "Verified public record", "385 runs"], ["10 matches · 278 runs", "ipl.com/player/pathum-nissanka"]),
        "Sediqullah Atal": (["Afghanistan", "Left-hand bat", "MI Cape Town", "Verified public record"], ["10 matches · 278 runs", "ipl.com/player/pathum-nissanka"]),
        "Salil Arora": (["Sunrisers Hyderabad", "125* off 45", "Verified public record"], ["Delhi Capitals (2026)", "10 matches · 278 runs"]),
        "Tristan Luus": (["South Africa", "conflicting", "MI Cape Town", "Verified public record"], ["Lucknow Super Giants (2026)", "Royal Challengers Bengaluru (2021"]),
        "Yash Thakur": (["Punjab Kings", "77.5 overs", "Verified public record"], ["Royal Challengers Bengaluru (2021"]),
        "Chama Milind": (["Left-hand bat", "No IPL match played", "104 wickets", "Verified public record"], ["Lucknow Super Giants (2026)", "Right-arm legbreak"]),
        "Pathum Nissanka": (["Sri Lanka", "278 runs"], []),
        "Wanindu Hasaranga": (["Sri Lanka", "hamstring", "Rajasthan Royals (2025)", "Lucknow Super Giants (2026)"], ["Right-arm medium"]),
    }
    for name, (must, mustnt) in EXPECT.items():
        pid = pg.evaluate(f"PL.find(p=>p.name=='{name}').id")
        txt = dossier_text(pg, pid)
        for m in must: ok(f"REG-05 {name}: shows '{m}'", m.lower() in txt.lower())
        for m in mustnt: ok(f"REG-05 {name}: no copied value '{m.strip()}'", m.lower() not in txt.lower())
        if name in ("Ackeem Auguste","Sediqullah Atal","Salil Arora","Tristan Luus","Yash Thakur","Chama Milind"):
            links = pg.evaluate("[...document.querySelectorAll('#dos table a')].map(a=>a.href)")
            ok(f"REG-05 {name}: every record link is https and external", links and all(l.startswith("https://") for l in links), links[:2])
        pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    b.close()
print("TOTAL", sum(r["pass"] for r in res), "/", len(res)); json.dump(res, open("qa/v5/data-probe.json", "w"), indent=1)

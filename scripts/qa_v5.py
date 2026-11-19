"""QA v5 crawler. Usage: qa_v5.py <url> <outdir>. Every PASS/FAIL line is an executed check against the live page."""
import sys, json, os
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
VPS = [] if os.environ.get("QA_REG_ONLY") else [int(x) for x in os.environ.get("QA_VPS","360,390,430,768,1024,1280,1440,1920").split(",")]
HEIGHT = {360: 740, 390: 844, 430: 932, 768: 1024, 1024: 768, 1280: 800, 1440: 900, 1920: 1080}
SHOT = {1440, 390}
res = []
def ok(name, cond, detail=""):
    res.append({"name": name, "pass": bool(cond), "detail": str(detail)})
    print(("PASS " if cond else "FAIL ") + name, ("| " + str(detail)) if detail and not cond else "")
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in VPS:
        pg = b.new_page(viewport={"width": w, "height": HEIGHT[w]})
        errs, bad_req = [], []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERR " + str(e)))
        pg.on("requestfailed", lambda r: bad_req.append(r.url[-70:]))
        pg.on("response", lambda r: bad_req.append(f"{r.status} {r.url[-70:]}") if r.status >= 400 else None)
        pg.goto(URL); pg.wait_for_selector("#enter", timeout=15000); pg.wait_for_timeout(600)
        pg.click("#enter"); pg.wait_for_timeout(1500)
        ok(f"{w}: landing closes, app visible", pg.locator("#open").count() == 0 and pg.locator("#main .view").count() == 1)
        n = pg.evaluate("document.querySelectorAll('#nav button').length")
        ok(f"{w}: 15 nav items present", n == 15, n)
        for i in range(n):
            if w < 900:
                pg.evaluate("document.querySelector('#mb')&&document.querySelector('#mb').offsetParent&&!document.querySelector('#mm.on')&&document.querySelector('#mb').click()"); pg.wait_for_timeout(150)
                btn = pg.locator("#mm button, #mm [data-nav]").nth(i) if pg.locator("#mm button, #mm [data-nav]").count() > i else pg.locator("#nav button").nth(i)
            else:
                btn = pg.locator("#nav button").nth(i)
            label = pg.evaluate(f"document.querySelectorAll('#nav button')[{i}].textContent.trim()")
            try:
                btn.click(timeout=4000)
            except Exception as e:
                ok(f"{w}: click nav '{label}'", False, str(e)[:120]); continue
            pg.wait_for_timeout(900)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            ok(f"{w}: '{label}' no horizontal overflow", sw <= w + 1, sw)
            ok(f"{w}: '{label}' renders content", pg.evaluate("document.querySelector('#main').innerText.trim().length") > 200)
            h = pg.evaluate("[...document.querySelectorAll('#main h1,#main h2')].length")
            ok(f"{w}: '{label}' has heading", h >= 1, h)
            if w in SHOT: pg.screenshot(path=f"{OUT}/{w}-{i:02d}-{label.replace(' ', '_')}.png")
        pg.wait_for_timeout(500)
        broken = pg.evaluate("[...document.images].filter(i=>i.complete&&i.naturalWidth==0&&i.src).map(i=>i.src.slice(-50))")
        ok(f"{w}: no broken images", not broken, broken)
        ok(f"{w}: no console errors", not errs, "; ".join(errs[:3]))
        ok(f"{w}: no failed requests", not bad_req, "; ".join(bad_req[:3]))
        pg.close()

    if os.environ.get("QA_SKIP_REG"):
        b.close(); json.dump(res, open(f"{OUT}/results.json", "w"), indent=1)
        print("TOTAL", sum(r["pass"] for r in res), "/", len(res)); sys.exit(0)
    # ---------- regression tests for fixed bugs ----------
    for w in (1440, 390, 1024):
        pg = b.new_page(viewport={"width": w, "height": HEIGHT[w]}); reqs = []
        pg.on("response", lambda r: reqs.append((r.status, r.url)))
        pg.goto(URL); pg.wait_for_selector("#enter"); pg.click("#enter"); pg.wait_for_timeout(1200)
        pg.evaluate("show(12)"); pg.wait_for_timeout(1200)
        # REG-01: international prospects have no portraits -> explicit placeholder, no 404 request
        ph = pg.evaluate("[...document.querySelectorAll('#main .pimg.mono')].length")
        ok(f"REG-01 {w}: 15 international prospects + Gerald Coetzee use labelled placeholder", ph == 16, ph)
        ok(f"REG-01 {w}: placeholders expose accessible name", pg.evaluate("[...document.querySelectorAll('#main .pimg.mono')].every(e=>/No portrait available for/.test(e.getAttribute('aria-label')||''))"))
        ok(f"REG-01 {w}: no 4xx/5xx asset requests in Emerging Gems", not [r for r in reqs if r[0] >= 400], [r for r in reqs if r[0] >= 400][:3])
        # REG-03: the 20 submitted players show 20 distinct loaded portraits
        for y in range(0, pg.evaluate("document.body.scrollHeight") + 900, 700): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(120)
        pg.wait_for_timeout(600)
        imgs = pg.evaluate("[...document.querySelectorAll('#main img.pimg')].map(i=>({s:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0}))")
        srcs = [i['s'] for i in imgs]
        ok(f"REG-03 {w}: submitted-player portraits all load", imgs and all(i['ok'] for i in imgs), [i['s'] for i in imgs if not i['ok']][:3])
        ok(f"REG-03 {w}: no duplicate portrait among submitted players", len(set(srcs)) == len(srcs), len(srcs) - len(set(srcs)))
        # REG-02: long badges must wrap, never push the page wider than the viewport
        pg.evaluate("show(1)"); pg.wait_for_timeout(1200)
        ok(f"REG-02 {w}: Pressure Intelligence no horizontal overflow", pg.evaluate("document.documentElement.scrollWidth") <= w + 1, pg.evaluate("document.documentElement.scrollWidth"))
        pg.close()

    # REG-04: official logo shown undistorted on landing + app chrome
    for w in (360, 390, 1024, 1440):
        pg = b.new_page(viewport={"width": w, "height": HEIGHT[w]})
        pg.goto(URL); pg.wait_for_selector("#enter"); pg.wait_for_timeout(1500)
        geo = lambda sel: pg.evaluate("(s)=>{const i=document.querySelector(s);if(!i)return null;const r=i.getBoundingClientRect();return {w:r.width,h:r.height,nw:i.naturalWidth,nh:i.naturalHeight,vis:r.width>0}}", sel)
        g = geo("#open .rrlogo img")
        ok(f"REG-04 {w}: landing logo loads", g and g["nw"] == 97 and g["nh"] == 148, g)
        ok(f"REG-04 {w}: landing logo not distorted (aspect within 1.5%)", g and abs((g["w"] / g["h"]) / (97 / 148) - 1) < 0.015, g)
        pg.screenshot(path=f"{OUT}/landing-{w}.png")
        pg.click("#enter"); pg.wait_for_timeout(1500)
        sel = "aside .rrlogo img" if w >= 1000 else ".top .rrlogo img"
        g = geo(sel)
        ok(f"REG-04 {w}: app-chrome logo loads and undistorted", g and g["nw"] == 97 and g["vis"] and abs((g["w"] / g["h"]) / (97 / 148) - 1) < 0.02, g)
        ok(f"REG-04 {w}: no horizontal overflow with logo", pg.evaluate("document.documentElement.scrollWidth") <= w + 1, pg.evaluate("document.documentElement.scrollWidth"))
        pg.screenshot(path=f"{OUT}/chrome-{w}.png")
        pg.close()
    b.close()
json.dump(res, open(f"{OUT}/results.json", "w"), indent=1)
print("TOTAL", sum(r["pass"] for r in res), "/", len(res))

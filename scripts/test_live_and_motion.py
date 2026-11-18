"""(1) Stage 3 data-contract test: a TEST FIXTURE (not shipped, not real) injected as window.P3 must switch the app to verified mode.
(2) prefers-reduced-motion test. Usage: test_live_and_motion.py <url>"""
import sys, json
from playwright.sync_api import sync_playwright
URL=sys.argv[1]; res=[]
def ok(n,c,x=""): res.append((n,bool(c))); print(("PASS " if c else "FAIL ")+n,x)
FIX="window.P3="+json.dumps([{"id":f"TEST-{k:02d}","name":f"Test Fixture {k:02d}","kind":"bat" if k<=6 else "bowl","role":"Opener","sample":300+k*10,"pressureSample":120+k,"score":round(3-k*.4,2),"lo":round(2-k*.4,2),"hi":round(4-k*.4,2),"reliability":60+k,"consistency":50+k,"phase":[1.0,-.5,.8],"competition":[100,150,10],"dot":35.0,"primary":130.0,"timeline":[[1,2,3,-1],[0,1],[2],[1],[3]]} for k in range(1,13)])+";"
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={"width":1440,"height":900});ctx.add_init_script(FIX);pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL);pg.wait_for_timeout(600);pg.click("#skip");pg.wait_for_timeout(900);pg.evaluate("show(2)");pg.wait_for_timeout(1200)
    t=pg.locator("#main").inner_text()
    ok("LIVE: verified note shown, no preview switch",pg.locator("[data-pv]").count()==0 and "VERIFIED STAGE 3" in t.upper())
    ok("LIVE: ranks and scores rendered without 'synthetic' wording","synthetic" not in t.lower() and "+2.60" in t,t[:0])
    ok("LIVE: stripe/watermark off",pg.locator("body.pv-on").count()==0)
    pg.locator("[data-open]").first.click();pg.wait_for_timeout(1300);dt=pg.locator("#dos").inner_text()
    ok("LIVE: dossier shows verified, no 'Fictional demo' badge","VERIFIED" in dt.upper() and "FICTIONAL DEMO" not in dt.upper().replace("FICTIONAL DEMO PROFILE","")),
    pg.keyboard.press("Escape");pg.wait_for_timeout(900);pg.evaluate("show(4)");pg.wait_for_timeout(900);ok("LIVE: comparison renders radar",pg.locator("#cmp svg[aria-label^='Radar']").count()==1)
    ok("LIVE: no page errors",len(errs)==0,"; ".join(errs[:2]));ctx.close()
    rc=b.new_context(viewport={"width":1440,"height":900},reduced_motion="reduce");pg=rc.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto(URL);pg.wait_for_timeout(500)
    ok("RM: intro final state shown immediately (headline visible at 500ms)",pg.evaluate("getComputedStyle(document.querySelector('#open .ln span')).opacity")=="1")
    pg.click("#enter");pg.wait_for_timeout(500);ok("RM: app opens without iris animation",pg.locator("#open").count()==0)
    ok("RM: counters at final value instantly",pg.evaluate("[...document.querySelectorAll('.kband [data-c]')].map(e=>e.textContent).join()")=="883,200,961,811,138")
    pg.evaluate("show(1)");pg.wait_for_timeout(1200);ok("RM: heatmap fully visible",pg.evaluate("parseFloat(getComputedStyle(document.querySelector('#hs .hmc')).opacity)>0.5"))
    ok("RM: reveal elements visible",pg.evaluate("[...document.querySelectorAll('.rv')].every(e=>getComputedStyle(e).opacity=='1')"))
    ok("RM: no page errors",len(errs)==0,"; ".join(errs[:2]));b.close()
print("TOTAL",sum(1 for r in res if r[1]),"/",len(res));json.dump(res,open("reports/live_motion.json","w"))

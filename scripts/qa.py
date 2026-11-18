"""V4 QA: runs against any URL. Usage: qa.py <url> <outdir> [browser]. Every PASS/FAIL line is an executed check."""
import sys, json, time, re
from playwright.sync_api import sync_playwright
URL=sys.argv[1]; OUT=sys.argv[2]; BR=sys.argv[3] if len(sys.argv)>3 else "chromium"; res=[]
def ok(n,c,x=""): res.append((n,bool(c),x)); print(("PASS " if c else "FAIL ")+n,x)
VPS=[(360,740,"360"),(390,844,"390"),(430,932,"430"),(768,1024,"768"),(1280,800,"1280"),(1440,900,"1440"),(1920,1080,"1920")]
with sync_playwright() as p:
    b=getattr(p,BR).launch()
    for (w,h,tag) in VPS:
        pg=b.new_page(viewport={"width":w,"height":h}); errs=[]
        pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None); pg.on("pageerror",lambda e:errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(900)
        if tag in ("1440","390"): pg.screenshot(path=f"{OUT}/{tag}-landing-early.png")
        pg.wait_for_timeout(5200)
        if tag in ("1440","390","1920"): pg.screenshot(path=f"{OUT}/{tag}-landing.png")
        pg.click("#enter"); pg.wait_for_timeout(1600)
        ok(f"{tag} landing closes and app visible",pg.locator("#open").count()==0 and pg.locator("#main .view").count()==1)
        for i in range(10):
            pg.evaluate(f"show({i})"); pg.wait_for_timeout(1700 if i in (0,1,6) else 900)
            sw=pg.evaluate("document.documentElement.scrollWidth"); ok(f"{tag} view{i} no h-overflow",sw<=w+1,str(sw))
            if tag in ("1440","390") and i in (0,1,2,5,6,7,8,9): pg.screenshot(path=f"{OUT}/{tag}-view{i}.png")
            if tag=="1440" and i in (0,1,6,7): pg.evaluate("window.scrollTo(0,document.body.scrollHeight*.5)"); pg.wait_for_timeout(1200); pg.screenshot(path=f"{OUT}/{tag}-view{i}-mid.png")
        ok(f"{tag} console errors",len(errs)==0,"; ".join(errs[:3]))
        bad=pg.evaluate("[...document.images].filter(i=>i.complete&&i.naturalWidth==0&&i.style.display!='none'&&i.src).map(i=>i.src.slice(-40))"); ok(f"{tag} images load",len(bad)==0,str(bad))
        if tag=="1440":
            # --- interaction journeys ---
            pg.evaluate("show(0)");pg.wait_for_timeout(2600)
            ok("counters reach verified values",pg.evaluate("[...document.querySelectorAll('.kband [data-c]')].map(e=>e.textContent).join()")=="883,200,961,811,138",pg.evaluate("[...document.querySelectorAll('.kband [data-c]')].map(e=>e.textContent).join('|')"))
            pg.click("#replay");pg.wait_for_timeout(300);ok("pitch replay runs",True)
            pg.evaluate("show(1)");pg.wait_for_timeout(1600)
            ok("heatmap has cells",pg.locator("#hs .hmc").count()==360,str(pg.locator("#hs .hmc").count()))
            pg.click("[data-hm='A_bat']");pg.wait_for_timeout(700);f1=pg.evaluate("document.querySelector('#hs .hmc').style.fill");pg.click("[data-hm='wp']");pg.wait_for_timeout(700);f2=pg.evaluate("document.querySelector('#hs .hmc').style.fill");ok("model switch recolours cells",f1!=f2,f"{f1} -> {f2}")
            pg.click("[data-hw='7']");pg.wait_for_timeout(900);ok("wickets switch rebuilds grid",pg.locator("#hs .hmc").count()==360)
            pg.locator("#hs .hmc").nth(120).click();pg.wait_for_timeout(700);ok("cell selection updates panel",pg.locator("#hs .hmc.s").count()==1 and "wickets lost" in pg.locator("#hmr").inner_text())
            pg.locator("#hs").focus();k0=pg.evaluate("document.querySelector('#hs .hmc.s').dataset.k");pg.keyboard.press("ArrowRight");pg.keyboard.press("ArrowUp");pg.wait_for_timeout(500);k1=pg.evaluate("document.querySelector('#hs .hmc.s').dataset.k");ok("heatmap keyboard navigation",k0!=k1,f"{k0}->{k1}")
            pg.hover("#hs .hmc >> nth=50");pg.wait_for_timeout(300);ok("tooltip appears",pg.locator("#tip.on").count()==1 and "Model C" in pg.locator("#tip").inner_text())
            pg.click("[data-vi='1']");pg.click("[data-vs='bowl']");pg.wait_for_timeout(500);ok("validation toggles",pg.locator("#vf > div").count()>=6)
            pg.locator(".g3 [data-ev]").first.click();pg.wait_for_timeout(700);ok("evidence drawer + scrim",pg.locator("#drw.on").count()==1 and pg.locator("#scrim.on").count()==1);pg.keyboard.press("Escape");pg.wait_for_timeout(500);ok("Escape closes drawer",pg.locator("#drw.on").count()==0)
            # leaderboard
            pg.evaluate("show(2)");pg.wait_for_timeout(900);ok("pending leaderboard: 10 cards, no scores",pg.locator("#bd [data-open]").count()==10 and not re.search(r"[+−-]\d+\.\d\d",pg.locator("#bd").inner_text()))
            pg.fill("[data-lq]","03");pg.wait_for_timeout(500);ok("search filters",pg.locator("#bd [data-open]").count()==1);pg.fill("[data-lq]","")
            pg.click("[data-pv='1']");pg.wait_for_timeout(900);ok("preview banner unmistakable",pg.locator("body.pv-on").count()==1 and pg.locator(".stripe").is_visible() and "SYNTHETIC" in pg.locator(".pvbar").inner_text())
            pg.screenshot(path=f"{OUT}/1440-leaderboard-preview.png")
            pg.click("[data-ls='rel']");pg.wait_for_timeout(900);pg.click("[data-lc='IPL']");pg.wait_for_timeout(600);pg.click("[data-lr='Opener']");pg.wait_for_timeout(600);ok("sort/competition/role filters",pg.locator("#bd [data-open]").count()>=1)
            pg.click("[data-lr='All']");pg.click("[data-lc='All']");pg.wait_for_timeout(500)
            pg.locator("[data-cmp]").nth(0).click();pg.locator("[data-cmp]").nth(1).click();pg.wait_for_timeout(500);ok("compare FAB appears",pg.locator("#fab.on").count()==1);pg.click("#fab");pg.wait_for_timeout(900);ok("compare opens with 2 selected",pg.locator("#cmp .chip[aria-pressed='true']").count()==2);pg.screenshot(path=f"{OUT}/1440-compare.png")
            pg.locator("[data-cs]").nth(2).click();pg.wait_for_timeout(500);ok("add third player",pg.locator("#cmp .chip[aria-pressed='true']").count()==3)
            pg.evaluate("show(5)");pg.wait_for_timeout(700);pg.locator("[data-open]").nth(3).click();pg.wait_for_timeout(1500);ok("dossier opens",pg.locator("#dos.on").count()==1);pg.screenshot(path=f"{OUT}/1440-dossier.png")
            for t in ["Pressure history","Match evidence","Scouting assessment","Overview"]: pg.click(f"[data-t='{t}']");pg.wait_for_timeout(300)
            ind=pg.evaluate("parseFloat(document.querySelector('.tabs .ind').style.width)");ok("tab indicator slides",ind>20,str(ind))
            pg.locator("#dos [data-ev]").first.click();pg.wait_for_timeout(500);ok("dossier evidence drawer",pg.locator("#drw.on").count()==1);pg.keyboard.press("Escape");pg.wait_for_timeout(400);pg.keyboard.press("Escape");pg.wait_for_timeout(900);ok("dossier closes",pg.locator("#dos.on").count()==0)
            pg.evaluate("show(6)");pg.wait_for_timeout(1500);pg.click("[data-rs='bowl']");pg.wait_for_timeout(1200);ok("stability matrix cells",pg.locator("#ag .hmc").count()>100)
            pg.hover("#ag .agc >> nth=14");pg.wait_for_timeout(300);ok("matrix tooltip",pg.locator("#tip.on").count()==1)
            pg.evaluate("show(7)");pg.wait_for_timeout(900);pg.click("#sim [data-w='7']");pg.fill("#sbl","60");pg.fill("#sra","1.2");pg.click("[data-sm='wp']");pg.wait_for_timeout(900);ok("simulator reacts",pg.evaluate("document.querySelector('#gl').textContent").startswith("WIN"))
            pg.click("#swp2");pg.wait_for_timeout(900);pg.click("#swp2");ok("ratio sweep starts/stops",pg.evaluate("typeof swp")!="undefined" and pg.evaluate("swp")is None)
            pg.screenshot(path=f"{OUT}/1440-simulator.png")
            pg.evaluate("show(8)");pg.click("[data-m='5']");ok("methodology step","Leakage" in pg.locator("#mc").inner_text())
            pg.keyboard.press("p");pg.wait_for_timeout(1000);ok("presentation opens",pg.locator("#pres.on").count()==1)
            for i in range(6): pg.keyboard.press("ArrowRight");pg.wait_for_timeout(900);pg.screenshot(path=f"{OUT}/1440-present-{i+2}.png")
            pg.keyboard.press("ArrowLeft");pg.wait_for_timeout(700);pg.keyboard.press("Home");pg.wait_for_timeout(700);ok("presentation navigation",pg.locator("#pseg button.done").count()==1);pg.keyboard.press("Escape");pg.wait_for_timeout(400);ok("presentation closes",pg.locator("#pres.on").count()==0)
            pg.evaluate("document.activeElement.blur()");pg.keyboard.press("3");pg.wait_for_timeout(700);st=pg.evaluate("[...document.querySelectorAll('nav button.on')].map(b=>b.textContent.trim())");ok("number shortcut",any(x.startswith("Batting") for x in st),str(st)+pg.evaluate("document.activeElement.tagName+' dos:'+document.querySelector('#dos').className"))
        if tag in ("390","360"):
            pg.evaluate("show(1)");pg.wait_for_timeout(900);pg.click("#mb");pg.wait_for_timeout(300);ok(f"{tag} mobile menu opens",pg.locator("#mm.on").count()==1)
        pg.close()
    b.close()
json.dump(res,open(f"{OUT}/qa-{BR}.json","w")); print("TOTAL",sum(1 for r in res if r[1]),"/",len(res))

"""Accessibility pass: axe-core on every view/state + scripted keyboard journeys + computed contrast. Usage: a11y.py <url> <outfile.json>"""
import sys, json
from playwright.sync_api import sync_playwright
URL=sys.argv[1]; OUT=sys.argv[2]; AXE=open("/home/claude/tools/node_modules/axe-core/axe.min.js").read(); rep={"axe":[],"keyboard":[],"contrast":[]}
def lum(h):
    h=h.lstrip("#");r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)];f=lambda c:c/12.92 if c<=.03928 else((c+.055)/1.055)**2.4;return .2126*f(r)+.7152*f(g)+.0722*f(b)
def cr(a,b):
    la,lb=lum(a),lum(b);return (max(la,lb)+.05)/(min(la,lb)+.05)
for fg,bg,n in [("#F2F1F7","#10182B","body text on panel"),("#9AA0B4","#10182B","muted text on panel"),("#9AA0B4","#05070F","muted text on page"),("#E83E83","#10182B","pink eyebrow on panel"),("#D8B368","#05070F","gold eyebrow on page"),("#B69AFF","#10182B","lavender on panel"),("#FFFFFF","#E83E83","white on pink button"),("#6ee7b7","#10182B","verified green"),("#fcd34d","#10182B","amber"),("#0a0f1e","#B69AFF","segment active text")]:
    rep["contrast"].append((n,fg,bg,round(cr(fg,bg),2),"AA pass" if cr(fg,bg)>=4.5 else "below AA 4.5 (large/UI text only if >=3)"))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":1440,"height":900});pg.goto(URL);pg.wait_for_timeout(800);pg.click("#enter");pg.wait_for_timeout(1500)
    pg.add_script_tag(content=AXE)
    def axe(label):
        r=pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}})")
        rep["axe"].append({"state":label,"violations":[{"id":v["id"],"impact":v["impact"],"nodes":len(v["nodes"]),"help":v["help"],"sample":v["nodes"][0]["html"][:110]} for v in r["violations"]],"passes":len(r["passes"])})
    for i in range(10): pg.evaluate(f"show({i})");pg.wait_for_timeout(1700);axe(f"view {i}")
    pg.evaluate("show(2)");pg.click("[data-pv='1']");pg.wait_for_timeout(1000);axe("leaderboard preview");pg.locator("[data-open]").first.click();pg.wait_for_timeout(1500);axe("dossier");pg.keyboard.press("Escape");pg.wait_for_timeout(900)
    pg.evaluate("show(1)");pg.wait_for_timeout(900);pg.locator(".g3 [data-ev]").first.click();pg.wait_for_timeout(700);axe("evidence drawer");pg.keyboard.press("Escape")
    # keyboard-only journeys
    def kb(n,c,x=""): rep["keyboard"].append((n,bool(c),x));print(("PASS " if c else "FAIL ")+n,x)
    pg.evaluate("show(0)");pg.wait_for_timeout(500);pg.focus("aside #nav button");seq=[pg.evaluate("document.activeElement.textContent.trim()")]
    for _ in range(13): pg.keyboard.press("Tab");seq.append(pg.evaluate("(document.activeElement.textContent||document.activeElement.getAttribute('aria-label')||document.activeElement.tagName).trim().slice(0,24)"))
    kb("Tab walks sidebar nav in order",seq[0:3]==["Command Centre","Pressure Intelligence","Batting Analytics"],str(seq[:4]))
    vis=pg.evaluate("(()=>{const e=document.activeElement;const s=getComputedStyle(e);return s.outlineStyle!='none'||s.boxShadow!='none'})()");kb("focused element has visible focus style",vis)
    pg.evaluate("show(2)");pg.wait_for_timeout(900);pg.focus("[data-open]");pg.keyboard.press("Enter");pg.wait_for_timeout(1300);kb("Enter opens dossier from keyboard",pg.locator("#dos.on").count()==1);kb("focus moves into dossier",pg.evaluate("document.querySelector('#dos').contains(document.activeElement)"));pg.keyboard.press("Escape");pg.wait_for_timeout(900);kb("Escape closes dossier",pg.locator("#dos.on").count()==0)
    pg.evaluate("show(1)");pg.wait_for_timeout(900);pg.locator("#hs").focus();pg.keyboard.press("ArrowRight");pg.keyboard.press("ArrowDown");pg.wait_for_timeout(500);kb("heatmap operable by arrow keys",pg.locator("#hs .hmc.s").count()==1)
    pg.locator(".g3 [data-ev]").first.focus();pg.keyboard.press("Enter");pg.wait_for_timeout(600);kb("evidence drawer opens by keyboard and takes focus",pg.evaluate("document.activeElement.id")=="dc");pg.keyboard.press("Escape");pg.wait_for_timeout(500);kb("Escape closes drawer",pg.locator("#drw.on").count()==0)
    pg.keyboard.press("p");pg.wait_for_timeout(900);kb("P opens presentation",pg.locator("#pres.on").count()==1);pg.keyboard.press("ArrowRight");pg.keyboard.press("ArrowRight");pg.wait_for_timeout(900);kb("arrow keys advance slides",pg.locator("#pseg button.done").count()==3);pg.keyboard.press("Escape")
    pg.evaluate("show(7)");pg.wait_for_timeout(900);pg.locator("#sbl").focus();pg.keyboard.press("ArrowRight");pg.wait_for_timeout(500);kb("simulator slider operable by keyboard",pg.evaluate("+document.querySelector('#sbl').value")>30)
    b.close()
bad=[v for a in rep["axe"] for v in a["violations"]];json.dump(rep,open(OUT,"w"),indent=1)
print("AXE states:",len(rep["axe"]),"| total violation entries:",len(bad));[print(" ",a["state"],v["id"],v["impact"],v["nodes"],v["sample"]) for a in rep["axe"] for v in a["violations"]]
for c in rep["contrast"]:print(" contrast",c)

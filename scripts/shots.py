"""Screenshots of every section at desktop (1440) and mobile (390) from the FINAL standalone, plus a recorded walkthrough."""
import sys, os
from playwright.sync_api import sync_playwright
U=sys.argv[1]; NAMES=["command-centre","pressure-intelligence","batting","bowling","comparison","dossiers","ranking-stability","match-simulator","methodology","data-integrity"]
with sync_playwright() as p:
    b=p.chromium.launch()
    for (w,h,tag) in [(1440,900,"desktop"),(390,844,"mobile")]:
        pg=b.new_page(viewport={"width":w,"height":h});pg.goto(U);pg.wait_for_timeout(6200);pg.screenshot(path=f"screenshots/{tag}-00-landing.png");pg.click("#enter");pg.wait_for_timeout(1500)
        for i,n in enumerate(NAMES):
            pg.evaluate(f"show({i})");pg.wait_for_timeout(2300 if i in (0,1,6,7) else 1300)
            if i==1:
                pg.evaluate("document.querySelector('#inst').scrollIntoView({block:'start'})");pg.wait_for_timeout(900);pg.locator("#hs .hmc").nth(150).click();pg.wait_for_timeout(900)
            if i==4: pg.evaluate("document.querySelector('[data-pv]').click()");pg.wait_for_timeout(900)
            pg.screenshot(path=f"screenshots/{tag}-{i+1:02d}-{n}.png")
            if i in (2,): pg.evaluate("document.querySelector('[data-pv=\"1\"]').click()");pg.wait_for_timeout(1100);pg.screenshot(path=f"screenshots/{tag}-03b-batting-layout-preview.png");pg.evaluate("show(0)")
            if i==5:
                pg.evaluate("document.querySelector('[data-open]').click()");pg.wait_for_timeout(1500);pg.screenshot(path=f"screenshots/{tag}-06b-player-dossier.png");pg.keyboard.press("Escape");pg.wait_for_timeout(800)
        pg.evaluate("document.querySelector('#pbtn')?.click()||document.querySelector('#pb2')?.click()") if tag=="desktop" else None
        if tag=="desktop":
            pg.wait_for_timeout(900);pg.keyboard.press("ArrowRight");pg.keyboard.press("ArrowRight");pg.keyboard.press("ArrowRight");pg.keyboard.press("ArrowRight");pg.wait_for_timeout(1500);pg.screenshot(path="screenshots/desktop-11-presentation.png")
        pg.close()
    # 1920
    pg=b.new_page(viewport={"width":1920,"height":1080});pg.goto(U);pg.wait_for_timeout(6200);pg.click("#enter");pg.wait_for_timeout(2200);pg.screenshot(path="screenshots/desktop1920-01-command-centre.png");pg.close()
    # walkthrough video
    ctx=b.new_context(viewport={"width":1440,"height":900},record_video_dir="video/tmp",record_video_size={"width":1440,"height":900});pg=ctx.new_page();pg.goto(U);pg.wait_for_timeout(6500);pg.click("#enter");pg.wait_for_timeout(2500)
    pg.mouse.wheel(0,700);pg.wait_for_timeout(1200);pg.mouse.wheel(0,900);pg.wait_for_timeout(1500)
    pg.click("aside nav button[data-i='1']");pg.wait_for_timeout(1800);pg.evaluate("document.querySelector('#inst').scrollIntoView({block:'start'})");pg.wait_for_timeout(1500)
    for m in ["A_bat","B_bat_geo","C_bat","wp"]: pg.click(f"[data-hm='{m}']");pg.wait_for_timeout(900)
    pg.click("[data-hm='C_bat']");pg.click("[data-hw='7']");pg.wait_for_timeout(1600)
    for k in (60,120,200,260): pg.locator("#hs .hmc").nth(k).click();pg.wait_for_timeout(900)
    pg.click("aside nav button[data-i='2']");pg.wait_for_timeout(1500);pg.click("[data-pv='1']");pg.wait_for_timeout(1800);pg.click("[data-ls='rel']");pg.wait_for_timeout(1500)
    pg.locator("[data-cmp]").nth(0).click();pg.locator("[data-cmp]").nth(1).click();pg.locator("[data-cmp]").nth(2).click();pg.wait_for_timeout(800)
    pg.locator("[data-open]").first.click();pg.wait_for_timeout(2500)
    for t in ["Batting","Pressure history","Scouting assessment"]: pg.click(f"[data-t='{t}']");pg.wait_for_timeout(1100)
    pg.keyboard.press("Escape");pg.wait_for_timeout(1200);pg.click("#fab");pg.wait_for_timeout(2500)
    pg.click("aside nav button[data-i='6']");pg.wait_for_timeout(2500);pg.click("[data-rs='bowl']");pg.wait_for_timeout(2000)
    pg.click("aside nav button[data-i='7']");pg.wait_for_timeout(1500);pg.click("#sim [data-w='7']");pg.click("#swp2");pg.wait_for_timeout(5500)
    pg.click("aside nav button[data-i='9']");pg.wait_for_timeout(2500)
    pg.keyboard.press("p");pg.wait_for_timeout(1800)
    for _ in range(6): pg.keyboard.press("ArrowRight");pg.wait_for_timeout(2300)
    pg.keyboard.press("Escape");pg.wait_for_timeout(800);ctx.close();b.close()

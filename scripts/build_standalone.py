"""Builds dist/superr-intelligence-v4-standalone.html: CSS, JS, data and images inlined into one file."""
import re, os, base64, json
os.makedirs("dist", exist_ok=True)
mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
uri = lambda p: f"data:{mime[os.path.splitext(p)[1]]};base64," + base64.b64encode(open(p, "rb").read()).decode()
s = open("index.html").read()
s = re.sub(r'<link rel="stylesheet" href="(src/css/[^"]+)">', lambda m: "<style>" + open(m.group(1)).read().replace("../../assets/", "assets/") + "</style>", s)
s = re.sub(r'<script src="([^"]+)"></script>', lambda m: "<script>" + open(m.group(1)).read() + "</script>", s)
s = re.sub(r'(?<![\w/${}])assets/[\w/.-]+\.(?:svg|png|jpg|jpeg|webp)', lambda m: uri(m.group(0)) if os.path.exists(m.group(0)) else m.group(0), s)
am = {}
for root, _, fs in os.walk("assets"):
    if "_unused" in root: continue
    for f in fs:
        if f.endswith((".svg", ".png", ".jpg", ".jpeg", ".webp")): am[os.path.join(root, f)] = uri(os.path.join(root, f))
shim = "<script>const AM=" + json.dumps(am) + ";const dsc=Object.getOwnPropertyDescriptor(Element.prototype,'innerHTML');Object.defineProperty(Element.prototype,'innerHTML',{configurable:true,get:dsc.get,set(v){if(typeof v=='string')v=v.replace(/src=\"(assets\\/[^\"]+)\"/g,(m,p)=>AM[p]?'src=\"'+AM[p]+'\"':m);dsc.set.call(this,v)}});</script>"
s = s.replace("<head>", "<head>" + shim, 1)
open("dist/superr-intelligence-v4-standalone.html", "w").write(s)
print("standalone", round(os.path.getsize("dist/superr-intelligence-v4-standalone.html") / 1e6, 2), "MB")

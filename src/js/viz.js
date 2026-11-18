// ---------- shared visual instruments (real grid values only) ----------
const ST=[[0,[29,74,92]],[.42,[182,154,255]],[.74,[232,62,131]],[1,[240,210,138]]];
function heat(t){t=Math.max(0,Math.min(1,t));let i=1;while(i<ST.length-1&&t>ST[i][0])i++;const a=ST[i-1],b=ST[i],u=(t-a[0])/(b[0]-a[0]),c=a[1].map((v,k)=>Math.round(v+(b[1][k]-v)*u));return`rgb(${c})`}
const GRI=n=>D.grid.cols.indexOf(n),GROWS=D.grid.rows,GMAX={C_bat:Math.max(...GROWS.map(r=>r[GRI("C_bat")])),LI:Math.max(...GROWS.map(r=>r[GRI("LI")]))};
const gget=(w,b,r)=>GROWS.find(x=>x[0]==w&&x[1]==b&&Math.abs(x[2]-r)<.01);
const HMS={A_bat:["Model A · rule points (0–7)",7,"A"],B_bat_geo:["Model B · continuous index (0–1)",1,"B"],C_bat:["Model C · leverage × adversity",null,"C"],LI:["Relative leverage (1.0 = average delivery)",null,"LI"],wp:["Win probability (batting side), shown inverted",1,"WP"]};
function hnorm(m,row){const v=row[GRI(m)];return m=="wp"?1-v:m=="C_bat"?Math.sqrt(v/GMAX.C_bat):m=="LI"?Math.sqrt(v/GMAX.LI):v/HMS[m][1]}
const CSORT=GROWS.map(r=>r[GRI("C_bat")]).sort((a,b)=>a-b),pctC=v=>{let lo=0,hi=CSORT.length;while(lo<hi){const m=(lo+hi)>>1;CSORT[m]<v?lo=m+1:hi=m}return lo/CSORT.length};
const band=p=>p>.9?"top 10% of model states":p>.75?"top quartile":p>.5?"above median":p>.25?"below median":"bottom quartile";
// cricket pitch instrument: wickets in hand, balls left (ring), chase ratio (marker on the strip), pressure ring colour
function pitchViz(){const pips=Array.from({length:10},(_,i)=>`<circle class="tr pip" data-i="${i}" cx="${52+i*32}" cy="372" r="9" fill="#55DCC8"/>`).join("");
 return`<svg class="pv" viewBox="0 0 400 410" style="width:100%;max-width:440px;display:block;margin:auto" role="img" aria-label="Cricket ground showing wickets lost, balls remaining and chase ratio for the selected model state" id="pv">
 <defs><radialGradient id="pgr" cx=".5" cy=".5"><stop offset="0" stop-color="#14405a"/><stop offset=".8" stop-color="#0c2238"/><stop offset="1" stop-color="#08101f"/></radialGradient></defs>
 <circle cx="200" cy="170" r="165" fill="url(#pgr)"/><circle class="tr" id="pring" cx="200" cy="170" r="168" fill="none" stroke="#B69AFF" stroke-width="4"/>
 <circle cx="200" cy="170" r="104" fill="none" stroke="#fff" stroke-opacity=".18" stroke-dasharray="5 7"/>
 <circle class="tr" id="parc" cx="200" cy="170" r="152" fill="none" stroke="#D8B368" stroke-width="5" stroke-linecap="round" transform="rotate(-90 200 170)" stroke-dasharray="955" stroke-dashoffset="0"/>
 <rect x="186" y="95" width="28" height="150" rx="3" fill="#8f7f58" opacity=".55"/><path d="M180 108h40M180 232h40" stroke="#fff" stroke-opacity=".5"/>
 <g fill="#f2f1f7" opacity=".85"><rect x="193" y="96" width="2" height="9"/><rect x="199" y="96" width="2" height="9"/><rect x="205" y="96" width="2" height="9"/><rect x="193" y="236" width="2" height="9"/><rect x="199" y="236" width="2" height="9"/><rect x="205" y="236" width="2" height="9"/></g>
 <g class="tr" id="pbl" style="transform:translateY(120px)"><circle cx="200" cy="100" r="7" fill="#E83E83"/><circle cx="200" cy="100" r="16" fill="#E83E83" opacity=".22"/></g>
 <text id="pwp" x="200" y="62" fill="#F2F1F7" font-size="30" text-anchor="middle" font-weight="600">–</text><text x="200" y="80" fill="#9AA0B4" font-size="10" text-anchor="middle" letter-spacing="2">WIN PROBABILITY</text>
 <text id="prt" x="200" y="274" fill="#9AA0B4" font-size="11" text-anchor="middle"></text>
 <text x="38" y="170" fill="#9AA0B4" font-size="9" transform="rotate(-90 38 170)" text-anchor="middle" letter-spacing="2">BOWLER END ⟵ RATIO ⟶ BATTER END</text>
 ${pips}<text x="200" y="398" fill="#9AA0B4" font-size="10" text-anchor="middle" letter-spacing="2">WICKETS IN HAND</text></svg>`}
function pitchSet(root,w,b,r,t){const q=s=>root.querySelector(s),row=gget(w,b,r);if(!row)return;q("#pring").setAttribute("stroke",heat(t));q("#pring").setAttribute("stroke-width",3+t*7);q("#parc").setAttribute("stroke-dashoffset",955*(1-b/120));
 q("#pbl").style.transform=`translateY(${(1-(r-.3)/1.7)*130+8}px)`;q("#pwp").textContent=(row[GRI("wp")]*100).toFixed(1)+"%";q("#prt").textContent=`ratio ${r.toFixed(1)} · ${b} balls left · ${w} wickets lost`;
 root.querySelectorAll(".pip").forEach((p,i)=>{p.setAttribute("fill",i<10-w?"#55DCC8":"#E83E83");p.setAttribute("opacity",i<10-w?1:.55)})}
function replay(el){el.classList.remove("in");void el.offsetWidth;requestAnimationFrame(()=>el.classList.add("in"))}

// ---------- cinematic opening (≈5s, skippable, no audio) ----------
(function(){
 const o=$("#open"),mob=innerWidth<700,K=mob?.62:1;let done=false,raf,T=[];
 const R=(a,b)=>a+Math.random()*(b-a);
 // procedural original artwork (no club marks): Rajasthani hill-fort, tiered jharokha palace façade, stadium bowl, floodlights
 const mer=(x,y,w,n,h=14,g=10)=>Array.from({length:n},(_,i)=>`<rect x="${x+i*(w/n)}" y="${y-h}" width="${w/n-g/2}" height="${h}"/>`).join("");
 const arch=(x,y,w,h)=>`<path d="M${x} ${y+h}V${y+w/2}a${w/2} ${w/2} 0 0 1 ${w} 0V${y+h}z"/>`;
 let pal="";for(let t=0;t<5;t++){const w=360-t*52,x=190+(360-w)/2,y=470-t*54;pal+=`<rect x="${x}" y="${y}" width="${w}" height="54"/>`+Array.from({length:6-t},(_,i)=>arch(x+14+i*((w-28)/(6-t)),y+12,Math.max(14,(w-28)/(6-t)-14),30)).join("").replace(/<path/g,'<path class="win"')+`<path d="M${x-8} ${y}h${w+16}l-6 -10h-${w+4}z"/>`}
 const fort=`<path d="M900 640C1000 560 1060 520 1120 505L1140 440L1160 505C1230 470 1300 440 1380 450L1600 620V900H900z"/><rect x="1040" y="470" width="300" height="70"/>${mer(1040,470,300,16)}<rect x="1100" y="410" width="60" height="62"/>${mer(1100,410,60,4,10,6)}<rect x="1240" y="400" width="80" height="72"/><path d="M1240 400a40 40 0 0 1 80 0z"/><rect x="1275" y="372" width="10" height="28"/><rect x="1180" y="430" width="50" height="42"/><path d="M1180 430a25 25 0 0 1 50 0z"/>`;
 const stands=`<path d="M-50 640Q800 470 1650 640V900H-50z" fill="#0b1226"/><path d="M-50 700Q800 540 1650 700V900H-50z" fill="#0a0f1f"/><g fill="#d8b368" opacity=".5">${Array.from({length:70},()=>`<rect x="${R(0,1600)|0}" y="${R(600,700)|0}" width="3" height="3" opacity="${R(.1,.8).toFixed(2)}"/>`).join("")}</g>`;
 const TW=[[250,330],[600,300],[1000,300],[1350,330]];
 const towers=TW.map((t,i)=>`<g class="tower" data-i="${i}"><rect x="${t[0]-3}" y="${t[1]}" width="6" height="${700-t[1]}" fill="#10162a"/><rect class="head" x="${t[0]-26}" y="${t[1]-14}" width="52" height="18" rx="3"/></g>`).join("");
 const beams=TW.map((t,i)=>`<polygon class="beam${i%2?" m":""}" data-i="${i}" points="${t[0]-20},${t[1]} ${t[0]+20},${t[1]} ${t[0]+(800-t[0])*.55+260},780 ${t[0]+(800-t[0])*.55-260},780" fill="url(#bm)"/>`).join("");
 const stars=Array.from({length:mob?18:90},()=>`<circle cx="${R(0,1600)|0}" cy="${R(0,430)|0}" r="${R(.5,1.5).toFixed(1)}" opacity="${R(.2,.9).toFixed(2)}"/>`).join("");
 o.innerHTML=`<div class="cam"><div class="lay" data-p="2"><svg class="sky" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMax slice"><defs><linearGradient id="sk" x2="0" y2="1"><stop offset="0" stop-color="#0a0e24"/><stop offset=".55" stop-color="#2a1b45"/><stop offset=".85" stop-color="#a8456a"/><stop offset="1" stop-color="#f0a56a"/></linearGradient></defs><rect width="1600" height="900" fill="url(#sk)"/><circle cx="1180" cy="330" r="70" fill="#ffd9a0" opacity=".8"/><circle cx="1180" cy="330" r="190" fill="#ffd9a0" opacity=".1"/></svg><svg class="stars" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMax slice" style="position:absolute;inset:0" fill="#fff">${stars}</svg></div>
 <div class="lay heritage" data-p="5"><svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMax slice"><defs><linearGradient id="hl" x2="0" y2="1"><stop stop-color="#d8b368" stop-opacity=".9"/><stop offset=".5" stop-color="#7a3d55"/><stop offset="1" stop-color="#150f24"/></linearGradient></defs><g transform="translate(170,-50)"><g fill="#0c0a1c" stroke="#0c0a1c">${fort}</g><g fill="url(#hl)" class="lit" opacity=".9">${fort.replace(/<path d="M900[^>]*>/,"")}</g></g><g transform="translate(660,95)"><g fill="#0c0a1c">${pal}</g><g class="lit" fill="url(#hl)" opacity=".85">${pal}</g><g fill="#ffcf8a" class="lit">${pal.replace(/<rect[^>]*>/g,"").replace(/<path d="M[^"]*h[^>]*>/g,"")}</g></g></svg></div>
 <div class="lay" data-p="9"><svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMax slice"><defs><linearGradient id="bm" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#ffd9e8" stop-opacity="0"/></linearGradient><radialGradient id="gr" cx=".5" cy=".5"><stop stop-color="#1d4a5c"/><stop offset=".7" stop-color="#0d2236"/><stop offset="1" stop-color="#070d1c"/></radialGradient></defs><g class="stand">${stands}</g><g class="ground"><ellipse cx="800" cy="760" rx="640" ry="110" fill="url(#gr)"/><ellipse cx="800" cy="760" rx="440" ry="72" fill="none" stroke="#fff" stroke-opacity=".22" stroke-dasharray="6 8"/><path d="M780 700L820 700L840 800L760 800Z" fill="#d9c593" opacity=".42"/><g stroke="#fff" stroke-opacity=".4"><path d="M776 735h48M776 785h48"/></g></g>${towers}<g style="mix-blend-mode:screen">${beams}</g></svg></div>
 <div class="haze"></div><canvas id="fx"></canvas><img id="ballimg" src="assets/hero/cricket-ball.svg" alt="" width="96" height="90"></div>
 <div class="sweep"></div><div class="flash"></div><div class="vig"></div><div class="tl"></div><button id="skip">Skip ↵</button>
 <div class="lc"><span class="rrlogo lg"><img src="assets/brand/rr-logo.png" alt="Rajasthan Royals logo" width="63" height="96"></span><p class="eb eyb" style="display:flex;gap:10px;align-items:center"><img src="assets/culture/marwari-safa.svg" alt="" width="26" height="26">SupeRR Selector Season 2 · Competition concept</p>
 <h1 class="h1 big" aria-label="The game changes under pressure."><span class="ln"><span style="--d:.0s">The game</span></span><span class="ln"><span style="--d:.12s">changes under</span></span><span class="ln"><span class="gt" style="--d:.24s">pressure.</span></span></h1>
 <p class="sup">Where Rajasthan's royal spirit meets the science of cricket.</p>
 <div class="ctr"><button class="cta" id="enter">Enter the scouting war room →</button><span class="mute" style="font-size:12px;max-width:300px">Stage 3 chase-pressure evidence · 10 batters and 10 bowlers submitted</span></div></div>`;
 const $$=s=>o.querySelectorAll(s),cv=$("#fx"),cx=cv.getContext("2d");
 let W,H,dpr=Math.min(devicePixelRatio||1,2);const rs=()=>{W=cv.width=o.clientWidth*dpr;H=cv.height=o.clientHeight*dpr};rs();
 const P=Array.from({length:mob?12:46},()=>({x:Math.random(),y:Math.random(),r:R(.6,2),s:R(.01,.05),a:R(.1,.6)}));
 let trail=[],ball=null,t0=0,lit=0,lastT=0;const spr=document.createElement("canvas");spr.width=spr.height=64;{const g=spr.getContext("2d"),gr=g.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,"#ff7fb0");gr.addColorStop(1,"rgba(255,127,176,0)");g.fillStyle=gr;g.fillRect(0,0,64,64)}
 const at=(ms,f)=>T.push(setTimeout(f,ms*K));
 function loop(t){raf=requestAnimationFrame(loop);if(mob&&t-lastT<33)return;lastT=t;cx.clearRect(0,0,W,H);const e=(t-t0)/1000;
  cx.fillStyle="#fff";P.forEach(p=>{p.y-=p.s*.003*(lit?1:.3);if(p.y<0)p.y=1;cx.globalAlpha=p.a*Math.min(1,lit/2+.1)*(.5+.5*Math.sin(e*1.3+p.x*9));cx.beginPath();cx.arc(p.x*W,p.y*H,p.r*dpr,0,7);cx.fill()});
  if(ball){const u=Math.min(1,(t-ball.t)/ (1500*K)),x=(1-u)*(1-u)*-.08+2*(1-u)*u*.45+u*u*1.1,y=(1-u)*(1-u)*.74+2*(1-u)*u*.02+u*u*.56,s=.55+Math.sin(u*Math.PI)*1.1;
   const px=x*W,py=y*H;trail.push([px,py,s]);if(trail.length>(mob?10:18))trail.shift();trail.forEach((q,i)=>{cx.globalAlpha=i/trail.length*.5;const r=26*q[2]*dpr;cx.drawImage(spr,q[0]-r,q[1]-r,r*2,r*2)});
   const im=$("#ballimg");im.style.opacity=u>0&&u<1?1:0;im.style.transform=`translate(${x*o.clientWidth-im.offsetWidth/2}px,${y*o.clientHeight-im.offsetHeight/2}px) scale(${s}) rotate(${u*900}deg)`;
   if(u>=1){ball=null;trail=[];im.style.opacity=0}}
  cx.globalAlpha=1};
 function layout(){const f=o.querySelector(".flash");f.style.setProperty("--fx","78%");f.style.setProperty("--fy","60%")}
 function finalState(){o.classList.add("fin","em","rev","cam1","go2","go3","go4");$$(".tower").forEach(t=>t.classList.add("on"));$$(".beam").forEach(b=>b.classList.add("on"));lit=3}
 function go(x,y,quick){if(done)return;done=true;T.forEach(clearTimeout);cancelAnimationFrame(raf);const cxp=x??innerWidth/2,cyp=y??innerHeight*.6;o.style.setProperty("--cx",cxp+"px");o.style.setProperty("--cy",cyp+"px");$("#app").style.display="block";show(0);
  if(RM||quick){o.remove();return}const rg=$("#ring");rg.style.setProperty("--cx",cxp+"px");rg.style.setProperty("--cy",cyp+"px");rg.classList.add("go");o.classList.add("leave");setTimeout(()=>{o.remove();rg.remove()},950)}
 $("#enter").onclick=e=>go(e.clientX||innerWidth/2,e.clientY||innerHeight/2);$("#skip").onclick=()=>go(null,null,true);
 addEventListener("keydown",e=>{if(!done&&(e.key=="Enter"||e.key=="Escape"||e.key==" ")){e.preventDefault();go(null,null,true)}});addEventListener("resize",rs);
 // gentle pointer parallax (desktop only)
 if(!RM&&!mob)addEventListener("pointermove",e=>{if(done)return;const dx=(e.clientX/innerWidth-.5),dy=(e.clientY/innerHeight-.5);$$(".lay").forEach(l=>{const p=+l.dataset.p||3;l.style.transform=`translate(${-dx*p*3}px,${-dy*p*2}px)`})});
 if(RM){finalState();return}
 if(!mob)requestAnimationFrame(t=>{t0=t;loop(t)});else cv.style.display="none";
 const tw=$$(".tower"),bm=$$(".beam");at(100,()=>{o.classList.add("em");o.classList.add("cam1")});
 [500,820,1140,1460].forEach((ms,i)=>{at(ms-80,()=>tw[i].classList.add("fl"));at(ms,()=>{tw[i].classList.remove("fl");tw[i].classList.add("on");bm[i].classList.add("on");lit=i+1});at(ms+90,()=>{tw[i].classList.remove("on")});at(ms+150,()=>tw[i].classList.add("on"))});
 at(1700,()=>{if(!mob){ball={t:performance.now()};return}const im=$("#ballimg"),w=o.clientWidth,h=o.clientHeight,pt=u=>{const x=(1-u)*(1-u)*-.08+2*(1-u)*u*.45+u*u*1.1,y=(1-u)*(1-u)*.74+2*(1-u)*u*.02+u*u*.56,s=.55+Math.sin(u*Math.PI)*1.1;return{opacity:u>0&&u<1?1:0,transform:`translate(${x*w-im.offsetWidth/2}px,${y*h-im.offsetHeight/2}px) scale(${s}) rotate(${u*900}deg)`}};im.animate([0,.25,.5,.75,1].map(pt),{duration:1500*K,easing:"linear",fill:"forwards"})});
 at(2750,()=>{o.querySelector(".flash").classList.add("go");o.classList.add("rev");o.querySelector(".sweep").classList.add("go")});
 at(2850,()=>{o.classList.add("go2")});at(3700,()=>o.classList.add("go3"));at(4300,()=>o.classList.add("go4"));
 const tl=o.querySelector(".tl");tl.style.transition=`width ${5.2*K}s linear`;requestAnimationFrame(()=>tl.style.width="100%");
 at(5800,()=>{cancelAnimationFrame(raf)});
})();

const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname,'docs');
const srv = http.createServer((req,res)=>{
  let p = decodeURIComponent(req.url.split('?')[0]); if(p.endsWith('/')) p+='index.html';
  const f = path.join(root,p); if(!fs.existsSync(f)){res.writeHead(404);res.end('nf');return;}
  const ext = path.extname(f); const ct = {'.html':'text/html; charset=utf-8','.css':'text/css','.svg':'image/svg+xml','.xml':'text/xml'}[ext]||'text/plain';
  res.writeHead(200,{'content-type':ct}); res.end(fs.readFileSync(f));
}).listen(8765);
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({viewport:{width:1280,height:900}});
  const p = await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  const base='http://localhost:8765';
  const shots=['/', '/inserat-auf-deutsch/','/kaufnebenkosten/','/fragen-an-den-maeklare/','/behoerden-reihenfolge/','/fixkosten-goeteborg/','/404.html'];
  for(const u of shots){ await p.goto(base+u,{waitUntil:'load'}); await p.waitForTimeout(400); await p.screenshot({path:'shot'+(u.replace(/\//g,'_')||'_index')+'.png',fullPage:true}); }
  // mobile
  const m = await b.newPage({viewport:{width:390,height:844}}); await m.goto(base+'/fixkosten-goeteborg/'); await m.waitForTimeout(300); await m.screenshot({path:'shot_mobile_fixkosten.png',fullPage:true});
  await m.goto(base+'/'); await m.screenshot({path:'shot_mobile_index.png',fullPage:true});
  const hs = await m.evaluate(()=>document.documentElement.scrollWidth); console.log('mobile scrollWidth', hs);

  // --- functional: inserat
  await p.goto(base+'/inserat-auf-deutsch/');
  let out = await p.evaluate(()=>document.getElementById('calc').innerText); console.log('SAMPLE calc:\n'+out);
  const t1 = `Villa, Kungälv\nPris 4 200 000 kr\nUpplåtelseform Tomträtt\nBoarea 120 m²\nAntal rum 5 rum\nByggår 1978\nDriftkostnad 42 000 kr/år`;
  await p.fill('#src', t1); await p.click('#go');
  out = await p.evaluate(()=>document.getElementById('out').innerText+'\n--\n'+document.getElementById('calc').innerText+'\n--\n'+document.getElementById('flagbox').innerText);
  console.log('TOMTRÄTT test:\n'+out);
  const t2 = `3 rum, 72 m²\nUtgångspris 3 100 000 kr\nAvgift 3 900 kr/mån\nBostadsrätt`;
  await p.fill('#src', t2); await p.click('#go');
  out = await p.evaluate(()=>document.getElementById('out').innerText); console.log('ROOMS test:\n'+out);

  // --- kaufnebenkosten defaults
  await p.goto(base+'/kaufnebenkosten/');
  console.log('KNK:\n'+await p.evaluate(()=>document.getElementById('once').innerText+'\n'+document.getElementById('year').innerText));
  // --- fixkosten
  await p.goto(base+'/fixkosten-goeteborg/');
  console.log('FIX:\n'+await p.evaluate(()=>document.getElementById('out').innerText));
  // --- fragen copy count
  await p.goto(base+'/fragen-an-den-maeklare/');
  const n = await p.evaluate(()=>['br','villa','fritid'].map(k=>GROUPS[k].reduce((a,g)=>a+g.q.length,0))); console.log('fragen counts',n);
  await p.goto(base+'/behoerden-reihenfolge/'); await p.click('#kinder button[data-v=ja]'); console.log('steps', await p.evaluate(()=>document.querySelectorAll('#steps>li').length));
  console.log('ERRORS:', errs);
  await b.close(); srv.close();
})();

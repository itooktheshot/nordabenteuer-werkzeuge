const { chromium } = require('playwright'); const http=require('http'),fs=require('fs'),path=require('path');
const root=path.join(__dirname,'docs');
const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';const f=path.join(root,p);if(!fs.existsSync(f)){r.writeHead(404);return r.end()}r.writeHead(200,{'content-type':f.endsWith('.css')?'text/css':'text/html; charset=utf-8'});r.end(fs.readFileSync(f))}).listen(8767);
const B='http://localhost:8767';
const CASES = {
hemnet_br: `Såggatan 12A
Majorna, Göteborgs kommun
Bostadsrättslägenhet
Utgångspris
2 950 000 kr
Avgift
4 212 kr/mån
Pris/m²
43 382 kr/m²
Antal rum
3 rum
Boarea
68 m²
Driftkostnad
9 600 kr/år
Byggår
1952
Våning
3 av 5, hiss finns
Förening
Brf Sjöfarten
Energiklass
D
Upplåtelseform
Bostadsrätt
Visning
Söndag 2 november 12:00–12:45`,
hemnet_villa: `Hamnvägen 4
Grebbestad, Tanums kommun
Fritidshus
Pris
3 475 000 kr
Antal rum
4 rum
Boarea
82,5 m²
Biarea
20 m²
Tomtarea
1 250 m²
Driftkostnad
31 200 kr/år
Byggår
1968
Upplåtelseform
Äganderätt
Energiklass
F
Tillträde
Enligt överenskommelse`,
booli: `Boarea 108,5 m²
Rum 4 rum
Avgift 5 575 kr/mån
Byggår 1909
Hiss
Balkong`,
rental: `Hyra 9 500 kr/mån
2 rum, 54 m²
Uthyres från 1 december`,
german: `Schöne 3-Zimmer-Wohnung in Hamburg, 68 m², Kaltmiete 1.200 €`,
slutpris: `Slutpris 3 310 000 kr
Utgångspris 2 950 000 kr
Avgift 4 212 kr/mån
Boarea 68 m²
Upplåtelseform Bostadsrätt`,
tomtratt: `Pris 5 200 000 kr
Upplåtelseform Tomträtt
Bostadstyp Villa
Boarea 140 m²
Tomtarea 780 m²
Byggår 1934`,
empty_spaces: `Utgångspris: 1 795 000 kr
Avgift: 3 101 kr/mån
Boarea: 45 m²
Antal rum: 1,5 rum
Byggår: 1965`,
};
(async()=>{const b=await chromium.launch();const ctx=await b.newContext();const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push('PAGEERR '+e.message));
await p.goto(B+'/inserat-auf-deutsch/');
for(const [name,txt] of Object.entries(CASES)){
  await p.fill('#src',txt); await p.click('#go');
  const r=await p.evaluate(()=>{const g=i=>document.getElementById(i);const rows=[...document.querySelectorAll('dl.fields>div')].map(d=>d.querySelector('dt').textContent+' = '+d.querySelector('dd.val').textContent);const miss=g('out').querySelector('.miss')?.textContent||'';const empty=g('out').querySelector('.empty')?.textContent||'';const calc=[...document.querySelectorAll('#calc li')].map(l=>l.querySelector('.k').textContent+' → '+l.querySelector('.v').textContent);const flags=[...document.querySelectorAll('#flagbox .flag')].map(f=>f.textContent.slice(0,70));return {rows,miss,empty,calc,flags}});
  console.log('\n### '+name); console.log(JSON.stringify(r,null,1));
}
// kaufnebenkosten edge cases
await p.goto(B+'/kaufnebenkosten/');
const knk=async(label)=>{console.log('\n### KNK '+label, await p.evaluate(()=>[...document.querySelectorAll('#once li')].map(l=>l.querySelector('.k').firstChild.textContent+' → '+l.querySelector('.v').firstChild.textContent).join(' | ')+' || '+[...document.querySelectorAll('#year li')].map(l=>l.querySelector('.k').firstChild.textContent+' → '+l.querySelector('.v').firstChild.textContent).join(' | ')))};
await p.fill('#pant','5000000'); await knk('pant>lan');
await p.fill('#tax',''); await p.fill('#pant','0'); await knk('no tax');
await p.fill('#pris','0'); await knk('pris 0');
await p.click('#typ button[data-v=br]'); await knk('br');
await p.click('#typ button[data-v=tomt]'); await p.fill('#pris','4200000'); await p.fill('#tax','5000000'); await knk('tomt tax>pris');
// fixkosten
await p.goto(B+'/fixkosten-goeteborg/');
const fix=async(label)=>{console.log('\n### FIX '+label, await p.evaluate(()=>[...document.querySelectorAll('#out li')].map(l=>l.querySelector('.k').firstChild.textContent+' → '+l.querySelector('.v').firstChild.textContent).join(' | ')))};
await p.fill('#brutto','8000'); await fix('brutto 8000');
await p.fill('#brutto','30000'); await fix('brutto 30000');
await p.fill('#brutto','120000'); for(let i=0;i<3;i++) await p.click('#addkid'); await fix('5 kids 120k');
await p.click('#addkid'); console.log('kids after 6th click', await p.evaluate(()=>document.querySelectorAll('.kidrow').length));
for(let i=0;i<5;i++) await p.click('.kidrow button'); await fix('0 kids');
await p.selectOption('#karten','0'); await fix('no cards');
// behörden: all combos
await p.goto(B+'/behoerden-reihenfolge/');
for(const d of ['lang','kurz']) for(const s of ['anstellung','selbst','studium','familie']) for(const k of ['nein','ja']){await p.click(`#dauer button[data-v=${d}]`);await p.click(`#status button[data-v=${s}]`);await p.click(`#kinder button[data-v=${k}]`);const n=await p.evaluate(()=>document.querySelectorAll('#steps>li').length);const links=await p.evaluate(()=>[...document.querySelectorAll('#steps a')].map(a=>a.href));process.stdout.write(`${d}/${s}/${k}:${n} `);}
console.log('\nbehörden links unique', await p.evaluate(()=>[...new Set([...document.querySelectorAll('#steps a')].map(a=>a.getAttribute('href')))].join(' ')));
// fragen copy fallback
await p.goto(B+'/fragen-an-den-maeklare/'); await p.click('#copy'); console.log('copy status:', await p.evaluate(()=>document.getElementById('said').textContent));
await p.click('#typ button[data-v=fritid]'); console.log('fritid items', await p.evaluate(()=>document.querySelectorAll('ol.q li').length));
console.log('\nERRORS', errs.filter(e=>!/ERR_TUNNEL|Failed to load resource/.test(e)));
await b.close();srv.close();})();

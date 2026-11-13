const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const{pathToFileURL}=require('node:url');
const root=process.env.CODEX_NODE_DEPENDENCIES||'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const{chromium}=require(path.join(root,'playwright')),sharp=require(path.join(root,'sharp'));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,p))).digest('hex');
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const page=await browser.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
await page.route(/^https?:/,r=>r.abort());await page.goto(pathToFileURL(path.join(__dirname,'Creative01V4.html')).href);await page.evaluate(()=>document.fonts.ready);
const checks=await page.evaluate(()=>({actualCopy:{hook:[...document.querySelectorAll('.hook .row')].map(e=>e.textContent).join(' '),promise:[...document.querySelectorAll('.promise-line')].map(e=>e.textContent).join(' '),cta:document.querySelector('.cta .row').textContent},copy:[...document.querySelectorAll('[data-logical-copy]')].map(e=>({class:e.className,logical:e.dataset.logicalCopy,lines:[...e.children].map(x=>x.textContent),box:e.getBoundingClientRect().toJSON()})),rows:[...document.querySelectorAll('.row')].map(e=>({width:e.getBoundingClientRect().width,runs:[...e.children].map(x=>({text:x.textContent,dir:x.dir,box:x.getBoundingClientRect().toJSON()}))})),fonts:[...document.fonts].map(f=>({family:f.family,status:f.status}))}));
const expected={hook:'كتوجد لـCampus France ومحتار فاختيار الـFormations؟',promise:'عمّر ملفك الدراسي، واكتشف جوج تكوينات مقترحة مع معلومات تساعدك تفهم اختياراتك.',cta:'شوف جوج Formations مجاناً'};
checks.exactCopy=Object.fromEntries(Object.entries(expected).map(([key,value])=>[key,checks.actualCopy[key]===value]));if(Object.values(checks.exactCopy).some(v=>!v))throw Error('Actual visible copy differs');
await page.screenshot({path:path.join(__dirname,'Creative01V4.png')});
await sharp(path.join(__dirname,'Creative01V4.png')).resize(360,450).png().toFile(path.join(__dirname,'Creative01V4-phone-preview.png'));
await page.setViewportSize({width:2240,height:1460});await page.goto(pathToFileURL(path.join(__dirname,'comparison.html')).href);await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:path.join(__dirname,'reference32-vs-Creative01V4-comparison.png')});await browser.close();
checks.sha256={source:hash('assets/reference32-original.webp'),full:hash('Creative01V4.png'),phone:hash('Creative01V4-phone-preview.png')};fs.writeFileSync(path.join(__dirname,'render-checks.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify({exactCopy:checks.exactCopy,sha256:checks.sha256}));
})().catch(e=>{console.error(e);process.exit(1)});

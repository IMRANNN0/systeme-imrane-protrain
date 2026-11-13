const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const{pathToFileURL}=require('node:url');
const root=process.env.CODEX_NODE_DEPENDENCIES||'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const{chromium}=require(path.join(root,'playwright')),sharp=require(path.join(root,'sharp'));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,p))).digest('hex');
(async()=>{
for(const name of ['info','sciences','droit','gestion','lettres'])if(!fs.existsSync(path.join(__dirname,`assets/generated-${name}.png`)))throw Error(`Missing generated raster: ${name}`);
const baseline=JSON.parse(fs.readFileSync(path.join(__dirname,'v4-preservation-baseline.json')));
const originalV4Available=fs.existsSync(path.join(__dirname,'../v4'));
if(originalV4Available)for(const item of baseline){const actual=crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'../v4',item.file))).digest('hex');if(actual!==item.sha256)throw Error(`V4 changed: ${item.file}`);}

const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const page=await browser.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
await page.route(/^https?:/,r=>r.abort());await page.goto(pathToFileURL(path.join(__dirname,'Creative01V5.html')).href);await page.evaluate(()=>document.fonts.ready);await page.evaluate(async()=>{await Promise.all([...document.images].map(i=>i.decode()));await Promise.all([...document.querySelectorAll('image.academic-raster')].map(el=>new Promise((resolve,reject)=>{const i=new Image();i.onload=resolve;i.onerror=reject;i.src=el.getAttribute('href')})))});
const checks=await page.evaluate(()=>({actualCopy:{hook:[...document.querySelectorAll('.hook .row')].map(e=>e.textContent).join(' '),promise:[...document.querySelectorAll('.promise-line')].map(e=>e.textContent).join(' '),cta:document.querySelector('.cta .row').textContent},copy:[...document.querySelectorAll('[data-logical-copy]')].map(e=>({class:e.className,logical:e.dataset.logicalCopy,lines:[...e.children].map(x=>x.textContent),box:e.getBoundingClientRect().toJSON()})),rows:[...document.querySelectorAll('.row')].map(e=>({width:e.getBoundingClientRect().width,runs:[...e.children].map(x=>({text:x.textContent,dir:x.dir,box:x.getBoundingClientRect().toJSON()}))})),fonts:[...document.fonts].map(f=>({family:f.family,status:f.status}))}));
const expected={hook:'كتوجد لـCampus France ومحتار فاختيار الـFormations؟',promise:'عمّر ملفك الدراسي، واكتشف جوج تكوينات مقترحة مع معلومات تساعدك تفهم اختياراتك.',cta:'شوف جوج Formations مجاناً'};
checks.v4Preserved=originalV4Available?true:'External historical folder absent from standalone source archive; preserved V4 comparison image included';checks.academicRasterCount=await page.locator('image.academic-raster').count();if(checks.academicRasterCount!==5)throw Error('Expected five raster objects');checks.codeDrawnAcademicSymbols=await page.locator('#illustrative-academic-choices path').count();if(checks.codeDrawnAcademicSymbols)throw Error('Code icon found');
checks.exactCopy=Object.fromEntries(Object.entries(expected).map(([key,value])=>[key,checks.actualCopy[key]===value]));if(Object.values(checks.exactCopy).some(v=>!v))throw Error('Actual visible copy differs');
await page.screenshot({path:path.join(__dirname,'Creative01V5.png')});
await sharp(path.join(__dirname,'Creative01V5.png')).resize(360,450).png().toFile(path.join(__dirname,'Creative01V5-phone-preview.png'));
await page.setViewportSize({width:2240,height:1460});await page.goto(pathToFileURL(path.join(__dirname,'comparison.html')).href);await page.evaluate(()=>document.fonts.ready);await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));await page.screenshot({path:path.join(__dirname,'Creative01V4-vs-V5-comparison.png')});await browser.close();
const current=await sharp(path.join(__dirname,'Creative01V5.png')).ensureAlpha().raw().toBuffer();
const previous=await sharp(path.join(__dirname,'assets/Creative01V4-preserved.png')).ensureAlpha().raw().toBuffer();
const circles=[[158,201,32],[299,166,47.5],[249,307,38],[681,207,49],[646,361,42]];
let changedOutside=0,changedInside=0;
for(let y=0;y<1350;y++)for(let x=0;x<1080;x++){let diff=false;const i=(y*1080+x)*4;for(let c=0;c<4;c++)if(current[i+c]!==previous[i+c])diff=true;if(diff){const inside=circles.some(([cx,cy,r])=>Math.hypot(x-cx*1.25,y-cy*1.25)<r*1.25+2);inside?changedInside++:changedOutside++;}}
checks.pixelStability={changedInsideAcademicCircles:changedInside,changedOutsideAcademicCircles:changedOutside};if(changedOutside)throw Error(`Unexpected changes outside academic circles: ${changedOutside}`);
checks.sha256={source:hash('assets/reference32-original.webp'),full:hash('Creative01V5.png'),phone:hash('Creative01V5-phone-preview.png')};fs.writeFileSync(path.join(__dirname,'render-checks.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify({exactCopy:checks.exactCopy,sha256:checks.sha256}));
})().catch(e=>{console.error(e);process.exit(1)});

/* Offline code-native artifact export, no external page or forms. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const dependencyRoot=process.env.CODEX_NODE_DEPENDENCIES||'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(dependencyRoot,'playwright')),sharp=require(path.join(dependencyRoot,'sharp'));
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,file))).digest('hex');
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const page=await browser.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});const errors=[];
page.on('pageerror',e=>errors.push(String(e)));await page.route(/^https?:/,r=>r.abort());
await page.goto(pathToFileURL(path.join(__dirname,'Creative01V2.html')).href,{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
const checks=await page.evaluate(()=>{
const box=e=>e.getBoundingClientRect().toJSON(),style=e=>getComputedStyle(e);
const rows=[...document.querySelectorAll('.manual-row')].map(e=>({class:e.className,box:box(e),runs:[...e.querySelectorAll('.run')].map(r=>({text:r.textContent,dir:r.dir,unicodeBidi:style(r).unicodeBidi,box:box(r)}))}));
return {dimensions:{width:document.querySelector('.ad').offsetWidth,height:document.querySelector('.ad').offsetHeight},fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),text:{hookLines:[...document.querySelectorAll('.hook-line')].map(e=>e.textContent),hook:document.querySelector('.hook').textContent,support:document.querySelector('.support').textContent,cta:document.querySelector('.cta').textContent},rows,photoBand:box(document.querySelector('.photo-band')),photo:box(document.querySelector('.photo')),support:{box:box(document.querySelector('.support')),fontSize:style(document.querySelector('.support')).fontSize,lines:[...document.querySelectorAll('.support-line')].map(e=>({text:e.textContent,box:box(e),overflow:e.scrollWidth>e.clientWidth}))},cta:{box:box(document.querySelector('.cta')),background:style(document.querySelector('.cta')).backgroundColor,color:style(document.querySelector('.cta')).color},nowrap:[...document.querySelectorAll('.hook-line,.support-line')].every(e=>style(e).whiteSpace==='nowrap'),images:[...document.images].map(i=>({source:i.getAttribute('src'),complete:i.complete,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight,box:box(i)}))};
});
const expected={hook:'كتوجد لـCampus France؟ ومحتار فاختيار الـFormations؟',support:'عمّر ملفك الدراسي وشوف جوج تكوينات مقترحة مجاناً.',cta:'شوف جوج Formations مجاناً'};
checks.exactCopy=Object.fromEntries(Object.entries(expected).map(([k,v])=>[k,checks.text[k]===v]));
checks.exactHookLines=checks.text.hookLines.length===2&&checks.text.hookLines[0]==='كتوجد لـCampus France؟'&&checks.text.hookLines[1]==='ومحتار فاختيار الـFormations؟';
checks.visualRunGeometry=checks.rows.map(row=>({class:row.class,rightToLeftSequence:row.runs.every((r,i)=>i===0||r.box.right<=row.runs[i-1].box.left),gaps:row.runs.slice(1).map((r,i)=>row.runs[i].box.left-r.box.right),insideCanvas:row.runs.every(r=>r.box.left>=62&&r.box.right<=1018)}));
checks.pageErrors=errors;checks.photoSharePercent=checks.photoBand.height/1350*100;checks.supportAt360Px=parseFloat(checks.support.fontSize)/3;
const rgb=hex=>hex.match(/\w\w/g).map(v=>parseInt(v,16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4),lum=hex=>rgb(hex).reduce((v,c,i)=>v+c*[.2126,.7152,.0722][i],0);checks.ctaContrast=(lum('F2A541')+.05)/(lum('0F2A1F')+.05);
if(!checks.exactHookLines||Object.values(checks.exactCopy).some(v=>!v)||checks.visualRunGeometry.some(r=>!r.rightToLeftSequence||!r.insideCanvas)||checks.support.lines.some(l=>l.overflow))throw Error('Copy or geometry validation failed: '+JSON.stringify(checks));
await page.screenshot({path:path.join(__dirname,'Creative01V2.png')});
const ctaSample=await sharp(path.join(__dirname,'Creative01V2.png')).extract({left:80,top:1240,width:1,height:1}).removeAlpha().raw().toBuffer();checks.ctaBackgroundPixel={x:80,y:1240,rgb:[...ctaSample],hex:'#'+ctaSample.toString('hex').toUpperCase()};if(checks.ctaBackgroundPixel.hex!=='#F2A541')throw Error('CTA exported background pixel mismatch');
await sharp(path.join(__dirname,'Creative01V2.png')).resize({width:360}).png().toFile(path.join(__dirname,'Creative01V2-phone-preview.png'));
await page.setViewportSize({width:2280,height:1505});await page.goto(pathToFileURL(path.join(__dirname,'comparison.html')).href,{waitUntil:'load'});await page.screenshot({path:path.join(__dirname,'Creative01V1-vs-V2-comparison.png')});
await browser.close();checks.pngSha256=hash('Creative01V2.png');checks.v1ComparisonCopySha256=hash('comparison-v1-original.png');fs.writeFileSync(path.join(__dirname,'render-checks.json'),JSON.stringify(checks,null,2));console.log(JSON.stringify({exactCopy:checks.exactCopy,visualRunGeometry:checks.visualRunGeometry,photoSharePercent:checks.photoSharePercent,supportAt360Px:checks.supportAt360Px,ctaContrast:checks.ctaContrast,pngSha256:checks.pngSha256,pageErrors:errors}));
})().catch(e=>{console.error(e);process.exit(1)});

/* Offline artifact export. No network navigation, no external form interaction. */
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const dependencyRoot = process.env.CODEX_NODE_DEPENDENCIES || 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const { chromium } = require(path.join(dependencyRoot, 'playwright'));
const sharp = require(path.join(dependencyRoot, 'sharp'));
(async()=>{
  const executablePath = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
  const browser = await chromium.launch({headless:true,executablePath});
  const page = await browser.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
  const problems=[];
  page.on('pageerror',e=>problems.push(String(e)));
  await page.route('https://**',route=>route.abort());
  await page.route('http://**',route=>route.abort());
  await page.goto(pathToFileURL(path.join(__dirname,'Creative01V1.html')).href,{waitUntil:'load'});
  await page.evaluate(()=>document.fonts.ready);
  const checks=await page.evaluate(()=>({
    dimensions:{width:document.querySelector('.ad').offsetWidth,height:document.querySelector('.ad').offsetHeight},
    fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),
    text:{hook:document.querySelector('.hook').textContent,support:document.querySelector('.support').textContent,cta:document.querySelector('.cta').textContent},
    elements:[...document.querySelectorAll('.brand,.headline,.hook .line,.photo-band,.choices,.illustration,.footer,.support,.cta')].map(e=>({class:e.className,box:e.getBoundingClientRect().toJSON(),scrollWidth:e.scrollWidth,clientWidth:e.clientWidth}))
  }));
  const expected={hook:'كتوجد لـCampus France ومحتار فاختيار الـFormations؟',support:'اكتشف تكوينات مقترحة حسب الملف الدراسي ديالك.',cta:'شوف جوج Formations مجاناً'};
  checks.exactCopy=Object.fromEntries(Object.entries(expected).map(([key,value])=>[key,checks.text[key]===value]));
  if(Object.values(checks.exactCopy).some(pass=>!pass))throw Error('Exact copy mismatch');
  await page.screenshot({path:path.join(__dirname,'Creative01V1.png')});
  await browser.close();
  await sharp(path.join(__dirname,'Creative01V1.png')).resize({width:360}).png().toFile(path.join(__dirname,'Creative01V1-phone-preview.png'));
  fs.writeFileSync(path.join(__dirname,'render-checks.json'),JSON.stringify({...checks,pageErrors:problems},null,2));
  console.log(JSON.stringify({export:'Creative01V1.png',dimensions:checks.dimensions,fonts:checks.fonts,pageErrors:problems}));
})().catch(e=>{console.error(e);process.exit(1)});

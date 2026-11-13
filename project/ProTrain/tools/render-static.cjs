/* Portable local HTML export. Does not alter or approve the input creative. */
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const args = process.argv.slice(2);
const input = args.shift();
const options = {};
for (let i=0;i<args.length;i+=2) options[args[i]] = args[i+1];
if (!input || !options['--output']) {
  console.error('Usage: node tools/render-static.cjs <input.html> --output <new.png> [--width 1080 --height 1350]');
  process.exit(2);
}
const source = path.resolve(input), output = path.resolve(options['--output']);
if (!fs.existsSync(source) || !source.endsWith('.html')) throw new Error('Existing HTML input required');
if (fs.existsSync(output)) throw new Error('Output exists; select a new path to preserve prior exports');
const width = Number(options['--width'] || 1080), height = Number(options['--height'] || 1350);
if (!Number.isInteger(width) || !Number.isInteger(height) || width<1 || height<1 || width>4096 || height>4096) throw new Error('Dimensions must be integers from 1 to 4096');
const load = name => process.env.CODEX_NODE_DEPENDENCIES
  ? require(path.join(process.env.CODEX_NODE_DEPENDENCIES, name)) : require(name);
const {chromium} = load('playwright');
(async()=>{
  const browser=await chromium.launch({headless:true, executablePath:process.env.CHROME_PATH || undefined});
  try {
    const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
    const errors=[];
    page.on('pageerror',e=>errors.push(String(e)));
    await page.route(/^https?:/,route=>route.abort());
    await page.goto(pathToFileURL(source).href,{waitUntil:'load'});
    await page.evaluate(()=>document.fonts.ready);
    const images=await page.evaluate(async()=>{
      await Promise.all([...document.images].map(image=>image.decode()));
      return [...document.images].every(image=>image.complete && image.naturalWidth>0);
    });
    if (!images || errors.length) throw new Error('Asset/page check failed: '+errors.join('; '));
    fs.mkdirSync(path.dirname(output),{recursive:true});
    await page.screenshot({path:output});
    console.log(JSON.stringify({output,width,height,pageErrors:errors.length,imagesLoaded:images,networkAllowed:false,approval:'unchanged'}));
  } finally {await browser.close();}
})().catch(e=>{console.error(e.message);process.exitCode=1;});

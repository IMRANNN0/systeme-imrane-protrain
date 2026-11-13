// Separate bundling from rendering to release Webpack's heap before Chromium.
import {mkdirSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const temporary=path.join(root,'.cache','darija-ad-temp');
mkdirSync(temporary,{recursive:true});
process.env.TMP=temporary;
process.env.TEMP=temporary;
const serveUrl=path.join(root,'.cache','darija-ad-bundle');
const mode=process.argv[2];
if(mode==='bundle'){
  const {bundle}=await import('@remotion/bundler');
  await bundle({entryPoint:path.join(root,'src/index.ts'),outDir:serveUrl,
    onProgress:p=>{if(p===100)console.log('Bundle complete');}});
}else if(mode==='video'){
  const {renderMedia,selectComposition}=await import('@remotion/renderer');
  const composition=await selectComposition({serveUrl,id:'DarijaAd',timeoutInMilliseconds:120000});
  let last=-1;
  await renderMedia({serveUrl,composition,codec:'h264',audioCodec:'aac',crf:17,
    outputLocation:path.join(root,'out/protrain-darija-ad-v1.mp4'),isProduction:false,concurrency:1,
    timeoutInMilliseconds:120000,mediaCacheSizeInBytes:256*1024*1024,
    onProgress:({renderedFrames})=>{const step=Math.floor(renderedFrames/60);if(step!==last){console.log(`Rendered ${renderedFrames}/285`);last=step;}}});
  console.log('Exported out/protrain-darija-ad-v1.mp4');
}else{throw new Error('Use bundle or video in separate Node processes.');}

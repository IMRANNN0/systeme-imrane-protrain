// Bundle and render in separate processes so Webpack's heap is released before Chrome starts.
import {mkdirSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root=fileURLToPath(new URL('../',import.meta.url));
const temporary=path.join(root,'.cache','craft-temp');
mkdirSync(temporary,{recursive:true});
process.env.TMP=temporary;
process.env.TEMP=temporary;
const serveUrl=path.join(root,'.cache','craft-bundle');
const mode=process.argv[2];
if(mode==='bundle'){
  const {bundle}=await import('@remotion/bundler');
  await bundle({entryPoint:path.join(root,'src/index.ts'),outDir:serveUrl,
    onProgress:(p)=>{if(p===100)console.log('Bundle complete');}});
}else if(mode==='video'){
  const {renderMedia,selectComposition}=await import('@remotion/renderer');
  const composition=await selectComposition({serveUrl,id:'CraftStudy',timeoutInMilliseconds:120000,logLevel:'info'});
  let last=-1;
  await renderMedia({serveUrl,composition,codec:'h264',outputLocation:path.join(root,'out/craft-study.mp4'),
    isProduction:false,concurrency:1,timeoutInMilliseconds:120000,mediaCacheSizeInBytes:64*1024*1024,logLevel:'info',
    onProgress:({renderedFrames})=>{const step=Math.floor(renderedFrames/60);if(step!==last){console.log(`Rendered ${renderedFrames}/270`);last=step;}}});
  console.log('Exported out/craft-study.mp4');
}else{
  throw new Error('Use bundle or video; run in separate Node processes with --max-old-space-size=512');
}

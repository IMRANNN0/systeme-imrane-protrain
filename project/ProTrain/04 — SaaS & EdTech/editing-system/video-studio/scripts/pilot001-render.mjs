// Run bundle and video in separate processes to release bundler memory.
import {existsSync,mkdirSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const temporary = path.join(root, '.cache', 'pilot001-temp');
mkdirSync(temporary, {recursive:true});
process.env.TEMP = temporary;
process.env.TMP = temporary;
const serveUrl = path.join(root, '.cache', 'pilot001-bundle');
const mode = process.argv[2];
if (mode === 'bundle') {
  const {bundle} = await import('@remotion/bundler');
  await bundle({entryPoint:path.join(root,'src/index.ts'),outDir:serveUrl,onProgress:progress => { if(progress === 100) console.log('Pilot001 bundle complete'); }});
} else if (mode === 'video') {
  const outputLocation = path.resolve(root,process.argv[3] || 'out/ptm-p001-preview-v1.mp4');
  const relative = path.relative(path.join(root,'out'),outputLocation);
  if(relative.startsWith('..') || path.isAbsolute(relative) || existsSync(outputLocation)) throw new Error('Choose a new versioned output inside studio/out; prior exports are preserved.');
  const {renderMedia,selectComposition} = await import('@remotion/renderer');
  const composition = await selectComposition({serveUrl,id:'Pilot001',timeoutInMilliseconds:120000});
  let last = -1;
  console.log(`Pilot001: ${composition.durationInFrames} frames / ${composition.fps} fps`);
  await renderMedia({serveUrl,composition,outputLocation,
    codec:'h264',audioCodec:'aac',sampleRate:48000,pixelFormat:'yuv420p',colorSpace:'bt709',crf:18,
    // Explicit intended SDR encoding; source-image color and visual result still need QA.
    isProduction:false,concurrency:1,timeoutInMilliseconds:120000,mediaCacheSizeInBytes:256*1024*1024,
    onProgress:({renderedFrames}) => { const step = Math.floor(renderedFrames / 90); if(step !== last) {console.log(`Rendered ${renderedFrames}/${composition.durationInFrames}`);last=step;} }});
  console.log(`Exported ${outputLocation}; technical, listening and creative QA pending`);
} else {
  throw new Error('Use node --max-old-space-size=512 scripts/pilot001-render.mjs bundle, then video in a separate process.');
}

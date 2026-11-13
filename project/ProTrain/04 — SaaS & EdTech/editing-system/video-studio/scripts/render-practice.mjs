import {spawnSync} from 'node:child_process';
import {mkdirSync, openSync, closeSync, readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
// Codex sandbox temp paths may contain "!", which Webpack rejects.
const temporary = path.join(root, '.cache', 'render-temp');
mkdirSync(temporary, {recursive: true});
const choices = {
  comparison: ['PracticeComparison', 'out/practice-comparison.mp4'],
  cut: ['PracticeCut', 'out/practice-cut.mp4'],
  v2: ['PracticeComparisonV2', 'out/practice-comparison-v2.mp4'],
};
const requested = process.argv[2];
if (requested && !(requested in choices)) throw new Error('Use comparison, cut or v2');
const stills = process.argv[3] === 'stills';
if (stills && requested !== 'v2') throw new Error('Review stills currently configured for v2');
for (const [composition, output] of requested ? [choices[requested]] : [choices.comparison, choices.cut]) {
  const target = stills ? 'out/v2-stills' : output;
  const logPath = path.join(root, '.cache', `${composition}-${stills ? 'stills' : 'render'}.log`);
  const log = openSync(logPath, 'w');
  console.log(`Exporting ${composition}${stills ? ' review frames' : ''}`);
  const result = spawnSync(process.execPath, [
    'node_modules/@remotion/cli/remotion-cli.js', 'render', 'src/index.ts', composition,
    target, '--is-production=false', '--concurrency=1', '--timeout=120000', '--log=verbose',
    ...(stills ? ['--frames=0,74,75,120,210,224,225,240,270,300,360,404,405,450,539', '--image-format=png'] : []),
  ], {cwd: root, stdio: ['ignore', log, log], env: {...process.env, TEMP: temporary, TMP: temporary}});
  closeSync(log);
  if (result.error) throw result.error;
  if (result.status !== 0) {
    console.error(readFileSync(logPath,'utf8').split('\n').slice(-25).join('\n'));
    process.exit(result.status ?? 1);
  }
  console.log(`Exported ${target}`);
}

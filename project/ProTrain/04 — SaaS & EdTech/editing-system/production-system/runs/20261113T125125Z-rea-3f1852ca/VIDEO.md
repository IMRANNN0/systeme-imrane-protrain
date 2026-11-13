---
videomd: 1
name: ptm-p001-preview-v2
description: 'Made with (inferred): code / template render 89%, AI-generated video 11%'
source:
  file: ptm-p001-preview-v2.mp4
  sha256: 6f540262ea1d3e7e137c8b88d6a31c002c3e66c861752c0b77611fba7b897dcb
  duration: 38.0
  size: 1080x1920
  fps: 30.0
  aspect: '9:16'
shots: 5
lang: en
made_mix:
  code_render: 0.8921
  ai_video: 0.1079
confidence: 0.708
readers:
- tools
open_questions: 4
generator:
  name: rea-video
  version: 0.1.0
---

# ptm-p001-preview-v2.mp4

**Verdict** (inferred): Mixed production: code / template render 89% + AI-generated video 11%; overlays: animated sticker / GIF, static graphics, static sticker (composited in code / an editor); audio: voice + 21 possible sound effects (unconfirmed signal candidates); packaging: stickers / GIFs ×2, 2 possible sound effects at text / sticker pops (unconfirmed)
**Made with** (inferred, by duration): code / template render 89%, AI-generated video 11%
**Remake**: 1 AI video shot → 1 generation unit, 1 Seedance 2.0 call; code render / screen capture 4 shots → 1 code project

## Open questions

- The VLM did not run (No VLM; live action / AI / 3D are told apart from pixel statistics only, so confidence is limited. An agent that can see images: run rea-vi…
- Shot #1 (0.0–4.1s): AI or live action, to confirm: only a sharpness rhythm, no duplicate frames (re-encodes leave it too) and no AIGC label, needs an image read…
- Shot #4 (17.3–30.0s): code / template render at only 58% confidence, runner-up ai_video
- No AI listened to the soundtrack: real voice versus TTS is inferred from the waveform; the effects were picked off the mix where the sound jumps, so plosives an…

## Map

Read this page first; for detail, open only the file you need. Each line is `path | ~tokens | what is in it · when to read it`; paths are relative to this directory.

```videomd-map
video/timeline.md | 399 | Timeline: one line per shot · what a stretch says, which shots need review, how a shot was made
video/content.md | 87 | Content and structure · what it says, the narrative line, structure, the script
video/cast.md | 32 | Cast, scenes and props · reference images for characters, first-frame prompts
video/sound.md | 869 | Sound · voice, music, sound effects, beats and sources
video/look.md | 439 | Camera, lighting and editing · for filmed shots: framing, camera, lighting, kit
video/packaging.md | 354 | Packaging · subtitles, styled text, stickers, picture-in-picture: timing and style
video/remake.md | 2961 | Remake plan · generation units, shoots, code builds, real material to collect
video/shots/*.md | 368 | Per-shot detail, tokens per file on average · checking one shot: what is seen, the inference and its basis, prompts, frames
breakdown.json | 21796 | Full raw data · for programs; a model rarely needs it
shots/ | - | contact sheet, first and last frame of each shot · checking by eye
storyboard.jpg | - | storyboard of the whole video · the whole video at a glance
sfx/ | - | a clip of each sound effect · finding matching effects
packaging/ | - | subtitle files, packaging timeline, sticker frames · remaking subtitles and packaging
audio.png | - | waveform and beat chart · seeing the rhythm
```

## How to read

- One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
- `story` job in the story and the point · `seen` what is on screen · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
- Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).
- What is “seen” can be checked against the frames; what is “inferred” is the tools' and image readers' judgement, with the basis in each shot file. When they disagree, trust the frames.

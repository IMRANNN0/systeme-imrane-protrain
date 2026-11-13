---
videomd: 1
part: packaging
tokens: 342
---

## Packaging layer (subtitles / styled text / stickers / sound-effect hits)

- Stickers / GIFs: static sticker / image ×1, animated sticker / GIF ×1
- Possible SFX hits (unconfirmed signal candidates) on: sticker in ×2
- 1 persistent layers (unchanged across cuts: lay each on once for its span, not per shot): animated sticker / GIF 11.7–29.9s
- Exports: `packaging/timeline.json` (SRT is the subtitle timeline; ASS carries colour, outline, position and entrance animation, swap in the original font; timeline.json is the full timeline)

**Stickers / GIFs / picture-in-picture**

| Time | Kind | Position | Motion | Confidence | Crop |
|---|---|---|---|---|---|
| 0.30–3.60s | static sticker / image | x5% y54% w80% h9% | static | medium (appears and disappears mid-shot) | ![sticker_01](packaging/sticker_01.jpg) |
| 11.70–29.90s | animated sticker / GIF | x40% y54% w45% h6% | animated | medium (unchanged across a cut) | ![sticker_03](packaging/sticker_03.jpg) |
- 3 more things that pop up in the picture were not counted as stickers (elements appear on their own in 3D / animation / layout shots)

Remake: burn subtitles and styled text in with `packaging/overlays.ass` (ffmpeg -vf ass=overlays.ass), or rebuild them from timeline.json in CapCut / Remotion; stickers and GIFs need matching assets (meme / GIF libraries), crops are under packaging/.

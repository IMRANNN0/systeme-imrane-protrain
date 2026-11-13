---
videomd: 1
part: remake
tokens: 2950
---

## Remake plan

**1 AI video shot → 1 generation unit, 1 Seedance 2.0 call; code render / screen capture 4 shots → 1 code project**

- Grouping: AI shots in the same scene joined by hard cuts are generated in one call; ≤15s per call; consecutive hard cuts inside a unit preferably ≤8s, at most 10s; split at dissolves / fades and scene changes
- Audio: the model can generate action sound effects and ambience along with the picture; voice-over is better done as separate TTS and mixed in, so copy and timing stay editable
- Packaging: the sticker on the generated shots is post-production packaging: keep it out of the prompts, erase it from reference frames, and lay it back on from the packaging timeline after generation
- The prompts below are written generically; before generating with Seedance 2.0, rewrite them the way it expects (timing and shots, how references are addressed, dialogue, exclusions): `rea-video models seedance-2.0`

A video model can take these inputs; each generation unit below lists which ones to feed and where they come from:
- **Text prompt**: always; describes the picture, action and camera
- **First frame**: locks the composition and subject of frame one. Without it this is plain text-to-video and framing changes every time
- **Last frame**: also locks the final frame so the model only fills in between. Suits a single shot with a camera move or action
- **Reference images**: how the product and people look, so they stay the same across shots (`@图片1` in the prompt)
- **Reference video**: copy the action, camera move and rhythm, not the picture (`@视频1`); not every model takes one

### Generation units

One generation per unit. The table lists what to feed the model; open a unit for where each input comes from and the prompt.

| Unit | Shots | Time | Duration | Mode | Feed | Continuity |
|---|---|---|---|---|---|---|
| G1 | #1 | 0.0–4.1s | 4.1s | single shot | first frame + last frame | — |

**G1 · shots #1 · 4.1s · first + last frame to video**

| Input | Needed | From | Why |
|---|---|---|---|
| text prompt | yes | see the prompt below | describes picture, action and camera; every other input only constrains it |
| first frame | yes | source frame `shots/shot_001_first.jpg` (to change product, person or style, redraw it with an image model from the first-frame prompt below) | locks composition, shot size and subject position; with text alone every generation frames it differently |
| last frame | worth it | source frame `shots/shot_001_last.jpg`, treated like the first frame | the shot moves; pinning the end frame leaves the model only the in-between, so motion and the final framing stay close to the source |
| reference video | no | — | this unit locks framing with first / last frames; the model takes no reference video alongside them, so put action and camera move in the prompt |

- Shots #1 have no prompt

```text
Vertical 9:16; soft frontal light (flat light), soft light (almost no lit / shadow edge), neutral (about 5000K), background slightly soft.
(prompt missing: run --vlm or have the agent write one from the frames)
```

### Code composition

One Remotion / HTML project rebuilt from the text tracks and layout (text and UI are 100% controllable; changing copy is a data change). An LLM can write this project directly.

- Part 1: shots #2–#5 (4.1–38.0s)

Remake assets (all in the report folder; hand them over together with the data below to whoever writes the code, or to an LLM):
- `shots/shot_XXX_first.jpg` / `_last.jpg`: first / last frame of each shot at full size, for layout, type size and margins
- `shots/shot_XXX_strip.jpg`: key frames about every 0.5 s, to follow the animation
- `shots/shot_XXX_elements.jpg` and `_el_NN.jpg` / `_st_NN.jpg` / `_ly_NN.jpg`: full-size crop of every element once settled, numbered as in the motion timeline; redraw shapes from them, cut out icons, logos and illustrations that cannot be redrawn
- `packaging/overlays.ass`, `packaging/timeline.json`: timing, position and colour of the text

How to build the pictures (by the measured picture type):
- vector shapes: SVG shapes + interpolate() / spring() keyframes, positions and timing measured from the frame
- gradients / colour fields: CSS linear / radial gradients, or a few large circles with filter: blur() drifting slowly; glass cards with backdrop-filter

| Shot | Time | Build | Picture | Camera | Colours | On-screen text |
|---|---|---|---|---|---|---|
| #2 | 4.1–11.6s | vector shapes | (to fill from the images: what the elements form and how they move) | static | ground #f4f4ee · #f0a447 #0a6b47 #77a18e #4f5440 | — |
| #3 | 11.6–17.3s | vector shapes | (to fill from the images: what the elements form and how they move) | static | ground #f3f4f0 · #f9fbfe #102b22 #d5dcd8 #aab6b1 | — |
| #4 | 17.3–30.0s | vector shapes | (to fill from the images: what the elements form and how they move) | static | ground #e5c7a9 · #d5ad85 #2a402d #172e20 #096a46 | — |
| #5 | 30.0–38.0s | gradients / colour fields | (to fill from the images: what the elements form and how they move) | static | ground #0a6943 · #eea445 #77a893 #edf0eb #408568 | — |

Per-shot motion timeline (measured: positions in % of frame width / height, colours sampled once the element settles; read together with the key-frame strip)

**Motion #2 4.1–11.6s · 4 events**

- Ground #f4f4ee; other main colours #f0a447 #0a6b47 #77a18e #4f5440
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 11%–21%, y 6%–11% · #479379 · [crop](shots/shot_002_st_01.jpg)
- S2. never moves: shape / text block · x 52%–86%, y 8%–11% · #23322b · [crop](shots/shot_002_st_02.jpg)
- S3. never moves: shape / text block · x 63%–88%, y 12%–18% · #f2a440 · [crop](shots/shot_002_st_03.jpg)
- S4. never moves: shape / text block · x 70%–87%, y 20%–25% · #1c2e26 · [crop](shots/shot_002_st_04.jpg)
- S5. never moves: shape / text block · x 25%–69%, y 20%–24% · #1c3027 · [crop](shots/shot_002_st_05.jpg)
- S6. never moves: shape / text block · x 12%–84%, y 31%–39% · #086841 · [crop](shots/shot_002_st_06.jpg)
- S7. never moves: shape / text block · x 33%–38%, y 38%–39% · #086840 · [crop](shots/shot_002_st_07.jpg)
- S8. never moves: shape / text block · x 42%–49%, y 38%–39% · #086840 · [crop](shots/shot_002_st_08.jpg)
1. 4.17–4.63s · middle (x 11%–84%, y 32%–41%) · changes, linear · #ccdcd0 · [crop](shots/shot_002_el_01.jpg)
2. 4.50–4.63s · top (x 13%–84%, y 29%–30%) · appears, instant · #0d6642 · [crop](shots/shot_002_el_02.jpg)
3. 6.17–6.57s · middle (x 11%–84%, y 41%–55%) · appears, linear · #f2a440 · [crop](shots/shot_002_el_03.jpg)
4. 8.30–11.23s · middle (x 9%–89%, y 61%–65%) · disappears, ease-in-out · #cfd2ce · [crop](shots/shot_002_el_04.jpg)

**Motion #3 11.6–17.3s · 2 events**

- Ground #f3f4f0; other main colours #f9fbfe #102b22 #d5dcd8 #aab6b1
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 11%–21%, y 6%–11% · #469378 · [crop](shots/shot_003_st_01.jpg)
- S2. never moves: shape / text block · x 52%–86%, y 8%–11% · #23322b · [crop](shots/shot_003_st_02.jpg)
- S3. never moves: shape / text block · x 68%–87%, y 15%–20% · #132920 · [crop](shots/shot_003_st_03.jpg)
- S4. never moves: shape / text block · x 10%–36%, y 16%–20% · #132920 · [crop](shots/shot_003_st_04.jpg)
- S5. never moves: shape / text block · x 37%–67%, y 16%–20% · #132920 · [crop](shots/shot_003_st_05.jpg)
- S6. never moves: shape / text block · x 69%–88%, y 26%–31% · #096841 · [crop](shots/shot_003_st_06.jpg)
- S7. never moves: shape / text block · x 8%–91%, y 32%–55% · #ccdcd3 · [crop](shots/shot_003_st_07.jpg)
- S8. never moves: shape / text block · x 8%–13%, y 32%–51% · #b8c7bd · [crop](shots/shot_003_st_08.jpg)
- Continuous layer: 2% of the frame moves through the whole shot (x 9%–62%, y 32%–54%), e.g. drifting gradients, particle flow, breathing glow
1. 14.20–14.27s · middle (x 9%–89%, y 55%–61%) · appears, instant · #0f2a20 · [crop](shots/shot_003_el_01.jpg)
2. 17.27–17.33s · middle (x 9%–87%, y 57%–62%) · changes, instant · #ccd2cd · [crop](shots/shot_003_el_02.jpg)

**Motion #4 17.3–30.0s · 4 events**

- Ground #e5c7a9; other main colours #d5ad85 #2a402d #172e20 #096a46
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 0%–22%, y 0%–20% · #f1f1e6 · [crop](shots/shot_004_st_01.jpg)
- S2. never moves: shape / text block · x 25%–30%, y 0%–2% · #bd8f61 · [crop](shots/shot_004_st_02.jpg)
- S3. never moves: shape / text block · x 4%–10%, y 14%–16% · #c09262 · [crop](shots/shot_004_st_03.jpg)
- S4. never moves: shape / text block · x 8%–24%, y 21%–25% · #f6f3ee · [crop](shots/shot_004_st_04.jpg)
- S5. never moves: shape / text block · x 33%–42%, y 40%–41% · #086841 · [crop](shots/shot_004_st_05.jpg)
- S6. never moves: shape / text block · x 20%–22%, y 61%–64% · #1a301f · [crop](shots/shot_004_st_06.jpg)
- S7. never moves: shape / text block · x 9%–26%, y 91%–100% · #f2cca7 · [crop](shots/shot_004_st_07.jpg)
- In sequence: 3 same-size elements, 3.57s apart, about 0.07s each (items 1, 2, 4 below)
1. 22.63–22.70s · top (x 9%–89%, y 21%–32%) · changes, instant · #cfa77d · [crop](shots/shot_004_el_01.jpg)
2. 27.03–27.10s · top (x 9%–89%, y 19%–29%) · changes, instant · #ecd9ca · [crop](shots/shot_004_el_02.jpg)
3. 27.03–27.10s · middle (x 11%–87%, y 35%–54%) · changes, instant · #086841 · [crop](shots/shot_004_el_03.jpg)
4. 29.77–29.83s · middle (x 9%–89%, y 55%–62%) · changes, instant · #e5cbb0 · [crop](shots/shot_004_el_04.jpg)

**Motion #5 30.0–38.0s · 2 events**

- Ground #0a6943; other main colours #eea445 #77a893 #edf0eb #408568
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 8%–22%, y 5%–12% · #f5f3ee · [crop](shots/shot_005_st_01.jpg)
- S2. never moves: shape / text block · x 49%–88%, y 7%–12% · #f6f3ee · [crop](shots/shot_005_st_02.jpg)
- S3. never moves: shape / text block · x 8%–88%, y 17%–27% · #f2a440 · [crop](shots/shot_005_st_03.jpg)
- S4. never moves: shape / text block · x 68%–86%, y 34%–39% · #daf4e9 · [crop](shots/shot_005_st_04.jpg)
- S5. never moves: shape / text block · x 10%–31%, y 35%–39% · #d8f5e4 · [crop](shots/shot_005_st_05.jpg)
- S6. never moves: shape / text block · x 32%–52%, y 35%–39% · #d7f5e7 · [crop](shots/shot_005_st_06.jpg)
- S7. never moves: shape / text block · x 28%–68%, y 43%–47% · #b1ddca · [crop](shots/shot_005_st_07.jpg)
- S8. never moves: shape / text block · x 21%–76%, y 49%–54% · #a6ceba · [crop](shots/shot_005_st_08.jpg)
1. 30.20–35.67s · middle (x 9%–89%, y 55%–61%) · changes, ease-in-out · #086841 · [crop](shots/shot_005_el_01.jpg)
2. 32.53–35.67s · middle (x 9%–89%, y 61%–65%) · changes, ease-in-out · #086841 · [crop](shots/shot_005_el_02.jpg)

---
videomd: 1
part: timeline
shots: 5
tokens: 385
---

# Timeline

One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
`story` job in the story and the point · `seen` what is on screen · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).

```videomd-timeline
#01 0.0-4.1 | camera static | overlay graphic, static sticker | made~ AI-generated video 38% · runner-up 3D render 34% | material~ AI-generated | remake AI generation · G1 | flag low confidence,to confirm
#02 4.1-11.6 | camera static | made~ code / template render 82% · runner-up 3D render 10% | material~ rendered by the creator | remake code render · Part 1
#03 11.6-17.3 | camera static | transition jump cut | overlay animated sticker / GIF | made~ code / template render 75% · runner-up 3D render 12% | material~ rendered by the creator | remake code render · Part 1
#04 17.3-30.0 | camera static | overlay animated sticker / GIF | made~ code / template render 58% · runner-up AI-generated video 16% | material~ rendered by the creator | remake code render · Part 1 | flag low confidence
#05 30.0-38.0 | camera static | made~ code / template render 91% · runner-up screen recording / screenshot 3% | material~ rendered by the creator | remake code render · Part 1
```
